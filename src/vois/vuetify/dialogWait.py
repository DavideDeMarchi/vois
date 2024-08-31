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
import traitlets
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
    indeterminate : bool, optional
        If True the progress bar will constantly animate (to be used when completion progress is unknown). Default is True.
        If set to False, setting the value property of the dialog (e.g.: dlg.value = 30) to the percentage will change the progress bar.
    height : int, optional
        Height of the progress bar in pixels (default is 4)
    linecolor : str, optional
        Color of the progress bar (default is None, meaning that the progress bar will be white or black depending on settings.dark_mode)
    showtext : bool, optional
        If True the percentage text will be displayed at the center of the progress bar (default is False)
    textcolor : str, optional
        Color of the percentage text displayed if the showtext parameter is True (default is '#cccccc')
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
    
    dialog        = traitlets.Bool(True).tag(sync=True)
    text          = traitlets.Unicode('').tag(sync=True)
    indeterminate = traitlets.Bool(True).tag(sync=True)
    value         = traitlets.Int(40).tag(sync=True)
    height        = traitlets.Int(5).tag(sync=True)
    showtext      = traitlets.Bool(False).tag(sync=True)
    textcolor     = traitlets.Unicode('#cccccc').tag(sync=True)
    color         = traitlets.Unicode(settings.color_first).tag(sync=True)
    dark          = traitlets.Bool(settings.dark_mode).tag(sync=True)
    
    @traitlets.default('template')
    def _template(self):
        darkmode  = ''
        if self.dark:
            darkmode  = 'dark'
            
        if not self.linecolor is None:
            linecolor = self.linecolor
        else:
            linecolor = settings.textcolor_notdark
            if self.dark:
                linecolor = settings.textcolor_dark

        sss = ''
        if self.showtext:
            sss = '''
<template v-slot:default="{ value }">
   <strong style="color: %s;">{{ Math.ceil(value) }}%%</strong>
</template>
''' % self.textcolor
    
        return '''
<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      hide-overlay
      persistent
      width="300"
      style='z-index:20001;'
    >
      <v-card
        color="%s"
        %s
      >
        <v-card-text>
          <br>{{ text }}
          <v-progress-linear
            :indeterminate="indeterminate"
            :value="value"
            :height="height"
            color="%s"
            class="mb-0 mt-2">
            %s
          </v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>''' % (self.color, darkmode, linecolor, sss)
    
    
    def __init__(self, output=None, text='Please wait...', indeterminate=True, height=4, linecolor=None, showtext=False, textcolor='#cccccc',
                 color=settings.color_first, dark=settings.dark_mode, *args, **kwargs):
        
        self.text          = text
        self.indeterminate = indeterminate
        self.height        = height
        self.linecolor     = linecolor
        self.showtext      = showtext
        self.textcolor     = textcolor
        self.color         = color
        self.dark          = dark
        
        self.value         = 0
        
        super().__init__(*args, **kwargs)
        
        if not output is None:
            with output:
                display(self)
       
    
    def close(self):
        """Close the dialogWait."""
        self.dialog = False
