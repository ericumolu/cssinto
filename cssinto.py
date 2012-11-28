#!/usr/local/bin/python3.1

#    This file is part of cssinto.
#
#    cssinto is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    cssinto is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import sys
import fileinput
import re

class CssValue:
    def __init__(self, value):
        self.value = value.strip()

    def show(self):
        return self.value

class CssProperty:
    def __init__(self,property,declaration_full):
        self.value_pattern = ':(.+);'
        self.value_split_pattern = '\ *'
        self.value_split = ' '
        self.close = ";"
        self.value = []
        self.declaration_full = declaration_full
        self.property = property

        self.set_value()
    def set_value(self,value="",pos=-1):
        if not value:
            value = re.findall(self.value_pattern,self.declaration_full)[0]
        
        value = value.strip()

        if pos > -1:
            if pos > (len(self.value) - 1):
                self.value.append(CssValue(value))
            else:
                self.value[pos] = CssValue(value)
        else:
            self.value = []
            for vl in re.split(self.value_split_pattern,value):
                self.value.append(CssValue(vl))

    #return this properties values
    def show_value(self):
        value_all = []
        for value in self.value:
            value_all.append(value.show())

        return self.value_split.join(value_all) + self.close

class CssBody:
    def __init__(self,body_full):
        self.open = "{"
        self.close = "}"
        self.declaration_split = ":"
        self.end_of_line = ";"
        self.declaration_pattern = '\ *[\w\-]+\ *:[\'\"\w#%\.\ -]+;?'
        self.property_pattern = '(.+):'
        self.property_split = '\n'
        self.property_pre = '\t'
        self.property = {}
        self.body_full = body_full
        self.add_property()

    def add_property(self,property=""):
        for declaration in re.findall(self.declaration_pattern,self.body_full):
            property = re.findall(self.property_pattern,declaration)[0]
            property = property.strip()
            self.property[property] = CssProperty(property,declaration)

    def get_property(self,property):
        return self.property.get(property,None)

    #return this body property
    def show_property(self):
        property_all = []
        property_all.append(self.open)

        for property in self.property:
            property_all.append(self.property_pre + property + self.declaration_split + self.property[property].show_value())
        
        property_all.append(self.close)

        return self.property_split.join(property_all)


class CssSelectorUnit:
    def __init__(self,unit):
        self.count = 0
        self.pseudo_element = ""
        unit = unit.strip()
        if not unit[0].isalpha():
            self.type = unit[0]
            self.name = unit[1:]
        else:
            self.type = ""
            self.name = unit

    def show(self):
        return self.type + self.name

class CssSelector:
    def __init__(self,selector_full):
        self.unit = []
        self.selector_full = selector_full.strip()
        self.unit_split = ' '
        self.add_unit()

    def add_unit(self):
        for unit in re.split('\ *',self.selector_full):
            self.unit.append(CssSelectorUnit(unit))

    def show_unit(self):
        unit_name = []
        for unit in self.unit:
            unit_name.append(unit.show())
        return self.unit_split.join(unit_name)
            
class CssBlock:
    def __init__(self,block_full):
        self.selector_pattern = '([:\w#\.,\ ]+)\{'
        self.declaration_pattern_all = '{(.+)}'
        self.selector_split = ','
        self.body = None
        self.selector_body_split = '\n'

        self.selector = []
        self.block_full = block_full
    
        self.add_selector()
        self.add_body()

    def add_selector(self,selector_all=""):
        if not selector_all:
            selector_all = re.findall(self.selector_pattern,self.block_full)[0]
        for selector in selector_all.split(self.selector_split):
            self.selector.append(CssSelector(selector))

    def change_selector(self,selector_loc):
        pass

    def show_selector(self,selector_list = None):
        selector_show = []
        
        if selector_list == None:
            selector_list = self.selector

        for selector in selector_list:
                selector_show.append(selector.show_unit())

        return self.selector_split.join(selector_show)

    def show_body(self):
        return self.body.show_property()

    def add_body(self):
        declaration_all = re.findall(self.declaration_pattern_all,self.block_full)[0]
        self.body = CssBody(declaration_all)

    def get_body(self):
        return self.body

class Css:
    def __init__(self):
        self.block_pattern = '[:\w#\.,\ ]+\{(?:\ *[\w\-]+\ *:[\'\"\w#%\.\ -]+;?)+}'
        self.whitespace_pattern = '[\t\n\r\f\v]'

        self.css_full = ""
        self.block_sep = '\n' 
        self.block_spacer = 2

        self.block = []

    def set_css_full(self, css_full):
        self.css_full = re.sub(self.whitespace_pattern,'',css_full)

    def add_block(self):
        split = re.findall(self.block_pattern,self.css_full)
        for block in split:
            self.block.append(CssBlock(block))

    def read(self,file=""):
        css_file = open(file,'r')

        css_full = ""

        for line in css_file:
            css_full += line    

        self.set_css_full(css_full)

    def show_block(self,block_list = None):
        block_all = []
    
        if block_list == None:
            block_list = self.block

        for block in block_list:
            block_all.append(block.show_selector() + self.block_sep + block.show_body())

        block_all = (self.block_sep * self.block_spacer).join(block_all)

        return block_all

    def get_block_selector(self,selector):
        match = []
        for block in self.block:
            if selector == block.show_selector():
                match.append(block)
        return match
            
    def get_block(self,index):
        return self.block[index]
