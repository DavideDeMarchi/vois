"""Widget to select a range of float values"""
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
# rangeSliderFloat control
#####################################################################################################################################################
class rangeSliderFloat():
    """
    Compound widget to select a range of float values in a specific range.
        
    Parameters
    ----------
    selectedminvalue : float
        Initial minimum value of the slider
    selectedmaxvalue : float
        Initial maximum value of the slider
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
        Python function to call when the changes the range value of the slider. The function will receive a single parameter, containing the new value of the opacity in the range from 0.0 to 1.0 (default is None)
    editable : bool, optional
        If True the min and max label can be edited by clicking on them (default is False)
    editableWidth : int, optional
        If the slider is editable, set the width of the v.TextField widgets to enter the min and max value (default is 90)
            
    Example
    -------
    Creation and display of a range slider widget to select an opacity range in a custom interval::
        
        from vois.vuetify import rangeSliderFloat
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        o = rangeSliderFloat.rangeSliderFloat(1.8, 2.5, text='Select Value in [1.0,3.0]:',
                                              minvalue=1.0, maxvalue=3.0, onchange=onchange)
        
        display(o.draw())
        display(output)

    .. figure:: figures/rangeSliderFloat.png
       :scale: 100 %
       :alt: opacity widget

       Example of an range slider widget to select a floating point range.
   """

    # Initialization
    def __init__(self, selectedminvalue, selectedmaxvalue, minvalue=0.0, maxvalue=1.0, text='Select', showpercentage=True, decimals=2, maxint=None, 
                 labelwidth=0, sliderwidth=200, resetbutton=False, showtooltip=False, onchange=None,
                 editable=False, editableWidth=90):
        
        self.onchange = onchange
        
        self.editable = editable
        self.editableWidth = editableWidth
        
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.showpercentage = showpercentage
        self.decimals       = decimals
        
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
        
        self.intvaluemin = self.float2integer(selectedminvalue)
        self.intvaluemax = self.float2integer(selectedmaxvalue)
        
        #self.label  = label.label(text, textweight=400, margins=0, margintop=4, height=22)
        
        if self.labelwidth > 0:
            spx = '%dpx'%self.labelwidth
            style = 'width: %s; min-width: %s; max-width: %s;'%(spx,spx,spx)
        else:
            style = ''
        self.label = v.Html(tag='div', children=[text], class_='pa-0 ma-0 mt-4', style_=style)
        self.slider = v.RangeSlider(v_model=[self.intvaluemin,self.intvaluemax],
                                    dense=True, xsmall=True, 
                                    ticks=False, thumb_size=10, dark=settings.dark_mode,
                                    color=settings.color_first, track_color="grey",
                                    class_="pa-0 ma-0 ml-3 mr-5 mt-3 mb-n1",
                                    style_='max-width: %dpx; width: %dpx;'%(self.sliderwidth,self.sliderwidth),
                                    min=0, max=self.maxint, vertical=False, height=32, disabled=False)
        self.slider.on_event('input',  self.oninput)
        self.slider.on_event('change', self.onsliderchange)

        self.fieldmin = v.TextField(autofocus=True, hide_details=True, single_line=True, hide_spin_buttons=False, dense=True, outlined=True, color=settings.color_first, type="number", class_='pa-0 ma-0 mt-2')
        self.cfieldmin = v.Card(flat=True, children=[self.fieldmin], width=self.editableWidth, max_width=self.editableWidth)
        self.fieldmin.on_event('change', self.onchangefieldmin)
        self.fieldmin.on_event('blur',   self.onchangefieldmin)
        self.fieldmax = v.TextField(autofocus=True, hide_details=True, single_line=True, hide_spin_buttons=False, dense=True, outlined=True, color=settings.color_first, type="number",class_='pa-0 ma-0 mt-2')
        self.cfieldmax = v.Card(flat=True, children=[self.fieldmax], width=self.editableWidth, max_width=self.editableWidth)
        self.fieldmax.on_event('change', self.onchangefieldmax)
        self.fieldmax.on_event('blur',   self.onchangefieldmax)
        
        if self.showpercentage:
            self.labelvaluemin = v.Html(tag='div', children=[str(self.intvaluemin) + self.postchar], class_='pa-0 ma-0 mt-4 ml-4')
            self.labelvaluemax = v.Html(tag='div', children=[str(self.intvaluemax) + self.postchar], class_='pa-0 ma-0 mt-4')
            self.fieldmin.v_model = self.intvaluemin
            self.fieldmax.v_model = self.intvaluemax
        else:
            self.labelvaluemin = v.Html(tag='div', children=['{:.{prec}f}'.format(selectedminvalue, prec=self.decimals) + self.postchar], class_='pa-0 ma-0 mt-4 ml-4')
            self.labelvaluemax = v.Html(tag='div', children=['{:.{prec}f}'.format(selectedmaxvalue, prec=self.decimals) + self.postchar], class_='pa-0 ma-0 mt-4')
            self.fieldmin.v_model = selectedminvalue
            self.fieldmax.v_model = selectedmaxvalue

        self.labelvaluemin.on_event('click', self.onvaluemin)
        self.labelvaluemax.on_event('click', self.onvaluemax)
       
        
        if self.resetbutton:
            self.bupmin = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-right'])])
            self.bupmin.on_event('click', self.onupmin)
            self.cupmin = v.Card(children=[self.bupmin], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cupmin = tooltip.tooltip("Increase min",self.cupmin)

            self.bdnmin = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-left'])])
            self.bdnmin.on_event('click', self.ondnmin)
            self.cdnmin = v.Card(children=[self.bdnmin], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cdnmin = tooltip.tooltip("Decrease min",self.cdnmin)

            self.bresmin = v.Btn(icon=True, x_small=True, rounded=False, elevation=0, width=15, height=15, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-close'])])
            self.bresmin.on_event('click', self.onresetmin)
            self.cresmin = v.Card(children=[self.bresmin], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cresmin = tooltip.tooltip("Reset min value",self.cresmin)
                
            self.buttonsmin = widgets.HBox([self.cdnmin,self.cresmin,self.cupmin])

            self.bupmax = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-right'])])
            self.bupmax.on_event('click', self.onupmax)
            self.cupmax = v.Card(children=[self.bupmax], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cupmax = tooltip.tooltip("Increase max",self.cupmax)

            self.bdnmax = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-left'])])
            self.bdnmax.on_event('click', self.ondnmax)
            self.cdnmax = v.Card(children=[self.bdnmax], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cdnmax = tooltip.tooltip("Decrease max",self.cdnmax)

            self.bresmax = v.Btn(icon=True, x_small=True, rounded=False, elevation=0, width=15, height=15, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-close'])])
            self.bresmax.on_event('click', self.onresetmax)
            self.cresmax = v.Card(children=[self.bresmax], elevation=0, class_='pa-0 ma-0 mr-1 mt-4', style_="overflow: hidden;")
            if showtooltip: self.cresmax = tooltip.tooltip("Reset max value",self.cresmax)
                
            self.buttonsmax = widgets.HBox([self.cdnmax,self.cresmax,self.cupmax])
        else:
            self.bupmin = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-up'])])
            self.bupmin.on_event('click', self.onupmin)
            self.cupmin = v.Card(children=[self.bupmin], elevation=0, class_='pa-0 ma-0 mr-1 mt-2', style_="overflow: hidden;")
            if showtooltip: self.cupmin = tooltip.tooltip("Increase min",self.cupmin)

            self.bdnmin = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-down'])])
            self.bdnmin.on_event('click', self.ondnmin)
            self.cdnmin = v.Card(children=[self.bdnmin], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1', style_="overflow: hidden;")
            if showtooltip: self.cdnmin = tooltip.tooltip("Decrease min",self.cdnmin)

            self.buttonsmin = widgets.VBox([self.cupmin,self.cdnmin])

            self.bupmax = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-up'])])
            self.bupmax.on_event('click', self.onupmax)
            self.cupmax = v.Card(children=[self.bupmax], elevation=0, class_='pa-0 ma-0 mr-1 mt-2', style_="overflow: hidden;")
            if showtooltip: self.cupmax = tooltip.tooltip("Increase max",self.cupmax)

            self.bdnmax = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-menu-down'])])
            self.bdnmax.on_event('click', self.ondnmax)
            self.cdnmax = v.Card(children=[self.bdnmax], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1', style_="overflow: hidden;")
            if showtooltip: self.cdnmax = tooltip.tooltip("Decrease max",self.cdnmax)

            self.buttonsmax = widgets.VBox([self.cupmax,self.cdnmax])
        
        self.row = v.Row(justify='start', class_='pa-0 ma-0', no_gutters=True, children=[self.label, self.labelvaluemin, self.buttonsmin, self.slider, self.buttonsmax, self.labelvaluemax], style_="overflow: hidden;")
        
        
    # When carriage return on the self.fieldmin or an external click
    def onchangefieldmin(self, *args):
        self.row.children = [self.label, self.labelvaluemin, self.buttonsmin, self.slider, self.buttonsmax, self.labelvaluemax]
        v = self.value
        self.value = float(self.fieldmin.v_model), v[1]
        self.fieldmin.v_model = self.value[0]
        
    # When carriage return on the self.fieldmax or an external click
    def onchangefieldmax(self, *args):
        self.row.children = [self.label, self.labelvaluemin, self.buttonsmin, self.slider, self.buttonsmax, self.labelvaluemax]
        v = self.value
        self.value = v[0], float(self.fieldmax.v_model)
        self.fieldmax.v_model = self.value[1]
        
    # On click on the self.labelvaluemin: display the self.fieldmin
    def onvaluemin(self, *args):
        if self.editable and not self.slider.disabled:
            self.fieldmin.v_model = self.value[0]
            self.row.children = [self.label, self.cfieldmin, self.buttonsmin, self.slider, self.buttonsmax, self.labelvaluemax]
        
    # On click on the self.labelvaluemax: display the self.fieldmax
    def onvaluemax(self, *args):
        if self.editable and not self.slider.disabled:
            self.fieldmax.v_model = self.value[1]
            self.row.children = [self.label, self.labelvaluemin, self.buttonsmin, self.slider, self.buttonsmax, self.cfieldmax]
        
        
    # Input event on the slider
    def oninput(self, *args):
        if self.showpercentage:
            valuemin,valuemax = self.slider.v_model
            self.labelvaluemin.children=[str(valuemin) + self.postchar]
            self.labelvaluemax.children=[str(valuemax) + self.postchar]
        else:
            valuemin,valuemax = self.slider.v_model
            valuemin = self.integer2float(valuemin)
            valuemax = self.integer2float(valuemax)
            self.labelvaluemin.children=['{:.{prec}f}'.format(valuemin, prec=self.decimals) + self.postchar]
            self.labelvaluemax.children=['{:.{prec}f}'.format(valuemax, prec=self.decimals) + self.postchar]

            
    # Input change on the slider
    def onsliderchange(self, *args):
        if self.showpercentage:
            valuemin,valuemax = self.slider.v_model
            self.labelvaluemin.children=[str(valuemin) + self.postchar]
            self.labelvaluemax.children=[str(valuemax) + self.postchar]
        else:
            valuemin,valuemax = self.slider.v_model
            valuemin = self.integer2float(valuemin)
            valuemax = self.integer2float(valuemax)
            self.labelvaluemin.children=['{:.{prec}f}'.format(valuemin, prec=self.decimals) + self.postchar]
            self.labelvaluemax.children=['{:.{prec}f}'.format(valuemax, prec=self.decimals) + self.postchar]
        
        if not self.onchange is None:
            self.onchange([self.integer2float(x) for x in self.slider.v_model])
        v1,v2 = self.slider.v_model
        self.bupmin.disabled = v1 >= v2
        self.bdnmin.disabled = v1 <= 0
        self.bupmax.disabled = v2 >= self.maxint
        self.bdnmax.disabled = v2 <= v1
            
            
    # Click on the up button
    def onupmin(self, *args):
        v1,v2 = self.slider.v_model
        if v1 < v2:
            self.slider.v_model = [v1+1, v2]
            self.onsliderchange()
    
    # Click on the down button
    def ondnmin(self, *args):
        v1,v2 = self.slider.v_model
        if v1 > 0:
            self.slider.v_model = [v1-1, v2]
            self.onsliderchange()
    
    # Click on the reset min button
    def onresetmin(self, *args):
        v1,v2 = self.slider.v_model
        self.slider.v_model = [self.intvaluemin, v2]
        self.onsliderchange()

        
    # Click on the up button
    def onupmax(self, *args):
        v1,v2 = self.slider.v_model
        if v2 < self.maxint:
            self.slider.v_model = [v1, v2+1]
            self.onsliderchange()
    
    # Click on the down button
    def ondnmax(self, *args):
        v1,v2 = self.slider.v_model
        if v2 > v1:
            self.slider.v_model = [v1, v2-1]
            self.onsliderchange()
        
    # Click on the reset max button
    def onresetmax(self, *args):
        v1,v2 = self.slider.v_model
        self.slider.v_model = [v1, self.intvaluemax]
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
        Get/Set the slider range value as a list of min and max selected value.
        
        Returns
        --------
        value : list of 2 floats
            Current value of the range slider

        Example
        -------
        Programmatically set the slider value
            
            s.value = [0.56, 0.83]
        
        """
        return [self.integer2float(x) for x in self.slider.v_model]
   

    # Set the slider value
    @value.setter
    def value(self, newvalue):
        v1,v2 = newvalue

        if v1 > v2: v1,v2 = v2,v1
        if v1 < self.minvalue:
            v1 = self.minvalue
        if v2 > self.maxvalue:
            v2 = self.maxvalue
            
        intvaluemin = self.float2integer(v1)
        intvaluemax = self.float2integer(v2)
        self.slider.v_model = [intvaluemin,intvaluemax]
        self.onsliderchange()

        
    # disabled property
    @property
    def disabled(self):
        return self.slider.disabled
    
    # Set the slider disabled state
    @disabled.setter
    def disabled(self, flag):
        self.slider.disabled = flag
        
        if self.resetbutton:
            self.bresmin.disabled = flag
            self.bresmax.disabled = flag
        
        self.bupmin.disabled = flag
        self.bdnmin.disabled = flag
        self.bupmax.disabled = flag
        self.bdnmax.disabled = flag
        