#!/usr/bin/python3
import sys,os
from pathlib import Path
import FileReader
import FIleWriter
import OutputWriter
import InputReader
from Tasks import Task


tasksFolderLocation = os.path.join(str(Path.home()),".tasksFolder")
recurringTasksFile = os.path.join(tasksFolderLocation,"recurringTasks")
oneOffTasksFile = os.path.join(tasksFolderLocation,"oneOffTasks")
confFile = os.path.join(tasksFolderLocation,"conf")

options = {}

def printHelp():
    OutputWriter.helpMessage()
    return 0
def createTask(creatorArgs):
    recurrProperArgs = ['recur','r','recurring']
    oneOffProperArgs = ['once','o','oneoff']
    argAmount = len(creatorArgs)
    silentMode = False
    if argAmount >= 1 and creatorArgs[0] == 'help':
        OutputWriter.creatorHelp()
        return 0
    if argAmount >= 1 and creatorArgs[0] == 's':
        silentMode = True
        creatorArgs = creatorArgs[1:]
        argAmount = argAmount - 1
    if argAmount == 0:
        isRecurring = InputReader.promptForIsRecurring()
    else:
        isRecurringCandidate = creatorArgs[0]
        if isRecurringCandidate in recurrProperArgs:
            isRecurring = True
        elif isRecurringCandidate in oneOffProperArgs:
            isRecurring = False
        else:
            OutputWriter.wrongInputMessage(creatorArgs[0], '-c')
            return 1
    taskDets = creatorArgs[1:]
    argsOk,wrongArg = InputReader.verifyAndPrepRecurrArgs(taskDets) if isRecurring else InputReader.verifyAndPrepOneOffArgs(taskDets)
    if not argsOk:
        OutputWriter.wrongInputMessage(wrongArg, '-c')
        return 1
    else:
        taskToAdd = InputReader.createRecurring(taskDets) if isRecurring else InputReader.createOneOff(taskDets)
    if isRecurring:
        if argAmount <= 1 or (silentMode or InputReader.askToAddRecurr(taskToAdd)):
            FIleWriter.addRecurring(taskToAdd)
    else:
        if argAmount <= 1 or (silentMode or InputReader.askToAddOneOff(taskToAdd)):
            FIleWriter.addOneOff(taskToAdd)
    return 0
def printSchedule():
    print("Entered printSchedule")
def deleteTask():
    print("Entered deleteTask")
def configure():
    if os.stat(confFile).st_size == 0:
        FIleWriter.initConfFile()

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
    InputReader.setWrapUpFunc(wrapUp)
    FileReader.setFileLocations(recurringTasksFile,oneOffTasksFile,confFile)
    FIleWriter.setFileLocations(recurringTasksFile,oneOffTasksFile,confFile)
    options = FileReader.fetchConfOptions()
    return parseArgsAndDecide(allCmdArgs)

def main(argvector):
    allCmdArgs = argvector[1:]
    exitCode = do(allCmdArgs)
    sys.exit(exitCode)

if __name__ == "__main__":
    main(sys.argv)