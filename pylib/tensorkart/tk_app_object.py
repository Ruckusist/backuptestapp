"""
Filename: tk_app_object.py
creator: eric
collection: tensorkart,
function: Main Program Launcher
critical: True
"""
import os
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
 ##
from xpad import xpad as XboxController

class game_recorder(wx.Frame,object):
    def __init__(self,parent=None,id=-1,title="test",options=None):
        self.options = options
        h_ = 800
        w_ = 600
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
        self.sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.initMenu()
        
        # Build out the Screen
        self.panes_h1 = []
        self.panes_h2 = []
        self.panes_h3 = []
        self.img_output_pane()
        self.graph_output_pane()
        self.recording_button_pane()
        self.progress_test_pane()
        self.build_panels()
        
        # recording stuff
        self.recording = False
        self.preview = False
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.rate = 200
        self.timer.Start(self.rate)
        
        # controller stuff
        self.controller = XboxController()
        #pad = xpad()
        #lx,ly,rx,ry,x,a,b,y,rb = pad.read()
        # playback stuff
        self.playingback = False
    
        ########################################
    def img_output_pane(self,image=None):
        self.img_panel = wx.Panel(self)
        self.panes_h1.append(self.img_panel)
        img = wx.EmptyImage(320,240)
        tmp = img.ConvertToBitmap()
        if image is not None: img = image;
        tmp = img.ConvertToBitmap()
        self.image_in_pane = wx.StaticBitmap(self.img_panel, bitmap=tmp)
        self.btn_preview = wx.Button(self.img_panel, wx.ID_ANY, label="hide", pos=(5,5), size=(85,25))
        self.Bind(wx.EVT_BUTTON, self.on_btn_preview, self.btn_preview)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_preview, self.btn_preview)
        
      
    def graph_output_pane(self,):
        self.joy_panel = wx.Panel(self)
        self.init_plot()
        self.PlotCanvas = FigCanvas(self.joy_panel, wx.ID_ANY, self.fig)
        self.panes_h1.append(self.joy_panel)
        
    def recording_button_pane(self,):
        self.rec_panel = wx.Panel(self)
        self.panes_h2.append(self.rec_panel)
        self.txt_outputDir = wx.TextCtrl(self.rec_panel, wx.ID_ANY, pos=(5,0), size=(320,30))
        #uid = dt.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.txt_outputDir.ChangeValue("/home/eric/git/DeskApp/data/samples/" + "SESSION_FOLDER")
        self.btn_playback = wx.Button(self.rec_panel, wx.ID_ANY, label="Playback", pos=(330,40), size=(100,30))
        self.btn_record = wx.Button(self.rec_panel, wx.ID_ANY, label="Record", pos=(330,0), size=(100,30))
        self.Bind(wx.EVT_BUTTON, self.on_btn_playback, self.btn_playback)
        self.Bind(wx.EVT_BUTTON, self.on_btn_record, self.btn_record)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_record, self.btn_record)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_playback, self.btn_playback)
        
    def progress_test_pane(self,):
		progress = wx.Gauge(self)
		
		self.panes_h3.append(progress)
		self.progress1 = progress

    def build_panels(self):
        self.SetAutoLayout(True)
        for h1 in self.panes_h1:
            self.sizer_h1.Add(h1,1,flag = wx.EXPAND|wx.ALL)
        for h2 in self.panes_h2:
            self.sizer_h2.Add(h2,1,flag = wx.EXPAND|wx.ALL)                    
        for h3 in self.panes_h3:
            self.sizer_h3.Add(h3,1,flag = wx.EXPAND|wx.ALL)                    
        self.sizer_v.Add(self.sizer_h1)
        self.sizer_v.Add(self.sizer_h2)
        self.sizer_v.Add(self.sizer_h3)
        self.SetSizer(self.sizer_v)
        
    def initMenu(self): #{File,Edit,View,Console,Help}
        #{File}
        MenuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        MenuBar.Append(fileMenu,"&File")
        Exit = fileMenu.Append(wx.NewId(), "E&xit","Now is the time for reboot.")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow,Exit)
        self.SetMenuBar(MenuBar)
        
        #{Record}
        recmenu = wx.Menu()
        MenuBar.Append(recmenu,"&Record")
        start = recmenu.Append(wx.NewId(), "&Start...", "Do it")
        self.Bind(wx.EVT_MENU, self.on_btn_record,start)
        testprogress = recmenu.Append(wx.NewId(), "&Progress Test...", "try it out")
        self.Bind(wx.EVT_MENU, self.on_btn_progress_test, testprogress)

        #(Roms)
        romMenu = wx.Menu()
        MenuBar.Append(romMenu,"&Rom")
        self.roms = os.listdir("/home/eric/games/n64/")
        index = 0
        for rom in self.roms:
            rom = romMenu.Append(index,"{}".format(rom),"{}".format(rom))
            self.Bind(wx.EVT_MENU, self.gameStart,rom)
            index +=1
            #"wmctrl -lp | grep Youth | sed -e 's/^\([^ ]*\).*$/\1/g'"
            #"xdotool windowmove 0x04800001 100 100"
    