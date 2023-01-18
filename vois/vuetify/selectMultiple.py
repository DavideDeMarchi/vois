"""Multiple selection widget."""
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
    from . import fontsettings
except:
    import settings
    import fontsettings



#####################################################################################################################################################
# Class to display a multiple selection widget
#####################################################################################################################################################
class selectMultiple():
    """
    Single selection widget from a dropdown list. Passing the parameter newvalues_enabled=True enables the user to insert new strings in the widget.
        
    Parameters
    ----------
    label : str
        Help text to display 
    values : list of strings
        Strings to be displayed in the dropdown list of the widget 
    selected : list of str, optional
        List of strings that are initially selected (default is [])
    mapping : function, optional
        Python function to call to transform the visible strings into codes (for example names of countries to their iso2 codes)
    reverse_mapping : function, optional
        Python function to call to transform the codes into visible strings (for example iso2 codes of countries to their names)
    onchange : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive no parameter (use value property to retrieve the current selection)
    width : int, optional
        Width in pixel of the widget (default is 300 pixels)
    marginy : int, optional
        Margin in y coordinates to position the widget from top (default is 1)
            
    Example
    -------
    Creation and display of a multiple selection widget for the selection of one or more countries::
        
        from vois.vuetify import selectMultiple
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()
        display(output)

        def onchange():
            with output:
                print(sel.value)

        sel = selectMultiple.selectMultiple('Country:',
                                            ['Belgium', 'France', 'Italy', 'Germany'],
                                            selected=['France', 'Italy'],
                                            width=200,
                                            onchange=onchange)
        sel.draw()

    .. figure:: figures/selectMultiple.png
       :scale: 100 %
       :alt: selectMultiple widget

       Example of a selectMultiple widget to select from a list of countries.
   """
    
    # Initialization
    def __init__(self, label, values, selected=[], mapping=None, reverse_mapping=None, width=300, onchange=None, marginy=1):
        self.label           = label
        self.values          = values
        self.mapping         = mapping           # Function to convert names to codes
        self.reverse_mapping = reverse_mapping   # Function to convert codes to names
        self.width           = width
        self.onchange        = onchange
        
        self.select = None
        self.value  = selected
        
        self.select = v.Select(v_model=self._value,
                               label=self.label, dense=True, solo=False, outlined=True, multiple=True, chips=False, clearable=True,
                               item_color=settings.color_first, color=settings.color_first, class_='pa-0 mx-0 my-%d mb-n6' % marginy,
                               items=self.values, style_='max-width: %dpx; font-family: %s; font-weight:400; text-transform: none' % (self.width, fontsettings.font_name))
        
        self.select.on_event('input', self.__internal_onchange)

        
    def __internal_onchange(self, widget, event, data):
        self._value = data
        if self.onchange: self.onchange()
        
        
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html widget that contains a v.Select as its unique child)"""
        self.select.value = self._value
        return v.Html(tag='div',children=[self.select], style_='overflow: hidden;')
    
    
    # value property is a list!
    @property
    def value(self):
        """
        Get/Set the selected value.
        
        Returns
        --------
        v : str
            list of strings of the items currently selected

        Example
        -------
        Programmatically select a list of values::
            
            sel.value = ['Italy', 'Belgium']
            print(sel.value)
        
        """
        if not self.mapping is None:
            return [self.mapping(x) for x in self._value]
        return self._value
    

    @value.setter
    def value(self, v):
        if not self.reverse_mapping is None:
            self._value = [self.reverse_mapping(x) for x in v]
        else:
            self._value = v

        if not self.select is None:
            self.select.v_model = self._value
            if self.onchange: self.onchange()

        
