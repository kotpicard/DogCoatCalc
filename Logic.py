from text_en import *

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


def unique(arr):
    present = []
    for elem in arr:
        if elem not in present:
            present.append(elem)
    return present


class Allele:
    def __init__(self, value):
        self.value = value.strip()

    def __eq__(self, other):
        return other == self.value

    def __repr__(self):
        return self.value.strip()

    def __str__(self):
        return self.value.strip()

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
        self.value = "Any allele except {}".format(str(self.notValue)).replace('"', "").replace("'", "").replace("[",
                                                                                                                 "").replace(
            "]", "")

    def __eq__(self, other):
        print([x for x in self.notValue], other, "THIS")
        return all([x != other for x in self.notValue])

    def __ne__(self, other):
        return True

    def __add__(self, other):
        if type(other) == NotAllele:
            print("BEFORENOTVALUE", self.notValue)
            self.notValue += other.notValue
            self.notValue = unique(self.notValue)
            self.value = "Any allele except {}".format(str(self.notValue)).replace('"', "").replace("'", "").replace(
                "[", "").replace("]", "")
            print("AFTER NOTVALUE", self.notValue, self.value)
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
        allele2 = allele2.strip()
        self.alleles = []
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

    def CanBeReplacedBy(self, original, replacement, force_replace):
        # replacement is ALLELE
        print("TESTING REPLACEMENT", end=" ")
        print(original, replacement)
        if type(replacement) == AnyAllele:
            return True
        elif type(original) == Allele:
            if type(replacement) == Allele and original == replacement:
                return "test other" if force_replace else True
            else:
                return False
        elif type(replacement) == Allele and type(original) == NotAllele and replacement.value in original.notValue:
            return False
        elif type(original) == NotAllele and type(replacement) == NotAllele and all(
                [x in original.notValue for x in replacement.notValue]):
            return "test other" if force_replace else True
        else:
            print("CAN REPLACE")
            return True

    def CanReplace(self, replacement, force_replacement=False):
        # replacement is locus
        result = []
        if type(replacement) == Locus:
            replacement = replacement.alleles
        print("replacing", self.alleles, replacement)
        if self.CanBeReplacedBy(self.alleles[0], replacement[0], force_replacement) and self.CanBeReplacedBy(
                self.alleles[1],
                replacement[1], force_replacement):
            if self.CanBeReplacedBy(self.alleles[0], replacement[0],
                                    force_replacement) == "test other" or self.CanBeReplacedBy(
                self.alleles[1],
                replacement[1], force_replacement) == "test other":
                result.append("test other 1")
            else:
                result.append(1)

        if self.CanBeReplacedBy(self.alleles[0], replacement[1], force_replacement) and self.CanBeReplacedBy(
                self.alleles[1],
                replacement[0], force_replacement):
            if self.CanBeReplacedBy(self.alleles[0], replacement[1],
                                    force_replacement) == "test other" or self.CanBeReplacedBy(
                self.alleles[0],
                replacement[1], force_replacement) == "test other":
                result.append("test other -1")
            result.append(-1)
        elif all([type(x) == AnyAllele for x in replacement]):
            result.append(True)
        else:
            result.append(False)

        if "test other 1" in result:
            print("test other 1")
            if -1 in result:
                print("-1")
                return -1

            else:
                print("1")
                return 1
        elif "test other -1" in result:
            print("test other -1")
            if 1 in result:
                print("1")
                return 1
            else:
                print("-1")
                return -1
        elif False in result:
            return False
        else:
            return result[0]

    def replace(self, replacement, force_replacement=False):
        # replacement is locus
        # print("EQUALITY TEST", self == replacement)
        if type(replacement) == Locus:
            replacement = replacement.alleles
        order = self.CanReplace(replacement, force_replacement)
        print(force_replacement)
        if type(order) == int:
            self.alleles = self.alleles[::order]
            print(self.alleles)
            temp = []
            for i in range(2):
                # print("original", self.alleles[i], "replacement", replacement[i])
                if type(replacement[i]) != AnyAllele:
                    if type(self.alleles[i]) == type(replacement[i]) == NotAllele:
                        temp.append(self.alleles[i] + replacement[i])
                        print("ADDED TO NOTVALUE")
                        print(temp)
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
        print(target[self.locus].CanReplace(self.cond(target), False))
        print(target[self.locus], self.cond(target))
        return target[self.locus].replace(self.cond(target))


