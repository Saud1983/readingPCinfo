# import win32pdh
# import string
# import win32api
#
#
# def process_ids():
#     # Each instance is a process, you can have multiple processes w/same name
#     junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
#     proc_ids = []
#     proc_dict = {}
#     for instance in instances:
#         if instance in proc_dict:
#             proc_dict[instance] = proc_dict[instance] + 1
#         else:
#             proc_dict[instance] = 0
#     for instance, max_instances in proc_dict.items():
#         for i_num in range(max_instances+1):
#             hq = win32pdh.OpenQuery()  # initializes the query handle
#             path = win32pdh.MakeCounterPath((None, 'process', instance, None, i_num, 'ID Process'))
#             counter_handle = win32pdh.AddCounter(hq, path)
#             win32pdh.CollectQueryData(hq)  # Collects data for the counter
#             type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
#             proc_ids.append((instance, str(val)))
#             win32pdh.CloseQuery(hq)
#
#     proc_ids.sort()
#     return proc_ids
#
#
# print(process_ids())
#
# #-----------------------------------------------------------------------------------------------------
# # http://timgolden.me.uk/pywin32-docs/html/win32/help/process_info.html
# # another try:
#
# import win32pdh, string, win32api
# from win32com.server.exception import COMException
# import win32com.server.util
# import win32com.client.dynamic
#
# #to generate guids use:
# #import pythoncom
# #print pythoncom.CreateGuid()
#
# class pyperf:
#     # COM attributes.
#     _reg_clsid_ = '{763AE791-1D6B-11D4-A38B-00902798B22B}'
#                #guid for your class in registry
#     _reg_desc_ = "get process list and ids"
#     _reg_progid_ = "PyPerf.process" #The progid for this class
#
#     _public_methods_ = ['procids','proclist' ]  #names of callable methods
#     def __init__(self):
#         self.object='process'
#         self.item='ID Process'
#     def proclist(self):
#         try:
#             junk, instances = win32pdh.EnumObjectItems(None,None,self.object, win32pdh.PERF_DETAIL_WIZARD)
#             return instances
#         except:
#             raise COMException("Problem getting process list")
#     def procids(self):
#         #each instance is a process, you can have multiple processes w/same name
#         instances=self.proclist()
#         proc_ids=[]
#         proc_dict={}
#         for instance in instances:
#             if instance in proc_dict:
#                 proc_dict[instance] = proc_dict[instance] + 1
#             else:
#                 proc_dict[instance]=0
#         for instance, max_instances in proc_dict.items():
#             for inum in range(max_instances+1):
#                 try:
#                     hq = win32pdh.OpenQuery() # initializes the query handle
#                     path = win32pdh.MakeCounterPath( (None,self.object,instance, None, inum, self.item) )
#                     counter_handle=win32pdh.AddCounter(hq, path) #convert counter path to counter handle
#                     win32pdh.CollectQueryData(hq) #collects data for the counter
#                     type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
#                     proc_ids.append(instance+'\t'+str(val))
#                     win32pdh.CloseQuery(hq)
#                 except:
#                     pass
#                     # raise COMException("Problem getting process id")
#
#         proc_ids.sort()
#         return proc_ids
#
# a = pyperf()
#
# print(a.proclist())
# print(a.procids())
#
#
#
# if __name__=='__main__':
#     import win32com.server.register
#     win32com.server.register.UseCommandLine(pyperf)
#
#
# def process_ids():
#     # Each instance is a process, you can have multiple processes w/same name
#     junk, instances = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
#     proc_ids = []
#     proc_dict = {}
#     for instance in instances:
#         if instance in proc_dict:
#             proc_dict[instance] = proc_dict[instance] + 1
#         else:
#             proc_dict[instance] = 0
#     for instance, max_instances in proc_dict.items():
#         for i_num in range(max_instances+1):
#             hq = win32pdh.OpenQuery()  # initializes the query handle
#             path = win32pdh.MakeCounterPath((None, 'process', instance, None, i_num, 'ID Process'))
#             counter_handle = win32pdh.AddCounter(hq, path)
#             win32pdh.CollectQueryData(hq)  # Collects data for the counter
#             type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
#             proc_ids.append((instance, str(val)))
#             win32pdh.CloseQuery(hq)
#
#     proc_ids.sort()
#     return proc_ids
#
#
# print(process_ids())
#
#
# #----------------------------------------------------------------------------------------------------
# # Bessssssssssssst code
# import psutil
# import re
# import sqlite3
#
# conn = sqlite3.connect('win_processes.db')
#
# cur = conn.cursor()
#
# cur.execute(""" CREATE TABLE processes (
#             memory_percent real,
#             process_ID integer,
#             name text,
#             memory_usage real,
#             cpu real,
#             ports text,
#             path text,
#             version text
#             )""")
#
#
# def data_getter():
#     list_of_process_objects = []
#     for proc in psutil.process_iter():
#         try:
#             p_info = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'connections', 'exe', 'cwd'])
#
#             p_info['vms'] = proc.memory_info().vms / (1024 * 1024)
#             list_of_process_objects.append(p_info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return list_of_process_objects
#
#
# def collect_more_date():
#     all_process_list = data_getter()
#
#     for i in all_process_list:
#         ports = []
#         # print("\n")
#         # print(f"memory_percent = {i['memory_percent']}")
#         mp = i['memory_percent']
#         # print(f"Process ID = {i['pid']}")
#         pid = i['pid']
#         # print(f"Name = {i['name']}")
#         name = i['name']
#         # print(f"Memory Usage = {i['vms']}")
#         vms = i['vms']
#         # print(f"CPU = {i['cpu_percent']}")
#         cpu = i['cpu_percent']
#         if len(i['connections']) > 0:
#             for x in range(len(i['connections'])):
#                 ports.append(i['connections'][x][3][1])
#         # print(f"Ports = {ports}")
#         prt = str(ports)
#         # print(f"Path = {i['exe']}")
#         path = i['exe']
#         version_pattern = re.compile(r"(\d+ ?$|"
#                                      r"\d+.?\d+ ?$|"
#                                      r"\d+.?\d+.?\d+ ?$|"
#                                      r"\d+.?\d+.?\d+.?\d+ ?$|"
#                                      r"\d+.?\d+.?\d+.?\d+.?\d+ ?$)")
#         if type(i['cwd']) == str:
#             matches = version_pattern.findall(i['cwd'])
#             if len(matches) > 0:
#                 # print(f"Version = {matches[0]}")
#                 version = matches[0]
#             else:
#                 # print(f"Version = Path")  # {i['cwd']}")
#                 version = 'Path'
#         else:
#             # print(f"Version = None")  # {i['cwd']}")
#             version = 'None'
#         with conn:
#             cur.execute("INSERT INTO processes VALUES "
#                         "(:memory_percent, :process_ID, :name, :memory_usage, :cpu, :ports, :path, :version)",
#                         {'memory_percent': mp, 'process_ID': pid, 'name': name, 'memory_usage': vms, 'cpu': cpu,
#                          'ports': prt, 'path': path, 'version': version})
#             conn.commit()
#
#
# collect_more_date()
# running = True
# while running:
#     choice = input("Please choose from the following"
#                    " '1' to select all data,"
#                    " '2' to select by software,"
#                    " '0' To collect new data,"
#                    " OR"
#                    " Enter any other key to stop\n")
#
#     if choice == '1':
#         cur.execute("SELECT * FROM processes")
#         print(cur.fetchall())
#     elif choice == '2':
#         software = input(" Enter software name: \n")
#         cur.execute("SELECT * FROM processes WHERE name=:name ", {'name': software})
#         print(cur.fetchall())
#     elif choice == '0':
#         collect_more_date()
#     else:
#         running = False
#
# # another code to only collect data every 2 max_instancesimport psutil


