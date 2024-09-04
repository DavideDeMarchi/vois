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
    def __init__(self, width='50vw', height='50vh', splitmode=0, bordercolor='#006600', **kwargs):
        
        super().__init__(**kwargs)
        
        self._width       = width
        self._height      = height
        self._splitmode   = splitmode
        self._bordercolor = bordercolor
        
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
            w = 'calc(%s / 2)'%self._width
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
                                width=w, min_width=w, max_width=w,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = v.Card(flag=True, tile=True,
                                width=w, min_width=w, max_width=w,
                                height=self._height, min_height=self._height, max_height=self._height)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.HBox([self.card1, self.card2])]
            
            
        # 2 vertical contents
        elif self._splitmode == 2:
            h = 'calc(%s / 2)'%self._height
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-bottom: 1px solid %s;'%self._bordercolor,
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=h, min_height=h, max_height=h)
            self.card2 = v.Card(flag=True, tile=True, 
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=h, min_height=h, max_height=h)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.VBox([self.card1, self.card2])]

        # 2 vertical contents + 1 on the right at full height
        elif self._splitmode == 3:
            w = 'calc(%s / 2)'%self._width
            h = 'calc(%s / 2)'%self._height
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s'%(self._bordercolor,self._bordercolor),
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
            self.card3 = v.Card(flag=True, tile=True,
                                width=w, min_width=w, max_width=w,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card4 = None
            
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), self.card3])]
            
        # 4 contents
        else:
            w = 'calc(%s / 2)'%self._width
            h = 'calc(%s / 2)'%self._height
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s; border-bottom: 1px solid %s'%(self._bordercolor,self._bordercolor),
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: 1px solid %s;'%self._bordercolor,
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
            self.card3 = v.Card(flag=True, tile=True, style_='border: 0px solid red; border-bottom: 1px solid %s'%self._bordercolor,
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
            self.card4 = v.Card(flag=True, tile=True,
                                width=w, min_width=w, max_width=w,
                                height=h, min_height=h, max_height=h)
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
        