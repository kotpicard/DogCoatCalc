# LOCI
# 0 - Agouti Ay, aw, at, a
# 1 - Liver B, b
# 2 - Dilution D, d
# 3 - Red distribution Em, E, Eg, Ea, Eh, e
# 4 - Greying G, g
# 5 - Red Dilution I, i
# 6 - Black K, kbr, k
# 7 - Merle M, m
# 8 - Spotting S, sp, si
# 9 - Ticking T, Tr, t
LOCUS0 = ["Ay", "aw", "at"]
LOCUS1 = ["B", "b"]
LOCUS2 = ["D", "d"]
LOCUS3 = ["Em", "E", "e"]
LOCUS4 = ["G", "g"]
LOCUS5 = ["I", "i"]
LOCUS6 = ["K", "kbr", "k"]
LOCUS7 = ["M", "m"]
LOCUS8 = ["S", "sp", "si"]
LOCUS9 = ["T", "Tr", "t"]
ALLELES = [LOCUS0, LOCUS1, LOCUS2, LOCUS3, LOCUS4, LOCUS5, LOCUS6, LOCUS7, LOCUS8, LOCUS9]


class Allele:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return other == self.value

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def ReturnCondition(self, number):
        return ReverseCondition(Condition(number, "HasAtLeastOne", self.value))


class AnyAllele(Allele):
    def __init__(self, value="Any Allele"):
        super().__init__(value)

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return True

    def ReturnCondition(self, number):
        return ReverseCondition(Condition(number, "ZeroCondition", None))


class NotAllele(Allele):
    def __init__(self, notValue, value="None"):
        super().__init__(value)
        if type(notValue) == str:
            self.notValue = [notValue]
        else:
            self.notValue = notValue
        self.value = "Any allele except {}".format(str(self.notValue)[1:-1])

    def __eq__(self, other):
        return all([x != other for x in self.notValue])

    def __add__(self, other):
        if type(other) == NotAllele:
            self.notValue += other.notValue
            self.notValue = list(set(self.notValue))
        return self

    def ReturnCondition(self, number):
        if len(self.notValue) == 1:
            return ReverseCondition(Condition(number, "IsNotHomozygousFor", self.notValue[0]))
        else:
            current = MultipleCondition(ReverseCondition(Condition(number, "IsNotHomozygousFor", self.notValue[0])),
                                        ReverseCondition(Condition(number, "ZeroCondition", None)))
            for value in self.notValue[1:]:
                current = MultipleCondition(ReverseCondition(Condition(number, "IsNotHomozygousFor", value)), current)
            return current


