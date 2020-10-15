#!/usr/bin/python3
import sys,os,json,subprocess,datetime
from pathlib import Path



class Taskmaster:
    
    tasksFolderLocation = str(Path.home())+"/.tasksFolder"
    recurringTasksFile = tasksFolderLocation+"/recurringTasks"
    oneOffTasksFile = tasksFolderLocation+"/oneOffTasks"
    confFile = tasksFolderLocation+"/conf"
    
    options = {}

    class FileWriter:
        
        @staticmethod
        def initConfFile():
            with open(Taskmaster.confFile,'w') as optionsFile:
                optionsFile.write('{}\n')
    
    class FileReader:
        
        @staticmethod
        def fetchConfOptions():
            with open(Taskmaster.confFile) as optionsFile:
                fetchedOptions = json.loads(optionsFile.read().strip())
                return fetchedOptions
        
    
    class outputWriter:

        color = {
            "purple": '\033[95m',
            "cyan": '\033[96m',
            "darkcyan": '\033[36m',
            "blue": '\033[94m',
            "green": '\033[92m',
            "yellow": '\033[93m',
            "red": '\033[91m',
            "bold": '\033[1m',
            "underline": '\033[4m',
            "end": '\033[0m'
        }
        @classmethod
        def helpMessage(cls):
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
            print(cls.color["bold"]+title+cls.color["end"])
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print(explanation)
            print('')
            print(usage)
            print(tip)
            print(command0+command1+more1+command2+more2+command3+command4)
            print(ctrld)
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print(examplesString)
            print(examples)
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print('Me: Orfeas Zografos')
            print('orfeas.zografos@gmail.com for if you find I f\'ed something up too much')
            print('or to tell me how cool this is(\'nt)')
            
        @classmethod
        def wrongInputMessage(cls,invalidInput,caller=None):
            print("taskmaster.py: invalid input -- '{}'".format(invalidInput))
            extraString = ''
            if caller is not None:
                extraString = " or 'taskmaster.py {} help'".format(caller)
            print("Try 'taskmaster.py --help'{} for more information".format(extraString))
    
    class inputReader:
        
        suppliedWrapUpFunc = None
        @classmethod
        def eofSafeInput(cls,promptText):
            try:
                return input(promptText)
            except EOFError:
                if cls.suppliedWrapUpFunc: cls.suppliedWrapUpFunc()
                print("Exiting...")
                sys.exit(0)
        @classmethod
        def isProperTimeString(cls,timeStringToCheck):
            properTimesOfDay = ['morning','noon','afternoon','evening','night']
            if timeStringToCheck not in properTimesOfDay:
                try:
                    datetime.datetime.strptime(timeStringToCheck, "%H:%M")
                    return True
                except ValueError:
                    return False
            else:
                return True
        @classmethod
        def checkAndPrepDateString(cls,dateStringToCheck):
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
                today = datetime.date.today()
                targetDate = today + datetime.timedelta(days=date)
                date = datetime.datetime.strftime(targetDate, "%d-%m-%Y")
                return date
        @classmethod
        def checkAndPrepDaysTimesString(cls,stringToCheck):
            properDays = ['mon','tue','wed','thu','fri','sat','sun']
            daysTimesSplitted = list(map(lambda x:x.split(), list(map(lambda x:x.strip(), stringToCheck.lower().split(',')))))
            for i in daysTimesSplitted:
                if len(i) == 0 or i[0] not in properDays or(len(i)==2 and not cls.isProperTimeString(i[1])):
                    return None
            return daysTimesSplitted
        @classmethod
        def verifyAndPrepRecurrArgs(cls,argsToCheck):
            argAmount = len(argsToCheck)
            if argAmount >= 1:
                if not Taskmaster.FileReader.taskNameIsUnique(argsToCheck[0]):
                    return False,argsToCheck[0]+'not a unique task name'
            if argAmount >= 2:
                daysTimes = cls.checkAndPrepDaysTimesString(argsToCheck[1])
                if daysTimes is None:
                    return False,argsToCheck[1]
                else:
                    argsToCheck[1] = daysTimes
            if argAmount >= 3:
                if not argsToCheck[2].isnumeric() and argAmount > 3:
                    return False,argsToCheck[2]+'too many args'
                else:
                    argsToCheck[2] = int(argsToCheck[2])
            return True,None
        @classmethod
        def verifyAndPrepOneOffArgs(cls,argsToCheck):
            argAmount = len(argsToCheck)
            if argAmount >= 1:
                if not Taskmaster.FileReader.taskNameIsUnique(argsToCheck[0]):
                    return False,argsToCheck[0]+'not a unique task name'
            if argAmount >= 2:
                date = checkAndPrepDateString(argsToCheck[1])
                if date is None:
                    return False,argsToCheck[1]
                else:
                    argsToCheck[1] = date
            if argAmount >= 3:
                if not cls.isProperTimeString(argsToCheck[2]):
                    return False,argsToCheck[2]
            if argAmount >= 4:
                lowerCasedArg = argsToCheck[3].lower()
                if lowerCasedArg not in ['y','n','yes','no']:
                    return False,argsToCheck[3]
                else:
                    argsToCheck[3] = True if lowerCasedArg in ['y','yes'] else False
            if argAmount >= 5:
                if not argsToCheck[4].isnumeric() and argAmount > 5:
                    return False,argsToCheck[4]
                else:
                    argsToCheck[4] = int(argsToCheck[4])
            return True,None
        
        @classmethod
        def promptForIsRecurring(cls):
            while(True):
                isRecurring = cls.eofSafeInput("Is it a recurring task?(Y/n):").strip()
                if isRecurring not in ['y','n','yes','no']:
                    print("Invalid answer, try again or press Ctrl-D to exit")
                else:
                    isRecurring = True if isRecurring in ['y','yes'] else False
                    return isRecurring    
        @classmethod
        def promptForTaskName(cls):
            while(True):
                name = cls.eofSafeInput("Give the task a name:\n").strip()
                if name: return name
                else: print("Invalid name, try again or press Ctrl-D to exit")
        @classmethod
        def promptForDaysTimes(cls):
            while(True):
                daysTimesString = cls.eofSafeInput("When shall this task repeat?(e.g.: 'Mon 10:10,mon 10:20 , TUE'):\n").strip()
                daysTimesSplitted = cls.checkAndPrepDaysTimesString(daysTimesString)
                if daysTimesSplitted is not None:
                    return daysTimesSplitted
                else:
                    print("Invalid input, try again or press Ctrl-D to exit")
        @classmethod
        def promptForDate(cls):
            while(True):
                date = cls.eofSafeInput("Specify the date when the task takes place(dd-mm-yyyy format):\n")
                if cls.isProperDateString(date):
                    return date
                else:
                    print("Invalid input, try again or press Ctrl-D to exit")
        @classmethod
        def promptForTime(cls):
            while(True):
                time = cls.eofSafeInput("Specify at what time")
        @classmethod
        def promptForDescription(cls):
            possibleDescription = cls.eofSafeInput("Explain the task in more detail(or just press Enter):\n").strip()
            return possibleDescription if possibleDescription != '' else None
        @classmethod
        def promptWantsCronAction(cls):
            yesOrNo = cls.eofSafeInput("Do you want to schedule a cron job to occur some time prior?[Y/n(default n)]:\n").strip().lower()
            return (True if yesOrNo in ['yes','y'] else False)
        @classmethod
        def promptCronMins(cls):
            while(True):
                mins = cls.eofSafeInput("Specify how long (in minutes) would you like the cronjob to take place:\n").strip()
                if mins.isnumeric():
                    return int(mins)
                else:
                    print("Not a valid number, try again or press Ctrl-D to exit")
        @classmethod
        def promptCronCommand(cls):
            while(True):
                commandString = cls.eofSafeInput("Specify what the cronjob should be:\n").strip()
                yesOrNo = cls.eofSafeInput("Is the command '{}' ok?[Y/n(default y)]:\n".format(commandString))
                yesOrNo = True if yesOrNo in ['yes','y',''] else False
                if yesOrNo:
                    return commandString

        @classmethod
        def resolveDescCron(cls,remainingArgs):
            argAmount = len(remainingArgs)
            cronActionMins = None
            cronAction = None
            description = None
            if argAmount == 0:
                if cls.promptWantsCronAction():
                    cronActionMins = cls.promptCronMins()
                    cronAction = cls.promptCronCommand()
                description = cls.promptForDescription()
            if argAmount >= 1:
                if not isinstance(remainingArgs[0],int):
                    description = remainingArgs[0]
                else:
                    cronActionMins = remainingArgs[0]
                    cronAction = cls.promptCronCommand() if argAmount < 2 else remainingArgs[1]
                    description = cls.promptForDescription() if argAmount < 3 else remainingArgs[2]
            return cronActionMins,cronAction,description
        @classmethod
        def createRecurring(cls,suppliedArgs):
            taskToRet = {
                "name":None,
                "daysTimes":None,
                "cronActionMins":None,
                "cronAction":None,
                "description":None
            }
            argAmount = len(suppliedArgs)
            taskToRet["name"] = cls.promptForTaskName() if argAmount < 1 else suppliedArgs[0]
            taskToRet["daysTimes"] = cls.promptForDaysTimes() if argAmount < 2 else suppliedArgs[1]
            taskToRet["cronActionMins"],taskToRet["cronAction"],taskToRet["description"] = cls.resolveDescCron(suppliedArgs[2:])
            return taskToRet


        @classmethod
        def createOneOff(cls,suppliedArgs):
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
            taskToRet["name"] = cls.promptForTaskName() if argAmount < 1 else suppliedArgs[0]
            taskToRet["date"] = cls.promptForDate() if argAmount < 2 else suppliedArgs[1]
            taskToRet["time"] = cls.promptForTime() if argAmount < 3 else suppliedArgs[2]
            taskToRet["isDeadlined"] = cls.promptForIsDeadlined() if argAmount < 4 else suppliedArgs[3]
            taskToRet["cronActionMins"],taskToRet["cronAction"],taskToRet["description"] = cls.resolveDescCron(suppliedArgs[4:])
            return taskToRet

    @classmethod
    def help(cls):
        cls.outputWriter.helpMessage()
        return 0

    @classmethod
    def createTask(cls,creatorArguments):
        isRecurringProperArgs = ['recur','r','recurring']
        isOneOffProperArgs = ['once','o','oneoff']
        isDeadlinedProperArgs =['dl','deadlined','nodl']
        argAmount = len(creatorArguments)
        if argAmount == 0:
            isRecurring = cls.inputReader.promptForIsRecurring()
        else:
            isRecurringCandidate = creatorArguments[0]
            if isRecurringCandidate in isRecurringProperArgs:
                isRecurring = True
            elif isRecurringCandidate in isOneOffProperArgs:
                isRecurring = False
            else:
                cls.outputWriter.wrongInputMessage(creatorArguments[0],'-c')
                return 1
        taskDetails = creatorArguments[1:]
        argsOk,wrongArg = cls.inputReader.verifyAndPrepRecurrArgs(taskDetails) if isRecurring else cls.inputReader.verifyAndPrepOneOffArgs(taskDetails)
        if not argsOk:
            cls.outputWriter.wrongInputMessage(wrongArg, '-c')
            return 1
        else:
            taskToAdd = cls.inputReader.createRecurring(taskDetails) if isRecurring else cls.inputReader.createOneOff(taskDetails)
        if isRecurring:
            if creatorArguments <= 1 or cls.outputWriter.askToAddRecurr(taskToAdd):
                cls.FileWriter.addRecurring(taskToAdd)
        else:
            if creatorArguments <= 1 or cls.outputWriter.askToAddOneOff(taskToAdd):
                cls.FileWriter.addOneOff(taskToAdd)
        return 0
        
    @classmethod
    def printSchedule(cls,printerArguments):
        print("Entered printSchedule")
    @classmethod
    def deleteTask(cls,deleteArguments):
        print("Entered deleteTask")
    @classmethod
    def configure(cls,confArgumets):
        if os.stat(cls.confFile).st_size == 0:
            cls.FileWriter.initConfFile()
    
    @classmethod
    def wrapUp(cls):
        #wrap up possible open stuffs and exit normally
        print("Wrapping up...")
            

    @classmethod
    def parseArgsAndDecide(cls,argumentsList):
        if len(argumentsList)==0 or argumentsList[0] in ['-h','--help']:
            return cls.help()
        elif argumentsList[0] in ['-c','--create']:
            return cls.createTask(argumentsList[1:])
        elif argumentsList[0] in ['-s','--say','-p']:
            return cls.printSchedule(argumentsList[1:])
        elif argumentsList[0] in ['-d','--delete']:
            return cls.deleteTask(argumentsList[1:])
        elif argumentsList[0] in ['-o','--conf','--options']:
            return cls.configure(argumentsList[1:])
        else:
            cls.outputWriter.wrongInputMessage(argumentsList[0])
            return 1
    
    @classmethod
    def setConfOptions(cls):
        cls.options = cls.FileReader.fetchConfOptions()
    @classmethod
    def setWrapUpFunc(cls):
        cls.inputReader.suppliedWrapUpFunc = cls.wrapUp
    @classmethod
    def createOrVerifyDir(cls):
        if not os.path.exists(cls.tasksFolderLocation):
            os.makedirs(cls.tasksFolderLocation)
        if not os.path.exists(cls.recurringTasksFile):
            open(cls.recurringTasksFile, 'w').close()
        if not os.path.exists(cls.oneOffTasksFile):
            open(cls.oneOffTasksFile, 'w').close()
        if not os.path.exists(cls.confFile):
            open(cls.confFile, 'w').close()
            cls.configure([])

    @classmethod
    def do(cls,argumentsList):
        cls.createOrVerifyDir()
        cls.setConfOptions()
        cls.setWrapUpFunc()
        return cls.parseArgsAndDecide(argumentsList)


def main(argvector):
    argumentsList = argvector[1:]
    argumentCount = len(argumentsList)
    exitCode = Taskmaster.do(argumentsList)
    sys.exit(exitCode)


if __name__ == "__main__":
    main(sys.argv)