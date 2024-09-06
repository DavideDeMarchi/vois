"""Button widget to call a python function when clicked."""
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

from vois.vuetify.utils.util import *
from typing import Callable, Any, Union, Optional


#######################################################################################################################
# Button class. On click python function called when clicked
# Uses settings font to display the button text and interactivity when hover
#######################################################################################################################
class Button(v.Html):
    """
    Button widget to call a python function when clicked.
        
    Parameters
    ----------
    text : str
        Test string to be displayed on the button widget
    on_click : function, optional
        Python function to call when the user clicks on the button. The function will receive as parameter the value of the argument (default is None)
    on_dblclick : function, optional
        Python function to call when the user double-clicks on the button. The function will receive as parameter the value of the argument (default is None)
    argument : any, optional
        Argument to be passed to the onclick function when user click on the label (default is None)
    width : int, optional
        Width of the button widget in pixels (default is 100)
    height : int, optional
        Height of the button widget in pixels (default is 36)
    selected : bool, optional
        Flag to show the button as selected (default is False)
    disabled : bool, optional
        Flag to show the button as disabled (default is False)
    tooltip : str, optional
        Tooltip text to show when the user hovers on the button (default is '')
    large : bool, optional
        Flag that sets the large version of the button (default is False)
    x_large : bool, optional
        Flag that sets the xlarge version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    x_small : bool, optional
        Flag that sets the xsmall version of the button (default is False)
    outlined : bool, optional
        Flag to show the button as outlined (default is False)
    text_weight : int, optional
        Weight of the text to be shown in the label (default is 500, Bold is any value greater or equal to 500)
    href : str, optional
        URL to open when the button is clicked (default is None)
    target : str, optional
        Designates the target attribute (where the URL page is opened, for instance: '_blank' to open it in a new browser tab). This should only be applied when using the href parameter (default is None)
    only_text : bool, optional
         If True, the button will contain only the text (default is False)
    text_color : str, optional
        Color used for the button text (default is None)
    icon: str, optional
        Name of the icon to display aside the text of the label (default is None)
    icon_large : bool, optional
        Flag that sets the large version of the icon (default is False)
    icon_small : bool, optional
        Flag that sets the small version of the icon (default is False)
    icon_left : bool, optional
        Flag that sets the position of the icon  to the left of the text of the label (default is False)
    icon_color : str, optional
        Color of the icon (default is 'black' if settings.dark_mode is False and 'white if settings.dark_mode is True)
    auto_select : bool, optional
        If True, the button becomes selected when clicked (default is False)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    rounded : bool, optional
        Flag to display the button with rounded corners (default is the value of settings.button_rounded)
    tile : bool, optional
        Flag to remove the button small border (default is False)
    color_selected : str, optional
        Color used for the button when it is selected (default is settings.color_first)
    color_unselected : str, optional
        Color used for the button when it is not selected (default is settings.color_second)
            
    Note
    ----
    All the icons from https://materialdesignicons.com/ site can be used, just by prepending 'mdi-' to their name.
    
    All the free icons from https://fontawesome.com/ site can be used, just by prepending 'fa-' to their name.
    
    
    Example
    -------
    Creation and display of a some button widgets playing with the parameters::
        
        from vois.vuetify import settings, Button

        def onclick(arg=None):
            if arg==1: b1.selected = not b1.selected
            if arg==2: b2.selected = not b2.selected
            else:      b3.selected = not b3.selected

        b1 = Button('Test button 1', text_weight=300, on_click=onclick, argument=1,
                    width=150, height=36, 
                    tooltip='Tooltip for button 1', selected=False, rounded=True,
                    icon='mdi-car-light-high', iconColor='black')

        b2 = Button('Test button 2', text_weight=450, on_click=onclick, argument=2,
                    width=150, height=48,
                    tooltip='Tooltip for button 2', selected=True, rounded=False)

        b3 = Button('Test button 3', text_weight=450, on_click=onclick, argument=3,
                    width=150, height=38,
                    text_color=settings.color_first,
                    tooltip='Tooltip for button 3', outlined=True, rounded=True)

        b4 = Button('Contacts', only_text=True, text_color=settings.color_first,
                    width=150, height=28,
                    href='https://ec.europa.eu/info/contact_en', target="_blank",
                    tooltip='Open a URL')

        display(b1)
        display(b2)
        display(b3)
        display(b4)


    .. figure:: figures/button.png
       :scale: 100 %
       :alt: button widget

       Example of a 4 button widgets with different display modes.
   """
    deprecation_alias = dict(onclick='on_click', xlarge='x_large', xsmall='x_small', textweight='text_weight',
                             onlytext='only_text', textcolor='text_color', iconlarge='icon_large',
                             iconsmall='icon_small',
                             iconleft='icon_left', iconcolor='icon_color', autoselect='auto_select',
                             colorselected='color_selected', colorunselected='color_unselected',
                             ondblclick='on_dblclick')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self, text: str,
                 on_click: Optional[Union[Callable[[], None], Callable[[dict[str, Any]], None]]] = None,
                 argument: Optional[Any] = None,  # TODO forzare a dict per **kwargs
                 width: int = 100,
                 height: int = 36,
                 selected: bool = False,
                 disabled: bool = False,
                 tooltip: str = '',
                 large: bool = False,
                 x_large: bool = False,
                 small: bool = False,
                 x_small: bool = False,
                 outlined: bool = False,
                 text_weight: int = 500,
                 href: Optional[str] = None,
                 target: Optional[str] = None,
                 only_text: bool = False,
                 text_color: Optional[str] = None,
                 class_: str = "pa-0 ma-0",
                 icon: Optional[str] = None,
                 icon_large: bool = False,
                 icon_small: bool = False,
                 icon_left: bool = False,
                 icon_color: str = None,
                 auto_select: bool = False,
                 dark: bool = None,
                 rounded: bool = None,
                 tile: bool = False,
                 color_selected: str = None,
                 color_unselected: str = None,
                 on_dblclick: Optional[Union[Callable[[], None], Callable[[dict[str, Any]], None]]] = None,
                 style_: str = '',
                 **kwargs) -> None:

        from vois.vuetify import settings, fontsettings
        
        super().__init__(**kwargs)

        self.on_click = on_click
        self.on_dblclick = on_dblclick
        self.argument = argument
        self._selected = selected
        self._disabled = disabled
        self.auto_select = auto_select
        self._text = text
        self.icon_large = icon_large
        self.icon_small = icon_small
        self._color_selected   = settings.color_first  if color_selected is None else color_selected
        self._color_unselected = settings.color_second if color_unselected is None else color_unselected
        self._dark             = settings.dark_mode if dark is None else dark
        self._rounded          = settings.button_rounded if rounded is None else rounded
        if icon_color is None:
            self.icon_color = 'white' if settings.dark_mode else 'black'
        else:
            self.icon_color = icon_color
                
        self._icon = icon

        self.icon_distance = " ml-2"

        if text_color:
            color = text_color
        else:
            color = self._color_selected if self._selected else self._color_unselected

        if self._icon is None:
            childs = [self._text]
        else:
            if not self._text:
                self.icon_distance = ""
            elif icon_left:
                self.icon_distance = " mr-2"

            icn = v.Icon(class_="pa-0 ma-0 %s" % self.icon_distance, large=self.icon_large, small=self.icon_small,
                         color=self.icon_color, children=[self._icon])
            if icon_left:
                if not self._text:
                    childs = [icn]
                else:
                    childs = [icn, self._text]
            else:
                if not self._text:
                    childs = [icn]
                else:
                    childs = [self._text, icn]

        self.b = v.Btn(color=color, dark=self._dark, icon=only_text, depressed=True, outlined=outlined, large=large,
                       x_large=x_large, small=small, x_small=x_small,
                       disabled=disabled, width=width, min_width=width, height=height, min_height=height, href=href,
                       target=target, tile=tile,
                       children=childs,
                       style_='font-family: %s; font-size: 17; font-weight: %d; text-transform: none; ' % (
                           fontsettings.font_name, text_weight) + style_,
                       rounded=self._rounded)

        self.b.on_event('click', self.__internal_onclick)
        self.b.on_event('dblclick', self.__internal_ondblclick)

        if len(tooltip) > 0:
            self.b.v_on = 'tooltip.on'
        self.container = v.Container(class_=class_, children=[
            v.Tooltip(color=settings.tooltip_backcolor, transition="scale-transition", bottom=True,
                      v_slots=[{'name': 'activator', 'variable': 'tooltip', 'children': self.b}],
                      children=[tooltip])])

        self.tag = 'div'
        self.children = [self.container]

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self

    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.on_click:
            if self.argument is not None:
                self.on_click(self.argument)  # TODO switch to kwargs
            else:
                self.on_click()
        if self.auto_select:
            self.selected = True

    # Manage dblclick event
    def __internal_ondblclick(self, widget=None, event=None, data=None):
        if self.on_dblclick:
            if self.argument:  # TODO usare argument diversi da onclick
                self.on_dblclick(self.argument)
            else:
                self.on_dblclick()

    @property
    def selected(self):
        """
        Get/Set the selected state of the button widget.
        
        Returns
        --------
        selected status : bool
            True if the button is selected, False otherwise

        Example
        -------
        Programmatically select a button::
            
            b.selected = True
            print(b.selected)
        """
        return self._selected

    @selected.setter
    def selected(self, flag):
        self._selected = bool(flag)
        if self._selected: color = self._color_selected
        else:              color = self._color_unselected
        self.b.color = color

        
    @property
    def disabled(self):
        """
        Get/Set the disabled state of the button widget.
        
        Returns
        --------
        disabled status : bool
            True if the button is disabled, False otherwise
        """
        return self._disabled

    @disabled.setter
    def disabled(self, flag):
        self._disabled = bool(flag)
        self.b.disabled = self._disabled

    # Change the icon for the button
    def setIcon(self, iconname):  # TODO da fare come text
        """
        Change the icon for the button

        Example
        -------
        Creation of a button and programmatically change its icon::
                
            from vois.vuetify import settings, button
            
            b = Button('Test button', text_weight=450, width=150, height=46,
                       selected=True, rounded=True,
                       icon='mdi-menu-open', icon_color='black', icon_large=True)
            display(b.draw())
            b.setIcon('mdi-menu')

        """
        warnings.warn("This method is deprecate used instead button_obj.icon = 'your_icon_name'", DeprecationWarning,
                      stacklevel=2)
        self.icon = iconname

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon_name: str):
        """
        Change the icon for the button

        Example
        -------
        Creation of a button and programmatically change its icon::

            from vois.vuetify import settings, Button

            b = Button('Test button', text_weight=450, width=150, height=46,
                       selected=True, rounded=True,
                       icon='mdi-menu-open', icon_color='black', icon_large=True)
            display(b)
            b.icon = 'mdi-menu'

        """
        self._icon = icon_name
        for item in self.b.children:
            if type(item).__name__ == 'Icon':
                newicon = v.Icon(class_="pa-0 ma-0 %s" % self.icon_distance, large=self.icon_large,
                                 small=self.icon_small,
                                 color=self.icon_color, children=[self._icon])
                self.b.children = [newicon if x == item else x for x in self.b.children]
                break

    # Change the text for the button
    def setText(self, newtext: str):
        """
        Change the text for the button

        Example
        -------
        Creation of a button and programmatically change its text::

            from vois.vuetify import settings, Button

            b = Button('Test button', text_weight=450, width=250, height=46,
                       selected=True, rounded=True)
            display(b.draw())
            b.setText('New button text')

        """
        warnings.warn("This method is deprecate used instead button_obj.text = 'your_new_text'", DeprecationWarning,
                      stacklevel=2)
        self.text = newtext

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        """
        Change the text for the button

        Example
        -------
        Creation of a button and programmatically change its text::

            from vois.vuetify import settings, Button

            b = Button('Test button', text_weight=450, width=250, height=46,
                       selected=True, rounded=True)
            display(b)
            b.text = 'New button text'

        """
        tmp = self.b.children
        tmp[tmp.index(self._text)] = value
        self.b.children = []
        self.b.children = tmp
        self._text = value

        
    @property
    def color_selected(self):
        """
        Get/Set the color of the button when it is in the selected state.
        
        Returns
        --------
        c : str
            widget color

        Example
        -------
        Programmatically change the widget color::
            
            s.color_selected = '#00FF00'
            print(s.color_selected)
        
        """
        return self._color_selected
        
    @color_selected.setter
    def color_selected(self, color):
        self._color_selected = color
        if self._selected:
            self.b.color = self._color_selected


    @property
    def color_unselected(self):
        """
        Get/Set the color of the button when it is in the unselected state.
        
        Returns
        --------
        c : str
            widget color

        Example
        -------
        Programmatically change the widget color::
            
            s.color_unselected = '#00FF00'
            print(s.color_unselected)
        
        """
        return self._color_selected
        
    @color_unselected.setter
    def color_unselected(self, color):
        self._color_unselected = color
        if not self._selected:
            self.b.color = self._color_unselected

        
    @property
    def dark(self):
        return self._dark

    @dark.setter
    def dark(self, flag):
        """
        Change the dark mode for the button

        Example
        -------
        Creation of a button and programmatically change its dark mode::

            from vois.vuetify import settings, Button

            b = Button('Test button', text_weight=450, width=250, height=46,
                       selected=True, rounded=True)
            display(b)
            b.dark = True

        """
        self._dark = flag
        
        self.icon_color = 'black'
        if self._dark:
            self.icon_color = 'white'
        
        self.b.dark = self._dark
        
        for item in self.b.children:
            if type(item).__name__ == 'Icon':
                newicon = v.Icon(class_="pa-0 ma-0 %s" % self.icon_distance, large=self.icon_large,
                                 small=self.icon_small,
                                 color=self.icon_color, children=[self._icon])
                self.b.children = [newicon if x == item else x for x in self.b.children]
                break
        
    @property
    def rounded(self):
        return self._dark

    @rounded.setter
    def rounded(self, flag):
        """
        Change the rounded state for the button

        Example
        -------
        Creation of a button and programmatically change its rounded state::

            from vois.vuetify import settings, Button

            b = Button('Test button', text_weight=450, width=250, height=46,
                       selected=True, rounded=True)
            display(b)
            b.rounded = False

        """
        self._rounded = flag
        self.b.rounded = self._rounded
        