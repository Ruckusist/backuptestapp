#!/usr/bin/python2
"""
Filename: app.py
creator: eric
collection: tensorkart, /pylib/tensorkart/
function: GUI for TK with all actions
critical: True
"""
"""
import wx
#import wx.wizard	
#import os, shutil
import sys#time
#from datetime import datetime as dt

#import pygame

#from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
#from skimage.color import rgb2gray
#from skimage.transform import resize
#from skimage.io import imread

#import matplotlib.image as mpimg
#import tk_model as tkmodel
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
 ###
import tk_model as tkmodel
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
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
        #  self.loss came with a broken syntax
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
        #data_to_plot = []
        plt.ion()
        plt.figure("Selected Plot", figsize=(16,6))
        for i in range(len(img)):
            #LOG(i, " ", joystick_values[i,:])
            print(" i, " ", joystick_values[i,:]")
 
            
            
"""         
            
            
            
            
            
            
            
            
            
            
            
                       
#!/usr/bin/env python
#import sys
#import pygame
#import wx
#wx.App()
#import numpy as np
#from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.io import imread

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


IMG_W = 200
IMG_H = 66

class test_window(wx.Frame): pass
    
    
class processor(object):
    


    def take_screenshot():
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.Bitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        return bmp.GetSubBitmap(wx.Rect([0,0],[615,480]))
    
    
    def prepare_image(img):
        if(type(img) == wx._core.Bitmap):
            buf = img.ConvertToImage().GetData()
            img = np.frombuffer(buf, dtype='uint8')
    
        img = img.reshape(480, 615, 3)
        img = resize(img, [IMG_H, IMG_W])
    
        return img
    
    def load_sample(self,sample):
        image_files = np.loadtxt(sample + '/data.csv', delimiter=',', dtype=str, usecols=(0,))
        joystick_values = np.loadtxt(sample + '/data.csv', delimiter=',', usecols=(1,2,3,4,5))
        return image_files, joystick_values
    
    
    # training data viewer
    def viewer(self,sample):
        
        image_files, joystick_values = self.load_sample(sample)
    
        plotData = []
    
        plt.ion()
        plt.figure('viewer', figsize=(16, 6))
    
        for i in range(len(image_files)):
    
            # joystick
            print i, " ", joystick_values[i,:]
    
            # format data
            plotData.append( joystick_values[i,:] )
            if len(plotData) > 30:
                plotData.pop(0)
            x = np.asarray(plotData)
    
            # image (every 3rd)
            if (i % 3 == 0):
                plt.subplot(121)
                image_file = image_files[i]
                img = mpimg.imread(image_file)
                plt.imshow(img)
    
            # plot
            plt.subplot(122)
            plt.plot(range(i,i+len(plotData)), x[:,0], 'r')
            plt.hold(True)
            plt.plot(range(i,i+len(plotData)), x[:,1], 'b')
            plt.plot(range(i,i+len(plotData)), x[:,2], 'g')
            plt.plot(range(i,i+len(plotData)), x[:,3], 'k')
            plt.plot(range(i,i+len(plotData)), x[:,4], 'y')
            plt.draw()
            plt.hold(False)
    
            plt.pause(0.0001) # seconds
            i += 1
    
    
    # prepare training data
    def prepare(samples):
        print "Preparing data"
    
        X = []
        y = []
    
        for sample in samples:
            print sample
    
            # load sample
            image_files, joystick_values = load_sample(sample)
    
            # add joystick values to y
            y.append(joystick_values)
    
            # load, prepare and add images to X
            for image_file in image_files:
                image = imread(image_file)
                vec = prepare_image(image)
                X.append(vec)
    
        print "Saving to file..."
        X = np.asarray(X)
        y = np.concatenate(y)
    
        np.save("data/X", X)
        np.save("data/y", y)
    
        print "Done!"
        return
    

if __name__ == '__main__':
    if sys.argv[1] == 'viewer':
        viewer(sys.argv[2])
    elif sys.argv[1] == 'prepare':
        prepare(sys.argv[2:])
