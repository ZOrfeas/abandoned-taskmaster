import datetime,sys
from FileReader import taskNameIsUnique
from OutputWriter import prettyPrintOneOff,prettyPrintRecurr
suppliedWrapUpFunc = None

def setWrapUpFunc(func):
    suppliedWrapUpFunc = func

def eofSafeInput(promptText):
    try:
        return input(promptText)
    except EOFError:
        if suppliedWrapUpFunc: suppliedWrapUpFunc()
        print("Exiting...")
        sys.exit(0)

def checkAndPrepTimeString(timeStringToCheck):
    properTimesOfDay = {'morning':'09:00','noon':'14:00','afternoon':'18:00','evening':'21:00','night':'00:00','':None}
    if timeStringToCheck not in properTimesOfDay:
        try:
            datetime.datetime(timeStringToCheck, "%H:%M")
            return timeStringToCheck
        except ValueError:
            return None
    else:
        if timeStringToCheck in properTimesOfDay and timeStringToCheck != '':
            timeStringToCheck = properTimesOfDay[timeStringToCheck]
        return timeStringToCheck

def checkAndPrepDateString(dateStringToCheck):
    properDateStrings = ['today','tomorrow','the day after']
    if dateStringToCheck not in properDateStrings and not dateStringToCheck.isnumeric():
        try:
            datetime.datetime.strptime(dateStringToCheck, "%d-%m-%Y")
            return dateStringToCheck
        except ValueError:
            return None
    else:
        if dateStringToCheck == 'today': date = 0
        elif dateStringToCheck == 'tomorrow': date = 1
        elif dateStringToCheck == 'the day after': date = 2
        else: date = dateStringToCheck
        today = datetime.date.today()
        targetDate = today + datetime.timedelta(days=date)
        date = datetime.datetime.strftime(targetDate, "%d-%m-%Y")
        return date

def checkAndPrepDaysTimesString(stringToCheck):
    properDays = ['mon','tue','wed','thu','fri','sat','sun']
    daysTimesSplitted = list(map(lambda x:x.split(), list(map(lambda x:x.strip(), stringToCheck.lower().split(',')))))
    for i in daysTimesSplitted:
        if len(i) == 0 or i[0] not in properDays or(len(i)==2 and checkAndPrepTimeString(i[1]) is None):
            return None   
        elif len(i) == 2:
            i[1] = checkAndPrepTimeString(i[1])
    return daysTimesSplitted

def verifyAndPrepRecurrArgs(argsToCheck):
    argAmount = len(argsToCheck)
    if argAmount >= 1:
        if not taskNameIsUnique(argsToCheck[0]):
            return False,argsToCheck[0]+'not a unique name'
    if argAmount >= 2:
        daysTimes = checkAndPrepDaysTimesString(argsToCheck[1])
        if daysTimes is None:
            return False,argsToCheck[1]
        else:
            argsToCheck[1] = daysTimes
    if argAmount >= 3:
        if (not argsToCheck[2].isnumeric()) and argAmount > 3:
            return False,argsToCheck[2]+' too many args'
        elif argsToCheck[2].isnumeric():
            argsToCheck[2] = int(argsToCheck[2])
    return True,None
   
def verifyAndPrepOneOffArgs(argsToCheck):
    argAmount = len(argsToCheck)
    if argAmount >= 1:
        if not taskNameIsUnique(argsToCheck[0]):
            return False,argsToCheck[0]+' not a unique name'
    if argAmount >= 2:
        date = checkAndPrepDateString(argsToCheck[1])
        if date is None:
            return False,argsToCheck[1]
        else:
            argsToCheck[1] = date
    if argAmount >= 3:
        time = checkAndPrepTimeString(argsToCheck[2])
        if time is None:
            return False,argsToCheck[2]
        else:
            argsToCheck[2] = time
    if argAmount >= 4:
        if argsToCheck[3] not in ['dl','nodl']:
            return False,argsToCheck[3]
        else:
            argsToCheck[3] = True if argsToCheck[3] == 'dl' else False
    if argAmount >= 5:
        if (not argsToCheck[4].isnumeric()) and argAmount > 5:
            return False,argsToCheck[4]+' too many args'
        else:
            argsToCheck[4] = int(argsToCheck[4])
    return True,None

def promptForIsRecurring():
    isRecurring = eofSafeInput("Is it a recurring task?(Y/n):\n").strip()
    if isRecurring not in ['y','n','yes','no']:
        print("Invalid answer, try again or press Ctrl-D to exit")
    else:
        isRecurring = True if isRecurring in ['y','yes'] else False
        return isRecurring     

def promptForTaskName():
        name = eofSafeInput("Give the task a name:\n").strip()
        if name: return name
        else: print("Invalid name, try again or press Ctrl-D to exit")     

