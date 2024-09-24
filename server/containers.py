import logging
from typing import Any, Dict
import docker
from model import *

OKGREEN = '\033[92m'
ENDC = '\033[0m'

MB = 1024*1024
GB = 1024*1024*1024

logging.basicConfig(level=logging.INFO, format=f"{OKGREEN}%(levelname)s{ENDC} %(message)s")

def get_cpu_usage_percent(container_stats: Dict[str, Any]):
  cpu_delta: int = container_stats['cpu_stats']['cpu_usage']['total_usage'] - container_stats['precpu_stats']['cpu_usage']['total_usage']
  system_delta: int = container_stats['cpu_stats']['system_cpu_usage'] - container_stats['precpu_stats']['system_cpu_usage']
  number_of_cores: int = len(container_stats['cpu_stats']['cpu_usage']['percpu_usage'])
  cpu_percent: float = (cpu_delta / system_delta) * number_of_cores * 100
  return cpu_percent


def get_ram_usage_percent(container_stats: Dict[str, Any]):
  return container_stats['memory_stats']['usage']/container_stats['memory_stats']['limit'] * 100


def get_containers_info() -> list:
  client = docker.from_env()
  containers = client.containers.list(filters={"status": ["running"]})

  containers_info = []
  logging.info("CONTAINER ID \tNAME \t\tCPU % \t\tMEM % \tUSAGE / LIMIT")
  for container in containers:
    stats: Dict[str, Any] = container.stats(stream=False)
    cpu_percent = get_cpu_usage_percent(stats)
    memory_percent = get_ram_usage_percent(stats)

    info = Container(id=container.short_id, name=container.name[:12], cpu_percent=round(cpu_percent, 2), mem_percent=round(memory_percent, 2), mem_usage_mb=round(stats['memory_stats']['usage']/MB, 2), mem_limit_gb=round(stats['memory_stats']['limit']/GB, 2))
    logging.info(f"{info.id} \t{info.name} \t{info.cpu_percent}% \t\t{info.mem_percent}% \t{info.mem_usage_mb} MB / {info.mem_limit_gb} GB")
    containers_info.append(info.__dict__)
  
  return containers_info