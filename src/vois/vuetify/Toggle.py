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
from vois.vuetify import Button
from vois.vuetify.utils.util import *
from typing import Callable, Optional


#####################################################################################################################################################
# Toggle buttons control
#####################################################################################################################################################
class Toggle(v.Row):
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
    on_change : function, optional
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
    color_selected : str, optional
        Color used for the buttons when they are selected (default is settings.color_first)
    color_unselected : str, optional
        Color used for the buttons when they are not selected (default is settings.color_second)
    dark : bool, optional
        Flag that controls the color of the text and icons in foreground (if True, the text and icons will be displayed in white, otherwise in black)
    padding_row : int, optional
        Horizontal padding among toggle buttons (1 unit means 4 pixels). Default is 1
    padding_col : int, optional
        Vertical padding among toggle buttons (1 unit means 4 pixels). Default is 2
    tile : bool, optional
        Flag to remove the buttons small border (default is False)
    large : bool, optional
        Flag that sets the large version of the button (default is False)
    x_large : bool, optional
        Flag that sets the xlarge version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    x_small : bool, optional
        Flag that sets the xsmall version of the button (default is False)

    Example
    -------
    Creation and display of a widget for the selection among 3 options::
        
        from vois.vuetify import Toggle
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()

        def onchange(index):
            with output:
                print(index)

        t = Toggle(0, ['Option 1', 'Option 2', 'Option 3'], tooltips=['Tooltip for option 1'],
                          on_change=onchange, row=False, width=150, rounded=False)

        display(t)
        display(output)


    .. figure:: figures/toggle.png
       :scale: 100 %
       :alt: toggle widget

       Toogle widget for selecting alternative options using buttons.
   """

    deprecation_alias = dict(onchange='on_change', colorselected='color_selected', colorunselected='color_unselected',
                             paddingrow='padding_row', paddingcol='padding_col', xsmall='x_small',
                             xlarge='x_large')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 index: int,
                 labels: list[str],
                 tooltips: list[str] = [],
                 icons: list[str] = [],
                 on_change: Optional[Callable[[int], None]] = None,
                 row: bool = True,
                 width: int = 150,
                 height: int = 36,
                 justify: str = 'space-between',
                 rounded: Optional[bool] = None,
                 outlined: bool = False,
                 color_selected: Optional[str] = None,
                 color_unselected: Optional[str] = None,
                 dark: Optional[bool] = None,
                 padding_row: int = 1,
                 padding_col: int = 2,
                 tile: bool = False,
                 small: bool = False,
                 x_small: bool = False,
                 large: bool = False,
                 x_large: bool = False,
                 **kwargs):

        super().__init__(class_="pa-0 ma-0", justify=self.justify, style_="overflow: hidden;", **kwargs)

        from vois.vuetify import settings

        self.index = index  # Index of the selected button
        self.labels = labels
        self.tooltips = tooltips
        self.icons = icons
        self.on_change = on_change
        self.row = row
        self.width = width
        self.height = height
        self.justify = justify
        self.rounded = rounded if rounded is not None else settings.button_rounded
        self.outlined = outlined
        self._color_selected = color_selected if color_selected is not None else settings.color_first
        self._color_unselected = color_unselected if color_unselected is not None else settings.color_second
        self._dark = dark if dark is not None else settings.dark_mode
        self.padding_row = padding_row
        self.padding_col = padding_col
        self.tile = tile
        self.small = small
        self.x_small = x_small
        self.large = large
        self.x_large = x_large

        self.__createButtons()

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Create the toggle buttons
    def __createButtons(self):

        icon_color = 'black'
        if self._dark:
            icon_color = 'white'

        self.buttons = []
        i = 0
        for label in self.labels:
            tooltip = ''
            if i < len(self.tooltips):
                tooltip = self.tooltips[i]

            icon = None
            if i < len(self.icons):
                icon = self.icons[i]

            if self.row:
                c = "pa-0 ma-0 mr-%d" % self.padding_row
            else:
                c = "pa-0 ma-0 mb-%d" % self.padding_col

            b = Button(label, dark=self._dark, class_=c, small=self.small, xsmall=self.x_small, large=self.large,
                       xlarge=self.x_large,
                       icon=icon, icon_color=icon_color,
                       on_click=self.__internal_onchange, argument=i, width=self.width, height=self.height,
                       tooltip=tooltip, selected=(i == self.index),
                       rounded=self.rounded, tile=self.tile, outlined=self.outlined,
                       color_selected=self._color_selected,
                       color_unselected=self._color_unselected)
            self.buttons.append(b)
            i += 1

        if self.row:
            self.children = self.buttons
        else:
            self.col = v.Col(cols=12, class_="pa-0 ma-0", children=[x for x in self.buttons],
                             style_="overflow: hidden;")

            self.children = [self.col]

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
            if self.on_change:
                self.on_change(self.index)

    # Get/Set the color of the selected button
    @property
    def color_selected(self):
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
        return self._color_selected

    @color_selected.setter
    def color_selected(self, color):
        for b in self.buttons:
            b.color_selected = color
            if b._selected:
                b.b.color = color

    # Get/Set the color of the unselected button
    @property
    def color_unselected(self):
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
        return self._color_unselected

    @color_unselected.setter
    def color_unselected(self, color):
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
        if self.on_change:
            self.on_change(self.index)

    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Row or v.Col widget)"""
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
