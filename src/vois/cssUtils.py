"""CSS utility functions to ensure Voila' behaviour is coherent with JupyterLab."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2024
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
from ipywidgets import HTML
from IPython.display import display
from IPython.display import HTML as ipyHTML
import ipyvuetify as v

from vois.vuetify import settings, iconButton


###########################################################################################################################################################################
# V.I. Avoid left margin in Output widgets inside dialog-boxes!!!
###########################################################################################################################################################################
def dialogBoxesLeftMargin(output=None):
    
    command = '''
<style>.jp-OutputPrompt {
    flex: 0 0 0 !important;
    display: inline !important;
    min-width: 0 !important;
}
</style>'''
    
    if output is None:
        display(HTML(command))
    else:
        with output:
            display(HTML(command))

            

###########################################################################################################################################################################
# Settings for popup when clicking on map: popup is correctly displayed also in Voila'
###########################################################################################################################################################################
def popupDisplay(output=None):

    command = '''
<style>
.leaflet-popup-tip {
    width: 17px !important;
    height: 17px !important;
    padding: 1px !important;
    margin: -10px auto 0 !important;
    -webkit-transform: rotate(45deg) !important;
    -moz-transform: rotate(45deg) !important;
    -ms-transform: rotate(45deg) !important;
    transform: rotate(45deg) !important;
}

.leaflet-popup-content-wrapper, .leaflet-popup-tip {
    background: #fff;
    color: #333;
    box-shadow: 0 3px 14px rgba(0,0,0,0.4);
}

.leaflet-popup-content-wrapper {
    padding: 1px !important;
    text-align: left !important;
    border-radius: 12px !important;
}
</style>'''

    if output is None:
        display(HTML(command))
    else:
        with output:
            display(HTML(command))

            
            
###########################################################################################################################################################################
# Change default font-size of the labels of the vuetify Switch widget
###########################################################################################################################################################################
def switchFontSize(output=None, size=14):
    
    command = '''
<style>.vuetify-styles .v-label {
    font-size: %dpx;
}
</style>'''%int(size)
    
    if output is None:
        display(HTML(command))
    else:
        with output:
            display(HTML(command))

    
###########################################################################################################################################################################
# Execute all settings by displaying all the <style> instructions
###########################################################################################################################################################################
def allSettings(output=None):
    dialogBoxesLeftMargin(output)
    popupDisplay(output)
    
    
    
###########################################################################################################################################################################
# Copy text to clipboard
###########################################################################################################################################################################
def copyToClipboard(txt, output=None):
    command = '''
<script>
    navigator.clipboard.writeText('%s').then(function() {
    console.log('Copying to clipboard was successful!');
  }, function(err) {
    console.error('Could not copy text: ', err);
  });    
</script>'''%(txt)
    
    if output is None:
        display(ipyHTML(command))
    else:
        with output:
            display(ipyHTML(command))
