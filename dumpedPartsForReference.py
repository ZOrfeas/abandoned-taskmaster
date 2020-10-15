def createTask(cls,creatorArguments):
    isRecurringArgs = ['recur','r','recurring']
    isOneOffArgs = ['once','o','oneoff']
    isDeadlinedArgs = ['dl','deadlined','nodl']
  
    argAmount = len(creatorArguments)
    if argAmount == 0:
        name = cls.inputReader.promptForTaskName()
        isRecurring = cls.inputReader.promptForIsRecurring()
        taskToAdd,error = cls.inputReader.promptRecurring() if isRecurring else cls.inputReader.promptOneOff()
    elif argAmount == 1:
        name = creatorArguments[0]
        isRecurring = cls.inputReader.getIsRecurring()
        taskToAdd,error = cls.inputReader.promptRecurring() if isRecurring else cls.inputReader.promptOneOff()
    else:
        name = creatorArguments[0]
        isRecurringCandidate =creatorArguments[1].lower()
        if isRecurringCandidate in isRecurringArgs:
            isRecurring = isRecurringCandidate
            taskToAdd,error = cls.inputReader.promptRecurring(creatorArguments[2:])
        elif isRecurringCandidate in isOneOffArgs:
            isRecurring = isRecurringCandidate
            taskToAdd,error = cls.inputReader.promptOneOff(creatorArguments[2:])
        else:
            cls.outputWriter.wrongInputMessage(creatorArguments[1],'-c')
            return 1
    if taskToAdd is None:
        cls.outputWriter.wrongInputMessage(creatorArguments[error],'-c')
        return 1
    elif isRecurring:
        taskToAdd["name"]=name
        cls.FileWriter.addRecurring(taskToAdd)
    else:
        taskToAdd["name"]=name
        cls.FileWriter.addOneOff(taskToAdd)
    
def promptRecurring(cls,suppliedArgs,wrapUpFunc=None):
    taskToRet = {
        "name":None,
        "daysTimes":None,
        "cronActionMins":None,
        "cronAction":None,
        "description":None
    }
    properDays = ['mon','tue','wed','thu','fri','sat','sun']
    nrOfSuppliedArgs = len(suppliedArgs)
    if nrOfSuppliedArgs == 0:
        notYetFoundDays = True
        while(True):
            daysTimes = cls.eofSafeInput("When does this task repeat?(e.g.: Mon 10:10, thu 20:24, SAT 23:59, Tue):\n")
            daysTimesSplitted = list(map(lambda x:x.split(), list(map(lambda x:x.strip(), daysTimes.lower().split(',')))))
            for i in daysTimesSplitted:
                if len(i)==0 or i[0] not in properDays or (len(i)==2 and not cls.isProperTimeString(i[1])):
                    print("Invalid times/days, try again or press Ctrl-D to exit")
                    continue
                else:
                    notYetFoundDays = False
    else:
        daysTimes = suppliedArgs[0]
        daysTimesSplitted = list(map(lambda x:x.split(), list(map(lambda x:x.strip(), daysTimes.lower().split(',')))))
        for i in daysTimesSplitted:
            if len(i)==0 or i[0] not in properDays or (len(i)==2 and not cls.isProperTimeString(i[1])):
                return None,2
    taskToRet["daysTimes"] = daysTimesSplitted
    if nrOfSuppliedArgs == 1:
        if cls.wantsCronAction():
            taskToRet["cronActionMins"] = cls.askCronMins()
            taskToRet["cronAction"] = cls.askCronCommand()
        possibleDescription = cls.eofSafeInput("Explain the task in more detail if you want:\n")
        taskToRet["description"] = possibleDescription if possibleDescription!='' else None
    if nrOfSuppliedArgs == 2:
        if suppliedArgs[1].isnumeric():
            taskToRet["cronActionMins"] = suppliedArgs[1]
            taskToRet["cronAction"] = cls.askCronCommand()
            possibleDescription = cls.eofSafeInput("Explain the task in more detail if you want:\n")
            taskToRet["description"] = possibleDescription if possibleDescription!='' else None 
        else:
            taskToRet["description"] = suppliedArgs[1]
    if nrOfSuppliedArgs == 3:
        if suppliedArgs[1].isnumeric():
            taskToRet["cronActionMins"] = suppliedArgs[1]
            taskToRet["cronAction"] = suppliedArgs[2]
            possibleDescription = cls.eofSafeInput("Explain the task in more detail if you want:\n")
            taskToRet["description"] = possibleDescription if possibleDescription!='' else None
        else:
            return None,3
    if nrOfSuppliedArgs == 4:
        if suppliedArgs[1].isnumeric():
            taskToRet["cronActionMins"] = suppliedArgs[1]
            taskToRet["cronAction"] = suppliedArgs[2]
            taskToRet["description"] = suppliedArgs[3]
        else:
            return None,3
    return taskToRet,-1