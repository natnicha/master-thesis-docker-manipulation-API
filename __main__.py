import logging
from typing import Any, Dict
import docker

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
  return stats['memory_stats']['usage']/stats['memory_stats']['limit'] * 100


if __name__ == "__main__":
  client = docker.from_env()
  containers = client.containers.list(filters={"status": ["running"]})
  stats: Dict[str, Any] = containers[0].stats(stream=False)

  cpu_percent = get_cpu_usage_percent(stats)
  logging.info(f"CPU usage: {round(cpu_percent, 2)}%")

  memory_percent = get_ram_usage_percent(stats)
  logging.info(f"Memory usage: {round(memory_percent, 2) }% ({round(stats['memory_stats']['usage']/MB, 2)} MB / {round(stats['memory_stats']['limit']/GB, 2)} GB)")
