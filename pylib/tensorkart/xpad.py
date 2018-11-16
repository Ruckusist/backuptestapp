#!/usr/bin/python2
"""
Filename: Deskapp.py
creator: eric
collection: DeskApp,
function: Main Program Launcher
critical: False
"""

import pygame

class xpad(object):
    def __init__(self,options=None):
        try:
            pygame.init()
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
            print 'unable to connect to Xbox Controller'
            
    def read(self):
        pygame.event.pump()
        
        # left stick
        L_x_axis = self.joystick.get_axis(0)
        L_y_axis = self.joystick.get_axis(1)
        # right stick
        #R_x_axis = self.joystick.get_axis(2)
        #R_y_axis = self.joystick.get_axis(3)
        # face buttons
        #x_btn = self.joystick.get_button(0)
        a_btn = self.joystick.get_button(1)
        b_btn = self.joystick.get_button(2)
        #y_btn = self.joystick.get_button(3)
        # top buttons
        rb = self.joystick.get_button(5)
        #return[L_x_axis,L_y_axis,R_x_axis,R_y_axis,x_btn,a_btn,b_btn,y_btn,rb]
        #return [x, y, a, b, rb]
        return [L_x_axis, L_y_axis, a_btn, b_btn, rb]
        
    def manual_override(self):
        pygame.event.pump()
        return self.joystick.get_button(4) == 1
        
#pad = xpad()
#lx,ly,rx,ry,x,a,b,y,rb = pad.read()
#print(lx,ly,rx,ry,x,a,b,y,rb)