class MultipleCondition:
    def __init__(self, cond1, cond2, connectiontype="AND"):
        self.name = None
        self.argument = None
        self.type = connectiontype

        self.cond1 = cond1
        print(type(self.cond1))
        if type(cond1) != MultipleCondition:
            self.locus1 = cond1.locus
        if type(cond1) == Condition:
            self.cond1 = ReverseCondition(cond1)
        self.cond2 = cond2
        if type(cond2) != MultipleCondition:
            self.locus2 = cond2.locus
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
            print(type(self.cond1))
            if type(self.cond1) != MultipleCondition:
                target = target[self.locus1]
                print(target.CanReplace(self.cond1.cond(target), False))
                return target.CanReplace(self.cond1.cond(target))
            elif type(self.cond1) == MultipleCondition:
                return self.cond1.CanResolve(target, target)

    def TestCond2(self, target):
        if self.type == "AND":
            print("testing", self.cond2.name)
            if type(self.cond2) != MultipleCondition:
                target = target[self.locus2]
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
            print("direction1, direction2", direction1, direction2)
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
            print("Error: cannot resolve multiple condition on these targets")
            return [0,0]


class Genotype:
    def __init__(self, loci=None):
        self.status = True
        if not loci:
            self.loci = [Locus(i) for i in range(10)]
        else:
            self.loci = loci

    def CreateFromString(self, string):
        loci_text = string.split("|")
        for i in range(10):
            print(i, loci_text[i] if "K" in loci_text[i] else "")
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
        return results, probabilities
        # if all(results):
        #     probability = 1
        #     for p in probabilities:
        #         probability *= p
        #     return True, probability
        # else:
        #     return False, 0


class Phenotype:
    def __init__(self, type, display=True):
        self.desc = type+"description of phenotype"
        self.conditions = []  # list of conditions for this phenotype to show
        self.reverseConditions = []
        self.type = type
        self.display = display

    def AddCondition(self, locus, cond, argument):
        self.conditions.append(Condition(locus, cond, argument))

    def AddMultipleCondition(self, arguments):
        cond1 = Condition(*arguments[0])
        cond2 = Condition(*arguments[1])
        self.conditions.append(MultipleCondition(cond1, cond2))

    def CreateReverseConditions(self):
        self.reverseConditions = [ReverseCondition(x) if type(x)==Condition else x for x in self.conditions]

    def TestConditions(self, genotype):
        tests = [x.Execute(genotype) for x in self.conditions]
        prob = 1
        for test in tests:
            prob *= test[1]
        return all([x[0] for x in tests]), prob

    def ImposeConditions(self, genotype):
        self.CreateReverseConditions()
        for cond in self.reverseConditions:
            # print(cond.locus, cond.name)
            result = cond.Execute(genotype)
            if not result:
                genotype.status = False


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
BLACK = Phenotype("COLOR_BLACK")
LIVER = Phenotype("COLOR_BLACK")
BLUE = Phenotype("COLOR_BLACK")
ISABELLA = Phenotype("COLOR_BLACK")

## COLOR - PHEOMELANIN
RED = Phenotype("COLOR_RED")
DILUTE_RED = Phenotype("COLOR_RED")

## WHITE
WHITE = Phenotype("COLOR_RED")

