from cloudpss.job.jobTres import JobTres


class JobMachine(object):
    '''job machine'''

    def __init__(self, id, name, tres, valid=None):
        self.id = id
        self.name = name
        self.tres = JobTres(**tres)  # type: ignore
        self.valid = valid