"""Single selection widget from a dropdown list."""
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
# Class to display a single selection widget
#####################################################################################################################################################
class selectSingle():
    """
    Single selection widget from a dropdown list. Passing the parameter newvalues_enabled=True enables the user to insert new strings in the widget.
        
    Parameters
    ----------
    label : str
        Help text to display 
    values : list of strings
        Strings to be displayed in the dropdown list of the widget 
    selection : str, optional
        String that is initially selected (default is '')
    mapping : function, optional
        Python function to call to transform the visible strings into codes (for example names of countries to their iso2 codes)
    reverse_mapping : function, optional
        Python function to call to transform the codes into visible strings (for example iso2 codes of countries to their names)
    onchange : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive no parameter (use value property to retrieve the current selection)
    width : int, optional
        Width in pixel of the widget (default is 300 pixels)
    clearable : bool, optional
        Flag that controls if the widget should show to the user the 'X' button to clear its content (default is True)
    marginy : int, optional
        Margin in y coordinates to position the widget from top (default is 1)
    newvalues_enabled : bool, optional
        Flag that enables the user to insert new values beside those listed in the dropdown (default is False)
    newvalues_type : str, optional
        Type of the new values that the user can add in case newvalues_enabled is True (default is 'text')
    colorbackground : bool, optional
        Flag that controls the filling of the widget background with color when a value of the list is selected (default is False)
    color : str, optional
        Foreground color of the widget (default is settings.color_first)
            
    Example
    -------
    Creation and display of a single select widget for the selection of a country::
        
        from vois.vuetify import selectSingle
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def onchange():
            with output:
                print(sel.value)

        sel = selectSingle.selectSingle('Country:',
                                        ['Belgium', 'France', 'Italy', 'Germany'],
                                        selection='France',
                                        width=200,
                                        onchange=onchange)
        sel.draw()

    .. figure:: figures/selectSingle.png
       :scale: 100 %
       :alt: selectSingle widget

       Example of a selectSingle widget to select from a list of countries.
   """
    
    # Initialization
    def __init__(self, label, values, selection='', mapping=None, reverse_mapping=None, width=300, onchange=None, clearable=True, marginy=1,
                       newvalues_enabled=False, newvalues_type='text', colorbackground=False, color=None):
        
        self.label           = label
        self.values          = values
        self.mapping         = mapping           # Function to convert names to codes
        self.reverse_mapping = reverse_mapping   # Function to convert codes to names
        self.width           = width
        self.onchange        = onchange

        self.select = None
        self.value = selection
        
        self.colorbackground = colorbackground
        
        self._color = color
        if self._color is None:
            self._color = settings.color_first
        
        color,backcolor = self.__getColors()
        if newvalues_enabled:
            self.select = v.Combobox(v_model=self._value, label=self.label, dense=True, solo=False, outlined=True, multiple=False, chips=False, clearable=clearable, 
                                     item_color=self._color, color=self._color, class_='pa-0 mx-0 my-%d mb-n4' % marginy,
                                     background_color=backcolor,
                                     items=self.values, style_='max-width: %dpx; font-family: %s; font-weight:400; text-transform: none' % (self.width, fontsettings.font_name),
                                     type_=newvalues_type, autofocus=False, disabled=False)
            #self.select.on_event('keydown', self.__internal_onchange)
            #self.select.on_event('change', self.__internal_onchange)
        else:
            self.select = v.Select(v_model=self._value, label=self.label, dense=True, solo=False, outlined=True, multiple=False, chips=False, clearable=clearable, 
                                   item_color=self._color, color=self._color, class_='pa-0 mx-0 my-%d mb-n4' % marginy,
                                   background_color=backcolor, # menu_props="{ auto: true, maxHeight: 600 }",  # menu_props seems not working!
                                   items=self.values, style_='max-width: %dpx; font-family: %s; font-weight:400; text-transform: none' % (self.width, fontsettings.font_name), disabled=False)
        
        self.select.on_event('input', self.__internal_onchange)
        
        
    def __getColors(self):
        color     = self._color
        backcolor = 'white'
        if self.colorbackground and not self._value is None and len(str(self._value)) > 0 and self._value in self.values:
            color     = settings.select_textcolor
            backcolor = self._color
        return color,backcolor
        
        
    def __internal_onchange(self, widget, event, data):
        self._value = self.select.v_model
        color,backcolor = self.__getColors()
        self.select.color = color
        self.select.background_color = backcolor
        if self.onchange: self.onchange()

    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html widget that contains a v.Select or a v.Combobox as its unique child)"""
        return v.Html(tag='div',children=[self.select], style_='overflow: hidden;')

    
    # value property
    @property
    def value(self):
        """
        Get/Set the selected value.
        
        Returns
        --------
        v : str
            text of the item currently selected

        Example
        -------
        Programmatically select one value::
            
            sel.value = 'Italy'
            print(sel.value)
        
        """
        if not self.mapping is None:
            return self.mapping(self._value)
        return self._value
    
    @value.setter
    def value(self, v):
        if not self.reverse_mapping is None:
            newv = self.reverse_mapping(v)
        else:
            newv = v
        
        if newv in self.values:
            self._value = newv

            if not self.select is None:
                self.select.v_model = self._value
                if self.onchange: self.onchange()
        else:
            if newv is None or len(newv) == 0:
                self._value = ''
            else:
                raise ValueError('Trying to set a value that is not in the list of allowed values.')


    # disabled property
    @property
    def disabled(self):
        """
        Get/Set the disabled state.
        """
        return self.select.disabled
    
    @disabled.setter
    def disabled(self, flag):
        self.select.disabled = flag
        

    # color property
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
            color,backcolor = self.__getColors()
            self.select.color     = c
            self.background_color = backcolor
        