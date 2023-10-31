import json
import threading
import time
import traceback
from typing import List

import requests
from websocket import ABNF

from algo_bus.logger import get_algo_bus_logger
from algo_bus.model import MessageType, AppLogin
from algo_bus.model.enum_class import ConnectionStatus
from algo_bus.model.instruction import InstructionReport, InstructionControl, InstructionCreate
from algo_bus.model.order import OrderCancel, OrderCreate, OrderCreateReport, OrderFillReport, OrderCancelReport, OrderCancelRsp
from algo_bus.spi.algo_bus_spi import AlgoBusSPI
from algo_bus.ws.websocket_client import WebsocketClient


class AlgoBusApi(threading.Thread):
    def __init__(self, config: dict, logger=None) -> None:
        super(AlgoBusApi, self).__init__()
        self.algo_bus_spi: AlgoBusSPI = None
        ssl = config['ssl']
        algo_bus_address = config['algo_bus_address']

        self.http_url = "https://" if ssl else "http://" + algo_bus_address + config['http_endpoint']

        ws_algo_bus_address = "wss://" if ssl else "ws://" + algo_bus_address + config['ws_endpoint']
        client_id = config['client_id']
        client_secret = config['client_secret']
        self.ws_url = ws_algo_bus_address + "?clientId=" + client_id + "&clientSecret=" + client_secret
        self.ws = None
        self.init_ws()
        self.logger = logger if logger else get_algo_bus_logger()

    def init_ws(self):
        self.ws = WebsocketClient(url=self.ws_url, on_open=self.on_open, on_data=self.on_data, on_error=self.on_error, on_close=self.on_close)

    def register_spi(self, algo_bus_spi: AlgoBusSPI):
        self.algo_bus_spi = algo_bus_spi

    def on_open(self, ws):
        self.logger.debug("[AlgoBusApi] ws on_open")
        if self.ws and self.ws.sock and self.ws.sock.connected:
            if self.algo_bus_spi:
                self.algo_bus_spi.on_connection_change(ConnectionStatus.CONNECTED)
            else:
                self.logger.debug("[AlgoBusApi] not register spi, not callback on_connection_change")

    def on_data(self, ws, data: str, data_type: ABNF, continue_flag):
        self.logger.debug(f"[AlgoBusApi] on_data: {data}")
        try:
            if data_type is ABNF.OPCODE_TEXT:
                response_json = json.loads(data)
                message_type = MessageType[response_json['messageType']]
                if message_type == MessageType.HEARTBEAT:
                    self.logger.info("[AlgoBusApi] heartbeat")
                    return
                elif message_type == MessageType.INSTRUCTION_REPORT:
                    parent_order = InstructionReport()
                    parent_order.load_from_json(data)
                    self.algo_bus_spi.on_instruction_report(parent_order)
                elif message_type == MessageType.ORDER_CREATE:
                    order = OrderCreate()
                    order.load_from_json(data)
                    self.algo_bus_spi.on_order_create(order)
                elif message_type == MessageType.ORDER_CANCEL:
                    cancel_order = OrderCancel()
                    cancel_order.load_from_json(data)
                    self.algo_bus_spi.on_order_cancel(cancel_order)
                else:
                    self.logger.warn(f"[AlgoBusApi] unknown message type: {message_type}")
                    # raise Exception(f"unknown message type: {message_type}")
        except Exception as e:
            self.logger.error(f"[AlgoBusApi] on_data error: {e}, {traceback.format_exc()}")

    def on_error(self, ws, exception):
        self.ws = None
        reason = exception.resp_headers['reason'] if hasattr(exception, "resp_headers") else exception
        self.logger.error(f"[AlgoBusApi] ws on_error: {exception}, {traceback.format_exc()}, reason: {reason}")
        if self.algo_bus_spi:
            self.algo_bus_spi.on_connection_change(ConnectionStatus.DISCONNECTED)
        else:
            self.logger.debug("[AlgoBusApi] not register spi, not callback on_connection_change")

    def on_close(self, ws, close_status_code, close_msg):
        self.ws = None
        return
        self.logger.error(f"[AlgoBusApi] on_close code: {close_status_code}, close_msg: {close_msg}")
        if self.algo_bus_spi:
            self.algo_bus_spi.on_connection_change(ConnectionStatus.DISCONNECTED)
        else:
            self.logger.debug("[AlgoBusApi] not register spi, not callback on_connection_change")

    def login(self, app_login: AppLogin):
        self.logger.debug(f"[AlgoBusApi] login: {str(app_login)}")
        self.ws.send(str(app_login))

    def send_instruction_create(self, instruction_create: InstructionCreate):
        self.logger.debug(f"[AlgoBusApi] send_instruction_create: {str(instruction_create)}")
        self.ws.send(str(instruction_create))

    def send_instruction_control(self, instruction_control: InstructionControl):
        self.logger.debug(f"[AlgoBusApi] send_instruction_control: {str(instruction_control)}")
        self.ws.send(str(instruction_control))

    def send_order_create_report(self, order_create_report: OrderCreateReport):
        self.logger.debug(f"[AlgoBusApi] send_order_create_report: {str(order_create_report)}")
        self.ws.send(str(order_create_report))

    def send_order_fill_report(self, order_fill_report: OrderFillReport):
        self.logger.debug(f"[AlgoBusApi] send_order_fill_report {str(order_fill_report)}")
        self.ws.send(str(order_fill_report))

    def send_order_cancel_report(self, order_cancel_report: OrderCancelReport):
        self.logger.debug(f"[AlgoBusApi] send_order_cancel_report: {str(order_cancel_report)}")
        self.ws.send(str(order_cancel_report))

    def send_order_cancel_rsp(self, order_cancel_rsp: OrderCancelRsp):
        self.logger.debug(f"[AlgoBusApi] send_order_cancel_rsp: {str(order_cancel_rsp)}")
        self.ws.send(str(order_cancel_rsp))

    def query_instruction(self) -> List[InstructionReport]:
        query_url = self.http_url + "/instruction/"
        response = requests.get(query_url, headers={"token": "THIS_IS_SUPER_TOKEN"}, verify=False)
        result = []
        if response.status_code == 200 and len(response.text) > 0:
            for item in response.json():
                instruction_report = InstructionReport()
                instruction_report.load_from_json(item)
                result.append(instruction_report)
        return result

    def check_ws_connection(self):
        time.sleep(10)
        while True:
            if self.ws and self.ws.sock and self.ws.sock.connected:
                self.logger.debug(f"[AlgoBusApi] connection is alive.")
            else:
                self.logger.debug(f"[AlgoBusApi] connection is invalid, reconnect.")
                self.init_ws()
                self.ws.start()
            time.sleep(10)

    def run(self) -> None:
        threading.Thread(target=self.check_ws_connection, daemon=True).start()
        self.ws.run_forever()
