'''
Michael Peluso
NJIT ID 31522013
23 March 2023
CS 332 H02
'''

# Import
import sys
import os 
from datetime import date
from datetime import datetime
import math

# Open File
with open("config.txt") as f:
#with open(sys.argv[1]) as f:
    lines = f.readlines()


# Gather config values
confLines = int(lines[0])
unit = lines[1].strip()
numTasks = int(lines[2])
scheduling = lines[3].strip()
timeslice = int(lines[4])
cpuUtil = None
if confLines - numTasks > 5 :
    cpuUtil = tuple(map(int, lines[5].split()))


# Gather task information
tasks = []
for i in range(confLines - numTasks, confLines):
    info = lines[i].split()
    task = {
        'name': info[0],
        'arr': int(info[1]),
        'cpu': int(info[2]),
        'io': int(info[3]),
        'compl' : None,
        'tr' : None,
        'rt' : None,
        'remainingCPU' : int(info[2]),
        'remainingIO' : int(info[3])
    }
    tasks.append(task)

# Extra variables
time = 0
queue = []
ioQueue = []
tasksToComplete = True
remainingTasks = []
currTS = timeslice
util = 0

# Serial Computing
if scheduling == "sc" :

    # Prioritize Tasks
    tasks = sorted(tasks, key = lambda x: (x["arr"], x['name']))

    for t in tasks :
        
        # Wait until task arrives
        while t['arr'] > time :
            time = time + 1
            
        # Run task
        time = time + t['cpu'] + t['io']
        t['compl'] = time
        t['tr'] = time - t['arr']
        t['rt'] = time - ( t['arr'] + t['cpu'] + t['io'] )

        tasks = sorted(tasks, key = lambda x: x['name']) 

        # CPU utilization
        if cpuUtil != None :
            val = min(cpuUtil[1], t['compl'] - t['io']) - max(t['compl'] - t['cpu'] - t['io'], cpuUtil[0])
            if val > 0 :
                util = util + val

    if cpuUtil != None and cpuUtil[1] - cpuUtil[0] > 0 :
        util = util / (cpuUtil[1] - cpuUtil[0]) * 100


# Timesharing
elif scheduling == "ts" :
    tasks = sorted(tasks, key = lambda x: x['name'])
    remainingTasks = tasks.copy()
    queue = tasks.copy()

    # Simulate OS
    while tasksToComplete :

        # Process current I/O
        if len(ioQueue) > 0 :
            t = ioQueue[0]
            t['remainingIO'] = t['remainingIO'] - 1

            # Task I/O complete
            if t['remainingIO'] <= 0 :
                t['compl'] = time
                t['tr'] = t['compl'] - t['arr']
                remainingTasks.remove(t)
                ioQueue.pop(0)

        # Proccess CPU
        t = queue[0]
        if t['arr'] <= time :
        
            # Calculate response time
            t['rt'] = time - t['arr'] if t['rt'] == None else t['rt']
        
            # Process task on CPU
            if t['remainingCPU'] > 0 :
                t['remainingCPU'] = t['remainingCPU'] - 1
                
                # CPU utilization
                if cpuUtil != None and time >= cpuUtil[0] and time <= cpuUtil[1] :
                    util = util + 1

            # Task completed
            if t['remainingCPU'] <= 0 and t not in ioQueue and t['compl'] == None :
                    ioQueue.append(t)

        # Cycle queue
        if time % timeslice == 0 or timeslice == 1 :
            queue.append(queue.pop(0))
                    
        # Incrememnt time
        time = time + 1
                
        # End simulation
        if len(remainingTasks) == 0 :
            tasksToComplete = False

    # CPU utilization calculation
    if cpuUtil != None and cpuUtil[1] - cpuUtil[0] > 0 :
        util = util / (cpuUtil[1] - cpuUtil[0]) * 100


# Multitasking
elif scheduling == "mt" :
    tasks = sorted(tasks, key = lambda x: x['name'])
    remainingTasks = tasks.copy()

    # Preemtive checks
    for t in tasks :

        # Add tasks arriving at time = 0
        if t['arr'] <= 0 :
                queue.append(t)

        # Queue tasks with only I/O
        if t['cpu'] <= 0 and t['io'] > 0 :
            ioQueue.append(t)

        # Disregard empty tasks
        if t['cpu'] <= 0 and t['io'] <= 0 :
            remainingTasks.remove(t)
    
    # Simulate OS
    while tasksToComplete :

        # Process current I/O
        if len(ioQueue) > 0 :
            t = ioQueue[0]
            t['remainingIO'] = t['remainingIO'] - 1

            # Task I/O complete
            if t['remainingIO'] <= 0 :
                t['compl'] = time + 1
                t['tr'] = t['compl'] - t['arr']
                remainingTasks.remove(t)
                ioQueue.pop(0)

            # Cycle I/O queue
            else :
                ioQueue.append(ioQueue.pop(0))

        # Tasks in queue
        if len(queue) > 0 :
            t = queue[0]
        
            # Calculate response time
            t['rt'] = time - t['arr'] if t['rt'] == None else t['rt']
        
            # Process task on CPU
            if t['remainingCPU'] >= 0 :
                t['remainingCPU'] = t['remainingCPU'] - 1
                
                # CPU utilization
                if cpuUtil != None and time > cpuUtil[0] and time <= cpuUtil[1] :
                    util = util + 1

            # Task compeltes on CPU
            if t['remainingCPU'] <= 0 :
                queue.pop(0)
                currTS = timeslice + 1

                # Task completed
                if t['remainingIO'] <= 0 :
                    t['compl'] = time + 1
                    t['tr'] = t['compl'] - t['arr']
                    remainingTasks.remove(t)

                # Add to I/O queue
                elif t not in ioQueue :
                    ioQueue.append(t)

            # Cycle queue
            elif currTS == 1 :
                queue.append(queue.pop(0))
                currTS = timeslice + 1
        else :
            currTS = timeslice + 1
                    
        # Incrememnt time
        time = time + 1
        currTS = currTS - 1

        # Add arriving tasks to queue
        for tsk in tasks :
            if tsk['arr'] <= time and tsk not in queue and tsk not in ioQueue and tsk['compl'] == None:
                queue.append(tsk)
                
        # End simulation
        if len(remainingTasks) == 0 :
            tasksToComplete = False

    # CPU utilization calculation
    if cpuUtil != None and cpuUtil[1] - cpuUtil[0] > 0 :
        util = util / (cpuUtil[1] - cpuUtil[0]) * 100


# Print specs
print(os.path.basename(__file__), ' run  ', date.today().strftime("%m/%d/%y"), '  ', datetime.now().strftime("%H:%M:%S"), '  ', numTasks, ' jobs ; unit of time is ', sep='', end='')

if scheduling == 'sc' :
    print('1', unit, sep='')
    print('SERIAL COMPUTING ', end='')
if scheduling == 'ts' :
    print(timeslice, unit, sep='')
    print('TIMESHARING ', end='')
if scheduling == 'mt' :
    print(timeslice, unit, sep='')
    print('MULTITASKING ', end='')

if cpuUtil != None :
    print('\tCPU utilization [',cpuUtil[0],unit,',',cpuUtil[1],unit,'] is ', '{:.0f}%'.format(util), sep='')
else :
    print('\tCPU utilization unlisted', sep='')

print('\tArr.\tCPU\tI/O\tCompl\tTr\tRt')

for t in tasks :
    i = 9
    for value in t.values():
        if i == 2 :
            break
        i = i - 1
        print(value, end='\t')
    print()

# end of file
