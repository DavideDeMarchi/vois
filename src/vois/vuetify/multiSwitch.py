"""Widget to select independent options using a list of buttons displayed horizontally or vertically."""
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
    from . import Button
except:
    import settings
    import tooltip
    import Button


#####################################################################################################################################################
# Multi switch  control
#####################################################################################################################################################
class multiSwitch():
    """
    Widget to select independent options using a list of buttons displayed horizontally or vertically.
        
    Parameters
    ----------
    values : list of bool
        Initial state of the buttons representing the independent options
    labels : list of strings
        Strings to be displayed as text of the options
    tooltips : list of strings, optional
        Tooltip text for the options
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    onchange : function, optional
        Python function to call when the user clicks on one of the buttons. The function will receive a parameter of list containing the status of all the buttons, from 0 to len(labels)-1
    row : bool, optional
        Flag to display the buttons horizontally or vertically (default is True)
    width : int, optional
        Width in pixels of the buttons (default is 150)
    height : int, optional
        Height in pixels of the buttons (default is 36)
    justify : str, optional
        In case of horizontal placement, applies the justify-content css property. Available options are: start, center, end, space-between and space-around.
    rounded : bool, optional
        Flag to display the buttons with a rounded shape (default is the button_rounded flag defined in the settings.py module)
    outlined : bool, optional
        Flag to display the buttons as outlined (default is True)
    colorselected : str, optional
        Color used for the buttons when they are selected (default is settings.color_first)
    colorunselected : str, optional
        Color used for the buttons when they are not selected (default is settings.color_second)
    managedblclick : bool, optional
        If True the dblclick event is managed to select a single button of the multi-switch (default is False)
    paddingrow : int, optional
        Horizontal padding among toggle buttons (1 unit means 4 pixels). Default is 1
    paddingcol : int, optional
        Vertical padding among toggle buttons (1 unit means 4 pixels). Default is 2
    tile : bool, optional
        Flag to remove the buttons small border (default is False)
    large : bool, optional
        Flag that sets the large version of the button (default is False)
    xlarge : bool, optional
        Flag that sets the xlarge version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    xsmall : bool, optional
        Flag that sets the xsmall version of the button (default is False)

    Example
    -------
    Creation and display of a widget for the selection of 3 independent options::
        
        from vois.vuetify import multiSwitch
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()

        def onchange(values):
            with output:
                print(values)

        m = multiSwitch.multiSwitch([False, True, False], ['Option 1', 'Option 2', 'Option 3'],
                                    tooltips=['Tooltip for option 1'], 
                                    onchange=onchange, row=False, width=150, rounded=False, outlined=True,
                                    colorselected='#FFA300', colorunselected='#aaaaaa')

        display(m.draw())
        display(output)


    .. figure:: figures/multiSwitch.png
       :scale: 100 %
       :alt: multiSwitch widget

       multiSwitch widget for selecting independent options using buttons.
   """

    # Initialization
    def __init__(self, values, labels, tooltips=None, color=settings.color_first, onchange=None, dark=settings.dark_mode,
                 row=True, width=150, height=36, justify='space-between', rounded=settings.button_rounded, outlined=False,
                 colorselected=settings.color_first, colorunselected=settings.color_second,
                 managedblclick=False, paddingrow=1, paddingcol=2, tile=False,
                 small=False, xsmall=False, large=False, xlarge=False):
        
        self.values   = [bool(x) for x in values]    # list of boolean values
        self.labels   = labels
        self.tooltips = tooltips
        self.color    = color
        self.dark     = dark
        self.onchange = onchange
        self.row      = row
        self.width    = width
        self.height   = height
        self.justify  = justify
        self.rounded  = rounded
        self.outlined = outlined
        self.colorselected   = colorselected
        self.colorunselected = colorunselected
        self.managedblclick  = managedblclick
        self.paddingrow = paddingrow
        self.paddingcol = paddingcol
        self.tile   = tile
        self.small  = small
        self.xsmall = xsmall
        self.large  = large
        self.xlarge = xlarge
        
        self.__createButtons()
        
        
    # Create the toggle buttons
    def __createButtons(self):

        self.buttons = []
        i = 0
        for label in self.labels:
            tooltip = ''
            if i < len(self.tooltips):
                tooltip = self.tooltips[i]
            
            if self.row: c = "pa-0 ma-0 mr-%d"%self.paddingrow
            else:
                if i == len(self.labels)-1:
                    c = "pa-0 ma-0 mb-7"
                else:
                    c = "pa-0 ma-0 mb-%d"%self.paddingcol
                    
            b = Button(label, class_=c, onclick=self.__internal_onchange, ondblclick=self.__internal_dblclick, argument=i, tooltip=tooltip, selected=self.values[i],
                              small=self.small, xsmall=self.xsmall, large=self.large, xlarge=self.xlarge, width=self.width, height=self.height,
                              rounded=self.rounded, tile=self.tile, outlined=self.outlined, dark=self.dark, colorselected=self.colorselected, colorunselected=self.colorunselected)
            self.buttons.append(b)
            i += 1

        if self.row: self.group = v.Row(class_="pa-0 ma-0", justify=self.justify, children=[x.draw() for x in self.buttons], style_="overflow: hidden;")
        else:        self.group = v.Col(cols=12, class_="pa-0 ma-0", children=[x.draw() for x in self.buttons], style_="overflow: hidden;")


    # Get the active button
    @property
    def value(self):
        """
        Get/Set the status of the multiSwitch buttons.
        
        Returns
        --------
        flags : list of booleans
            Selected status of all the options

        Example
        -------
        Programmatically set the options and print the status of the multiSwitch buttons::
            
            t.value = [False, True, True]
            print(t.value)
        
        """
        return self.values
   
    
    # Set the status of the buttons
    @value.setter
    def value(self, values):
        if len(values) == len(self.values):
            self.values = [bool(x) for x in values]
            for i in range(len(self.values)):
                self.buttons[i].selected = self.values[i]
            if self.onchange:
                self.onchange(self.values)


    # Manage onchange event
    def __internal_onchange(self, index):
        self.values[index] = not self.values[index]
        self.buttons[index].selected = self.values[index]
        if self.onchange:
            self.onchange(self.values)
            
        
    # Manage dblclick event
    def __internal_dblclick(self, index):
        if self.managedblclick:

            i = 0
            for b in self.buttons:
                if i == index: 
                    self.values[i] = True
                    b.selected = True
                else:
                    self.values[i] = False
                    b.selected = False
                    
                i += 1
                
            if self.onchange:
                self.onchange(self.values)
            
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Row or v.Col widget)"""
        return self.group