import psutil
import re
import sqlite3
import time
import hashlib


DEBUG = True  # To give the programmer a choice between starting the program in debugging mode or production mode

conn = sqlite3.connect('win_processes.db')

cur = conn.cursor()

cur.execute(""" CREATE TABLE processes (
            memory_percent real,
            process_ID integer,
            name text,
            memory_usage real,
            cpu real,
            ports text,
            path text,
            hash256 blob,
            version text
            )""")


def hasher(path):
    """ This function is to calculate the hash based on sha256 algorithm by passing the 'path' argument, the commented
    lines are to there for future needs purposes to compare between current hash and the previous hash"""

    # correct_sum = "a93969ba56a867f8fae9a5be8c88d2ac26cd2e0cbda0253fa2e4ebb683f3102f" # For future use

    hasher = hashlib.sha256()  # To initialize a variable that uses sha256 algorithm for hashing
    with open(path, "rb") as f:  # Reading the exe file in binary mode
        while True:  # Infinite loop that only stops using a break if the file has no more content inside
            # good idea not to fill up the memory by reading the full content of a file at once, the file could be huge
            chunk = f.read(524288)  # Temporary variable that holds a different part of a file with limited size
            if not chunk:  # Means if there is no contents to read break the while loop
                break

            # Note: (hashing 'abc' + hashing 'def') will give the same result as hashing 'abcdef' all together
            hasher.update(chunk)  # Add the new part to the hasher for applying the sha256 on it
    output = hasher.hexdigest()  # Is the method to give the hashing result in hexadecimal type

    # For future use to pass to arguments, one is the current path to calculate the hash, and the other is previous hash

    # print("Result:", output)
    # if correct_sum == output:
    #     print("The sums match!", correct_sum, "=", 'cmd_output')
    # else:
    #     print(
    #         "The sums don't match! Check that your inputs were correct",
    #         correct_sum,
    #         "is not equal to",
    #         'cmd_output',
    #     )

    return output  # Return the result as hexadecimal code


