'''
Created on Jan 22, 2013

@author: oliver
'''

import wx
from datetime import datetime

# Make a shorter alias
_ = wx.GetTranslation

class WxHelpers(object):
    '''
    classdocs
    '''

    def pydate2wxdate(self, date):
        '''
        Converts python datetime object to wx.date object
        @param date: date as Python datetime object
        @type date: datetime
        @return: date as wx.datetime object 
        '''
        assert isinstance(date, (datetime, date))
        tt = date.timetuple()
        dmy = (tt[2], tt[1]-1, tt[0])
        wxdate = wx.DateTime.FromDMY(*dmy)
        return wxdate
    
    def wxdate2pydate(self, date):
        '''
        Converts wx.date datetime object to python datetime object
        @param date: date as wx.datetime object
        @type date: wx.datetime
        @return: date as python datetime object 
        '''
        assert isinstance(date, wx.DateTime)
        if date.IsValid():
            ymd = map(int, date.FormatISODate().split('-'))
            return datetime(*ymd)
        else:
            return None
        
    def fill_comboboxes(self, dct):
        for cb_name, cb_dct in dct.items():
            attr = getattr(self, cb_name)
            attr.Append('', {'label':'','id':''})
            for k, v in cb_dct.items():
                v = _(v)
                sub_dct = {'label':v,'id':k}
                attr.Append(sub_dct['label'], sub_dct)
                


    def set_cb_value(self, cb, item_id):
        '''
        Searches for the given item_id in the list of itemObjects
        of the given combobox and set the combobox's selection
        to that item if found.
        
        @param cb: wx.combobox control
        @type cb: object
        @param item_id: item_id to be searched for
        @type item_id: int, string   
        '''
        count = cb.GetCount()
        i = 0
        cb.SetValue = ''
        while i < count:
            itemObj = cb.GetClientData(i)
            if itemObj['id'] == item_id:
                cb.SetSelection(i)
                break
            i += 1
 
    def get_cb_value(self, cb):
        '''
        Returns the itemObject of the given combobox's selection.
        ItemObject is a dictionary with keys label and id.
        The label is the string being displayed in the control, the
        id the one that gets returned to be stored in database.
        
        @param cb: wx.combobox control 
        @type cb: object
        '''
        dct = {'id':None,'label':''}
        itemObject = cb.GetClientData(cb.GetSelection())
        if itemObject:
            dct['id'] = itemObject['id']
            dct['label'] = itemObject['label']
        return dct
            
        