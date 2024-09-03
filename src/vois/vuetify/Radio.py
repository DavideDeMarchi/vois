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

from vois.vuetify import tooltip
from vois.vuetify.utils.util import *
from typing import Callable, Optional


#####################################################################################################################################################
# Radio control
#####################################################################################################################################################
class Radio(v.RadioGroup):
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
    on_change : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive a single parameter, containing the index of the selected option in the range from 0 to len(labels)-1
    row : bool, optional
        Flag to control the position of radio buttons, either horizontal or vertical (default is True)
            
    Example
    -------
    Creation and display of a radio widget to select among three options::
        
        from vois.vuetify import Radio
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_change(value):
            with output:
                print(value)

        r = Radio(0,
                ['Option 0', 'Option 1', 'Option 2'],
                tooltips=['Tooltip for Option 1'],
                on_change=on_change,
                row=True)

        display(r)
        display(output)

    .. figure:: figures/radio.png
       :scale: 100 %
       :alt: radio widget

       Example of a radio widget to select from three options.
   """

    deprecation_alias = dict(onchange='on_change')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 index: int,
                 labels: list[str],
                 tooltips: list[str] = [],
                 color: str = None,
                 on_change: Optional[Callable[[int], None]] = None,
                 row: bool = True):

        from vois.vuetify import settings

        self.value = index
        self.labels = labels
        self.tooltips = tooltips
        self.color = color if color is not None else settings.color_first
        self.on_change = on_change
        self.row = row

        self.r = []
        i = 0
        for label in self.labels:
            if self.row:
                self.r.append(v.Radio(label=label, class_="pa-0 ma-0 ml-2 mt-2 mr-6 mb-n3", color=self.color))
            else:
                self.r.append(v.Radio(label=label, class_="pa-0 ma-0 ml-2 mt-3 mr-6 mb-n2", color=self.color))
            if i < len(self.tooltips):
                self.r[i] = tooltip.tooltip(self.tooltips[i], self.r[i])
            i += 1

        super().__init__(v_model=self.value, row=self.row, class_="pa-0 ma-0", large=True,
                         color=self.color, children=self.r, style_="overflow: hidden;")

        # If requested onchange management
        if self.on_change:
            self.on_event('change', self.__internal_onchange)

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        self.value = widget.v_model
        if self.on_change:
            self.on_change(self.value)

    # Returns the vuetify object to display (the v.RadioGroup itself)
    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
