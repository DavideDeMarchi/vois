"""Example of resizable SVG drawing to use inside a Content"""
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
from ipywidgets import widgets, HTML, Layout
import ipyvuetify as v
import pandas as pd
import random

# Vois imports
from vois import svgMap
from vois.vuetify import settings, palettePickerEx


#####################################################################################################################################################
# Example of resizable SVG drawing to use inside a Content
#####################################################################################################################################################
class SVGdrawing():
    
    def __init__(self,
                 width='30vw',        # Dimensions of the overall card displaying the SVG
                 height='40vh',
                 color_first=None,    # Main color
                 color_second=None,   # Secondary color
                 dark=None,           # Dark flag
                 **kwargs):
        
        self._width  = width
        self._height = height
        
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

        # Create the card that will contain the SVG drawing
        self.card = v.Card(flat=True, tile=True, width=self._width, height=self._height,
                           style_='overflow: hidden;', class_='d-flex align-center justify-center')  # The content of the card is centered horizontally and vertically
        
        
        # Creation of the SVG displaying the map of Europe
        self.codes_selected = []
        self.df = pd.DataFrame(columns=['iso2code','value','label'])
        for code in svgMap.country_codes:
            value = random.randint(0,100)
            record = {'iso2code': code, 'value': value, 'label': '%d' % value }
            self.df.loc[len(self.df)] = record
            
            selected = random.randint(0,100) >= 90
            if selected:
                self.codes_selected.append(code)
        
        # Palette picker
        self.pp = None
        self.pp = palettePickerEx.palettePickerEx(family='sequential', value='Viridis', interpolate=True, show_interpolate_switch=False, clearable=False, width=200,
                                                  onchange=self.updateChart, show_opacity_slider=False, onchangeOpacity=None)
        
        self.updateChart()
        
        
    # Draw th widget
    def draw(self):
        return self.card
        
        
    # Updte the chart
    def updateChart(self, *args):
        if self.pp is not None and self.pp.colors is not None and len(self.pp.colors) > 1:
            svg = svgMap.svgMapEurope(self.df,
                                      code_column='iso2code',
                                      width=self._width,
                                      height=self._height,
                                      stdevnumber=1.5, 
                                      colorlist=self.pp.colors,
                                      stroke_width=4.0,
                                      stroke_selected='red',
                                      onhoverfill='#f8bd1a',
                                      codes_selected=self.codes_selected,
                                      legendtitle='Legent title',
                                      legendunits='KTOE per 100K inhabit.')

            # Display the SVG inside the card
            self.card.children = [HTML(svg)]
        
        
    # Configure the SVG drawing
    def configure(self):
        return v.Card(flat=True, class_='pa-2 ma-0', children=[self.pp.draw()])


    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = w
        self.updateChart()
        self.card.width = w

        
    @property
    def height(self):
        return self._height
        
    @height.setter
    def height(self, h):
        self._height = h
        self.updateChart()
        self.card.height = h

        
    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        if self.pp is not None:
            self.pp.color = color
    