import decimal

class Container(object):    
    def __init__(self, name: str, cpu: decimal, mem: decimal, req_mem: decimal, req_cpu: decimal, cpu_percent: decimal, mem_percent: decimal):
        self.name = name
        self.cpu = cpu
        self.mem = mem
        self.req_mem = req_mem
        self.req_cpu = req_cpu
        self.cpu_percent = cpu_percent
        self.mem_percent = mem_percent
