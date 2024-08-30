"""Widget to select among alternative options using a list of buttons displayed horizontally or vertically."""
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
import ipyvuetify as v

try:
    from . import settings
    # from . import Button
except:
    import settings
    # import Button

from vois.vuetify import Button

#####################################################################################################################################################
# Toggle buttons control
#####################################################################################################################################################
class toggle():
    """
    Widget to select among alternative options using a list of buttons displayed horizontally or vertically.
        
    Parameters
    ----------
    index : int
        Index of the selected option at start (from 0 to len(labels)-1)
    labels : list of strings
        Strings to be displayed as text of the options
    tooltips : list of strings, optional
        Tooltip text for the options (default is the empty list)
    icons : list of strings, optional
        Icons for the options (default is the empty list)
    onchange : function, optional
        Python function to call when the user clicks on one of the buttons. The function will receive a parameter of type int containing the index of the clicked button, from 0 to len(labels)-1
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
        Flag to display the buttons as outlined (default is False)
    colorselected : str, optional
        Color used for the buttons when they are selected (default is settings.color_first)
    colorunselected : str, optional
        Color used for the buttons when they are not selected (default is settings.color_second)
    dark : bool, optional
        Flag that controls the color of the text and icons in foreground (if True, the text and icons will be displayed in white, otherwise in black)
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
    Creation and display of a widget for the selection among 3 options::
        
        from vois.vuetify import toggle
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()

        def onchange(index):
            with output:
                print(index)

        t = toggle.toggle(0, ['Option 1', 'Option 2', 'Option 3'], tooltips=['Tooltip for option 1'], 
                          onchange=onchange, row=False, width=150, rounded=False)

        display(t.draw())
        display(output)


    .. figure:: figures/toggle.png
       :scale: 100 %
       :alt: toggle widget

       Toogle widget for selecting alternative options using buttons.
   """

    # Initialization
    def __init__(self, index, labels, tooltips=[], icons=[], onchange=None,
                 row=True, width=150, height=36, justify='space-between', rounded=settings.button_rounded, outlined=False,
                 colorselected=settings.color_first, colorunselected=settings.color_second, dark=settings.dark_mode,
                 paddingrow=1, paddingcol=2, tile=False, small=False, xsmall=False, large=False, xlarge=False):
        
        self.index      = index    # Index of the selected button
        self.labels     = labels
        self.tooltips   = tooltips
        self.icons      = icons
        self.onchange   = onchange
        self.row        = row
        self.width      = width
        self.height     = height
        self.justify    = justify
        self.rounded    = rounded
        self.outlined   = outlined
        self._colorselected   = colorselected
        self._colorunselected = colorunselected
        self._dark            = dark
        self.paddingrow       = paddingrow
        self.paddingcol       = paddingcol
        self.tile   = tile
        self.small  = small
        self.xsmall = xsmall
        self.large  = large
        self.xlarge = xlarge
        
        self.__createButtons()
        
        
    # Create the toggle buttons
    def __createButtons(self):

        iconcolor = 'black'
        if self._dark:
            iconcolor = 'white'
                
        self.buttons = []
        i = 0
        for label in self.labels:
            tooltip = ''
            if i < len(self.tooltips):
                tooltip = self.tooltips[i]

            icon = None
            if i < len(self.icons):
                icon = self.icons[i]
                
                
            if self.row: c = "pa-0 ma-0 mr-%d"%self.paddingrow
            else:        c = "pa-0 ma-0 mb-%d"%self.paddingcol
                    
            b = Button(label, dark=self._dark, class_=c, small=self.small, xsmall=self.xsmall, large=self.large, xlarge=self.xlarge,
                       icon=icon, icon_color=iconcolor,
                       onclick=self.__internal_onchange, argument=i, width=self.width, height=self.height, tooltip=tooltip, selected=(i==self.index),
                       rounded=self.rounded, tile=self.tile, outlined=self.outlined, colorselected=self._colorselected, colorunselected=self._colorunselected)
            self.buttons.append(b)
            i += 1

        if self.row: self.group = v.Row(class_="pa-0 ma-0", justify=self.justify, children=[x.draw() for x in self.buttons], style_="overflow: hidden;")
        else:        self.group = v.Col(cols=12, class_="pa-0 ma-0", children=[x.draw() for x in self.buttons], style_="overflow: hidden;")


    # Get the active button
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
            
            t.value = 2
            print(t.value)
        
        """
        return self.index
   
    
    # Set the active button
    @value.setter
    def value(self, index):
        if index >= 0 and index < len(self.buttons):
            self.buttons[self.index].selected = False
            self.index = index
            self.buttons[self.index].selected = True
            if self.onchange:
                self.onchange(self.index)
            

    # Get/Set the color of the selected button
    @property
    def colorselected(self):
        """
        Get/Set the color of the selected button.
        
        Returns
        --------
        color : str
            Color of the selected button

        Example
        -------
        Programmatically change the color of the selected button::
            
            t.colorselected = '#ff0000'
            print(t.colorselected)
        
        """
        return self._colorselected
   
    
    @colorselected.setter
    def colorselected(self, color):
        for b in self.buttons:
            b.color_selected = color
            if b._selected:
                b.b.color = color
                
                
    # Get/Set the color of the unselected button
    @property
    def colorunselected(self):
        """
        Get/Set the color of the unselected buttons.
        
        Returns
        --------
        color : str
            Color of the unselected buttons

        Example
        -------
        Programmatically change the color of the unselected buttons::
            
            t.colorunselected = '#ff0000'
            print(t.colorunselected)
        
        """
        return self._colorunselected
   
    
    @colorunselected.setter
    def colorunselected(self, color):
        for b in self.buttons:
            b.color_unselected = color
            if not b._selected:
                b.b.color = color
                
                
    # Get/Set the dark mode
    @property
    def dark(self):
        """
        Get/Set the dark mode of the buttons.
        
        Returns
        --------
        flag : bool
            If True the text and the icons are displayed in white color, otherwise in black color

        Example
        -------
        Programmatically change the dark mode::
            
            t.dark = Fals
            print(t.dark)
        
        """
        return self._dark
   
    
    @dark.setter
    def dark(self, flag):
        self._dark = flag
        
        for b in self.buttons:
            b.dark = self._dark
                
                
    # Manage onchange event
    def __internal_onchange(self, index):
        self.buttons[self.index].selected = False
        self.index = index
        self.buttons[self.index].selected = True
        if self.onchange:
            self.onchange(self.index)
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Row or v.Col widget)"""
        return self.group

