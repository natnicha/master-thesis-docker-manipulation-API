import logging
from flask import Flask
import containers
import pods
import req_stat
import metrics

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello, World!'
  
@app.route('/pod', methods=['GET'])
def get_pod():   
  containers_info = containers.get_pod_info()
  return containers_info

@app.route('/pod/confirm', methods=['POST'])
def get_confirmed_pod():
  return pods.get_confirmed_pod()

@app.route('/pod/scale/in', methods=['POST'])
def post_scale_in():
  return pods.scale_service_in()

@app.route('/pod/scale/out', methods=['POST'])
def post_scale_out():
  return pods.scale_service_out()

@app.route('/app/stat', methods=['GET'])
def get_stat():
  containers_info = containers.get_pod_info()
  requests_stat = req_stat.get_stat()
  return {
    'containers': containers_info,
    'requests_stat': requests_stat
  }

@app.route('/pod/set-pod-count/<pod_count>', methods=['POST'])
def post_set_pod(pod_count):
  return pods.set_pod_count(int(pod_count))

@app.route('/metrics', methods=['GET'])
def collect_metrics():
  try:
    metrics.collect_metrics()
  except Exception as e:
    logging.info(str(e))
    return {"http": str(e)}
  return {"http": "200 OK"}
