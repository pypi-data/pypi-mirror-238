import datetime
import json
from enum import Enum

from _decimal import Decimal

from algo_bus.model.enum_class import Exchange, OrderSide, OrderStatus, FillStatus, ReportType, OrderPriceType, InstructionStatus


class Message:
    def __init__(self):
        self.messageType: MessageType = MessageType.UNDEFINED

    def __str__(self) -> str:
        return json.dumps(self, cls=CustomEncoder, ensure_ascii=False)

    def __repr__(self) -> str:
        return json.dumps(self, cls=CustomEncoder, ensure_ascii=False)

    def load_from_json(self, message):
        if type(message) == str:
            json_dict = json.loads(message)
        elif type(message) == dict:
            json_dict = message
        else:
            raise TypeError("message type must be str or dict")
        for key in json_dict:
            if hasattr(self, key):
                if key == "messageType":
                    setattr(self, key, MessageType[json_dict[key]])
                elif key == "exchange":
                    setattr(self, key, Exchange[json_dict[key]])
                elif key == "orderSide":
                    setattr(self, key, OrderSide[json_dict[key]])
                elif key == "orderStatus":
                    setattr(self, key, OrderStatus[json_dict[key]])
                elif key == "fillStatus":
                    setattr(self, key, FillStatus[json_dict[key]])
                elif key == "reportType":
                    setattr(self, key, ReportType[json_dict[key]])
                elif key == "transactTime" or key == "placedTime":
                    setattr(self, key, datetime.time.fromisoformat(json_dict[key]) if json_dict[key] and json_dict[key] != "None" else None)
                else:
                    setattr(self, key, json_dict[key])


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (Exchange, OrderSide, MessageType, OrderStatus, OrderPriceType, InstructionStatus, FillStatus, ReportType)):
            return str(o.name)
        if isinstance(o, datetime.time):
            return str(o.strftime("%H:%M:%S.%f")[:-3])
        if isinstance(o, Decimal):
            return str(o)
        return {attr: getattr(o, attr) for attr in dir(o) if attr[0] != '_' and callable(getattr(o, attr)) is False}


class MessageType(Enum):
    UNDEFINED = "UNDEFINED"
    HEARTBEAT = "HEARTBEAT"
    INSTRUCTION_CREATE = "INSTRUCTION_CREATE"
    INSTRUCTION_REPORT = "INSTRUCTION_REPORT"

    INSTRUCTION_CONTROL = "INSTRUCTION_CONTROL"
    INSTRUCTION_CONTROL_RSP = "INSTRUCTION_CONTROL_RSP"

    CANCEL_PARENT_ORDER = "CANCEL_PARENT_ORDER"

    ORDER_CREATE = "ORDER_CREATE"
    ORDER_CREATE_REPORT = "ORDER_CREATE_REPORT"

    ORDER_CANCEL = "ORDER_CANCEL"
    ORDER_CANCEL_REPORT = "ORDER_CANCEL_REPORT"

    ORDER_FILL_REPORT = "ORDER_FILL_REPORT"

    ERROR_RESPONSE = "ERROR_RESPONSE"


class AppLogin(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.CREATE_PARENT_ORDER_REQUEST
        self.algoAppId: str = ""
        self.algoAppKey: str = ""
