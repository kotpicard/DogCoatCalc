from RoundedButton import RoundedButton
from GuiConstants import *


class GoalCtrl(wx.Panel):
    def __init__(self, parent, size=(600, 150)):
        super().__init__(parent=parent, size=size)
        self.SetBackgroundColour(Color(Hex_BACKGROUNDBOX).rgb)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # testgoals = [("Black", "COLOR"), ("Liver", "COLOR"), ("Merle", "MERLE"), ("No Spotting", "WHITE")]
        # self.AddGoal(testgoals)
        self.SetSizerAndFit(self.sizer)
        self.Layout()

    def AddGoal(self, goallist):
        goal_sizer = wx.FlexGridSizer(1, 0, 0,0)
        for goal in goallist[:-1]:
            button = RoundedButton(parent=self, label=goal[0], colors=GOALCOLORS[goal[1]])
            goal_sizer.Add(button, 0, wx.EXPAND)
            line = wx.StaticLine(self, style=wx.LI_HORIZONTAL, size=(10,5))
            goal_sizer.Add(line, 0, wx.ALIGN_CENTER)
        button = RoundedButton(parent=self, label=goallist[-1][0], colors=GOALCOLORS[goallist[-1][1]])
        goal_sizer.Add(button, 0, wx.EXPAND)
        self.sizer.Add(goal_sizer, 0, wx.EXPAND | wx.ALL, 10)



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


