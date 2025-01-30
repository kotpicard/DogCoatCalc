import wx


class RoundedButton(wx.Panel):
    def __init__(self, parent, label, size=(100, 50), corner_radius=20,
                 colors=(wx.Colour(100, 149, 237), wx.Colour(72, 118, 255))):
        super().__init__(parent, size=size)
        self.label = label
        self.corner_radius = corner_radius

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(parent.GetBackgroundColour())

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_hover_leave)

        self.default_color = colors[0]
        self.hover_color = colors[1]
        self.current_color = self.default_color
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        self.Refresh()


    def on_hover_enter(self, event):
        self.current_color = self.hover_color
        self.Refresh()

    def on_hover_leave(self, event):
        self.current_color = self.default_color
        self.Refresh()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(0, 0, *self.GetSize())

        w, h = self.GetSize()

        gc.SetBrush(wx.Brush(self.current_color))
        gc.SetPen(wx.Pen(self.current_color))

        gc.DrawRoundedRectangle(0, 0, w, h, self.corner_radius)

        gc.SetFont(self.GetFont(), wx.Colour(255, 255, 255))  # White text
        text_width, text_height = gc.GetTextExtent(self.label)
        gc.DrawText(self.label, (w - text_width) / 2, (h - text_height) / 2)
        self.Update()

