import json,subprocess
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

def fetchConfOptions():
    with open(confFile) as optionsFile:
        fetchedOptions = json.loads(optionsFile.read().strip())
        return fetchedOptions

def nameNotInFile(name,file):
    grepString = '"name": "'+name+'"'
    grepProcess = subprocess.run(['grep','-q',grepString,file])
    return bool(grepProcess.returncode)

def taskNameIsUnique(nameToCheck):
    if nameNotInFile(nameToCheck,recurringTasksFile) and nameNotInFile(nameToCheck,oneOffTasksFile):
        return True
    else:
        return False

def findTaskLocationWithName(taskName):
    if not nameNotInFile(taskName,recurringTasksFile):
        return recurringTasksFile
    elif not nameNotInFile(taskName,oneOffTasksFile):
        return oneOffTasksFile
    else:
        return None

def fetchRecurrTaskWithName(taskName):
    grepProcess = subprocess.run(['grep','"name": "'+taskName+'"',recurringTasksFile], stdout=subprocess.PIPE, universal_newlines=True)
    taskString = grepProcess.stdout.splitlines()
    taskDict = json.loads(taskString)
    return Task(True,taskDict)
def fetchOneOffTaskWithName(taskName):
    grepProcess = subprocess.run(['grep','"name": "'+taskName+'"',oneOffTasksFile], stdout=subprocess.PIPE, universal_newlines=True)
    taskString = grepProcess.stdout.splitlines()
    taskDict = json.loads(taskString)
    return Task(False,taskDict)