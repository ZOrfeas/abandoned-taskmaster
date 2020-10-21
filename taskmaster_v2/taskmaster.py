#!/usr/bin/python3
import sys,os
from pathlib import Path
# from .FileReader import FileReader 
# from .FIleWriter import FIleWriter
# from .InputReader import InputReader
# from .OutputWriter import OutputWriter
# from .Task import Task
import FileReader
import FIleWriter
import OutputWriter
import InputReader
import Task


tasksFolderLocation = os.path.join(str(Path.home()),".tasksFolder")
recurringTasksFile = os.path.join(tasksFolderLocation,"recurringTasks")
oneOffTasksFile = os.path.join(tasksFolderLocation,"oneOffTasks")
confFile = os.path.join(tasksFolderLocation,"conf")

options = {}

def printHelp():
    OutputWriter.helpMessage()
    return 0
def createTask():
    print()
def printSchedule():
    print("Entered printSchedule")
def deleteTask():
    print("Entered deleteTask")
def configure():
    if os.stat(confFile).st_size == 0:
        FIleWriter.initConfFile(confFile)

def parseArgsAndDecide(allCmdArgs):
    if len(allCmdArgs)==0 or allCmdArgs[0] in ['-h', '--help']:
        return printHelp()
    elif allCmdArgs[0] in ['-c','--create']:
        return createTask(allCmdArgs[1:])
    elif allCmdArgs[0] in ['-s','--say','-p']:
        return printSchedule(allCmdArgs[1:])
    elif allCmdArgs[0] in ['-d','--delete']:
        return deleteTask(allCmdArgs[1:])
    elif allCmdArgs[0] in ['-o','--conf','--options']:
        return configure(allCmdArgs[1:])
    else:
        OutputWriter.wrongInputMessage(allCmdArgs[0])
        return 1

def getConfOptions(confFile):
    options = FileReader.fetchConfOptions(confFile)
    
def findOrMakeAFile(path):
    if not os.path.exists(path):
        open(path,'w').close()
        return 1
    return 0

def checkAndSetUpDir():
    if not os.path.exists(tasksFolderLocation):
        os.makedirs(tasksFolderLocation)
    findOrMakeAFile(recurringTasksFile)
    findOrMakeAFile(oneOffTasksFile)
    if findOrMakeAFile(confFile):
        configure()

def wrapUp():
    '''Wrap up func for when exiting a prompt prematurely'''
    print("Wrapping up...")

def do(allCmdArgs):
    checkAndSetUpDir()
    getConfOptions(confFile)
    InputReader.setWrapUpFunc(wrapUp)
    return parseArgsAndDecide(allCmdArgs)

def main(argvector):
    allCmdArgs = argvector[1:]
    exitCode = do(allCmdArgs)
    sys.exit(exitCode)

if __name__ == "__main__":
    main(sys.argv)