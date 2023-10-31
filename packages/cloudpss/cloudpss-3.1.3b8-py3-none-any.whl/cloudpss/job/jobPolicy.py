from cloudpss.job.jobQueue import JobQueue
from cloudpss.job.jobTres import JobTres
from cloudpss.utils.graphqlUtil import graphql_request


class JobPolicy(object):

    def __init__(self, id, name, users, functions, tres, minPriority,
                 maxPriority, maxDuration, createTime, updateTime, visibility,
                 queue):
        self.id = id
        self.name = name
        self.users = users
        self.functions = functions
        print(tres)
        self.tres = []
        for tre in tres:
            self.tres.append(JobTres(**tre))  # type: ignore
        self.minPriority = minPriority
        self.maxPriority = maxPriority
        self.maxDuration = maxDuration
        self.createTime = createTime
        self.updateTime = updateTime
        self.visibility = visibility
        self.queue = JobQueue(**queue)  # type: ignore

    @staticmethod
    def fetch(id):
        query = '''query($input:JobPolicyInput!)
            {
                jobPolicy(input:$input)
                {
                    id 
                    name 
                    users 
                    functions 
                    tres {
                        cpu
                        ecpu
                        mem
                    } 
                    minPriority 
                    maxPriority 
                    maxDuration 
                    createTime 
                    updateTime 
                    visibility 
                    queue {
                        id
                        name
                        scheduler
                        machines {
                            id
                            name
                            tres {
                                cpu
                                ecpu
                                mem
                            }
                            valid
                        }
                        createTime
                        updateTime
                        load
                    }
                }
                
            }'''
        variables = {'input': {'id': id}}
        r = graphql_request(query, variables)
        print (r)
        if 'errors' in r:
            raise Exception(r['errors'])
        return JobPolicy(**r['data']['jobPolicy'])

    @staticmethod
    def fetchMany(input):
        query = '''query($input:JobPoliciesInput!)
            {
                jobPolicies(input:$input)
                {
                    items {
                        id 
                        name 
                        users 
                        functions 
                        tres {
                            cpu
                            ecpu
                            mem
                        } 
                        minPriority 
                        maxPriority 
                        maxDuration 
                        createTime 
                        updateTime 
                        visibility 
                        queue {
                            id
                            name
                            scheduler
                            machines {
                                id
                                name
                                tres {
                                    cpu
                                    ecpu
                                    mem
                                }
                                valid
                            }
                            createTime
                            updateTime
                            load
                        }
                    }
                    cursor
                    count
                    total
                }
            }'''
        variables = {'input': input}
        r = graphql_request(query, variables)
        if 'errors' in r:
            raise Exception(r['errors'])
        policies = []
        for policy in r['data']['jobPolicies']['items']:
            policies.append(JobPolicy(**policy))
        return policies