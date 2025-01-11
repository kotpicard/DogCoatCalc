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
        self.Bind(EVT_REQUEST_GENOTYPE_BY_ID, self.PassToDataLayer)
        self.Bind(EVT_EDIT_LOCUS, self.PassToLogicLayer)
        self.Bind(EVT_PASS_GENOTYPE, self.PassToLogicLayer)
        self.Bind(EVT_OPEN_EDIT_LOCUS, self.PassToLogicLayer)
        self.Bind(EVT_PASS_EDIT_LOCUS_DATA, self.PassToMainWindow)
        self.Bind(EVT_GENOTYPE_CHANGED, self.PassToMainWindow)
        self.Bind(EVT_SAVE, self.PassToDataLayer)
        self.Bind(EVT_REQUEST_DOGS, self.PassToDataLayer)
        self.Bind(EVT_PASS_DOGS, self.ProcessPassDogs)
        self.Bind(EVT_PARENT_SELECTED, self.PassToDataLayer)
        self.Bind(EVT_ADD_RELATIVE, self.RequestRelativeData)
        self.Bind(EVT_ADD_GOAL, self.PassToLogicLayer)
        self.Bind(EVT_PASS_GOAL, self.PassToDataLayer)
        self.Bind(EVT_NAV_DATA_PASS, self.PassToMainWindow)
        self.Bind(EVT_DELETE_GOAL, self.PassToDataLayer)
        self.Bind(EVT_REQUEST_ALL_GOALS, self.PassToDataLayer)
        self.Bind(EVT_DISPLAY_GOALS, self.PassToMainWindow)
        self.Bind(EVT_BEGIN_BREEDCALC, self.PassToDataLayer)
        self.Bind(EVT_DO_BREEDCALC, self.PassToLogicLayer)

        wx.PostEvent(self.DataLayer, LoadEvent())

    def RequestRelativeData(self, evt):
        dogid = evt.dogid
        relativeid = evt.relativeid
        relativetype = evt.type
        wx.PostEvent(self.DataLayer,
                     RequestDogs(filter=lambda x: x.id in [dogid, relativeid], data=relativetype, destination="top"))

    def ProcessAddRelative(self, evt):
        print(evt.data, evt.dogs)

    def ProcessPassDogs(self, evt):
        if evt.destination != "top":
            self.PassToMainWindow(evt)
        else:
            self.ProcessAddRelative(evt)

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
        if evt.type == "parentselected":
            wx.PostEvent(self.MainWindow, PassSelectedParentDataEvent(dog=evt.dog))

    def NavEventHandler(self, evt):
        if evt.destination == "MyDogs":
            wx.PostEvent(self.DataLayer, DisplayAllDogsEvent())
        if evt.destination == "BreedingCalc":
            wx.PostEvent(self.MainWindow, NavDataPass(destination="BreedingCalc", data=None))
        if evt.destination == "Goals":
            wx.PostEvent(self.DataLayer, RequestAllGoalsEvent(type="displayall"))

    def DisplayDogs(self, evt):
        event = NavDataPass(destination="MyDogs", data=evt.descs)
        wx.PostEvent(self.MainWindow, event)


a = DogApp()
a.MainLoop()
