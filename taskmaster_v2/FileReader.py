import json,subprocess,datetime
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
    taskString = grepProcess.stdout.splitlines()[0]
    taskDict = json.loads(taskString)
    return taskDict
def fetchOneOffTaskWithName(taskName):
    grepProcess = subprocess.run(['grep','"name": "'+taskName+'"',oneOffTasksFile], stdout=subprocess.PIPE, universal_newlines=True)
    taskString = grepProcess.stdout.splitlines()[0]
    taskDict = json.loads(taskString)
    return taskDict

def fetchDateOneOffs(dateString):
    grepProcess = subprocess.run(['grep','"date": "'+dateString+'"',oneOffTasksFile], stdout=subprocess.PIPE, universal_newlines=True)
    taskList = grepProcess.stdout.splitlines()
    taskDictsTypes = list(map(lambda x:(False,json.loads(x)), taskList))
    return taskDictsTypes

def fetchDayRecurrs(dayString):
    grepProcess = subprocess.run(['grep','\["'+dayString+'"',recurringTasksFile], stdout=subprocess.PIPE, universal_newlines=True)
    taskList = grepProcess.stdout.splitlines()
    taskDictsTypes = list(map(lambda x:(True,json.loads(x)), taskList))
    return taskDictsTypes

def fetchDateTaskDictsAndTypes(dateString):
    dayOfWeek = datetime.datetime.strptime(dateString, "%d-%m-%Y").strftime("%a").lower()
    oneOffs = fetchDateOneOffs(dateString)
    recurrs = fetchDayRecurrs(dayOfWeek)
    return oneOffs + recurrs

def fetchUpComingWeekTaskDictsAndTypes():
    todayObj = datetime.date.today()
    weekTaskList = []
    for offset in range(0,7):
        targetDateObj = todayObj + datetime.timedelta(days=offset)
        targetDate = targetDateObj.strftime("%d-%m-%Y")
        weekTaskList.append(fetchDateTaskDictsAndTypes(targetDate))
    return weekTaskList
    
def fetchWeeklyTaskDictsAndTypes():
    daysOfWeek = {0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat",6:"sun"}
    weeklyTaskList = []
    for day in range(0,7):
        weeklyTaskList.append(fetchDayRecurrs(daysOfWeek[day]))
    return weeklyTaskList
