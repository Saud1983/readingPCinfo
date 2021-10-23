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
import sqlite3

conn = sqlite3.connect('memory.db')

cur = conn.cursor()

cur.execute(""" CREATE TABLE processes (
            memory_percent real,
            process_ID integer,
            name text,
            memory_usage real,
            cpu real,
            ports text,
            path text,
            version text
            )""")


def data_getter():
    list_of_oric_objects = []
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'connections', 'exe', 'cwd'])

            p_info['vms'] = proc.memory_info().vms / (1024 * 1024)
            list_of_oric_objects.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_oric_objects


def collect_more_date():
    all_process_list = data_getter()

    for i in all_process_list:
        ports = []
        # print("\n")
        # print(f"memory_percent = {i['memory_percent']}")
        mp = i['memory_percent']
        # print(f"Process ID = {i['pid']}")
        pid = i['pid']
        # print(f"Name = {i['name']}")
        name = i['name']
        # print(f"Memory Usage = {i['vms']}")
        vms = i['vms']
        # print(f"CPU = {i['cpu_percent']}")
        cpu = i['cpu_percent']
        if len(i['connections']) > 0:
            for x in range(len(i['connections'])):
                ports.append(i['connections'][x][3][1])
        # print(f"Ports = {ports}")
        prt = str(ports)
        # print(f"Path = {i['exe']}")
        path = i['exe']
        version_pattern = re.compile(r"(\d+ ?$|"
                                     r"\d+.?\d+ ?$|"
                                     r"\d+.?\d+.?\d+ ?$|"
                                     r"\d+.?\d+.?\d+.?\d+ ?$|"
                                     r"\d+.?\d+.?\d+.?\d+.?\d+ ?$)")
        if type(i['cwd']) == str:
            matches = version_pattern.findall(i['cwd'])
            if len(matches) > 0:
                # print(f"Version = {matches[0]}")
                version = matches[0]
            else:
                # print(f"Version = Path")  # {i['cwd']}")
                version = 'Path'
        else:
            # print(f"Version = None")  # {i['cwd']}")
            version = 'None'
        with conn:
            cur.execute("INSERT INTO processes VALUES "
                        "(:memory_percent, :process_ID, :name, :memory_usage, :cpu, :ports, :path, :version)",
                        {'memory_percent': mp, 'process_ID': pid, 'name': name, 'memory_usage': vms, 'cpu': cpu,
                         'ports': prt, 'path': path, 'version': version})
            conn.commit()


collect_more_date()
running = True
while running:
    choice = input("Please choose from the following"
                   " '1' to select all data,"
                   " '2' to select by software,"
                   " '0' To collect new data,"
                   " OR"
                   " Enter any other key to stop\n")

    if choice == '1':
        cur.execute("SELECT * FROM processes")
        print(cur.fetchall())
    elif choice == '2':
        software = input(" Enter software name: \n")
        cur.execute("SELECT * FROM processes WHERE name=:name ", {'name': software})
        print(cur.fetchall())
    elif choice == '0':
        collect_more_date()
    else:
        running = False

#--------------------------------------------------------------------------------------
# Test code for reading a dictionary

# {'client00': {'account_info': {
# 'account_balance': 0,
# 'account_id': 1022821753,
# 'account_password': '0000',
# 'account_type': 'normal'},
# 'personal_info': {
# 'National_id': 1022818684,
# 'first_name': 'Khalid',
# 'last_name': 'Waleed',
# 'mobile_no': 500053197}},
# 'client0': {'account_info': {
# 'account_balance': 0,
# 'account_id': 1066865284,
# 'account_password': '0000',
# 'account_type': 'normal'},
# 'personal_info': {'National_id': 1066858745,
# 'first_name': 'Ali',
# 'last_name': 'Ahmed',
# 'mobile_no': 533222025}}}

import ast, pprint, re



running = True
while running:  # Program starts here.
    choice1 = input("Enter the account number, or"
                    " '1' to create a new account,"
                    " '2' to check the clients book"
                    " '0' to stop the program :\n")
    a='a-zA-Z'
    account = '1066865284'

    pattern = re.compile(fr"'[{a}]+_[{a}]+': ?{account},")
    with open('clients_book.txt', 'r+') as c:
        # cont = c.read()
        matches = pattern.findall(c.read())
        for m in matches:
            print(m)
        # dictionary = ast.literal_eval(matches)
        dictionary = {}
    if choice1 == "2":  # 3rd choice
        # print(dictionary)
        choice1 = '1066865284'



        for element in dictionary.items():
            if str(element[1]['account_info']['account_id']) == choice1:  # Here the choice can be an account number
                item = element[1]
                pprint.pprint(item)
