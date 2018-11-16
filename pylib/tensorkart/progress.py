#!/usr/bin/python
#
# Copyright (C) 2017

# This file provides an easy way to get a progress bar.
#


# This class is a wrapper for Iterable, to be used in-line in for loops, etc.
#
# Works with or without wx, tqdm, ipython.
#
# Compatible with Python 2.7, 3.x
#
class progress(object):
    def __init__(self, iterable=None, desc=None, wx=None, **kwargs):
        self.tqdm = False
        self.gauge = wx
        
        if wx is not None:
            self.iterable = iterable
            self.index = 0
            self.length = len(iterable)
            
            wx.SetValue(0)
            wx.SetRange(self.length)
            
        else:
            try:
                __IPYTHON__
                from tqdm import tqdm_notebook
#                print('ipython progress')
                self.iterable = tqdm_notebook(iterable=iterable, desc=desc, **kwargs)
                self.tqdm = True

            except NameError or ImportError: # Not iPython environment, or no tqdm_notebook
                try:
                    from tqdm import tqdm
#                    print('standard progress')
                    self.iterable = tqdm(iterable=iterable, desc=desc, **kwargs)
                    self.tqdm = True

                except ImportError: # no tqdm! that's cool, we'll do it our own way
#                    print('no tqdm!')
                    self.iterable = iterable
                    self.index = 0
                    self.length = len(iterable)
        
        
        if not self.tqdm and desc is not None and wx is None:
            print ('>>> PROGRESS BAR >>> ' + desc)
        
    def __iter__(self):
        iterable = self.iterable
        
        for obj in iterable:
            yield obj
            
            # do all our UI updates AFTER the step's work has been done (yield above)
            if not self.tqdm: # tqdm handles everything itself, if we're using it
                index = self.index + 1
                gauge = self.gauge
                
                if gauge is None:
                    print ('>>> %s of %s' % (index, self.length))
                else:
                    self.gauge.SetValue(index)
                    
                self.index = index
            






# Example progress() usage:
#
#for i in progress(range(3), desc='first one   ', leave=False):
#    sleep(1)
#    print(i)
#    for i in progress(range(50), desc=colored('a bigger one', 'cyan'), leave=False):
#        sleep(0.1)
#

def main():
    from time import sleep
    
    for i in progress(range(3), desc='first one   ', leave=True):
        sleep(1)
#        print(i)
    

if __name__ == '__main__':
    main()
    