class Locus:
    def __init__(self, number, allele1=AnyAllele(), allele2=AnyAllele()):
        self.child_possible_alleles = Possibility()
        self.number = number
        self.alleles = [allele1, allele2]
        self.dam_conditions = []
        self.sire_conditions = []
        self.general_conditions = []

    def __repr__(self):
        if type(self.alleles[0]) == AnyAllele or type(self.alleles[1]) == Allele:
            self.alleles = self.alleles[::-1]
        return "/".join([str(x) for x in self.alleles])

    def CreateFromString(self, string):
        allele1, allele2 = string.split("/")
        if "except" in allele1:
            self.alleles.append(NotAllele(allele1.split(" ")[-1].split(",")))
        elif "Any" in allele1:
            self.alleles.append(AnyAllele())
        else:
            self.alleles.append(Allele(allele1))

        if "except" in allele2:
            self.alleles.append(NotAllele(allele2.split(" ")[-1].split(",")))
        elif "Any" in allele2:
            self.alleles.append(AnyAllele())
        else:
            self.alleles.append(Allele(allele2))

    def __eq__(self, other):
        if type(other) == Locus:
            return (self.alleles[0].value == other.alleles[0].value and self.alleles[1].value == other.alleles[
                1].value) or (self.alleles[0].value == other.alleles[1].value and self.alleles[1].value ==
                              other.alleles[0].value)
        else:
            return (self.alleles[0].value == other[0].value and self.alleles[1].value == other[1].value) or (
                    self.alleles[0].value == other[1].value and self.alleles[1].value == other[0].value)

    def CanBeReplacedBy(self, original, replacement):
        # replacement is ALLELE
        print("TESTING REPLACEMENT", end=" ")
        print(original, replacement)
        if type(replacement) == AnyAllele:
            return True
        elif type(original) == Allele:
            if type(replacement) == Allele and original == replacement:
                return True
            else:
                return False
        elif type(replacement) == Allele and type(original) == NotAllele and replacement.value in original.notValue:
            return False
        else:
            print("CAN REPLACE")
            return True

    def CanReplace(self, replacement):
        # replacement is locus
        print("replacing", self.alleles, replacement)
        if self.CanBeReplacedBy(self.alleles[0], replacement[0]) and self.CanBeReplacedBy(self.alleles[1],
                                                                                          replacement[1]):
            print("order1")
            return 1

        elif self.CanBeReplacedBy(self.alleles[0], replacement[1]) and self.CanBeReplacedBy(self.alleles[1],
                                                                                            replacement[0]):
            print("order2")
            return -1
        elif all([type(x) == AnyAllele for x in replacement]):
            return True
        else:
            return False

    def replace(self, replacement):
        # replacement is locus
        # print("EQUALITY TEST", self == replacement)
        order = self.CanReplace(replacement)
        if type(order) == int:
            self.alleles = self.alleles[::order]
            # print(self.alleles)
            temp = []
            for i in range(2):
                if type(replacement[i]) != AnyAllele and self != replacement:
                    if type(self.alleles[i]) == type(replacement[i]) == NotAllele:
                        temp.append(self.alleles[i] + replacement[i])
                    else:
                        # print(replacement[i])
                        temp.append(replacement[i])
                else:
                    temp.append(self.alleles[i])
            self.alleles = temp
            print("AFTER REPLACEMENT", self.alleles)
            return True
        elif not order:
            return False

    def CreateParentConditions(self):
        condition1 = self.alleles[0].ReturnCondition(self.number)
        condition2 = self.alleles[1].ReturnCondition(self.number)
        print(condition1, condition2)
        if condition1.name != "ZeroCondition" or condition2.name != "ZeroCondition":
            if condition1.name == condition2.name:
                if condition1.argument == condition2.argument:
                    self.dam_conditions.append(condition1)
                    self.sire_conditions.append(condition2)
            else:
                self.general_conditions.append(MultipleCondition(condition1, condition2))

    def CreateChildConditions(self):
        if type(self.alleles[0]) == type(self.alleles[1]) == Allele:
            return Condition(self.number, "HasAtLeastOne", self.alleles[0].value)
        if type(self.alleles[0]) == type(self.alleles[1]) == NotAllele:
            common_alleles = []
            for allele in self.alleles[0].notValue:
                if allele in self.alleles[1].notValue:
                    common_alleles.append(allele)
            if len(common_alleles) == 1:
                return Condition(self.number, "IsNotHomozygousFor", common_alleles[0])
            elif len(common_alleles):
                current = MultipleCondition(Condition(self.number, "IsNotHomozygousFor", common_alleles[0]),
                                            Condition(self.number, "ZeroCondition", None))
                for allele in common_alleles[1:]:
                    current = MultipleCondition(Condition(self.number, "IsNotHomozygousFor", allele), current)
                return current

    def CreateChildPossibilities(self):
        self.child_possible_alleles = Possibility()
        if self.alleles[0].value == self.alleles[1].value:
            self.child_possible_alleles.AddPossibility(self.alleles[0], 1)
        else:
            self.child_possible_alleles.AddPossibility(self.alleles[0], 0.5)
            self.child_possible_alleles.AddPossibility(self.alleles[1], 0.5)
        return self.child_possible_alleles


