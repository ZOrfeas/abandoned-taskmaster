import json,os,datetime

recurringTasksFile = None
oneOffTasksFile = None
confFile = None

def setFileLocations(recurGiven,oneOffGiven,confGiven):
    global recurringTasksFile
    global oneOffTasksFile
    global confFile
    recurringTasksFile = recurGiven
    oneOffTasksFile = oneOffGiven
    confFile = confGiven

def initConfFile():
    with open(confFile,'w') as optionsFile:
        optionsFile.write('{}\n')

def craftOneOffCronJob(task):
    [hour,mins] = task["time"].split(':')
    cronAction = task["cronAction"]
    cronMins = task["cronActionMins"]
    taskDate = datetime.datetime.strptime(task["date"], "%d-%m-%Y")
    realTaskTime = taskDate + datetime.timedelta(hours=int(hour),minutes=int(mins))
    realCronTime = realTaskTime - datetime.timedelta(minutes=int(cronMins))
    [mins,hour,day,month] = datetime.datetime.strftime(realCronTime, "%-M|%-H|%-d|%-m").split('|')
    cronJob = "{} {} {} {} * {}".format(mins,hour,day,month,cronAction)
    return cronJob

def makeCronSelfDelete(cronCommand):
    selfDeletingCron = cronCommand + "; crontab -l | grep -v '"+cronCommand+"' | crontab -"
    return selfDeletingCron

def addCronJob(cronCommand):
    fullCronJob = "(crontab -l ; echo '"+cronCommand+"') | sort -u - | crontab -"
    os.system(fullCronJob)

def addOneOffCronJob(task):
    cronJob = craftOneOffCronJob(task)
    cronJob = makeCronSelfDelete(cronJob)
    addCronJob(cronJob)

def appendTaskToFile(task,file):
    with open(file, 'a') as targetFile:
        targetFile.write(json.dumps(task)+'\n')

def addOneOff(taskToAdd):
    if canAddCron(taskToAdd):
        addOneOffCronJob(taskToAdd)
    scheduleOneOffDeletion(taskToAdd)
    appendTaskToFile(taskToAdd,oneOffTasksFile)

def addRecurring(taskToAdd):
    if canAddCron(taskToAdd):
        addRecurCronJob(taskToAdd)
    appendTaskToFile(taskToAdd,recurringTasksFile)