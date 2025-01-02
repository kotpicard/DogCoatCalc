from GuiConstants import *


class LinkButton(wx.Panel):
    def __init__(self, parent, label, size=(50, 50), textcolors=(Color(Hex_FONTLINKCOLOR).rgb, Color(Hex_FONTLINKCOLORHOVER).rgb)):
        super().__init__(parent, size=size)
        self.label = label

        # Ensure the panel background matches its parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(parent.GetBackgroundColour())

        # Bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_hover_leave)

        # Button colors
        self.default_color = parent.GetBackgroundColour()
        self.normal_text_color = textcolors[0]
        self.text_color = textcolors[0]
        self.hover_text_color = textcolors[1]

    def on_hover_enter(self, event):
        self.text_color = self.hover_text_color
        self.Refresh()

    def on_hover_leave(self, event):
        self.text_color = self.normal_text_color
        self.Refresh()

    def on_click(self, event):
        wx.MessageBox(f"You clicked '{self.label}'!", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_paint(self, event):
        # Create a graphics context for smooth drawing
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        #
        # # Clear the background to match the parent's background color
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(0, 0, *self.GetSize())

        # Get the size of the panel
        w, h = self.GetSize()
        #

        # Draw the label
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, underline=True)
        gc.SetFont(font, self.text_color)  # White text
        text_width, text_height = gc.GetTextExtent(self.label)
        gc.DrawText(self.label, (w - text_width) / 2, (h - text_height) / 2)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a panel inside the frame
        panel = wx.Panel(self)

        # Add a rounded button to the panel
        button = LinkButton(panel, label="Click Me", size=(120, 50))
        button.SetPosition((50, 50))  # Position the button in the panel

        # Set the frame size and center it
        self.SetSize((300, 200))
        self.Center()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Rounded Button Example")
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