class Condition:
    def __init__(self, locus, cond, argument):

        self.locus = locus
        self.name = cond
        if cond == "DoesntHaveAllele":
            self.cond = self.DoesntHaveAllele
        elif cond == "HasAtLeastOne":
            self.cond = self.HasAtLeastOne
        elif cond == "IsHomozygousFor":
            self.cond = self.IsHomozygousFor
        elif cond == "IsNotHomozygousFor":
            self.cond = self.IsNotHomozygousFor
        elif cond == "IsExactly":
            self.cond = self.IsExactly
        elif cond == "ZeroCondition":
            self.cond = self.ZeroCondition
        else:
            self.cond = self.Error
        self.argument = argument

    def __repr__(self):
        return " ".join([str(self.locus), self.name, str(self.argument)])

    def DoesntHaveAllele(self, target):
        return any([x != self.argument for x in target[self.locus].alleles])

    def HasAtLeastOne(self, target):
        return self.argument in target[self.locus].alleles

    def IsHomozygousFor(self, target):
        return all([x == self.argument for x in target[self.locus].alleles])

    def IsNotHomozygousFor(self, target):
        # print("TEST")
        # print(any([x != self.argument for x in target[self.locus].alleles]))
        return any([x != self.argument for x in target[self.locus].alleles])

    def IsExactly(self, target):
        return self.argument == target[self.locus].alleles or self.argument == target[self.locus].alleles[::-1]

    def ZeroCondition(self, target):
        return True

    def Error(self, target):
        return False

    def Execute(self, target):
        # print(self.name, self.argument, target[self.locus].alleles)
        # print(self.cond(target))
        if type(target) == Genotype:
            return self.cond(target), 1
        if type(target) == PossibleGenotype:
            targets = [x[0] for x in target.loci[self.locus]]
            probabilities = [x[1] for x in target.loci[self.locus]]
            target_genotypes = [Genotype() for _ in range(len(targets))]
            for i in range(len(targets)):
                target_genotypes[i].loci[self.locus] = targets[i]
            tests = [self.cond(partial_target) for partial_target in target_genotypes]
            prob = sum([probabilities[x] if tests[x] else 0 for x in range(len(tests))])
            return any(tests), prob


class ReverseCondition(Condition):
    def __init__(self, condition):
        locus = condition.locus
        cond = condition.name
        argument = condition.argument
        super().__init__(locus, cond, argument)

    def DoesntHaveAllele(self, target):
        return NotAllele(self.argument), NotAllele(self.argument)

    def HasAtLeastOne(self, target):
        return Allele(self.argument), AnyAllele()

    def IsHomozygousFor(self, target):
        return Allele(self.argument), Allele(self.argument)

    def IsNotHomozygousFor(self, target):
        return NotAllele(self.argument), AnyAllele()

    def IsExactly(self, target):
        return Allele(self.argument[0]), Allele(self.argument[1])

    def ZeroCondition(self, target):
        return AnyAllele(), AnyAllele()

    def Error(self, target):
        return "Error: wrong condition type"

    def Execute(self, target):
        print("EXECUTING", self)
        print(target[self.locus].CanReplace(self.cond(target)))
        print(target[self.locus], self.cond(target))
        return target[self.locus].replace(self.cond(target))


