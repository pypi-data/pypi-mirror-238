from enum import Enum


class InstructionStatus(Enum):
    ALGO_STATUS_UNDEFINED = 0
    ALGO_STATUS_CREATED = 1
    ALGO_STATUS_STARTED = 2
    ALGO_STATUS_STOPPED = 3
    ALGO_STATUS_FAILED = 4
    ALGO_STATUS_SUSPENDED = 5


class OrderPriceType(Enum):
    PRICE_TYPE_LIMIT = 0


class ConnectionStatus(Enum):
    CONNECTED = 0
    DISCONNECTED = 1


class OrderSide(Enum):
    ORDER_SIDE_UNDEFINED = 0
    ORDER_SIDE_BUY = 1
    ORDER_SIDE_SELL = 2


class ControlType(Enum):
    UNDEFINED = 0
    CANCEL = 1
    SUSPEND = 2
    RESUME = 3


class OrderStatus(Enum):
    ORDER_STATUS_UNDEFINED = 0
    ORDER_STATUS_PLACING = 1
    ORDER_STATUS_PLACED = 2
    ORDER_STATUS_PARTIAL_FILLED = 3
    ORDER_STATUS_FILLED = 4
    ORDER_STATUS_CANCELLING = 5
    ORDER_STATUS_CANCELLED = 6
    ORDER_STATUS_PARTIAL_CANCELLING = 7
    ORDER_STATUS_PARTIAL_CANCELLED = 8
    ORDER_STATUS_FAILED = 9


class ReportType(Enum):
    ORDER = "ORDER"
    FILL = "FILL"
    CANCEL = "CANCEL"


class Exchange(Enum):
    EXCHANGE_UNDEFINED = 0
    EXCHANGE_SH_A = 1
    EXCHANGE_SZ_A = 2
    EXCHANGE_HK = 3
    EXCHANGE_SK = 4
    EXCHANGE_BJ = 5


class FillStatus(Enum):
    FILL_STATUS_UNDEFINED = 0
    FILL_STATUS_FILLED = 1
    FILL_STATUS_CANCELLED = 2
    FILL_STATUS_FAILED = 3
