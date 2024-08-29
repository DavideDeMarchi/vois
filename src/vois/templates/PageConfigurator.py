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
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, page
from vois.templates import template1panel, template2panels, template3panels


LEFT_WIDTH = 400   # Width  in pixels of the left bar

#####################################################################################################################################################
# Interactive page configurator widget
#####################################################################################################################################################
class PageConfigurator(v.Container):
    
    # Initialization
    def __init__(self, output, **kwargs):
        
        super().__init__(**kwargs)
        
        # Initial settings
        settings.dark_mode      = True
        settings.color_first    = '#0d856d'
        settings.color_second   = '#a0dcd0'
        settings.button_rounded = True
        
        self.output = output
        
        self.card = v.Card(flat=True, color='#ccffcc', width=LEFT_WIDTH, min_width=LEFT_WIDTH, max_width=LEFT_WIDTH,height='100px')
        
        self.page = template1panel.template1panel(self.output)
        self.pagecard = self.page.create()

        self.children = [self.card]
        
