from CustomEvents import *
from GoalCtrl import GoalCtrl
from LinkBoxCtrl import LinkBoxCtrl
from GuiConstants import *
from RoundedButton import RoundedButton
from BrowseDogsPanel import BrowseDogsPanel
from LinkButton import LinkButton
from DogSelectDialog import DogSelectDialog
from text_en import *
from AddDogPanel import AddDogPanel


class DefaultPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        DefaultPanelSizer = wx.BoxSizer(wx.VERTICAL)

        top_half = wx.Panel(self)
        DefaultPanelSizer.Add(top_half, 1, wx.EXPAND)

        bottom_half = wx.Panel(self)
        DefaultButtonSizer = wx.GridSizer(2, 2, 20, 20)  # 2 rows, 2 cols, 10px spacing

        ButtonMyDogs = wx.Button(bottom_half, label=TEXT_MYDOGS)
        ButtonMyBreedings = wx.Button(bottom_half, label=TEXT_MYBREEDINGS)
        ButtonBreedingCalc = wx.Button(bottom_half, label=TEXT_BREEDINGCALC)
        ButtonBreedingGoals = wx.Button(bottom_half, label=TEXT_MYGOALS)

        ButtonMyDogs.SetFont(FONT_BIG)
        ButtonMyBreedings.SetFont(FONT_BIG)
        ButtonBreedingCalc.SetFont(FONT_BIG)
        ButtonBreedingGoals.SetFont(FONT_BIG)

        ButtonMyDogs.Bind(wx.EVT_BUTTON, self.ClickedMyDogsButton)
        ButtonMyBreedings.Bind(wx.EVT_BUTTON, self.ClickedMyBreedingsButton)
        ButtonBreedingCalc.Bind(wx.EVT_BUTTON, self.ClickedBreedingCalcButton)
        ButtonBreedingGoals.Bind(wx.EVT_BUTTON, self.ClickedBreedingGoalsButton)

        DefaultButtonSizer.Add(ButtonMyDogs, 0, wx.EXPAND)
        DefaultButtonSizer.Add(ButtonMyBreedings, 0, wx.EXPAND)
        DefaultButtonSizer.Add(ButtonBreedingCalc, 0, wx.EXPAND)
        DefaultButtonSizer.Add(ButtonBreedingGoals, 0, wx.EXPAND)

        bottom_half.SetSizer(DefaultButtonSizer)

        DefaultPanelSizer.Add(bottom_half, 2, wx.EXPAND | wx.ALL, 20)

        self.SetSizer(DefaultPanelSizer)

    def ClickedMyDogsButton(self, e):
        evt = NavigationEvent(destination="MyDogs")
        wx.PostEvent(self.GetParent(), evt)

    def ClickedMyBreedingsButton(self, e):
        evt = NavigationEvent(destination="AllBreedingResults")
        wx.PostEvent(self.GetParent(), evt)

    def ClickedBreedingCalcButton(self, e):
        evt = NavigationEvent(destination="BreedingCalc")
        print("breeding calc")
        wx.PostEvent(self.GetParent(), evt)

    def ClickedBreedingGoalsButton(self, e):
        evt = NavigationEvent(destination="Goals", data=None)
        wx.PostEvent(self.GetParent(), evt)


class MyDogsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.dogspanel = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 8)
        self.Bind(EVT_OPEN_DOG_PAGE, self.PassToMainWindow)
        sizer = wx.BoxSizer(wx.VERTICAL)
        button = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_ADD,
                               colors=BUTTONCOLORS)
        button2 = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_REFRESH,
                                colors=BUTTONCOLORS)
        button3 = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_BACK,
                                colors=BUTTONCOLORS)
        button3.Bind(wx.EVT_LEFT_DOWN, self.GoBack)
        button2.Bind(wx.EVT_LEFT_DOWN, self.Reload)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.dogspanel, 5, wx.EXPAND | wx.ALL, 10)
        buttonsizer.Add(button, 0, wx.ALL, 10)
        buttonsizer.AddStretchSpacer()
        buttonsizer.Add(button2, 0, wx.ALL, 10)
        buttonsizer.AddStretchSpacer()
        buttonsizer.Add(button3, 0, wx.ALL, 10)
        sizer.Add(buttonsizer, 0, wx.ALL, 0)
        self.SetSizer(sizer)
        button.Bind(wx.EVT_LEFT_DOWN, self.AddDog)

    def PassToMainWindow(self, e):
        wx.PostEvent(self.GetParent(), e)

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), OpenMainMenu())

    def Fill(self, elems):
        print("FILLING")
        for i in range(len(elems)):
            self.dogspanel.AddElement(elems[i], i)

    def AddDog(self, e):
        evt = AddDogEvent()
        wx.PostEvent(self.GetParent(), evt)

    def Reload(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="MyDogs"))


