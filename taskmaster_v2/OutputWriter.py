from datetime import date, datetime, timedelta
import textwrap as tw
import copy

class color:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'
    
def wrongInputMessage(error, caller=None):
    print("taskmaster.py: invalid input -- '{}'".format(error))
    extraString = ''
    if caller is not None:
        extraString = " or 'taskmaster.py {} help'".format(caller)
    print("Try 'taskmaster.py --help'{} for more information".format(extraString))

def helpMessage():
    title =       '                                       TASKMASTER                                       '
    explanation = '                          A cli app to help organize your days                          '
    usage =       'Usage: taskmaster.py [OPTION] [FURTHER ARGS]                                            '
    tip =         'All options can be given FURTHER ARGS but will exit if input is invalid:                '
    command0 =    '  -h, --help                 outputs this help message and exit\n'
    command1 =    '  -c, --create               creates a task, if no FURTHER ARGS are given prompts       \n'
    more1    =    '                             accordingly, use "taskmaster.py -c help" for info     \n'
    command2 =    '  -s, --say, -p              say/print a day\'s, week\'s schedule or all recurring tasks\n'
    more2    =    '                             currently registered, use "taskmaster.py -s help" for info\n'
    command3 =    '  -d, --delete               delete a task by name, use "taskmaster.py -d help" for info\n'
    command4 =    '  -o, --options, --conf      prompts to change the given option, or all if not specified\n'
    more4    =    '                             use "taskmaster.py -o help" for info'
    ctrld    =    'press Ctrl-D to exit from text input prompts'
    splittingLine='----------------------------------------------------------------------------------------'
    examplesString=     'Examples:'
    examples = ''
    print('')
    print(color.bold+title+color.end)
    print(color.bold+splittingLine+color.end)
    print(explanation)
    print('')
    print(usage)
    print(tip)
    print(command0+command1+more1+command2+more2+command3+command4)
    print(ctrld)
    print(color.bold+splittingLine+color.end)
    print(examplesString)
    print(examples)
    print(color.bold+splittingLine+color.end)
    print('Me: Orfeas Zografos')
    print('orfeas.zografos@gmail.com for if you find I f\'ed something up too much')
    print('or to tell me how cool this is(\'nt)')

def creatorHelp():
    print()
def printerHelp():
    print()
def deleterHelp():
    print()

def printDaysTimes(daysTimes):
    last = len(daysTimes) - 1
    for i,pair in enumerate(daysTimes):
        print(*pair, end='')
        if i < last: print(', ', end='')
    print()

def printCronDesc(task):
    cronActionMins = task.cronMins
    cronAction = task.cronAction
    desc = task.description
    if cronActionMins is not None:
        print(color.red+"CronJob:"+color.end, end=' ')
        print("{} mins before the task's time '{}' will be executed.".format(cronActionMins,cronAction))
    print(color.underline+"Details:"+color.end, end=' ')
    print(tw.fill(desc,50)) if desc is not None else print()

def prettyPrintRecurr(taskToPrint):
    print()
    print(color.red+taskToPrint.name+color.end)
    print(color.underline+"On: "+color.end, end='')
    printDaysTimes(taskToPrint.daysTimes)
    printCronDesc(taskToPrint)

def prettyPrintOneOff(taskToPrint):
    print()
    print(color.bold+taskToPrint.name+color.end)
    print(color.underline+"At: "+color.end, end='')
    print(taskToPrint.date, end='')
    print('',end='') if taskToPrint.time is None else print(' '+taskToPrint.time, end='')
    print("(deadline!)") if taskToPrint.isDeadlined == 'dl' else print()
    printCronDesc(taskToPrint)

def printerOptions():
    print("Implement!")

def prepForSort(taskList,dateObject):
    dayOfWeek = dateObject.strftime("%a").lower()
    returnableList = []
    for task in taskList:
        if task.isRecurring:
            for pair in task.daysTimes:
                if pair[0] == dayOfWeek:
                    temp = copy.deepcopy(task)
                    temp.daysTimes = [pair]
                    returnableList.append(temp)
        else:
            returnableList.append(task)
    return returnableList
                
def sortKey(task):
    if task.isRecurring:
        if len(task.daysTimes[0]) == 1: return -1
        else: return datetime.strptime(task.daysTimes[0][1], "%H:%M").strftime("%H:%M")
    else:
        if task.time is None: return -1
        else: return datetime.strptime(task.time, "%H:%M").strftime("%H:%M")

def sortADaysTasks(taskList):
    '''Sort by time a list of tasks on a day'''
    sortedList = sorted(taskList, sortKey)
    return sortedList

def printUpcomingWeek(tasksList):
    today = datetime.today()
    for num,oneDay in enumerate(tasksList):
        temp = prepForSort(oneDay,today + timedelta(days=num))
        sortedTemp = sortADaysTasks(temp)
        

def printWeeklyTasks(tasksList):
    print(tasksList)
def printRequestedDate(tasksList):
    print(tasksList)