from RoundedButton import RoundedButton
from GuiConstants import *
import wx


class GoalCtrl(wx.ScrolledWindow):
    def __init__(self, parent, size=(600, 150)):
        super().__init__(parent=parent, size=size)

        # Set up scrolling properties
        self.SetScrollRate(10, 10)
        self.SetBackgroundColour(wx.Colour(Color(Hex_BACKGROUNDBOX).rgb))

        # Main sizer for the panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Example: Uncomment and test with sample goals
        # testgoals = [("Black", "COLOR"), ("Liver", "COLOR"), ("Merle", "MERLE"), ("No Spotting", "WHITE")]
        # self.AddGoal(testgoals)

        self.SetSizer(self.sizer)
        self.Layout()

    def AddGoal(self, goallist):
        # Create a horizontal sizer for the row of goals
        goal_sizer = wx.FlexGridSizer(1, 0, 0, 0)  # One row, unlimited columns
        for goal in goallist[:-1]:
            # Add a button for each goal
            button = RoundedButton(parent=self, label=goal[0], colors=GOALCOLORS[goal[1]])
            goal_sizer.Add(button, 1, wx.EXPAND)

            # Add a separator line
            line = wx.StaticLine(self, style=wx.LI_HORIZONTAL, size=(10, 5))
            goal_sizer.Add(line, 0, wx.ALIGN_CENTER)

        # Add the last button without a separator
        button = RoundedButton(parent=self, label=goallist[-1][0], colors=GOALCOLORS[goallist[-1][1]])
        goal_sizer.Add(button, 1, wx.EXPAND)

        # Add the goal sizer to the main vertical sizer
        self.sizer.Add(goal_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Adjust scrollable area
        self.Layout()
        self.SetupScrolling()

    def SetupScrolling(self):
        self.SetVirtualSize(self.sizer.GetMinSize())
        self.FitInside()



# Main application for testing
if __name__ == "__main__":
    app = wx.App(False)
    frame = wx.Frame(None, title="Scrollable Panel Example", size=(800, 400))

    panel = wx.Panel(frame)
    goal_ctrl = GoalCtrl(panel, size=(600, 150))

    # Sample data for testing
    testgoals = [("Black", "COLOR"), ("Liver", "COLOR"), ("Merle", "MERLE"), ("No Spotting", "WHITE")]
    goal_ctrl.AddGoal(testgoals)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(goal_ctrl, 1, wx.EXPAND | wx.ALL, 10)
    panel.SetSizer(sizer)

    frame.Show()
    app.MainLoop()

# class MyFrame(wx.Frame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Create a panel inside the frame
#         panel = wx.Panel(self)
#
#         # Create our custom text-box-like panel with buttons
#         text_box_with_buttons = GoalCtrl(panel)
#
#         # Layout using sizer
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         sizer.Add(text_box_with_buttons, flag=wx.EXPAND | wx.ALL, border=10)
#
#         panel.SetSizer(sizer)
#
#         # Set frame size and center it
#         self.SetSize((1000, 800))
#         self.Center()
#
#
# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None, title="TextBox with Buttons Inside")
#         frame.Show()
#         return True
#
#
# if __name__ == "__main__":
#     app = MyApp()
#     app.MainLoop()