class DogPanel(wx.Panel):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        dogdatasizer = wx.BoxSizer(wx.VERTICAL)
        namelabel = wx.StaticText(self, label=values[0])
        dogid = int(values[0].split(".")[0])
        self.dogid = dogid
        self.name = values[0].split(".")[1]
        self.age = values[2]
        self.sex = values[1]
        self.coat = values[3]
        previd = dogid - 1
        nextid = dogid + 1
        namelabel.SetFont(FONT_BIG)
        namelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        dogdatasizer.Add(namelabel, 0, wx.ALL)
        agelabel = wx.StaticText(self, label=TEXT_AGE + self.age)
        sexlabel = wx.StaticText(self, label=TEXT_SEX + self.sex)

        # breedlabel = wx.StaticText(self, label=TEXT_BREED)
        coatlabel = wx.StaticText(self, label=TEXT_COAT + values[3])
        viewgenotypebutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_VIEWGENOTYPE,
                                           colors=BUTTONCOLORS)
        viewgenotypebutton.Bind(wx.EVT_LEFT_DOWN, self.OpenGenotypeView)

        breedingtestsbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_BREEDINGCALC,
                                            colors=BUTTONCOLORS)

        breedingtestsbutton.Bind(wx.EVT_LEFT_DOWN, self.OpenCalcWithData)

        dogdatasizer.Add(agelabel, 0, wx.ALL)
        dogdatasizer.Add(sexlabel, 0, wx.ALL)
        # dogdatasizer.Add(breedlabel, 0, wx.ALL)
        dogdatasizer.Add(coatlabel, 0, wx.ALL)
        dogdatasizer.Add(viewgenotypebutton, 0, wx.ALL, 5)
        dogdatasizer.Add(breedingtestsbutton, 0, wx.ALL, 5)

        linkeddatasizer = wx.BoxSizer(wx.VERTICAL)
        relativeslabel = wx.StaticText(self, label=TEXT_RELATIVES)
        relativeslabel.SetFont(FONT_BIG)
        relativeslinkbox = LinkBoxCtrl(self)
        addrelativebutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_ADDRELATIVE,
                                          colors=BUTTONCOLORS)
        addrelativebutton.Bind(wx.EVT_LEFT_DOWN, self.AddRelative)
        breedingtestresultslabel = wx.StaticText(self, label=TEXT_BREEDINGTESTRESULTS)
        breedingtestresultslabel.SetFont(FONT_BIG)
        breedingtestresultslinkbox = LinkBoxCtrl(self)
        linkeddatasizer.Add(relativeslabel, 0, wx.EXPAND | wx.ALL, 10)
        linkeddatasizer.Add(relativeslinkbox, 0, wx.EXPAND | wx.ALL, 10)
        linkeddatasizer.Add(addrelativebutton, 0, wx.ALL, 10)
        linkeddatasizer.Add(breedingtestresultslabel, 0, wx.EXPAND | wx.ALL, 10)
        linkeddatasizer.Add(breedingtestresultslinkbox, 0, wx.EXPAND | wx.ALL, 10)

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(dogdatasizer, 1, wx.EXPAND | wx.ALL, 20)
        topsizer.AddSpacer(200)
        topsizer.Add(linkeddatasizer, 2, wx.EXPAND | wx.ALL, 20)

        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonprev = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_PREVDOG,
                                   colors=BUTTONCOLORS)
        buttonprev.num = previd
        buttonprev.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)

        buttonnext = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_NEXTDOG,
                                   colors=BUTTONCOLORS)
        buttonnext.num = nextid
        buttonnext.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)
        buttonback = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_BACK,
                                   colors=BUTTONCOLORS)
        buttonback.Bind(wx.EVT_LEFT_DOWN, self.GoBack)

        bottomsizer.Add(buttonprev, 0, wx.ALL, 10)
        bottomsizer.Add(buttonback, 0, wx.ALL, 10)
        bottomsizer.Add(buttonnext, 0, wx.ALL, 10)

        dogsizer = wx.BoxSizer(wx.VERTICAL)
        dogsizer.Add(topsizer, 5, wx.EXPAND | wx.ALL, 10)
        dogsizer.AddSpacer(50)
        dogsizer.Add(bottomsizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(dogsizer)

        self.Bind(EVT_PASS_DOGS, self.PopulateRelativeSelection)
        self.Bind(EVT_OPEN_DOG_PAGE, self.passToMainWindow)
        self.Bind(EVT_RELATIVE_SELECTED, self.GetTypeOfRelative)
        self.Bind(EVT_PASS_DATA, self.ProcessAddRelative)

    def ProcessAddRelative(self, e):
        wx.PostEvent(self.GetParent(), AddRelativeEvent(type=e.relativetype, relativeid=e.relativedogid, dogid=e.dogid))

    def GetTypeOfRelative(self, e):
        PopupAddRelative(self, relativedogid=e.dogid, dogid=self.dogid)

    def passToMainWindow(self, e):
        wx.PostEvent(self.GetParent(), e)

    def AddRelative(self, e):
        self.PopUpDogSelector()

    def PopulateRelativeSelection(self, e):
        wx.PostEvent([x for x in self.GetChildren() if type(x) == DogSelectDialog][0], e)

    def PopUpDogSelector(self, dogtype="Relative"):
        dialog = DogSelectDialog(parent=self, who=dogtype, data=self.dogid)
        dialog.Show()

    def OpenCalcWithData(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="BreedingCalc"))
        wx.PostEvent(self.GetParent(), ParentSelectedEvent(dogid=self.dogid, type="parentselected"))

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="MyDogs"))

    def OpenDogPage(self, e):
        num = e.GetEventObject().num
        wx.PostEvent(self.GetParent(), OpenDogPageEvent(num=num))

    def OpenGenotypeView(self, e):
        wx.PostEvent(self.GetParent(), OpenGenotypeViewEvent(dogid=self.dogid))


