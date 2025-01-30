from RoundedButton import RoundedButton
from GuiConstants import *
from text_en import *


class DogDataPanel(wx.Panel):
    def __init__(self, parent_panel, values):
        super().__init__(parent_panel)
        self.parent_panel = parent_panel
        self.SetBackgroundColour(self.parent_panel.GetBackgroundColour())
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.create_components(values)
        self.SetSizer(self.sizer)

    def create_components(self, values):
        namelabel = wx.StaticText(self.parent_panel, label=values[0])
        namelabel.SetFont(FONT_BIG)
        self.sizer.Add(namelabel, 0, wx.ALL, 5)

        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_SEX+values[1]), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_AGE+values[2]), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_COAT+values[3]), 0, wx.ALL, 5)

        view_genotype_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label=TEXT_VIEWGENOTYPE, colors=BUTTONCOLORS
        )
        breeding_tests_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label=TEXT_BREEDINGTESTS, colors=BUTTONCOLORS
        )

        self.sizer.Add(view_genotype_button, 0, wx.ALL, 5)
        self.sizer.Add(breeding_tests_button, 0, wx.ALL, 5)

