import wx

from MainWindow import MainWindow
from DataLayer import DataLayer
from LogicLayer import LogicLayer

from CustomEvents import *


class DogApp(wx.App):
    def __init__(self):
        super().__init__()
        self.MainWindow = MainWindow(None, "Dog Coat Calculator", self)
        self.DataLayer = DataLayer(self)
        self.LogicLayer = LogicLayer(self)
        # evt = LoadEvent()
        # wx.PostEvent(self.DataLayer, evt)
        self.Bind(EVT_LOAD_DOG_FROM_DATA, self.PassToLogicLayer)
        self.Bind(EVT_PASS_DOG, self.PassToDataLayer)
        self.Bind(EVT_PASS_DOG_DATA, self.PassDogData)
        self.Bind(EVT_NAVIGATION, self.NavEventHandler)
        self.Bind(EVT_DISPLAY_ALL_DOGS, self.DisplayDogs)
        self.Bind(EVT_REQUEST_DOG_BY_ID, self.PassToDataLayer)
        self.Bind(EVT_INCORRECT_GENOTYPE, self.PassToMainWindow)
        self.Bind(EVT_VIEW_GENOTYPE, self.RequestGenotypeData)
        self.Bind(EVT_VIEWGEN_DATAPASS, self.PassToLogicLayer)
        self.Bind(EVT_FORMATTEDGEN_DATAPASS, self.PassToMainWindow)
        self.Bind(EVT_EDIT_LOCUS, self.PassToLogicLayer)
        self.Bind(EVT_PASS_GENOTYPE, self.PassToLogicLayer)
        self.Bind(EVT_OPEN_EDIT_LOCUS, self.PassToLogicLayer)
        self.Bind(EVT_PASS_EDIT_LOCUS_DATA, self.PassToMainWindow)

    def RequestGenotypeData(self, evt):
        dogid = evt.dogid
        wx.PostEvent(self.DataLayer, RequestGenotypeByID(dogid=dogid, type="viewgenotype"))

    def PassToMainWindow(self, evt):
        wx.PostEvent(self.MainWindow, evt)

    def PassToDataLayer(self, evt):
        wx.PostEvent(self.DataLayer, evt)

    def PassToLogicLayer(self, evt):
        wx.PostEvent(self.LogicLayer, evt)

    def PassDogData(self, evt):
        if evt.type == "byid":
            wx.PostEvent(self.MainWindow, PassDataForDogPageEvent(dog=evt.dog))
        if evt.type == "add":
            wx.PostEvent(self.LogicLayer, evt)
            wx.PostEvent(self, NavigationEvent(destination="MyDogs"))

    def NavEventHandler(self, evt):
        if evt.destination == "MyDogs":
            wx.PostEvent(self.DataLayer, DisplayAllDogsEvent())

    def DisplayDogs(self, evt):
        event = NavDataPass(destination="MyDogs", data=evt.descs)
        wx.PostEvent(self.MainWindow, event)


a = DogApp()
a.MainLoop()
