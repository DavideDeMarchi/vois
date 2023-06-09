"""Radio buttons to allow users to select from a predefined set of options."""
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
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
    from . import tooltip
except:
    import settings
    import tooltip


#####################################################################################################################################################
# Radio control
#####################################################################################################################################################
class radio:
    """
    Radio buttons to allow users to select from a predefined set of options.
        
    Parameters
    ----------
    index : int
        Index of the option initially selected (from 0 to len(labels)-1)
    labels : list of strings
        Strings to be displayed as options in the radio widget
    tooltips : list of str, optional
        List of strings to use as tooltips for the corresponding radio items (default is None)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    onchange : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive a single parameter, containing the index of the selected option in the range from 0 to len(labels)-1
    row : bool, optional
        Flag to control the position of radio buttons, either horizontal or vertical (default is True)
            
    Example
    -------
    Creation and display of a radio widget to select among three options::
        
        from vois.vuetify import radio
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        r = radio.radio(0,
                        ['Option 0', 'Option 1', 'Option 2'],
                        tooltips=['Tooltip for Option 1'],
                        onchange=onchange,
                        row=True)

        display(r.draw())
        display(output)

    .. figure:: figures/radio.png
       :scale: 100 %
       :alt: radio widget

       Example of a radio widget to select from three options.
   """

    # Initialization
    def __init__(self, index, labels, tooltips=None, color=settings.color_first, onchange=None, row=True):
        
        self.value    = index
        self.labels   = labels
        self.tooltips = tooltips
        self.color    = color
        self.onchange = onchange
        self.row      = row
        
        self.r = []
        i = 0
        for label in self.labels:
            if self.row: self.r.append(v.Radio(label=label, class_="pa-0 ma-0 ml-2 mt-2 mr-6 mb-n3", color=settings.color_first))
            else:        self.r.append(v.Radio(label=label, class_="pa-0 ma-0 ml-2 mt-3 mr-6 mb-n2", color=settings.color_first))
            if i < len(self.tooltips):
                self.r[i] = tooltip.tooltip(self.tooltips[i], self.r[i])
            i += 1

        self.rg = v.RadioGroup(v_model=self.value, row=self.row, class_="pa-0 ma-0", large=True, 
                               color=settings.color_first, children=self.r, style_="overflow: hidden;")
        
        # If requested onchange management
        if not self.onchange is None:
            self.rg.on_event('change', self.__internal_onchange)
        
    
    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        self.value = data
        if self.onchange:
            self.onchange(data)
    
    # Returns the vuetify object to display (the v.RadioGroup itself)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.RadioGroup widget)"""
        return self.rg

