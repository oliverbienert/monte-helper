# -*- coding: utf-8 -*-
'''
Created on Jul 6, 2012

@author: oliver
'''

import os
import errno
import sys
import re

class Helpers(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.emptystr = re.compile(r'^[ \t]*$', re.U)
        
    def if_empty(self, val):
        v = '%s' % val
        match = self.emptystr.match(v)
        if match:
            return True
        else:
            return False

    def valuePercent(self, value):
        '''
        Formats and returns a given value as a percent value
        @param value: Value to be formatted
        @type value: int
        @return: Formatted string with percent sign
        @rtype: string  
        '''
        if value > 0:
            value *= 100
            ret = "%d %%" % value
        else:
            ret = ""
        return ret
        
    def to_euro(self, value):
        '''
        Formats and returns a given value as a currency value (€).
        Float values will be cast to integer.
        @param value: Value to be formatted
        @type value: float
        @return: Formatted string with euro sign
        @rtype: string  
        '''
        try:
            v = int(value)
            ret = u"%d €" % v
        except (ValueError, TypeError):
            ret = ""
        return ret
    
    def make_sure_path_exists(self, path):
        '''
        Creates a given path if it does not exist.
        
        @param path: Path to be created.
        @type path: string 
        '''
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        
    def find_key(self, dct, val):
        '''
        Return the first key found for a given value in the given dictionary.
        
        @param dct: Dictionary to be searched.
        @type dct: Dictionary
        @param val: Value to be searched for.  
        @return: Key found  
        '''
        return [k for k, v in dct.iteritems() if v == val][0]
    
    def converttoint(self, val):
        '''
        Try to convert a value to an integer. If conversion fails,
        return the unchanged value.
        @param val: Value to changed.
        @return: Value as integer or unchanged value. 
        '''
        try:
            val = int(val)
        except (ValueError, TypeError):
            pass
        return val
    
    def read_from_file(self, filename):
        '''
        Read file from given path a returns file content as string.
        @param filename: File to be read.
        @type filename: string
        @return: Content of file
        @rtype: string 
        '''
        # Get module directory
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS  #@UndefinedVariable
        else:
            basedir = os.path.dirname(__file__)
        # Open and read statement from file
        with open(os.path.join(basedir, filename), 'r') as fh:
            content = fh.read()
        # return statement as string
        return content          
    
