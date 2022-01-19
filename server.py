from urllib import response
from flask import Flask, send_from_directory
from flask import request, Response, make_response, render_template
from flask_cors import CORS, cross_origin
import psutil
import json
import subprocess
import time

from werkzeug.datastructures import ContentRange

from src.Controller import *
app = Flask(__name__)#, template_folder='C:\\Users\\Admin\\Desktop\\Server\\my-app\\build\\', static_folder='C:\\Users\\Admin\\Desktop\\Server\\my-app\\build\\static')
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.route("/getList", methods = ['GET'])
def getList():
    response = Response(json.dumps(available_processes), status=200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/service/<name>/start", methods=['POST'])
def service_start(name):
    if Process_mng().start(name) == True:
        return Response(status=200)
    return Response('Start was failed', status=500)

@app.route("/service/<name>/stop", methods=['POST'])
def service_stop(name):
    if Process_mng().stop(name) == True:
        return Response(status=200)
    return Response('Stop was failed', status=500)

@app.route("/service/<name>/restart", methods=['POST'])
def service_restart(name):
    stop = Process_mng().stop(name)
    start = Process_mng().start(name)
    if stop == True and start == True:
        return Response(status=200)
    return Response('Restart was failed', status=500)

@app.route('/service/<name>/getInfo', methods = ['GET'])
def service_info(name):
    try:
        body = json.dumps({'info':[Process_mng().service_info(name)]})
        response = Response(body, status=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["content-type"] = "application/json; charset=utf-8"
        return response
    except:
        return Response('No data was received.', status=500)

@app.route('/getSystemData', methods=['GET'])
def getSystemData():
    try:
        body = json.dumps(System_mng().getSystemInfo())
        response = Response(body, status=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["content-type"] = "application/json; charset=utf-8"
        return response
    except:
        return Response('No data was received.', status=500)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')
    
    
if __name__ == "__main__":
    app.debug = True
    app.run(host='192.168.0.218', port=3030)









# def nodeManager(action, process):
#     if action == 'start' or action == 'stop':
#         subprocess.run(f'net {action} {process}',shell=True)
#     elif action ==  'restart':
#         subprocess.run(f'net stop {process}',shell=True)
#         time.sleep(2)
#         subprocess.run(f'net start {process}',shell=True)
#     else:
#         print("Неверный параметр.")
#         return False

# @app.route("/data", methods=['POST'])
# def get_data():
#     # body = str(request.data, 'utf-8') #dict(json.loads(request.data))
#     # print('req body: ', body)
#     # data = json.JSONDecoder().decode(body)
#     data = json.loads(request.data)
#     #print(data)
#     for i in data:
#         print(i["process"], i["action"])
#         if i["process"] in available_processes:
#             result_run = nodeManager(i["action"], i["process"])
#             if result_run == False:
#                 response = Response('Run command fail', status = 500)
#                 response.headers["Access-Control-Allow-Origin"] = "*"
#                 return response
#         else:
#             response = Response('Node not found', status = 500)
#             response.headers["Access-Control-Allow-Origin"] = "*"
#             return response
#     response = Response('Restarted', status = 200)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response

# @app.route("/data", methods=['GET'])
# def result():
#     #result =[]
#     # for process in processes:
#     #     status = Process_mng().status(available_processes)
#     #     #result.append({"process":process, "status":status})
#     answer = Response(json.dumps(Process_mng().status(available_processes)), status=200, mimetype='application/json')
#     answer.headers["Access-Control-Allow-Origin"] = "*"
#     return answer