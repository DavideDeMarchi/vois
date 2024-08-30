"""Interactive page configurator"""
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
from vois.vuetify import settings, toggle, ColorPicker
from vois.templates import template1panel, template2panels, template3panels


LEFT_WIDTH = 400   # Width  in pixels of the left bar


#####################################################################################################################################################
# Interactive page configurator widget
#####################################################################################################################################################
class PageConfigurator(v.Html):

    # Initialization
    def __init__(self, output, **kwargs):

        super().__init__(**kwargs)

        self.output = output
        #self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        #self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        #self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')

        self.card = v.Card(flat=True, width=LEFT_WIDTH, min_width=LEFT_WIDTH, max_width=LEFT_WIDTH, height='200px', class_='pa-2 pt-4 ma-0')

        # Widgets
        self.panelsLabel  = v.Html(tag='div', children=['Page format: '], class_='pa-0 ma-0 mt-1 mr-3', style_='font-size: 17px; font-weight: 500; color: %s;'%settings.color_first)
        self.togglePanels = toggle.toggle(0,
                                          ['1', '2', '3'],
                                          tooltips=['Page with 1 left panel', 'Page with 2 panels: left and bottom', 'Page with 3 panels: left, bottom and right'],
                                          dark=True, onchange=self.onSelectedTemplate, row=True, width=42, justify='start', paddingrow=1, tile=True)

        self.titlecolor  = ColorPicker(color=settings.color_first,  width=30, height=30, rounded=False, on_change=self.titlecolorChange,  offset_x=True, offset_y=False)        
        self.footercolor = ColorPicker(color=settings.color_second, width=30, height=30, rounded=False, on_change=self.footercolorChange, offset_x=True, offset_y=False)        
        
        self.card.children = [widgets.VBox([
                                widgets.HBox([self.panelsLabel, self.togglePanels.draw()]),
                                self.titlecolor,
                                self.footercolor,
                                ])
                             ]
        
        # Set v.Html members
        self.tag = 'div'
        self.children = [self.card]
        
        # Initial page
        self.page = None
        self.onSelectedTemplate(0)

    
    # Forced close
    def on_force_close(self, *args):
        self.output.clear_output()

        
    # Selection of 1, 2 or 3 panels template
    def onSelectedTemplate(self, index):

        # Default state (back button on the left and JEODPP logo as application logo
        statusdict = {
            'left_back'  : True,
            'logoappurl' : 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/BDAP_Logo1024transparent.png'
        }
        
        # Read the state and close the current page
        if self.page is not None:
            statusdict = self.page.state
            self.page.close()

        # Create the instance of the page with the requested number of panels
        if index == 0:
            self.page = template1panel.template1panel(self.output)
        elif index == 1:
            self.page = template2panels.template2panels(self.output)
        else:
            self.page = template3panels.template3panels(self.output)

        self.page.customButtonAdd('mdi-delete', 'Click here to force page closing', self.on_force_close)
            
        # Create the page widgets and display the PageConfigurator in the left panel
        self.page.create()
        self.page.cardLeft.children = [self]

        # Set the state
        self.page.state = statusdict

        # Open the page with minimal transition
        self.page.transition = 'dialog-top-transition'
        self.page.open()
        if 'transition' in statusdict:
            self.page.transition = statusdict['transition']
        else:
            self.page.transition = 'dialog-bottom-transition'

    
    # Change of the titlecolor property
    def titlecolorChange(self):
        color = self.titlecolor.color

        # page color
        self.page.titlecolor = color
        
        # widgets color
        self.togglePanels.colorselected = color
                
        # labels color
        self.panelsLabel.style_ = 'font-size: 17px; font-weight: 500; color: %s;'%color
        
        
    # Change of the footercolor property
    def footercolorChange(self):
        color = self.footercolor.color
        
        # page color
        self.page.footercolor = color

        # widgets color
        self.togglePanels.colorunselected = color
        