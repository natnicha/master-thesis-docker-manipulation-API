import datetime
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
  return {
    'containers': containers_info
  }

@app.route('/app/stat', methods=['GET'])
def get_stat():
  containers_info = containers.get_containers_info()
  requests_stat = req_stat.get_stat()
  return {
    'containers': containers_info,
    'requests_stat': requests_stat
  }

@app.route('/app/now', methods=['GET'])
def get_now():
  return {
    'now': datetime.datetime.timestamp(datetime.datetime.now()),
  }

@app.route('/scale/in', methods=['POST'])
def post_scale_in():
  return pods.scale_service_in()

@app.route('/scale/out', methods=['POST'])
def post_scale_out():
  return pods.scale_service_out()
