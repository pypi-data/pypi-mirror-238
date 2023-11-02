"""Manage GDN collection streams"""
import base64
import json
import logging
import os
import time
import uuid

import pulsar
import singer
from c8 import C8Client
from prometheus_client import start_http_server, Counter
from singer import utils
from singer.catalog import CatalogEntry

from macrometa_source_collection.util import start_acknowledgment_task, MSG_ACK_BATCH_SIZE, write_to_state, \
    KEY_LAST_MSG_ID, KEY_FULL_TABLE_COMPLETED

LOGGER = singer.get_logger('macrometa_source_collection')

region_label = os.getenv("GDN_FEDERATION", "NA")
tenant_label = os.getenv("GDN_TENANT", "NA")
fabric_label = os.getenv("GDN_FABRIC", "NA")
workflow_label = os.getenv("WORKFLOW_UUID", "NA")
metric_service_url = os.getenv("METRIC_SERVICE_API")
is_metrics_enabled = os.getenv("MACROMETA_SOURCE_COLLECTION_IS_METRICS_ENABLED", 'False')


class GDNCollectionClient:
    """Client for handling GDN collection streams."""

    def __init__(self, config) -> None:
        """Init new GDN Collection Client."""
        self._host = config.get("gdn_host")
        self._fabric = config.get("fabric")
        _apikey = config.get("api_key")
        self._wf_uuid = os.getenv('WORKFLOW_UUID')
        self._collection = config.get("source_collection")
        self._cursor_batch_size = config.get("cursor_batch_size")
        self._cursor_ttl = config.get("cursor_ttl")
        self._c8_client = C8Client(
            "https",
            host=self._host,
            port=443,
            geofabric=self._fabric,
            apikey=_apikey
        )
        self._auth = pulsar.AuthenticationToken(_apikey)
        split_apikey = _apikey.rsplit(".", 2)
        self._tenant = split_apikey[0].strip() if len(split_apikey) >= 3 else "_mm"

        try:
            # try to enable collection stream on the source collection.
            self._c8_client.update_collection_properties(self._collection, has_stream=True)
        except:
            pass

        self.exported_bytes = Counter("exported_bytes", "Total number of bytes exported from GDN collections",
                                      ['region', 'tenant', 'fabric', 'workflow'])
        self.exported_documents = Counter("exported_documents",
                                          "Total number of documents exported from GDN collections",
                                          ['region', 'tenant', 'fabric', 'workflow'])
        self.export_errors = Counter("export_errors", "Total count of errors while exporting data from GDN collections",
                                     ['region', 'tenant', 'fabric', 'workflow'])
        if is_metrics_enabled.lower() == 'false':
            self.ingest_errors = Counter('ingest_errors', 'Total number of errors during ingestion',
                                         ['region', 'tenant', 'fabric', 'workflow'])
        # Start the Prometheus HTTP server for exposing metrics
        LOGGER.info("Macrometa collection source is starting the metrics server.")
        start_http_server(8000)

    def sync(self, stream: CatalogEntry, state):
        """Return documents in target GDN collection as records."""
        LOGGER.info(f"Found State: {state}")
        if self._c8_client.has_collection(self._collection):
            self.send_schema_message(stream)
            LOGGER.info("Schema properties: %s", stream.schema.to_dict().get("properties"))
            # When subscribed to a topic, the Pulsar client may output some log messages to stdout.
            # However, Meltano tap/target processes these log messages as input singer records,
            # which can lead to unexpected behavior.
            # To prevent this issue, we disable Pulsar logging here to ensure a clean data flow.
            _pulsar_logger = logging.getLogger("pulsar-logger")
            _pulsar_logger.setLevel(logging.CRITICAL)
            _pulsar_logger.addHandler(logging.NullHandler())

            # Create a consumer beforehand to capture changes done while loading existing data
            _pulsar_client = pulsar.Client(
                f"pulsar+ssl://{self._host}:6651/",
                authentication=self._auth,
                tls_allow_insecure_connection=False,
                logger=_pulsar_logger,
            )
            _sub_name = self._wf_uuid if self._wf_uuid else f"cs_{uuid.uuid1()}"
            _topic = f"persistent://{self._tenant}/c8local.{self._fabric}/{self._collection}"
            _consumer: pulsar.Consumer = _pulsar_client.subscribe(
                _topic, _sub_name, initial_position=pulsar.InitialPosition.Earliest)

            # Initiate full table sync
            full_table_completed = singer.get_bookmark(state, self._collection, KEY_FULL_TABLE_COMPLETED)
            if full_table_completed:
                LOGGER.info("Full table sync already completed.")
            else:
                LOGGER.info("Full table sync started.")
                self.load_existing_data(stream, stream.schema)
                full_table_completed = True
                state = write_to_state(state, self._collection, KEY_FULL_TABLE_COMPLETED, full_table_completed)
                LOGGER.info("Full table sync completed.")

            # Initiate CDC sync
            LOGGER.info("CDC sync started.")
            start_acknowledgment_task(self._collection, _consumer)
            un_ack_msgs = 0
            while True:
                try:
                    msg = _consumer.receive()
                    time_extracted = utils.now()
                    data = msg.data()
                    if data is None or not data:
                        continue
                    props = msg.properties()
                    j = json.loads(data.decode("utf8"))
                    j.pop('_id', None)
                    j.pop('_rev', None)
                    record_sent = False
                    if props["op"] == "INSERT" or props["op"] == "UPDATE":
                        # skip inserts not having valid schema
                        if self._is_conforming_to_schema(j, stream.schema):
                            j['_sdc_deleted_at'] = None
                            singer_record = self.msg_to_singer_message(stream, j, None, time_extracted)
                            singer.write_message(singer_record)
                            record_sent = True
                    elif props["op"] == "DELETE":
                        # Currently, we don't have a way to validate schema here
                        j.pop('_delete', None)
                        j['_sdc_deleted_at'] = singer.utils.strftime(utils.now())
                        singer_record = self.msg_to_singer_message(stream, j, None, time_extracted)
                        singer.write_message(singer_record)
                        record_sent = True

                    if record_sent:
                        un_ack_msgs += 1
                        if un_ack_msgs == MSG_ACK_BATCH_SIZE:
                            # Convert the byte representation of the message ID to a Base64-encoded string
                            msg_id_base64 = base64.b64encode(msg.message_id().serialize()).decode('utf-8')
                            state = write_to_state(state, self._collection, KEY_LAST_MSG_ID, msg_id_base64)
                            un_ack_msgs = 0
                        if is_metrics_enabled.lower() == 'true':
                            self.exported_bytes.labels(region_label, tenant_label, fabric_label, workflow_label).inc(
                                len(json.dumps(j)))
                            self.exported_documents.labels(region_label, tenant_label, fabric_label,
                                                           workflow_label).inc()
                except Exception as e:
                    LOGGER.warn(f"Exception occurred: {e}")
                    if is_metrics_enabled.lower() == 'false':
                        self.ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                    else:
                        self.export_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                    raise e
        else:
            raise FileNotFoundError("Collection {} not found".format(self._collection))

    def load_existing_data(self, stream, schema_properties):
        cursor = self._c8_client._fabric.c8ql.execute(f"FOR d IN @@collection RETURN d",
                                                      bind_vars={"@collection": self._collection}, stream=True,
                                                      batch_size=self._cursor_batch_size, ttl=self._cursor_ttl)
        try:
            while (not cursor.empty()) or cursor.has_more():
                rec = cursor.next()
                time_extracted = utils.now()
                rec.pop('_id', None)
                rec.pop('_rev', None)
                # skip existing data not having valid schema
                if self._is_conforming_to_schema(rec, schema_properties):
                    singer_record = self.msg_to_singer_message(stream, rec, None, time_extracted)
                    start_time = time.time()
                    singer.write_message(singer_record)
                    end_time = time.time()
                    if end_time - start_time > 10:
                        LOGGER.warn(f"Took {end_time - start_time}seconds to write record:{singer_record}")
                    if is_metrics_enabled.lower() == 'true':
                        self.exported_bytes.labels(region_label, tenant_label, fabric_label, workflow_label).inc(
                            len(json.dumps(rec)))
                        self.exported_documents.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
        except Exception as e:
            time.sleep(100)
            raise e

    def send_schema_message(self, stream: CatalogEntry, bookmark_properties=[]):
        schema_message = singer.SchemaMessage(stream=stream.stream,
                                              schema=stream.schema.to_dict(),
                                              key_properties=stream.key_properties,
                                              bookmark_properties=bookmark_properties)
        singer.write_message(schema_message)

    def msg_to_singer_message(self, stream, msg, version, time_extracted):
        return singer.RecordMessage(
            stream=stream.stream,
            record=msg,
            version=version,
            time_extracted=time_extracted
        )

    def _is_conforming_to_schema(self, rec: dict, schema: CatalogEntry) -> bool:
        """
        Checks if record conforms to provided schema.

        Parameters:
            rec (dict): Record to check for conformity
            schema (CatalogEntry): Schema definition in singer format
        """
        properties = schema.properties
        columns = self._get_columns(properties)

        if len(rec.keys() ^ columns) == 0 and all(
            rec[key] is None
            or (
                isinstance(properties[key].type, list)
                and get_singer_data_type(rec[key]) in properties[key].type
            )
            or (
                isinstance(properties[key].type, str)
                and get_singer_data_type(rec[key]) == properties[key].type
            )
            for key in rec.keys()
        ):
            return True

        LOGGER.warn(
            "The schema of the record: %s, does not match the current schema. Skipping it..",
            json.dumps(rec)
        )
        return False

    def _get_columns(self, properties: dict) -> list:
        columns = list(properties.keys())
        columns.remove("_sdc_deleted_at")
        return columns

def get_singer_data_type(val):
    if val is None:
        return "null"
    elif type(val) == str:
        return "string"
    elif type(val) == int:
        return "integer"
    elif type(val) == float:
        return "number"
    elif type(val) == bool:
        return "boolean"
    elif type(val) == list:
        return "array"
    else:
        return "object"
