#!/bin/python2
"""
AG DESKAPP 2017 - wxPython
"""
import wx
import wx.wizard	
import os, shutil
#import sys, time
from datetime import datetime as dt
import numpy as np
try:
    import tensorflow as tf
except:
    print("training not available")
import pygame
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
## from utils
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.io import imread
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
##
import pylib.tk_model as tkmodel

##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class utils(object):
    def screen_cap(self,):
        full_screen = wx.ScreenDC()
         #img = full_screen.GetAsBitmap() # saw it in the list
        size = full_screen.GetSize()
        img = wx.Bitmap(size[0],size[1])
        mem = wx.MemoryDC(img)
        mem.Blit(0,0,size[0],size[1],full_screen,0,0)
        return img.GetSubBitmap(wx.Rect([0,0],[615,480]))
##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class basic_window(wx.Frame,object):
    """ this fires a basic context window"""
    def __init__(self,parent=None,id=-1,title="test",options=None):
        h_ = 400 # this windows size
        w_ = 225
        size = (h_,w_)
        if options is not None:
            if options.verbose is True: print("Step 4-1: Loading BootScreen.")
            self.options = options
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)        
        # Centre of the screen
        x = w / 2
        y = h / 2        
        # Minus application offset
        x -= (h_ / 2)
        y -= (w_ / 2)
        self.options.center = (x,y)
        #print(self.options.center)
        wx.Frame.__init__(self, parent=parent,id=id,title=title,pos=self.options.center,size=size) # init the class
        self.panel = wx.Panel(self) # use the whole self as panel
        self.cancel_button = wx.Button(self.panel, label="cancel", pos=(5, 5), size=(75, 30)) # make this default
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.cancel_button) # default
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow) # default
    
    def OnCloseMe(self, event):
        self.Close(True)
        return False

    def OnCloseWindow(self, event):
        self.Destroy()
        
    # Just grouping the empty event handlers together
    def OnPrev(self, event): pass
    def OnNext(self, event): pass
    def OnLast(self, event): pass
    def OnFirst(self, event): pass
    def OnOpen(self, event): pass
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass
    def OnOptions(self, event): pass
##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class XboxController:
    def __init__(self):
        try:
            pygame.init()
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
            print('unable to connect to Xbox Controller')
    def read(self):
        pygame.event.pump()
        x = self.joystick.get_axis(0)
        y = self.joystick.get_axis(1)
        
        x_btn = self.joystick.get_button(0)
        a = self.joystick.get_button(1)
        b = self.joystick.get_button(2) # b=1, x=2
        y_btn = self.joystick.get_button(3)
        rb = self.joystick.get_button(5)
        
        self.joystick.get_button(0)
        rb = self.joystick.get_button(5)
        return [x, y, a, b, rb]
    def manual_override(self):
        pygame.event.pump()
        return self.joystick.get_button(4) == 1
##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
class Data(object):
    def __init__(self):
        self._X = np.load("data/X.npy")
        self._y = np.load("data/y.npy")
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples = self._X.shape[0]

    @property
    def num_examples(self):
        return self._num_examples

    def next_batch(self, batch_size):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._X[start:end], self._y[start:end]

       
