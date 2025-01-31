from CustomEvents import *
import wx
from text_en import *


class DataLayer(wx.EvtHandler):
    def __init__(self, parent, path="data.txt"):
        super().__init__()
        self.dogs = []
        self.goals = []
        self.breedings = []
        self.currentDogID = 0
        self.currentBreedingID = 0
        self.parent = parent
        self.tempbreedingdata = None
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
        self.Bind(EVT_REQUEST_ALL_BREEDINGS, self.PassAllBreedings)
        self.Bind(EVT_OPEN_BREEDING_RESULT, self.PassBreedingByNumber)
        self.Bind(EVT_LOAD_ALL_BREEDINGS, self.LoadAllRelatives)

    def FindGoalByDescs(self, goal):
        for i, g in enumerate(self.goals):
            new_descs = [x for x in goal.split("*")]
            original_descs = [x.desc for x in g.elements]
            if all([x in original_descs for x in new_descs]) and all([x in new_descs for x in original_descs]):
                return i

    def LoadBreedings(self, e):
        for elem in self.tempbreedingdata:
            goalids = None
            # data = elem.split["|"]
            breedingtype = elem[0]
            if breedingtype == "Conventional":
                parent1 = elem[1]
                parent2 = elem[2]
                goals = elem[3]
            else:
                mainparent = elem[1]
                goals = elem[2]
            if goals:
                if not self.goals:
                    for goalelem in goals.split("&"):
                        descs = goalelem[1:].split("*")
                        wx.PostEvent(self.parent, AddGoalEvent(data=descs, origin="load"))

                goalids = [self.FindGoalByDescs(goal) for goal in goals.split("&")]
            if elem[0] == "Conventional":
                wx.PostEvent(self,
                             BeginBreedingCalculation(data=(breedingtype, (parent1, parent2), goalids), origin="load"))
            else:
                wx.PostEvent(self,
                             BeginBreedingCalculation(data=(breedingtype, (mainparent, None), goalids), origin="load"))

    def LoadAllRelatives(self, e):
        for dog in self.dogs:
            if type(dog.dam) == int:
                dog.dam = self.dogs[dog.dam]
            if type(dog.sire) == int:
                dog.sire = self.dogs[dog.sire]
            dog.children = [self.dogs[int(x)] for x in dog.children]
            dog.relatives = [self.dogs[int(x)] for x in dog.relatives]
        for dog in self.dogs:
            if dog.HasMother():
                dog.SetParent(dog.dam)
            if dog.HasFather():
                dog.SetParent(dog.sire)
        LoadAllBreedings()

    def PassBreedingByNumber(self, e):
        wx.PostEvent(self.parent, ViewBreedingResult(breedingresult=self.breedings[e.num]))

    def PassAllBreedings(self, e):
        wx.PostEvent(self.parent, NavDataPass(destination="AllBreedingResults", data=self.breedings))

    def AddBreedingResult(self, e):
        breedingresult = e.breeding
        self.breedings.append(breedingresult)
        if e.origin != "load":
            wx.PostEvent(self.parent, ViewBreedingResult(breedingresult=breedingresult))
        wx.PostEvent(self, SaveEvent())

    def PassBreedingCalculationData(self, e):
        breedingtype, parents, goals = e.data
        parents = [self.dogs[x] for x in parents if x is not None]
        if breedingtype == "PickMate":
            parents.append([dog for dog in self.dogs if dog.sex != parents[0].sex])
        if goals:
            goals = [self.goals[x] for x in goals]
        wx.PostEvent(self.parent, DoBreedingCalculation(data=(breedingtype, parents, goals), origin=e.origin))

    def DeleteGoal(self, evt):
        which = evt.data
        keep = []
        for i in range(len(self.goals)):
            if i not in which:
                keep.append(self.goals[i])
        self.goals = keep
        wx.PostEvent(self.parent, NavigationEvent(destination="Goals"))

    def ProcessPassGoal(self, evt):
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
        if all([x != goal for x in self.goals]):
            self.goals.append(goal)
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
        if evt.destination == "top":
            if not evt.order:
                result = result[::-1]
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
            newevt = PassGenotypeDataEvent(genotype=genotype, type=evt.subtype, data=evt.data, dog=self.dogs[evt.dogid])
            wx.PostEvent(self.parent, newevt)

    def AddDogFromTopLayer(self, evt):
        self.currentDogID = len(self.dogs)
        evt.dog.id = self.currentDogID
        self.currentDogID += 1
        self.dogs.append(evt.dog)
        if len(self.dogs) == evt.maxid:
            wx.PostEvent(self, LoadAllBreedings())

    def PassDogByID(self, evt):
        if int(evt.dogid) in range(len(self.dogs)):
            dogid = int(evt.dogid)
            if evt.type == "byid":
                filtered_breedings = [(i, self.breedings[i]) for i in range(len(self.breedings)) if
                                      self.breedings[i].parent1.id == dogid or self.breedings[
                                          i].parent2.id == dogid]

                mother = False if self.dogs[dogid].dam is None or "Mother of" in self.dogs[dogid].dam.name else (
                TEXT_MOTHER + ": " + self.dogs[dogid].dam.name, self.dogs[dogid].dam.id)
                father = False if self.dogs[dogid].sire is None or "Father of" in self.dogs[dogid].sire.name else (
                TEXT_FATHER + ": " + self.dogs[dogid].sire.name, self.dogs[dogid].sire.id)
                children = [(TEXT_CHILD + ": " + x.name, x.id) for x in self.dogs[dogid].children]
                relatives = [mother, father] + children + [(TEXT_OTHER_RELATIVES + ": " + x.name, x.id) for x in
                                                           self.dogs[dogid].relatives]

                wx.PostEvent(self.parent,
                             PassDogDataEvent(dog=self.dogs[int(evt.dogid)], type=evt.type, data=filtered_breedings,
                                              relativedata=relatives))
            else:
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
                datafile.write(elem[0].upper() + ":" + str(elem[1]) + "\n")

        datafile.write("##BREEDINGS")
        datafile.write("\n")
        for breeding in self.breedings:
            datafile.write("#")
            breedingdata = breeding.ToText()
            datafile.write(breedingdata + "\n")

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
            alldogs = []
            for i in range(0, len(data_dogs), 10):
                dogslice = data_dogs[i:i + 10]
                alldogs.append(dogslice)
            wx.PostEvent(self.parent, LoadAllDogs(data=alldogs))
            data_goals = [x.strip("\n") for x in data_goals if "#" in x]
            data_breedings = [x.strip("\n")[1:] for x in data_breedings if "#" in x]

            for elem in data_goals:
                descs = elem[1:].split("*")
                wx.PostEvent(self.parent, AddGoalEvent(data=descs, origin="load"))
            tempbreedingdata = []
            for elem in data_breedings:
                breedingtype = elem.split("|")[0]
                if breedingtype == "Conventional":
                    parent1index = int(elem.split("|")[1])
                    parent2index = int(elem.split("|")[2])
                    goals = elem.split("|")[3]
                    data = (breedingtype, parent1index, parent2index, goals)
                else:
                    mainparentindex = int(elem.split("|")[1])
                    goals = elem.split("|")[2]
                    data = (breedingtype, mainparentindex, goals)
                tempbreedingdata.append(data)
            self.tempbreedingdata = tempbreedingdata
