from GuiConstants import *


class LinkButton(wx.Panel):
    def __init__(self, parent, label, size=(200, 50),
                 textcolors=(Color(Hex_FONTLINKCOLOR).rgb, Color(Hex_FONTLINKCOLORHOVER).rgb)):
        super().__init__(parent, size=size)
        self.label = label

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_hover_leave)
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.default_color = parent.GetBackgroundColour()
        self.normal_text_color = textcolors[0]
        self.text_color = textcolors[0]
        self.hover_text_color = textcolors[1]

    def on_size(self, event):
        self.Refresh()

    def on_hover_enter(self, event):
        self.text_color = self.hover_text_color
        self.Refresh()

    def on_hover_leave(self, event):
        self.text_color = self.normal_text_color
        self.Refresh()

    def on_paint(self, event):
        self.Refresh()
        self.Update()
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        gc.SetBrush(wx.Brush(self.GetParent().GetBackgroundColour()))
        gc.DrawRectangle(0, 0, *self.GetSize())

        w, h = self.GetSize()
        #

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, underline=True)
        gc.SetFont(font, self.text_color)
        text_width, text_height = gc.GetTextExtent(self.label)
        gc.DrawText(self.label, (w - text_width) / 2, (h - text_height) / 2)
