"""Widget to select among alternative display using a list of tabs displayed horizontally or vertically."""
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
    from . import tooltip
except:
    import settings
    import tooltip


#####################################################################################################################################################
# Tabs control
#####################################################################################################################################################
class tabs:
    """
    Widget to select among alternative display using a list of tabs displayed horizontally or vertically.
        
    Parameters
    ----------
    index : int
        Index of the selected option at start (from 0 to len(labels)-1)
    labels : list of strings
        Strings to be displayed as text of the options
    contents : list of widgets, optional
        Widgets to be alternatively displayed when each of the tabs option is selected (for instance could be a list of ipywidgets.Output widgets). Default is None
    tooltips : list of strings, optional
        List of strings to be used as tooltips for the single tabs, in order (default is None)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    onchange : function, optional
        Python function to call when the user clicks on one of the tabs. The function will receive a parameter of type int containing the index of the selected tab, from 0 to len(labels)-1
    row : bool, optional
        Flag to display the tabs horizontally or vertically (default is True)
            
    Example
    -------
    Creation and display of a tabs widget to select among alternative Outputs display::
        
        from vois.vuetify import tabs
        from ipywidgets import widgets
        from IPython.display import display

        debug = widgets.Output()

        output0 = widgets.Output()
        output1 = widgets.Output()
        output2 = widgets.Output()

        with output0: print('This is output 0')
        with output1: print('This is output 1')
        with output2: print('This is output 2')

        def onchange(index):
            with debug:
                print(index)

        t = tabs.tabs(0, ['Option 0', 'Option 1', 'Option 2'],
                      contents=[output0,output1,output2],
                      onchange=onchange, row=False)

        display(t.draw())
        display(debug)

    .. figure:: figures/tabs.png
       :scale: 100 %
       :alt: tabs widget

       Creation of a tabs widget to display ipywidgets.Output content at every selection.
   """

    # Initialization
    def __init__(self, index, labels, contents=None, tooltips=None, color=None, dark=settings.dark_mode, onchange=None, row=True):
        
        self.index    = index
        self.labels   = labels
        self.onchange = onchange

        self._color = color
        if self._color is None:
            self._color = settings.color_first
        
        s = ''
        if dark:
            s = "color: %s;" % settings.textcolor_dark
            
        self.tab_list = []
        self.tab_list_with_tooltips = []
        i = 0
        for index,label in enumerate(self.labels):
            t = v.Tab(children=[label], style_=s, disabled=False)
            t.on_event('click', self.__internal_onchange)
            if isinstance(tooltips, list) and len(tooltips) > index:
                self.tab_list_with_tooltips.append(tooltip.tooltip(tooltips[index],t))
            else:
                self.tab_list_with_tooltips.append(t)
                
            self.tab_list.append(t)
            i += 1
            
        content_list = []
        if not contents is None:
            content_list = [v.TabItem(children=[x]) for x in contents]
            
        self.slider = v.TabsSlider(color=self._color, dark=dark)
        
        backcolor = 'white'
        textcolor = settings.textcolor_notdark
        if dark:
            backcolor = settings.dark_background
            textcolor = settings.textcolor_dark

        self.tabswidget = v.Tabs(v_model=self.index, vertical=not row, dense=True, class_='pa-0 ma-0', 
                                 #background_color='white', color=settings.textcolor_notdark,
                                 background_color=backcolor, color=textcolor, 
                                 children=[self.slider] + self.tab_list_with_tooltips + content_list)
        
   

    # Manage onchange event
    def __internal_onchange(self, widget, event, data):
        self.index = self.tab_list.index(widget)
        if self.onchange:
            self.onchange(self.index)
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Tabs widget)"""
        return self.tabswidget

    
    # Get the active tab
    @property
    def value(self):
        """
        Get/Set the active tab index.
        
        Returns
        --------
        index : int
            Index of the selected tab (from 0 to len(labels)-1)

        Example
        -------
        Programmatically select one of the tab and print the index of the selected option::
            
            t.value = 2
            print(t.value)
        
        """
        return self.index
   
    
    # Set the active button
    @value.setter
    def value(self, index):
        if index >= 0 and index < len(self.labels):
            self.index = index
            self.tabswidget.v_model = self.index
            if self.onchange:
                self.onchange(self.index)

                
    # disabled property
    @property
    def disabled(self):
        """
        Get/Set the disabled state.
        """
        return max([x.disabled for x in self.tab_list])
    
    @disabled.setter
    def disabled(self, flag):
        for tab in self.tab_list:
            tab.disabled = flag
            
            
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
            