# COLORS - NAMES
BLACK.desc = TEXT_BLACK
LIVER.desc = TEXT_LIVER
BLUE.desc = TEXT_BLUE
ISABELLA.desc = TEXT_ISABELLA
RED.desc = TEXT_RED
DILUTE_RED.desc = TEXT_DILUTE_RED
WHITE.desc = TEXT_WHITE

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
SABLE = Phenotype("AGOUTI")
AGOUTI = Phenotype("AGOUTI")
TANPOINT = Phenotype("AGOUTI")
BRINDLE = Phenotype("K_LOCUS")
SOLID_EUMELANIN = Phenotype("K_LOCUS")
SOLID_PHEOMELANIN = Phenotype("E_LOCUS")
MASK = Phenotype("E_LOCUS")
NO_MERLE = Phenotype("MERLE", False)
MERLE = Phenotype("MERLE")
DOUBLE_MERLE = Phenotype("MERLE")
NO_WHITE = Phenotype("WHITE")
MINOR_WHITE = Phenotype("WHITE")
PIEBALD = Phenotype("WHITE")
IRISH_WHITE = Phenotype("WHITE")
MINOR_TICKING = Phenotype("TICKING")
NO_TICKING = Phenotype("TICKING", False)
TICKING = Phenotype("TICKING")
ROANING = Phenotype("TICKING")
ROANING_AND_TICKING = Phenotype("TICKING")
GREYING = Phenotype("GREYING")
NO_GREYING = Phenotype("GREYING", False)
ALLOW_AGOUTI = Phenotype("K_LOCUS", False)
NORMAL_EXTENSION = Phenotype("E_LOCUS", False)

## DESCRIPTIONS
SABLE.desc = TEXT_SABLE
AGOUTI.desc = TEXT_AGOUTI
TANPOINT.desc = TEXT_TANPOINT
BRINDLE.desc = TEXT_BRINDLE
SOLID_EUMELANIN.desc = TEXT_SOLID_EUMELANIN
SOLID_PHEOMELANIN.desc = TEXT_SOLID_EUMELANIN
MASK.desc = TEXT_MASK
NO_MERLE.desc = TEXT_NO_MERLE
MERLE.desc = TEXT_MERLE
DOUBLE_MERLE.desc = TEXT_DOUBLE_MERLE
NO_WHITE.desc = TEXT_NO_WHITE
MINOR_WHITE.desc = TEXT_MINOR_WHITE
PIEBALD.desc = TEXT_PIEBALD
IRISH_WHITE.desc = TEXT_IRISH_WHITE
NO_TICKING.desc = TEXT_NO_TICKING
MINOR_TICKING.desc = TEXT_MINOR_TICKING
TICKING.desc = TEXT_TICKING
ROANING.desc = TEXT_ROANING
ROANING_AND_TICKING.desc = TEXT_ROANING_AND_TICKING
GREYING.desc = TEXT_GREYING

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

TICKING.AddCondition(9, "IsHomozygousFor", "T")
TICKING.AddCondition(8, "IsNotHomozygousFor", "S")

ROANING_AND_TICKING.AddCondition(9, "IsExactly", ["T", "Tr"])
ROANING_AND_TICKING.AddCondition(8, "IsNotHomozygousFor", "S")

NO_TICKING.AddCondition(9, "IsHomozygousFor", "t")

ROANING.AddCondition(8, "IsNotHomozygousFor", "S")
ROANING.AddCondition(9, "DoesntHaveAllele", "T")
ROANING.AddCondition(9, "HasAtLeastOne", "Tr")

GREYING.AddCondition(4, "HasAtLeastOne", "G")
GREYING.AddCondition(3, "IsNotHomozygousFor", "e")

NO_GREYING.AddCondition(4, "IsHomozygousFor", "g")
ALLOW_AGOUTI.AddCondition(6, "IsHomozygousFor", "k")
NORMAL_EXTENSION.AddCondition(3, "DoesntHaveAllele", "Em")
NORMAL_EXTENSION.AddCondition(3, "IsNotHomozygousFor", "e")