class MultipleCondition:
    def __init__(self, cond1, cond2, connectiontype="AND"):
        self.name = None
        self.argument = None
        self.type = connectiontype

        self.locus1 = cond1.locus
        self.locus2 = cond2.locus
        self.cond1 = cond1
        if type(cond1) == Condition:
            self.cond1 = ReverseCondition(cond1)
        self.cond2 = cond2
        if type(cond2) == Condition:
            self.cond2 = ReverseCondition(cond2)
        self.resolved = False
        self.resolvable = False
        self.name = self.CreateName()

    def CreateNameCond1(self):
        if type(self.cond1) != MultipleCondition:
            return self.cond1.name + " " + str(self.cond1.argument)
        else:
            return self.cond1.CreateName()

    def CreateNameCond2(self):
        if type(self.cond2) != MultipleCondition:
            return self.cond2.name + " " + str(self.cond2.argument)
        else:
            return self.cond2.CreateName()

    def CreateName(self):
        return "Multiple Condition: {} {} {}".format(self.CreateNameCond1(), self.type, self.CreateNameCond2())

    def __repr__(self):
        return self.name

    def TestCond1(self, target):
        if self.type == "AND":
            print("testing", self.cond1.name)
            target = target[self.locus1]
            if type(self.cond1) != MultipleCondition:
                print(target.CanReplace(self.cond1.cond(target)))
                return target.CanReplace(self.cond1.cond(target))
            elif type(self.cond1) == MultipleCondition:
                return self.cond1.CanResolve(target, target)

    def TestCond2(self, target):
        if self.type == "AND":
            target = target[self.locus2]
            print("testing", self.cond2.name)
            if type(self.cond2) != MultipleCondition:
                print(target.CanReplace(self.cond2.cond(target)))
                return target.CanReplace(self.cond2.cond(target))
            elif type(self.cond2) == MultipleCondition:
                return self.cond2.CanResolve(target, target)

    def ResolveCond1(self, target):
        if type(self.cond1) != MultipleCondition:
            self.cond1.Execute(target)
        elif type(self.cond1) == MultipleCondition:
            self.Execute(target, target)

    def ResolveCond2(self, target):
        if type(self.cond2) != MultipleCondition:
            self.cond2.Execute(target)
        elif type(self.cond2) == MultipleCondition:
            self.Execute(target, target)

    def CanResolve(self, target1, target2):
        if self.type == "AND":
            direction1 = self.TestCond1(target1) and self.TestCond2(target2)
            direction2 = self.TestCond1(target2) and self.TestCond2(target1)
            if direction1 and direction2:
                self.resolvable = 0
                return False
            elif direction1:
                self.resolvable = 1
                return True
            elif direction2:
                self.resolvable = 2
                return True
            else:
                self.resolvable = -1
                return False

    def Execute(self, target1, target2=None):
        # needs to resolve in ONE direction only unless performed on same target
        print("EXECUTING MULTIPLE", self.name)
        if not target2:
            target2 = target1
        self.CanResolve(target1, target2)
        print(self.resolvable)
        if self.resolvable == 0:
            if target1 != target2:
                self.resolvable = True
                return "Not enough information to resolve multiple condition"
            else:
                self.ResolveCond1(target1)
                self.ResolveCond2(target2)
                self.resolved = True
        elif self.resolvable == 1:
            self.ResolveCond1(target1)
            self.ResolveCond2(target2)
            self.resolved = True
        elif self.resolvable == 2:
            self.ResolveCond1(target2)
            self.ResolveCond2(target1)
            self.resolved = True
        else:
            return "Error: cannot resolve multiple condition on these targets"


class Genotype:
    def __init__(self, loci=None):
        if not loci:
            self.loci = [Locus(i) for i in range(10)]
        else:
            self.loci = loci

    def CreateFromString(self, string):
        loci_text = string.split("|")
        for i in range(10):
            self.loci[i].CreateFromString(loci_text[i])

    def __getitem__(self, item):
        return self.loci[item]

    def __len__(self):
        return len(self.loci)

    def __repr__(self):
        return " | ".join([str(x) for x in self.loci])

    def __str__(self):
        return " | ".join([str(x) for x in self.loci])


class PossibleGenotype(Genotype):
    def __init__(self, loci):
        super().__init__()
        self.loci = loci

    def __repr__(self):
        temp = []
        for locus in self.loci:
            temp.append("; ".join([str(100 * x[1]) + "%: " + str(x[0]) for x in locus]))
        return "\n".join(temp)

    def TestMultiplePhenotypes(self, phenotypes):
        results = []
        probabilities = []
        for phenotype in phenotypes:
            result, prob = phenotype.TestConditions(self)
            results.append(result)
            probabilities.append(prob)
        if all(results):
            probability = 1
            for p in probabilities:
                probability *= p
            return True, probability
        else:
            return False, 0


