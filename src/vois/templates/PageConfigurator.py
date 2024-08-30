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
from vois import colors
from vois.vuetify import settings, toggle, ColorPicker
from vois.templates import template1panel, template2panels, template3panels


LEFT_WIDTH = 400   # Width  in pixels of the left bar


# Change style of a label
def labelchange(lab, size=14, weight=400, color=settings.color_first, width=None):
    if width is None:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s;'%(size,weight,color)
    else:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s; width: %dpx'%(size,weight,color,int(width))
    
# Creation of a label
def label(text, class_='pa-0 ma-0 mt-1 mr-3', size=14, weight=400, color=settings.color_first, width=None):
    lab = v.Html(tag='div', children=[text], class_=class_)
    labelchange(lab, size, weight, color, width)
    return lab

    
#####################################################################################################################################################
# Interactive page configurator widget
#####################################################################################################################################################
class PageConfigurator(v.Html):

    # Initialization
    def __init__(self, output, **kwargs):

        super().__init__(**kwargs)

        self.output = output
        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')

        self.card = v.Card(flat=True, width=LEFT_WIDTH, min_width=LEFT_WIDTH, max_width=LEFT_WIDTH, height='200px', class_='pa-2 pt-4 ma-0')

        # Widgets
        self.labelwidth   = 110
        self.togglewidth  = 50
        self.paddingrow   = 1
        self.biglabelsize = 17
        
        self.panelsLabel  = label('Page format: ', size=self.biglabelsize, weight=500, width=self.labelwidth)
        self.togglePanels = toggle.toggle(0,
                                          ['1', '2', '3'],
                                          tooltips=['Page with 1 left panel', 'Page with 2 panels: left and bottom', 'Page with 3 panels: left, bottom and right'],
                                          dark=True, onchange=self.onSelectedTemplate, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)

        
        self.titlecolor  = ColorPicker(color=settings.color_first,  width=80, height=30, rounded=False, on_change=self.titlecolorChange,  offset_x=True, offset_y=False)        
        self.footercolor = ColorPicker(color=settings.color_second, width=80, height=30, rounded=False, on_change=self.footercolorChange, offset_x=True, offset_y=False)        
        
        self.titledark = toggle.toggle(0, ['', '', ''], dark=True, icons=['mdi-alpha-w-box-outline', 'mdi-alpha-b-box-outline', 'mdi-auto-fix'],
                                       tooltips=['Display text in white color on the title bar', 'Display text in black color on the title bar', 'Automatically select text color for the title bar'],
                                       onchange=self.titledarkChange, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)

        self.footerlinked = toggle.toggle(0, ['', '', ''], dark=True, icons=['mdi-link-off', 'mdi-link-variant', 'mdi-link-variant-minus'],
                                          tooltips=['Free selection of footer color', 'Footer color is the complementary of the title color', 'Footer color is the monochrome complementary of the title color'],
                                          onchange=self.footerlinkedChange, row=True, width=self.togglewidth-16, height=30, justify='start', paddingrow=self.paddingrow, tile=True)
        
        self.footerdark = toggle.toggle(1, ['', '', ''], dark=True, icons=['mdi-alpha-w-box-outline', 'mdi-alpha-b-box-outline', 'mdi-auto-fix'],
                                        tooltips=['Display text in white color on the footer bar', 'Display text in black color on the footer bar', 'Automatically select text color for the footer bar'],
                                        onchange=self.footerdarkChange, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)
        
        self.card.children = [widgets.VBox([
                                widgets.HBox([self.panelsLabel, self.togglePanels.draw()]),
                                self.spacerY,
                                self.spacerY,
                                widgets.HBox([label('Title bar color:',  color='black', width=self.labelwidth), self.titlecolor, self.spacerX, label('Link:', color='black', width=30), self.footerlinked.draw()]),
                                self.spacerY,
                                widgets.HBox([label('Footer bar color:', color='black', width=self.labelwidth), self.footercolor]),
                                self.spacerY,
                                widgets.HBox([label('Title bar text:',   color='black', width=self.labelwidth), self.titledark.draw()]),
                                self.spacerY,
                                widgets.HBox([label('Footer bar text:',  color='black', width=self.labelwidth), self.footerdark.draw()]),
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
        self.page.toggleBasemap.colorselected = color
        self.togglePanels.colorselected       = color
        self.titledark.colorselected          = color
        self.footerdark.colorselected         = color
        self.footerlinked.colorselected       = color
        self.titledarkChange(self.titledark.value)
                
        # labels color
        labelchange(self.panelsLabel, size=self.biglabelsize, weight=500, color=color, width=self.labelwidth)
        
        # Auto calculate footer color
        if self.footerlinked.index == 1:     # complementary
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            complementary = colors.complementary(colortuple)
            self.footercolor.color = colors.rgb2hex(complementary)

        elif self.footerlinked.index == 2:   # monochrome lighter
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            monochrome = colors.lighter(colortuple, 0.6)
            self.footercolor.color = colors.rgb2hex(monochrome)
        
        
    # Change of the footercolor property
    def footercolorChange(self):
        color = self.footercolor.color
        
        # page color
        self.page.footercolor = color

        # widgets color
        self.page.toggleBasemap.colorunselected = color
        self.togglePanels.colorunselected       = color
        self.titledark.colorunselected          = color
        self.footerdark.colorunselected         = color
        self.footerlinked.colorunselected       = color
        self.footerdarkChange(self.footerdark.value)
                
        
    # Change of the titledark property
    def titledarkChange(self, index):

        # White text color
        if index == 0:
            self.page.titledark          = True
            self.togglePanels.dark       = True
            self.titledark.dark          = True
            self.footerdark.dark         = True
            self.footerlinked.dark       = True
            self.page.toggleBasemap.dark = True
        
        # Black text color
        elif index == 1:
            self.page.titledark          = False
            self.togglePanels.dark       = False
            self.titledark.dark          = False
            self.footerdark.dark         = False
            self.footerlinked.dark       = False
            self.page.toggleBasemap.dark = False
        
        # Auto color depending on title bar color
        else:
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            if colors.isColorDark(colortuple):
                self.page.titledark          = True
                self.togglePanels.dark       = True
                self.titledark.dark          = True
                self.footerdark.dark         = True
                self.footerlinked.dark       = True
                self.page.toggleBasemap.dark = True
            else:
                self.page.titledark          = False
                self.togglePanels.dark       = False
                self.titledark.dark          = False
                self.footerdark.dark         = False
                self.footerlinked.dark       = False
                self.page.toggleBasemap.dark = False

                
    # Change of the footerdark property
    def footerdarkChange(self, index):

        # White text color
        if index == 0:
            self.page.footerdark = True
        
        # Black text color
        elif index == 1:
            self.page.footerdark = False
        
        # Auto color depending on title bar color
        else:
            color = self.footercolor.color
            colortuple = colors.string2rgb(color)
            if colors.isColorDark(colortuple):
                self.page.footerdark = True
            else:
                self.page.footerdark = False
                
                
    # Change of the footerlinked toggle
    def footerlinkedChange(self, index):
        self.footercolor.disabled = index > 0
        self.titlecolorChange()