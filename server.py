from flask import Flask, send_from_directory
from flask import request,Response, make_response, render_template
import psutil
import json
import subprocess
import time
#from .src.ProcessInfo import *
app = Flask(__name__, template_folder='C:\\Users\\Admin\\Desktop\\Server\\my-app\\build\\', static_folder='C:\\Users\\Admin\\Desktop\\Server\\my-app\\build\\static')

def nodeManager(action, process):
    if action == 'start' or action == 'stop':
        subprocess.run(f'net {action} {process}',shell=True)
    elif action ==  'restart':
        subprocess.run(f'net stop {process}',shell=True)
        time.sleep(2)
        subprocess.run(f'net start {process}',shell=True)
    else:
        print("Неверный параметр.")
        return False
    
processes = ['ControlNode','RenderNode','UserNode', 'StorageNode', 'postgresql-x64-13']

@app.route("/data", methods=['POST'])
def get_data():
    body = str(request.data, 'utf-8') #dict(json.loads(request.data))
    print('req body: ', body)
    data = json.JSONDecoder().decode(body)
    print(data)
    for i in data:
        print(i["process"], i["action"])
        if i["process"] in processes:
            result_run = nodeManager(i["action"], i["process"])
            if result_run == False:
                response = Response('Run command fail', status = 500)
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response
        else:
            response = Response('Node not found', status = 500)
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response
    response = Response('Restarted', status = 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/data", methods=['GET'])
def result():
    result =[]
    for process in processes:
        status = Process_mng.status(process)
        result.append({"process":process, "status":status})
    answer = Response(json.dumps(result), status=200, mimetype='application/json')
    answer.headers["Access-Control-Allow-Origin"] = "*"
    return answer

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')
    
    
if __name__ == "__main__":
    app.debug = True
    app.run(host='192.168.0.218', port=3030)