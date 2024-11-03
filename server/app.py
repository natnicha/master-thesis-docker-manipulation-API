from flask import Flask, request
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
  args = request.args.to_dict()
  requests_stat = req_stat.get_stat(args['from'], args['to'])
  return {
    'containers': containers_info,
    'requests_stat': requests_stat
  }

@app.route('/scale/in', methods=['POST'])
def post_scale_in():
  return pods.scale_service_in()

@app.route('/scale/out', methods=['POST'])
def post_scale_out():
  return pods.scale_service_out()