class PopupAddRelative(wx.Frame):
    def __init__(self, parent, relativedogid, dogid):
        super().__init__(parent)
        self.relativedogid = relativedogid
        self.dogid = dogid
        titlelabel = wx.StaticText(self, label=TEXT_ADDRELATIVE)
        titlelabel.SetFont(FONT_BIG)
        typelabel = wx.StaticText(self, label=TEXT_TYPE)
        typelabel.SetFont(FONT_BIG)
        option1 = wx.RadioButton(self, label=TEXT_PARENT)
        option2 = wx.RadioButton(self, label=TEXT_FULLSIBLING)
        option3 = wx.RadioButton(self, label=TEXT_HALFSIBLING_FATHER)
        option4 = wx.RadioButton(self, label=TEXT_HALFSIBLING_MOTHER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonselect = RoundedButton(self, TEXT_SELECT, colors=BUTTONCOLORS)
        buttoncancel = RoundedButton(self, TEXT_CANCEL, colors=BUTTONCOLORS)
        buttonsizer.AddStretchSpacer()
        buttonsizer.Add(buttonselect, 1, wx.ALL, 15)
        buttonsizer.Add(buttoncancel, 1, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)
        buttoncancel.Bind(wx.EVT_LEFT_DOWN, self.Cancel)
        buttonselect.Bind(wx.EVT_LEFT_DOWN, self.Selected)

        sizer.Add(titlelabel)
        sizer.Add(typelabel)
        sizer.Add(option1)
        sizer.Add(option2)
        sizer.Add(option3)
        sizer.Add(option4)
        sizer.Add(buttonsizer)
        self.SetSizer(sizer)
        self.Layout()
        self.Center()
        self.Show()

    def Selected(self, e):
        values = [x.GetLabel() if x.GetValue() else "" for x in self.GetChildren() if type(x) == wx.RadioButton]
        value = "".join(values)
        wx.PostEvent(self.GetParent(),
                     PassDataEvent(origin="addrelativepopup", target="dogpanel", relativetype=value,
                                   relativedogid=self.relativedogid, dogid=self.dogid))
        self.Destroy()

    def Cancel(self, e):
        self.Destroy()


class GenotypePanel(wx.Panel):
    def __init__(self, parent, data):
        # data is tuple (id, name, genotype object prepared for display)
        # genotype format: (((value, type),(value,type)), etc)
        # values: anyallele, notallele, allele
        super().__init__(parent)
        self.data = data
        self.dogid = data[0]
        name = data[1]
        genotype = data[2]
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        titlelabel = wx.StaticText(self, label="Genotype of " + name)
        titlelabel.SetFont(FONT_BIG)
        backbutton = RoundedButton(self, label=TEXT_BACK, colors=BUTTONCOLORS)
        backbutton.Bind(wx.EVT_LEFT_DOWN, self.GoBack)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(titlelabel, 0, wx.ALL, 5)
        topsizer.AddStretchSpacer(2)
        topsizer.Add(backbutton, 0, wx.ALL, 5)
        genotypesizer = wx.GridSizer(2, 5, 30, 5)
        for locusnumber, locus in enumerate(genotype):
            value1 = locus[0][0]
            value2 = locus[1][0]
            locussizer = wx.BoxSizer(wx.VERTICAL)
            if locus[0][1] == "allele":
                color1 = Color(Hex_ALLELE).rgb
            elif locus[0][1] == "notallele":
                color1 = Color(Hex_NOTALLELE).rgb
            else:
                color1 = Color(Hex_ANYALLELE).rgb
            if locus[1][1] == "allele":
                color2 = Color(Hex_ALLELE).rgb
            elif locus[1][1] == "notallele":
                color2 = Color(Hex_NOTALLELE).rgb
            else:
                color2 = Color(Hex_ANYALLELE).rgb
            button1 = RoundedButton(self, label=value1, colors=(color1, color1))
            button2 = RoundedButton(self, label=value2, colors=(color2, color2))
            button1.Bind(wx.EVT_LEFT_DOWN, self.OpenEditLocus)
            button1.locusnumber = locusnumber
            button2.Bind(wx.EVT_LEFT_DOWN, self.OpenEditLocus)
            button2.locusnumber = locusnumber
            locussizer.Add(button1, 2, wx.EXPAND | wx.ALL, 5)
            locussizer.Add(button2, 2, wx.EXPAND | wx.ALL, 5)
            genotypesizer.Add(locussizer, 1, wx.EXPAND | wx.ALL, 0)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(topsizer, 1, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(genotypesizer, 5, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainsizer)

    def OpenEditLocus(self, e):
        number = e.GetEventObject().locusnumber
        evt = OpenEditLocusEvent(number=number, dogid=self.dogid)
        wx.PostEvent(self.GetParent(), evt)

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), OpenDogPageEvent(num=self.dogid))


