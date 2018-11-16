"""
Filename: Deskapp.py
creator: eric
collection: DeskApp,
function: Main Program Launcher
critical: True
"""


import wx

class Image_Panel(wx.Panel,object):
    def __init__(self, options=None):
        self.options = options
        
    def Build_Window(self,):
        img = wx.EmptyImage(320,240)
        self.tmp = img.ConvertToBitmap()
        self.image = wx.StaticBitmap(self, bitmap=self.tmp)
        
    def Build_Controls(self):
        self.btn_preview = wx.Button(self.img_panel, wx.ID_ANY, label="hide", pos=(5,5), size=(85,25))
        self.Bind(wx.EVT_BUTTON, self.on_btn_preview, self.btn_preview)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_btn_preview, self.btn_preview)
        
    def on_btn_preview(self, event=False):
        self.preview = not self.preview        
        if not self.preview:
            self.image = wx.StaticBitmap(self, bitmap=self.tmp)    
        
    def on_update_btn_preview(self,event=False):
        label = "hide" if self.preview else "Show"
        self.btn_preview.SetLabel(label)
        

def main():
    DeskApp = app.DeskApp(options)
    provider = wx.CreateFileTipProvider(options.startuptip, 2); wx.ShowTip(None, provider, True)
    DeskApp.MainLoop()

if __name__ == '__main__':
    main()