class Phenotype:
    def __init__(self):
        self.desc = "description of phenotype"
        self.conditions = []  # list of conditions for this phenotype to show
        self.reverseConditions = []

    def AddCondition(self, locus, cond, argument):
        self.conditions.append(Condition(locus, cond, argument))

    def CreateReverseConditions(self):
        self.reverseConditions = [ReverseCondition(x) for x in self.conditions]

    def TestConditions(self, genotype):
        tests = [x.Execute(genotype) for x in self.conditions]
        prob = 1
        for test in tests:
            prob *= test[1]
        return all([x[0] for x in tests]), prob

    def ImposeConditions(self, genotype):
        self.CreateReverseConditions()
        print("################################################################")
        for cond in self.reverseConditions:
            # print(cond.locus, cond.name)
            print("LOOK HERE LOOK HERE LOOK HERE")
            print(cond.Execute(genotype), end="THIS LINE!!!!!!!!!!!!!!!!!!!")


class Possibility:
    def __init__(self):
        self.possibleAlleles = []
        self.probabilities = []

    def AddPossibility(self, allele, prob):
        self.possibleAlleles.append(allele)
        self.probabilities.append(prob)

    def Combine(self, otherPossibility, locus_number):
        results = []
        for i in range(len(self.possibleAlleles)):
            for j in range(len(otherPossibility.possibleAlleles)):
                result_locus = Locus(locus_number, self.possibleAlleles[i], otherPossibility.possibleAlleles[j])
                if result_locus not in [x[0] for x in results]:
                    results.append([result_locus, self.probabilities[i] * otherPossibility.probabilities[j]])
                else:
                    ind = [x[0] for x in results].index(result_locus)
                    results[ind][1] += self.probabilities[i] * otherPossibility.probabilities[j]
        return results

    def __repr__(self):
        return "; ".join(["{}: {}%".format(self.possibleAlleles[i], self.probabilities[i] * 100) for i in
                          range(len(self.possibleAlleles))])

    def __str__(self):
        return "; ".join(["{}: {}%".format(self.possibleAlleles[i], self.probabilities[i] * 100) for i in
                          range(len(self.possibleAlleles))])

    def __getitem__(self, item):
        return self.possibleAlleles[item], self.probabilities[item]


##### PHENOTYPES

## COLOR - EUMELANIN
BLACK = Phenotype()
LIVER = Phenotype()
BLUE = Phenotype()
ISABELLA = Phenotype()

## COLOR - PHEOMELANIN
RED = Phenotype()
DILUTE_RED = Phenotype()

## WHITE
WHITE = Phenotype()

# COLORS - NAMES
BLACK.desc = "Black"
LIVER.desc = "Liver"
BLUE.desc = "Blue"
ISABELLA.desc = "Isabella"
RED.desc = "Red"
DILUTE_RED.desc = "Fawn/cream/silver/white"
WHITE.desc = "White"

