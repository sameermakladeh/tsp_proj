'''creating a GUI for the project'''

import wx

# create an application object
app = wx.App()

# create a frame and show it
frm = wx.Frame(None, title = 'hello world').Show()

# event loop
app.MainLoop()


