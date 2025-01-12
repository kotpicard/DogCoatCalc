import wx


class RoundedButton(wx.Panel):
    def __init__(self, parent, label, size=(100, 50), corner_radius=20,
                 colors=(wx.Colour(100, 149, 237), wx.Colour(72, 118, 255))):
        super().__init__(parent, size=size)
        self.label = label
        self.corner_radius = corner_radius

        # Ensure the panel background matches its parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(parent.GetBackgroundColour())

        # Bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        # self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_hover_leave)

        # Button colors
        self.default_color = colors[0]  # Cornflower blue
        self.hover_color = colors[1]  # Dodger blue
        self.current_color = self.default_color
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        self.Refresh()
        self.Update()


    def on_hover_enter(self, event):
        self.current_color = self.hover_color
        self.Refresh()

    def on_hover_leave(self, event):
        self.current_color = self.default_color
        self.Refresh()

    def on_paint(self, event):
        self.Refresh()
        # Create a graphics context for smooth drawing
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # Clear the background to match the parent's background color
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(0, 0, *self.GetSize())

        # Get the size of the panel
        w, h = self.GetSize()

        # Set brush and pen for the rounded rectangle
        gc.SetBrush(wx.Brush(self.current_color))
        gc.SetPen(wx.Pen(self.current_color))

        # Draw a rounded rectangle
        gc.DrawRoundedRectangle(0, 0, w, h, self.corner_radius)

        # Draw the label
        gc.SetFont(self.GetFont(), wx.Colour(255, 255, 255))  # White text
        text_width, text_height = gc.GetTextExtent(self.label)
        gc.DrawText(self.label, (w - text_width) / 2, (h - text_height) / 2)


# class MyFrame(wx.Frame):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Create a panel inside the frame
#         panel = wx.Panel(self)
#
#         # Add a rounded button to the panel
#         button = RoundedButton(panel, label="Click Me", size=(120, 50), corner_radius=25)
#         button.SetPosition((50, 50))  # Position the button in the panel
#
#         # Set the frame size and center it
#         self.SetSize((300, 200))
#         self.Center()
#
#
# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None, title="Rounded Button Example")
#         frame.Show()
#         return True
#
#
# if __name__ == "__main__":
#     app = MyApp()
#     app.MainLoop()
