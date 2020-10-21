import json,subprocess
from os import name

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