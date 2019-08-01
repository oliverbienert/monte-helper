# -*- coding: utf-8 -*-
'''
Created on Jan 4, 2013

@author: oliver
'''
import wx
import logging
from datetime import datetime
from Helpers import Helpers

logger = logging.getLogger('montehelper.%s' % __name__)
# Make a shorter alias
_ = wx.GetTranslation

class ListCtrlValidator(wx.PyValidator, Helpers):
    '''
    This validator is used to ensure that the user has entered something
        into the listctrl cells.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Helpers.__init__(self)
        wx.Validator.__init__(self)
        
    def Clone(self):
        """ Standard cloner.
    
            Note that every validator must implement the Clone() method.
        """
        return ListCtrlValidator()
    
    def Validate(self, win):
        
        # sys.stdout.write("Variable win: %s" % win)
        listctrl = self.GetWindow()
        lc_name = listctrl.GetName()
        logger.debug('Validating listview %s' % lc_name)
        for item in listctrl.GetObjects():
            # Get the id of the listview row
            item_id = listctrl.GetID(item)
            for k,v in item.items():
                logger.debug('Checking key %s: %s' % (k,v))
                # This fields must not be empty
                if k in ('number', 'fonnumbertype_id', 'incometype_id', 'email', 'relation_id') and self.if_empty(v):
                    # Select row in listview, show warning message and return
                    listctrl.SelectLine(item_id)
                    wx.MessageBox(_('Please fill table completely!'), "Error")
                    return False
                elif k in ('income'):
                    # Income value has to be integer
                    try:
                        v = int(v)
                    except (ValueError, TypeError):
                        listctrl.SelectLine(item_id)
                        wx.MessageBox(_('Please insert a valid income'), "Error") 
                        return False
            # Check rulings dates
            if lc_name == 'lv_rulings':
                # startdate have to be older than enddate
                if (item['startdate'] >= item['enddate']):
                    listctrl.SelectLine(item_id)
                    wx.MessageBox(_('No valid time period!'), "Error")
                    return False
                # Check if enddate lies in the past
                today = datetime.now()
                if (today > item['enddate']):
                    listctrl.SelectLine(item_id)
                    wx.MessageBox(_('Time period ends in the past!'), "Error")
                    return False
        return True

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