OTHER_PHENOTYPES = [SABLE, AGOUTI, TANPOINT, BRINDLE, SOLID_EUMELANIN, SOLID_PHEOMELANIN, MASK, MERLE, DOUBLE_MERLE,
                    NO_WHITE, MINOR_WHITE, PIEBALD, IRISH_WHITE, MINOR_TICKING, TICKING, ROANING, ROANING_AND_TICKING,
                    GREYING,
                    NO_MERLE, NO_TICKING, NO_GREYING, ALLOW_AGOUTI, NORMAL_EXTENSION]

ALL_PHENOTYPES = COLOR_PHENOTYPES + OTHER_PHENOTYPES

PHEN_DICT = dict()
for elem in OTHER_PHENOTYPES + COLOR_PHENOTYPES:
    PHEN_DICT[elem.desc] = elem


class Goal:
    def __init__(self, elements):
        self.elements = elements

    def ToText(self):
        goaldata = self.ToList()
        text = "*".join([x[0] for x in goaldata])
        return text

    def __eq__(self, other):
        if type(other) == Goal:
            return other.ToText() == self.ToText()

    def ToList(self):
        return [(x.desc, x.type) for x in self.elements]

    def CheckConditions(self, target):
        # target is possiblegenotype
        results, probs = target.TestMultiplePhenotypes(self.elements)
        # results is true/false if possible, probs is % of possible genotypes that pass the test for each element
        elementresults = []
        # result meanings
        # 0: impossible
        # 1: might be possible (any allele in genotype)
        # 2: is possible (known alleles)
        # 3: is certain
        for i in range(len(results)):
            print(i, len(results))
            if not results[i]:
                elementresults.append(0)
            else:
                # we know it's at least possible - need to check for nonspecific alleles in given locus
                loci = [x.locus for x in self.elements[i].conditions]
                temp = []
                for ln in loci:
                    locus = target.loci[ln]
                    possible_locus_versions = [x[0] for x in locus]
                    # if there is any version where we don't know an allele it's not specific
                    nonspecific = any(
                        [not all([type(x) == Allele for x in l.alleles]) for l in possible_locus_versions])
                    if nonspecific:
                        # might be possible but we can't be sure as parent alleles are not fully known
                        temp.append(1)
                    else:
                        if probs[i] != 1:
                            # result is specific but uncertain
                            temp.append(2)
                        else:
                            # result is both specific and certain
                            temp.append(3)
                print(temp)
                elementresults.append(sum(temp) / len(temp))
        return elementresults


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
        self.coatdesc = "| ".join([str(x.desc) for x in self.coat])

    def SetParent(self, parent):
        if parent.sex == "f":
            self.dam = parent
        else:
            self.sire = parent
        if self not in parent.children:
            parent.children.append(self)
        print("CHIDLREN", parent.children)
        self.ImposeParentAndChildConditions()

    def UpdateCoat(self):
        possible_phenotypes = [x for x in ALL_PHENOTYPES if x.TestConditions(self.genotype)[0]]
        print([x.desc+x.type for x in possible_phenotypes], "UPDATING")
        append = False
        for phen in possible_phenotypes:
            if sum([x.type == phen.type for x in possible_phenotypes]) == 1:
                if not phen in self.coat:
                    print("APPENDING", phen.desc, phen.type)
                    self.coat.append(phen)
                # if phen.type == "GREYING":
                #     if any([type(x) == Allele and x == Allele("G") for x in self.genotype[4].alleles]):
                #         append = True  # fix for no non-greying
                # if phen.type == "E_LOCUS":
                #     if phen.desc == SOLID_EUMELANIN:
                #         if all([type(x) == Allele and x == Allele("e") for x in self.genotype[3].alleles]):
                #             append = True  # fix for no normal extension
                # else:
                #     append = True


    def HasMother(self):
        return True if type(self.dam) == Dog and "Mother of" not in self.dam.name else False

    def HasFather(self):
        return True if type(self.sire) == Dog and "Father of" not in self.sire.name else False

    def ToList(self):
        return [("id", int(self.id)),
                ("name", self.name), ("age", str(self.age)), ("sex", self.sex),
                ("coat", "|".join([str(x.desc) for x in self.coat])),
                ("genotype", str(self.genotype)),
                ("mother", str(self.dam.id) if self.dam else None),
                ("father", str(self.sire.id) if self.sire else None),
                ("children", "|".join([str(x.id) for x in self.children]) if self.children else None),
                ("relatives", "|".join([str(x.id) for x in self.relatives]) if self.relatives else None)]

    def ToDesc(self):
        return [str(self.id) + ". " + self.name, "Male" if self.sex == "m" else "Female", str(self.age),
                "\n".join([str(x.desc) for x in self.coat if x.display])]

    def CreateParents(self):
        if type(self.dam) != Dog:
            self.dam = Dog(Genotype(), name="Mother of {}".format(self.name), sex="f", coat=[])
        if not self in self.dam.children:
            self.dam.children.append(self)
        print(type(self.dam.children))
        if type(self.sire) != Dog:
            self.sire = Dog(Genotype(), name="Father of {}".format(self.name), sex="m", coat=[])
        if not self in self.sire.children:
            self.sire.children.append(self)

    def CreateAllParentConditions(self):
        self.CreateParents()
        for locus_number in range(len(self.genotype)):
            own_locus = self.genotype[locus_number]
            own_locus.CreateParentConditions()

    def ImposeParentAndChildConditions(self):
        self.CreateAllParentConditions()
        self.ImposeAllParentConditions()
        self.dam.ImposeChildConditions()
        self.sire.ImposeChildConditions()

    def ImposeAllParentConditions(self):
        print("imposing conditions on parents {} and {}".format(self.dam.name, self.sire.name))
        for locus_number in range(len(self.genotype)):
            own_locus = self.genotype[locus_number]
            for condition in own_locus.dam_conditions:
                # print("DAM", condition.name, condition.argument)
                condition.Execute(self.dam.genotype)
            for condition in own_locus.sire_conditions:
                # print("SIRE", condition.name, condition.argument)
                condition.Execute(self.sire.genotype)
            for condition in own_locus.general_conditions:
                # print("GEN", condition.name, condition.argument)
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
        print("impose child conditions")
        if self.children:
            for child in self.children:
                for condition in self.childConditions:
                    if type(condition) == Condition:
                        reverse = ReverseCondition(condition)
                        print(reverse)
                        reverse.Execute(child.genotype)
                    if type(condition) == MultipleCondition:
                        condition.Execute(child.genotype)
                child.CreateChildData()

    def Breed(self, partner, breedingtype, goals=None):
        if breedingtype == "Conventional":
            if self.sex == partner.sex:
                return "Error: can't breed same sex dogs"
            else:
                return BreedingResult(self, partner, breedingtype, goals)
        elif breedingtype == "PickMate":
            return BreedingResult(self, partner, breedingtype, goals)


