import base64
import copy
import json
import threading
import time

import pulsar
import singer
from c8connector.util import state_file_dir

LOGGER = singer.get_logger('macrometa_source_collection')
MSG_ACK_INTERVAL = 60  # seconds
MSG_ACK_BATCH_SIZE = 1000
KEY_LAST_MSG_ID = "last_msg_id"
KEY_FULL_TABLE_COMPLETED = "full_table_completed"


def write_to_state(state, collection, key, value):
    """
    Write the specified value to the state JSON for a specific collection and key.

    This function updates the state JSON by writing the provided value to the specified collection and key.
    Additionally, it creates a StateMessage with the updated state value and writes it to the singer messages.

    Parameters:
        state (dict): The current state JSON representing the bookmarked messages.
        collection (str): The name of the collection to which the value is associated.
        key (str): The key under which the value is stored within the collection.
        value (Any): The value to be stored in the state JSON.

    Returns:
        dict: The updated state JSON after writing the value to the specified collection and key.
    """
    state = singer.write_bookmark(state, collection, key, value)
    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))
    return state


def retrieve_last_message_id_from_state(collection: str):
    """
    Retrieve the last processed message ID from the state.json file.

    Parameters:
        collection (str): The name of the collection for which to retrieve the message ID.

    Returns:
        pulsar.MessageId or None: The last processed message ID or None if not found.
    """
    try:
        with open(f"{state_file_dir}/state.json", "r") as state_file:
            state = json.load(state_file)
            if state:
                bookmark = state.get("bookmarks", {}).get(collection, {})
                last_msg_id_bytes = bookmark.get(KEY_LAST_MSG_ID, None)
                if last_msg_id_bytes:
                    # Decode the Base64-encoded string back to bytes
                    msg_id_bytes = base64.b64decode(last_msg_id_bytes)
                    return pulsar.MessageId.deserialize(msg_id_bytes)
                else:
                    return None
            else:
                return None
    except FileNotFoundError:
        LOGGER.warning(f"state.json file not found in {state_file_dir}.")
        return None
    except Exception as e:
        LOGGER.error(f"Couldn't retrieve `{KEY_LAST_MSG_ID}` from state. Error: {e}")
        return None


def acknowledge_messages_periodically(collection: str, consumer: pulsar.Consumer):
    """
    Periodically acknowledge Pulsar messages up to the last processed message ID.

    This method runs in a separate thread, acknowledging messages every 1 minute.

    Parameters:
        collection (str): The name of the collection for which to acknowledge messages.
        consumer (pulsar.Consumer): The Pulsar consumer instance.
    """
    while True:
        acknowledge_up_to_last_message(collection, consumer)
        time.sleep(MSG_ACK_INTERVAL)


def acknowledge_up_to_last_message(collection: str, consumer: pulsar.Consumer):
    """
    Acknowledge Pulsar messages up to the last processed message ID.

    Parameters:
        collection (str): The name of the collection for which to acknowledge messages.
        consumer (pulsar.Consumer): The Pulsar consumer instance.
    """
    try:
        last_msg_id = retrieve_last_message_id_from_state(collection)
        if last_msg_id:
            consumer.acknowledge_cumulative(last_msg_id)
    except Exception as e:
        LOGGER.error(f"Couldn't acknowledge last processed message id. Error: {e}")


def start_acknowledgment_task(collection: str, consumer: pulsar.Consumer):
    """
    Start the acknowledgment task for periodically acknowledging Pulsar messages.

    Parameters:
        collection (str): The name of the collection for which to acknowledge messages.
        consumer (pulsar.Consumer): The Pulsar consumer instance.
    """
    acknowledge_up_to_last_message(collection, consumer)
    ack_thread = threading.Thread(target=acknowledge_messages_periodically, args=(collection, consumer))
    ack_thread.start()
