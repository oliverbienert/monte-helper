# -*- coding: utf-8 -*-
'''
Created on Jul 21, 2012

@author: oliver
'''

import wx
import re
from WxHelpers import WxHelpers
from datetime import datetime

# Make a shorter alias
_ = wx.GetTranslation

class TextObjectValidator(wx.PyValidator, WxHelpers):
    """ This validator is used to ensure that the user has entered something
        into the text object editor dialog's text field.
    """
    def __init__(self):
        """ Standard constructor.
        """
        WxHelpers.__init__(self)
        wx.PyValidator.__init__(self)
        self.validname = re.compile(r'^((?!\d|_)\w)+$', re.U)
        self.validpostcode = re.compile(r'^\d{5}$')
    
    def Clone(self):
        """ Standard cloner.
    
            Note that every validator must implement the Clone() method.
        """
        return TextObjectValidator()
    
    
    def Validate(self, win):
        """ Validate the contents of the given text control.
        """
        ret = True
        textCtrl = self.GetWindow()
        value = textCtrl.GetValue()
        tcname = textCtrl.GetName()
        
        if tcname in ('name', 'firstname', 'city', 'street', 'number', 'postcode') and len(value) == 0:
            wx.MessageBox(_('Please insert a value!'), "Error")
            ret = False
        elif tcname in ('name', 'firstname', 'city'):
            match = self.validname.match(value)
            if not match:
                wx.MessageBox(_('Please insert a name!'), "Error") 
                ret = False
        elif tcname in ('postcode',):
            match = self.validpostcode.match(value)
            if not match:
                wx.MessageBox(_('Please insert a valid number!'), "Error") 
                ret = False
        elif tcname in ('benefit', 'householdsize') and len(value) > 0:
            try:
                value = int(value)
            except (ValueError, TypeError):
                wx.MessageBox(_('Please insert a valid number!'), "Error") 
                ret = False
        elif tcname in ('birthdate',):
            value = self.wxdate2pydate(value)
            if value == None:
                wx.MessageBox(_('Please insert a valid date'), "Error")
                ret = False
            else:
                today = datetime.now()
                if (today < value):
                    wx.MessageBox(_('Please insert a date in the past'), "Error")
                    ret = False
        elif tcname in ('joindate',):
            value = self.wxdate2pydate(value)
            today = datetime.now()
            if value != None and today < value:
                wx.MessageBox(_('Please insert a date in the past'), "Error")
                ret = False
        elif tcname in ('separationdate'):
            value = self.wxdate2pydate(value)
            if value != None:
                datectrl = win.FindWindowByName('joindate')
                joining_date = self.wxdate2pydate(datectrl.GetValue())
                if joining_date != None and value < joining_date:
                    wx.MessageBox(_('Date of joining have to be older than date of separation!'), "Error")
                    ret = False
        if (ret == False):
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
        else:
            textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
        return ret
    
    def TransferToWindow(self):
        """ Transfer data from validator to window.
    
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.
    
    
    def TransferFromWindow(self):
        """ Transfer data from window to validator.
    
            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.
    
#----------------------------------------------------------------------