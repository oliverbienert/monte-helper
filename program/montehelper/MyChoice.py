'''
Created on Jun 14, 2012

@author: oliver
'''
import wx

class MyChoice(wx.Choice):
    '''
    classdocs
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(MyChoice, self).__init__(*args, **kwargs)
        self.choices = kwargs['choices']
        
    def SetValue(self, value):
        i = self.choices.index(value)
        self.SetSelection(i)
        
    def GetValue(self):
        "Get the value from the editor"
        selection = self.choices[self.GetCurrentSelection()]
        return selection