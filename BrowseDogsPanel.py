import wx
from LinkButton import LinkButton
from text_en import *
from CustomEvents import *
from GuiConstants import Hex_BACKGROUNDBOX, Color


class BrowseDogsPanel(wx.ScrolledWindow):
    def __init__(self, parent, background, cols):
        super().__init__(parent)
        self.selected = []

        self.sizer = wx.FlexGridSizer(0, cols, 10, 10)
        self.SetBackgroundColour(background)

        self.SetSizer(self.sizer)

        self.SetScrollRate(20, 20)
        self.EnableScrolling(True, True)
        self.Layout()
        self.FitInside()

    def AddLinkOnly(self, value):
        button = LinkButton(self, label=value)
        self.sizer.Add(button)

    def AddElement(self, values, i=None):
        elementsizer = wx.BoxSizer(wx.VERTICAL)
        button = LinkButton(self, label=values[0])
        button.num = i
        button.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)
        sexlabel = wx.StaticText(self, label=TEXT_SEX + values[1])
        agelabel = wx.StaticText(self, label=TEXT_AGE + values[2])
        coatlabel = wx.StaticText(self, label=TEXT_COAT + values[3])

        elementsizer.Add(button, 0, wx.ALIGN_CENTER)
        elementsizer.Add(sexlabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        elementsizer.Add(agelabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        # elementsizer.Add(breedlabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        elementsizer.Add(coatlabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        self.sizer.Add(elementsizer)
        self.sizer.Layout()

    def AddSelectableElement(self, values, i=None):
        elementsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        radio = wx.RadioButton(self)
        radio.num=i
        radio.Bind(wx.EVT_RADIOBUTTON, self.selectedstatusupdate)
        topsizer.Add(radio, wx.ALL, 5)
        button = LinkButton(self, label=values[0])
        button.num = i
        button.Bind(wx.EVT_LEFT_DOWN, self.OpenDogPage)
        topsizer.Add(button)
        sexlabel = wx.StaticText(self, label=TEXT_SEX + values[1])
        agelabel = wx.StaticText(self, label=TEXT_AGE + values[2])
        coatlabel = wx.StaticText(self, label=TEXT_COAT + values[3])

        elementsizer.Add(topsizer, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        elementsizer.Add(sexlabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        elementsizer.Add(agelabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)
        elementsizer.Add(coatlabel, 0, wx.ALIGN_CENTER | wx.LEFT, 15)

        self.sizer.Add(elementsizer)
        self.sizer.Layout()

    def selectedstatusupdate(self, e):
        num = e.GetEventObject().num
        if num in self.selected:
            self.selected.remove(num)
        else:
            self.selected.append(num)

    def OpenDogPage(self, e):
        print("open dog page", e.GetEventObject().num)
        num = e.GetEventObject().num
        if num is not None:
            wx.PostEvent(self.GetParent(), OpenDogPageEvent(num=num))


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Scrollable Panel Example")

        # Create the main panel
        panel = wx.Panel(self)

        # Add the scrollable panel
        scrollable_panel = BrowseDogsPanel(panel, Color(Hex_BACKGROUNDBOX).rgb, 2)
        scrollable_panel.AddElement(["NEW", "NEW", "NEW", "NEW", "NEW"])

        # Set up a vertical box sizer for the main frame
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(scrollable_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Set the sizer for the panel
        panel.SetSizerAndFit(sizer)

        # Set the frame size and center it
        self.SetSize((400, 300))
        self.Center()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
