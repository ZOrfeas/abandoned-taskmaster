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
            try:
                datetime.datetime.strptime(timeStringToCheck, "%H:%M")
                return True
            except ValueError:
                return False
        @classmethod
        def verifyRecurrArgs(cls,argsToCheck):
            
    
        @classmethod
        def promptForTaskName(cls):
            nameNotFound = True
            while(nameNotFound):
                name = cls.eofSafeInput("Give the task a name:\n").strip()
                if name: nameNotFound = False
                else: print("Invalid name, try again or press Ctrl-D to exit")
            return name
        @classmethod
        def promptForIsRecurring(cls):
            repeat = True
            while(repeat):
                isRecurring = cls.eofSafeInput("Is it a recurring task?(Y/n):").strip()
                if isRecurring not in ['y','n','yes','no']:
                    print("Invalid answer, try again or press Ctrl-D to exit")
                else:
                    isRecurring = True if isRecurring in ['y','yes'] else False
                    repeat = False
            return isRecurring
        
        @classmethod
        def createRecurring(cls,suppliedArgs):
            properDays = ['mon','tue','wed','thu','fri','sat','sun']
            taskToRet = {
                "name":None,
                "daysTimes":None,
                "cronActionMins":None,
                "cronAction":None,
                "description":None
            }
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
        argsOk,wrongArg = cls.inputReader.verifyRecurrArgs(taskDetails) if isRecurring else cls.inputReader.verifyOneOffArgs(taskDetails)
        if not argsOk:
            cls.outputWriter.wrongInputMessage(wrongArg, '-c')
            return 1
        else:
            taskToAdd = cls.inputReader.createRecurring(taskDetails) if isRecurring else cls.inputReader.createOneOff(taskDetails)
        if isRecurring:
            cls.FileWriter.addRecurring(taskToAdd)
        else:
            cls.FileWriter.addOneOff(taskToAdd)
        
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