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
from vois.vuetify import settings, toggle
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
        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')

        self.card = v.Card(flat=True,
                           #color='#ccffcc',
                           width=LEFT_WIDTH,
                           min_width=LEFT_WIDTH,
                           max_width=LEFT_WIDTH,
                           height='100px',
                           class_='pa-2 pt-4 ma-0')

        # Widgets
        self.panelsLabel  = v.Html(tag='div', children=['Page format: '], class_='pa-0 ma-0 mt-1 mr-3', style_='font-size: 17px; font-weight: 500; color: %s;'%settings.color_first)
        self.togglePanels = toggle.toggle(0,
                                          ['1', '2', '3'],
                                          tooltips=['Page with 1 left panel', 'Page with 2 panels: left and bottom', 'Page with 3 panels: left, bottom and right'],
                                          dark=True, onchange=None, row=True, width=42, justify='start', paddingrow=1, tile=True)

        self.card.children = [widgets.HBox([self.panelsLabel, self.togglePanels.draw()])]
        
        # Initial page
        self.page = template1panel.template1panel(self.output, left_back=True)
        self.pagecard = self.page.create()
        
        self.page.cardLeft.children = [self]

        self.tag = 'div'
        self.children = [self.card]

