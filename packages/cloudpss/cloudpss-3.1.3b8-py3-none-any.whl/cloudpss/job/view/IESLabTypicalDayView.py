from .IESView import IESView

class IESLabTypicalDayView(IESView):
    def GetTypicalDayNum():
        '''
            获取当前result的典型日数量
            
            :return: int类型，代表典型日数量
        '''
    def GetTypicalDayInfo(dayID):
        '''
            获取dayID对应典型日的基础信息
            
            :params: dayID int类型，表示典型日的ID，数值位于 0~典型日数量 之间
            
            :return: dict类型，代表典型日的基础信息，包括典型日所代表的日期范围、典型日的名称等
        '''
    def GetTypicalDayCurve(dayID, dataType):
        '''
            获取dayID对应典型日下dataType参数的时序曲线
            
            :params: dayID int类型，表示典型日的ID，数值位于 0~典型日数量 之间
            :params: dataType enum类型，标识辐照强度、环境温度、土壤温度、建筑物高度风速、风机高度风速、电负荷、热负荷、冷负荷的参数类型
            
            :return: list<float>类型，代表以1h为时间间隔的该参数的日内时序曲线
        '''
    pass