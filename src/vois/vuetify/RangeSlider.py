"""Slider to select a range of numeric values."""
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
import warnings
import ipyvuetify as v

from vois.vuetify.utils.util import *
from typing import Callable, Any, Union, Optional


#####################################################################################################################################################
# Integer range slider class
#####################################################################################################################################################
class RangeSlider(v.RangeSlider):
    """
    Slider to select a range of numeric values.
        
    Parameters
    ----------
    selected_min_value : numeric
        Minimum value of the selected range
    selected_max_value : numeric
        Maximum value of the selected range
    min_value : numeric
        Minimum value selectable by the user
    max_value : numeric
        Maximum value selectable by the user
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    onchange : function, optional
        Python function to call when the user selects a value. The function will receive two parameters of numeric type containing the current min and max value selected by the user
    height : int, optional
        Height of the slider widget in pixel (default is 250 pixels)
    vertical : bool, optional
        Flag to display the range slider in vertical mode (default is True)
            
    Example
    -------
    Creation and display of a range slider widget::
        
        from vois.vuetify import RangeSlider
        
        s = RangeSlider(5,18, 0,20)
        display(s)

    .. figure:: figures/rangeSlider.png
       :scale: 100 %
       :alt: rangeSlider widget

       RangeSlider widget example
   """

    deprecation_alias = dict(selectedminvalue='selected_min_value', selectedmaxvalue='selected_max_value',
                             minvalue='min_value', maxvalue='max_value', onchange='on_change')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 selected_min_value: int,
                 selected_max_value: int,
                 min_value: int,
                 max_value: int,
                 color: Optional[str] = None,
                 on_change: Optional[Callable[[tuple[int, int]], None]] = None,
                 height: int = 250,
                 vertical: bool = True):

        from vois.vuetify import settings

        self.selected_min_value = selected_min_value
        self.selected_max_value = selected_max_value
        self.min_value = min_value
        self.max_value = max_value
        self.color = color if color is not None else settings.color_first
        self.on_change = on_change
        self.height = height
        self.vertical = vertical

        if self.vertical:
            margins = "ml-n5 mr-1 mt-n6 mb-n7"
        else:
            margins = "ml-5  mr-5 mt-4  mb-n6"

        self.slider = self

        super().__init__(v_model=[self.selected_min_value, self.selected_max_value], dense=True, small=True,
                         thumb_color=self.color,
                         thumb_label="always", thumb_size=32, ticks=True, ticks_size=10,
                         color=self.color, track_color="grey", class_="pa-0 ma-0 %s" % margins,
                         min=self.min_value, max=self.max_value, vertical=self.vertical, height=self.height)

        # If requested onchange management
        if not self.on_change is None:
            self.slider.on_event('end', self.__internal_onchange)

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.on_change:
            self.on_change(data[0], data[1])

    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
