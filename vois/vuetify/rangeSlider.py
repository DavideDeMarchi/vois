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
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
except:
    import settings


#####################################################################################################################################################
# Integer range slider class
#####################################################################################################################################################
class rangeSlider:
    """
    Slider to select a range of numeric values.
        
    Parameters
    ----------
    selectedminvalue : numeric
        Minimum value of the selected range
    selectedmaxvalue : numeric
        Maximum value of the selected range
    minvalue : numeric
        Minimum value selectable by the user
    maxvalue : numeric
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
        
        from vois.vuetify import rangeSlider
        
        s = rangeSlider.rangeSlider(5,18, 0,20)
        s.draw()

    .. figure:: figures/rangeSlider.png
       :scale: 100 %
       :alt: rangeSlider widget

       RangeSlider widget example
   """

   
    # Initialization
    def __init__(self, selectedminvalue, selectedmaxvalue, minvalue, maxvalue, color=settings.color_first, onchange=None,
                 height=250, vertical=True):
        
        self.selectedminvalue = selectedminvalue
        self.selectedmaxvalue = selectedmaxvalue
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.color    = color
        self.onchange = onchange
        self.height   = height
        self.vertical = vertical
        
        if self.vertical: margins = "ml-n5 mr-1 mt-n6 mb-n7"
        else:             margins = "ml-5  mr-5 mt-4  mb-n6"
        
        self.slider = v.RangeSlider(v_model=[self.selectedminvalue,self.selectedmaxvalue], dense=True, small=True, thumb_color=self.color, 
                                    thumb_label="always", thumb_size=32, ticks=True, ticks_size=10, 
                                    color=self.color, track_color="grey", class_="pa-0 ma-0 %s" % margins,
                                    min=self.minvalue, max=self.maxvalue, vertical=self.vertical, height=self.height) 
        
        # If requested onchange management
        if not self.onchange is None:
            self.slider.on_event('end', self.__internal_onchange)
        
    
    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.onchange:
            self.onchange(data[0],data[1])
    
    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html widget that contains a v.RangeSlider as its unique child)"""
        return v.Html(tag='div',children=[self.slider], style_='overflow: hidden;')
            