# COLORS - CONDITIONS
# BLACK
BLACK.AddCondition(3, "IsNotHomozygousFor", "e")
BLACK.AddCondition(1, "HasAtLeastOne", "B")
BLACK.AddCondition(2, "HasAtLeastOne", "D")
# LIVER
LIVER.AddCondition(3, "IsNotHomozygousFor", "e")
LIVER.AddCondition(1, "IsHomozygousFor", "b")
LIVER.AddCondition(2, "HasAtLeastOne", "D")
# BLUE
BLUE.AddCondition(3, "IsNotHomozygousFor", "e")
BLUE.AddCondition(1, "HasAtLeastOne", "B")
BLUE.AddCondition(2, "IsHomozygousFor", "d")
# ISABELLA
ISABELLA.AddCondition(3, "IsNotHomozygousFor", "e")
ISABELLA.AddCondition(1, "IsHomozygousFor", "b")
ISABELLA.AddCondition(2, "IsHomozygousFor", "d")
# RED
RED.AddCondition(6, "DoesntHaveAllele", "K")
RED.AddCondition(5, "IsNotHomozygousFor", "i")
# DILUTE RED
DILUTE_RED.AddCondition(6, "DoesntHaveAllele", "K")
DILUTE_RED.AddCondition(5, "IsHomozygousFor", "i")
# WHITE
WHITE.AddCondition(6, "DoesntHaveAllele", "K")
WHITE.AddCondition(5, "IsHomozygousFor", "i")

COLOR_PHENOTYPES = [BLACK, LIVER, BLUE, ISABELLA, RED, DILUTE_RED, WHITE]

#### OTHER
SABLE = Phenotype()
AGOUTI = Phenotype()
TANPOINT = Phenotype()
BRINDLE = Phenotype()
SOLID_EUMELANIN = Phenotype()
SOLID_PHEOMELANIN = Phenotype()
MASK = Phenotype()
NO_MERLE = Phenotype()
MERLE = Phenotype()
DOUBLE_MERLE = Phenotype()
NO_WHITE = Phenotype()
MINOR_WHITE = Phenotype()
PIEBALD = Phenotype()
IRISH_WHITE = Phenotype()
MINOR_TICKING = Phenotype()
NO_TICKING = Phenotype()
TICKING = Phenotype()
ROANING = Phenotype()
NO_GREYING = Phenotype()
GREYING = Phenotype()

## DESCRIPTIONS
SABLE.desc = "Sable"
AGOUTI.desc = "Agouti"
TANPOINT.desc = "Tan points"
BRINDLE.desc = "Brindle"
SOLID_EUMELANIN.desc = "Solid color"
SOLID_PHEOMELANIN.desc = "Solid color"
MASK.desc = "Masked"
NO_MERLE.desc = "No merle"
MERLE.desc = "Merle"
DOUBLE_MERLE.desc = "Double merle"
NO_WHITE.desc = "No white spotting"
MINOR_WHITE.desc = "Little white spotting"
PIEBALD.desc = "Piebald white pattern"
IRISH_WHITE.desc = "Irish white pattern"
NO_TICKING.desc = "No ticking/roaning"
MINOR_TICKING.desc = "Minor ticking"
TICKING.desc = "Ticking"
ROANING.desc = "Roaning"
NO_GREYING.desc = "No greying"
GREYING.desc = "Greying"

### CONDITIONS
SABLE.AddCondition(6, "IsNotHomozygousFor", "K")
SABLE.AddCondition(3, "IsNotHomozygousFor", "e")
SABLE.AddCondition(0, "HasAtLeastOne", "Ay")

AGOUTI.AddCondition(6, "IsNotHomozygousFor", "K")
AGOUTI.AddCondition(3, "IsNotHomozygousFor", "e")
AGOUTI.AddCondition(0, "DoesntHaveAllele", "Ay")
AGOUTI.AddCondition(0, "HasAtLeastOne", "aw")

TANPOINT.AddCondition(6, "IsNotHomozygousFor", "K")
TANPOINT.AddCondition(3, "IsNotHomozygousFor", "e")
TANPOINT.AddCondition(0, "IsHomozygousFor", "at")

BRINDLE.AddCondition(6, "IsNotHomozygousFor", "K")
BRINDLE.AddCondition(3, "IsNotHomozygousFor", "e")
BRINDLE.AddCondition(6, "HasAtLeastOne", "kbr")

SOLID_EUMELANIN.AddCondition(6, "HasAtLeastOne", "K")
SOLID_EUMELANIN.AddCondition(3, "IsNotHomozygousFor", "e")

