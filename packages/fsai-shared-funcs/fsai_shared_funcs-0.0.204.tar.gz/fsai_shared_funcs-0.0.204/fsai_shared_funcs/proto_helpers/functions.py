from datetime import datetime

from ..time_helper import get_pb_ts_from_datetime


def dict_to_proto(dictionary, protobuf_message, field_types_mapping=None):
    if field_types_mapping is None:
        field_types_mapping = {}

    # Iterate over the key-value pairs in the dictionary
    for key, value in dictionary.items():
        # Check if the value is a datetime
        if isinstance(value, datetime):
            # Convert datetime to protobuf timestamp and set it using CopyFrom
            getattr(protobuf_message, key).CopyFrom(get_pb_ts_from_datetime(value))
        # Check if the value is a dictionary
        elif key in field_types_mapping and isinstance(value, dict):
            # If the key is in the mapping and the value is a dictionary, create a nested protobuf message of the specified type
            nested_message = field_types_mapping[key]
            getattr(protobuf_message, key).CopyFrom(
                dict_to_proto(value, nested_message, field_types_mapping)
            )
        else:
            # Set the field value in the Protobuf message
            setattr(protobuf_message, key, value)

    return protobuf_message
