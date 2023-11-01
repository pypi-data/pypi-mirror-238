import datetime
from typing import List

from algo_bus.model import Message, MessageType
from algo_bus.model.enum_class import Exchange, OrderSide, ControlType, InstructionStatus


class InstructionCreate(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.INSTRUCTION_CREATE
        self.localInstructionId: str = ""
        self.code: str = ""
        self.orderSide: OrderSide = OrderSide.ORDER_SIDE_UNDEFINED
        self.exchange: Exchange = Exchange.EXCHANGE_UNDEFINED
        self.quantity: int = 0
        self.amount: float = 0.0
        self.transactTime: datetime.time = datetime.datetime.now().time()
        self.startTime: str = ""
        self.endTime: str = ""
        self.algoCode: str = ""
        self.algoParam: str = ""


class InstructionReport(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.INSTRUCTION_REPORT
        self.localInstructionId: str = ""
        self.instructionId: str = ""
        self.code: str = ""
        self.orderSide: OrderSide = OrderSide.ORDER_SIDE_UNDEFINED
        self.exchange: Exchange = Exchange.EXCHANGE_UNDEFINED
        self.quantity: int = 0
        self.amount: float = 0.0
        self.transactTime: datetime.time = datetime.datetime.now().time()
        self.startTime: str = ""
        self.endTime: str = ""
        self.algoCode: str = ""
        self.algoParam: str = ""
        self.filledQuantity: int = 0
        self.placingQuantity: int = 0
        self.filledAmount: float = 0.0
        self.instructionStatus: InstructionStatus = InstructionStatus.ALGO_STATUS_UNDEFINED
        self.statusMessage: str = ""


class InstructionControl(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.INSTRUCTION_CONTROL
        self.instructionId: str = ""
        self.controlType: ControlType = ControlType.UNDEFINED


class InstructionControlRsp(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.INSTRUCTION_CONTROL_RSP
        self.instructionId: str = ""
        self.errCode: int = 0
        self.errMsg: str = ""
        self.transactTime: datetime.time = datetime.datetime.now().time()


class InstructionQuery(Message):
    def __init__(self):
        super().__init__()
        self.instructionId: List[str] = []
        self.startTime: str = ""
        self.endTime: str = ""
        self.instructionStatus: List[InstructionStatus] = []
        self.orderSide: OrderSide = OrderSide.ORDER_SIDE_UNDEFINED


class Pagination:
    def __init__(self):
        super().__init__()
        self.pageSize: int = 0
        self.pageNum: int = 0
