import os,sys
import time

import socketio
import threading
import struct
sio = socketio.Client()
class SocketStream():
    def __init__(self):
        # sio.connect('ws://10.101.10.119/',socketio_path='/api/real-time/socket.io')
        pass
    
    def connect(self):
        sio.emit('start-job', { 'type': 'start-job', 'context': 'real-time-data' })
        sio.emit('real-time-data', { 'type': 'real-time-data', 'context': 'real-time-data' })
        sio.emit('data-panel', { 'type': 'data-panel', 'context': 'real-time-data' })
        print("I'm connected!")
    
    @sio.event
    def connect_error(self,data):
        print("The connection failed!")

    @sio.event
    def disconnect(self):
        print("I'm disconnected!")
        
    @sio.on('data-panel')
    def on_event(self,data):
        print( data)
    @sio.on('start-job')
    def start_job(self,data):
        print( data)
    @sio.on('stop-job')
    def stop_job(self,data):
        print( data)    
    @sio.on('close-job')
    def close_job(self,data):
        print( data)  
    @sio.on('recording')
    def recording(self,data):
        print( data)
    @sio.on('load-record-data')
    def load_record_data(self,data):
        print( data)
    @sio.on('real-time-data')
    def real_time_data(self,data):
        data =struct.unpack('f'*int(len(data)/4),data)
        
        print(len(data))
                         
    
if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    os.environ['CLOUDPSS_API_URL'] = 'ws://10.101.10.119/'
    # job = cloudpss.Job.fetch()
    
    
    # @sio.event
    # def connect():
    #     sio.emit('start-job', { 'type': 'start-job', 'context': 'real-time-data' })
    #     sio.emit('real-time-data', { 'type': 'real-time-data', 'context': 'real-time-data' })
    #     sio.emit('data-panel', { 'type': 'data-panel', 'context': 'real-time-data' })
    #     print("I'm connected!")

    # @sio.event
    # def connect_error(data):
    #     print("The connection failed!")

    # @sio.event
    # def disconnect():
    #     print("I'm disconnected!")
        
    # @sio.on('data-panel')
    # def on_event(data):
    #     print( data)
    # @sio.on('start-job')
    # def start_job(data):
    #     print( data)
    # @sio.on('stop-job')
    # def stop_job(data):
    #     print( data)    
    # @sio.on('close-job')
    # def close_job(data):
    #     print( data)  
    # @sio.on('recording')
    # def recording(data):
    #     print( data)
    # @sio.on('load-record-data')
    # def load_record_data(data):
    #     print( data)
    # @sio.on('real-time-data')
    # def real_time_data(data):
    #     data =struct.unpack('f'*int(len(data)/4),data)
        
    #     print(len(data))
        
    
    sio.connect('ws://10.101.10.119/',socketio_path='/api/real-time/socket.io')
   
    thread = threading.Thread(target=sio.wait, args=())
    thread.setDaemon(True)
    thread.start()
        
    while True:
        time.sleep(1)
        print('main')
        pass