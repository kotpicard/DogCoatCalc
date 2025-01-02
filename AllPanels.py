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
        wx.PostEvent(self.GetParent(), evt)

    def ClickedBreedingGoalsButton(self, e):
        evt = NavigationEvent(destination="Goals")
        wx.PostEvent(self.GetParent(), evt)


class MyDogsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.dogspanel = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 8)
        sizer = wx.BoxSizer(wx.VERTICAL)
        button = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_ADD,
                               colors=BUTTONCOLORS)
        button2 = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_REFRESH,
                               colors=BUTTONCOLORS)
        button2.Bind(wx.EVT_LEFT_DOWN, self.Reload)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.dogspanel, 5, wx.EXPAND | wx.ALL, 10)
        buttonsizer.Add(button, 0, wx.ALL, 10)
        buttonsizer.Add(button2, 0,wx.ALL, 10)
        buttonsizer.AddStretchSpacer(3)
        sizer.Add(buttonsizer, 0, wx.ALL, 0)
        self.SetSizer(sizer)
        button.Bind(wx.EVT_LEFT_DOWN, self.AddDog)

    def Fill(self, elems):
        for elem in elems:
            self.dogspanel.AddElement(elem)

    def AddDog(self,e):
        evt = AddDogEvent()
        wx.PostEvent(self.GetParent(), evt)

    def Reload(self,e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="MyDogs"))


class DogPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        dogdatasizer = wx.BoxSizer(wx.VERTICAL)
        namelabel = wx.StaticText(self, label=TEXT_NAMEBARE)
        namelabel.SetFont(FONT_BIG)
        namelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        dogdatasizer.Add(namelabel, 0, wx.ALL)
        sexlabel = wx.StaticText(self, label=TEXT_SEX)
        agelabel = wx.StaticText(self, label=TEXT_AGE)
        breedlabel = wx.StaticText(self, label=TEXT_BREED)
        coatlabel = wx.StaticText(self, label=TEXT_COAT)
        viewgenotypebutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_VIEWGENOTYPE,
                                           colors=BUTTONCOLORS)
        breedingtestsbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_BREEDINGTESTS,
                                            colors=BUTTONCOLORS)
        dogdatasizer.Add(sexlabel, 0, wx.ALL)
        dogdatasizer.Add(agelabel, 0, wx.ALL)
        dogdatasizer.Add(breedlabel, 0, wx.ALL)
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
        buttonnext = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_NEXTDOG,
                                   colors=BUTTONCOLORS)
        bottomsizer.Add(buttonprev, 0, wx.ALL, 10)
        bottomsizer.AddStretchSpacer()
        bottomsizer.Add(buttonnext, 0, wx.ALL, 10)

        dogsizer = wx.BoxSizer(wx.VERTICAL)
        dogsizer.Add(topsizer, 5, wx.EXPAND | wx.ALL, 10)
        dogsizer.AddSpacer(50)
        dogsizer.Add(bottomsizer, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(dogsizer)


class BreedingPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        self.Bind(EVT_SELECT_DOG, self.SelectHandler)
        breedingtypesizer = wx.BoxSizer(wx.VERTICAL)
        breedingtypelabel = wx.StaticText(self, label=TEXT_BREEDINGTYPE)
        breedingtypelabel.SetFont(FONT_BIG)
        breedingtypelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        radio1 = wx.RadioButton(self, label=TEXT_CONV)
        radio2 = wx.RadioButton(self, label=TEXT_PICKMATE)
        radio3 = wx.RadioButton(self, label=TEXT_PICKPAIR)
        radio4 = wx.RadioButton(self, label=TEXT_CREATE)
        breedingtypesizer.Add(breedingtypelabel, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio1, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio2, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio3, 0, wx.ALL, 5)
        breedingtypesizer.Add(radio4, 0, wx.ALL, 5)

        damsizer = wx.BoxSizer(wx.VERTICAL)
        damlabel = wx.StaticText(self, label=TEXT_DAM)
        damlabel.SetFont(FONT_BIG)
        damlabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        damselectbutton = RoundedButton(self, TEXT_SELECT, (100, 25), 15, BUTTONCOLORS)
        damselectbutton.Bind(wx.EVT_LEFT_DOWN, self.damselectbutton)
        damselectsizer = wx.BoxSizer(wx.HORIZONTAL)
        damselectsizer.Add(damlabel, 2)
        damselectsizer.Add(damselectbutton, 3, wx.TOP, 7)
        damnamelinkbutton = LinkButton(self, TEXT_NAMEBARE)
        damagelabel = wx.StaticText(self, label=TEXT_AGE)
        dambreedlabel = wx.StaticText(self, label=TEXT_BREED)
        damcoatlabel = wx.StaticText(self, label=TEXT_COAT)
        damsizer.Add(damselectsizer)
        damsizer.Add(damnamelinkbutton)
        damsizer.Add(damagelabel)
        damsizer.Add(dambreedlabel)
        damsizer.Add(damcoatlabel)

        siresizer = wx.BoxSizer(wx.VERTICAL)
        sirelabel = wx.StaticText(self, label=TEXT_SIRE)
        sirelabel.SetFont(FONT_BIG)
        sirelabel.SetForegroundColour(Color(Hex_FONTCOLORBG).rgb)
        sireselectbutton = RoundedButton(self, TEXT_SELECT, (100, 25), 15, BUTTONCOLORS)
        sireselectbutton.Bind(wx.EVT_LEFT_DOWN, self.sireselectbutton)
        sireselectsizer = wx.BoxSizer(wx.HORIZONTAL)
        sireselectsizer.Add(sirelabel, 2)
        sireselectsizer.Add(sireselectbutton, 3, wx.TOP, 7)
        sirenamelinkbutton = LinkButton(self, TEXT_NAMEBARE)
        sireagelabel = wx.StaticText(self, label=TEXT_AGE)
        sirebreedlabel = wx.StaticText(self, label=TEXT_BREED)
        sirecoatlabel = wx.StaticText(self, label=TEXT_COAT)
        siresizer.Add(sireselectsizer)
        siresizer.Add(sirenamelinkbutton)
        siresizer.Add(sireagelabel)
        siresizer.Add(sirebreedlabel)
        siresizer.Add(sirecoatlabel)

        parentsizer = wx.BoxSizer(wx.VERTICAL)
        parentsizer.Add(damsizer)
        parentsizer.Add(siresizer)

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
