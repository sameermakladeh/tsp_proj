'''creating a GUI for the project'''

import wx
import os


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.quote = wx.StaticText(self, label = "your quote: ", pos = (20,30))
        grid.Add(self.quote, pos = (0,0))

        # something to see how it works
        self.logger = wx.TextCtrl(self, pos=(300,20), size = (200,300), style = wx.TE_MULTILINE|wx.TE_READONLY)

        # a BUTTON
        self.button = wx.Button(self, label = 'save', pos = (200,325))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        # edit control
        self.lblname = wx.StaticText(self, label = 'your name :', pos = (20,60))
        grid.Add(self.lblname, pos = (1,0))
        self.editname = wx.TextCtrl(self, value = 'enter your name here', pos = (150,60), size = (140, -1))
        grid.Add(self.editname, pos = (1,1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

        # combo box ctrl
        self.sampleList = ['friends', 'advertising', 'music']
        self.lblhear = wx.StaticText(self, label = 'How did you hear of us?', pos = (20,90))
        grid.Add(self.lblhear, pos = (3,0))
        self.edithear = wx.ComboBox(self, pos = (150,90), size = (95,-1), choices = self.sampleList, style = wx.CB_DROPDOWN)
        grid.Add(self.edithear, pos = (3,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.edithear)

        # add a spacer
        grid.Add((10,40), pos = (2,0))

        # checkbox
        self.insure = wx.CheckBox(self, label = 'Do you want insurance?', pos = (20,180))
        grid.Add(self.insure, pos = (4,0), span = (1,2), flag = wx.BOTTOM, border = 5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        # radio Box
        radioList = ['blue', 'green', 'red', 'yellow', 'black', 'gray']
        rb = wx.RadioBox(self, label="What color you like?", pos=(20,210), choices=radioList, majorDimension=3, style=wx.RA_SPECIFY_COLS)
        grid.Add(rb, pos = (5,0), span = (1,2))
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

        hsizer.Add(grid, 0, wx.ALL, 5)
        hsizer.Add(self.logger)
        mainSizer.Add(hsizer, 0, wx.ALL, 5)
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self, event):
        self.logger.AppendText('click on object with Id %d\n' % event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())


app = wx.App(False)
frame = wx.Frame(None, title = "Demo with notebook")
nb = wx.Notebook(frame)

nb.AddPage(ExamplePanel(nb), "Absolute position")
nb.AddPage(ExamplePanel(nb), "page 2")
nb.AddPage(ExamplePanel(nb), "page 3")
frame.Show()
app.MainLoop()


'''
app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
'''





'''
class MainWindow(wx.Frame):
    # derive from frame a new class
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (500,500))
        self.dirname = ''
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()  # creates a status bar in the bottom of the window

        # set the menu up, set ID's, these are standard
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, '&Open', "open a file to edit")
        filemenu.AppendSeparator()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "info")
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", "terminate the program")

        # create the menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # add the File to menubar
        self.SetMenuBar(menuBar)  # add menubar to the frame

        # set the events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen(), menuOpen)

        # size things up
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0,6):
            self.buttons.append(wx.Button(self, -1, "Button &" + str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        # layout sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()



    def OnAbout(self, event):
        # show a dialog with OK button
        dlg = wx.MessageDialog(self, "text_1", "text_2 becuase hehe", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self):
        # opens a file
        dlg = wx.FileDialog(self,"Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


app = wx.App(False)  # does not redirects stdout to a window
frame = MainWindow(None, "something something")  # frame is the top level window
app.MainLoop()


'''



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