SOLID_PHEOMELANIN.AddCondition(3, "IsHomozygousFor", "e")

MASK.AddCondition(3, "HasAtLeastOne", "Em")

NO_MERLE.AddCondition(7, "IsHomozygousFor", "m")
MERLE.AddCondition(7, "IsExactly", ["M", "m"])
MERLE.AddCondition(3, "IsNotHomozygousFor", "e")
DOUBLE_MERLE.AddCondition(7, "IsHomozygousFor", "M")
DOUBLE_MERLE.AddCondition(3, "IsNotHomozygousFor", "e")

NO_WHITE.AddCondition(8, "IsHomozygousFor", "S")

MINOR_WHITE.AddCondition(8, "HasAtLeastOne", "S")
MINOR_WHITE.AddCondition(8, "IsNotHomozygousFor", "S")

PIEBALD.AddCondition(8, "DoesntHaveAllele", "S")
PIEBALD.AddCondition(8, "HasAtLeastOne", "sp")

IRISH_WHITE.AddCondition(8, "IsHomozygousFor", "si")

MINOR_TICKING.AddCondition(9, "IsExactly", ["T", "t"])
MINOR_TICKING.AddCondition(8, "IsNotHomozygousFor", "S")

TICKING.AddCondition(9, "HasAtLeastOne", "T")
TICKING.AddCondition(9, "DoesntHaveAllele", "t")
TICKING.AddCondition(8, "IsNotHomozygousFor", "S")

ROANING.AddCondition(8, "IsNotHomozygousFor", "S")
ROANING.AddCondition(9, "DoesntHaveAllele", "T")
ROANING.AddCondition(9, "HasAtLeastOne", "Tr")

GREYING.AddCondition(4, "HasAtLeastOne", "G")
GREYING.AddCondition(3, "IsNotHomozygousFor", "e")

OTHER_PHENOTYPES = [SABLE, AGOUTI, TANPOINT, BRINDLE, SOLID_EUMELANIN, SOLID_PHEOMELANIN, MASK, MERLE, DOUBLE_MERLE,
                    NO_WHITE, MINOR_WHITE, PIEBALD, IRISH_WHITE, MINOR_TICKING, TICKING, ROANING, GREYING, NO_GREYING,
                    NO_MERLE, NO_TICKING]

PHEN_DICT = dict()
for elem in OTHER_PHENOTYPES + COLOR_PHENOTYPES:
    PHEN_DICT[elem.desc] = elem


