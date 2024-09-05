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
from ipywidgets import widgets
import ipyvuetify as v

# Vois imports
from vois.templates import mapUtils


#####################################################################################################################################################
# Main content of a template1/2/3panels class
#####################################################################################################################################################
class Content(v.Card):

    # Initialization
    def __init__(self,
                 width='50vw',            # Overall width
                 height='50vh',           # Overall height
                 splitmode=0,             # 0=single content,  1=two contents splitted vertically,   2=two contents splitted horizontally,   3=three contents,   4=four contents
                 bordercolor='#006600',   # Color of the splitting borders
                 leftwidthperc=50,        # width in percentage of left column
                 topheightperc=50,        # height in percentage of top row
                 **kwargs):
        
        super().__init__(**kwargs)
        
        self._width         = width
        self._height        = height
        self._splitmode     = splitmode
        self._bordercolor   = bordercolor
        self._leftwidthperc = leftwidthperc
        self._topheightperc = topheightperc
        
        self.card = v.Card(flat=True, color='#eeeeee', tile=True,
                           width=self._width,   min_width=self._width,   max_width=self._width,
                           height=self._height, min_height=self._height, max_height=self._height)
        
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
            self.card1 = v.Card(flag=True, tile=True,
                                width=self._width,   min_width=self._width,   max_width=self._width,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = None
            self.card3 = None
            self.card4 = None
            
            self.card.children = [self.card1]
        
        # 2 horizontal contents
        elif self._splitmode == 1:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
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
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-bottom: 1px solid %s;'%self._bordercolor,
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
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s'%(self._bordercolor,self._bordercolor),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card4 = None
            
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), self.card3])]
            
        # 4 contents
        else:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s'%(self._bordercolor,self._bordercolor),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True, style_='border: 0px solid red; border-bottom: 1px solid %s'%self._bordercolor,
                                width=wr, min_width=wr, max_width=wr,
                                height=ht, min_height=ht, max_height=ht)
            self.card4 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=hb, min_height=hb, max_height=hb)
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), widgets.VBox([self.card3, self.card4])])]
    
    
    
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