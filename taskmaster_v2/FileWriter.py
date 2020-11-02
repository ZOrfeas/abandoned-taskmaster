import json,os,datetime
from FileReader import fetchRecurrTaskWithName,fetchOneOffTaskWithName
from Tasks import Task

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
    [hour,mins] = task.time.split(':')
    cronAction = task.cronAction
    cronMins = task.cronMins
    taskDate = datetime.datetime.strptime(task.date, "%d-%m-%Y")
    realTaskTime = taskDate + datetime.timedelta(hours=int(hour),minutes=int(mins))
    realCronTime = realTaskTime - datetime.timedelta(minutes=int(cronMins))
    [mins,hour,day,month] = datetime.datetime.strftime(realCronTime, "%-M|%-H|%-d|%-m").split('|')
    cronJob = "{} {} {} {} * {}".format(mins,hour,day,month,cronAction)
    return cronJob

def craftOneOffDeleter(task):
    taskDate = datetime.datetime.strptime(task.date, "%d-%m-%Y")
    taskDelTime = taskDate + datetime.timedelta(days=1)
    [day,month] = datetime.datetime.strftime(taskDelTime, "%-d|%-m").split('|')
    cronDeleter = "taskmaster.py --delete {}".format(task.name)
    cronJob = "* * {} {} * {}".format(day,month,cronDeleter)
    return cronJob

def craftRecurCronJob(task):
    days = {"sun":0,"mon":1,"tue":2,"wed":3,"thu":4,"fri":5,"sat":6}
    daysFixer = {"mon":7,"tue":1,"wed":2,"thu":3,"fri":4,"sat":5,"sun":6}
    cronJobs = []
    cronAction = task.cronAction
    cronMins = task.cronMins
    for i in task.daysTimes:
        dayObject = datetime.datetime.strptime("Mon", "%a")
        dayObject = dayObject + datetime.timedelta(days=daysFixer[i[0]])
        [hour,mins] = i[1].split(':')
        realTaskTime = dayObject + datetime.timedelta(hours=int(hour),minutes=int(mins))
        realCronTime = realTaskTime - datetime.timedelta(minutes=int(cronMins))
        [mins,hour,day] = datetime.datetime.strftime(realCronTime, "%-M|%-H|%a").split('|')
        day = days[day.lower()]
        cronJob = "{} {} * * {} {}".format(mins,hour,day,cronAction)
        cronJobs.append(cronJob)
    return cronJobs

def makeCronSelfDelete(cronCommand):
    grepString = cronCommand
    selfDeletingCron = cronCommand + "; crontab -l | grep -v -F \""+grepString+"\" | crontab -"
    return selfDeletingCron

def addCronJob(cronCommand):
    fullCronJob = "(crontab -l ; echo '"+cronCommand+"') | sort -u - | crontab -"
    os.system(fullCronJob)

def addOneOffCronJob(task):
    cronJob = craftOneOffCronJob(task)
    cronJob = makeCronSelfDelete(cronJob)
    addCronJob(cronJob)

def scheduleOneOffDeletion(task):
    cronJob = craftOneOffDeleter(task)
    cronJob = makeCronSelfDelete(cronJob)
    addCronJob(cronJob)

def addRecurCronJob(task):
    cronJobs = craftRecurCronJob(task)
    for job in cronJobs: addCronJob(job)

def appendTaskToFile(task,file):
    with open(file, 'a') as targetFile:
        targetFile.write(json.dumps(task.makeDict())+'\n')

def addOneOff(taskToAdd):
    if taskToAdd.wantsCron():
        if not taskToAdd.cronWellDefined():
            print("CronJob requested but some info missing. Reminder: CronJob will take place {} mins before the times specifed".format(taskToAdd.cronMins))
            taskToAdd.resolveCronInconsistencies()
        addOneOffCronJob(taskToAdd)
    scheduleOneOffDeletion(taskToAdd)
    appendTaskToFile(taskToAdd,oneOffTasksFile)

def addRecurring(taskToAdd):
    if taskToAdd.wantsCron():
        if not taskToAdd.cronWellDefined():
            print("CronJob requested but some info missing. Reminder: CronJob will take place {} mins before the times specifed".format(taskToAdd.cronMins))
            taskToAdd.resolveCronInconsistencies()
        addRecurCronJob(taskToAdd)
    appendTaskToFile(taskToAdd,recurringTasksFile)

def deleteCronJob(job):
    grepString = job
    command = "crontab -l | grep -v -F \""+grepString+"\" | crontab -"
    os.system(command)

def deleteRecurrCrons(task):
    cronJobs = craftRecurCronJob(task)
    for job in cronJobs: deleteCronJob(job)

def deleteOneOffCron(task):
    cronJob = craftOneOffCronJob(task)
    deleteCronJob(cronJob)

def deleteOneOffDeleter(task):
    cronJob = craftOneOffDeleter(task)
    deleteCronJob(cronJob)

def deleteNameFromFile(name,file):
    sedCommand = "sed -i '/\"name\": \""+name+"\"/d' "+file
    os.system(sedCommand)

def deleteRecurrWithName(taskName):
    task = Task(True,fetchRecurrTaskWithName(taskName))
    deleteNameFromFile(taskName,recurringTasksFile)
    deleteRecurrCrons(task)

def deleteOneOffWithName(taskName):
    task = Task(False,fetchOneOffTaskWithName(taskName))
    deleteNameFromFile(taskName,oneOffTasksFile)
    deleteOneOffCron(task)
    deleteOneOffDeleter(task)
    

