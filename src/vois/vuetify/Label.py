"""Label widget to display a text with an optional icon."""
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

from vois.vuetify import tooltip, fontsettings
from vois.vuetify.utils.util import *

from typing import Callable, Optional, Any


#####################################################################################################################################################
# Label class that can display also an icon
#####################################################################################################################################################
class Label(v.Html):
    """
    Label widget to display a text with an optional icon.
        
    Parameters
    ----------
    text : str
        Test string to be displayed on the label widget
    onclick : function, optional
        Python function to call when the user clicks on the label. The function will receive as parameter the value of the argument (default is None)
    argument : any, optional
        Argument to be passed to the onclick function when user click on the label (default is None)
    disabled : bool, optional
        Flag to show the label as disabled (default is False)
    text_weight : int, optional
        Weight of the text to be shown in the label (default is 350, Bold is any value greater or equal to 500)
    height : int, optional
        Height of the label widget in pixels (default is 20)
    margins : int, optional
        Dimension of the margins on all directions (default is 0)
    margin_top : int, optional
        Dimension of the margin on top of the label (default is None)
    icon: str, optional
        Name of the icon to display aside the text of the label (default is None)
    icon_large : bool, optional
        Flag that sets the large version of the icon (default is False)
    icon_small : bool, optional
        Flag that sets the small version of the icon (default is False)
    icon_left : bool, optional
        Flag that sets the position of the icon  to the left of the text of the label (default is False)
    icon_color : str, optional
        Color of the icon (default is 'black')
    tooltip_text : str, optional
        Tooltip string to display when the user hovers on the label (default is None)
    text_color : str, optional
        Color used for the label text
    back_color : str, optional
        Color used for the background of the label
    dark : bool, optional
        Flag to invert the text and back_color (default is the value of settings.dark_mode)
            

    Note
    ----
    All the icons from https://materialdesignicons.com/ site can be used, just by prepending 'mdi-' to their name.
    
    All the free icons from https://fontawesome.com/ site can be used, just by prepending 'fa-' to their name.


    Example
    -------
    Creation and display of a label widget containing an icon::
        
        from vois.vuetify import Label

        lab = Label('Test label', text_weight=300, margins=2,
                      icon='mdi-car-light-high', icon_color='red',
                      icon_large=True, height=22)

        display(lab)
    
    
    .. figure:: figures/label.png
       :scale: 100 %
       :alt: label widget

       Example of a label widget with text and an icon.
   """

    # Initialization
    deprecation_alias = dict(textweight='text_weight', margintop='margin_top', iconlarge='icon_large',
                             iconsmall='icon_small', iconleft='icon_left', iconcolor='icon_color',
                             textcolor='text_color', onclick='on_click', backcolor='back_color')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 text: str,
                 on_click: Optional[Callable[[Optional[Any]], None]] = None,
                 argument: Optional[Any] = None,
                 disabled: bool = False,
                 text_weight: int = 350,
                 height: int = 20,
                 margins: int = 0,
                 margin_top: Optional[int] = None,
                 icon: Optional[str] = None,
                 icon_large: bool = False,
                 icon_small: bool = False,
                 icon_left: bool = False,
                 icon_color: str = 'black',
                 tooltip_text: Optional[str] = None,
                 text_color: Optional[str] = None,
                 back_color: Optional[str] = None,
                 dark: Optional[str] = None,
                 **kwargs):

        super().__init__(tag='div', **kwargs)

        from vois.vuetify import settings

        self.labeltext = text
        self.on_click = on_click
        self.argument = argument

        self.disabled = disabled
        self.text_weight = text_weight
        self.height = height
        self.margins = margins
        self.margin_top = margin_top

        self.icon = icon
        self.icon_left = icon_left
        self.icon_large = icon_large
        self.icon_small = icon_small
        self.icon_color = icon_color

        self.tooltip_text = tooltip_text

        self.text_color = text_color
        self.back_color = back_color
        self.dark = dark if dark is not None else settings.dark_mode

        if not self.dark is None:
            if self.dark:
                if self.back_color is None:
                    self.back_color = '#111111'
                if self.text_color is None:
                    self.text_color = 'white'

        self.__createLabel()

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Create the label
    def __createLabel(self):
        if self.icon is None:
            childs = [self.labeltext]
        else:
            childs = [self.labeltext,
                      v.Icon(left=self.icon_left, large=self.icon_large, small=self.icon_small, color=self.icon_color,
                             children=[self.icon])]

        strstyle = 'font-family: %s; font-size: 10; font-weight: %d; text-transform: none;' % (
            fontsettings.font_name, self.text_weight)
        if not self.text_color is None:
            strstyle += 'color: %s;' % self.text_color
        if not self.back_color is None:
            strstyle += 'background-color: %s;' % self.back_color

        self.item = v.Card(disabled=self.disabled, elevation=0, height=self.height, depressed=True, children=childs,
                           style_=strstyle)
        if not self.tooltip_text is None:
            self.item = tooltip.tooltip(self.tooltip_text, self.item)

        # If requested onclick management
        if not self.on_click is None:
            self.item.on_event('click', self.__internal_onclick)

        if not self.margin_top is None:
            self.container = v.Container(class_="pa-0 ma-%s mt-%s" % (str(self.margins), str(self.margin_top)),
                                         children=[self.item])
        else:
            self.container = v.Container(class_="pa-0 ma-%s" % (str(self.margins)), children=[self.item])

        self.children = [self.container]

    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.on_click:
            if not self.argument is None:
                self.on_click(self.argument)
            else:
                self.on_click()

    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self

    # Get the label text
    @property
    def text(self):
        """
        Get/Set the label text.
        
        Returns
        --------
        text : str
            Text currently shown in the label

        Example
        -------
        Programmatically set the label text (needs a re-display to be visible!)::
            
            lab.text = 'New text for the label'
            display(lab.draw())
            print(lab.text)
        
        """
        return self.labeltext

    # Set the label text
    @text.setter
    def text(self, new_text):
        self.labeltext = new_text
        self.__createLabel()