class AllelePanel(wx.Panel):
    def __init__(self, parent, number, options, dogid):
        super().__init__(parent)
        self.dogid = dogid
        self.number = number
        self.options = options
        self.type = "allele"
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        titlelabel = wx.StaticText(self, label=TEXT_CHANGE_ALLELE + str(number))
        titlelabel.SetFont(FONT_BIG)

        typelabel = wx.StaticText(self, label=TEXT_TYPE)
        typelabel.SetFont(FONT_BIG)
        typebutton1 = wx.RadioButton(self, label=TEXT_ALLELE, style=wx.RB_GROUP)
        typebutton1.Bind(wx.EVT_RADIOBUTTON, self.LayoutAllele)
        typebutton2 = wx.RadioButton(self, label=TEXT_NOTALLELE)
        typebutton2.Bind(wx.EVT_RADIOBUTTON, self.LayoutNotAllele)
        typebutton3 = wx.RadioButton(self, label=TEXT_ANYALLELE)
        typebutton3.Bind(wx.EVT_RADIOBUTTON, self.LayoutAnyAllele)
        typesizer = wx.BoxSizer(wx.VERTICAL)
        typesizer.Add(typelabel, 0, wx.ALL, 5)
        typesizer.Add(typebutton1, 0, wx.ALL, 5)
        typesizer.Add(typebutton2, 0, wx.ALL, 5)
        typesizer.Add(typebutton3, 0, wx.ALL, 5)
        self.bottomsizer = wx.BoxSizer(wx.VERTICAL)
        self.CreateBottomSizer("allele")
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsave = RoundedButton(self, label=TEXT_SAVE, colors=BUTTONCOLORS)
        buttonsave.Bind(wx.EVT_LEFT_DOWN, self.ProcessEdit)
        buttoncancel = RoundedButton(self, label=TEXT_CANCEL, colors=BUTTONCOLORS)
        buttoncancel.Bind(wx.EVT_LEFT_DOWN, self.CancelButton)
        buttonsizer.AddStretchSpacer(4)
        buttonsizer.Add(buttonsave, 0, wx.ALL, 5)
        buttonsizer.Add(buttoncancel, 0, wx.ALL, 5)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(titlelabel, 0, wx.ALL, 5)
        mainsizer.Add(typesizer, 4, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(self.bottomsizer, 4, wx.EXPAND | wx.ALL, 5)
        mainsizer.Add(buttonsizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(mainsizer)
        self.Layout()

    def CancelButton(self, e):
        wx.PostEvent(self.GetParent(), OpenGenotypeViewEvent(dogid=self.dogid))

    def ProcessEdit(self, e):
        print("processing edit")
        if self.type != "anyallele":
            children = [x.GetWindow() for x in self.bottomsizer.GetChildren()]
            values = [x.GetLabel() for x in children if type(x) in [wx.RadioButton, wx.CheckBox] and x.GetValue()]
            for x in self.bottomsizer.GetChildren():
                print(type(x))
        else:
            values = []
        print(self.type, self.dogid, values)
        wx.PostEvent(self.GetParent(),
                     EditLocusEvent(replacementtype=self.type, dogid=self.dogid, number=self.number, values=values))

    def LayoutAllele(self, e):
        self.CreateBottomSizer("allele")
        self.type = "allele"

    def LayoutNotAllele(self, e):
        self.CreateBottomSizer("notallele")
        self.type = "notallele"

    def LayoutAnyAllele(self, e):
        self.CreateBottomSizer("anyallele")
        self.type = "anyallele"

    def CreateBottomSizer(self, selection):
        self.bottomsizer.Clear(delete_windows=True)
        if selection == "allele":
            valuelabel = wx.StaticText(self, label=TEXT_VALUE)
            valuelabel.SetFont(FONT_BIG)
            self.bottomsizer.Add(valuelabel, 0, wx.ALL, 5)
            self.bottomsizer.Add(wx.RadioButton(self, label=self.options[0], style=wx.RB_GROUP), 0)
            for option in self.options[1:]:
                self.bottomsizer.Add(wx.RadioButton(self, label=option), 0, wx.ALL, 5)
        if selection == "notallele":
            valuelabel = wx.StaticText(self, label=TEXT_NOT_VALUE)
            valuelabel.SetFont(FONT_BIG)
            self.bottomsizer.Add(valuelabel, 0, wx.ALL, 5)
            for option in self.options:
                self.bottomsizer.Add(wx.CheckBox(self, label=option), 0, wx.ALL, 5)
        self.Layout()


class GoalsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        titlelabel = wx.StaticText(self, label=TEXT_MYGOALS)
        titlelabel.SetFont(FONT_BIG)
        self.goalctrl = GoalCtrl(self)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonadd = RoundedButton(self, label=TEXT_ADD, colors=BUTTONCOLORS)
        buttonadd.Bind(wx.EVT_LEFT_DOWN, self.AddGoal)
        buttondelete = RoundedButton(self, label=TEXT_DELETE, colors=BUTTONCOLORS)
        buttondelete.Bind(wx.EVT_LEFT_DOWN, self.DeleteGoal)
        buttonback = RoundedButton(self, label=TEXT_BACK, colors=BUTTONCOLORS)
        buttonback.Bind(wx.EVT_LEFT_DOWN, self.GoBack)
        buttonsizer.Add(buttonadd, 1, wx.ALL, 5)
        buttonsizer.Add(buttondelete, 1, wx.ALL, 5)
        buttonsizer.AddStretchSpacer(1)
        buttonsizer.Add(buttonback, 1, wx.ALL, 5)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(titlelabel, 0, wx.ALL, 10)
        mainsizer.Add(self.goalctrl, 1, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(buttonsizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainsizer)
        self.Layout()
        self.Center()

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), OpenMainMenu())

    def Fill(self, data):
        print("FILLING GOALS")
        self.goalctrl.Fill(data)
        self.Layout()

    def AddGoal(self, e):
        wx.PostEvent(self.GetParent(), OpenAddGoalPanel(origin="goals"))
        print("ADDING")

    def DeleteGoal(self, e):
        dialog = wx.MessageDialog(self, TEXT_DELETE_WARNING, style=wx.OK | wx.CANCEL)
        test = dialog.ShowModal()
        dialog.Destroy()
        if test == wx.ID_OK:
            wx.PostEvent(self.GetParent(), DeleteGoalEvent(data=self.goalctrl.selected))


class AddGoalPanel(wx.Panel):
    def __init__(self, parent, origin):
        super().__init__(parent)
        self.origin = origin
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        goalsizer = wx.BoxSizer(wx.VERTICAL)
        coatlabel = wx.StaticText(self, label=TEXT_ADD_GOAL)
        coatlabel.SetFont(FONT_BIG)
        coatsizer = wx.FlexGridSizer(2, 3, 20, 20)

        blackcolorsizer = wx.BoxSizer(wx.VERTICAL)
        blackcolorsizer.Add(wx.StaticText(self, label=TEXT_BLACK_COLOR), 0, wx.ALL, 5)
        blackcolorsizer.Add(wx.CheckBox(self, label=TEXT_BLACK), 0, wx.ALL, 5)
        blackcolorsizer.Add(wx.CheckBox(self, label=TEXT_LIVER), 0, wx.ALL, 5)
        blackcolorsizer.Add(wx.CheckBox(self, label=TEXT_BLUE), 0, wx.ALL, 5)
        blackcolorsizer.Add(wx.CheckBox(self, label=TEXT_ISABELLA), 0, wx.ALL, 5)

        redcolorsizer = wx.BoxSizer(wx.VERTICAL)
        redcolorsizer.Add(wx.StaticText(self, label=TEXT_RED_COLOR), 0, wx.ALL, 5)
        redcolorsizer.Add(wx.CheckBox(self, label=TEXT_RED), 0, wx.ALL, 5)
        redcolorsizer.Add(wx.CheckBox(self, label=TEXT_DILUTE_RED), 0, wx.ALL, 5)

        spottingsizer = wx.BoxSizer(wx.VERTICAL)
        spottingsizer.Add(wx.StaticText(self, label=TEXT_WHITE_SPOTTING), 0, wx.ALL, 5)
        spottingsizer.Add(wx.CheckBox(self, label=TEXT_NO_WHITE), 0, wx.ALL, 5)
        spottingsizer.Add(wx.CheckBox(self, label=TEXT_MINOR_WHITE), 0, wx.ALL, 5)
        spottingsizer.Add(wx.CheckBox(self, label=TEXT_PIEBALD), 0, wx.ALL, 5)
        spottingsizer.Add(wx.CheckBox(self, label=TEXT_IRISH_WHITE), 0, wx.ALL, 5)

        merlesizer = wx.BoxSizer(wx.VERTICAL)
        merlesizer.Add(wx.StaticText(self, label=TEXT_MERLE), 0, wx.ALL, 5)
        merlesizer.Add(wx.CheckBox(self, label=TEXT_NO_MERLE), 0, wx.ALL, 5)
        merlesizer.Add(wx.CheckBox(self, label=TEXT_MERLE), 0, wx.ALL, 5)
        merlesizer.Add(wx.CheckBox(self, label=TEXT_DOUBLE_MERLE), 0, wx.ALL, 5)

        tickingsizer = wx.BoxSizer(wx.VERTICAL)
        tickingsizer.Add(wx.StaticText(self, label=TEXT_TICKING), 0, wx.ALL, 5)
        tickingsizer.Add(wx.CheckBox(self, label=TEXT_NO_TICKING), 0, wx.ALL, 5)
        tickingsizer.Add(wx.CheckBox(self, label=TEXT_MINOR_TICKING), 0, wx.ALL, 5)
        tickingsizer.Add(wx.CheckBox(self, label=TEXT_TICKING), 0, wx.ALL, 5)
        tickingsizer.Add(wx.CheckBox(self, label=TEXT_ROANING), 0, wx.ALL, 5)

        patternsizer = wx.BoxSizer(wx.VERTICAL)
        patternsizer.Add(wx.StaticText(self, label=TEXT_COATPATTERN), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_SOLID_EUMELANIN), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_SABLE), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_AGOUTI), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_TANPOINT), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_BRINDLE), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_MASK), 0, wx.ALL, 5)
        patternsizer.Add(wx.CheckBox(self, label=TEXT_GREYING), 0, wx.ALL, 5)

        coatsizer.AddMany([blackcolorsizer, redcolorsizer, spottingsizer, merlesizer, tickingsizer, patternsizer])
        goalsizer.Add(coatlabel, 0, wx.ALL, 10)
        goalsizer.Add(coatsizer, 5, wx.EXPAND)

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(goalsizer, 5, wx.EXPAND | wx.ALL, 15)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomsizer.AddStretchSpacer(3)
        addbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_ADD,
                                  colors=BUTTONCOLORS)
        cancelbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_CANCEL,
                                     colors=BUTTONCOLORS)
        bottomsizer.Add(addbutton, 1, wx.ALL, 10)
        bottomsizer.Add(cancelbutton, 1, wx.ALL, 10)
        cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.Cancel)
        addbutton.Bind(wx.EVT_LEFT_DOWN, self.AddGoal)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(topsizer, 3, wx.EXPAND)
        mainsizer.AddStretchSpacer(2)
        mainsizer.Add(bottomsizer, 1, wx.ALL, 10)
        self.SetSizer(mainsizer)
        self.Layout()

    def Cancel(self, e):
        if self.origin == "breeding":
            wx.PostEvent(self.GetParent(), ReturnToBreedingFromGoal())
        else:
            wx.PostEvent(self.GetParent(), NavigationEvent(destination="Goals"))

    def AddGoal(self, e):
        children = [x for x in self.GetChildren() if type(x) == wx.CheckBox]
        selected = [x.GetLabel() for x in children if x.GetValue()]
        if selected:
            wx.PostEvent(self.GetParent(), AddGoalEvent(data=selected, origin=self.origin))


