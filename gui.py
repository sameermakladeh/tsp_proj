'''creating a GUI for the project'''
import wx
import os

class MainWindow(wx.Frame):
    # derive from frame a new class
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (500,500))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()  # creates a status bar in the bottom of the window

        # set the menu up
        filemenu = wx.Menu()

        # set ID's, these are standard
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "info")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "terminate the program")

        # create the menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # add the File to menubar
        self.SetMenuBar(menuBar)  # add menubar to the frame

        # set the events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)


        self.Show(True)

    def OnAbout(self, event):
        # show a dialog with OK button
        dlg = wx.MessageDialog(self, "text_1", "text_2 becuase hehe", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

app = wx.App(False)  # does not redirects stdout to a window
frame = MainWindow(None, "something something")  # frame is the top level window
app.MainLoop()






'''
# create a frame and show it
class HelloFrame(wx.Frame):
    # a frame that says something
    def __init__(self, *args, **kw):
        # ensure the parents init gets called
        super().__init__(*args, **kw)

        # create a panel and put text in it
        pnl = wx.Panel(self)
        st = wx.StaticText(pnl, label = "print something", pos = (25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu and a status bar
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("hello darkness my old friend...")

    def makeMenuBar(self):
        # we do a menu with items!

        # first make the menu with an exit
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&erm, hello...\tCtrl-H", "help string in status bar")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # help menu
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # make the menu with the two items, '&' means that the next letter is underlined and uses hotkeys
        menuBar = wx.Menu()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # feed the frame
        self.SetMenuBar(menuBar)

        # activate handlers to call the corresponded functions
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        # close the frame
        self.Close(True)

    def OnHello(self, event):
        # say something
        wx.MessageBox("get a life")

    def OnAbout(self, event):
        # display an about dialog, the "|" lets us use icons associated with an item
        wx.MessageBox("about us:", wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    # this creates the app and start the event loop
    app = wx.App()
    frm = HelloFrame(None, title = 'testing 101')
    frm.Show()
    app.MainLoop()

'''



