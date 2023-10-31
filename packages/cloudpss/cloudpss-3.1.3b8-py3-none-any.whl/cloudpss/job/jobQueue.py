from cloudpss.job.jobMachine import JobMachine


class JobQueue(object):

    def __init__(self, id, name, scheduler, machines, createTime, updateTime,
                 load):
        self.id = id
        self.name = name
        self.scheduler = scheduler
        self.machines = [JobMachine(**m) for m in machines]
        self.createTime = createTime
        self.updateTime = updateTime
        self.load = load
