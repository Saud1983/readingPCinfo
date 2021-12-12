import psutil
import re
import sqlite3
import time
import hashlib
from threading import Timer

DEBUG = True  # To give the programmer a choice between starting the program in debugging mode or production mode
conn = sqlite3.connect('win_processes.db', check_same_thread=False)
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


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
        print('Done')


def hasher(path):
    """ This function is to calculate the hash based on sha256 algorithm by passing the 'path' argument, the commented
    lines are to there for future needs purposes to compare between current hash and the previous hash"""

    # correct_sum = "a93969ba56a867f8fae9a5be8c88d2ac26cd2e0cbda0253fa2e4ebb683f3102f" # For future use
    # print('hasher started'+ ' ' + time.strftime('%H:%M:%S'))

    hasher = hashlib.sha256()  # To initialize a variable that uses sha256 algorithm for hashing
    try:
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
        # print('Hasher Finished'+ ' ' + time.strftime('%H:%M:%S'))
    except PermissionError:
        output = 'No Data'
    return output  # Return the result as hexadecimal code


def data_getter():
    # print('Data getter started'+ ' ' + time.strftime('%H:%M:%S'))
    list_of_process_objects = []
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=['pid', 'name', 'memory_percent', 'cpu_percent', 'connections', 'exe', 'cwd'])

            p_info['vms'] = proc.memory_info().vms / (1024 * 1024)
            list_of_process_objects.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # print('Data getter Finished'+ ' ' + time.strftime('%H:%M:%S'))
    return list_of_process_objects


def collect_more_date():
    print('Data Collection ٍStarted' + ' ' + time.strftime('%H:%M:%S'))
    all_process_list = data_getter()

    for i in all_process_list:
        ports = []
        # print("\n")
        # print(f"memory_percent = {i['memory_percent']}")
        mp = i['memory_percent']
        # print(f"Process ID = {i['pid']}")
        pid = i['pid']
        if pid not in processes_ids:
            processes_ids.append(pid)
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
    print('Data Collection Finished'+ ' ' + time.strftime('%H:%M:%S'))



# def user_interact(message):
#     message1 = message
#     # display(message1)
#     choice = input("Please choose from the following"
#                    " '0' To collect new data, "
#                    " '1' to select all data,"
#                    " '2' to select by software,"
#                    " '3' to select by process id,"
#                    " OR"
#                    " Enter '@@' to stop\n")
#
#     if choice == '1':
#         cur.execute("SELECT * FROM processes")
#         all_processes_list = cur.fetchall()
#         for _ in all_processes_list:
#             print(_)
#
#     elif choice == '2':
#         software = input(" Enter software name: \n")
#         cur.execute("SELECT * FROM processes WHERE name=:name ", {'name': software})
#         software_list = cur.fetchall()
#         for _ in software_list:
#             print(_)
#
#     elif choice == '3':
#         process_id = input(" Enter process ID: \n")
#         cur.execute("SELECT * FROM processes WHERE process_id=:process_id ", {'process_id': process_id})
#         process_list = cur.fetchall()
#         for _ in process_list:
#             print(_)
#
#     elif choice == '0':
#         collect_more_date()
#     elif choice == "@@":
#         global running
#         running = False
#     else:
#         print('Invalid Entry')

def analyze_cpu_usage(message):
    display(message)
    for process_id in processes_ids:
        counter = 0
        print(process_id)
        cur.execute("SELECT * FROM processes WHERE process_id=:process_id ", {'process_id': process_id})
        same_process_list = cur.fetchall()
        for _ in same_process_list:
            print(_)
            counter += 1
        print(counter)
        print("="*150)





def display(message):
    print(message + ' ' + time.strftime('%H:%M:%S'))


processes_ids = []
running = True
m = 0
print('Auto data collection + user interaction started')
while running:
    print(f'loop number: {m}')
    if DEBUG:
        DEBUG = False
        timer = RepeatTimer(60, analyze_cpu_usage, ['Analyze CPU Started'])
        timer.start()

    else:
        DEBUG = True
        collect_more_date()
        time.sleep(23)

    m += 1

# if not running:
print('Auto data collection has stopped')
# timer.cancel()

