from decimal import Decimal
import logging
from kubernetes import client, config
import re
from model import *

OKGREEN = '\033[92m'
ENDC = '\033[0m'

logging.basicConfig(level=logging.INFO, format=f"{OKGREEN}%(levelname)s{ENDC} %(message)s")

CONVERSION_METRICS = {'n': '0.000000001', 'u':'0.000001', 'm':'0.001', 'Ti': '1099511627776', 'Gi': '1073741824', 'Mi': '1048576', 'Ki': '1024' }

def convert_to_byte(value: str):
    global CONVERSION_METRICS
    match = re.search(r'[a-zA-Z]{1,2}$', value)
    if match:
        metric = match.group()
        multiple = CONVERSION_METRICS[metric]
        value = value.replace(metric,'')
        return Decimal(value)*Decimal(multiple)
    return Decimal(value)

def get_containers_info() -> dict:
  config.load_kube_config()
  api = client.CustomObjectsApi()
  v1 = client.CoreV1Api()

  k8s_pods = api.list_namespaced_custom_object("metrics.k8s.io", "v1beta1", "default", "pods")
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
  
  return {
    'system': {
      'cpu_percent': round(total_system_cpu/len(containers_info), 2),
      'mem_percent': round(total_system_mem/len(containers_info), 2),
      'online_pods': len(containers_info)
    },
    'container': containers_info
  }