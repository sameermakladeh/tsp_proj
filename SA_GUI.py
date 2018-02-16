
import wx
import wx.xrc
import wx.grid
import os
import SA_solve
import numpy as np
import wxmplot
import pandas
import subprocess
from tkinter.filedialog import askopenfile


class SAFrame(wx.Frame):
    # derive from frame a new class
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='SA thingy', pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.ALIGN_CENTRE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetAutoLayout(True)

        '''' set up Menu'''
        self.m_menubar = wx.MenuBar(0)
        self.file_menu = wx.Menu()
        self.open_file = wx.MenuItem(self.file_menu, wx.ID_ANY, u"Open", u"Open an existing TSP file", wx.ITEM_NORMAL)
        self.file_menu.Append(self.open_file)

        self.save_file = wx.MenuItem(self.file_menu, wx.ID_ANY, u"Save", u"Save a TSP into a file", wx.ITEM_NORMAL)
        self.file_menu.Append(self.save_file)

        self.file_menu.AppendSeparator()

        self.exit = wx.MenuItem(self.file_menu, wx.ID_ANY, u"Exit", u"Terminate the program", wx.ITEM_NORMAL)
        self.file_menu.Append(self.exit)

        self.m_menubar.Append(self.file_menu, u"File")

        self.about_menu = wx.Menu()
        self.info = wx.MenuItem(self.about_menu, wx.ID_ANY, u"Info", u"Provides info on the program", wx.ITEM_NORMAL)
        self.about_menu.Append(self.info)

        self.m_menubar.Append(self.about_menu, u"About")

        self.SetMenuBar(self.m_menubar)

        '''creates a status bar in the bottom of the window'''
        self.m_statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        ''' set up sizer for GUI layout '''
        fgSizer1 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.06), 1, wx.EXPAND, 5)  # Add spacer pos. 1-5
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.06), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.06), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.06), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.06, self.GetSize()[1] * 0.1), 1, wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Parameters"), wx.VERTICAL)

        gSizer3 = wx.GridSizer(0, 2, 0, 0)

        self.max_tmp = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.DefaultSize,
                                   0)
        gSizer3.Add(self.max_tmp, 0, wx.ALL | wx.EXPAND, 5)

        self.maxTemp = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Max Temperature", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.maxTemp.Wrap(-1)
        gSizer3.Add(self.maxTemp, 0, wx.ALL | wx.EXPAND, 5)

        self.min_tmp = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        gSizer3.Add(self.min_tmp, 0, wx.ALL | wx.EXPAND, 5)

        self.MinTemp = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Min Temperature", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.MinTemp.Wrap(-1)
        gSizer3.Add(self.MinTemp, 0, wx.ALL | wx.EXPAND, 5)

        self.m_alph = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        gSizer3.Add(self.m_alph, 0, wx.ALL | wx.EXPAND, 5)

        self.alpha = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Alpha", wx.DefaultPosition, wx.DefaultSize, 0)
        self.alpha.Wrap(-1)
        gSizer3.Add(self.alpha, 0, wx.ALL | wx.EXPAND, 5)

        self.iter_num = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                    wx.DefaultSize, 0)
        gSizer3.Add(self.iter_num, 0, wx.ALL | wx.EXPAND, 5)

        self.iterations = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Iteration Number", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.iterations.Wrap(-1)
        gSizer3.Add(self.iterations, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer5.Add(gSizer3, 1, wx.EXPAND, 5)

        sbSizer11 = wx.StaticBoxSizer(wx.StaticBox(sbSizer5.GetStaticBox(), wx.ID_ANY, u"label"), wx.VERTICAL)

        self.solvit = wx.Button(sbSizer11.GetStaticBox(), wx.ID_ANY, u"Solve!", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer11.Add(self.solvit, 0, wx.ALL | wx.ALIGN_CENTRE, 5)

        self.init_sol = wx.Panel(sbSizer11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                 wx.TAB_TRAVERSAL)
        self.init_sol.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sbSizer11.Add(self.init_sol, 1, wx.EXPAND | wx.ALL, 5)

        sbSizer5.Add(sbSizer11, 1, wx.EXPAND, 5)

        fgSizer1.Add(sbSizer5, 1, wx.EXPAND, 5)

        sbSizer9 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Data"), wx.HORIZONTAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        ''' Graph initial data '''
        self.init_graph = wx.Panel(sbSizer9.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                   wx.TAB_TRAVERSAL)
        self.init_graph.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.init_graph.SetMinSize(wx.Size(460, 260))

        fgSizer4.Add(self.init_graph, 1, wx.EXPAND | wx.ALL, 5)

        self.tspdata = wx.grid.Grid(sbSizer9.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.VSCROLL)

        ''' set up the Grid for TSP data '''
        self.tspdata.CreateGrid(29, 2)
        self.tspdata.EnableEditing(True)
        self.tspdata.EnableGridLines(True)
        self.tspdata.SetGridLineColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.tspdata.EnableDragGridSize(False)
        self.tspdata.SetMargins(0, 0)
        for i in range(29):
            for j in range(2):
                self.tspdata.SetCellValue(i, j, '0')
                self.tspdata.SetCellEditor(i, j, wx.grid.GridCellFloatEditor())

        # Columns
        self.tspdata.EnableDragColMove(False)
        self.tspdata.EnableDragColSize(True)
        self.tspdata.SetColLabelSize(30)
        self.tspdata.SetColLabelValue(0, u"X")
        self.tspdata.SetColLabelValue(1, u"Y")
        self.tspdata.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.tspdata.EnableDragRowSize(True)
        self.tspdata.SetRowLabelSize(63)
        self.tspdata.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance
        self.tspdata.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        # Cell Defaults
        self.tspdata.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.tspdata.SetMinSize(wx.Size(240, 240))
        fgSizer4.Add(self.tspdata, 0, wx.ALIGN_TOP | wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        ''' Sizer configure - extra '''
        self.m_panel22 = wx.Panel(sbSizer9.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        fgSizer4.Add(self.m_panel22, 1, wx.EXPAND | wx.ALL, 5)

        gSizer7 = wx.GridSizer(0, 2, 0, 0)

        self.imdata = wx.Button(sbSizer9.GetStaticBox(), wx.ID_ANY, u"Import Data", wx.DefaultPosition, wx.DefaultSize,
                                0)
        gSizer7.Add(self.imdata, 0, wx.ALL | wx.ALIGN_CENTRE, 5)

        self.exdata = wx.Button(sbSizer9.GetStaticBox(), wx.ID_ANY, u"Export Data", wx.DefaultPosition, wx.DefaultSize,
                                0)
        gSizer7.Add(self.exdata, 0, wx.ALL | wx.ALIGN_CENTRE, 5)

        fgSizer4.Add(gSizer7, 1, wx.EXPAND, 5)

        sbSizer9.Add(fgSizer4, 1, wx.EXPAND, 5)

        fgSizer1.Add(sbSizer9, 1, wx.EXPAND, 5)

        fgSizer1.Add((self.GetSize()[0] * 0.06, self.GetSize()[1] * 0.1), 1, wx.EXPAND, 5)  # Add spacer pos. 8-9
        fgSizer1.Add((self.GetSize()[0] * 0.06, self.GetSize()[1] * 0.1), 1, wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Optimization"), wx.VERTICAL)
        sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(sbSizer6.GetStaticBox(), wx.ID_ANY, u"Action"), wx.HORIZONTAL)


        self.optimize = wx.Button(sbSizer7.GetStaticBox(), wx.ID_ANY, u"Optimize", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer7.Add(self.optimize, 0, wx.ALL, 5)

        self.outline = wx.Button(sbSizer7.GetStaticBox(), wx.ID_ANY, u"Outline", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer7.Add(self.outline, 0, wx.ALL, 5)

        self.learn = wx.Button(sbSizer7.GetStaticBox(), wx.ID_ANY, u"Learn", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer7.Add(self.learn, 0, wx.ALL, 5)

        sbSizer6.Add(sbSizer7, 1, wx.EXPAND, 5)

        self.opt_sol = wx.Panel(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                wx.TAB_TRAVERSAL)
        self.opt_sol.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sbSizer6.Add(self.opt_sol, 1, wx.EXPAND | wx.ALL, 5)

        self.opt_par = wx.Panel(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                wx.TAB_TRAVERSAL)
        self.opt_par.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        sbSizer6.Add(self.opt_par, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer1.Add(sbSizer6, 1, wx.EXPAND, 5)

        sbSizer10 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Opt. graph"), wx.VERTICAL)

        self.opt_graph = wx.Panel(sbSizer10.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                  wx.TAB_TRAVERSAL)
        self.opt_graph.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.opt_graph.SetMinSize(wx.Size(460, 260))

        sbSizer10.Add(self.opt_graph, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer1.Add(sbSizer10, 1, wx.CENTRE | wx.EXPAND, 5)

        fgSizer1.Add((self.GetSize()[0] * 0.06, self.GetSize()[1] * 0.1), 1, wx.EXPAND, 5)  # Add spacer pos. 12-16
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.04), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.04), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.04), 1, wx.EXPAND, 5)
        fgSizer1.Add((self.GetSize()[0] * 0.1, self.GetSize()[1] * 0.04), 1, wx.EXPAND, 5)


        self.SetSizerAndFit(fgSizer1)
        self.Centre(wx.BOTH)


        ''' Connect events '''
        self.Bind(wx.EVT_MENU, self.on_open, id=self.open_file.GetId())
        self.Bind(wx.EVT_MENU, self.on_save, id=self.save_file.GetId())
        self.Bind(wx.EVT_MENU, self.on_exit, id=self.exit.GetId())
        self.Bind(wx.EVT_MENU, self.on_about, id=self.info.GetId())
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.max_tmp.Bind(wx.EVT_TEXT, self.on_maxtemp)
        self.max_tmp.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_maxtmp)
        self.max_tmp.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_maxtmp)
        self.min_tmp.Bind(wx.EVT_TEXT, self.on_mintemp)
        self.min_tmp.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_mintmp)
        self.min_tmp.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_mintmp)
        self.m_alph.Bind(wx.EVT_TEXT, self.on_alpha)
        self.m_alph.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_alpha)
        self.m_alph.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_alpha)
        self.iter_num.Bind(wx.EVT_TEXT, self.on_iteration)
        self.iter_num.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_iter)
        self.iter_num.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_iter)
        self.solvit.Bind(wx.EVT_BUTTON, self.on_solvit)
        self.solvit.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_solvit)
        self.solvit.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_solvit)
        self.tspdata.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.on_change_data)
        self.imdata.Bind(wx.EVT_BUTTON, self.onimdata)
        self.imdata.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_imdata)
        self.imdata.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_imdata)
        self.exdata.Bind(wx.EVT_BUTTON, self.onexdata)
        self.exdata.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_exdata)
        self.exdata.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_exdata)
        self.optimize.Bind(wx.EVT_BUTTON, self.on_optimize)
        self.optimize.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_optimize)
        self.optimize.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_optimize)
        self.outline.Bind(wx.EVT_BUTTON, self.on_outline)
        self.outline.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_outline)
        self.outline.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_outline)
        self.learn.Bind(wx.EVT_BUTTON, self.on_learn)
        self.learn.Bind(wx.EVT_ENTER_WINDOW, self.on_hover_learn)
        self.learn.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_learn)
        self.Show()

    global pars, opt_pars, curr_data
    pars = opt_pars = [0, 0, 0, 0]
    curr_data = np.zeros((29,2))

    def __del__(self):
        pass

    ''' define Events '''

    def on_open(self, event):
        ''' Chose file to open, must be excel '''
        wildcard = "Excel Files (*.xlsx)|*.xlsx"
        openFileDialog = wx.FileDialog(frame, "Open", "", "",wildcard= wildcard,
                                       style= wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        d_file = pandas.read_excel(openFileDialog.GetFilename())

        col_names = d_file.columns
        col_data = d_file.values
        for i in range(len(col_data[:, 0])):
            for j in range(2):
                self.tspdata.SetCellValue(i, j, str(col_data[i][j]))
                self.tspdata.SetCellEditor(i, j, wx.grid.GridCellFloatEditor())
                curr_data[i][j] = self.tspdata.GetCellValue(i, j)

        pl = wxmplot.PlotPanel(self.init_graph, size=wx.Panel.GetSize(self.init_graph), dpi=100, fontsize=9)
        pl.clear()
        # Not sure why i need to provide limits but it wont work without!! :@
        pl.scatterplot(curr_data[:, 0], curr_data[:, 1], size=2, xmax=max(curr_data[:, 0]) * 1.01,
                       ymax=max(curr_data[:, 1]) * 1.01, xmin=min(curr_data[:, 0]) * 0.98,
                       ymin=min(curr_data[:, 1]) * 0.98)

    def on_save(self, event):
        event.Skip()

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

    def on_maxtemp(self, event):
        pars[0] = float(self.max_tmp.GetValue())

    def on_mintemp(self, event):
        pars[1] = float(self.min_tmp.GetValue())

    def on_alpha(self, event):
        pars[2] = float(self.m_alph.GetValue())

    def on_iteration(self, event):
        pars[3] = float(self.iter_num.GetValue())

    def on_solvit(self, event):
        # TODO change calling SA_solve to calling it with TSP and paramaters
        sol = SA_solve.solve(curr_data, pars)
        labs = ["best value: ", "time: ", "start: "]
        sols = [labs[0], str(sol[1]), labs[1], str(sol[2]), labs[2], str(curr_data[sol[0][0]])]  # show starting point
        self.init_sol.some_text = wx.StaticText(self.init_sol, label=str(sols[0:2]) + '\n' + str(sols[2:4]) +
                                                '\n' + str(sols[4:6]),
                                                size=wx.Panel.GetSize(self.init_sol), style=wx.ALIGN_CENTER)

        ''' Plot the graph so the order of visited points corresponds with the solution'''
        pl = wxmplot.PlotPanel(self.init_graph, size=wx.Panel.GetSize(self.init_graph), dpi=100, fontsize=9)
        pl.clear()
        plot_data = np.zeros((29, 2))
        j = 0
        for i in sol[0]:
            plot_data[j, 0] = curr_data[i, 0]
            plot_data[j, 1] = curr_data[i, 1]
            j += 1
        pl.plot(plot_data[:, 0], plot_data[:, 1], marker='o')


        #LAYOUT = "{!s:16} {!s:16} {!s:16} {!s:16}"
        #print(LAYOUT.format("Max Temperature", "Min Temperature", "Alpha", "Iteration Number"))
        #print(LAYOUT.format(*pars))

    def on_change_data(self, event):
        col_num = self.tspdata.GetNumberCols()
        row_num = self.tspdata.GetNumberRows()
        for i in range(row_num):
            for j in range(col_num):
                curr_data[i][j] = self.tspdata.GetCellValue(i, j)

        pl = wxmplot.PlotPanel(self.init_graph, size=wx.Panel.GetSize(self.init_graph), dpi=100, fontsize=9)
        pl.clear()
        # Not sure why i need to provide limits but it wont work without!! :@
        pl.scatterplot(curr_data[:, 0], curr_data[:, 1], size=2, xmax=max(curr_data[:, 0]) * 1.01,
                       ymax=max(curr_data[:, 1]) * 1.01, xmin=min(curr_data[:, 0]) * 0.98,
                       ymin=min(curr_data[:, 1]) * 0.98)

    def onimdata(self, event):
        ''' Fast importing of a file named 'tsp.xlsx' '''

        d_file = pandas.read_excel('tsp.xlsx')
        col_names = d_file.columns
        col_data = d_file.values
        for i in range(len(col_data[:, 0])):
            for j in range(2):
                self.tspdata.SetCellValue(i, j, str(col_data[i][j]))
                self.tspdata.SetCellEditor(i, j, wx.grid.GridCellFloatEditor())
                curr_data[i][j] = self.tspdata.GetCellValue(i, j)

        pl = wxmplot.PlotPanel(self.init_graph, size=wx.Panel.GetSize(self.init_graph), dpi=100, fontsize=9)
        pl.clear()
        # Not sure why i need to provide limits but it wont work without!! :@
        pl.scatterplot(curr_data[:, 0], curr_data[:, 1], size=2, xmax=max(curr_data[:, 0]) * 1.01,
                       ymax=max(curr_data[:, 1]) * 1.01, xmin=min(curr_data[:, 0]) * 0.98,
                       ymin=min(curr_data[:, 1]) * 0.98)

    def onexdata(self, event):
        event.Skip()

    def on_optimize(self, event):
        # TODO - make an optimized version
        #LAYOUT = "{!s:16} {!s:16} {!s:16} {!s:16}"
        #print(LAYOUT.format("Max Temperature", "Min Temperature", "Alpha", "Iteration Number"))
        #print(LAYOUT.format(*opt_pars))

        sol = SA_solve.solve(curr_data, pars)
        labs = ["best value: ", "time: ", "start: "]
        sols = [labs[0], str(sol[1]), labs[1], str(sol[2]), labs[2], str(curr_data[sol[0][0]])]  # show starting point
        self.opt_sol.some_text = wx.StaticText(self.opt_sol, label=str(sols[0:2]) + '\n' + str(sols[2:4]) +
                                                '\n' + str(sols[4:6]),
                                                size=wx.Panel.GetSize(self.opt_sol), style=wx.ALIGN_CENTER)

        self.opt_par.some_text = wx.StaticText(self.opt_par, label=str(opt_pars), size=wx.Panel.GetSize(self.opt_par), style=wx.ALIGN_CENTER)

        ''' Plot the graph so the order of visited points correspondes with the solution'''
        pl = wxmplot.PlotPanel(self.opt_graph, size=wx.Panel.GetSize(self.init_graph), dpi=100, fontsize=9)
        pl.clear()
        plot_data = np.zeros((29, 2))
        j = 0
        for i in sol[0]:
            plot_data[j, 0] = curr_data[i, 0]
            plot_data[j, 1] = curr_data[i, 1]
            j += 1
        pl.plot(plot_data[:, 0], plot_data[:, 1], marker='o')

        opt_bench = ' Benchmarking will be displayed here '
        self.opt_par.some_text = wx.StaticText(self.opt_graph, label=str(opt_bench),
                                               size=wx.Panel.GetSize(self.init_sol), style=wx.CENTER,
                                               pos=(wx.Panel.GetSize(self.init_graph)[0], 0))

    def on_outline(self, event):
        ''' get the outline points and show the solution without them '''
        outline = SA_solve.find_outline(curr_data, pars)

        self.opt_graph.some_text = wx.TextCtrl(self.opt_graph, size=wx.Panel.GetSize(self.init_graph),
                                               style=wx.TE_MULTILINE | wx.TE_BESTWRAP | wx.TE_READONLY )
        out_sol = []
        index = 0
        for acc in outline:
            if acc[3] > str(0.75):   # TODO: define what is a good benchmark value
                tst = 'point removed is: ({:.4f},{:.4f}) solution is: {} value is: {:.4f} accuracy is: {} \n'.format(
                    *outline[index][0], outline[index][1], outline[index][2], outline[index][3])
                self.opt_graph.some_text.AppendText(tst)
                self.opt_graph.some_text.AppendText('\n')
                out_sol.append(tst)
            index += 1


    def on_learn(self, event):
        event.Skip()

    def on_size(self, event):
        self.Fit()  # Prevent expansion

# These methods add information in the status bar
    def on_hover_solvit(self, event):
        self.m_statusBar.SetStatusText(" Solve the given TSP using SA algorithm ")

    def on_leave_solvit(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_optimize(self, event):
        self.m_statusBar.SetStatusText(" Solve given TSP with an optimized version of SA  ")

    def on_leave_optimize(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_outline(self, event):
        self.m_statusBar.SetStatusText(" Identify outline points in given TSP as problematic hubs ")

    def on_leave_outline(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_learn(self, event):
        self.m_statusBar.SetStatusText(" Initiate a learning algorithm on the parameters of SA and solve the TSP  ")

    def on_leave_learn(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_imdata(self, event):
        self.m_statusBar.SetStatusText(" Fast import of data using 'tsp.xlsx' file ")

    def on_leave_imdata(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_exdata(self, event):
        self.m_statusBar.SetStatusText(" not working yet (if at all :] ) ")

    def on_leave_exdata(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_maxtmp(self, event):
        self.m_statusBar.SetStatusText(" Enter desired Initial temperature of SA algorithm ")

    def on_leave_maxtmp(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_mintmp(self, event):
        self.m_statusBar.SetStatusText(" Enter desired Minimal temperature of SA algorithm ")

    def on_leave_mintmp(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_alpha(self, event):
        self.m_statusBar.SetStatusText(" Enter desired Decay variable of SA algorithm ")

    def on_leave_alpha(self, event):
        self.m_statusBar.SetStatusText("")

    def on_hover_iter(self, event):
        self.m_statusBar.SetStatusText(" Enter desired Number of iterations for each cycle of SA algorithm ")

    def on_leave_iter(self, event):
        self.m_statusBar.SetStatusText("")

    ''' End of event handling'''


app = wx.App(False)  # does not redirects stdout to a window
frame = SAFrame(None)  # frame is the top level window

''' inspect the layout if needed '''
#import wx.lib.inspection as wxli
#wxli.InspectionTool().Show()

app.MainLoop()
