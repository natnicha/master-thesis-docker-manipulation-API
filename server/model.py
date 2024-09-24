import decimal

class Container:    
    def __init__(self, id: str, name: str, cpu_percent: decimal, mem_percent: decimal, mem_usage_mb: decimal, mem_limit_gb: decimal):
        self.id = id
        self.name = name
        self.cpu_percent = cpu_percent
        self.mem_percent = mem_percent
        self.mem_usage_mb = mem_usage_mb
        self.mem_limit_gb = mem_limit_gb
