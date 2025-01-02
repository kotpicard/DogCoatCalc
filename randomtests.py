import wx


class NewWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="New Window", size=(300, 200))

        # Add a panel and some content
        panel = wx.Panel(self)
        label = wx.StaticText(panel, label="This is a new window!", pos=(50, 50))
        font = label.GetFont()
        font.SetPointSize(12)
        label.SetFont(font)

        # Frame settings
        self.Center()


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Main Window", size=(400, 300))

        # Main panel
        panel = wx.Panel(self)

        # Add a button
        button = wx.Button(panel, label="Open New Window", pos=(100, 100))
        button.Bind(wx.EVT_BUTTON, self.on_open_new_window)

        # Frame settings
        self.Center()

    def on_open_new_window(self, event):
        """Handle button click to open a new window."""
        new_window = NewWindow(self)  # Create a new instance of the NewWindow class
        new_window.Show()  # Show the new window


class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow()
        frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