class train_model(object):
    def __init__(self, options=None):
        self.options = options
        
        self.data = Data()
        self.build_model()
        self.L2NormConst = 0.001 # should be an option?
        self.model = tkmodel
        pass
    
    def build_model(self):
        self.sess = tf.InteractiveSession()
        self.train_vars = tf.trainable_variables()
        
        mean = tf.reduce_mean(tf.square(tf.sub(self.model.y_, self.model.y)))
        proc1 = tf.add_n([tf.nn.l2_loss(v) for v in self.train_vars])
        self.loss = mean + (proc1*self.L2NormConst)
        """  self.loss came with a broken syntax  """
        #self.loss =  tf.reduce_mean(tf.square(tf.sub(model.y_, model.y))) + 
        #        tf.add_n([tf.nn.l2_loss(v) for v in train_vars]) * 
        #        self.L2NormConst
        pass
    
    def save(self): 
        # Save the Model
        saver = tf.train.Saver()
        saver.save(self.sess, "/home/eric/git/Deskapp/data/model/tensorkart_model.ckpt")
        pass
    def load(self): pass

    def train(self): 
        train_step = tf.train.AdamOptimizer(1e-5).minimize(self.loss)    
        self.sess.run(tf.global_variables_initializer())
        # Training loop variables
        epochs = 99
        batch_size = 42        
        num_samples = self.data.num_examples
        step_size = int(num_samples / batch_size) # this was hardcoded in other examples
        
        for epoch in range(epochs):
            for i in range(step_size):
                batch = self.data.next_batch(100)
                train_step.run(feed_dict={self.model.x: batch[0], self.model.y_: batch[1], self.model.keep_prob: 0.8}) #! Hardcoded value
        
                if i%25 == 0:
                  loss_value = self.loss.eval(feed_dict={self.model.x:batch[0], self.model.y_: batch[1], self.model.keep_prob: 1.0})  #! hardcoded value
                  print("epoch: {} step: {} loss: {}".format(epoch, epoch * batch_size + i, loss_value))
        self.save()        
        pass
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
class process_input_folder(object):
    def __init__(self, options=None,path=None):
        self.options = options
        self.path = path
        #if path is None:
            #return: LOG("choose from the menu")
        pass

    def load_sample(self):
        sample = self.path
        self.image_files = np.loadtxt(sample + '/data.csv', delimiter=',', dtype=str, usecols=(0,))
        self.joystick_values = np.loadtxt(sample + '/data.csv', delimiter=',', usecols=(1,2,3,4,5))
        return self.image_files, self.joystick_values
    
    def plot_joy_values(self):
        #if self.path is None: return False
        img, joy = self.load_sample()
        data_to_plot = []
        plt.ion()
        plt.figure("Selected Plot", figsize=(16,6))
        for i in range(len(img)):
            #LOG(i, " ", joystick_values[i,:])
            print(" i, " ", joystick_values[i,:]")
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   
class game_recorder(wx.Frame,object):
    def __init__(self,parent=None,id=-1,title="test",options=None):
        self.options = options
        h_ = 625 
        w_ = 400
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
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.initMenu()
        
        # Build out the Screen
        self.panes_h1 = []
        self.panes_h2 = []
        self.img_output_pane()
        self.graph_output_pane()
        self.recording_button_pane()
        self.build_panels()
        
        # recording stuff
        self.recording = False
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.rate = 200
        self.timer.Start(self.rate)
        
        # controller stuff
        self.controller = XboxController()
        
    def img_output_pane(self,image=None):
        self.img_panel = wx.Panel(self)
        self.panes_h1.append(self.img_panel)
        img = wx.EmptyImage(320,240)
        tmp = img.ConvertToBitmap()
        if image is not None: img = image;
        tmp = img.ConvertToBitmap()
        self.image_in_pane = wx.StaticBitmap(self.img_panel, bitmap=tmp)
        return True
      
    def graph_output_pane(self,):
        self.joy_panel = wx.Panel(self)
        self.init_plot()
        self.PlotCanvas = FigCanvas(self.joy_panel, wx.ID_ANY, self.fig)
        self.panes_h1.append(self.joy_panel)
        return True
        
    def recording_button_pane(self,):
        self.rec_panel = wx.Panel(self)
        self.panes_h2.append(self.rec_panel)
        self.txt_outputDir = wx.TextCtrl(self.rec_panel, wx.ID_ANY, pos=(5,0), size=(320,30))
        #uid = dt.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.txt_outputDir.ChangeValue("/home/eric/git/DeskApp/data/samples/" + "SESSION_FOLDER")

        self.btn_record = wx.Button(self.rec_panel, wx.ID_ANY, label="Record", pos=(330,0), size=(100,30))
        self.Bind(wx.EVT_BUTTON, self.on_btn_record, self.btn_record)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_record, self.btn_record)
        
    def file_tree(self, rootdir):
        rootId = self.CalcTree.AddRoot(root)
    
        self.buildTreeRecursion(rootdir, rootId)
    
    def buildTreeRecursion(self, dir, parentId):
        # Iterate over the files in dir
        for file in dirFiles: 
            id = self.CalcTree.AppendItem(parentId, file) 
    
            if file is self.a_directory:
                self.buildTreeRecursion(file, id)

        
    def build_panels(self):
        self.SetAutoLayout(True)
        for h1 in self.panes_h1:
            self.sizer_h1.Add(h1,1,flag = wx.EXPAND|wx.ALL)
        for h2 in self.panes_h2:
            self.sizer_h2.Add(h2,1,flag = wx.EXPAND|wx.ALL)                    
        self.sizer_v.Add(self.sizer_h1)
        self.sizer_v.Add(self.sizer_h2)
        self.SetSizer(self.sizer_v)
        
    def initMenu(self): #{File,Edit,View,Console,Help}
        #{File}
        MenuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        MenuBar.Append(fileMenu,"&File")
        Exit = fileMenu.Append(wx.NewId(), "E&xit","Now is the time for reboot.")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow,Exit)
        self.SetMenuBar(MenuBar)
        
        #{record}
        recmenu = wx.Menu()
        MenuBar.Append(recmenu,"&Record")
        start = recmenu.Append(wx.NewId(), "&Start...", "Do it")
        self.Bind(wx.EVT_MENU, self.on_btn_record,start)

        #(Roms)
        romMenu = wx.Menu()
        MenuBar.Append(romMenu,"&Rom")
        self.roms = os.listdir("/home/eric/games/n64/")
        index = 0
        for rom in self.roms:
            rom = romMenu.Append(index,"{}".format(rom),"{}".format(rom))
            self.Bind(wx.EVT_MENU, self.gameStart,rom)
            index +=1
            "wmctrl -lp | grep Youth | sed -e 's/^\([^ ]*\).*$/\1/g'"
            "xdotool windowmove 0x04800001 100 100"
        
    def recording_toolbar(self,):
        toolbar = self.CreateToolBar() 
        self.SetToolBar(toolbar)
        self.test = 0
        
    def ToDo(self):
        #statusBar = self.CreateStatusBar() # init the Bottom Bar
        #toolbar = self.CreateToolBar() # init the Top Bar
        self.DOMORE = 42
        
    def gameStart(self,event):
        path = "/home/eric/games/n64/"
        x = event.GetId()
        rom_is = self.roms[x]
        print("Starting Game: {}".format(path+rom_is))
        # OS SYSTEM CALLS
        #move_screen = "xdotool windowmove $( wmctrl -lp | grep mupen64plus | sed -e 's/^\\([^ ]*\\).*$/\\/g' ) 200 200"
        start_game = "mupen64plus {1} '{0}' &".format(path+rom_is,self.options.mupenargs)
        os.system(start_game)
        #time.sleep(3)
        #os.system(move_screen)        
        return True
        
    
    ##########Game_Record_Controls######################
    def on_btn_record(self,event=False):
        # pause timer
        self.timer.Stop()
        # switch state
        self.recording = not self.recording

        if self.recording:
            self.start_recording()

        # un pause timer
        self.timer.Start(self.rate)
        
    def on_update_btn_record(self,event=False):
        label = "Stop" if self.recording else "Record"
        self.btn_record.SetLabel(label)
    
    def init_plot(self):
        self.plotMem = 50 # how much data to keep on the plot
        self.plotData = [[0] * (5)] * self.plotMem # mem storage for plot

        self.fig = Figure((4,3))
        self.axes = self.fig.add_subplot(111)


    def screen_cap(self,):
        full_screen = wx.ScreenDC()
        #img = full_screen.GetAsBitmap() # saw it in the list
        size = full_screen.GetSize()
        img = wx.EmptyBitmap(size[0],size[1])
        mem = wx.MemoryDC(img)
        mem.Blit(0,0,size[0],size[1],full_screen,0,0)
        return img.GetSubBitmap(wx.Rect(0,0,615,480))
        
    def poll(self):
        self.bmp = self.screen_cap()
        self.controller_data = self.controller.read()
        self.update_plot()

        if self.recording == True:
            self.save_data()


    def update_plot(self):
        self.plotData.append(self.controller_data) # adds to the end of the list
        self.plotData.pop(0) # remove the first item in the list, ie the oldest
    
    def save_data(self):
        image_file = self.outputDir+'/'+'img_'+str(self.t)+'.png'
        self.bmp.SaveFile(image_file, wx.BITMAP_TYPE_PNG)

        # make / open outfile
        outfile = open(self.outputDir+'/'+'data.csv', 'a')

        # write line
        outfile.write( image_file + ',' + ','.join(map(str, self.controller_data)) + '\n' )
        outfile.close()
        self.t += 1           
        
    def draw(self):
        # Image
        img = self.bmp.ConvertToImage()
        img = img.Rescale(320,240)
        self.image_in_pane.SetBitmap( img.ConvertToBitmap() )
        # Joystick
        x = np.asarray(self.plotData)
        self.axes.plot(range(0,self.plotMem), x[:,0], 'r')
        self.axes.hold(True)
        self.axes.plot(range(0,self.plotMem), x[:,1], 'b')
        self.axes.plot(range(0,self.plotMem), x[:,2], 'g')
        self.axes.plot(range(0,self.plotMem), x[:,3], 'k')
        self.axes.plot(range(0,self.plotMem), x[:,4], 'y')
        self.axes.hold(False)
        self.PlotCanvas.draw()
    
    def on_timer(self, event):
        self.poll()
        # stop drawing if recording to avoid slow downs
        if self.recording == False:
            self.draw()
            
    def start_recording(self):
        # check that a dir has been specified
        if self.txt_outputDir.IsEmpty():
            msg = wx.MessageDialog(self, 'Specify the Output Directory', 'Error', wx.OK | wx.ICON_ERROR)
            msg.ShowModal() == wx.ID_YES
            msg.Destroy()
            self.recording = False
        else: # a directory was specified
            self.outputDir = self.txt_outputDir.GetValue()
            self.t = 0
            # check if path exists - ie may be saving over data
            if os.path.exists(self.outputDir):
                msg = wx.MessageDialog(self, 'Output Directory Exists - Overwrite Data?', 'Yes or No', wx.YES_NO | wx.ICON_QUESTION)
                result = msg.ShowModal() == wx.ID_YES
                msg.Destroy()
                # overwrite the data
                if result == True:
                    # delete the dir
                    shutil.rmtree(self.outputDir)
                    # re-make dir
                    os.mkdir(self.outputDir)
                # do not overwrite the data
                else: # result == False
                    self.recording = False
                    self.txt_outputDir.SetFocus()
            # no directory so make one
            else:
                os.mkdir(self.outputDir)
                
    ############## Stock STUFF #########################
    def OnCloseMe(self, event): # out of order :()
        self.Close(True)
        return False

    def OnCloseWindow(self, event): # out of order #()
        self.Destroy()

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
        frame = game_recorder(parent=self,id=-1,title="Game Recorder",options=self.options)
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

        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class MySplashScreen(wx.SplashScreen):   
    def __init__(self):
        img = "/home/eric/git/DeskApp/img/ag_logo_png.png"
        bmp = wx.Image(img).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp, wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 2500, None, -1, style = wx.TRANSPARENT|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        wx.EVT_CLOSE(self, self.OnClose)
        #self.Bind(wx.EVT_IDLE, self.OnIdle)
        
    def OnClose(self, evt):
		self.Destroy()
    