def promptForDaysTimes():
    while(True):
        daysTimesString = eofSafeInput("When shall this task repeat?(e.g.: 'Mon 10:10,mon 10:20 , TUE'):\n").strip()
        daysTimesSplitted = checkAndPrepDaysTimesString(daysTimesString)
        if daysTimesSplitted is not None:
            return daysTimesSplitted
        else:
            print("Invalid input, try again or press Ctrl-D to exit")

def promptForDate():
    while(True):
        date = eofSafeInput("Specify the date when the task takes place(dd-mm-yyyy format):\n")
        date = checkAndPrepDateString(date)
        if date is not None:
            return date
        else:
            print("Invalid input, try again or press Ctrl-D to exit")

def promptForTime():
    while(True):
        time = eofSafeInput("Specify at what time(hh:mm 24-hour format) or just press enter:\n").strip()
        time = checkAndPrepTimeString(time)
        if time is not None:
            return time if time != '' else None
        else:
            print("Invalid time, try again or press Ctrl-D to Exit")

def promptForDescription():
    possibleDescription = eofSafeInput("Explain the task in more detail(or just press Enter):\n").strip()
    return possibleDescription if possibleDescription != '' else None

def promptWantsCronAction():
    yesOrNo = eofSafeInput("Do you want to schedule a cron job to occur some time prior?[Y/n(default n)]:\n").strip().lower()
    return (True if yesOrNo in ['yes','y'] else False)

def promptCronMins():
    while(True):
        mins = eofSafeInput("Specify how long (in minutes) would you like the cronjob to take place:\n").strip()
        if mins.isnumeric():
            return int(mins)
        else:
            print("Not a valid number, try again or press Ctrl-D to exit")

def promptCronCommand(cls):
    while(True):
        commandString = eofSafeInput("Specify what the cronjob should be:\n").strip()
        yesOrNo = eofSafeInput("Is the command '{}' ok?[Y/n(default y)]:\n".format(commandString))
        yesOrNo = True if yesOrNo in ['yes','y',''] else False
        if yesOrNo:
            return commandString
        
def promptForIsDeadlined(cls):
    while(True):
        yesOrNo = eofSafeInput("Is this the task's deadline?[Y/n(default n)]:\n").strip().lower()
        return (True if yesOrNo in ['yes','y'] else False)
    
def promptToAddTask():
    while(True):
        yesOrNo = eofSafeInput("Is this task ok?[Y/n(default y)]:\n").strip().lower()
        return (True if yesOrNo in ['yes','y',''] else False)

def resolveDescCron(remainingArgs):
    argAmount = len(remainingArgs)
    cronActionMins = None
    cronAction = None
    description = None
    if argAmount == 0:
        if promptWantsCronAction():
            cronActionMins = promptCronMins()
            cronAction = promptCronCommand()
        description = promptForDescription()
    if argAmount >= 1:
        if not isinstance(remainingArgs[0],int):
            description = remainingArgs[0]
        else:
            cronActionMins = remainingArgs[0]
            cronAction = promptCronCommand() if argAmount < 2 else remainingArgs[1]
            description = promptForDescription() if argAmount < 3 else remainingArgs[2]
    return cronActionMins,cronAction,description

def createRecurring(suppliedArgs):
    taskToRet = {
        "name":None,
        "daysTimes":None,
        "cronActionMins":None,
        "cronAction":None,
        "description":None
    }
    argAmount = len(suppliedArgs)
    taskToRet["name"] = promptForTaskName() if argAmount < 1 else suppliedArgs[0]
    taskToRet["daysTimes"] = promptForDaysTimes() if argAmount < 2 else suppliedArgs[1]
    taskToRet["cronActionMins"],taskToRet["cronAction"],taskToRet["description"] = resolveDescCron(suppliedArgs[2:])
    return taskToRet

def createOneOff(suppliedArgs):
    taskToRet = {
        "name":None,
        "date":None,
        "time":None,
        "isDeadlined":None,
        "cronActionMins":None,
        "cronAction":None,
        "description":None
    }
    argAmount = len(suppliedArgs)
    taskToRet["name"] = promptForTaskName() if argAmount < 1 else suppliedArgs[0]
    taskToRet["date"] = promptForDate() if argAmount < 2 else suppliedArgs[1]
    taskToRet["time"] = promptForTime() if argAmount < 3 else suppliedArgs[2]
    taskToRet["isDeadlined"] = promptForIsDeadlined() if argAmount < 4 else suppliedArgs[3]
    taskToRet["cronActionMins"],taskToRet["cronAction"],taskToRet["description"] = resolveDescCron(suppliedArgs[4:])
    return taskToRet

def askToAddOneOff(task):
    prettyPrintOneOff(task)
    return promptToAddTask()
def askToAddRecurr(task):
    prettyPrintRecurr(task)
    return promptToAddTask()
