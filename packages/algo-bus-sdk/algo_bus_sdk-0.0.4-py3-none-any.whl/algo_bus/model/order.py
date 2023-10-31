import datetime
import time
import uuid

from algo_bus.dtp import api_pb2 as dtp_api, type_pb2 as dtp_type
from algo_bus.model import Message, MessageType
from algo_bus.model.enum_class import Exchange, OrderSide, OrderStatus, FillStatus, OrderPriceType


class OrderCreate(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.ORDER_CREATE
        self.instructionId: str = ""
        self.orderId: str = ""
        self.code: str = ""
        self.exchange: Exchange = Exchange.EXCHANGE_UNDEFINED
        self.quantity: int = 0
        self.price: float = 0.0
        self.orderPriceType: OrderPriceType = OrderPriceType.PRICE_TYPE_LIMIT
        self.orderSide: OrderSide = OrderSide.ORDER_SIDE_UNDEFINED
        self.transactTime: datetime.time = None

    def to_dtp_place_message(self, account_no):
        place_header = dtp_api.RequestHeader()
        place_header.api_id = dtp_type.APP_ID_PLACE_ORDER
        place_header.request_id = str(uuid.uuid4())
        place_header.account_no = account_no
        place_header.ip = "ip"
        place_header.mac = "mac"
        place_header.harddisk = "harddisk"

        place_body = dtp_api.PlaceOrder()
        place_body.account_no = account_no
        place_body.order_original_id = self.orderId
        place_body.exchange = self.exchange.value
        place_body.code = self.code
        place_body.price = str(self.price)
        place_body.quantity = self.quantity
        place_body.order_side = self.orderSide.value
        place_body.order_type = dtp_type.ORDER_TYPE_LIMIT
        return place_header, place_body


class OrderCreateReport(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.ORDER_CREATE_REPORT
        self.orderId: str = ""
        self.code: str = ""
        self.exchange: Exchange = Exchange.EXCHANGE_UNDEFINED
        self.quantity: int = 0
        self.price: float = 0.0
        self.orderExchangeId: str = ""
        self.orderPriceType: OrderPriceType = OrderPriceType.PRICE_TYPE_LIMIT
        self.orderSide: OrderSide = OrderSide.ORDER_SIDE_UNDEFINED
        self.orderStatus: OrderStatus = OrderStatus.ORDER_STATUS_UNDEFINED
        self.placedTime: datetime.time = None

    def load_from_dtp(self, report):
        (report_header, report_body) = report
        self.orderId = report_body.order_original_id
        self.code = report_body.code
        self.exchange = Exchange(report_body.exchange)
        self.quantity = report_body.quantity
        self.price = float(report_body.price)
        self.orderExchangeId = report_body.order_exchange_id
        self.orderPriceType = OrderPriceType.PRICE_TYPE_LIMIT
        self.orderSide = OrderSide(report_body.order_side)
        self.orderStatus = OrderStatus(report_body.status)
        self.placedTime = report_body.placed_time


class OrderFillReport(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.ORDER_FILL_REPORT
        self.orderId: str = ""
        self.code: str = ""
        self.exchange: str = ""
        self.quantity: int = 0
        self.price: float = 0.0
        self.fillExchangeId: str = ""
        self.fillPrice: float = 0.0
        self.fillQuantity: int = 0
        self.fillTime: datetime.time = None
        self.fillStatus: FillStatus = FillStatus.FILL_STATUS_UNDEFINED
        self.fillAmount: float = 0.0
        self.totalFillQuantity: int = 0
        self.totalFillAmount: float = 0.0
        self.totalCancelledQuantity: int = 0

    def load_from_dtp(self, report):
        (report_header, report_body) = report
        self.orderId = report_body.order_original_id
        self.code = report_body.code
        self.exchange = Exchange(report_body.exchange)
        self.quantity = report_body.quantity
        self.price = float(report_body.price)
        self.fillExchangeId = report_body.fill_exchange_id
        self.fillPrice = float(report_body.fill_price)
        self.fillQuantity = report_body.fill_quantity
        self.fillTime = report_body.fill_time
        self.fillStatus = FillStatus(report_body.fill_status)
        self.fillAmount = float(report_body.fill_amount)
        self.totalFillQuantity = report_body.total_fill_quantity
        self.totalFillAmount = float(report_body.total_fill_amount)
        self.totalCancelledQuantity = report_body.total_cancelled_quantity


class OrderCancelReport(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.ORDER_CANCEL_REPORT
        self.orderId: str = ""
        self.code: str = ""
        self.exchange: str = ""
        self.quantity: int = 0
        self.totalFillQuantity: int = 0
        self.cancelledQuantity: int = 0

    def load_from_dtp(self, report: dtp_api.PlacedReport):
        (report_header, report_body) = report
        self.orderId = report_body.order_original_id
        self.code = report_body.code
        self.exchange = Exchange(report_body.exchange)
        self.quantity = report_body.quantity
        self.totalFillQuantity = 0
        self.cancelledQuantity = report_body.cancelled_quantity


class OrderCancel(Message):
    def __init__(self):
        super().__init__()
        self.messageType = MessageType.ORDER_CANCEL
        self.instructionId: str = ""
        self.orderId: str = ""
        self.code: str = ""
        self.exchange: Exchange = Exchange.EXCHANGE_UNDEFINED
        self.orderExchangeId: str = ""
        self.transactTime: datetime.time = None

    def to_dtp_cancel_message(self):
        place_header = dtp_api.RequestHeader()
        place_header.api_id = dtp_type.APP_ID_CANCEL_ORDER
        place_header.request_id = str(uuid.uuid4())
        account_no = "123"
        place_header.account_no = account_no
        place_header.ip = "ip"
        place_header.mac = "mac"
        place_header.harddisk = "harddisk"

        cancel_body = dtp_api.CancelOrder()
        cancel_body.account_no = account_no
        cancel_body.exchange = self.exchange.value
        cancel_body.code = self.code
        cancel_body.order_exchange_id = self.orderExchangeId
        return place_header, cancel_body


class OrderCancelRsp(Message):
    def __init__(self):
        super().__init__()
        self.orderId: str = ""
        self.errCode: int = 0
        self.errMsg: str = ""
