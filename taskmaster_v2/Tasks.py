from InputReader import promptForNonEmptyTime
class Task:
    
    def __init__(self,isRecurring,dictIn):
        self.isRecurring = isRecurring
        self.name = dictIn["name"]
        if isRecurring:
            self.daysTimes = dictIn["daysTimes"]
        else:
            self.date = dictIn["date"]
            self.time = dictIn["time"]
            self.isDeadlined = dictIn["isDeadlined"]
        self.cronMins = dictIn["cronActionMins"]
        self.cronAction = dictIn["cronAction"]
        self.description = dictIn["description"]

    def makeDict(self):
        toRetDict = {}
        toRetDict["name"] = self.name
        if self.isRecurring:
            toRetDict["daysTimes"] = self.daysTimes
        else:
            toRetDict["date"] = self.date
            toRetDict["time"] = self.time
            toRetDict["isDeadlined"] = self.isDeadlined
        toRetDict["cronActionMins"] = self.cronMins
        toRetDict["cronAction"] = self.cronAction
        toRetDict["description"] = self.description
        return toRetDict

    def wantsCron(self):
        if self.cronMins is not None:
            return True
        else:
            return False

    def cronWellDefined(self):
        if self.isRecurring:
            for i in self.daysTimes:
                if len(i) ==  1:
                    return False
        else:
            if self.time is None:
                return False
        return True
    
    def resolveCronInconsistencies(self):
        if self.isRecurring:
            for i in self.daysTimes:
                if len(i) == 1:
                    print("On {} at:".format(i[0]))
                    i.append(promptForNonEmptyTime())
        else:
            self.time = promptForNonEmptyTime()
