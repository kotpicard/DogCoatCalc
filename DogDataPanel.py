from RoundedButton import RoundedButton
from GuiConstants import *


class DogDataPanel(wx.Panel):
    def __init__(self, parent_panel, font_color, button_colors):
        super().__init__(parent_panel)
        self.parent_panel = parent_panel
        self.SetBackgroundColour(self.parent_panel.GetBackgroundColour())
        self.font_color = font_color
        self.button_colors = button_colors
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Main vertical sizer for layout

        # Add UI components to the sizer
        self.create_components()
        self.SetSizer(self.sizer)

    def create_components(self):
        """
        Create all UI components and add them to the sizer.
        """
        # Name Label
        namelabel = wx.StaticText(self.parent_panel, label="Name")
        font = namelabel.GetFont()
        font.SetPointSize(20)  # Set font size to 20
        namelabel.SetFont(font)
        namelabel.SetForegroundColour(self.font_color)
        self.sizer.Add(namelabel, 0, wx.ALL, 5)

        # Other Labels
        self.sizer.Add(wx.StaticText(self.parent_panel, label="Sex:"), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label="Age:"), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label="Breed:"), 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticText(self.parent_panel, label="Coat:"), 0, wx.ALL, 5)

        # Buttons
        view_genotype_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label="View Genotype", colors=self.button_colors
        )
        breeding_tests_button = RoundedButton(
            self.parent_panel, size=(200, 50), corner_radius=10, label="Breeding Tests", colors=self.button_colors
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
