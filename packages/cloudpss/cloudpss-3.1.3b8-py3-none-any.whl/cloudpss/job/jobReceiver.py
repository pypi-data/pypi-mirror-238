class JobReceiver(object):
    messages = []
    index = 0

    def __init__(self):
        self.index = 0
        self.messages = []

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return self

    def __next__(self):
        maxLength = len(self.messages)
        if self.index < maxLength:
            message = self.messages[self.index]
            self.index += 1
            return message
        raise StopIteration()

    def view(self, ViewType):
        """
            获取指定类型的视图数据

            :params viewType: 视图类型

            :returns: 对应类型的视图数据

            >>> view= receiver.view(EMTView)
        """
        return ViewType(self)