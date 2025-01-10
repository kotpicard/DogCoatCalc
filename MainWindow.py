from AllPanels import *


class MainWindow(wx.Frame):
    def __init__(self, parent, title, app):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 800))
        self.CreateStatusBar()
        self.CreateMenu()
        self.app = app
        self.MainSizer = wx.BoxSizer()
        # self.CreateDefaultPanel()
        # self.CreateBreedingTestPanel()
        # self.CreateDogPage()
        # self.CreateMyDogsPanel()
        self.CreateDefaultPanel()
        self.Center()
        self.Show()
        self.Bind(EVT_NAVIGATION, self.NavigationHandler)
        self.NAVDICT = {
            "MyDogs": self.CreateMyDogsPanel,
            "BreedingCalc": self.CreateBreedingTestPanel,
            "AllBreedingResults": self.CreateBreedingResultsPanel,
            "Goals": self.CreateGoalsPage
        }
        self.Bind(EVT_ADD_DOG, self.AddDogHandler)
        self.Bind(EVT_PASS_DOG_DATA, self.PassDogData)
        self.Bind(EVT_NAV_DATA_PASS, self.NavigationDataHandler)
        self.Bind(EVT_OPEN_DOG_PAGE, self.GoToDogPage)
        self.Bind(EVT_PASS_DATA_DOG_PAGE, self.CreateDogPage)
        self.Bind(EVT_INCORRECT_GENOTYPE, self.IncorrectGenotypeAlert)
        self.Bind(EVT_VIEW_GENOTYPE, self.InitViewGenotype)
        self.Bind(EVT_FORMATTEDGEN_DATAPASS, self.OpenGenotypeView)
        self.Bind(EVT_EDIT_LOCUS, self.PassToTopLayer)
        self.Bind(EVT_OPEN_EDIT_LOCUS, self.PassToTopLayer)
        self.Bind(EVT_PASS_EDIT_LOCUS_DATA, self.OpenEditLocus)
        self.Bind(EVT_GENOTYPE_CHANGED, self.GenotypeChangedHandler)
        self.Bind(EVT_MAIN_MENU, self.OpenDefaultPanel)
        self.Bind(EVT_REQUEST_DOGS, self.PassToTopLayer)
        self.Bind(EVT_PASS_DOGS, self.ProcessPassDogs)
        self.Bind(EVT_PARENT_SELECTED, self.PassToTopLayer)
        self.Bind(EVT_PASS_SELECTED_PARENT_DATA, self.PassToBreedingPanel)
        self.Bind(EVT_ADD_RELATIVE, self.PassToTopLayer)
        self.Bind(EVT_OPEN_ADD_GOAL, self.OpenAddGoal)
        self.Bind(EVT_ADD_GOAL, self.PassToTopLayer)
        self.Bind(EVT_DELETE_GOAL, self.PassToTopLayer)
        self.Bind(EVT_REQUEST_ALL_GOALS, self.PassToTopLayer)
        self.Bind(EVT_DISPLAY_GOALS, self.DisplayGoals)

    def DisplayGoals(self, e):
        if e.destination == "breeding":
            self.PassToBreedingPanel(e)


    def OpenAddGoal(self, e):
        self.MainSizer.Clear(delete_windows=True)
        addgoalpanel = AddGoalPanel(self, e.origin)
        self.MainSizer.Add(addgoalpanel)
        self.Layout()
        self.Center()

    def PassToBreedingPanel(self, e):
        target = [x for x in self.GetChildren() if type(x)==BreedingPanel][0]
        wx.PostEvent(target, e)

    def ProcessPassDogs(self, e):
        if e.destination == "selectdog":
            for child in [x for x in self.GetChildren() if type(x) == BreedingPanel]:
                wx.PostEvent(child, e)
        if e.destination == "addrelative":
            for child in [x for x in self.GetChildren() if type(x) == DogPanel]:
                wx.PostEvent(child, e)

    def GenotypeChangedHandler(self, e):
        wx.PostEvent(self.app, SaveEvent())
        self.InitViewGenotype(e)

    def PassToTopLayer(self, e):
        wx.PostEvent(self.app, e)

    def CreateMenu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, TEXT_ABOUT, INFO_ABOUT)
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, TEXT_EXIT, INFO_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")
        self.SetMenuBar(menuBar)

    def NavigationHandler(self, e):
        print(e, e.destination)
        wx.PostEvent(self.app, e)

    def NavigationDataHandler(self, e):
        self.MainSizer.Clear(delete_windows=True)
        print(e.destination)
        self.NAVDICT[e.destination](e.data)
        print("layout")
        self.Layout()
        self.Center()

    def OpenDefaultPanel(self, e):
        self.MainSizer.Clear(delete_windows=True)
        self.CreateDefaultPanel()
        self.Layout()
        self.Center()

    def CreateDefaultPanel(self):
        defaultpanel = DefaultPanel(self)
        self.MainSizer.Add(defaultpanel)

    def InitViewGenotype(self, e):
        wx.PostEvent(self.app, OpenGenotypeViewEvent(dogid=e.dogid))

    def OpenEditLocus(self, e):
        self.MainSizer.Clear(delete_windows=True)
        editlocuspanel = AllelePanel(self, number=e.number, dogid=e.dogid, options=e.options)
        self.MainSizer.Add(editlocuspanel)
        self.Layout()
        self.Center()

    def OpenGenotypeView(self, e):
        self.MainSizer.Clear(delete_windows=True)
        genotypepanel = GenotypePanel(self, e.data)
        self.MainSizer.Add(genotypepanel)
        self.Layout()
        self.Center()

    def AddDogHandler(self, e):
        self.MainSizer.Clear(delete_windows=True)
        test = AddDogPanel(self)
        self.MainSizer.Add(test)
        self.Layout()
        self.Center()

    def IncorrectGenotypeAlert(self, e):
        dialog = wx.MessageDialog(self, TEXT_INCORRECT_GENOTYPE, TEXT_WARNING, wx.OK | wx.ICON_WARNING)
        dialog.ShowModal()
        dialog.Destroy()
        self.InitViewGenotype(e)

    def PassDogData(self, e):
        wx.PostEvent(self.app, e)

    def CreateGoalsPage(self, data):
        print("HERE", data)
        goalspanel = GoalsPanel(self)
        goalspanel.Fill(data)
        self.MainSizer.Add(goalspanel)

    def GoToDogPage(self, evt):
        print("GO TO DOG PAGE", evt.num)
        dogid = evt.num
        wx.PostEvent(self.app, RequestDogByID(dogid=dogid, type="byid"))

    def CreateDogPage(self, evt):
        self.MainSizer.Clear(delete_windows=True)
        data = evt.dog.ToDesc()
        dogpanel = DogPanel(self, data)
        self.MainSizer.Add(dogpanel)
        self.Layout()
        self.Center()

    def CreateMyDogsPanel(self, data):
        mydogspanel = MyDogsPanel(self)
        mydogspanel.Fill(data)
        self.MainSizer.Add(mydogspanel)

    def CreateBreedingTestPanel(self, data):
        breedingpanel = BreedingPanel(self)
        self.MainSizer.Add(breedingpanel)

    def CreateBreedingResultsPanel(self, data):
        allbreedingresultspanel = AllBreedingResultsPanel(self)
        self.MainSizer.Add(allbreedingresultspanel)

    def CreateBreedingResult(self, data):
        breedingresultpanel = BreedingResultPanel(self, data["breedingtype"])
        self.MainSizer.Add(breedingresultpanel)
