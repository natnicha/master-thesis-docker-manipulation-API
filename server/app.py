from flask import Flask
from model import *

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
  
@app.route('/containers')
def containers():   
    container = Container(
        id='efb6c0c4566b', 
        name='ml.2.q5iuqge', 
        cpu_percent=0.19, 
        mem_percent=7.73, 
        mem_usage_mb=297.71, 
        mem_limit_gb=3.76
    )
    return {
        'containers': [container.__dict__]
    }