def data_getter():
    list_of_process_objects = []
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'connections', 'exe', 'cwd'])

            p_info['vms'] = proc.memory_info().vms / (1024 * 1024)
            list_of_process_objects.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list_of_process_objects


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

        if type(path) == str and len(path) > 15:  # Because some returned paths are NoneType and some aren't paths
            hash256 = hasher(path)
        else:
            hash256 = 'No Hash for this process'

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
                        "(:memory_percent, :process_ID, :name, :memory_usage, :cpu, :ports, :path, :hash256, :version)",
                        {'memory_percent': mp, 'process_ID': pid, 'name': name, 'memory_usage': vms, 'cpu': cpu,
                         'ports': prt,'hash256': hash256, 'path': path, 'version': version})
            conn.commit()


running = True
if DEBUG:
    collect_more_date()
    while running:
        choice = input("Please choose from the following"
                       " '0' To collect new data, "
                       " '1' to select all data,"
                       " '2' to select by software,"
                       " '3' to select by process id,"
                       " OR"
                       " Enter '@@' to stop\n")

        if choice == '1':
            cur.execute("SELECT * FROM processes")
            all_processes_list = cur.fetchall()
            for _ in all_processes_list:
                print(_)
        elif choice == '2':
            software = input(" Enter software name: \n")
            cur.execute("SELECT * FROM processes WHERE name=:name ", {'name': software})
            software_list = cur.fetchall()
            for _ in software_list:
                print(_)
        elif choice == '3':
            process_id = input(" Enter process ID: \n")
            cur.execute("SELECT * FROM processes WHERE process_id=:process_id ", {'process_id': process_id})
            process_list = cur.fetchall()
            for _ in process_list:
                print(_)
        elif choice == '0':
            collect_more_date()
        elif choice == "@@":
            running = False
        else:
            print('Invalid Entry')
else:
    while running:
        collect_more_date()
        time.sleep(30)
