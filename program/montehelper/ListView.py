# -*- coding: utf-8 -*-
'''
Created on Sep 21, 2012

@author: oliver
'''
import wx
import wx.lib.mixins.listctrl as listmix
import datetime
import logging
from Helpers import Helpers

logger = logging.getLogger('montehelper.%s' % __name__)

# Make a shorter alias
_ = wx.GetTranslation

class ListView(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter, Helpers):
    '''
    A listctrl based listview (reportmode) with
    sortable columns, autowidth last column and image columns.
    '''

    def __init__(self, parent, *params):
        '''
        Instantiates the Listview and initializes
        object-wide variables 
        '''
        super(ListView, self).__init__(parent,
                                       style = wx.LC_REPORT)
        # Extend the last column automatically
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        # ALternate colors
        self.evenRowsBackColor = wx.Colour(240, 248, 255) # ALICE BLUE
        self.oddRowsBackColor = wx.Colour(255, 250, 205) # LEMON CHIFFON
        # Helper methods
        Helpers.__init__(self)
        # Bind for sorting
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColumnClick)
        self.colnum = 0
        # Maps from column name to column number
        self.colnames = {}
        # Maps from column number to column name
        self.colnumbers = {}
        # Columns to be converted to string
        self.strConvCols = {}
        # Columns to contain images
        self.imgCols = {}
        # Item data mapping
        self.itemDataMap = {}
        # Item to object id mapping
        self.itemObjectID = {}
        # Store data dict objects
        self.id2obj_dict = {}
        # Windows definitely treats the first column differently. 
        # One workaround is to create an empty column 0 and hide it
        self.InsertColumn(self.colnum, '', width=1)
        self.colnames['dummy'] = self.colnum
        self.colnumbers[self.colnum] = 'dummy'
        self.colnum += 1        
        # catch resize event
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColDrag)
        
    def InitImageList(self, lst, dct):
        '''
        Sets the image list to be used by the list control
        The img_idx dict maps from a name to the index of the image
        in the image list
        '''
        self.SetImageList(lst, wx.IMAGE_LIST_SMALL)
        self.img_idx = dct
        
    def SetObjects(self, data):
        '''
        Fill the listview with data
        '''
        # Clear the list
        self.__clear()
        index = 0
        for dct in data:
            self.__updateItemDataMap(index, dct)
            index += 1
        # Now insert data in listview
        for key, values in self.itemDataMap.items():
            self.__insertTableRow(key, values)
        # Now that the list exists we can init the sorter mixin,
        listmix.ColumnSorterMixin.__init__(self, len(self.colnumbers))
        self.SetColumnWidth(0, 0)
    
    def GetObjects(self):
        '''
        Return the listview's objects
        '''
        lst = []
        for d in self.id2obj_dict.values():
            lst.append(d)
        return lst

    def SetColumn(self, colname, heading, colformat, width, stringConverter=None, image=None):
        '''
        Initialize the columns of the view
        '''
        self.InsertColumn(self.colnum, heading, colformat, width)
        # We store the colnum in a column name dict
        self.colnames[colname] = self.colnum
        # The other way round:
        # Register colname in column number dict
        self.colnumbers[self.colnum] = colname
        self.colnum += 1
        # Check if values have to be converted to string
        # or if it is a image column
        if stringConverter:
            self.strConvCols[colname] = stringConverter
        if image:
            self.imgCols[colname] = image
        # self.sortedcolumns = sorted(self.colnumbers.keys())[1:]
            
    def GetListCtrl(self):
        '''
        Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
        '''
        return self
    
    def GetSelectedObject(self):
        '''
        Get the object of the selected row
        '''
        
        indices = self.__getSelectedIndices()
        if len(indices) != 1:
            return None
        # Reverse mapping
        key = self.GetItemData(indices[0])
        oid = self.itemObjectID[key]
        dct = self.__id2obj(oid)
        return dct
    
    def AddObject(self, obj):
        '''
        Insert an new object (row)
        '''
        # Get last itemDataMap index
        try:
            # Get the largest index and increment it
            index = sorted(self.itemDataMap.keys())[-1] + 1
        except (IndexError):
            # No previous objects, we start with 0
            index = 0
        # Save the object in itemDataMap
        self.__updateItemDataMap(index, obj)
        # Insert new row
        self.__insertTableRow(index, self.itemDataMap[index])
    
    def RemoveObject(self, obj):
        '''
        Delete an object (row)
        '''
        oid = id(obj)
        index = self.find_key(self.itemObjectID, oid)
        # Delete from listview...
        self.DeleteItem(index)
        # and from the associated dicts
        del self.itemDataMap[index]
        del self.itemObjectID[index]
        del self.id2obj_dict[oid]
    
    def RefreshObject(self, obj):
        '''
        Update a row
        '''
        oid = id(obj)
        # Search in values of dict itemObjectID
        # and return key of found object id
        index = self.find_key(self.itemObjectID, oid)
        # Update itemDataMap
        self.__updateItemDataMap(index, obj)
        # Update list item (row)
        self.__updateTableRow(index, self.itemDataMap[index])
        
    def OnColumnClick(self, event):
        '''Sort the list view'''
        self.RefreshRows()
        
    def OnColDrag(self, evt):
        '''
        Prevent col drag events from dealing with column 0
        (the dummy column we build for Windows)
        '''
        if evt.m_col == 0:
            evt.Veto()
            
    def GetID(self, obj):
        oid = id(obj)
        index = self.find_key(self.itemObjectID, oid)
        return index
            
    def SelectLine(self, item_id):
        try:
            self.__unselectLines()
            self.SetItemState (item_id, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        except (Exception), e:
            logger.error('Error while trying to highlight listctrl item: %s' % e)

    def __clear(self):
        '''
        Clears the listview and resets all associated dicts
        '''
        self.DeleteAllItems()
        self.itemDataMap.clear()
        self.itemObjectID.clear()
        self.id2obj_dict.clear()        
        
    def __updatecol(self, index, col, val):
        '''
        Update the value in the given column of the current row
        '''
        img = False
        # Look up the column descriptor
        colname = self.colnumbers[col]
        # Look if the column name has been registered in strConvCols
        # and the value needs to be converted to a string somehow
        if colname in self.strConvCols:
            # Convert a datetime object
            if isinstance(val, (datetime.datetime, datetime.date, datetime.time)):
                val = val.strftime(self.strConvCols[colname])
            else:
                try:
                    # Apply the registered converter
                    val = self.strConvCols[colname] % val
                except (ValueError, TypeError):
                    # if failed, show an empty string
                    val = ''
                    # TODO: Log the error
        # Check if column is registered as image column
        elif colname in self.imgCols:
            # Value of column should be True or False
            if val == True:
                # Get the index of the required image in the imagelist
                val = self.img_idx[self.imgCols[colname]]
            else:
                val = -1
            img = True
        # Now insert value
        if img:
            # Set the image for the row and column
            self.SetItemColumnImage(index, col, val)
        else:
            if val == None:
                val = ''
            self.SetStringItem(index, col, _(val))

    def __getSelectedIndices(self, state =  wx.LIST_STATE_SELECTED):
        '''
        Returns a list of item id's of selected items (rows)
        '''
        indices = []
        lastFound = -1
        # Iterates over all selected items, appending
        # each item found to the list of id's
        while True:
            index = self.GetNextItem(
                lastFound,
                wx.LIST_NEXT_ALL,
                state,
            )
            if index == -1:
                break
            else:
                lastFound = index
                indices.append(index)
        return indices

    def __remember(self, obj):
        '''
        Store the given object and return object id
        '''
        # Get object id
        oid = id(obj)
        # Store object in dict id2obj_dict using it's id as key
        self.id2obj_dict[oid] = obj
        return oid
    
    def __id2obj(self, oid):
        '''
        Returns object by id
        '''
        return self.id2obj_dict[oid]
    
    def __updateItemDataMap(self, index, dct):
        '''
        Update the Listview's associated data dictionary
        '''
        # Get the column numbers, starting from 1
        sortedcolumns = sorted(self.colnumbers.keys())[1:]
        # Store dict object by it's id
        oid = self.__remember(dct)
        # Map to itemDataMap index
        self.itemObjectID[index] = oid
        # Get name of first column
        datarow = []
        # Append the dummy value for column 0
        datarow.append('')
        for col in sortedcolumns:
            colname = self.colnumbers[col]
            if colname not in dct:
                val = ''
            else:
                val = dct[colname]
            datarow.append(val)
        # One tablerow of data
        self.itemDataMap[index] = datarow
        
    def __insertTableRow(self, index, values):
        '''
        Insert a new item (row) in the listview
        '''
        # Insert a row and set column 0 with the dummie value
        self.InsertStringItem(index, values[0])
        # Now insert values of remaining columns
        col = 1
        for val in values[1:]:
            try:
                self.__updatecol(index, col, val)
            except (AttributeError, TypeError, ValueError), ex:
                print ex
                # TODO: Log error    
            col += 1
        self.__setbgcolor(index)
        self.SetItemData(index, index)
        
    def __updateTableRow(self, index, values):
        '''
        Updates an item (row) of the view
        '''
        col = 0
        for val in values:
            try:
                self.__updatecol(index, col, val)
            except (AttributeError, TypeError, ValueError), ex:
                print ex
                # TODO: Log error    
            col += 1
        self.__setbgcolor(index)
        self.SetItemData(index, index)
        
    def __setbgcolor(self, index):
        if index % 2:
            self.SetItemBackgroundColour(index, self.evenRowsBackColor)
        else:
            self.SetItemBackgroundColour(index, self.oddRowsBackColor)
            
    def __unselectLines(self):
        for index in self.__getSelectedIndices():
            self.SetItemState(index, 0, wx.LIST_STATE_SELECTED)
        