from LinkButton import LinkButton
from GuiConstants import *


class LinkBoxCtrl(wx.Panel):
    def __init__(self, parent, size=(600, 150)):
        super().__init__(parent=parent, size=size)
        self.SetBackgroundColour(Color(Hex_BACKGROUNDBOX).rgb)

        self.sizer = wx.FlexGridSizer(0, 5, 0, 0)
        self.SetSizer(self.sizer)

    def AddElement(self, value):
        button = LinkButton(self, value)
        self.sizer.Add(button, 0, wx.EXPAND)
        self.sizer.Layout()
        self.Layout()