class BreedingResult:
    def __init__(self, parent1, parent2, type, goals=None):
        self.type = type
        self.parent1 = parent1
        self.parent2 = parent2
        self.goals = goals
        print("I RECEIVED THESE GOALS: ", goals)
        if self.goals:
            self.goalslist = [x.ToList() for x in self.goals]
        else:
            self.goalslist = []
            self.goals = []
            self.goalscores = None
        if self.type == "Conventional":
            self.Preparations()
            self.possible_loci = []
            self.CalculatePossibleLoci()
            self.possibleGenotype = PossibleGenotype(self.possible_loci)
            self.possiblePhens, self.impossiblePhens = self.GetPossiblePhenotypes()
            self.possiblePhensAsGoals = [Goal([x]).ToList() for x in self.possiblePhens]
            print(self.possiblePhensAsGoals)
            self.impossiblePhensAsGoals = [Goal([x]).ToList() for x in self.impossiblePhens]
            self.goalscores = self.GetGoalScores()
        if self.type == "PickMate":
            self.mainparent = None
            self.bestmate = self.GetBestPartner()

    def ToText(self):
        return self.type + "|" + str(self.parent1.id) + "|" + str(self.parent2.id) + "|" + "&".join(
            [goal.ToText() for goal in self.goals])

    def Preparations(self):
        self.parent1.CreateChildData()
        self.parent2.CreateChildData()

    def GetBestPartner(self):
        self.mainparent = self.parent1 if type(self.parent1) == Dog else self.parent2
        otherpartners = self.parent1 if type(self.parent1) == list else self.parent2
        results = []
        for partner in otherpartners:
            tempbreeding = BreedingResult(self.mainparent, partner, "Conventional", self.goals)
            results.append(tempbreeding.goalscores)
        filter_fails = [all([0 not in goal for goal in partner]) for partner in results]
        filtered_results = []
        averages = [sum([sum(goal) / len(goal) for goal in partner]) / len(partner) for partner in results]
        for i, test in enumerate(filter_fails):
            if test:
                filtered_results.append((averages[i], results[i], otherpartners[i]))
        else:
            for i in range(len(averages)):
                filtered_results.append((averages[i], results[i], otherpartners[i]))
        filtered_results.sort(key=lambda x: x[0], reverse=True)
        return filtered_results[0]

    def GetPossiblePhenotypes(self):
        possible_phenotypes = [x for x in ALL_PHENOTYPES[:-1] if x.TestConditions(self.possibleGenotype)[0]]
        impossible_phenotypes = [x for x in ALL_PHENOTYPES[:-1] if x not in possible_phenotypes]
        return possible_phenotypes, impossible_phenotypes

    def CalculatePossibleLoci(self):
        for locus_number in range(len(self.parent1.genotype)):
            parent1_locus = self.parent1.childPossibilities[locus_number]
            parent2_locus = self.parent2.childPossibilities[locus_number]
            self.possible_loci.append(parent1_locus.Combine(parent2_locus, locus_number))

    def GetGoalScores(self):
        results = []
        if self.goals:
            for goal in self.goals:
                results.append(goal.CheckConditions(self.possibleGenotype))
        return results

