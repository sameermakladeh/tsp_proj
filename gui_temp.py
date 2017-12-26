import wx
import wx.grid
import os
import pandas


class SAFrame(wx.Frame):
    # derive from frame a new class
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (1500,750))
        self.dirname = ''  #  used for opening files
        self.CreateStatusBar()  # creates a status bar in the bottom of the window
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)  #

        '''' set up a Menu objects'''
        appMenu = wx.Menu()
        menuOpen = appMenu.Append(wx.ID_OPEN, '&Open file', 'Open an existing TSP file')
        menuSave = appMenu.Append(wx.ID_SAVE, '&Save file', 'Save TSP into a file')
        appMenu.AppendSeparator()
        menuAbout = appMenu.Append(wx.ID_ABOUT, '&About', 'Description of the program, SA algorithm '
                                                          'and its optimization')
        menuExit = appMenu.Append(wx.ID_EXIT, '&Exit', 'Terminate the program')

        '''' Creates the menu bar '''
        menuBar = wx.MenuBar()
        menuBar.Append(appMenu, '&File')
        self.SetMenuBar(menuBar)

        '''' Bind Events to functions '''
        self.Bind(wx.EVT_MENU, self.on_open, menuOpen)
        # self.Bind(wx.EVT_MENU, self.on_save, menuSave) TODO - do a save into a file (xls probably)
        self.Bind(wx.EVT_MENU, self.on_about, menuAbout)
        self.Bind(wx.EVT_MENU, self.on_exit, menuExit)

        '''' set up a Grid inside the frame and do something with it '''  # TODO - get dynamic data
        grid = wx.grid.Grid(self, pos=(100,200), size=(250,250))
        grid.CreateGrid(1,1)
        for i in range(9):
            grid.AppendRows(1)
        for j in range(1):
            grid.AppendCols(1)
        grid.SetColLabelValue(0, 'x axis')
        grid.SetColLabelValue(1, 'y axis')
        grid.Show()

        '''' set up a Panel inside the frame and do nothing with it '''
        panel = wx.Panel(self, pos=(500,500), size=(600,600))
        wx.TextCtrl(panel, pos=(600,600), size=(300,150))


        self.SetTitle('Welcome')
        self.Show()

    '''' define the functions of the GUI '''
    def on_open(self, event):
        # opens a file - TODO check how to get excel file into the designated area in the program
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def on_exit(self, event):
        self.Close(True)

    def on_about(self, event):
        # show a dialog with OK button
        dlg = wx.MessageDialog(self, "This programs enables the user to input a TSP as a problem on XY axis, "
                                     "and using Simulated Annealing algorithm parameters that the user enters the "
                                     "program solves the TSP and gives and initial good solution. Later the user can "
                                     "choose to optimize the parameters for the algorithm which should introduce better"
                                     " results.", "About the program and SA", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()




app = wx.App(False)  # does not redirects stdout to a window
frame = SAFrame(None, "something something")  # frame is the top level window
app.MainLoop()