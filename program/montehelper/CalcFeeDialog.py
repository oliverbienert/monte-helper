# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Sep  3 10:10:25 2012

import wx
from wx.lib.pubsub import setupkwargs #@UnusedImport
from wx.lib.pubsub import pub
from ObjectListView import ObjectListView as olv
from ObjectListView import ColumnDefn
from Helpers import Helpers
from WxHelpers import WxHelpers

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

# Make a shorter alias
_ = wx.GetTranslation

class CalcFeeDialog(wx.Dialog, WxHelpers, Helpers):
    def __init__(self, *args, **kwds):
        WxHelpers.__init__(self)
        Helpers.__init__(self)
        # begin wxGlade: CalcFeeDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.l_validfromdate = wx.StaticText(self, -1, _("Ruling valid from"))
        self.validfromdate = wx.DatePickerCtrl(self, -1)
        self.l_receiver = wx.StaticText(self, -1, _("Receiver"))
        self.receiver = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_TAB | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.l_income = wx.StaticText(self, -1, _("Underlying income"))
        self.l_calcfee = wx.StaticText(self, -1, _("Individual calculation"))
        self.l_notes = wx.StaticText(self, -1, _("Notes"))
        self.notes = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.b_ok = wx.Button(self, wx.ID_OK, "")
        self.b_cancel = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnOK, self.b_ok)
        # end wxGlade

        self.olv_income = olv(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.__initOLVIncome()
        self.olv_calcfee = olv(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.__initOLVCalcFee()
        self.__do_layout_noglade()
        
        pub.subscribe(self.Populate, 'dialog.calcfee.populate') #@UndefinedVariable

    def __set_properties(self):
        # begin wxGlade: CalcFeeDialog.__set_properties
        self.SetTitle(_("Parent's fee"))
        self.SetSize((673, 558))
        self.b_ok.SetMinSize((70, 30))
        self.b_cancel.SetMinSize((70, 30))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CalcFeeDialog.__do_layout
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add(self.l_validfromdate, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.validfromdate, 0, 0, 0)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_20.Add(self.l_receiver, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(sizer_20, 0, wx.EXPAND, 0)
        sizer_25.Add(self.receiver, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 3)
        sizer_7.Add(sizer_25, 1, wx.EXPAND, 0)
        sizer_9.Add(self.l_income, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_7.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_14.Add(self.l_calcfee, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(sizer_14, 0, wx.EXPAND, 0)
        sizer_7.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_16.Add(self.l_notes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_19.Add(self.notes, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 3)
        sizer_7.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 1, wx.ALL | wx.EXPAND, 3)
        sizer_6.Add(self.b_ok, 0, 0, 0)
        sizer_6.Add(self.b_cancel, 0, 0, 0)
        sizer_4.Add(sizer_6, 0, wx.ALL | wx.ALIGN_RIGHT, 3)
        self.SetSizer(sizer_4)
        self.Layout()
        # end wxGlade
        self.sizerIncome = sizer_12
        self.sizerCalcFee = sizer_15

    def __initOLVIncome(self):
        self.olv_income.SetColumns([
            ColumnDefn("Name", "left", 80, "name"),
            ColumnDefn("Vorname", "left",80, "firstname"),
            ColumnDefn("Nicht selbst.", "right", 70, "salary", stringConverter = self.to_euro),
            ColumnDefn("Selbst.", "right", 60, "income", stringConverter = self.to_euro),
            ColumnDefn("Arbeitsamt", "right", 65, "unemployment", stringConverter = self.to_euro),
            ColumnDefn("Unterhalt", "right", 60, "childsupport", stringConverter = self.to_euro),
            ColumnDefn("Sonst.", "right", 60, "misc", stringConverter = self.to_euro),
            ColumnDefn(u"Abzügl.", "right", 60, "less", stringConverter = self.to_euro),
            ColumnDefn("Gesamt", "right", 60, "totalincome", stringConverter = self.to_euro, isSpaceFilling=True)
        ])
        
    def __initOLVCalcFee(self):
        self.olv_calcfee.SetColumns([
            ColumnDefn("Name", "left", 100, "name"),
            ColumnDefn("Vorname", "left",100, "firstname"),
            ColumnDefn("Einkomm.", "right", 60, "income", stringConverter = self.to_euro),
            ColumnDefn("Kindergeld", "right", 60, "childbenefit", stringConverter = self.to_euro),
            ColumnDefn("Mind. 1", "right", 50, "reduction1", stringConverter = self.valuePercent),
            ColumnDefn("Mind. 2", "right", 50, "reduction2", stringConverter = self.valuePercent),
            ColumnDefn("Erw. Betr.", "right", 60, "extendeddaytime"),
            ColumnDefn("Einkomm.", "right", 60, "incomeapplied", stringConverter = self.to_euro),
            ColumnDefn("Beitrag", "right", 60, "fee", stringConverter = self.to_euro, isSpaceFilling=True)
        ])

    def __do_layout_noglade(self):
        self.sizerIncome.Add(self.olv_income, 1, wx.ALL|wx.EXPAND, 4)
        self.sizerCalcFee.Add(self.olv_calcfee, 1, wx.ALL|wx.EXPAND, 4)
        self.Layout()
        
    def Populate(self, data, address):
        lst = data['adults']
        for item in lst:
            self.olv_income.AddObject(item)
        lst = data['children']
        for item in lst:
            self.olv_calcfee.AddObject(item)
        addressStr = "%s, %s\n" % (address['name'], address['firstname'])
        addressStr += "%s %s\n" % (address['street'], address['number'])
        addressStr += "%s %s" % (address['postcode'], address['city'])
        self.receiver.ChangeValue(addressStr)

    def OnOK(self, event): # wxGlade: CalcFeeDialog.<event_handler>
        validfromdate = self.wxdate2pydate(self.validfromdate.GetValue())
        pub.sendMessage('dialog.calcfree.senddata',  #@UndefinedVariable
            validfromdate=validfromdate,
            receiver=self.receiver.GetValue(), 
            calcfees=self.olv_calcfee.GetObjects(), 
            income=self.olv_income.GetObjects(), 
            notes=self.notes.GetValue()
        )
        event.Skip()
        

# end of class CalcFeeDialog


