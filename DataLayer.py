from CustomEvents import *
import wx


class DataLayer(wx.EvtHandler):
    def __init__(self, parent, path="data.txt"):
        super().__init__()
        self.dogs = []
        self.goals = []
        self.breedings = []
        self.currentDogID = 0
        self.currentBreedingID = 0
        self.parent = parent
        self.dataLocation = path
        self.Bind(EVT_SAVE, self.SaveData)
        self.Bind(EVT_LOAD, self.LoadData)
        self.Bind(EVT_PASS_DOG, self.AddDogFromTopLayer)
        self.Bind(EVT_DISPLAY_ALL_DOGS, self.PassDogsForDisplay)
        self.Bind(EVT_REQUEST_DOG_BY_ID, self.PassDogByID)
        self.Bind(EVT_REQUEST_GENOTYPE_BY_ID, self.PassGenotypeByID)
        self.Bind(EVT_REQUEST_DOGS, self.PassDogsByCondition)
        self.Bind(EVT_PARENT_SELECTED, self.PassDogByID)
        self.Bind(EVT_PASS_GOAL, self.ProcessPassGoal)
        self.Bind(EVT_REQUEST_ALL_GOALS, self.ProcessPassGoal)
        self.Bind(EVT_DELETE_GOAL, self.DeleteGoal)
        self.Bind(EVT_BEGIN_BREEDCALC, self.PassBreedingCalculationData)
        self.Bind(EVT_ADD_BREEDING_RES, self.AddBreedingResult)

    def AddBreedingResult(self, e):
        breedingresult = e.breeding
        self.breedings.append(breedingresult)
        wx.PostEvent(self.parent, ViewBreedingResult(breedingresult=breedingresult))


    def PassBreedingCalculationData(self, e):
        breedingtype, parents, goals = e.data
        print(breedingtype, parents, goals)
        parents = [self.dogs[x] for x in parents if x is not None]
        if breedingtype == "PickMate":
            parents.append([dog for dog in self.dogs if dog.sex != parents[0].sex])
        goals = [self.goals[x] for x in goals]
        wx.PostEvent(self.parent, DoBreedingCalculation(data=(breedingtype, parents, goals)))

    def DeleteGoal(self, evt):
        which = evt.data
        keep = []
        for i in range(len(self.goals)):
            if i not in which:
                keep.append(self.goals[i])
        self.goals = keep
        wx.PostEvent(self.parent, NavigationEvent(destination="Goals"))

    def ProcessPassGoal(self, evt):
        print(evt.type)
        if evt.type == "add":
            self.AddGoal(evt.data, evt.origin)
        if evt.type == "displayall":
            self.PassAllGoals("Goals")
        if evt.type == "displaybreeding":
            self.PassAllGoals("Breeding")

    def PassAllGoals(self, type):
        data = []
        for goal in self.goals:
            data.append([(x.desc, x.type) for x in goal.elements])
        if type == "Goals":
            wx.PostEvent(self.parent, NavDataPass(destination="Goals", data=data))
        elif type == "Breeding":
            wx.PostEvent(self.parent, PassGoalsForDisplay(destination="breeding", data=data))

    def AddGoal(self, goal, origin):
        self.goals.append(goal)
        print(self.goals)
        wx.PostEvent(self, SaveEvent())
        if origin == "goals":
            wx.PostEvent(self.parent, NavigationEvent(destination="Goals"))
        elif origin == "breeding":
            wx.PostEvent(self.parent, NavigationEvent(destination="BreedingCalc"))
            wx.PostEvent(self, RequestAllGoalsEvent(type="displaybreeding"))

    def PassDogsByCondition(self, evt):
        result = [dog for dog in self.dogs if evt.filter(dog)]
        if evt.destination == "selectdog" or evt.destination == "addrelative":
            result = [self.FormatForSelection(dog) for dog in result]
        e = PassDogs(dogs=result, destination=evt.destination, data=evt.data)
        wx.PostEvent(self.parent, e)

    def FormatForSelection(self, dog):
        return [[dog.name, "Female" if dog.sex == "f" else "Male", str(dog.age), dog.coatdesc], dog.id]

    def PassGenotypeByID(self, evt):
        # evt.type, evt.dogid
        if evt.type == "viewgenotype":
            # if passing for view genotype window, pass the data to logic layer for formatting
            data = (evt.dogid, self.dogs[evt.dogid].name, self.dogs[evt.dogid].genotype)
            newevt = PassDataForViewGenotype(data=data)
            wx.PostEvent(self.parent, newevt)
        if evt.type == "passgenotype":
            genotype = self.dogs[evt.dogid].genotype
            newevt = PassGenotypeDataEvent(genotype=genotype, type=evt.subtype, data=evt.data)
            print("passing")
            wx.PostEvent(self.parent, newevt)

    def AddDogFromTopLayer(self, evt):
        # if evt.dog.id is not None:
        #     self.dogs.append(evt.dog)
        # else:
        self.currentDogID = len(self.dogs)
        evt.dog.id = self.currentDogID
        self.currentDogID += 1
        self.dogs.append(evt.dog)
        wx.PostEvent(self, SaveEvent())

    def PassDogByID(self, evt):
        if int(evt.dogid) in range(len(self.dogs)):
            wx.PostEvent(self.parent, PassDogDataEvent(dog=self.dogs[int(evt.dogid)], type=evt.type))

    def PassDogsForDisplay(self, evt):
        dog_descs = []
        for dog in self.dogs:
            dog_descs.append(dog.ToDesc())
        e = DisplayAllDogsEvent(descs=dog_descs)
        wx.PostEvent(self.parent, e)

    def SaveData(self, evt):
        datafile = open(self.dataLocation, "w")
        datafile.write("CURRENT_DOG_ID:" + str(self.currentDogID))
        datafile.write("\n")
        datafile.write("CURRENT_BREEDING_ID:" + str(self.currentBreedingID))
        datafile.write("\n")
        datafile.write("##DOGS")
        datafile.write("\n")
        for dog in self.dogs:
            datafile.write("#")
            dogdata = dog.ToList()
            for elem in dogdata:
                # print(elem)
                datafile.write(elem[0].upper() + ":" + str(elem[1]) + "\n")

        datafile.write("##BREEDINGS")
        datafile.write("\n")
        for breeding in self.breedings:
            datafile.write("#")
            breedingdata = breeding.ToList()
            for elem in breedingdata:
                datafile.write(elem[0].upper() + ":" + elem[1] + "\n")

        datafile.write("##GOALS")
        datafile.write("\n")
        for goal in self.goals:
            datafile.write("#")
            goaldata = goal.ToText()
            datafile.write(goaldata)
            datafile.write("\n")
        datafile.write("\n")
        datafile.close()

    def LoadData(self, evt):
        datafile = open(self.dataLocation)
        data = datafile.readlines()
        datafile.close()
        if data:
            self.currentDogID = int(data[0].split(":")[1])
            self.currentBreedingID = int(data[0].split(":")[1])
            breedingsstart = data.index("##BREEDINGS\n")
            goalsstart = data.index("##GOALS\n")
            data_dogs = data[3:breedingsstart]
            data_breedings = data[breedingsstart + 1:goalsstart]
            data_goals = data[goalsstart + 1:]
            print(data_dogs, data_goals, data_breedings)
            for i in range(0, len(data_dogs), 10):
                dogslice = data_dogs[i:i + 10]
                evt = LoadDogFromDataEvent(data=dogslice)
                wx.PostEvent(self.parent, evt)
