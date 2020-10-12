#!/usr/bin/python3
import sys,os,json
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
            more1    =    '                             accordingly, use "taskmaster.py -c help" for more info     \n'
            command2 =    '  -s, --say, -p              say/print a day\'s, week\'s schedule or all recurring tasks\n'
            more2    =    '                             currently registered\n'
            command3 =    '  -d, --delete               delete a task by name\n'
            command4 =    '  -o, --options, --conf      prompts to change the given option, or all if not specified'
            splittingLine='----------------------------------------------------------------------------------------'
            examples=     'Examples:'
            print('')
            print(cls.color["bold"]+title+cls.color["end"])
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print(explanation)
            print('')
            print(usage)
            print(tip)
            print(command0+command1+command1+more1+command2+more2+command3+command4)
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print(examples)
            print(cls.color["bold"]+splittingLine+cls.color["end"])
            print('Me: Orfeas Zografos')
            print('orfeas.zografos@gmail.com for if you find I f\'ed something up too much')
            print('or to tell me how cool this is(\'nt)')

        @classmethod
        def wrongInputMessage(cls,invalidInput):

    class inputReader:
        
        dummy = "dummy"

    @classmethod
    def help(cls,invalidInput=''):
        if not invalidInput:
            cls.outputWriter.helpMessage()
        else:
            cls.outputWriter.wrongInputMessage(invalidInput)
    @classmethod
    def createTask(cls,creatorArguments):
        print("Entered createTask")
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
    def parseArgsAndDecide(cls,argumentsList):
        if len(argumentsList)==0 or argumentsList[0] in ['-h','--help']:
            cls.help()
            return 0
        elif argumentsList[0] in ['-c','--create']:
            return cls.createTask(argumentsList[1:])
        elif argumentsList[0] in ['-s','--say','-p']:
            return cls.printSchedule(argumentsList[1:])
        elif argumentsList[0] in ['-d','--delete']:
            return cls.deleteTask(argumentsList[1:])
        elif argumentsList[0] in ['-o','--conf','--options']:
            return cls.configure(argumentsList[1:])
        else:
            cls.help(argumentsList[0])
            return 1
    
    @classmethod
    def setConfOptions(cls):
        cls.options = cls.FileReader.fetchConfOptions()
    
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
        return cls.parseArgsAndDecide(argumentsList)


def main(argvector):
    argumentsList = argvector[1:]
    argumentCount = len(argumentsList)
    exitCode = Taskmaster.do(argumentsList)
    sys.exit(exitCode)


if __name__ == "__main__":
    main(sys.argv)