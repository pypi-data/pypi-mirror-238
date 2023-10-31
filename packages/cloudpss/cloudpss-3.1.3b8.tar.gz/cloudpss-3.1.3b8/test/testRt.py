import os,sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..\\'))
import cloudpss 
import socketio
import threading
import struct
import json

class RealTimeSream(socketio.ClientNamespace):
    
    config = None
    messages = []
    series=[]
    outputNumericValue={}
    inputNumericValue={}
    
    end=False
    
    def __init__(self, namespace=None, *args, **kwargs):
        super().__init__(namespace)
        
        setattr(self, 'on_data-panel', self.on_data_panel)
        setattr(self, 'on_start-job', self.on_start_job)
        setattr(self, 'on_stop-job', self.on_stop_job)
        setattr(self, 'on_close-job', self.on_close_job)
        setattr(self, 'on_load-record-data', self.on_load_record_data)
        setattr(self, 'on_real-time-data', self.on_real_time_data)
        self.numericValueCallBack = kwargs.get('numericValueCallBack',None)
        self.chartCallBack = kwargs.get('chartCallBack',None)
        
        
        
        
    def on_connect(self):
        self.emit('start-job', { 'type': 'start-job', 'context': 'real-time-data' })
        self.emit('real-time-data', { 'type': 'real-time-data', 'context': 'real-time-data' })
        self.emit('data-panel', { 'type': 'data-panel', 'context': 'real-time-data' })
        pass

    def on_disconnect(self):
        pass

    def on_data_panel(self, data):
        # self.numericValue=data
        virtual_input=self.config['virtual_input']
        virtual_output=self.config['virtual_output']
        display=self.config['display']
        
        d ={}
        for x,v in display.items():
            d[v]=x
        
        for i in range(0,virtual_input):
            self.inputNumericValue[d[i]]=data[i]
        for i in range(0,virtual_output): 
            self.outputNumericValue[d[virtual_input+i]]=data[virtual_input+i]
        if self.numericValueCallBack is not None:
            self.numericValueCallBack(self.inputNumericValue,self.outputNumericValue)
    def on_start_job(self,data):
        self.config =data
        print( 'on_start_job',self.config)
    def on_stop_job(self,data):
        print('on_stop_job',flush=True)
        self.disconnect()
        self.end=True
    def on_close_job(self,data):
        print('on_close_job',flush=True)
        self.disconnect()
        self.end=True
    def on_recording(self,data):
        print( 'on_recording',data)
    def on_load_record_data(self,data):
        print( 'on_load_record_data',data)
    def on_real_time_data(self,d):
        
        data =struct.unpack('d'*int(len(d)/8),d)
        i = 0
        runTime =0
        channelLength=int(self.config['portNumber'])+1
        virtual_input=int(self.config['virtual_input'])
        for index in range(0,len(data)):
            val = data[index]
            if(index%channelLength==0):
                i=0
                runTime = val
            elif i>virtual_input:
                serieIndex = i - virtual_input - 1
                
                if len(self.series)-1<serieIndex:
                    
                    serie=  {
                        'name':  'data%d'%serieIndex,
                        'type': 'scatter',
                        'x': [],
                        'y': []
                    }  
                    self.series.append(serie)
                else:
                    serie=self.series[serieIndex]
                
                serie['x'].append(runTime)
                serie['y'].append(val)
            i+=1
        if self.chartCallBack is not None:
            self.chartCallBack(self.series)

    def close(self):
        self.end =True
        self.emit('close-job', { 'type': 'close-job', 'context': 'close-job' })
    def write(self,data):
        self.emit('send-message', data)
    @staticmethod
    def connect(*args, **kwargs):
        sio = socketio.Client()
        stream = RealTimeSream('',*args, **kwargs)
        
        sio.register_namespace(stream)
        sio.connect('ws://10.101.10.119/',socketio_path='/api/real-time/socket.io')
    
        thread = threading.Thread(target=sio.wait, args=())
        thread.setDaemon(True)
        thread.start()
        return stream

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    os.environ['CLOUDPSS_API_URL'] = 'ws://10.101.10.119/'
    job = cloudpss.currentJob()
    
    
    def numericValueCallBack(inputNumericValue,outputNumericValue):
        print(inputNumericValue,flush=True)
        
    def chartCallBack(series):
        job.plot(series,key='test1')

    stream = RealTimeSream.connect(numericValueCallBack=numericValueCallBack,chartCallBack=chartCallBack)
    def exitCallback():
        stream.close()
        time.sleep(1)
        print('exit')
        job.exit(0)

    job.on_abort(exitCallback, args=(), kwargs={})
    
    print('start',flush=True)
    while not stream.end :
        time.sleep(1)
        pass