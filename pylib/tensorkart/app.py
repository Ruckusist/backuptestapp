#!/usr/bin/python2
"""
Filename: app.py
creator: eric
collection: tensorkart, /pylib/tensorkart/
function: GUI for TK with all actions
critical: True
"""

import wx
import wx.wizard	
import os, shutil
from threading import Thread
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
#from skimage.color import rgb2gray
from skimage.transform import resize
#from skimage.io import imread
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import tk_model as tkmodel
from time import sleep
from progress import progress
import model
##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from xpad import xpad as XboxController
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   
#
#       GUI OUTPUT -- All tensorKart Modules Combined
#            
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
        self.sizer_h3 = wx.BoxSizer(wx.VERTICAL)
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
        # playback stuff
        self.playingback = False
        # playing Stuff
        self.playing = False
        self.serving = False
        
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
        self.prog_panel = wx.Panel(self)
        #progress = wx.Gauge(self,parent=self)
        self.panes_h3.append(self.prog_panel)
        #self.progress1 = progress
        self.btn_play = wx.Button(self.rec_panel, wx.ID_ANY, label="Record", pos=(330,0), size=(100,30))
        self.Bind(wx.EVT_BUTTON, self.on_btn_play, self.btn_play)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_play, self.btn_play)
  
  

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
        
    ###########################################################3
    
       
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

        
    ##########Game_Preview_Controls######################
    def on_btn_play(self, event=False):
        self.playing = not self.playing        
        if self.playing: self.startServer()
    def on_update_btn_play(self,event=False):
        label = "Stop" if self.playing else "Play"
        self.btn_play.SetLabel(label)
    ##########Game_Preview_Controls######################
    def on_btn_preview(self, event=False):
        self.preview = not self.preview        
        if self.preview: self.playback()
    def on_update_btn_preview(self,event=False):
        label = "hide" if self.preview else "Show"
        self.btn_preview.SetLabel(label)
    ##########Game_Playback_Controls######################
    def on_btn_playback(self, event=False):
        self.playingback = not self.playingback
    def on_update_btn_playback(self,event=False):
        label = "Stop" if self.playingback else "Playback"
        self.btn_playback.SetLabel(label)
    ##########Game_Progress_Controls######################
    def on_btn_progress_test(self, event=False):
        # You need to start any long-running things in a new thread
        # so that the UI continues to update
        class TestProgressThread(Thread):
            def __init__(self,wxapp):
                Thread.__init__(self)
                self.wxapp = wxapp
            
            def run(self):
                for i in progress(iterable=range(3), desc='just testing it', leave=False):
                    sleep(1)
        self.progress_thread = TestProgressThread(self)
        self.progress_thread.start()       
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
        if not self.playingback:
            self.bmp = self.screen_cap()
            self.controller_data = self.controller.read()
            self.update_plot()
        elif self.recording == True:
            self.save_data()
        elif self.serving == True: # we are playing back
            self.handler.bmp = self.screen_cap()

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
        if self.preview:
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

        
        
        
        
        
    def get_playback_data(self,playbackDir):
        # get dir of playback data
        image_files = np.loadtxt(playbackDir + '/data.csv', delimiter=',', dtype=str, usecols=(0,))
        joystick_values = np.loadtxt(playbackDir + '/data.csv', delimiter=',', usecols=(1,2,3,4,5))
        return image_files, joystick_values
        
    def draw_playback(self,playbackDir): 
        imgs, xpad = self.get_playback_data(playbackDir)
        plotData = []
        #self.fig.add_subplot(111)
        
        for i in range(len(imgs)):
            if not self.playingback:
                return
                
            plotData.append( xpad[i,:] )
            if len(plotData) > 60:
                plotData.pop(0)
            x = np.asarray(plotData)
            # Image
            if (i % 30 == 0):    
                img = wx.Image(imgs[i])
                img = img.Rescale(320,240)
                self.image_in_pane.SetBitmap( img.ConvertToBitmap() )
            # Joystick
            if (i % 60 == 0):
                self.axes.plot(range(i,i+len(plotData)), x[:,0], 'r')
                self.axes.hold(True)
                self.axes.plot(range(i,i+len(plotData)), x[:,1], 'b')
                self.axes.plot(range(i,i+len(plotData)), x[:,2], 'g')
                self.axes.plot(range(i,i+len(plotData)), x[:,3], 'k')
                self.axes.plot(range(i,i+len(plotData)), x[:,4], 'y')
                self.axes.hold(False)
                self.PlotCanvas.draw()
                #plt.pause(0.0001) # seconds
            i += 1
            
        self.playingback = False 
        
        
        
    def on_timer(self, event):
        if not self.playingback:
            self.poll()
            self.draw()
        else:
            pass # FIXME
            
    def playback(self): 
        # check that a dir has been specified
        if self.txt_outputDir.IsEmpty():
            msg = wx.MessageDialog(self, 'Specify the Output Directory', 'Error', wx.OK | wx.ICON_ERROR)
            msg.ShowModal() == wx.ID_YES
            msg.Destroy()
            self.playingback = False
        else: # a directory was specified
            self.outputDir = self.txt_outputDir.GetValue()
            self.playingback = True
            self.draw_playback(self.outputDir)       
