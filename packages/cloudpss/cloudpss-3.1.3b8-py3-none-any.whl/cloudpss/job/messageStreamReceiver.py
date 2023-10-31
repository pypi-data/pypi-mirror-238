import logging
from .jobReceiver import JobReceiver
import os
from urllib.parse import urlparse
import websocket
import pytz
import threading
import time
utc_tz = pytz.timezone('UTC')

from ..utils.IO import IO


class Message(object):

    def __init__(self, id, token):
        self.id = id
        self.token = token
        


class MessageStreamReceiver(JobReceiver):

    def __init__(self, job, dev=False):
        super().__init__()
        self.job = job
        self.dev = dev
        self.origin = os.environ.get('CLOUDPSS_API_URL',
                                     'https://cloudpss.net/')
        self.__hasOpen=False

    def receive(self, id, fr0m, on_open, on_message, on_error, on_close):
        """
        读取消息流中的数据
        id: 消息流id
        fr0m: 从哪个位置开始读取，如果为0则从头开始读取
        on_open: 连接建立时的回调函数
        on_message: 收到消息时的回调函数
        on_error: 发生错误时的回调函数
        on_close: 连接关闭时的回调函数
        """
        if id is None:
            raise Exception('id is None')
        u = list(urlparse(self.origin))
        head = 'wss' if u[0] == 'https' else 'ws'

        path = head + '://' + str(u[1]) + '/api/streams/id/' + id
        if fr0m is not None:
            path = path + '&from=' + str(fr0m)
        logging.info(f"receive data from websocket: {path}")
        ws = websocket.WebSocketApp(path,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        
        return ws
    
    ###下面是兼容Receiver部分功能实现

    def on_message(self, ws, message):
        data = IO.deserialize(message, 'ubjson')
        msg = IO.deserialize(data['data'], 'ubjson')
        if msg.get('type', None) == 'log' and self.dev:
            print(msg)
        self.messages.append(msg)
        # if msg and type(msg) is dict and msg.get('type', None) == 'terminate':
        #     self.close(ws)

    def on_error(self, ws, error):
        logging.info("MessageStreamReceiver error")
        msg = {
            'type': 'log',
            'verb': 'create',
            'version': 1,
            'data': {
                'level': 'error',
                'content': "websocket error",
            },
        }
        self.messages.append(msg)

    def on_close(self, *args, **kwargs):
        logging.info("MessageStreamReceiver close")
        self._status = 0
        msg = {
            'type': 'log',
            'verb': 'create',
            'version': 1,
            'data': {
                'level': 'error',
                'content': "websocket closed",
            },
        }
        self.messages.append(msg)

    def on_open(self, ws):
        self._status = 1
        self.__hasOpen=True
        pass

    def close(self, ws):
        self._status = 0
        ws.close()

    @property
    def end(self):
        return  not self._status

    def connect(self):
        self._status = 0
        self.ws = self.receive(self.job.output, None, self.on_open,
                               self.on_message, self.on_error, self.on_close)
        
        
        thread = threading.Thread(target=self.ws.run_forever, args=(None , None , 6, 3))
        thread.setDaemon(True)
        thread.start()
        while not self.__hasOpen:
            time.sleep(0.2)