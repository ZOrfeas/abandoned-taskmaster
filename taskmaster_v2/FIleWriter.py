import json


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

def appendTaskToFile(task,file):
    with open(file, 'a') as targetFile:
        targetFile.write(json.dumps(task)+'\n')

def addOneOff(taskToAdd):
    appendTaskToFile(taskToAdd,oneOffTasksFile)

def addRecurring(taskToAdd):
    appendTaskToFile(taskToAdd,recurringTasksFile)