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
        evt = NavigationEvent(destination="Goals")
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
        previd = dogid - 1
        nextid = dogid + 1
        namelabel.SetFont(FONT_BIG)
        namelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        dogdatasizer.Add(namelabel, 0, wx.ALL)
        agelabel = wx.StaticText(self, label=TEXT_AGE + values[2])
        sexlabel = wx.StaticText(self, label=TEXT_SEX + values[1])

        # breedlabel = wx.StaticText(self, label=TEXT_BREED)
        coatlabel = wx.StaticText(self, label=TEXT_COAT + values[3])
        viewgenotypebutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_VIEWGENOTYPE,
                                           colors=BUTTONCOLORS)
        viewgenotypebutton.Bind(wx.EVT_LEFT_DOWN, self.OpenGenotypeView)

        breedingtestsbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_BREEDINGTESTS,
                                            colors=BUTTONCOLORS)

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

    def GoBack(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="MyDogs"))

    def OpenDogPage(self, e):
        num = e.GetEventObject().num
        wx.PostEvent(self.GetParent(), OpenDogPageEvent(num=num))

    def OpenGenotypeView(self, e):
        wx.PostEvent(self.GetParent(), OpenGenotypeViewEvent(dogid=self.dogid))


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


class BreedingPanel(wx.Panel):
    def __init__(self, parent, damdata=None, siredata=None):
        super().__init__(parent)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        self.Bind(EVT_SELECT_DOG, self.SelectHandler)
        breedingtypesizer = wx.BoxSizer(wx.VERTICAL)
        breedingtypelabel = wx.StaticText(self, label=TEXT_BREEDINGTYPE)
        breedingtypelabel.SetFont(FONT_BIG)
        breedingtypelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        radio1 = wx.RadioButton(self, label=TEXT_CONV)
        radio2 = wx.RadioButton(self, label=TEXT_PICKMATE)
        breedingtypesizer.Add(breedingtypelabel, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio1, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio2, 0, wx.ALL, 5)

        self.damsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetupDamSizer(damdata)

        self.siresizer = wx.BoxSizer(wx.VERTICAL)
        self.SetupSireSizer(siredata)

        parentsizer = wx.BoxSizer(wx.VERTICAL)
        parentsizer.Add(self.damsizer)
        parentsizer.AddStretchSpacer(1)
        parentsizer.Add(self.siresizer)
        parentsizer.AddStretchSpacer(1)

        leftsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer.Add(breedingtypesizer, 1, wx.EXPAND | wx.ALL, 10)
        leftsizer.AddSpacer(30)
        leftsizer.Add(parentsizer, 2, wx.EXPAND | wx.ALL, 10)

        rightsizer = wx.BoxSizer(wx.VERTICAL)
        breedinggoalslabel = wx.StaticText(self, label=TEXT_GOALS)

        breedinggoalslabel.SetFont(FONT_BIG)
        goalctrl = GoalCtrl(self)
        buttonsizer = wx.GridSizer(2, 2, 10, 20)
        addgoalbutton = RoundedButton(self, TEXT_ADD, colors=BUTTONCOLORS)
        cleargoalbutton = RoundedButton(self, TEXT_CLEAR, colors=BUTTONCOLORS)
        loadgoalbutton = RoundedButton(self, TEXT_LOAD, colors=BUTTONCOLORS)
        savegoalbutton = RoundedButton(self, TEXT_SAVE, colors=BUTTONCOLORS)
        buttonsizer.Add(addgoalbutton, 1, wx.EXPAND)
        buttonsizer.Add(cleargoalbutton, 1, wx.EXPAND)
        buttonsizer.Add(loadgoalbutton, 1, wx.EXPAND)
        buttonsizer.Add(savegoalbutton, 1, wx.EXPAND)
        calculatebutton = RoundedButton(self, TEXT_CALCULATE, colors=BUTTONCOLORS)
        rightsizer.Add(breedinggoalslabel, 0, wx.RIGHT, 5)
        rightsizer.Add(goalctrl, 2, wx.EXPAND | wx.RIGHT | wx.TOP, 15)
        rightsizer.Add(buttonsizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP, 15)
        rightsizer.AddSpacer(200)
        rightsizer.Add(calculatebutton, 0, wx.EXPAND | wx.RIGHT | wx.BOTTOM, 15)

        breedingtestsizer = wx.BoxSizer(wx.HORIZONTAL)
        breedingtestsizer.Add(leftsizer, 1, wx.EXPAND)
        breedingtestsizer.AddSpacer(50)
        breedingtestsizer.Add(rightsizer, 1, wx.EXPAND)
        self.SetSizer(breedingtestsizer)

        self.Bind(EVT_REQUEST_DOGS, self.passToMainWindow)
        self.Bind(EVT_OPEN_DOG_PAGE, self.GoToDogPage)
        self.Bind(EVT_PASS_DOGS, self.ReceiveData)
        self.Bind(EVT_PARENT_SELECTED, self.passToMainWindow)
        self.Bind(EVT_PASS_SELECTED_PARENT_DATA, self.SetParentData)

    def SetParentData(self, e):
        data = e.dog.name, str(e.dog.age), e.dog.coatdesc, e.dog.id
        if e.dog.sex == "m":
            self.SetupSireSizer(data)
        else:
            self.SetupDamSizer(data)
        self.Layout()

    def passToMainWindow(self, e):
        wx.PostEvent(self.GetParent(), e)

    def SetupDamSizer(self, data=None):
        if data is not None:
            name, age, coat, dogid = data
        else:
            name = TEXT_NAMEBARE
            age, coat = "", ""
        self.damsizer.Clear(delete_windows=True)
        damlabel = wx.StaticText(self, label=TEXT_DAM)
        damlabel.SetFont(FONT_BIG)
        damlabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        damselectbutton = RoundedButton(self, TEXT_SELECT, (100, 25), 15, BUTTONCOLORS)
        damselectbutton.Bind(wx.EVT_LEFT_DOWN, self.damselectbutton)
        damselectsizer = wx.BoxSizer(wx.HORIZONTAL)
        damselectsizer.Add(damlabel, 2)
        damselectsizer.Add(damselectbutton, 3, wx.TOP, 7)
        damnamelinkbutton = LinkButton(self, name)
        damagelabel = wx.StaticText(self, label=TEXT_AGE + age)
        damcoatlabel = wx.StaticText(self, label=TEXT_COAT + coat)
        self.damsizer.Add(damselectsizer)
        self.damsizer.Add(damnamelinkbutton)
        self.damsizer.Add(damagelabel)
        self.damsizer.Add(damcoatlabel)

    def SetupSireSizer(self, data=None):
        if data is not None:
            name, age, coat, dogid = data
        else:
            name = TEXT_NAMEBARE
            age, coat = "", ""
        self.siresizer.Clear(delete_windows=True)
        sirelabel = wx.StaticText(self, label=TEXT_SIRE)
        sirelabel.SetFont(FONT_BIG)
        sirelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        sireselectbutton = RoundedButton(self, TEXT_SELECT, (100, 25), 15, BUTTONCOLORS)
        sireselectbutton.Bind(wx.EVT_LEFT_DOWN, self.sireselectbutton)
        sireselectsizer = wx.BoxSizer(wx.HORIZONTAL)
        sireselectsizer.Add(sirelabel, 2)
        sireselectsizer.Add(sireselectbutton, 3, wx.TOP, 7)
        sirenamelinkbutton = LinkButton(self, name)
        if data is not None:
            sirenamelinkbutton.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)
            sirenamelinkbutton.num = dogid
        sireagelabel = wx.StaticText(self, label=TEXT_AGE + age)
        sirecoatlabel = wx.StaticText(self, label=TEXT_COAT + coat)
        self.siresizer.Add(sireselectsizer)
        self.siresizer.Add(sirenamelinkbutton)
        self.siresizer.Add(sireagelabel)
        self.siresizer.Add(sirecoatlabel)

    def OpenDogPage(self, e):
        wx.PostEvent(self, OpenDogPageEvent(num=e.GetEventObject().num, status="unconfirmed"))

    def GoToDogPage(self, e):
        if e.status=="unconfirmed":
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

    def sireselectbutton(self, e):
        evt = SelectDogEvent(who="Sire")
        wx.PostEvent(self, evt)

    def damselectbutton(self, e):
        evt = SelectDogEvent(who="Dam")
        wx.PostEvent(self, evt)

    def SelectHandler(self, e):
        self.PopUpDogSelector(e.who)

    def PopUpDogSelector(self, dogtype):
        dialog = DogSelectDialog(parent=self, who=dogtype)
        dialog.Show()

    def GoToDogPage(self, e):
        dialog = wx.MessageDialog(self, TEXT_GOTODOGPAGEWARNING, style=wx.OK | wx.CANCEL)
        test = dialog.ShowModal()
        if test == wx.ID_OK:
            wx.PostEvent(self.GetParent(), e)


