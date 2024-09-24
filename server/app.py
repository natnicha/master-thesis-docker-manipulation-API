from flask import Flask
from model import *
from containers import *

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
  
@app.route('/containers')
def containers():   
    containers_info = get_containers_info()
    return {
        'containers': containers_info
    }

