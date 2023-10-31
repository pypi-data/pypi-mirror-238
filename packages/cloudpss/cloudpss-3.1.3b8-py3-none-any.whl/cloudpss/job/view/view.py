

from ..messageStreamSender import MessageStreamSender
from ..messageStreamReceiver import MessageStreamReceiver


class View(object):
    """
        结果视图基类，提供基础的结果获取接口
    """
    def __init__(self, receiver:MessageStreamReceiver,sender:MessageStreamSender=None) -> None:
        """
            初始化
        """
        self.result = {}
        self._receiver = receiver
        self._sender = sender
        self.__logsIndex = 0
        
    def __deepModify(self, dict1, dict2):

        for key, val in dict1.items():
            if type(val) is dict:
                self.__deepModify(val, dict2[key])
            else:
                dict2[key] = val
                
    def modify(self, data, model):
        """
            通过指定消息修改算例文件

            :params: data 消息字典 {}
            :params: model  项目

            >>> message= view.modify(data,model)

        """
        modifyData = data['data']
        payload = modifyData['payload']
        self.__deepModify(payload, model)
    
    def getMessagesByKey(self, key):
        """
            获取指定 key 的消息数据

            :params key: 数据key

            :returns: 对应 key 的数据数组

            >>> message= db.getMessagesByKey('log')
        """

        result = []
        for val in self._receiver:
            if val.get('key', None) == key:
                result.append(val)
        return result

    def getMessagesByType(self, type):
        """
            获取指定类型的消息数据

            :params type: 数据类型

            :returns: 对应类型的数据数组

            >>> message= db.getMessagesByType('log')
        """

        result = []
        for val in self._receiver:
            if val['type'] == type:
                result.append(val)
        return result

    def getMessage(self, index):
        """
            获取指定位置的消息数据

            :params index: 数据的位置信息

            :returns: 消息数据

            >>> message= db.getMessage(1)
        """
        return self._receiver.messages[index]

    def getMessages(self):
        """
            获取所有消息数据

            :returns: 消息数据数组
        """
        return self._receiver.messages
    
    
    def getLogs(self):
        '''
            获取当前任务的日志

            >>>logs= result.getLogs()
            {...}
        '''
        result = []
        length = len(self._receiver.messages)
        if (length > self.__logsIndex):
            for num in range(self.__logsIndex, length):
                val = self.getMessage(num)
                if val['type'] == 'log':
                    result.append(val)
            self.__logsIndex = length
        return result
    
    
    @property
    def end(self):
        """
            获取当前连接状态

            :returns: 当前连接状态  0:关闭 1:打开
        """
        return self._receiver.end