def initConfFile(confFile):
    with open(confFile,'w') as optionsFile:
        optionsFile.write('{}\n')