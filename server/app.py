from flask import Flask
from model import *
from containers import *

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
  
@app.route('/containers', methods=['GET'])
def containers():   
    containers_info = get_containers_info()
    return {
        'containers': containers_info
    }

@app.route('/scale/in', methods=['POST'])
def scale_in():
    return {}

@app.route('/scale/out', methods=['POST'])
def scale_in():
    return {}
