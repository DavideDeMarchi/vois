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

from vois.vuetify import settings, label, tooltip


#####################################################################################################################################################
# sliderFloat control
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
    maxint : int, optional
        Maximum integer number for the underlining integer slider (defines the slider sensitivity). Default value is None, meaning it will be automatically calculated
    labelwidth : int, optional
        Width of the label part of the widgets in pixels (default is 0, meaning it is automatically calculated based on the provided label text)
    sliderwidth : int, optional
        Width in pixels of the slider component of the widget (default is 200)
    resetbutton: bool, optional
        If True a reset button is displayed, allowing for resetting the widget to its initial value (default is False)
    showtooltip: bool, optional
        If True the up and down buttons will have a tooltip (default is False)
    onchange : function, optional
        Python function to call when the changes the value of the slider. The function will receive a single parameter, containing the new value of the slider in the range from minvalue to maxvalue (default is None)
    color : str, optional
        Color of the widget (default is settings.color_first)
    editable : bool, optional
        If True the label can be edited by clicking on it (default is False)
    editableWidth : int, optional
        If the slider is editable, set the width of the v.TextField widget to enter the value (default is 90)
            
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

        o = sliderFloat.sliderFloat(0.8, text='Fill opacity:', minvalue=0.0, maxvalue=1.0, onchange=onchange)
        
        display(o.draw())
        display(output)

    .. figure:: figures/sliderFloat.png
       :scale: 100 %
       :alt: opacity widget

       Example of an slider widget to select a floating point value.
   """

    # Initialization
    def __init__(self, value=1.0, minvalue=0.0, maxvalue=1.0, text='Select', showpercentage=True, decimals=2, maxint=None, 
                 labelwidth=0, sliderwidth=200, resetbutton=False, showtooltip=False, onchange=None, color=None,
                 editable=False, editableWidth=90):
        
        self.onchange = onchange
        
        self.editable = editable
        self.editableWidth = editableWidth
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.showpercentage = showpercentage
        self.decimals       = decimals
        
        self._color = color
        if self._color is None:
            self._color = settings.color_first
        
        if maxint is None:
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
        else:
            self.maxint = maxint
        
        self.postchar = ''
        if self.showpercentage: self.postchar = '%'
            
        self.labelwidth  = labelwidth
        self.sliderwidth = sliderwidth
        self.resetbutton = resetbutton
        
        self.int_initial_value = self.float2integer(value)
        
        #self.label  = label.label(text, textweight=400, margins=0, margintop=4, height=22)
        
        if self.labelwidth > 0:
            spx = '%dpx'%self.labelwidth
            style = 'width: %s; min-width: %s; max-width: %s;'%(spx,spx,spx)
        else:
            style = ''
        self.label = v.Html(tag='div', children=[text], class_='pa-0 ma-0 mt-4', style_=style)
        self.slider = v.Slider(v_model=self.int_initial_value,
                               dense=True, xsmall=True, 
                               ticks=False, thumb_size=10, dark=settings.dark_mode,
                               color=self._color, track_color="grey",
                               class_="pa-0 ma-0 ml-5 mr-4 mt-3 mb-n1",
                               style_='max-width: %dpx; width: %dpx;'%(self.sliderwidth,self.sliderwidth),
                               min=0, max=self.maxint, vertical=False, height=32)
        self.slider.on_event('input',  self.oninput)
        self.slider.on_event('change', self.onsliderchange)
        
        self.fieldvalue = v.TextField(autofocus=True, hide_details=True, single_line=True, hide_spin_buttons=False, dense=True, outlined=True, color=settings.color_first, type="number", class_='pa-0 ma-0 mt-2')
        self.cfieldvalue = v.Card(flat=True, children=[self.fieldvalue], width=self.editableWidth, max_width=self.editableWidth)
        self.fieldvalue.on_event('change', self.onchangefieldvalue)
        self.fieldvalue.on_event('blur',   self.onchangefieldvalue)
        
        if self.showpercentage:
            self.labelvalue = v.Html(tag='div', children=[str(self.int_initial_value) + self.postchar], class_='pa-0 ma-0 mt-4')
        else:
            self.labelvalue = v.Html(tag='div', children=['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar], class_='pa-0 ma-0 mt-4')

        self.labelvalue.on_event('click', self.onvaluechange)

        if self.resetbutton:
            self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-right'])])
            self.bup.on_event('click', self.onup)
            self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cup = tooltip.tooltip("Increase",self.cup)

            self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-left'])])
            self.bdn.on_event('click', self.ondn)
            self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cdn = tooltip.tooltip("Decrease",self.cdn)

            self.bres = v.Btn(icon=True, x_small=True, rounded=False, elevation=0, width=15, height=15, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-close'])])
            self.bres.on_event('click', self.onreset)
            self.cres = v.Card(children=[self.bres], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cres = tooltip.tooltip("Reset value",self.cres)
                
            self.buttons = widgets.HBox([self.cdn,self.cres,self.cup])
        else:
            self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-up'])])
            self.bup.on_event('click', self.onup)
            self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-2', style_="overflow: hidden;")
            if showtooltip: self.cup = tooltip.tooltip("Increase",self.cup)

            self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-down'])])
            self.bdn.on_event('click', self.ondn)
            self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1', style_="overflow: hidden;")
            if showtooltip: self.cdn = tooltip.tooltip("Decrease",self.cdn)
            
            self.buttons = widgets.VBox([self.cup,self.cdn])

        self.row = v.Row(justify='start', class_='pa-0 ma-0', no_gutters=True, children=[self.label, self.slider, self.buttons, self.labelvalue], style_="overflow: hidden;")            
        
        
    # When carriage return on the self.fieldvalue or an external click
    def onchangefieldvalue(self, *args):
        self.row.children = [self.label, self.slider, self.buttons, self.labelvalue]
        v = self.value
        self.value = float(self.fieldvalue.v_model)
        self.fieldvalue.v_model = self.value
        
    # On click on the self.labelvalue: display the self.fieldvalue
    def onvaluechange(self, *args):
        if self.editable and not self.slider.disabled:
            self.fieldvalue.v_model = self.value
            self.row.children = [self.label, self.slider, self.buttons, self.cfieldvalue]
            
        
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
    
    def onreset(self, *args):
        self.slider.v_model = self.int_initial_value
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
        return self.row

        
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

    @property
    def color(self):
        """
        Get/Set the widget color.
        
        Returns
        --------
        c : str
            widget color

        Example
        -------
        Programmatically change the widget color::
            
            s.color = '#00FF00'
            print(s.color)
        
        """
        return self._color
        
    @color.setter
    def color(self, c):
        if isinstance(c, str):
            self._color = c
            self.slider.color = self._color
        