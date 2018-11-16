#!/usr/bin/python2
"""
Filename: Deskapp.py
creator: eric
collection: DeskApp,
function: Main Program Launcher
critical: True
"""

from pylib.config import config
import pylib.app_object as app
import wx
# MAKE SURE TO CHECK YOUR CONFIGS!

def main():
    print("AG_DeskApp")
    options = config(verbose=True)
    if options.verbose is True: print("Step 1ons.");
    x = app.BootApp()        
    x.MainLoop()
    DeskApp = app.DeskApp(options)
    provider = wx.CreateFileTipProvider(options.startuptip, 2); wx.ShowTip(None, provider, True)
    DeskApp.MainLoop()

if __name__ == '__main__':
    main()