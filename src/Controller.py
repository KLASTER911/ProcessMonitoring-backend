import psutil
import json
import subprocess
import time
import platform,socket,re,uuid,json,psutil,logging,GPUtil

available_processes = []

class Process:
    def confirm_process(self, process):
        if process in available_processes:
            return True
        else:
            return False

class Process_mng(Process):
    def start(self, process):
        if not self.confirm_process(process):
            return False
        service = psutil.win_service_get(process)
        if service.status() == 'running':
            return True
        else:
            subprocess.run(f'net start {process}',shell=True)
            while service.status() != 'running':
                time.sleep(5)
                print(f'{process} запускается')
            else:
                return True

    def stop(self,process):
        if not self.confirm_process(process):
            return False
        service = psutil.win_service_get(process)
        if service.status() == 'stopped':
            return True
        else:
            i = 0
            while service.status() != "stopped":
                if i < 20:
                    subprocess.run(f'net stop {process}',shell=True)
                    i+=1
                    time.sleep(3)
                else:
                    subprocess.run(f'taskkill /IM {process}.exe /F', shell=True)
                    
            else:
                return True
        
    def status(self, process):
        return psutil.win_service_get(process).status()
    
    def service_info(self, process):
        return psutil.win_service_get(process).as_dict()

class System_mng:
    def getSystemInfo(self):
        try:
            platform_info=[]
            CPU_info=[]
            memory_info = []
            disk_info = []
            network_info = []
            GPU_info = []

            platform_info.append({
                                'Platform': platform.system(),
                                'Platform-release':platform.release(),
                                'Platform-version':platform.version(),
                                'Architecture':platform.machine(),
                                'Hostname':socket.gethostname(),
                                'Ip-address':socket.gethostbyname(socket.gethostname()),
                                'Mac-address':':'.join(re.findall('..', '%012x' % uuid.getnode())),
                                'Processor':platform.processor(),
                                'Ram':str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"})

            cpufreq = psutil.cpu_freq()                    
            CPU_info.append({
                                "Physical cores:": psutil.cpu_count(logical=False),
                                "Total cores:": psutil.cpu_count(logical=True),
                                "Max Frequency": f"{cpufreq.max:.2f}Mhz",
                                "Min Frequency": f"{cpufreq.min:.2f}Mhz",
                                "Current Frequency": f"{cpufreq.current:.2f}Mhz",
                                "Total CPU Usage": f"{psutil.cpu_percent()}%",
                                "CPU Usage Per Core": [{f"Core {i}": f"{percentage}%" for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1))}]})

            memory_info.append({
                                "Total": f"{self.get_size(psutil.virtual_memory().total)}",
                                "Available": f"{self.get_size(psutil.virtual_memory().available)}",
                                "Used": f"{self.get_size(psutil.virtual_memory().used)}",
                                "Percentage": rf"{psutil.virtual_memory().percent}%"})

            partitions = psutil.disk_partitions()
            for partition in partitions:
                disk_info.append({"Device": rf"{partition.device}", 
                                "Mountpoint": rf"{partition.mountpoint}", 
                                "File system type": rf"{partition.fstype}", 
                                "Total Size": rf"{self.get_size(psutil.disk_usage(partition.mountpoint).total)}",
                                "Used": rf"{self.get_size(psutil.disk_usage(partition.mountpoint).used)}",
                                "Free": rf"{self.get_size(psutil.disk_usage(partition.mountpoint).free)}",
                                "Percentage": rf"{psutil.disk_usage(partition.mountpoint).percent}%"})
            
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        network_info.append({"Interface": f"{interface_name}", 
                                            "IP Address":f"{address.address}",
                                            "Netmask":f"{address.netmask}",
                                            "Broadcast IP":f"{address.broadcast}"})
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        network_info.append({"Interface": f"{interface_name}", 
                                            "MAC Address":f"{address.address}",
                                            "Netmask":f"{address.netmask}",
                                            "Broadcast MAC":f"{address.broadcast}"}) 

            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                # gpu_id = gpu.id
                # gpu_name = gpu.name
                # gpu_load = f"{gpu.load*100}%"
                # gpu_free_memory = f"{gpu.memoryFree}MB"
                # gpu_used_memory = f"{gpu.memoryUsed}MB"
                # gpu_total_memory = f"{gpu.memoryTotal}MB"
                # gpu_temperature = f"{gpu.temperature} °C"
                # gpu_uuid = gpu.uuid
                GPU_info.append({
                    "Id":gpu.id, 
                    "Name":gpu.name, 
                    "Load":f"{gpu.load}%", 
                    "Free memory":f"{gpu.memoryFree} MB", 
                    "Used memory":f"{gpu.memoryUsed} MB",
                    "Total memory":f"{gpu.memoryTotal} MB", 
                    "Temperature":f"{gpu.temperature} C", 
                    "UUId":gpu.uuid})

            
            return {"Platform Info":platform_info,
                    "CPU Info":CPU_info,
                    "Memory Info":memory_info,
                    "Disk Info":disk_info,
                    "Network Info":network_info,
                    "GPU info":GPU_info,}

        except Exception as e:
            logging.exception(e)

    def get_size(self, bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor