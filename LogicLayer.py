from Logic import *
from CustomEvents import *
import wx


class LogicLayer(wx.EvtHandler):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.Bind(EVT_LOAD_DOG_FROM_DATA, self.LoadDog)
        self.Bind(EVT_PASS_DOG_DATA, self.CreateDog)

    def LoadDog(self, evt):
        data = [x[1].strip() for x in evt.data]
        genotype = Genotype()
        genotype.CreateFromString(data[5])
        dogid = int(data[0])
        name = data[1]
        age = int(data[2])
        sex = data[3]
        coat = data[4].split("|")
        mother = int(data[6])
        father = int(data[7])
        children = data[8].split("|")
        relatives = data[9].split("|")
        dog = Dog(genotype, coat, dogid, name, age, mother, father, sex)
        dog.children = children
        dog.relatives = relatives
        evt = PassDogToDataLayerEvent(dog=dog)
        wx.PostEvent(self.parent, evt)

    def CreateDog(self, e):
        name = e.name
        age = e.age
        sex = "f" if e.sex == "Female" else "m"
        coat = e.coat
        coat_phens = [PHEN_DICT[x] for x in coat]
        dog = Dog(Genotype(), coat=coat_phens, name=name, age=age, sex=sex)
        for p in coat_phens:
            p.ImposeConditions(dog.genotype)
        evt = PassDogToDataLayerEvent(dog=dog)
        wx.PostEvent(self.parent, evt)
