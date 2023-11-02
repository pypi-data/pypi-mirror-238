"""GDN data connector source for GDN Collections."""
import time
from collections import defaultdict
from urllib.parse import urlparse

import pkg_resources
import singer
from c8 import C8Client
from c8connector import C8Connector, Sample, ConfigProperty, ConfigAttributeType, Schema, SchemaAttributeType, \
    SchemaAttribute, ValidationException
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema as SingerSchema

from macrometa_source_collection.client import GDNCollectionClient, get_singer_data_type

LOGGER = singer.get_logger('macrometa_source_collection')

REQUIRED_CONFIG_KEYS = [
    'gdn_host',
    'fabric',
    'api_key',
    'source_collection'
]


class GDNCollectionSourceConnector(C8Connector):
    """GDNCollectionSourceConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "Macrometa Collection"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-source-collection"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_source_collection').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "source"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Source data from a Macrometa collection."

    def logo(self) -> str:
        """Returns the logo image for the connector."""
        return ""

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        try:
            config = self.get_config(integration)
            cursor_batch_size = int(config["cursor_batch_size"])
            if not 0 < cursor_batch_size <= 1024:
                raise ValidationException(f"Invalid `cursor_batch_size` value `{cursor_batch_size}` provided.")
            cursor_ttl = int(config["cursor_ttl"])
            if not 30 <= cursor_ttl <= 120:
                raise ValidationException(f"Invalid `cursor_ttl` value `{cursor_ttl}` provided.")
            C8Client(
                "https",
                host=config["gdn_host"],
                port=443,
                geofabric=config["fabric"],
                apikey=config["api_key"]
            ).collection(config["source_collection"])
        except Exception as e:
            raise ValidationException(e)

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        schema = {}
        data = []
        try:
            config = self.get_config(integration)
            schema, data = get_schema_and_data(C8Client(
                "https",
                host=config["gdn_host"],
                port=443,
                geofabric=config["fabric"],
                apikey=config["api_key"]
            ), config["source_collection"], 50)
        except Exception as e:
            raise ValidationException(e)
        data = data[:10]
        return [Sample(
            schema=Schema(config["source_collection"],
                          [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()]),
            data=data
        )]

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        schema = {}
        try:
            config = self.get_config(integration)
            schema, _ = get_schema_and_data(C8Client(
                "https",
                host=config["gdn_host"],
                port=443,
                geofabric=config["fabric"],
                apikey=config["api_key"]
            ), config["source_collection"], 50)
        except Exception as e:
            raise ValidationException(e)
        return [Schema(config["source_collection"],
                       [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()])]

    def reserved_keys(self) -> list[str]:
        """List of reserved keys for the connector."""
        return []

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('gdn_host', 'GDN Host', ConfigAttributeType.STRING, True, False,
                           description='Fully qualified GDN Host URL (note: Use Region URL for Local collections).',
                           placeholder_value='sample-dxb.paas.macrometa.io'),
            ConfigProperty('api_key', 'API Key', ConfigAttributeType.PASSWORD, True, False,
                           description='API key.',
                           placeholder_value='my_apikey'),
            ConfigProperty('fabric', 'Fabric', ConfigAttributeType.STRING, True, False,
                           description='Fabric name.',
                           default_value='_system'),
            ConfigProperty('source_collection', 'Source Collection', ConfigAttributeType.STRING, True, True,
                           description='Source collection name.',
                           placeholder_value='my_collection'),
            ConfigProperty('cursor_batch_size', 'Cursor Batch Size', ConfigAttributeType.INT, False, True,
                           description='Cursor batch size when retrieving records from GDN (a value between 1-1024).',
                           default_value='100'),
            ConfigProperty('cursor_ttl', 'Cursor TTL', ConfigAttributeType.INT, False, True,
                           description='Cursor TTL (time to live) in seconds when retrieving records from GDN '
                                       '(a value between 30-120).',
                           default_value='30')
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return ['catalog', 'discover', 'state']

    @staticmethod
    def get_config(integration: dict) -> dict:
        try:
            return {
                # Required config keys
                'gdn_host': extract_gdn_host(integration['gdn_host']),
                'api_key': integration['api_key'],
                'fabric': integration['fabric'],
                'source_collection': integration['source_collection'],

                # Optional config keys
                'cursor_batch_size': integration.get('cursor_batch_size', 100),
                'cursor_ttl': integration.get('cursor_ttl', 30)
            }
        except KeyError as e:
            raise ValidationException(f'Integration property `{e}` not found.') from e


def get_schema_and_data(client: C8Client, collection: str, sample_size: int, workflow_run=False):
    cursor = None
    schema_counts = defaultdict(int)
    records_by_schema = defaultdict(list)
    LOGGER.info("Determining schema..")
    while cursor is None or cursor.empty():
        cursor = client.execute_query(f"FOR d IN @@collection LIMIT 0, @count RETURN d",
                                      bind_vars={"@collection": collection, "count": sample_size})
        if cursor.empty():
            if workflow_run:
                LOGGER.info("Cannot determine schema as no records found in collection. Retrying after 30 seconds..")
                time.sleep(30)
            else:
                raise Exception("Cannot determine schema as no records found in collection.")

    while not cursor.empty():
        rec = cursor.next()
        rec.pop('_id', None)
        rec.pop('_rev', None)
        # Skip empty records or records with no keys
        if not rec or not rec.keys():
            continue

        schema_keys = rec.keys()
        schema = tuple((k, get_singer_data_type(rec[k])) for k in schema_keys)
        schema_counts[schema] += 1
        records_by_schema[schema].append(rec)

    schema = {"data": "object"}
    data = []
    if schema_counts:
        # Get the most common schema
        most_common_schema = max(schema_counts, key=schema_counts.get)
        schema = dict(most_common_schema)

        # Get the list of records associated with the most common schema
        data = records_by_schema[most_common_schema]
    return schema, data


def get_attribute_type(source_type: str) -> SchemaAttributeType:
    if source_type == 'string':
        return SchemaAttributeType.STRING
    elif source_type == 'integer':
        return SchemaAttributeType.LONG
    elif source_type == 'boolean':
        return SchemaAttributeType.BOOLEAN
    elif source_type == 'number':
        return SchemaAttributeType.DOUBLE
    else:
        return SchemaAttributeType.OBJECT


def do_discovery(config, workflow_run=False):
    collection_name = config['source_collection']
    schema, _ = get_schema_and_data(C8Client(
        "https",
        host=config["gdn_host"],
        port=443,
        geofabric=config["fabric"],
        apikey=config["api_key"]
    ), collection_name, 50, workflow_run)
    schema_properties = {
        k: SingerSchema(
            type=['null', 'string', 'integer', 'number', 'boolean', 'array', 'object'] if v == 'null' else (
                v if k == '_key' else ['null', v]),
            maxLength=255 if v == 'string' and k == '_key' else None,
            format=None
        )
        for k, v in schema.items()
    }
    # inject `_sdc_deleted_at` prop to the schema.
    schema_properties['_sdc_deleted_at'] = SingerSchema(type=['null', 'string'], format='date-time')
    singer_schema = SingerSchema(type='object', properties=schema_properties)
    catalog = Catalog([CatalogEntry(
        table=collection_name,
        stream=collection_name,
        tap_stream_id=collection_name,
        schema=singer_schema,
        key_properties=["_key"]
    )])
    dump_catalog(catalog)
    return catalog


def dump_catalog(catalog: Catalog):
    catalog.dump()


def do_sync(conn_config, catalog: Catalog, state):
    gdn_client = GDNCollectionClient(conn_config)
    gdn_client.sync(catalog.streams[0], state)


def extract_gdn_host(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        resource_name = parsed_url.netloc.strip()
    else:
        resource_name = parsed_url.path.strip()
    if not resource_name.startswith("api-"):
        resource_name = "api-" + resource_name
    return resource_name


def main_impl():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    conn_config = {'api_key': args.config['api_key'],
                   'gdn_host': extract_gdn_host(args.config['gdn_host']),
                   'fabric': args.config['fabric'],
                   'source_collection': args.config['source_collection']}

    if args.discover:
        do_discovery(conn_config, workflow_run=True)
    elif args.catalog:
        state = args.state or {}
        do_sync(conn_config, args.catalog, state)
    else:
        LOGGER.info("No properties were selected")
    return


def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc

if __name__ == "__main__":
    main()
