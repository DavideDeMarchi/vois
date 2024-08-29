"""Custom sample page with left and bottom panels"""
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
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, iconButton


#####################################################################################################################################################
# Dynamic button to open and close a panel
#####################################################################################################################################################
class dynamicButton():
    
    def __init__(self,
                 icon1='mdi-menu-left',
                 icon2='mdi-menu-right',
                 color1=settings.color_first,
                 color2=settings.color_first,
                 tooltip1='Close panel',
                 tooltip2='Open panel',
                 x1='10vw', y1='10vh',
                 x2='1vw',  y2='10vh',
                 onclick1=None,
                 onclick2=None):
        
        self.icon1    = icon1
        self.icon2    = icon2
        self.color1   = color1
        self.color2   = color2
        self.tooltip1 = tooltip1
        self.tooltip2 = tooltip2
        self.x1       = x1
        self.y1       = y1
        self.x2       = x2
        self.y2       = y2
        self.onclick1 = onclick1
        self.onclick2 = onclick2
        
        self.ib = iconButton.iconButton(icon=self.icon1, onclick=self.onclick, large=True, tooltip=self.tooltip1)
        
        self.nav = v.NavigationDrawer(stateless=True, permanent=True, floating=True, fixed=True, left=True, color="transparent", width=50, height=50,
                                      style_='left: %s; top: %s; z-index:1000;'%(self.x1, self.y1), class_='pa-0 ma-0', children=[self.ib.draw()])
        self.pos1 = True

        
    def draw(self):
        return self.nav
    
    
    def onclick(self):
        self.pos1 = not self.pos1
        self.setpos()
        
        
    def setpos(self):
        if self.pos1:
            self.nav.style_      = 'left: %s; top: %s; z-index:1000;'%(self.x1, self.y1)
            self.ib.tooltip      = self.tooltip1
            self.ib.btn.children = [v.Icon(children=[self.icon1], large=self.ib.large, small=self.ib.small, x_large=self.ib.x_large, x_small=self.ib.x_small)]
            self.ib.btn.color    = self.color1
            if not self.onclick2 is None: self.onclick2()
        else:
            self.nav.style_      = 'left: %s; top: %s; z-index:1000;'%(self.x2, self.y2)
            self.ib.tooltip      = self.tooltip2
            self.ib.btn.children = [v.Icon(children=[self.icon2], large=self.ib.large, small=self.ib.small, x_large=self.ib.x_large, x_small=self.ib.x_small)]
            self.ib.btn.color    = self.color2
            if not self.onclick1 is None: self.onclick1()

    @property
    def color(self):
        return self.color1
        
    @color.setter
    def color(self, c):
        self.color1 = c
        self.color2 = c
        self.ib.btn.color = c