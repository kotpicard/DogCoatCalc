from Logic import *
from CustomEvents import *
import wx


class LogicLayer(wx.EvtHandler):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.Bind(EVT_LOAD_DOG_FROM_DATA, self.LoadDog)
        self.Bind(EVT_PASS_DOG_DATA, self.CreateDog)
        self.Bind(EVT_VIEWGEN_DATAPASS, self.FormatForViewGen)

    def FormatForViewGen(self, evt):
        data = evt.data
        name = data[0]
        genotype = data[1]
        res = []
        for locus in genotype:
            value1 = locus.alleles[0].value
            value2 = locus.alleles[1].value
            if type(locus.alleles[0]) == Allele:
                type1 = "allele"
            elif type(locus.alleles[0]) == NotAllele:
                type1 = "notallele"
            else:
                type1 = "anyallele"
            if type(locus.alleles[1]) == Allele:
                type2 = "allele"
            elif type(locus.alleles[1]) == NotAllele:
                type2 = "notallele"
            else:
                type2 = "anyallele"
            res.append([(value1, type1), (value2, type2)])
        wx.PostEvent(self.parent, PassFormattedGenotype(data=(name, res)))

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
        coat_phens = [PHEN_DICT[x] for x in coat if x != "I don't know"]
        dog = Dog(Genotype(), coat=coat_phens, name=name, age=age, sex=sex)
        for p in coat_phens:
            p.ImposeConditions(dog.genotype)
        if dog.genotype.status:
            evt = PassDogToDataLayerEvent(dog=dog)
            wx.PostEvent(self.parent, evt)
        else:
            wx.PostEvent(self.parent, DogIncorrectGenotypeEvent())
