import logging
from datetime import datetime
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from decimal import Decimal
import re
from model import *

MIN_REPLICAS = 1
MAX_REPLICAS = 5

OKGREEN = '\033[92m'
ENDC = '\033[0m'

logging.basicConfig(level=logging.INFO, format=f"{OKGREEN}%(levelname)s{ENDC} %(message)s")

CONVERSION_METRICS = {'n': '0.000000001', 'u':'0.000001', 'm':'0.001', 'Ti': '1099511627776', 'Gi': '1073741824', 'Mi': '1048576', 'Ki': '1024' }

class ScalingPod():
  In = -1
  Out = 1


def convert_to_byte(value: str):
    global CONVERSION_METRICS
    match = re.search(r'[a-zA-Z]{1,2}$', value)
    if match:
        metric = match.group()
        multiple = CONVERSION_METRICS[metric]
        value = value.replace(metric,'')
        return Decimal(value)*Decimal(multiple)
    return Decimal(value)

def get_pod_info() -> dict:
  config.load_kube_config()
  api = client.CustomObjectsApi()
  v1 = client.CoreV1Api()

  k8s_pods = api.list_namespaced_custom_object("metrics.k8s.io", "v1beta1", "default", "pods")
  pods = v1.list_pod_for_all_namespaces(watch=False)
  total_pods = 0
  for pod in pods.items:
    if pod.metadata.namespace == "default":
      total_pods = total_pods + 1

  containers_info = []
  total_system_cpu = 0
  total_system_mem = 0
  
  logging.info("CONTAINER NAME \t\tCPU % \tUSAGE / REQ \t\tMEM % \tUSAGE / REQ")
  for stats in k8s_pods['items']:
    res = v1.read_namespaced_pod_status(stats['metadata']['name'], "default")
    
    usage = {
      'name': stats['metadata']['name'],
      'cpu' : stats['containers'][0]['usage']['cpu'],
      'mem': stats['containers'][0]['usage']['memory'],
      'req_cpu': res.spec.containers[0].resources.requests['cpu'],
      'req_mem': res.spec.containers[0].resources.requests['memory'],
    }
    converted_usage = {
      'name': stats['metadata']['name'],
      'cpu' : convert_to_byte(usage['cpu']),
      'mem': convert_to_byte(usage['mem']),
      'req_cpu': convert_to_byte(usage['req_cpu']),
      'req_mem': convert_to_byte(usage['req_mem']),
    }
    converted_usage['cpu_percent'] = round(100*converted_usage['cpu']/converted_usage['req_cpu'], 2)
    converted_usage['mem_percent'] = round(100*converted_usage['mem']/converted_usage['req_mem'], 2)
    
    info = Container(name=converted_usage['name'], 
      cpu=converted_usage['cpu'], 
      mem=converted_usage['mem'], 
      req_mem=converted_usage['req_mem'], 
      req_cpu=converted_usage['req_cpu'], 
      cpu_percent=converted_usage['cpu_percent'], 
      mem_percent=converted_usage['mem_percent']
    )
    total_system_cpu += info.cpu_percent
    total_system_mem += info.mem_percent
    logging.info(f"{info.name} \t{info.cpu_percent} \t{info.cpu} / {info.req_cpu} \t{info.mem_percent} \t{info.mem} / {info.req_mem}")
    containers_info.append(info.__dict__)
  
  if len(containers_info) == 0:
    return {
      'system': {
        'cpu_percent': None,
        'mem_percent': None,
        'online_pods': None,
        'total_pods': total_pods
      }
    }
  else:
    return {
      'system': {
        'cpu_percent': round(total_system_cpu/len(containers_info), 2),
        'mem_percent': round(total_system_mem/len(containers_info), 2),
        'online_pods': len(containers_info),
        'total_pods': total_pods
      },
      'container': containers_info
    }


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
  target_service = get_pod_info()
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

def get_confirmed_pod():
  container_info = get_pod_info()
  online_pods = int(container_info['system']['online_pods'])
  set_pod_count(online_pods)
  return get_pod_info()
