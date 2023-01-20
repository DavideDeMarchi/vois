"""Widget to select a float value"""
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
# floatSlider control
#####################################################################################################################################################
class sliderFloat():
    """
    Compound widget to select a float value in a specific range.
        
    Parameters
    ----------
    value : float, optional
        Initial value of the slider (default is 1.0)
    minvalue : float, optional
        Minimum value of the slider (default is 0.0)
    maxvalue : float, optional
        Maximum value of the slider (default is 1.0)
    text : str, optional
        Text to display on the left of the slider (default is 'Select')
    showpercentage : bool, optional
        If True, the widget will write the current value as a percentage inside the allowed range and will append the % sign to the right of the current value (default is True)
    decimals : int, optional
        Number of decimal digits to use in case showpercentage is False (default is 2)
    sliderwidth : int, optional
        Width in pixels of the slider component of the widget (default is 200)
    onchange : function, optional
        Python function to call when the changes the value of opacity. The function will receive a single parameter, containing the new value of the opacity in the range from 0.0 to 1.0 (default is None)
            
    Example
    -------
    Creation and display of a slider widget to select an opacity value in the range [0.0, 1.0]::
        
        from vois.vuetify import sliderFloat
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        o = sliderFloat.sliderFloat(0.8, text='Fill opacity:', min=0.0, max=1.0, onchange=onchange)
        
        display(o.draw())
        display(output)

    .. figure:: figures/sliderFloat.png
       :scale: 100 %
       :alt: opacity widget

       Example of an slider widget to select a floting point value.
   """

    # Initialization
    def __init__(self, value=1.0, minvalue=0.0, maxvalue=1.0, text='Select', showpercentage=True, decimals=2, labelwidth=0, sliderwidth=200, onchange=None):
        
        self.onchange = onchange
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.showpercentage = showpercentage
        self.decimals       = decimals
        
        if self.decimals <= 1:
            self.maxint = 10
        elif self.decimals == 2:
            self.maxint = 100
        elif self.decimals == 3:
            self.maxint = 1000
        elif self.decimals == 4:
            self.maxint = 10000
        else:
            self.maxint = 100000
        
        self.postchar = ''
        if self.showpercentage: self.postchar = '%'
            
        self.labelwidth  = labelwidth
        self.sliderwidth = sliderwidth
        
        intvalue = self.float2integer(value)
        
        #self.label  = label.label(text, textweight=400, margins=0, margintop=4, height=22)
        
        if self.labelwidth > 0:
            spx = '%dpx'%self.labelwidth
            style = 'width: %s; min-width: %s; max-width: %s;'%(spx,spx,spx)
        else:
            style = ''
        self.label = v.Html(tag='div', children=[text], class_='pa-0 ma-0 mt-4', style_=style)
        self.slider = v.Slider(v_model=intvalue,
                               dense=True, xsmall=True, 
                               ticks=False, thumb_size=10, dark=settings.dark_mode,
                               color=settings.color_first, track_color="grey",
                               class_="pa-0 ma-0 ml-5 mr-4 mt-3 mb-n1",
                               style_='max-width: %dpx; width: %dpx;'%(self.sliderwidth,self.sliderwidth),
                               min=0, max=self.maxint, vertical=False, height=32)
        self.slider.on_event('input',  self.oninput)
        self.slider.on_event('change', self.onsliderchange)
        
        if self.showpercentage:
            self.labelvalue = v.Html(tag='div', children=[str(intvalue) + self.postchar], class_='pa-0 ma-0 mt-4')
        else:
            self.labelvalue = v.Html(tag='div', children=['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar], class_='pa-0 ma-0 mt-4')

        self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-up'])])
        self.bup.on_event('click', self.onup)
        self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-2', style_="overflow: hidden;")
        self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-down'])])
        self.bdn.on_event('click', self.ondn)
        self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1', style_="overflow: hidden;")
        self.buttons = widgets.VBox([self.cup,self.cdn])
        
        
    # Input event on the slider
    def oninput(self, *args):
        if self.showpercentage:
            value = self.slider.v_model
            self.labelvalue.children=[str(value) + self.postchar]
        else:
            value = self.integer2float(self.slider.v_model)
            self.labelvalue.children=['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar]

            
    # Input change on the slider
    def onsliderchange(self, *args):
        if self.showpercentage:
            value = self.slider.v_model
            self.labelvalue.children=[str(value) + self.postchar]
        else:
            value = self.integer2float(self.slider.v_model)
            self.labelvalue.children=['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar]
        
        if not self.onchange is None:
            self.onchange(self.integer2float(self.slider.v_model))
        self.bup.disabled = self.slider.v_model >= self.maxint
        self.bdn.disabled = self.slider.v_model <= 0
            
            
    # Click on the up button
    def onup(self, *args):
        if self.slider.v_model < self.maxint:
            self.slider.v_model = self.slider.v_model + 1
            self.onsliderchange()
    
    # Click on the down button
    def ondn(self, *args):
        if self.slider.v_model > 0:
            self.slider.v_model = self.slider.v_model - 1
            self.onsliderchange()
    
    # Conversion of float value [minvalue,maxvalue] to integer in [0,self.maxint]
    def float2integer(self, value):
        return int(self.maxint * (max(self.minvalue, min(self.maxvalue, float(value))) - self.minvalue) / (self.maxvalue - self.minvalue))
    
    # Conversion of integer value [0,self.maxint] to float in [0.0,1.0]
    def integer2float(self, value):
        return ((self.maxvalue - self.minvalue) * float(value)) / float(self.maxint) + self.minvalue

    # Draw the widget
    def draw(self):
        """Returns the ipyvuetify object to display (a v.Row widget)"""
        return v.Row(justify='start', class_='pa-0 ma-0', no_gutters=True, children=[self.label, self.slider, self.buttons, self.labelvalue], style_="overflow: hidden;")

        
    # Get the slider value
    @property
    def value(self):
        """
        Get/Set the slider value.
        
        Returns
        --------
        value : float
            Current value of the slider

        Example
        -------
        Programmatically set the slider value
            
            s.value = 0.56
        
        """
        return self.integer2float(self.slider.v_model)
   

    # Set the slider value
    @value.setter
    def value(self, newvalue):
        if newvalue < self.minvalue:
            newvalue = self.minvalue
        if newvalue > self.maxvalue:
            newvalue = self.maxvalue
            
        intvalue = self.float2integer(newvalue)
        self.slider.v_model = intvalue
        self.onsliderchange()
