"""Dialog-box to display a message to the user during a lenghty operation."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2023
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
from traitlets import *
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
except:
    import settings

    
#####################################################################################################################################################
# Wait dialog for lenghty operations
# Example of usage:
#
# from ipywidgets import HTML, widgets, Layout
# 
# out = widgets.Output()
# display(out)
#
# dlg = dialogWait(out=out, text='Please wait for data loading...')
# with out:
#     display(dlg)
#
# dlg.close()
#####################################################################################################################################################
class dialogWait(v.VuetifyTemplate):
    """
    Dialog-box to display a message to the user during a lenghty operation.
        
    Parameters
    ----------
    text : str, optional
        Text to display on top of the dialog-box body (default is '')
    output : ipywidgets.Output, optional
        Output widget on which the widget has to be displayed
            
    Example
    -------
    Creation and display of dialogWait during a lenghty operation::
        
        from vois.vuetify import dialogWait
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        dlg = dialogWait.dialogWait(text='Please wait for processing to terminate...',
                                    output=output)

    .. figure:: figures/dialogWait.png
       :scale: 100 %
       :alt: dialogYesNo widget

       Example of a dialogWait opened during a lenghty operation.
   """
    
    dialog = Bool(True).tag(sync=True)
    text = Unicode('').tag(sync=True)
    
    darkmode  = ''
    linecolor = settings.textcolor_notdark
    if settings.dark_mode:
        darkmode  = 'dark'
        linecolor = settings.textcolor_dark
    
    template = Unicode('''
<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="%s"
        %s
      >
        <v-card-text>
          <br>{{ text }}
          <v-progress-linear
            indeterminate
            color="%s"
            class="mb-0 mt-2"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>''' % (settings.color_first, darkmode, linecolor) ).tag(sync=True)
    
    
    def __init__(self, output=None, text='Please wait...', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        if not output is None:
            with output:
                display(self)
       
    def close(self):
        """Close the dialogWait."""
        self.dialog = False
