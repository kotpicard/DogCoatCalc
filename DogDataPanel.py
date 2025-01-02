from RoundedButton import RoundedButton
from GuiConstants import *
from text_en import *


class DogDataPanel(wx.Panel):
    def __init__(self, parent_panel, values):
        super().__init__(parent_panel)
        self.parent_panel = parent_panel
        self.SetBackgroundColour(self.parent_panel.GetBackgroundColour())
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Main vertical sizer for layout

        # Add UI components to the sizer
        self.create_components(values)
        self.SetSizer(self.sizer)

    def create_components(self, values):
        # Name Label
        namelabel = wx.StaticText(self.parent_panel, label=values[0])
        namelabel.SetFont(FONT_BIG)
        self.sizer.Add(namelabel, 0, wx.ALL, 5)

        # Other Labels
        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_SEX+values[1]), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_AGE+values[2]), 0, wx.ALL, 5)
        # self.sizer.Add(wx.StaticText(self.parent_panel, label="Breed:"), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label=TEXT_COAT+values[3]), 0, wx.ALL, 5)

        # Buttons
        view_genotype_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label=TEXT_VIEWGENOTYPE, colors=BUTTONCOLORS
        )
        breeding_tests_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label=TEXT_BREEDINGTESTS, colors=BUTTONCOLORS
        )

        self.sizer.Add(view_genotype_button, 0, wx.ALL, 5)
        self.sizer.Add(breeding_tests_button, 0, wx.ALL, 5)


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Scrollable Panel Example")

        # Create the main panel
        panel = wx.Panel(self)

        # Add the scrollable panel
        scrollable_panel = DogDataPanel(self, Color(Hex_FONTCOLORBG).rgb, BUTTONCOLORS)

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
