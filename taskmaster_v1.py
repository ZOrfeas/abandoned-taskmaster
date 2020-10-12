#!/usr/bin/python3
import sys,os
from pathlib import Path



class Taskmaster:
    
    tasksFolderLocation = str(Path.home())+"/.tasksFolder"
    recurringTasksFile = tasksFolderLocation+"/recurringTasks"
    oneOffTasksFile = tasksFolderLocation+"/oneOffTasks"
    confFile = tasksFolderLocation+"/conf"

    class FileWriter:
        dummy = "dummy"
    class FileReader:
        dummy = "dummy"
    class Printer:
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
    def help(cls,inputOK=True):
        print("Entered help")
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
        print("Entered configure")
    
    @classmethod
    def parseArgsAndDecide(cls,argumentsList):
        if len(argumentsList)==0 or argumentsList[0] in ['-h','--help']:
            Taskmaster.help()
            return 0
        elif argumentsList[0] in ['-c','--create']:
            return Taskmaster.createTask(argumentsList[1:])
        elif argumentsList[0] in ['-s','--say','-p']:
            return Taskmaster.printSchedule(argumentsList[1:])
        elif argumentsList[0] in ['-d','--delete']:
            return Taskmaster.deleteTask(argumentsList[1:])
        elif argumentsList[0] in ['-o','--configure','--options']:
            return Taskmaster.configure(argumentsList[1:])
        else:
            Taskmaster.help(False)
            return 1
    
    @classmethod
    def createOrVerifyDir(cls):
        if not os.path.exists(Taskmaster.tasksFolderLocation):
            os.makedirs(Taskmaster.tasksFolderLocation)
        if not os.path.exists(Taskmaster.recurringTasksFile):
            open(Taskmaster.recurringTasksFile, 'w').close()
        if not os.path.exists(Taskmaster.oneOffTasksFile):
            open(Taskmaster.oneOffTasksFile, 'w').close()
        if not os.path.exists(Taskmaster.confFile):
            open(Taskmaster.confFile, 'w').close()
            Taskmaster.configure([])

    @staticmethod
    def do(argumentsList):
        Taskmaster.createOrVerifyDir()
        return Taskmaster.parseArgsAndDecide(argumentsList)


def main(argvector):
    argumentsList = argvector[1:]
    argumentCount = len(argumentsList)
    exitCode = Taskmaster.do(argumentsList)
    sys.exit(exitCode)


if __name__ == "__main__":
    main(sys.argv)