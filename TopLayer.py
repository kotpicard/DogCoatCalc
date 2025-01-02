import wx

from gui import MainWindow
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
        self.Bind(EVT_LOAD_DOG_FROM_DATA, self.LoadDogFromDataHandler)
        self.Bind(EVT_PASS_DOG, self.PassDogToDataLayer)
        self.Bind(EVT_PASS_DOG_DATA, self.PassDogData)
        self.Bind(EVT_NAVIGATION, self.NavEventHandler)
        self.Bind(EVT_DISPLAY_ALL_DOGS, self.DisplayDogs)

    def LoadDogFromDataHandler(self, evt):
        wx.PostEvent(self.LogicLayer, evt)

    def PassDogToDataLayer(self, evt):
        wx.PostEvent(self.DataLayer, evt)

    def PassDogData(self, evt):
        wx.PostEvent(self.LogicLayer, evt)
        if evt.type=="add":
            wx.PostEvent(self, NavigationEvent(destination="MyDogs"))

    def NavEventHandler(self, evt):
        if evt.destination == "MyDogs":
            wx.PostEvent(self.DataLayer, DisplayAllDogsEvent())

    def DisplayDogs(self, evt):
        event = NavDataPass(destination="MyDogs", data=evt.descs)
        wx.PostEvent(self.MainWindow, event)


a = DogApp()
a.MainLoop()
