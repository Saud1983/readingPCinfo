import win32pdh
import string
import win32api


def process_ids():
    # Each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids = []
    proc_dict = {}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance] = 0
    for instance, max_instances in proc_dict.items():
        for i_num in range(max_instances+1):
            hq = win32pdh.OpenQuery()  # initializes the query handle
            path = win32pdh.MakeCounterPath((None, 'process', instance, None, i_num, 'ID Process'))
            counter_handle = win32pdh.AddCounter(hq, path)
            win32pdh.CollectQueryData(hq)  # Collects data for the counter
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance, str(val)))
            win32pdh.CloseQuery(hq)

    proc_ids.sort()
    return proc_ids


print(process_ids())

#-----------------------------------------------------------------------------------------------------
# http://timgolden.me.uk/pywin32-docs/html/win32/help/process_info.html
# another try:

import win32pdh, string, win32api
from win32com.server.exception import COMException
import win32com.server.util
import win32com.client.dynamic

#to generate guids use:
#import pythoncom
#print pythoncom.CreateGuid()

class pyperf:
    # COM attributes.
    _reg_clsid_ = '{763AE791-1D6B-11D4-A38B-00902798B22B}'
               #guid for your class in registry
    _reg_desc_ = "get process list and ids"
    _reg_progid_ = "PyPerf.process" #The progid for this class

    _public_methods_ = ['procids','proclist' ]  #names of callable methods
    def __init__(self):
        self.object='process'
        self.item='ID Process'
    def proclist(self):
        try:
            junk, instances = win32pdh.EnumObjectItems(None,None,self.object, win32pdh.PERF_DETAIL_WIZARD)
            return instances
        except:
            raise COMException("Problem getting process list")
    def procids(self):
        #each instance is a process, you can have multiple processes w/same name
        instances=self.proclist()
        proc_ids=[]
        proc_dict={}
        for instance in instances:
            if instance in proc_dict:
                proc_dict[instance] = proc_dict[instance] + 1
            else:
                proc_dict[instance]=0
        for instance, max_instances in proc_dict.items():
            for inum in range(max_instances+1):
                try:
                    hq = win32pdh.OpenQuery() # initializes the query handle
                    path = win32pdh.MakeCounterPath( (None,self.object,instance, None, inum, self.item) )
                    counter_handle=win32pdh.AddCounter(hq, path) #convert counter path to counter handle
                    win32pdh.CollectQueryData(hq) #collects data for the counter
                    type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
                    proc_ids.append(instance+'\t'+str(val))
                    win32pdh.CloseQuery(hq)
                except:
                    pass
                    # raise COMException("Problem getting process id")

        proc_ids.sort()
        return proc_ids

a = pyperf()

print(a.proclist())
print(a.procids())



if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(pyperf)


def process_ids():
    # Each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids = []
    proc_dict = {}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance] = 0
    for instance, max_instances in proc_dict.items():
        for i_num in range(max_instances+1):
            hq = win32pdh.OpenQuery()  # initializes the query handle
            path = win32pdh.MakeCounterPath((None, 'process', instance, None, i_num, 'ID Process'))
            counter_handle = win32pdh.AddCounter(hq, path)
            win32pdh.CollectQueryData(hq)  # Collects data for the counter
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance, str(val)))
            win32pdh.CloseQuery(hq)

    proc_ids.sort()
    return proc_ids


print(process_ids())


#----------------------------------------------------------------------------------------------------
# Bessssssssssssst code
import psutil
import re


def get():
    listOfOricObjects = []
    for proc in psutil.process_iter():
        try:
            # pinfo = proc.as_dict(attrs=['pid','name','memory_percent','cpu_percent','connections','cmdline***',
            #                             'create_time***', 'cwd', 'environ***', 'exe', 'io_counters***', 'ionice***',
            #                             'memory_full_info***', 'memory_info***', 'memory_maps***',
            #                             'nice***', 'num_ctx_switches', 'num_handles', 'num_threads',
            #                             'open_files','ppid', 'status', 'threads', ])
            pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'connections', 'exe',
                                         'cwd'])

            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            listOfOricObjects.append(pinfo)
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass
    return listOfOricObjects
lista = get()


for i in lista:
    ports = []
    print(f"\nmemory_percent = {i['memory_percent']}")
    print(f"Process ID = {i['pid']}")
    print(f"Name = {i['name']}")
    print(f"Memory Usage = {i['vms']}")
    print(f"CPU = {i['cpu_percent']}")
    if len(i['connections']) > 0:
        for x in range(len(i['connections'])):
            ports.append(i['connections'][x][3][1])
    print(f"Ports = {ports}")
    if type(i['exe']) == str:
        print(f"Path = {i['exe']}")
    else:
        print(f"Path = {i['exe']}")
    version = re.compile(r"(\d+ ?$|\d+.?\d+ ?$|\d+.?\d+.?\d+ ?$|\d+.?\d+.?\d+.?\d+ ?$|\d+.?\d+.?\d+.?\d+.?\d+ ?$)")
    if type(i['cwd']) == str:
        matches = version.findall(i['cwd'])
        if len(matches) > 0:
            print(f"cwd = {matches[0]}")
        else:
            print(f"cwd2 = {i['cwd']}")
    else:
        print(f"cwd1 = {i['cwd']}")
