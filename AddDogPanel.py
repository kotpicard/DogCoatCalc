from CustomEvents import *
from GuiConstants import *
from RoundedButton import RoundedButton
from text_en import *


class AddDogPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        leftsizer = wx.BoxSizer(wx.VERTICAL)
        namelabel = wx.StaticText(self, label=TEXT_NAMEBARE)
        nameinput = wx.TextCtrl(self)
        agelabel = wx.StaticText(self, label=TEXT_AGEBARE)
        ageinput = wx.SpinCtrl(self)
        sexlabel = wx.StaticText(self, label=TEXT_SEXBARE)
        maleradio = wx.RadioButton(self, label=TEXT_MALE)
        femaleradio = wx.RadioButton(self, label=TEXT_FEMALE)
        leftsizer.Add(namelabel, 0, wx.ALL, 10)
        leftsizer.Add(nameinput, 0, wx.ALL, 10)
        leftsizer.Add(agelabel, 0, wx.ALL, 10)
        leftsizer.Add(ageinput, 0, wx.ALL, 10)
        leftsizer.Add(sexlabel, 0, wx.ALL, 10)
        leftsizer.Add(maleradio, 0, wx.ALL, 10)
        leftsizer.Add(femaleradio, 0, wx.ALL, 10)

        rightsizer = wx.BoxSizer(wx.VERTICAL)
        coatlabel = wx.StaticText(self, label=TEXT_COATBARE)
        coatsizer = wx.FlexGridSizer(2, 3, 20, 20)


        blackcolorsizer = wx.BoxSizer(wx.VERTICAL)
        blackcolorsizer.Add(wx.RadioButton(self, label=TEXT_BLACK, style=wx.RB_GROUP))
        blackcolorsizer.Add(wx.RadioButton(self, label=TEXT_LIVER))
        blackcolorsizer.Add(wx.RadioButton(self, label=TEXT_BLUE))
        blackcolorsizer.Add(wx.RadioButton(self, label=TEXT_ISABELLA))
        blackcolorsizer.Add(wx.RadioButton(self, label=TEXT_IDONTKNOW))
        redcolorsizer = wx.BoxSizer(wx.VERTICAL)
        redcolorsizer.Add(wx.RadioButton(self, label=TEXT_RED, style=wx.RB_GROUP))
        redcolorsizer.Add(wx.RadioButton(self, label=TEXT_DILUTE_RED))
        redcolorsizer.Add(wx.RadioButton(self, label=TEXT_IDONTKNOW))
        spottingsizer = wx.BoxSizer(wx.VERTICAL)
        spottingsizer.Add(wx.RadioButton(self, label=TEXT_NO_WHITE, style=wx.RB_GROUP))
        spottingsizer.Add(wx.RadioButton(self, label=TEXT_MINOR_WHITE))
        spottingsizer.Add(wx.RadioButton(self, label=TEXT_PIEBALD))
        spottingsizer.Add(wx.RadioButton(self, label=TEXT_IRISH_WHITE))
        spottingsizer.Add(wx.RadioButton(self, label=TEXT_IDONTKNOW))
        merlesizer = wx.BoxSizer(wx.VERTICAL)
        merlesizer.Add(wx.RadioButton(self, label=TEXT_NO_MERLE, style=wx.RB_GROUP))
        merlesizer.Add(wx.RadioButton(self, label=TEXT_MERLE))
        merlesizer.Add(wx.RadioButton(self, label=TEXT_DOUBLE_MERLE))
        merlesizer.Add(wx.RadioButton(self, label=TEXT_IDONTKNOW))
        tickingsizer = wx.BoxSizer(wx.VERTICAL)
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_NO_TICKING, style=wx.RB_GROUP))
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_MINOR_TICKING))
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_TICKING))
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_ROANING))
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_ROANING_AND_TICKING))
        tickingsizer.Add(wx.RadioButton(self, label=TEXT_IDONTKNOW))
        patternchoices = [
            TEXT_SOLID_EUMELANIN, TEXT_SABLE, TEXT_AGOUTI, TEXT_TANPOINT,
            TEXT_BRINDLE, TEXT_MASK, TEXT_GREYING, TEXT_IDONTKNOW
        ]
        patternsizer = wx.BoxSizer(wx.VERTICAL)
        for pattern in patternchoices:
            checkbox = wx.CheckBox(self, label=pattern)
            patternsizer.Add(checkbox, 0, wx.ALL, 0)
        coatsizer.AddMany([blackcolorsizer, redcolorsizer, spottingsizer, merlesizer, tickingsizer, patternsizer])
        rightsizer.Add(coatlabel, 0, wx.ALL, 10)
        rightsizer.Add(coatsizer, 5, wx.EXPAND)

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(leftsizer, 0, wx.ALL, 5)
        topsizer.AddStretchSpacer(1)
        topsizer.Add(rightsizer, 4, wx.EXPAND)
        bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomsizer.AddStretchSpacer(3)
        addbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_ADD,
                                  colors=BUTTONCOLORS)
        addbutton.Bind(wx.EVT_LEFT_DOWN, self.AddDog)
        cancelbutton = RoundedButton(self, size=(200, 50), corner_radius=10, label=TEXT_CANCEL,
                                     colors=BUTTONCOLORS)
        cancelbutton.Bind(wx.EVT_LEFT_DOWN, self.Cancel)
        bottomsizer.Add(addbutton, 1, wx.ALL, 10)
        bottomsizer.Add(cancelbutton, 1, wx.ALL, 10)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(topsizer, 3, wx.EXPAND)
        mainsizer.AddStretchSpacer(2)
        mainsizer.Add(bottomsizer, 1, wx.ALL, 10)
        self.SetSizer(mainsizer)

    def AddDog(self, e):
        children = [x for x in self.GetChildren() if type(x) not in [wx.StaticText, RoundedButton]]
        name = children[0].GetValue()
        age = children[1].GetValue()
        other = [x.GetLabel() for x in children[2:] if x.GetValue()]
        sex = other.pop(0)
        evt = PassDogDataEvent(name=name, age=age, sex=sex, coat=other, type="add", maxid=None)
        wx.PostEvent(self.GetParent(), evt)

    def Cancel(self, e):
        wx.PostEvent(self.GetParent(), NavigationEvent(destination="MyDogs"))



