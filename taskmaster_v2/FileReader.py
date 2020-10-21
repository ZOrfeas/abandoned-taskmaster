import json
def fetchConfOptions(confFile):
    with open(confFile) as optionsFile:
        fetchedOptions = json.loads(optionsFile.read().strip())
        return fetchedOptions