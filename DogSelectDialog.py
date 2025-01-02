from BrowseDogsPanel import BrowseDogsPanel
from GuiConstants import *
from RoundedButton import RoundedButton
from text_en import *

class DogSelectDialog(wx.Frame):
    def __init__(self, parent, who):
        super().__init__(parent, title=TEXT_SELECTDOG, size=(400, 500))
        self.SetBackgroundColour(Color(Hex_BACKGROUND).rgb)
        # Add a panel and some content
        title = wx.StaticText(self, label=TEXT_SELECT+" " + who)
        title.SetFont(FONT_BIG)
        panel = BrowseDogsPanel(self, Color(Hex_BACKGROUNDBOX).rgb, 3)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonselect = RoundedButton(self, TEXT_SELECT, colors=BUTTONCOLORS)
        buttoncancel = RoundedButton(self, TEXT_CANCEL, colors=BUTTONCOLORS)
        buttonsizer.AddStretchSpacer()
        buttonsizer.Add(buttonselect, 1, wx.ALL, 15)
        buttonsizer.Add(buttoncancel, 1, wx.BOTTOM | wx.TOP | wx.RIGHT, 15)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALL, 10)
        sizer.Add(panel, 2, wx.EXPAND | wx.ALL, 10)
        sizer.Add(buttonsizer, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        self.Center()

#
# class MainWindow(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title="Main Window", size=(400, 300))
#
#         # Main panel
#         panel = wx.Panel(self)
#
#         # Add a button
#         button = wx.Button(panel, label="Open New Window", pos=(100, 100))
#         button.Bind(wx.EVT_BUTTON, self.on_open_new_window)
#
#         # Frame settings
#         self.Center()
#
#     def on_open_new_window(self, event):
#         new_window = DogSelectDialog(self, "sire")  # Create a new instance of the NewWindow class
#         new_window.Show()  # Show the new window
#
#
# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MainWindow()
#         frame.Show()
#         return True
#
#
# if __name__ == "__main__":
#     app = MyApp()
#     app.MainLoop()
