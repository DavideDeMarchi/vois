"""Main content of the template1/2/3panels classes"""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2024
# 
# Licensed under the EUPL, Version 1.2 or as soon they will be approved by 
# the European Commission subsequent versions of the EUPL (the "Licence");
# 
# You may not use this work except in compliance with the Licence.
# 
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS"
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# 
# See the Licence for the specific language governing permissions and
# limitations under the Licence.

# Imports
from ipywidgets import widgets, Layout
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings
from vois.geo import Map, mapUtils
from vois.templates import PlotlyChart, SVGdrawing


#####################################################################################################################################################
# Main content of a template1/2/3panels class
#####################################################################################################################################################
class Content(v.Card):

    # Initialization
    def __init__(self,
                 output,
                 width='50vw',            # Overall width
                 height='50vh',           # Overall height
                 splitmode=0,             # 0=single content,  1=two contents splitted vertically,   2=two contents splitted horizontally,   3=three contents,   4=four contents
                 bordercolor='#006600',   # Color of the splitting borders
                 leftwidthperc=50,        # width in percentage of left column
                 topheightperc=50,        # height in percentage of top row
                 color_first=None,        # Main color
                 color_second=None,       # Secondary color
                 dark=None,               # Dark flag
                 **kwargs):
        
        super().__init__(**kwargs)
        
        self.output         = output
        self._width         = width
        self._height        = height
        self._splitmode     = splitmode
        self._bordercolor   = bordercolor
        self._leftwidthperc = leftwidthperc
        self._topheightperc = topheightperc
        
        # Colors of the configuration widgets
        self._color_first = color_first
        if self._color_first is None:
            self._color_first = settings.color_first
        
        self._color_second = color_second
        if self._color_second is None:
            self._color_second = settings.color_second
            
        self._dark = dark
        if self._dark is None:
            self._dark = settings.dark_mode

        # Main card
        self.card = v.Card(flat=True, color='#ffffff', tile=True,
                           width=self._width,   min_width=self._width,   max_width=self._width,
                           height=self._height, min_height=self._height, max_height=self._height)
        
        self.card1 = self.card2 = self.card3 = self.card4 = None
        self.card1children = self.card2children = self.card3children = self.card4children = None
        
        self.set1(Map.Map())
        self.update()
        
        self.children = [self.card]
        
    
    # Returns the vuetify object to display (the v.Card)
    def draw(self):
        return self
    
    
    # Update the content when splitmode is changed
    def update(self):

        wl = 'calc(%s * %f)'%(self._width, self._leftwidthperc/100)
        wr = 'calc(%s * %f)'%(self._width, (100 - self._leftwidthperc)/100)
        ht = 'calc(%s * %f)'%(self._height, self._topheightperc/100)
        hb = 'calc(%s * %f)'%(self._height, (100 - self._topheightperc)/100)
        
        # Single content
        if self._splitmode == 0:
            self.card1 = v.Card(flag=True, tile=True, style_='overflow: hidden;',
                                width=self._width,   min_width=self._width,   max_width=self._width,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = None
            self.card3 = None
            self.card4 = None
            
            self.card.children = [self.card1]
        
        # 2 horizontal contents
        elif self._splitmode == 1:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; overflow: hidden;'%self._bordercolor,
                                width=wl, min_width=wl, max_width=wl,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = v.Card(flag=True, tile=True, 
                                width=wr, min_width=wr, max_width=wr,
                                height=self._height, min_height=self._height, max_height=self._height)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.HBox([self.card1, self.card2])]
            
            
        # 2 vertical contents
        elif self._splitmode == 2:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-bottom: 1px solid %s; overflow: hidden;'%self._bordercolor,
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, 
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=hb, min_height=hb, max_height=hb)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.VBox([self.card1, self.card2])]

        # 2 vertical contents + 1 on the right at full height
        elif self._splitmode == 3:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s; overflow: hidden;'%(self._bordercolor,self._bordercolor),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; overflow: hidden;'%self._bordercolor,
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card4 = None
            
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), self.card3])]
            
        # 4 contents
        else:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s; overflow: hidden;'%(self._bordercolor,self._bordercolor),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; overflow: hidden;'%self._bordercolor,
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True, style_='border: 0px solid red; border-bottom: 1px solid %s; overflow: hidden;'%self._bordercolor,
                                width=wr, min_width=wr, max_width=wr,
                                height=ht, min_height=ht, max_height=ht)
            self.card4 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=hb, min_height=hb, max_height=hb)
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), widgets.VBox([self.card3, self.card4])])]
    
        
        self.set1(self.card1children)
        self.set2(self.card2children)
        self.set3(self.card3children)
        self.set4(self.card4children)
    
    
    # Set the content of cards 1,2,3,4 (can pass None or a widget that has width and height properties
    def set1(self, children=None):
        self.card1children = children
        if self.card1 is not None:
            if self.card1children is None:
                self.card1.children = []
            else:
                self.card1children.width  = 'calc(%s - 1px)'%self.card1.width
                self.card1children.height = 'calc(%s - 1px)'%self.card1.height
                self.card1.children = [self.card1children.draw()]
    
    def set2(self, children=None):
        self.card2children = children
        if self.card2 is not None:
            if self.card2children is None:
                self.card2.children = []
            else:
                self.card2children.width  = 'calc(%s - 1px)'%self.card2.width
                self.card2children.height = 'calc(%s - 1px)'%self.card2.height
                self.card2.children = [self.card2children.draw()]
    
    def set3(self, children=None):
        self.card3children = children
        if self.card3 is not None:
            if self.card3children is None:
                self.card3.children = []
            else:
                self.card3children.width  = 'calc(%s - 1px)'%self.card3.width
                self.card3children.height = 'calc(%s - 1px)'%self.card3.height
                self.card3.children = [self.card3children.draw()]
    
    def set4(self, children=None):
        self.card4children = children
        if self.card4 is not None:
            if self.card4children is None:
                self.card4.children = []
            else:
                self.card4children.width  = 'calc(%s - 1px)'%self.card4.width
                self.card4children.height = 'calc(%s - 1px)'%self.card4.height
                self.card4.children = [self.card4children.draw()]
                
                
    #####################################################################################################################################################
    # Properties
    #####################################################################################################################################################
    
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = w
        self.card.width = self._width
        self.card.min_width = self._width
        self.card.max_width = self._width

        
    @property
    def height(self):
        return self._height
        
    @height.setter
    def height(self, h):
        self._height = h
        self.card.height = self._height
        self.card.min_height = self._height
        self.card.max_height = self._height

        
    @property
    def splitmode(self):
        return self._splitmode
        
    @splitmode.setter
    def splitmode(self, sm):
        self._splitmode = int(sm)
        self.update()

        
    @property
    def bordercolor(self):
        return self._bordercolor
        
    @bordercolor.setter
    def bordercolor(self, bc):
        self._bordercolor = bc
        self.update()

        
    @property
    def leftwidthperc(self):
        return self._leftwidthperc
        
    @leftwidthperc.setter
    def leftwidthperc(self, w):
        self._leftwidthperc = min(100, max(w, 0))
        self.update()

        
    @property
    def topheightperc(self):
        return self._topheightperc
        
    @topheightperc.setter
    def topheightperc(self, h):
        self._topheightperc = min(100, max(h, 0))
        self.update()
        
        
    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        if self.card1children is not None: self.card1children.color_first = self._color_first
        if self.card2children is not None: self.card2children.color_first = self._color_first
        if self.card3children is not None: self.card3children.color_first = self._color_first
        if self.card4children is not None: self.card4children.color_first = self._color_first


    @property
    def color_second(self):
        return self._color_second
        
    @color_second.setter
    def color_second(self, color):
        self._color_second = color

        if self.card1children is not None: self.card1children.color_second = self._color_second
        if self.card2children is not None: self.card2children.color_second = self._color_second
        if self.card3children is not None: self.card3children.color_second = self._color_second
        if self.card4children is not None: self.card4children.color_second = self._color_second

    @property
    def dark(self):
        return self._dark
        
    @dark.setter
    def dark(self, flag):
        self._dark = flag
        
        if self.card1children is not None: self.card1children.dark = self._dark
        if self.card2children is not None: self.card2children.dark = self._dark
        if self.card3children is not None: self.card3children.dark = self._dark
        if self.card4children is not None: self.card4children.dark = self._dark
