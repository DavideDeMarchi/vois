"""Widget to select an opacity value in [0.0, 1.0]."""
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
from ipywidgets import widgets
import ipyvuetify as v

try:
    from . import settings
    from . import label
except:
    import settings
    import label


#####################################################################################################################################################
# Opacity control
#####################################################################################################################################################
class opacity():
    """
    Compound widget to insert an opacity value as a float in the range [0.0, 1.0].
        
    Parameters
    ----------
    value : float, optional
        Initial value of the opacity (default is 1.0)
    text : str, optional
        Text to display on the left of the opacity slider (default is 'Opacity')
    onchange : function, optional
        Python function to call when the changes the value of opacity. The function will receive a single parameter, containing the new value of the opacity in the range from 0.0 to 1.0 (default is None)
            
    Example
    -------
    Creation and display of a radio widget to select among three options::
        
        from vois.vuetify import opacity
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        o = opacity.opacity(0.8, text='Fill opacity:', onchange=onchange)
        
        display(o.draw())
        display(output)

    .. figure:: figures/opacity.png
       :scale: 100 %
       :alt: opacity widget

       Example of an opacity widget to select a floting poit value in the range [0.0, 1.0].
   """

    # Initialization
    def __init__(self, value=1.0, text='Opacity', onchange=None):
        
        self.onchange = onchange
        
        intvalue = self.float2integer(value)
        
        self.label  = label.label(text, textweight=400, margins=0, margintop=4, height=22)
        self.slider = v.Slider(v_model=intvalue,
                               dense=True, xsmall=True, 
                               ticks=True, thumb_size=10, dark=settings.dark_mode,
                               color=settings.color_first, track_color="grey",
                               class_="pa-0 ma-0 ml-5 mr-4 mt-3 mb-n1",
                               style_='max-width: 140px; width: 140px;',
                               min=0, max=100, vertical=False, height=32)
        self.slider.on_event('end',   self.onend)
        self.slider.on_event('input', self.oninput)
        self.labelvalue = v.Html(tag='div', children=[str(intvalue) + '%'], class_='pa-0 ma-0 mt-4')

        self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-up'])])
        self.bup.on_event('click', self.onup)
        self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-2', style_="overflow: hidden;")
        self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-down'])])
        self.bdn.on_event('click', self.ondn)
        self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1', style_="overflow: hidden;")
        self.buttons = widgets.VBox([self.cup,self.cdn])
        
    # End of movement on the slider
    def onend(self, *args):
        self.labelvalue.children = [str(self.slider.v_model) + '%']
        if not self.onchange is None:
            self.onchange(self.integer2float(self.slider.v_model))
        self.bup.disabled = self.slider.v_model >= 100
        self.bdn.disabled = self.slider.v_model <= 0
            
    # Input change on the slider
    def oninput(self, *args):
        self.labelvalue.children = [str(self.slider.v_model) + '%']
        
    # Click on the up button
    def onup(self, *args):
        self.slider.v_model = self.slider.v_model + 1
        self.onend()
    
    # Click on the down button
    def ondn(self, *args):
        self.slider.v_model = self.slider.v_model - 1
        self.onend()
    
    # Conversion of float value [0.0,1.0] to integer in [0,100]
    def float2integer(self, value):
        return int(100 * max(0.0, min(1.0,float(value))))
    
    # Conversion of integer value [0,100] to float in [0.0,1.0]
    def integer2float(self, value):
        return float(value) / 100.0

    # Draw the widget
    def draw(self):
        """Returns the ipyvuetify object to display (a v.Row widget)"""
        return v.Row(justify='start', class_='pa-0 ma-0', no_gutters=True, children=[self.label.draw(), self.slider, self.buttons, self.labelvalue], style_="overflow: hidden;")

        
    # Get the opacity value
    @property
    def value(self):
        """
        Get/Set the opacity value.
        
        Returns
        --------
        value : float
            Current value of the opacity in the range [0.0, 1.0]

        Example
        -------
        Programmatically set opacity value
            
            o.value = 0.56
        
        """
        return self.integer2float(self.slider.v_model)
   

    # Set the opacity value
    @value.setter
    def value(self, newvalue):
        if newvalue < 0.0:
            newvalue = 0.0
        if newvalue > 1.0:
            newvalue = 1.0
            
        intvalue = self.float2integer(newvalue)
        self.slider.v_model = intvalue
        self.onend()