class Dog:
    def __init__(self, genotype, coat=None, dogid=None, name=None, age=None, dam=None, sire=None, sex=None):
        self.genotype = genotype
        self.coat = coat
        self.id = dogid
        self.name = name
        self.age = age
        self.dam = dam
        self.sire = sire
        self.sex = sex
        self.children = []
        self.relatives = []
        self.childPossibilities = []
        self.childConditions = []

    def ToList(self):
        return [("id", int(self.id)),
                ("name", self.name), ("age", str(self.age)), ("sex", self.sex),
                ("coat", "|".join([str(x.desc) for x in self.coat])),
                ("genotype", str(self.genotype)),
                ("mother", str(self.dam.id) if self.dam else None),
                ("father", str(self.sire.id) if self.sire else None),
                ("children", "|".join([str(x.id) for x in self.children])),
                ("relatives", "|".join([str(x.id) for x in self.relatives]))]

    def ToDesc(self):
        return [str(self.id)+". "+self.name, "Male" if self.sex == "m" else "Female", str(self.age),
                "\n".join([str(x.desc) for x in self.coat])]

    def CreateParents(self):
        if type(self.dam) != Dog:
            self.dam = Dog(Genotype(), "Mother of {}".format(self.name), sex="f")
            self.dam.children.append(self)
        if type(self.sire) != Dog:
            self.sire = Dog(Genotype(), "Father of {}".format(self.name), sex="m")
            self.sire.children.append(self)

    def CreateAllParentConditions(self):
        self.CreateParents()
        for locus_number in range(len(self.genotype)):
            own_locus = self.genotype[locus_number]
            own_locus.CreateParentConditions()

    def ImposeAllParentConditions(self):
        for locus_number in range(len(self.genotype)):
            own_locus = self.genotype[locus_number]
            for condition in own_locus.dam_conditions:
                print("DAM", condition.name, condition.argument)
                condition.Execute(self.dam.genotype)
            for condition in own_locus.sire_conditions:
                print("SIRE", condition.name, condition.argument)
                condition.Execute(self.sire.genotype)
            for condition in own_locus.general_conditions:
                print("GEN", condition.name, condition.argument)
                condition.Execute(self.dam.genotype, self.sire.genotype)

    def CreateChildData(self):
        self.childPossibilities = []
        self.childConditions = []
        for locus_number in range(len(self.genotype)):
            locus = self.genotype[locus_number]
            self.childConditions.append(locus.CreateChildConditions())
            self.childPossibilities.append(locus.CreateChildPossibilities())

    def ImposeChildConditions(self):
        self.CreateChildData()
        for child in self.children:
            for condition in self.childConditions:
                if type(condition) == Condition:
                    reverse = ReverseCondition(condition)
                    reverse.Execute(child.genotype)
                if type(condition) == MultipleCondition:
                    condition.Execute(child.genotype)
            child.CreateChildData()

    def Breed(self, partner):
        if self.sex == partner.sex:
            return "Error: can't breed same sex dogs"
        else:
            return BreedingResult(self, partner)


class BreedingResult:
    def __init__(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2
        self.Preparations()
        self.possible_loci = []
        self.CalculatePossibleLoci()
        self.possibleGenotype = PossibleGenotype(self.possible_loci)

    def Preparations(self):
        self.parent1.CreateChildData()
        self.parent2.CreateChildData()

    def CalculatePossibleLoci(self):
        for locus_number in range(len(self.parent1.genotype)):
            parent1_locus = self.parent1.childPossibilities[locus_number]
            parent2_locus = self.parent2.childPossibilities[locus_number]
            self.possible_loci.append(parent1_locus.Combine(parent2_locus, locus_number))

##### TESTS


# test_genotype = Genotype()
# ISABELLA.ImposeConditions(test_genotype)
# BLACK.ImposeConditions(test_genotype)
# possible_phenotypes = [x.desc for x in OTHER_PHENOTYPES + COLOR_PHENOTYPES if x.TestConditions(test_genotype)[0]]
# print(possible_phenotypes)
# test_dog = Dog(test_genotype, "Test Dog")
# test_dog.CreateParents()
# ISABELLA.ImposeConditions(test_dog.dam.genotype)
# BLACK.ImposeConditions(test_dog.sire.genotype)
# print(test_dog.dam.genotype)
# print(test_dog.sire.genotype)
# test_dog.CreateAllParentConditions()
# test_dog.ImposeAllParentConditions()
# print(test_dog.genotype)
# print(test_dog.dam.genotype)
# print(test_dog.sire.genotype)
#
# test_dog.CreateChildData()
# print(test_dog.genotype)
# test_dog.dam.ImposeChildConditions()
# print(test_dog.dam.childConditions)
# print(test_dog.genotype)
# test_dog.CreateAllParentConditions()
# test_dog.ImposeAllParentConditions()
#
# print(test_dog.genotype)
# print(test_dog.dam.genotype)
# print(test_dog.sire.genotype)
# print("\n\n\n")
#
# test_dog.dam.Breed(test_dog.sire)
# breeding = test_dog.dam.Breed(test_dog.sire)
# print(breeding.possibleGenotype)
# print(breeding.possibleGenotype.TestMultiplePhenotypes([LIVER]))
# a = Locus(0)
# a1 = [a]
# c = Condition(0, "IsNotHomozygousFor", "a")
# print(c.Execute(a1))
