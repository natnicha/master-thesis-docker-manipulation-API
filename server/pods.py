import docker
import logging
from datetime import datetime

MIN_REPLICAS = 1
MAX_REPLICAS = 5

class ScalingPod():
  In = -1
  Out = 1

def get_service_info():
  client = docker.from_env()
  services = client.services.list(filters={"name":["ml_app"]})
  return services[0]

def get_service_replicas(service_info: dict):
  return service_info.attrs['Spec']['Mode']['Replicated']['Replicas']

def scale_service_in():
  return scale_service(ScalingPod.In)

def scale_service_out():
  return scale_service(ScalingPod.Out)

def scale_service(scale: ScalingPod):
  target_service = get_service_info()
  current_replicas = get_service_replicas(target_service)
  target_replicas = current_replicas + scale
  if target_replicas >= MIN_REPLICAS and target_replicas <= MAX_REPLICAS:
    start_dateTime = datetime.now()
    target_service.scale(target_replicas)
    check_container_status(target_replicas)
    finish_dateTime = datetime.now()
    time_spent = finish_dateTime-start_dateTime
    logging.info(f"successful scaling {scale} with: {time_spent}")
    return {
      'start_time': datetime.timestamp(start_dateTime),
      'finish_time': datetime.timestamp(finish_dateTime),
      'time_spent_sec': time_spent.total_seconds()
    }
  else:
    now = datetime.now()
    datetime_now = datetime.timestamp(now)
    return {
      'start_time': datetime_now,
      'finish_time': datetime_now,
      'time_spent_sec': 0.00
    }


def check_container_status(target_replicas: int):
  client = docker.from_env()
  timeout = 30
  is_all_pod_running = False
  start_time = datetime.now()
  while(not is_all_pod_running and ((datetime.now()-start_time).total_seconds() < timeout)):
    containers = client.containers.list(filters={"ancestor": "master-thesis-image-recognition-app"})
    if target_replicas != len(containers):
      continue
    for container in containers:
      if container.status != 'running':
        is_all_pod_running = False
        break
      if container.status == 'running':
        is_all_pod_running = True
  return 