class BreedingResultPanel(wx.Panel):
    def __init__(self, parent, breedingtype):
        super().__init__(parent)
        breedingresultsizer = wx.BoxSizer(wx.VERTICAL)
        bottombuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsave = RoundedButton(self, TEXT_SAVE, colors=BUTTONCOLORS)
        buttonclose = RoundedButton(self, TEXT_CLOSE, colors=BUTTONCOLORS)
        bottombuttonsizer.AddStretchSpacer()
        bottombuttonsizer.Add(buttonsave, 0, wx.ALL, 15)
        bottombuttonsizer.Add(buttonclose, 0, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)

        if breedingtype == BREEDINGTYPES[0]:  # conventional
            title = TEXT_CONVRESULTS
            subtitleleft = TEXT_POSSIBLECOATS
            subtitleright = TEXT_IMPOSSIBLECOATS
            titleright = wx.BoxSizer(wx.HORIZONTAL)
            damname = LinkButton(self, TEXT_DAM)
            xlabel = wx.StaticText(self, label="x")
            sirename = LinkButton(self, TEXT_SIRE)
            titleright.Add(damname, 0, wx.BOTTOM, 5)
            titleright.Add(xlabel, 0, wx.TOP, 15)
            titleright.Add(sirename, 0, wx.BOTTOM, 5)
            leftwidget = GoalCtrl(self)
            rightwidget = GoalCtrl(self)

        elif breedingtype == BREEDINGTYPES[1]:  # pick best mate
            title = TEXT_PICKMATERESULTS
            subtitleleft = TEXT_GOALS
            subtitleright = TEXT_BESTMATE
            titleright = LinkButton(self, TEXT_NAMEBARE)
            leftwidget = GoalCtrl(self)
            rightwidget = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 1)

        elif breedingtype == BREEDINGTYPES[2]:  # pick best pair
            title = TEXT_PICKPAIRRESULTS
            subtitleleft = TEXT_GOALS
            subtitleright = TEXT_BESTPAIR
            titleright = wx.StaticText(self, label="")
            leftwidget = GoalCtrl(self)
            rightwidget = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 1)

        else:  # create best mate
            title = TEXT_CREATERESULTS
            subtitleleft = TEXT_GOALS
            subtitleright = TEXT_BESTMATE
            titleright = LinkButton(self, TEXT_NAMEBARE)
            leftwidget = GoalCtrl(self)
            rightwidget = wx.BoxSizer(wx.VERTICAL)
            buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
            buttonviewgenotype = RoundedButton(self, TEXT_VIEWGENOTYPE, colors=BUTTONCOLORS)
            buttonsavetomydogs = RoundedButton(self, TEXT_SAVETOMYDOGS, colors=BUTTONCOLORS)
            buttonsizer.Add(buttonviewgenotype, 1, wx.ALL, 15)
            buttonsizer.Add(buttonsavetomydogs, 1, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)
            matectrl = GoalCtrl(self)
            rightwidget.Add(matectrl, 2, wx.EXPAND)
            rightwidget.Add(buttonsizer, 1, wx.EXPAND)

        title = wx.StaticText(self, label=title)
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
        leftsizer.Add(leftwidget, 2, wx.EXPAND | wx.ALL, 5)
        rightsizer.Add(subtitleright, 0, wx.ALL, 5)
        rightsizer.Add(rightwidget, 2, wx.EXPAND | wx.ALL, 5)
        contentsizer.Add(leftsizer, 1, wx.EXPAND | wx.ALL, 10)
        contentsizer.Add(rightsizer, 1, wx.EXPAND | wx.ALL, 10)
        breedingresultsizer.Add(contentsizer, 2, wx.EXPAND)
        breedingresultsizer.AddStretchSpacer()
        breedingresultsizer.Add(bottombuttonsizer, 0, wx.EXPAND)
        self.SetSizer(breedingresultsizer)


class AllBreedingResultsPanel(BrowseDogsPanel):
    def __init__(self, parent):
        super().__init__(parent, Color(Hex_BACKGROUNDBOX).rgb, 8)
