#!/usr/bin/python2
#!FWPH
"""
Filename: config.py
creator: eric
collection: DeskApp, /pylib
function: Static runtime options
critical: True
"""

import os

class config(object):
    """ This should be the main config,  """
    def __init__(self,verbose=False, filename=None):
        self.paths()
        
        self.verbose = verbose               # this turns on the internal log functionality
        self.debugging = False               # this throws a STDOUT with the program
        self.filename = filename             # this is unused
        self.mupenargs = "--nogui --noask"   # this is going to change
        self.app_height = 500                # "small" container
        self.app_width = 346                 # "small" container
        self.center = (960,540)              # hard coded center of 1080 screen for ease
        self.bg_color = "#FFFF13"            # fall back to this from img background
        
        
        # directories
    def paths(self):
        # hard coded paths that can be changed here during install
        self.root_path = "/home/eric/git/DeskApp/"
        # this data is for TensorKart
        self.samples = os.path.join(self.root_path, "data/samples/")
        self.models = os.path.join(self.root_path, "data/models/")
        self.databin = os.path.join(self.root_path, "data/bin/")
        
        # this is for the Main program
        self.startuptip = os.path.join(self.root_path, "out/startup_tips.txt")
        self.boot_sreen_img = os.path.join(self.root_path, "img/loadlogosmaller_500x281_jpg.jpg")