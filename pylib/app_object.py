#!/usr/bin/python2
"""
Filename: app_object.py
creator: eric
collection: DeskApp, /pylib
function: Main WxApp handler
critical: True
"""
# Main Windowing Interface
from wx_main_window import loader_window as Main_frame
import wx

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""  Basic Wxpython.SplashScreen setup, im not happy with it.  """
class MySplashScreen(wx.SplashScreen):   
    def __init__(self):
        img = "/home/eric/git/DeskApp/img/ag_logo_png.png"
        bmp = wx.Image(img).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp, wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 2500, None, -1, style = wx.TRANSPARENT|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        wx.EVT_CLOSE(self, self.OnClose)
        
    def OnClose(self, evt):
		self.Destroy()
    
class BootApp(wx.App): #for splash screen
    def OnInit(self):
        frame=MySplashScreen()
        frame.Show(1)
        frame.Centre()        # Always use Imperial.
        return True
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
""" The Launch App is usally pretty lightweight, obviously i put as much in as possible """
class DeskApp(wx.App, object):    
    def __init__(self,options=None):
        self.options = options
        if self.options.verbose is True: print("Step 2: Loading WxApp.")
        wx.App.__init__(self,self.options.debugging,None)        
            
    """ OnInit is loading a boot screen"""
    def OnInit(self):
        if self.options.verbose is True: print("Step 3: LoadMultiple screens with Bootup.")        
        self.main_frame = Main_frame(title="DeskApp - Main",options=self.options)
        self.frame = self.main_frame; self.frame.Show();
        self.SetTopWindow(self.frame)
        return True 
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$