class BreedingPanel(wx.Panel):
    def __init__(self, parent, damdata=None, siredata=None):
        super().__init__(parent)
        self.damdata = damdata
        self.siredata = siredata
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        self.sire = None
        self.dam = None
        breedingtypesizer = wx.BoxSizer(wx.VERTICAL)
        breedingtypelabel = wx.StaticText(self, label=TEXT_BREEDINGTYPE)
        breedingtypelabel.SetFont(FONT_BIG)
        breedingtypelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        radio1 = wx.RadioButton(self, label=TEXT_CONV)
        radio1.SetValue(True)
        self.breedingtype = "Conventional"
        radio1.Bind(wx.EVT_RADIOBUTTON, self.SetUpConventional)
        radio2 = wx.RadioButton(self, label=TEXT_PICKMATE)
        radio2.Bind(wx.EVT_RADIOBUTTON, self.SetUpPickMate)
        breedingtypesizer.Add(breedingtypelabel, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio1, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio2, 0, wx.ALL, 5)

        self.parentsizer = wx.BoxSizer(wx.VERTICAL)
        self.pickmateparentsizer = wx.BoxSizer(wx.VERTICAL)
        self.damsizer = wx.BoxSizer(wx.VERTICAL)
        self.siresizer = wx.BoxSizer(wx.VERTICAL)
        self.SetUpConventional(None)

        leftsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer.Add(breedingtypesizer, 1, wx.EXPAND | wx.ALL, 10)
        leftsizer.AddSpacer(30)
        leftsizer.Add(self.parentsizer, 2, wx.EXPAND | wx.ALL, 10)

        rightsizer = wx.BoxSizer(wx.VERTICAL)
        breedinggoalslabel = wx.StaticText(self, label=TEXT_GOALS)

        breedinggoalslabel.SetFont(FONT_BIG)
        self.goalctrl = GoalCtrl(self)
        buttonsizer = wx.GridSizer(2, 2, 10, 20)
        addgoalbutton = RoundedButton(self, TEXT_ADD, colors=BUTTONCOLORS)
        addgoalbutton.Bind(wx.EVT_LEFT_DOWN, self.AddGoal)
        cleargoalbutton = RoundedButton(self, TEXT_CLEAR, colors=BUTTONCOLORS)
        cleargoalbutton.Bind(wx.EVT_LEFT_DOWN, self.ClearGoals)
        loadgoalbutton = RoundedButton(self, TEXT_LOAD, colors=BUTTONCOLORS)
        loadgoalbutton.Bind(wx.EVT_LEFT_DOWN, self.LoadGoals)
        buttonsizer.Add(addgoalbutton, 1, wx.EXPAND)
        buttonsizer.Add(cleargoalbutton, 1, wx.EXPAND)
        buttonsizer.Add(loadgoalbutton, 1, wx.EXPAND)
        calculatebutton = RoundedButton(self, TEXT_CALCULATE, colors=BUTTONCOLORS)
        calculatebutton.Bind(wx.EVT_LEFT_DOWN, self.CalculateButtonClicked)
        backbutton = RoundedButton(self, TEXT_BACK, colors=BUTTONCOLORS)
        backbutton.Bind(wx.EVT_LEFT_DOWN, self.GoBack)
        rightsizer.Add(breedinggoalslabel, 0, wx.RIGHT, 5)
        rightsizer.Add(self.goalctrl, 2, wx.EXPAND | wx.RIGHT | wx.TOP, 15)
        rightsizer.Add(buttonsizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP, 15)
        rightsizer.AddSpacer(200)
        rightsizer.Add(calculatebutton, 0, wx.EXPAND | wx.RIGHT | wx.BOTTOM, 15)
        rightsizer.Add(backbutton, 0, wx.EXPAND | wx.RIGHT | wx.BOTTOM, 15)

        breedingtestsizer = wx.BoxSizer(wx.HORIZONTAL)
        breedingtestsizer.Add(leftsizer, 1, wx.EXPAND)
        breedingtestsizer.AddSpacer(50)
        breedingtestsizer.Add(rightsizer, 1, wx.EXPAND)
        self.SetSizer(breedingtestsizer)

        self.Bind(EVT_SELECT_DOG, self.SelectHandler)
        self.Bind(EVT_REQUEST_DOGS, self.passToMainWindow)
        self.Bind(EVT_OPEN_DOG_PAGE, self.GoToDogPage)
        self.Bind(EVT_PASS_DOGS, self.ReceiveData)
        self.Bind(EVT_PARENT_SELECTED, self.passToMainWindow)
        self.Bind(EVT_PASS_SELECTED_PARENT_DATA, self.SetParentData)
        self.Bind(EVT_DISPLAY_GOALS, self.FillGoalCtrl)

    def SetUpConventional(self, e):
        self.dam = self.sire = None
        self.breedingtype = "Conventional"
        self.parentsizer.Clear(delete_windows=True)
        self.pickmateparentsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetupParentSizer(self.damdata, self.damsizer, "Dam")
        self.SetupParentSizer(self.siredata, self.siresizer, "Sire")
        self.parentsizer.Add(self.damsizer)
        self.parentsizer.AddStretchSpacer(1)
        self.parentsizer.Add(self.siresizer)
        self.parentsizer.AddStretchSpacer(1)
        self.Layout()

    def SetupParentSizer(self, data, sizer, who):
        if data is not None:
            name, age, coat, dogid = data
        else:
            name = TEXT_NAMEBARE
            age, coat = "", ""
            dogid = -1
        if who == "Parent":
            parentlabel = wx.StaticText(self, label=TEXT_PARENT)
        elif who == "Dam":
            parentlabel = wx.StaticText(self, label=TEXT_DAM)
        else:
            parentlabel = wx.StaticText(self, label=TEXT_SIRE)
        sizer.Clear(delete_windows=True)
        parentlabel.SetFont(FONT_BIG)
        parentlabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        parentselectbutton = RoundedButton(self, TEXT_SELECT, (100, 25), 15, BUTTONCOLORS)
        parentselectbutton.type = who
        parentselectbutton.Bind(wx.EVT_LEFT_DOWN, self.parentselectbutton)
        parentselectsizer = wx.BoxSizer(wx.HORIZONTAL)
        parentselectsizer.Add(parentlabel, 2)
        parentselectsizer.Add(parentselectbutton, 3, wx.TOP, 7)
        parentnamelinkbutton = LinkButton(self, name)
        parentnamelinkbutton.num = dogid
        parentnamelinkbutton.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)
        parentagelabel = wx.StaticText(self, label=TEXT_AGE + age)
        parentcoatlabel = wx.StaticText(self, label=TEXT_COAT + coat)
        sizer.Add(parentselectsizer)
        sizer.Add(parentnamelinkbutton)
        sizer.Add(parentagelabel)
        sizer.Add(parentcoatlabel)
        self.Layout()

    def SetUpPickMate(self, e):
        self.dam = self.sire = None
        self.breedingtype = "PickMate"
        self.parentsizer.Clear(delete_windows=True)
        self.damsizer = wx.BoxSizer(wx.VERTICAL)
        self.siresizer = wx.BoxSizer(wx.VERTICAL)
        self.SetupParentSizer(None, self.pickmateparentsizer, "Parent")
        self.parentsizer.Add(self.pickmateparentsizer)
        self.Layout()

    def FillGoalCtrl(self, e):
        print("FILLING GOAL CTRL")
        data = e.data
        print("RECEIVED DATA", e.data)
        self.goalctrl.Fill(data)
        self.goalctrl.Layout()

    def ClearGoals(self, e):
        self.goalctrl.ClearGoals()

    def LoadGoals(self, e):
        wx.PostEvent(self.GetParent(), RequestAllGoalsEvent(type="displaybreeding"))

    def AddGoal(self, e):
        wx.PostEvent(self.GetParent(), OpenAddGoalPanel(origin="breeding"))

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), OpenMainMenu())

    def SetParentData(self, e):
        data = e.dog.name, str(e.dog.age), e.dog.coatdesc, e.dog.id
        if e.dog.sex == "m":
            self.sire = e.dog.id
            if self.breedingtype == "Conventional":
                self.SetupParentSizer(data, self.siresizer, "Sire")
            else:
                self.SetupParentSizer(data, self.pickmateparentsizer, "Parent")
        else:
            self.dam = e.dog.id
            if self.breedingtype == "Conventional":
                self.SetupParentSizer(data, self.damsizer, "Dam")
            else:
                self.SetupParentSizer(data, self.pickmateparentsizer, "Parent")
        self.Layout()

    def passToMainWindow(self, e):
        wx.PostEvent(self.GetParent(), e)

    def OpenDogPage(self, e):
        wx.PostEvent(self, OpenDogPageEvent(num=e.GetEventObject().num, status="unconfirmed"))

    def GoToDogPage(self, e):
        if e.num != -1:
            if e.status == "unconfirmed":
                dialog = wx.MessageDialog(self, TEXT_GOTODOGPAGEWARNING, style=wx.OK | wx.CANCEL)
                test = dialog.ShowModal()
                dialog.Destroy()
                if test == wx.ID_OK:
                    wx.PostEvent(self.GetParent(), e)
            else:
                self.passToMainWindow(e)

    def ReceiveData(self, e):
        target = [x for x in self.GetChildren() if type(x) == DogSelectDialog][0]
        wx.PostEvent(target, e)

    def parentselectbutton(self, e):
        evt = SelectDogEvent(who=e.GetEventObject().type)
        wx.PostEvent(self, evt)

    def SelectHandler(self, e):
        self.PopUpDogSelector(e.who)

    def PopUpDogSelector(self, dogtype):
        dialog = DogSelectDialog(parent=self, who=dogtype)
        dialog.Show()

    def CheckIfAllDataPresent(self):
        if self.breedingtype == "Conventional":
            print(self.sire, self.dam)
            return True if self.sire is not None and self.dam is not None else False
        if self.breedingtype == "PickMate":
            return True if (self.sire is not None or self.dam is not None) and self.goalctrl.selected else False

    def PrepareData(self):
        parents = self.sire, self.dam
        goals = self.goalctrl.selected
        return self.breedingtype, parents, goals

    def CalculateButtonClicked(self, e):
        # check if all necessary data has been input
        # if conventional, needs both parents
        # if pickmate, needs parent and at least one selected goal
        if self.CheckIfAllDataPresent():
            data = self.PrepareData()
            wx.PostEvent(self.GetParent(), BeginBreedingCalculation(data=data))
        else:
            dialog = wx.MessageDialog(self, message=TEXT_MISSING_DATA + TEXT_MISSING_DATA_BREEDING,
                                      caption=TEXT_MISSING_DATA_TITLE, style=wx.OK | wx.ICON_WARNING)
            dialog.ShowModal()
            dialog.Destroy()


