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
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
except:
    import settings


#####################################################################################################################################################
# Integer slider class
#####################################################################################################################################################
class slider:
    """
    Slider widget is a better visualization of the number input. It is used for gathering numerical user data.
        
    Parameters
    ----------
    selectedvalue : numeric
        Initial value of the slider
    minvalue : numeric
        Minimal value selectable by the user
    maxvalue : numeric
        Maximum value selectable by the user
    step : numeric, optional
        Step interval for ticks (default is 1.0)
    vertical : bool, optional
        Flag that controls the direction of the slider: horizontal or vertical (default is False)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    onchange : function, optional
        Python function to call when the user selects a value. The function will receive a parameter of numeric type containing the current value of the slider widget
    height : int, optional
        Height of the slider widget in pixel (default is 120 pixels)
    width : int, optional
        Width of the slider widget in pixel. It is needed only for vertical sliders (default is None)
            
    Example
    -------
    Creation and display of a slider widget::
        
        from vois.vuetify import slider
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def onchange(value):
            with output:
                print(value)

        s = slider.slider(2015, 2010,2021, onchange=onchange)
        display(s.draw())

    .. figure:: figures/slider.png
       :scale: 100 %
       :alt: slider widget

       Slider widget example
   """

   
    # Initialization
    def __init__(self, selectedvalue, minvalue, maxvalue, vertical=False, color=settings.color_first, onchange=None, height=120, width=None, step=1.0):
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.step     = step
        self.vertical = vertical
        self.width    = width
        self.onchange = onchange
        
        if vertical: c = "pa-0 ma-0 ml-n12 mr-n12 mt-n9 mb-n10"
        else:        c = "pa-0 ma-0 ml-5 mr-5 mt-n2 mb-n12"
        self.slider = v.Slider(v_model=selectedvalue, dense=True, small=True, thumb_color=color, 
                               thumb_label="always", thumb_size=32, ticks=True, ticks_size=10, 
                               color=color, track_color="grey", class_=c,
                               min=self.minvalue, max=self.maxvalue, step=self.step,
                               vertical=self.vertical, height=height)
        
        # If requested onchange management
        if not self.onchange is None:
            self.slider.on_event('end', self.__internal_onchange)

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
        if v >= self.minvalue and v <= self.maxvalue:
            self.slider.v_model = v
            if self.onchange:
                self.onchange(self.slider.v_model)
    
    
    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.onchange:
            self.onchange(data)
    
    
    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html that contains a v.Slider widget as its only child)"""
        if self.vertical and not self.width is None:
            return v.Html(tag='div',children=[self.slider], style_='width: %dpx; overflow: hidden;' % self.width)
        else:
            return v.Html(tag='div',children=[self.slider], style_='overflow: hidden;')
            
