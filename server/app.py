import logging
from flask import Flask
import containers
import pods
import req_stat

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello, World!'
  
@app.route('/containers', methods=['GET'])
def get_containers():   
  containers_info = containers.get_containers_info()
  return containers_info

@app.route('/containers/confirm', methods=['POST'])
def confirmed_containers():
  return pods.confirmed_containers()

@app.route('/app/stat', methods=['GET'])
def get_stat():
  containers_info = containers.get_containers_info()
  requests_stat = req_stat.get_stat()
  return {
    'containers': containers_info,
    'requests_stat': requests_stat
  }

@app.route('/metrics', methods=['GET'])
def collect_metrics():
  try:
    req_stat.collect_metrics()
  except Exception as e:
    logging.info(str(e))
    return {"http": str(e)}
  return {"http": "200 OK"}

@app.route('/pod/set-pod-count/<pod_count>', methods=['POST'])
def post_set_pod(pod_count):
  return pods.set_pod_count(int(pod_count))

@app.route('/pod/scale/in', methods=['POST'])
def post_scale_in():
  return pods.scale_service_in()

@app.route('/pod/scale/out', methods=['POST'])
def post_scale_out():
  return pods.scale_service_out()
