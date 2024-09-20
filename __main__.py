import logging
from typing import Any, Dict
import docker

if __name__ == "__main__":
  client = docker.from_env()
  services = client.services.list(status=True)
  containers = client.containers.list(filters={"status": ["running"]})
  stats: Dict[str, Any] = containers[0].stats(stream=False)

  cpu_delta: int = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
  system_delta: int = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
  number_of_cores: int = len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
  cpu_percent: float = (cpu_delta / system_delta) * number_of_cores * 100
  OKGREEN = '\033[92m'
  ENDC = '\033[0m'

  logging.basicConfig(level=logging.INFO, format=f"{OKGREEN}%(levelname)s{ENDC} %(message)s")
  logging.info(f"CPU usage: {round(cpu_percent, 2)}%")

  memory_percent: int = stats['memory_stats']['usage']/stats['memory_stats']['limit'] * 100
  MB = 1024*1024
  GB = 1024*1024*1024
  logging.info(f"Memory usage: {round(memory_percent, 2) }% ({round(stats['memory_stats']['usage']/MB, 2)} MB / {round(stats['memory_stats']['limit']/GB, 2)} GB)")
  # print(containers[0].logs().decode('utf-8'))
