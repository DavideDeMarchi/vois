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
import ipyvuetify as v

from vois.vuetify import Button

from vois.vuetify.utils.util import *

from typing import Callable, Optional


#####################################################################################################################################################
# Multi switch  control
#####################################################################################################################################################
class MultiSwitch(v.Html):
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
    on_change : function, optional
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
    color_selected : str, optional
        Color used for the buttons when they are selected (default is settings.color_first)
    color_unselected : str, optional
        Color used for the buttons when they are not selected (default is settings.color_second)
    manage_dbl_click : bool, optional
        If True the dblclick event is managed to select a single button of the multi-switch (default is False)
    padding_row : int, optional
        Horizontal padding among toggle buttons (1 unit means 4 pixels). Default is 1
    padding_col : int, optional
        Vertical padding among toggle buttons (1 unit means 4 pixels). Default is 2
    tile : bool, optional
        Flag to remove the buttons small border (default is False)
    large : bool, optional
        Flag that sets the large version of the button (default is False)
    x_large : bool, optional
        Flag that sets the x_large version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    x_small : bool, optional
        Flag that sets the x_small version of the button (default is False)

    Example
    -------
    Creation and display of a widget for the selection of 3 independent options::
        
        from vois.vuetify import MultiSwitch
        from ipywidgets import widgets
        from IPython.display import display
        
        output = widgets.Output()

        def on_change(values):
            with output:
                print(values)

        m = MultiSwitch([False, True, False], ['Option 1', 'Option 2', 'Option 3'],
                                    tooltips=['Tooltip for option 1'], 
                                    on_change=on_change, row=False, width=150, rounded=False, outlined=True,
                                    color_selected='#FFA300', color_unselected='#aaaaaa')

        display(m)
        display(output)


    .. figure:: figures/multiSwitch.png
       :scale: 100 %
       :alt: multiSwitch widget

       multiSwitch widget for selecting independent options using buttons.
   """

    # Initialization
    deprecation_alias = dict(onchange='on_change', colorselected='color_selected', colorunselected='color_unselected',
                             managedblclick='manage_dbl_click', paddingrow='padding_row', paddingcol='padding_col',
                             xsmall='x_small', xlarge='x_large')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 values: list[bool],
                 labels: list[str],
                 tooltips: list[str],
                 color: Optional[str] = None,
                 on_change: Optional[Callable[[list[bool]], None]] = None,
                 dark: Optional[bool] = None,
                 row: bool = True,
                 width: int = 150,
                 height: int = 36,
                 justify: str = 'space-between',
                 rounded: Optional[bool] = None,
                 outlined: bool = False,
                 color_selected: Optional[str] = None,
                 color_unselected: Optional[str] = None,
                 manage_dbl_click: bool = False,
                 padding_row: int = 1,
                 padding_col: int = 2,
                 tile: bool = False,
                 small: bool = False,
                 x_small: bool = False,
                 large: bool = False,
                 x_large: bool = False,
                 **kwargs):

        from vois.vuetify import settings

        super().__init__(tag='div', **kwargs)

        # self.style_ = 'padding: 0px; margin: 0px; ' + self.style_

        self.values = [bool(x) for x in values]  # list of boolean values
        self.labels = labels
        self.tooltips = tooltips
        self.color = color if color is not None else settings.color_first
        self.dark = dark if dark is not None else settings.dark_mode
        self.on_change = on_change
        self.row = row
        self.width = width
        self.height = height
        self.justify = justify
        self.rounded = rounded if rounded is not None else settings.button_rounded
        self.outlined = outlined
        self.color_selected = color_selected if color_selected is not None else settings.color_first
        self.color_unselected = color_unselected if color_unselected is not None else settings.color_second
        self.manage_dbl_click = manage_dbl_click
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

        self.buttons = []
        i = 0
        for label in self.labels:
            tooltip = ''
            if i < len(self.tooltips):
                tooltip = self.tooltips[i]

            if self.row:
                c = "pa-0 ma-0 mr-%d" % self.padding_row
            else:
                if i == len(self.labels) - 1:
                    c = "pa-0 ma-0 mb-7"
                else:
                    c = "pa-0 ma-0 mb-%d" % self.padding_col

            b = Button(label,
                       class_=c,
                       # text_color=self.color,
                       on_click=self.__internal_onchange,
                       on_dblclick=self.__internal_dblclick,
                       argument=i,
                       tooltip=tooltip,
                       selected=self.values[i],
                       small=self.small,
                       x_small=self.x_small,
                       large=self.large,
                       x_large=self.x_large,
                       width=self.width,
                       height=self.height,
                       rounded=self.rounded,
                       tile=self.tile,
                       outlined=self.outlined,
                       dark=self.dark,
                       color_selected=self.color_selected,
                       color_unselected=self.color_unselected)
            self.buttons.append(b)
            i += 1

        if self.row:
            self.group = v.Row(class_="pa-0 ma-0", justify=self.justify, children=[x for x in self.buttons],
                               style_="overflow: hidden;")
        else:
            self.group = v.Col(cols=12, class_="pa-0 ma-0", children=[x for x in self.buttons],
                               style_="overflow: hidden;")

        self.children = [self.group]

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
            if self.on_change:
                self.on_change(self.values)

    # Manage on_change event
    def __internal_onchange(self, index):
        self.values[index] = not self.values[index]
        self.buttons[index].selected = self.values[index]
        if self.on_change:
            self.on_change(self.values)

    # Manage dblclick event
    def __internal_dblclick(self, index):
        if self.manage_dbl_click:

            i = 0
            for b in self.buttons:
                if i == index:
                    self.values[i] = True
                    b.selected = True
                else:
                    self.values[i] = False
                    b.selected = False

                i += 1

            if self.on_change:
                self.on_change(self.values)

    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Row or v.Col widget)"""
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