#        sleep(5)

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
                
                
    ############## Play STUFF #########################
    
    def play(self): pass
        
    
    
    ############## Stock STUFF #########################
    def OnCloseMe(self, event): # out of order :()
        self.Close(True)
        return False

    def OnCloseWindow(self, event): # out of order #()
        self.Destroy()
        
        
    def startServer(self):
        self.handler = PlayComms()
        server = HTTPServer(('', 8321), self.handler)
        self.server_thread = PlayCommsThread(server)
        self.server_thread.start()       
        self.serving = True # should come after server thread has started

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from utils import take_screenshot, prepare_image
#from xpad import xpad as XboxController
import tensorflow as tf
#import model
from termcolor import cprint

class utils(object):
    def __init__(self,options=None): pass

    def screen_cap(self,):
        full_screen = wx.ScreenDC()
        #img = full_screen.GetAsBitmap() # saw it in the list
        size = full_screen.GetSize()
        img = wx.EmptyBitmap(size[0],size[1])
        mem = wx.MemoryDC(img)
        mem.Blit(0,0,size[0],size[1],full_screen,0,0)
        return img.GetSubBitmap(wx.Rect(0,0,615,480))
        
        
    def prepare_image(img):
        # this is a TF thing not a config thing
        IMG_W = 200
        IMG_H = 66
        if(type(img) == wx._core.Bitmap):
            buf = img.ConvertToImage().GetData()
            img = np.frombuffer(buf, dtype='uint8')
    
        img = img.reshape(480, 615, 3)
        img = resize(img, [IMG_H, IMG_W])
    
        return img


class GameOn(object): 
    def __init__(self,options=None): pass

    
# Play
class PlayGames(object):
    def __init__(self,options=None):
        
        #text = wx.StaticText(panel, -1, 'my text', (20, 100))
        #font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        #text.SetFont(font)
        pass
    
class PlayComms(BaseHTTPRequestHandler):
    def __init__(self,options=None):
        self.options = options
        self.man_control = XboxController()
        self.img = None
        self.tf_setup()
    
    def log_message(self, format, *args):
        pass
    
    def tf_setup(self):
        # Start session
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())
        
        # Load Model
        self.saver = tf.train.Saver()
        self.saver.restore(self.sess, "/home/eric/git/DeskApp/data/models/model.ckpt")
        pass
    
    def prepare_image(self,img):
        IMG_W = 200
        IMG_H = 66
        if(type(img) == wx._core.Bitmap):
            buf = img.ConvertToImage().GetData()
            img = np.frombuffer(buf, dtype='uint8')
    
        img = img.reshape(480, 615, 3)
        img = resize(img, [IMG_H, IMG_W])
    
        return img

    def do_GET(self):
        ## Look
        #bmp = take_screenshot()
        vec = self.prepare_image(self.bmp)

        ## Think
        joystick = model.y.eval(feed_dict={model.x: [vec], model.keep_prob: 1.0})[0]

        ## Act
        ### manual override
        manual_override = self.man_control.manual_override()

        if (manual_override):
            joystick = self.man_control.read()
            joystick[1] *= -1 # flip y (this is in the config when it runs normally)

        ### calibration
        output = [
            int(joystick[0] * 80),
            int(joystick[1] * 80),
            int(round(joystick[2])),
            int(round(joystick[3])),
            int(round(joystick[4])),
        ]

        ### print to console
        if (manual_override):
            cprint("Manual: " + str(output), 'yellow')
        else:
            cprint("AI: " + str(output), 'green')

        ### respond with action
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(output)
        return

class PlayCommsThread(Thread):
    def __init__(self,server):
        Thread.__init__(self)
        self.server = server
    
    def run(self):
        self.server.serve_forever()
        
"""     
        

if __name__ == '__main__':
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    server.serve_forever()
    pass
"""










