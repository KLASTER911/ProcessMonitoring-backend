import psutil
print(psutil.win_service_get('StorageNode').as_dict())
from src.Controller import *
print(json.dumps(System_mng().getSystemInfo()))