#### TESTS

#
# test_genotype = Genotype()
# ISABELLA.ImposeConditions(test_genotype)
# BLACK.ImposeConditions(test_genotype)
# possible_phenotypes = [x.desc for x in OTHER_PHENOTYPES + COLOR_PHENOTYPES if x.TestConditions(test_genotype)[0]]
# print(possible_phenotypes)
# test_dog = Dog(test_genotype, name="Test Dog", coat=[BLACK])
# test_dog.CreateParents()
# ISABELLA.ImposeConditions(test_dog.dam.genotype)
# ISABELLA.ImposeConditions(test_dog.sire.genotype)
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

# print(test_dog.genotype)
# print(test_dog.dam.genotype)
# print(test_dog.sire.genotype)
# print("\n\n\n")
#
# test_dog.dam.Breed(test_dog.sire)
# breeding = test_dog.dam.Breed(test_dog.sire)
# print(breeding.possibleGenotype)
# print(breeding.possibleGenotype.TestMultiplePhenotypes([ISABELLA, BLACK, BLUE, NO_WHITE]), "THIS HERE")
# goal = Goal([ISABELLA, BLACK, BLUE, NO_WHITE])
# print(goal.CheckConditions(breeding.possibleGenotype))
# a = Locus(0)
# a1 = [a]
# c = Condition(0, "IsNotHomozygousFor", "a")
# print(goal.ToList())
