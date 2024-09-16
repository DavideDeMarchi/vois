"""Slider widget is a better visualization of the number input. It is used for gathering numerical user data."""
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

import ipyvuetify as v
from vois.vuetify.utils.util import *
from typing import Callable, Any, Union, Optional


#####################################################################################################################################################
# Integer slider class
#####################################################################################################################################################
class Slider(v.Html):
    """
    Slider widget is a better visualization of the number input. It is used for gathering numerical user data.
        
    Parameters
    ----------
    selected_value : numeric
        Initial value of the slider
    min_value : numeric
        Minimal value selectable by the user
    max_value : numeric
        Maximum value selectable by the user
    step : numeric, optional
        Step interval for ticks (default is 1.0)
    vertical : bool, optional
        Flag that controls the direction of the slider: horizontal or vertical (default is False)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    on_change : function, optional
        Python function to call when the user selects a value. The function will receive a parameter of numeric type containing the current value of the slider widget
    height : int, optional
        Height of the slider widget in pixel (default is 120 pixels)
    width : int, optional
        Width of the slider widget in pixel. It is needed only for vertical sliders (default is None)
            
    Example
    -------
    Creation and display of a slider widget::
        
        from vois.vuetify import Slider
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def onchange(value):
            with output:
                print(value)

        s = Slider(2015, 2010, 2021, onchange=onchange)
        display(s)

    .. figure:: figures/slider.png
       :scale: 100 %
       :alt: slider widget

       Slider widget example
   """
    deprecation_alias = dict(selectedvalue='selected_value', minvalue='min_value', maxvalue='max_value',
                             onchange='on_change')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 selected_value: Union[int, float],
                 min_value: Union[int, float],
                 max_value: Union[int, float],
                 vertical=False,
                 color: str = None,
                 on_change: Optional[Callable[[], None]] = None,
                 height: int = 120,
                 width: int = None,
                 step: Union[int, float] = 1.0,
                 **kwargs):

        super().__init__(**kwargs)

        from vois.vuetify import settings

        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.vertical = vertical
        self.width = width
        self.on_change = on_change

        if vertical:
            c = "pa-0 ma-0 ml-n12 mr-n12 mt-n9 mb-n10"
        else:
            c = "pa-0 ma-0 ml-5 mr-5 mt-n2 mb-n12"
        self.slider = v.Slider(v_model=selected_value, dense=True, small=True, thumb_color=color,
                               thumb_label="always", thumb_size=32, ticks=True, ticks_size=10,
                               color=color if color is not None else settings.color_first,
                               track_color="grey", class_=c,
                               min=self.min_value, max=self.max_value, step=self.step,
                               vertical=self.vertical, height=height)

        # If requested onchange management
        if not self.on_change is None:
            self.slider.on_event('end', self.__internal_onchange)

        self.tag = 'div'
        self.children = [self.slider]

        if self.vertical and not self.width is None:
            self.style_ = 'width: %dpx; overflow: hidden;' % self.width
        else:
            self.style_ = 'overflow: hidden;'

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Get the value
    @property
    def value(self):
        """
        Get/Set the current value.
        
        Returns
        --------
        value : numeric
            Current value selected

        Example
        -------
        Programmatically set the value and print it::
            
            s.value = 2012
            print(s.value)
        
        """
        return self.slider.v_model

    # Set the value
    @value.setter
    def value(self, v):
        if self.min_value <= v <= self.max_value:
            self.slider.v_model = v
            if self.on_change:
                self.on_change(self.slider.v_model)

    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.on_change:
            self.on_change(data)

    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
