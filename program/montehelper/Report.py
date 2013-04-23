# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2012

@author: oliver
'''

import sys, os
import tempfile
import webbrowser
import shutil
from lxml import etree
from datetime import datetime
from Helpers import Helpers
from operator import itemgetter

if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS  #@UndefinedVariable
else:
    basedir = os.path.dirname(__file__)
    
class Report(Helpers):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Helpers.__init__(self)
    
    def createQAReport(self, children, isodate):
        xml_root = etree.Element('root')
        xml_title = etree.SubElement(xml_root, 'title')
        xml_title.text = u"Namens- und Adressliste der Kita- und Hortkinder für die Stichtagsmeldung"
        xml_date = etree.SubElement(xml_root, 'date')
        xml_date.text = isodate
        xml_fee = etree.SubElement(xml_root, 'children')
        children.sort(key=itemgetter('year_id','name','firstname'))
        for child in children:
            xml_child = etree.SubElement(xml_fee, 'child')
            for k, v in child.items():
                elem = etree.SubElement(xml_child, k)
                if k == 'birthdate':
                    v = v.strftime('%d.%m.%Y')
                elem.text = "%s" % v
        self.__createHTMLFile(xml_root, 'qa.xsl')
        
    def createFeeReport(self, **params):
        # The address
        xml_root = etree.Element('root')
        xml_title = etree.SubElement(xml_root, 'title')
        xml_title.text = "Elternbeitragsrechnung"
        xml_today = etree.SubElement(xml_root, 'today')
        xml_today.text = datetime.now().strftime('%d.%m.%Y')
        xml_validfromdate = etree.SubElement(xml_root, 'validfromdate')
        xml_validfromdate.text = params['validfromdate'].strftime('%d.%m.%Y')
        xml_address = etree.SubElement(xml_root, "address")
        for item in params['receiver'].split("\n"):
            row = etree.SubElement(xml_address, 'row')
            row.text = item
        xml_fee = etree.SubElement(xml_root, 'fee')
        for child in params['fees']:
            xml_child = etree.SubElement(xml_fee, 'child')
            for k, v in child.items():
                elem = etree.SubElement(xml_child, k)
                if k in ('reduction1', 'reduction2'):
                    v = self.valuePercent(v)
                elif k in ('income', 'benefit', 'incomeapplied', 'fee'):
                    v = self.to_euro(v)
                elem.text = "%s" % v
        xml_income = etree.SubElement(xml_root, 'income')
        for adult in params['income']:
            xml_adult = etree.SubElement(xml_income, 'adult')
            for k, v in adult.items():
                elem = etree.SubElement(xml_adult, k)
                if k in ('salary', 'income', 'unemployment', 'childsupport', 'misc', 'less', 'totalincome'):
                    v = self.to_euro(v)
                elem.text = "%s" % v
        xml_notes = etree.SubElement(xml_root, 'notes')
        xml_notes.text = params['notes']
        self.__createHTMLFile(xml_root, 'fee.xsl')
        # xml_serialized = etree.tostring(xml_root, xml_declaration=True, encoding='utf-8', pretty_print=True)   
        # self.__writeXMLFile(xml_serialized)
        
    def __createHTMLFile(self, xml_root, stylesheet):
        xslt_file = os.path.join(basedir, 'xsl', stylesheet)
        xslt_root = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_root)
        html_root = transform(xml_root)
        html = etree.tostring(html_root, method = 'html', encoding='utf-8', pretty_print=True)
        self.__openHTMLFile(html)
        
    def __openHTMLFile(self, xml_serialized):
        tmp_dir = tempfile.gettempdir()
        mytmpdir = os.path.join(tmp_dir, '.montehelper')
        self.make_sure_path_exists(mytmpdir)
        # Copy default.css to temp dir
        shutil.copy(os.path.join(basedir, 'xsl/default.css'), os.path.join(mytmpdir, 'default.css'))
        tmp_file = tempfile.NamedTemporaryFile(dir=mytmpdir, suffix='.html', delete=False)
        tmp_file.write(xml_serialized)
        tmp_file.close()
        url = "file://" + tmp_file.name
        webbrowser.open(url,new=2)
        
        
        
        
        
        
        
