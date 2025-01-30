from BrowseDogsPanel import BrowseDogsPanel
from GuiConstants import *
from RoundedButton import RoundedButton
from text_en import *
from CustomEvents import *


class DogSelectDialog(wx.Frame):
    def __init__(self, parent, who, data=None):
        super().__init__(parent, title=TEXT_SELECTDOG, size=(400, 500))
        if who == "Dam":
            wx.PostEvent(parent, RequestDogs(filter=lambda x: x.sex == "f", destination="selectdog", data=None))
            self.type = "parentselector"
        elif who == "Sire":
            wx.PostEvent(parent, RequestDogs(filter=lambda x: x.sex == "m", destination="selectdog", data=None))
            self.type = "parentselector"
        elif who == "Parent":
            wx.PostEvent(parent, RequestDogs(filter=lambda x: True, destination="selectdog",data=None))
            self.type = "parentselector"
        elif who == "Relative":
            wx.PostEvent(parent, RequestDogs(filter=lambda x: x.id != data, destination="addrelative", data=None))
            self.type = "relativeselector"

        self.who = who
        self.Bind(EVT_PASS_DOGS, self.ReceiveData)
        self.Bind(EVT_OPEN_DOG_PAGE, self.GoToDogPage)
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)

    def GoToDogPage(self, e):
        dialog = wx.MessageDialog(self, TEXT_GOTODOGPAGEWARNING, style=wx.OK | wx.CANCEL)
        test = dialog.ShowModal()
        evt = OpenDogPageEvent(num=e.num, status="confirmed")
        if test == wx.ID_OK:
            wx.PostEvent(self.GetParent(), evt)
            self.Destroy()

    def ReceiveData(self, e):
        data = e.dogs
        self.ContinueSetup(data)

    def ContinueSetup(self, data):
        title = wx.StaticText(self, label=TEXT_SELECT + " " + self.who)
        title.SetFont(FONT_BIG)
        self.panel = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 3)
        for elem in data:
            print(elem)
            self.panel.AddSelectableElement(elem[0], elem[1])
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonselect = RoundedButton(self, TEXT_SELECT, colors=BUTTONCOLORS)
        buttoncancel = RoundedButton(self, TEXT_CANCEL, colors=BUTTONCOLORS)
        buttonsizer.AddStretchSpacer()
        buttonsizer.Add(buttonselect, 1, wx.ALL, 15)
        buttonsizer.Add(buttoncancel, 1, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)
        buttoncancel.Bind(wx.EVT_LEFT_DOWN, self.Cancel)
        buttonselect.Bind(wx.EVT_LEFT_DOWN, self.Selected)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALL, 10)
        sizer.Add(self.panel, 2, wx.EXPAND | wx.ALL, 10)
        sizer.Add(buttonsizer, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.Layout()
        self.Center()

    def Selected(self, e):
        if self.type == "parentselector":
            wx.PostEvent(self.GetParent(), ParentSelectedEvent(dogid=self.panel.selected[0], type="parentselected"))
        if self.type == "relativeselector":
            wx.PostEvent(self.GetParent(), PotentialRelativeSelectedEvent(dogid=self.panel.selected[0]))
        self.Destroy()

    def Cancel(self, e):
        self.Destroy()
