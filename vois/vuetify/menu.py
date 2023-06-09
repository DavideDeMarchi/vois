"""Menu widget opened on hover on a button."""
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
# Menu control
#####################################################################################################################################################
class menu:
    """
    Menu widget opened on hover on a button.
        
    Parameters
    ----------
    index : int
        Index of the option initially selected (from 0 to len(labels)-1)
    title : str
        Title string to display in the button
    labels : list of strings
        Strings to be displayed as options in the menu widget
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    onchange : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive a single parameter, containing the index of the selected option in the range from 0 to len(labels)-1
    width : int, optional
        Width of the button in pixels (default is 150 pixels)
    highliteselection: bool, optional
        If True, the menu will show the selected option in bold (default is True)
            
    Example
    -------
    Creation and display of a menu widget to select among three options::
        
        from vois.vuetify import menu
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        m = menu.menu(0, 'Hover to select',
                      ['Option 0', 'Option 1', 'Option 2'],
                      onchange=onchange, highliteselection=True)

        display(m.draw())
        display(output)

    .. figure:: figures/menu.png
       :scale: 100 %
       :alt: menu widget

       Example of a menu widget to select from three options.
   """

    # Initialization
    def __init__(self, index, title, labels, color=settings.color_first, onchange=None, width=150, highliteselection=True):
        
        self.index    = index
        self.title    = title
        self.labels   = labels
        self.color    = color
        self.onchange = onchange
        self.width    = width
        
        
        self.style_normal = 'font-family: %s; font-weight:400;' % (fontsettings.font_name)
        if highliteselection: self.style_selected = 'font-family: %s; font-weight:700;' % (fontsettings.font_name)
        else:                 self.style_selected = self.style_normal
        
        # Create the controls
        self.items = []
        i = 0
        for label in self.labels:
            item = v.ListItem(children=[label])
            if i == self.index: item.style_ = self.style_selected
            else:               item.style_ = self.style_normal
                
            self.items.append(item)
            item.on_event('click', self.__internal_onchange)
            i += 1

        self.menu = v.Menu(offset_y=True, open_on_hover=True, dense=True,
                           v_slots=[{
                                  'name': 'activator',
                                  'variable': 'menuData',
                                  'children': v.Btn(v_on='menuData.on', depressed=True, large=False, dense=True, class_='pa-0 ma-0', color=settings.color_first,
                                                    rounded=True, height=36, width=self.width,
                                                    style_='font-family: %s; text-transform: none' % (fontsettings.font_name), children=[self.title]),
                                   }],
                           children=[v.List(children=self.items)] )

    
    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.index >= 0 and self.index < len(self.items):
            self.items[self.index].style_ = self.style_normal
        self.index = self.items.index(widget)
        self.items[self.index].style_ = self.style_selected
        if self.onchange:
            self.onchange(self.index)
    
    
    # Get the active option
    @property
    def value(self):
        """
        Get/Set the active option index.
        
        Returns
        --------
        index : int
            Index of the selected option (from 0 to len(labels)-1)

        Example
        -------
        Programmatically select one of the options and print the index of the selected option::
            
            m.value = 2
            print(m.value)
        
        """
        return self.index
   
    
    # Set the active option
    @value.setter
    def value(self, index):
        if index >= 0 and index < len(self.items):
            if self.index >= 0 and self.index < len(self.items):
                self.items[self.index].style_ = self.style_normal
            self.index = index
            self.items[self.index].style_ = self.style_selected
            if self.onchange:
                self.onchange(self.index)
                
                
    # Returns the vuetify object to display (the v.Menu itself)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Menu widget)"""
        return self.menu

