import json

from google.protobuf.json_format import MessageToJson


def message_to_json(message):
    message_json = MessageToJson(message, including_default_value_fields=True)
    message_json_obj = json.loads(message_json)
    return json.dumps(message_json_obj, separators=(',', ':'))
