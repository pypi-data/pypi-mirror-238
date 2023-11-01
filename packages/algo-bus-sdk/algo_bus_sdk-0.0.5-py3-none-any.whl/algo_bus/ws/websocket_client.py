import ssl
import threading

from websocket import WebSocketApp


class WebsocketClient(WebSocketApp, threading.Thread):
    def __init__(self, url, header=None, on_open=None, on_message=None, on_error=None, on_close=None, on_ping=None, on_pong=None, on_cont_message=None, keep_running=True,
                 get_mask_key=None, cookie=None, subprotocols=None, on_data=None):
        self.thread = None
        super().__init__(url, header, on_open, on_message, on_error, on_close, on_ping, on_pong, on_cont_message, keep_running, get_mask_key, cookie, subprotocols, on_data)
        threading.Thread.__init__(self, target=self.run_forever)

    def run_forever(self, sockopt=None, sslopt=None, ping_interval=0, ping_timeout=None, ping_payload="", http_proxy_host=None, http_proxy_port=None, http_no_proxy=None,
                    http_proxy_auth=None, skip_utf8_validation=False, host=None, origin=None, dispatcher=None, suppress_origin=False, proxy_type=None):
        sslopt = {"cert_reqs": ssl.CERT_NONE}
        return super().run_forever(sockopt, sslopt, ping_interval, ping_timeout, ping_payload, http_proxy_host, http_proxy_port, http_no_proxy, http_proxy_auth,
                                   skip_utf8_validation, host, origin, dispatcher, suppress_origin, proxy_type)

    def run(self) -> None:
        self.run_forever()