class BootApp(wx.App): #for splash screen
    def OnInit(self):
        frame=MySplashScreen()
        frame.Show(1)
        frame.Centre()        
        return True
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class DeskApp(wx.App, object):
    """ This should control the middle functions to get between actions """
    def __init__(self,options=None):
        self.options = options
        if self.options.verbose is True: print("Step 2: Loading WxApp.")
        wx.App.__init__(self,False,None)        
            
    """ OnInit is loading a boot screen"""
    def OnInit(self):
        if self.options.verbose is True: print("Step 3: LoadMultiple screens with Bootup.")
        #self.main_frame = game_record(title="DeskApp - Record",options=self.options)
        
        self.main_frame = loader_window(title="DeskApp - Main",options=self.options)
        self.frame = self.main_frame; self.frame.Show();
        self.SetTopWindow(self.frame)
        return True 
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class config(object):
    """ This should be the main config,  """
    def __init__(self,verbose=False, filename=None):
        self.TensorKart_configs()
        self.boot_sreen_img = "/home/eric/Documents/loadlogosmaller_500x281_jpg.jpg"
        self.verbose = verbose
        self.filename = filename
        self.mupenargs = "--nogui --noask"
        self.app_height = 500
        self.app_width = 346        
        self.center = (960,540)
        self.bg_color = "#FFFF13"
        
    def TensorKart_configs(self):
        self.keep_prob = 0.8
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def main():
    print("AG_DeskApp")
    options = config(verbose=True)
    if options.verbose is True: print("Step 1: Register options.");
    #x = BootApp()        
    #x.MainLoop()
    app = DeskApp(options)
    #provider = wx.CreateFileTipProvider("startup_tips.txt", 2); wx.ShowTip(None, provider, True)
    app.MainLoop()

if __name__ == '__main__':
    main()
