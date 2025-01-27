import logging
from datetime import datetime
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import containers
MIN_REPLICAS = 1
MAX_REPLICAS = 5

class ScalingPod():
  In = -1
  Out = 1

def scale_pods(replicas: int):
  try:
    configuration = config.load_kube_config()

    api_client = client.ApiClient(configuration)
    apps_v1 = client.AppsV1Api(api_client)
    api_response = apps_v1.patch_namespaced_deployment_scale('ml-app', "default", {"spec": {"replicas": replicas}})
    print(api_response)
  except ApiException as e:
    print("Exception when calling AppsV1Api->patch_namespaced_deployment_scale: %s\n" % e)

def get_service_replicas(service_info: dict):
  return service_info['system']['total_pods']

def scale_service_in():
  return scale_service(ScalingPod.In)

def scale_service_out():
  return scale_service(ScalingPod.Out)

def scale_service(scale: ScalingPod):
  target_service = containers.get_containers_info()
  current_replicas = get_service_replicas(target_service)
  target_replicas = current_replicas + scale
  if target_replicas >= MIN_REPLICAS and target_replicas <= MAX_REPLICAS:
    start_dateTime = datetime.now()
    scale_pods(target_replicas)
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
  timeout = 90
  is_all_pod_running = False
  start_time = datetime.now()
  api = client.CustomObjectsApi()
  while(not is_all_pod_running and ((datetime.now()-start_time).total_seconds() < timeout)):
    k8s_pods = api.list_namespaced_custom_object("metrics.k8s.io", "v1beta1", "default", "pods")
    if target_replicas != len(k8s_pods['items']):
      continue
    else:
      is_all_pod_running = True
  return 

def set_pod_count(pod_count: int):
  if pod_count >= MIN_REPLICAS and pod_count <= MAX_REPLICAS:
    start_dateTime = datetime.now()
    scale_pods(pod_count)
    check_container_status(pod_count)
    finish_dateTime = datetime.now()
    time_spent = finish_dateTime-start_dateTime
    logging.info(f"successful scaling {pod_count} with: {time_spent}")
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

def confirmed_containers():
  container_info = containers.get_containers_info()
  online_pods = int(container_info['system']['online_pods'])
  set_pod_count(online_pods)
  return containers.get_containers_info()
