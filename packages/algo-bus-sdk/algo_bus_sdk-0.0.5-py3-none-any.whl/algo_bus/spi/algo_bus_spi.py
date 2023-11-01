from algo_bus.model.enum_class import ConnectionStatus
from algo_bus.model.instruction import InstructionControlRsp, InstructionReport
from algo_bus.model.order import OrderCreate, OrderCancel


class AlgoBusSPI:
    def __init__(self) -> None:
        super().__init__()

    def on_connection_change(self, connection_status: ConnectionStatus):
        """
        当连接状态发生变化时通过该接口通知算法使用方， SDK内部实现断线重连，算法使用方不需要主动重连；

        :param connection_status:
        :return:
        """
        pass

    def on_instruction_report(self, instruction_report: InstructionReport):
        """
        该方法不能阻塞，应当异步处理该回报（如果SDK内部实现了并行处理，则可以忽略该约束）

        :param instruction_report:
        :return:
        """
        pass

    def on_instruction_control_rsp(self, instruction_control_rsp: InstructionControlRsp):
        """
        标识母单控制操作是否成功

        :param instruction_control_rsp:
        :return:
        """
        pass

    def on_order_create(self, order_create: OrderCreate):
        """
        该方法不能阻塞，应当异步调用三方交易接口，完成子单创建

        :param order_create:
        :return:
        """
        pass

    def on_order_cancel(self, order_cancel: OrderCancel):
        """
        该方法不能阻塞，应当异步调用三方交易接口，完成子单撤单

        :param order_cancel:
        :return:
        """
        pass
