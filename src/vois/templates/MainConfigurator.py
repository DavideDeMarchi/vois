"""mainPage Configurator"""
# Author(s): Davide.De-Marchi@ec.europa.eu, Edoardo.Ramalli@ec.europa.eu
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
from ipywidgets import widgets, HTML
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, page

# Local imports
import mainPage


# Panels dimensioning
LEFT_WIDTH = '30vw'


#####################################################################################################################################################
# mainPage Configurator
#####################################################################################################################################################
class MainConfigurator(page.page):


    # Initialization
    def __init__(self, output, onclose=None, leftWidth=LEFT_WIDTH, **kwargs):
        super().__init__('mainPage', 'Visual configurator', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre', left_back=True, **kwargs)

        # Initialize member variables
        self.leftWidth = leftWidth

    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%settings.color_first
        self.main_width  = 'calc(100vw - %s)'%self.leftWidth
        self.main_height = self.height
        self.cardLeft   = v.Card(flat=True, style_=st + 'border-right-width: 0px;', outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardMain   = v.Card(flat=True, style_=st + 'display: flex; justify-content: center; align-items: center;', outlined=True, width=self.main_width, height=self.main_height, color='#eeeeee')
        
        # Creation of the contents for the panels
        self.createMain()
        self.createLeft()
        
        # Compose the panels
        self.card.children = [ widgets.HBox([self.cardLeft, self.cardMain]) ]
        
        return self.card

    
    # Create the content of the left panel
    def createLeft(self):
        pass
    
    # Create the content of the Main panel
    def createMain(self):

        self.main = mainPage.mainPage(background_image=55)
        
        # Display the content inside the main card
        self.cardMain.children = [self.main.preview()]
        
    