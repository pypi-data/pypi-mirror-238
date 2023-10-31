import sys,os
import threading
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import websocket

from cloudpss.utils.IO import IO
import time
import logging

class MessageStreamSender():

    def __init__(self, job, dev=False):
        super().__init__()
        self.job = job
        self.dev = dev
        self.origin = os.environ.get('CLOUDPSS_API_URL',
                                     'https://cloudpss.net/')

    ###下面是兼容Receiver部分功能实现

    def on_message(self, ws, message):
        logging.info('on_message',message)

    def on_error(self, ws, error):
        logging.info('on_error')

    def on_close(self, *args, **kwargs):
        time.sleep(0.5)
        self._status = 0
        
        logging.info('on_close')

    def on_open(self, ws):
        self._status = 1
        logging.info('on_open')
        pass

    def close(self):
        
        self._status = 0
        self.ws.close()

    @property
    def status(self):
        return self._status

    def write(self, message):
        data = IO.serialize(message, 'ubjson',None)
        self.ws.send(data, websocket.ABNF.OPCODE_BINARY)
        
    def connect(self):
        logging.info('connect')
        self._status = 0
        if self.job.input is None:
            raise Exception('id is None')
        u = list(urlparse(self.origin))
        head = 'wss' if u[0] == 'https' else 'ws'

        path = head + '://' + str(u[1]) + '/api/streams/token/' + self.job.input
        logging.info(f"receive data from websocket: {path}")
        
        self.ws = websocket.WebSocketApp(path,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        
        thread = threading.Thread(target=self.ws.run_forever, args=(None , None , 6, 3))
        thread.setDaemon(True)
        thread.start()
        while self.status != 1:
            time.sleep(0.2)