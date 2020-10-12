#!/usr/bin/python3
import os,sys,subprocess,fileinput,json,datetime
from pathlib import Path

home = str(Path.home())
argumentList = sys.argv[1:]
shortOptions = {
    "h": 1, #help
    "a": 2, #add
    "r": 3, #remove
    "t": 4, #today
    "w": 5, #week
    "d": 6  #day
}
longOptions = {
    "help"   :1,
    "add"    :2,
    "remove" :3,
    "today"  :4,  
    "week"   :5,
    "day"   :6
}
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

def longShortPicker(argument):
    if (len(argument) > 2) and (argument[1] == '-'):
        return longOptions.get(argument[2:], "Invalid")
    elif (len(argument) == 2) and (argument[0] =='-'):
        return shortOptions.get(argument[1:], "Invalid")
    else:
        return "Invalid"


class Taskmaster:

    def grepForDay(targetDateObject):
        targetDate = datetime.datetime.strftime(targetDateObject, "%d-%m-%Y")
        targetDay = datetime.datetime.strftime(targetDateObject, "%a").lower()

        grepPatternRecurring = '"'+targetDay+'"'
        grepPatternOneOffs = '"'+targetDate+'"'

        processRecurring = subprocess.run(['grep',grepPatternRecurring,home+"/.tasksFile"],stdout=subprocess.PIPE,universal_newlines=True)
        processOneOffs = subprocess.run(['grep',grepPatternOneOffs,home+"/.tasksFile"],stdout=subprocess.PIPE,universal_newlines=True)

        targetRecurring = processRecurring.stdout.splitlines()
        targetOneOffs = processOneOffs.stdout.splitlines()
        targetRecurring = list(map(lambda x:json.loads(x),targetRecurring))
        targetOneOffs = list(map(lambda x:json.loads(x),targetOneOffs))
        return (targetRecurring, targetOneOffs)


    def printRecurring(recurringTask,nowDay):
        print(color.red+recurringTask["name"]+color.end)
        timesList = []
        for i in recurringTask["daysTimes"]:
            if i[0]==nowDay and len(i)==2:
                timesList.append(i[1])
        print(color.bold+color.underline+"When:"+color.end)
        if timesList:        
            timesList = sorted(timesList)
            print("At ", end='')
            print(*timesList, sep=", ")
        else:
            print("Anytime")
        if recurringTask["description"] is not None:
            print(color.bold+color.underline+"Info:"+color.end)
            print(recurringTask["description"])

    def printOneOff(oneOffTask):
        print(color.red+oneOffTask["name"]+color.end)
        if oneOffTask["isDeadlined"]: print(color.blue+"!!!DEADLINE!!!"+color.end)
        print(color.bold+color.underline+"When:"+color.end)
        if oneOffTask["time"] is None:
            print("Anytime")
        elif oneOffTask["time"] in ['morning','noon','afternoon','evening','night']:
            print("In the "+oneOffTask["time"]) if oneOffTask["time"] in ["morning","afternoon","evening"] else print("At"+oneOffTask["time"])
        else:
            print("At "+ oneOffTask["time"])
        if oneOffTask["description"] is not None:
            print(color.bold+color.underline+"Info:"+color.end)
            print(oneOffTask["description"])


    def help():
        print(
        '''This is a (real-life) Task Manager cli app.
        Usage: taskmaster OPTION

        -h, --help          prints the current message :)
        -a, --add           adds a task
        -r, --remove        removes a task
        -t, --today         gives current day's schedule
        -w, --week          gives current week's (7 upcoming days) schedule
        -d, --day           gives the schedule at a specific date, or a number of days counting from today
        ''')

    def add():
        print("Adding a task...")
        isRecurring = input("Is it a recurring task?[y/n(default is n)]: \n")
        if isRecurring != 'y' and isRecurring != 'Y' and isRecurring != 'n' and isRecurring != 'N' and isRecurring != '':print("Invalid input"); exit(2)
        isRecurring = True if("n" if isRecurring == '' else isRecurring.lower())=='y' else False
        
        helper = True
        while(helper):
            name = input("Give the task a unique name(hopefully something other than 'exit'): \n")
            process = subprocess.run(['grep','-q','"name": "'+name+'"',home+"/.tasksFile"])
            if process.returncode == 0 or name in ["mon","tue","wed","thu","fri","sat","sun"]: print("Task name exists or is forbidden, try another one")
            else: helper = False
        
        def recurringCreate(name):
            daysTimes = input("Specify when the task shall repeat separated by commas[e.g. Mon|Tue|Wed|Thu|Fri|Sat|Sun 14:15, Tue 12:45...(time can be ommited)]: \n")
            #splits daysTimes seperated by commas after lower-casing them, strips whitespace then splits days and times apart in two piece tuples
            daysTimes = list(map(lambda x:x.split(), list(map(lambda x:x.strip(), daysTimes.lower().split(',')))))
            description = input("Explain the task in more detail if you want to: \n")
            createdTask = {
                "name": name,
                "daysTimes":daysTimes,
                "description":None if description=='' else description
            }
            return createdTask
        def oneOffCreate(name):
            isDeadlined = input("Is this task deadlined?(y/n(default is n): \n")
            isDeadlined = True if("n" if isDeadlined == '' else isDeadlined.lower())=='y' else False
            dateHelper = True
            while(dateHelper):
                date = input("Give the task a date[in DD-MM-YYYY format, 'today','tomorrow','the day after' also work as well as numbers counting up from today(0)]: \n")
                date = date.lower()
                if (date not in ['today','tomorrow','the day after']) and not date.isnumeric():
                    try:
                        datetime.datetime.strptime(date,"%d-%m-%Y")
                    except ValueError:
                        print("Invalid input, try again")
                    else: dateHelper = False
                else:
                    if date == 'today': date = 0
                    elif date == 'tomorrow': date = 1
                    elif date == 'the day after': date = 2
                    today = datetime.date.today()
                    targetDate = today + datetime.timedelta(days=date)
                    date = datetime.datetime.strftime(targetDate,"%d-%m-%Y")
                    dateHelper = False
            timeHelper = True
            while(timeHelper):
                time = input("Is it time specific? If so specify[Hour:Min(24-hour format) or morning|noon|afternoon|evening|night], can also be left empty: \n")
                time = time.lower()
                if (time not in ['morning','noon','afternoon','evening','night','']):
                    try:
                        datetime.datetime.strptime(time,"%H:%M")
                    except ValueError:
                        print("Invalid input, try again")
                    else: timeHelper = False
                else:
                    timeHelper = False
            description = input("Explain the task in more detail if you want to: \n")
            createdTask = {
                "name": name,
                "isDeadlined":isDeadlined,
                "date":date,
                "time":None if time=='' else time,
                "description":None if description=='' else description               
            }
            return createdTask

        taskToAdd = recurringCreate(name) if isRecurring else oneOffCreate(name)

        haveFoundOneEmpty = False
        isDone = False
        for line in fileinput.input([home+"/.tasksFile"],inplace=True):
            if not isDone and len(line.strip()) == 0:
                if isRecurring:
                    line = json.dumps(taskToAdd)+"\n\n"
                    isDone = True
                elif not isRecurring and not haveFoundOneEmpty:
                    haveFoundOneEmpty = True
                elif not isRecurring and haveFoundOneEmpty:
                    line = json.dumps(taskToAdd)+"\n\n"
                    isDone = True
            sys.stdout.write(line)
        print("Task successfully created")
    
    def remove():
        helper = True
        while(helper):
            taskToDelete = input("Specify the name of the task to delete or type 'exit' to exit: \n")
            if taskToDelete == 'exit': print("Exiting..."); exit(0)
            process = subprocess.run(['grep','-q',taskToDelete,home+"/.tasksFile"])
            if process.returncode == 1: print("Task name doesn't exist, try again")
            else: helper = False
        # deleterProcess = subprocess.run(['sed','-i',properString,home+"/.tasksFile"])
        command = "sed -i '/\"name\": \""+taskToDelete+"\"/d' "+home+"/.tasksFile"
        os.system(command)
        print("Task successfully deleted")

                    
    def today():
        dateObject = datetime.date.today()
        todaysDate = datetime.datetime.strftime(dateObject, "%d-%m-%Y")
        todaysDay = datetime.datetime.strftime(dateObject,"%a").lower()

        todaysRecurring,todaysOneOffs = Taskmaster.grepForDay(dateObject)
        
        print('')
        print("                 Today you need to                 ")
        print('')
        if todaysRecurring:
            for i in todaysRecurring:
                Taskmaster.printRecurring(i,todaysDay)
                print("___________________________________________________")
        if todaysOneOffs:
            for i in todaysOneOffs:
                Taskmaster.printOneOff(i)
                print("___________________________________________________")
        if not todaysOneOffs and not todaysRecurring:
            print("                  Do nothing !!(?)                 ")
        else:
            print('')
            print("                    Good luck...                 ")
        print('')

    def week():
        todayDateObject = datetime.datetime.today()
        weekTasks = []
        for i in range(0,7):
            targetDateObject = todayDateObject + datetime.timedelta(days=i)
            weekTasks.append(grepForDay(targetDateObject))
        maxVertical = 0
        for day in weekTasks:
            currDayTasksNr = len(weekTasks[day][0])+len(weekTasks[day][1])
            if currDayTasksNr > maxVertical: maxVertical = currDayTasksNr
        def sortOneDaysTasks(recurring,oneOffs):
            print("kwstas")

    def day():
        dateHelper=True
        while(dateHelper):
            date = input("Which day's schedule?[in DD-MM-YYYY format, 'today','tomorrow','the day after' also work as well as numbers counting up from today(0)]: \n")
            if date == 'today' or date == '0':
                Taskmaster.today()
                exit()
            if(date not in['today','tomorrow','the day after']) and not date.isnumeric():
                try:
                    targetDateObject = datetime.datetime.strptime(date,"%d-%m-%Y")
                except ValueError:
                    print("Invalid input, try again")
                else: dateHelper = False
            else:
                if date == 'today': date = 0
                elif date == 'tomorrow': date = 1
                elif date == 'the day after': date = 2
                today = datetime.date.today()
                targetDateObject = today + datetime.timedelta(days=date)
                dateHelper = False
        targetDate = datetime.datetime.strftime(targetDateObject,"%d-%m-%Y")
        targetDay = datetime.datetime.strftime(targetDateObject,"%a").lower()
        grepPatternRecurring = '"'+targetDay+'"'
        grepPatternOneOffs = '"'+targetDate+'"'

        targetRecurring,targetOneOffs = Taskmaster.grepForDay(targetDateObject)
        print('')
        if date == 1:
            print("                Tomorrow you need to                ")
        else:
            print("             At "+targetDate+" you need to             ")
        print('')
        if targetRecurring:
            for i in targetRecurring:
                Taskmaster.printRecurring(i,targetDay)
                print("___________________________________________________")
        if targetOneOffs:
            for i in targetOneOffs:
                Taskmaster.printOneOff(i)
                print("___________________________________________________")
        if not targetOneOffs and not targetRecurring:
            print("                  Do nothing !!(?)                 ")
        else:
            print('')
            print("                    That's all...                 ")  
        print('') 


    responseFuncs = {
        1:help,
        2:add,
        3:remove,
        4:today,
        5:week,
        6:day
    }
    

    @staticmethod
    def do(caseNumber):
        Taskmaster.responseFuncs.get(caseNumber,help)()

if not os.path.exists(home+"/.tasksFile"):
    temp = open(home+"/.tasksFile","w")
    temp.write("Recurring\n\nOne-offs\n\n")
    temp.close()
    
if len(argumentList) == 1:
    caseNumber = longShortPicker(argumentList[0])
    if caseNumber == "Invalid":
        help()
        exit(0)
    else: Taskmaster.do(caseNumber)
else:
    help()
    exit(0)