class BreedingResultPanel(wx.Panel):
    def __init__(self, parent, breedingresult):
        super().__init__(parent)
        self.breedingresult = breedingresult
        self.breedingtype = self.breedingresult.type
        breedingresultsizer = wx.BoxSizer(wx.VERTICAL)
        bottombuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonbackcalc = RoundedButton(self, TEXT_BACK_TO_CALC, colors=BUTTONCOLORS)
        buttonbackcalc.Bind(wx.EVT_LEFT_DOWN, self.GoBackToBreedCalc)
        buttonbackbreedings = RoundedButton(self, TEXT_BACK_TO_MY_BREEDINGS, colors=BUTTONCOLORS)
        bottombuttonsizer.AddStretchSpacer(3)
        bottombuttonsizer.Add(buttonbackcalc, 1, wx.ALL, 15)
        bottombuttonsizer.Add(buttonbackbreedings, 1, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)
        self.Bind(EVT_OPEN_DOG_PAGE, self.PassToParent)

        if self.breedingtype == "Conventional":
            self.dam = self.breedingresult.parent1 if self.breedingresult.parent1.sex == "f" else self.breedingresult.parent2
            self.sire = self.breedingresult.parent1 if self.dam != self.breedingresult.parent1 else self.breedingresult.parent2
            title = TEXT_CONVRESULTS
            subtitleleft = TEXT_POSSIBLECOATS
            subtitleright = TEXT_IMPOSSIBLECOATS
            titleright = wx.BoxSizer(wx.HORIZONTAL)
            damname = LinkButton(self, self.dam.name)
            damname.num = self.dam.id
            damname.Bind(wx.EVT_LEFT_DOWN, self.GoToDogPage)
            xlabel = wx.StaticText(self, label="x")
            sirename = LinkButton(self, self.sire.name)
            sirename.num = self.sire.id
            sirename.Bind(wx.EVT_LEFT_DOWN, self.GoToDogPage)
            titleright.Add(damname, 0, wx.BOTTOM, 5)
            titleright.Add(xlabel, 0, wx.TOP, 15)
            titleright.Add(sirename, 0, wx.BOTTOM, 5)
            self.leftwidget = GoalCtrl(self, size=(300, 300))
            self.rightwidget = GoalCtrl(self, size=(300, 300))
            subtitlegoal = TEXT_GOALS
            self.goalwidget = GoalCtrl(self, size=(300, 300))


        else:  # pick best mate
            title = TEXT_PICKMATERESULTS
            subtitleleft = TEXT_GOALS
            subtitleright = TEXT_BESTMATE
            titleright = LinkButton(self, self.breedingresult.mainparent.name)
            titleright.Bind(wx.EVT_LEFT_DOWN, self.GoToDogPage)
            titleright.num=self.breedingresult.mainparent.id
            self.leftwidget = GoalCtrl(self)
            self.rightwidget = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 1)

        title = wx.StaticText(self, label=title)
        title.SetFont(FONT_BIG)
        subtitleleft = wx.StaticText(self, label=subtitleleft)
        subtitleright = wx.StaticText(self, label=subtitleright)
        subtitleleft.SetFont(FONT_BIG)
        subtitleright.SetFont(FONT_BIG)
        titlesizer = wx.BoxSizer(wx.HORIZONTAL)
        titlesizer.Add(title, 0, wx.ALL, 5)
        titlesizer.Add(titleright, 0, wx.ALL, 5)
        breedingresultsizer.Add(titlesizer, 0, wx.ALL, 15)
        contentsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer.Add(subtitleleft, 0, wx.ALL, 5)
        leftsizer.Add(self.leftwidget, 2, wx.EXPAND | wx.ALL, 5)
        rightsizer.Add(subtitleright, 0, wx.ALL, 5)
        rightsizer.Add(self.rightwidget, 2, wx.EXPAND | wx.ALL, 5)
        contentsizer.Add(leftsizer, 1, wx.EXPAND | wx.ALL, 10)
        contentsizer.Add(rightsizer, 1, wx.EXPAND | wx.ALL, 10)
        if self.breedingtype == "Conventional":
            subtitlegoal = wx.StaticText(self, label=subtitlegoal)
            subtitlegoal.SetFont(FONT_BIG)
            goalsizer = wx.BoxSizer(wx.VERTICAL)
            goalsizer.Add(subtitlegoal, 0, wx.ALL, 5)
            goalsizer.Add(self.goalwidget, 2, wx.EXPAND | wx.ALL, 5)
            contentsizer.Add(goalsizer, 1, wx.EXPAND | wx.ALL, 10)
        breedingresultsizer.Add(contentsizer, 1, wx.EXPAND)
        breedingresultsizer.AddStretchSpacer()
        breedingresultsizer.Add(bottombuttonsizer, 0, wx.EXPAND)
        self.PopulateWidgets()
        self.SetSizer(breedingresultsizer)

    def PassToParent(self, e):
        wx.PostEvent(self.GetParent(), e)

    def PopulateWidgets(self):
        if self.breedingtype == "Conventional":
            self.leftwidget.Fill(self.breedingresult.possiblePhensAsGoals, False)
            self.rightwidget.Fill(self.breedingresult.impossiblePhensAsGoals, False)
            print(self.breedingresult.goalslist, "GOALSLIST")
            self.goalwidget.Fill(self.breedingresult.goalslist, False, self.breedingresult.goalscores)

        else:
            print(self.breedingresult.bestmate)
            self.leftwidget.Fill(self.breedingresult.goalslist, False, self.breedingresult.bestmate[1])
            self.rightwidget.AddElement(self.breedingresult.bestmate[2].ToDesc(), self.breedingresult.bestmate[2].id)

    def GoBackToBreedings(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="AllBreedingResults"))

    def GoBackToBreedCalc(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="BreedingCalc"))

    def GoToDogPage(self, e):
        dialog = wx.MessageDialog(self, TEXT_GOTODOGPAGEWARNING, style=wx.OK | wx.CANCEL)
        test = dialog.ShowModal()
        evt = OpenDogPageEvent(num=e.GetEventObject().num, status="confirmed")
        if test == wx.ID_OK:
            wx.PostEvent(self.GetParent(), evt)
            self.Destroy()


class AllBreedingResultsPanel(BrowseDogsPanel):
    def __init__(self, parent):
        super().__init__(parent, Color(Hex_BACKGROUNDBOX).rgb, 8)
