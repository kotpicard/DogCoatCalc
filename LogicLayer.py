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
        self.Bind(EVT_EDIT_LOCUS, self.StartLocusEdit)
        self.Bind(EVT_PASS_GENOTYPE, self.ProcessGenotype)
        self.Bind(EVT_OPEN_EDIT_LOCUS, self.GetOptionsForEditLocus)

    def StartLocusEdit(self, evt):
        dogid = evt.dogid
        values = evt.values
        replacementtype = evt.replacementtype
        number = evt.number
        print(dogid, values, replacementtype, number)
        wx.PostEvent(self.parent, RequestGenotypeByID(dogid=dogid, type="passgenotype", subtype="editlocus",
                                                      data=(values, number, replacementtype, dogid)))

    def ProcessGenotype(self, evt):
        if evt.type == "editlocus":
            self.ProcessLocusEdit(genotype=evt.genotype, data=evt.data)

    def ProcessLocusEdit(self, genotype, data):
        # data is values, number, replacementtype, dogid
        values = data[0]
        number = data[1]
        replacementtype = data[2]
        print(replacementtype)
        dogid = data[3]
        if replacementtype == "anyallele":
            print("any")
            replacementallele = AnyAllele()
        elif replacementtype == "notallele":
            print("not")
            replacementallele = NotAllele(values)
        else:
            print("allele")
            replacementallele = Allele(values[0])
            print(type(replacementallele))
        replacementlocus = Locus(number, allele1=replacementallele, allele2=AnyAllele())
        print("REPLACEMENT", replacementlocus)
        canreplace = genotype[number].CanReplace(replacementlocus)
        print(canreplace, "CANREPLACE")
        if canreplace:
            genotype[number].replace(replacementlocus)
            wx.PostEvent(self.parent, DogGenotypeChangedEvent(dogid=dogid))
        else:
            wx.PostEvent(self.parent, DogIncorrectGenotypeEvent(dogid=dogid))

    def GetOptionsForEditLocus(self, evt):
        locusnumber = evt.number
        options = ALLELES[locusnumber]
        newevt = PassEditLocusDataEvent(number=locusnumber, dogid=evt.dogid, options=options)
        wx.PostEvent(self.parent, newevt)

    def FormatForViewGen(self, evt):
        data = evt.data
        dogid = data[0]
        name = data[1]
        genotype = data[2]
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
        wx.PostEvent(self.parent, PassFormattedGenotype(data=(dogid, name, res)))

    def LoadDog(self, evt):
        data = [x.split(":")[1].strip() for x in evt.data]
        print(data)
        genotype = Genotype()
        genotype.CreateFromString(data[5])
        dogid = int(data[0])
        name = data[1]
        age = int(data[2])
        sex = data[3]
        coat = data[4].split("|")
        coat = [PHEN_DICT[x] for x in coat if x != "I don't know"]
        mother = None if data[6] == "None" else int(data[6])
        father = None if data[7] == "None" else int(data[7])
        children = data[8].split("|")
        relatives = data[9].split("|")
        dog = Dog(genotype, coat, dogid, name, age, mother, father, sex)
        dog.children = None if children == ["None"] else children
        dog.relatives = None if relatives == ["None"] else relatives
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
