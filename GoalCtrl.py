from RoundedButton import RoundedButton
from GuiConstants import *
import wx
from math import floor, ceil


class GoalCtrl(wx.ScrolledWindow):
    def __init__(self, parent, size=(600, 150)):
        super().__init__(parent=parent, size=size)
        # Set up scrolling properties
        self.goals = []

        self.SetScrollRate(10, 10)
        self.SetBackgroundColour(wx.Colour(Color(Hex_BACKGROUNDBOX).rgb))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.goal_sizers = []
        self.currentgoalid = 0
        self.SetSizer(self.sizer)
        self.selected = []
        self.Layout()

    def AddGoal(self, goallist, selectable, customcolors):
        print(goallist, customcolors)
        goal_sizer = wx.FlexGridSizer(1, 0, 0, 0)
        if selectable:
            selector = wx.CheckBox(self)
            selector.Bind(wx.EVT_CHECKBOX, self.UpdateSelected)
            selector.num = self.currentgoalid
            self.currentgoalid += 1
            goal_sizer.Add(selector, 0, wx.ALIGN_CENTER)
        for i, goal in enumerate(goallist[:-1]):
            if not customcolors:
                colors = GOALCOLORS[goal[1]]
            else:
                value = customcolors[i]
                # value is 1-3
                if value == 0:
                    colors = (Color(Hex_IMPOSSIBLE).rgb, Color(Hex_IMPOSSIBLE).rgb)
                else:
                    low = floor(value)
                    high = ceil(value)
                    scale = value - low
                    lowcolor = GOALTESTCOLORS[low - 1]
                    highcolor = GOALTESTCOLORS[high - 1]
                    color = Color().GetColorInBetween(lowcolor, highcolor, scale)
                    colors = (color, color)

            button = RoundedButton(parent=self, label=goal[0], colors=colors)
            goal_sizer.Add(button, 1, wx.EXPAND)

            line = wx.StaticLine(self, style=wx.LI_HORIZONTAL, size=(10, 5))
            goal_sizer.Add(line, 0, wx.ALIGN_CENTER)

        if not customcolors:
            colors = GOALCOLORS[goallist[-1][1]]
        else:
            value = customcolors[-1]
            # value is 1-3
            if value == 0:
                colors = (Color(Hex_IMPOSSIBLE.rgb), Color(Hex_IMPOSSIBLE.rgb))
            else:
                low = floor(value)
                high = ceil(value)
                scale = value - low
                lowcolor = GOALTESTCOLORS[low - 1]
                highcolor = GOALTESTCOLORS[high - 1]
                color = Color().GetColorInBetween(lowcolor, highcolor, scale)
                colors = (color, color)

        button = RoundedButton(parent=self, label=goallist[-1][0], colors=colors)
        goal_sizer.Add(button, 1, wx.EXPAND)
        self.sizer.Add(goal_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.goal_sizers.append(goal_sizer)

        # Adjust scrollable area
        self.Layout()
        self.SetupScrolling()

    def Fill(self, data, selectable=True, customcolors=False):
        for i,elem in enumerate(data):
            if elem not in self.goals:
                self.goals.append(elem)
                if customcolors:
                    self.AddGoal(elem, selectable, customcolors[i])
                else:
                    self.AddGoal(elem, selectable, customcolors)

    def SetupScrolling(self):
        self.SetVirtualSize(self.sizer.GetMinSize())
        self.FitInside()

    def ClearGoals(self):
        for sizer in self.goal_sizers:
            sizer.Clear(delete_windows=True)
        self.Layout()

    def UpdateSelected(self, e):
        num = e.GetEventObject().num
        if num in self.selected:
            self.selected.remove(num)
            print(num, "deselected")
        else:
            self.selected.append(num)
            print(num, "selected")
        print(self.selected)

# # Main application for testing
# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = wx.Frame(None, title="Scrollable Panel Example", size=(800, 400))
#
#     panel = wx.Panel(frame)
#     goal_ctrl = GoalCtrl(panel, size=(600, 150))
#
#     # Sample data for testing
#     testgoals = [("Black", "COLOR"), ("Liver", "COLOR"), ("Merle", "MERLE"), ("No Spotting", "WHITE")]
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#     goal_ctrl.AddGoal(testgoals)
#
#     sizer = wx.BoxSizer(wx.VERTICAL)
#     sizer.Add(goal_ctrl, 1, wx.EXPAND | wx.ALL, 10)
#     panel.SetSizer(sizer)
#
#     frame.Show()
#     app.MainLoop()
#
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
# #
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
