import psutil
import json
import subprocess
import time

available_processes = ['ControlNode','RenderNode','UserNode', 'StorageNode', 'postgresql-x64-13']

class Process:
    def confirm_process(self, process):
        if process in available_processes:
            return True
        else:
            return False


class Process_mng(Process):
    def start(self):
        pass

    def stop(self):
        pass

    def status(self, *processes:str) -> list:
        print(processes)
        statuses = []
        if type(processes) == tuple:
            processes = processes[0]
        for process in processes:
            if self.confirm_process(process):
                process_status = psutil.win_service_get(process).status()
            else: 
                process_status = 'Error'
            statuses.append({"process":process, "status":process_status})
        return statuses

class Response_creater:
    def create_response(status_code, body):
        pass

class Body_parser:
    def parse_body():
        pass

print(Process_mng().status(available_processes))