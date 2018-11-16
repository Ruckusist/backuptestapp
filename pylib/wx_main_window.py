#!/usr/bin/python2
"""
Filename: wx_main_window.py
creator: eric
collection: DeskApp, /pylib
function: Main Program Launcher
critical: True
"""

import wx
import tensorkart.app as tkapp
"""TensorKart_App:More than MarioKart"""

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   
class loader_window(wx.Frame,object):
    def __init__(self,parent=None,id=-1,title="test",options=None):
        self.options = options
        if options is not None:
            h_ = self.options.app_height
            w_ = self.options.app_width
        else:
            h_ = 400 
            w_ = 225
        size = (h_,w_)
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)        
        # Centre of the screen
        x = w / 2
        y = h / 2        
        # Minus application offset
        x -= (h_ / 2)
        y -= (w_ / 2)
        self.options.center = (x,y)
        wx.Frame.__init__(self, parent=parent,id=id,title=title,pos=self.options.center,size=size) # init the class
        #self.panel = wx.Panel(self,-1) # use the whole self as panel
        #self.panel.SetBackgroundColour(self.options.bg_color) # set panel color
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) # default
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.initMenu()
        
        # Build out the Screen
        self.panes = []
        self.img_output_pane()
        self.build_panels()
        
    def img_output_pane(self,image=None):
        self.img_panel = wx.Panel(self)
        self.panes.append(self.img_panel)
        img = wx.Image(self.options.boot_sreen_img)
        if image is not None: img = image;
        tmp = img.ConvertToBitmap()
        bmp = wx.StaticBitmap(self.img_panel, bitmap=tmp)
        return bmp
        
    def build_panels(self):
        self.test = 0
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        for panel in self.panes:
            self.sizer.Add(panel,1,flag = wx.EXPAND|wx.ALL)
        self.Layout()
        
    def initMenu(self): #{File,Edit,View,Console,Help}
        #{File}
        MenuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        MenuBar.Append(fileMenu,"&File")
        Exit = fileMenu.Append(wx.NewId(), "E&xit","Now is the time for reboot.")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow,Exit)
        #{edit}
        editmenu = wx.Menu()
        editmenu.Append(wx.NewId(), "&Copy", "Copy in status bar")
        editmenu.Append(wx.NewId(), "C&ut", "")
        editmenu.Append(wx.NewId(), "Paste", "")
        editmenu.AppendSeparator()
        editmenu.Append(wx.NewId(), "&Options...", "Display Options")
        MenuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(MenuBar)
        #{console}
        consoleMenu = wx.Menu()
        pyShell = consoleMenu.Append(-1,"&Pythyon Shell","Open Python Shell")
        pyFill = consoleMenu.Append(-1, "&View Namespace","Open Pyfilling Namespace Viewer")
        MenuBar.Append(consoleMenu, "&Console")
        self.Bind(wx.EVT_MENU, self.python_shell,pyShell)
        self.Bind(wx.EVT_MENU, self.python_Name_viewer,pyFill)
        #(Examples)
        exampleMenu = wx.Menu()
        picture_frame = exampleMenu.Append(-1,"&Game Recorder","blank transparent frame")
        
        MenuBar.Append(exampleMenu, "E&xamples")
        self.Bind(wx.EVT_MENU,self.launch_game_record,picture_frame)
        
    def recording_toolbar(self,):
        #toolbar = self.CreateToolBar() 
        self.test = 0
        
    def ToDo(self):
        #statusBar = self.CreateStatusBar() # init the Bottom Bar
        #toolbar = self.CreateToolBar() # init the Top Bar
        self.DOMORE = 42
        
    ############## Example STUFF #########################
    def launch_game_record(self,event):
        frame = tkapp.game_recorder(parent=self,title="Game Recorder",options=self.options)
        frame.Show()
    ############## CONSOLE STUFF #########################    
    def python_shell(self, event):
        """ Action caused by ^Menu^Python Shell """
        try:
            from wx.py.shell import ShellFrame
        except:
            print("Failing to load wx.py.shell")
        print("LOG THIS: Python Shell has been called $date $time $sessionID")
        frame = ShellFrame(parent=self)
        frame.Show()

    def python_Name_viewer(self, event):
        """ Action caused by ^Menu^View Namespace """
        try:
            from wx.py.filling import FillingFrame
        except:
            print("Failing to load wx.py.filling")
        print("LOG THIS: namespace viewer has been called $date $time $sessionID")
        frame = FillingFrame(parent=self)
        frame.Show()    
    
    ############## Stock STUFF #########################
    def OnCloseMe(self, event): # out of order :()
        self.Close(True)
        return False

    def OnCloseWindow(self, event): # out of order #()
        self.Destroy()
