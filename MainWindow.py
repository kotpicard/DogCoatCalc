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

    def CreateMenu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, TEXT_ABOUT, INFO_ABOUT)
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, TEXT_EXIT, INFO_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "File")
        self.SetMenuBar(menuBar)

    def NavigationHandler(self, e):
        wx.PostEvent(self.app, e)

    def NavigationDataHandler(self, e):
        self.MainSizer.Clear(delete_windows=True)
        print(e.destination)
        self.NAVDICT[e.destination](e.data)
        print("layout")
        self.Layout()
        self.Center()

    def CreateDefaultPanel(self):
        defaultpanel = DefaultPanel(self)
        self.MainSizer.Add(defaultpanel)

    def InitViewGenotype(self, e):
        wx.PostEvent(self.app, e)

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
        dialog.ShowModal()  # Show the dialog modally
        dialog.Destroy()

    def PassDogData(self, e):
        wx.PostEvent(self.app, e)

    def CreateGoalsPage(self, data):
        ...

    def GoToDogPage(self, evt):
        print("GO TO DOG PAGE", evt.num)
        dogid = evt.num
        wx.PostEvent(self.app, RequestDogByID(dogid=dogid))

    def CreateDogPage(self, evt):
        self.MainSizer.Clear(delete_windows=True)
        data = evt.dog.ToDesc()
        dogpanel = DogPanel(self, data)
        self.MainSizer.Add(dogpanel)
        self.Layout()
        self.Center()

    def CreateMyDogsPanel(self, data):
        print("HERE")
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
