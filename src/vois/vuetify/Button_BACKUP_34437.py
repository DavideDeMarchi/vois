"""Button widget to call a python function when clicked."""
from abc import ABC

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
import warnings

# try:
#     from . import settings
#     from . import fontsettings
# except:
#     import settings
#     import fontsettings

from vois.vuetify import settings, fontsettings
from vois.vuetify.utils.util import deprecated_init_alias
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
    xLarge : bool, optional
        Flag that sets the xlarge version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    xSmall : bool, optional
        Flag that sets the xsmall version of the button (default is False)
    outlined : bool, optional
        Flag to show the button as outlined (default is False)
    textWeight : int, optional
        Weight of the text to be shown in the label (default is 500, Bold is any value greater or equal to 500)
    href : str, optional
        URL to open when the button is clicked (default is None)
    target : str, optional
        Designates the target attribute (where the URL page is opened, for instance: '_blank' to open it in a new browser tab). This should only be applied when using the href parameter (default is None)
    onlyText : bool, optional
         If True, the button will contain only the text (default is False)
    textColor : str, optional
        Color used for the button text (default is None)
    icon: str, optional
        Name of the icon to display aside the text of the label (default is None)
    iconLarge : bool, optional
        Flag that sets the large version of the icon (default is False)
    iconSmall : bool, optional
        Flag that sets the small version of the icon (default is False)
    iconLeft : bool, optional
        Flag that sets the position of the icon  to the left of the text of the label (default is False)
    iconColor : str, optional
        Color of the icon (default is 'black')
    autoSelect : bool, optional
        If True, the button becomes selected when clicked (default is False)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    rounded : bool, optional
        Flag to display the button with rounded corners (default is the value of settings.button_rounded)
    tile : bool, optional
        Flag to remove the button small border (default is False)
    colorSelected : str, optional
        Color used for the button when it is selected (default is settings.color_first)
    colorUnselected : str, optional
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

        b1 = Button('Test button 1', textWeight=300, on_click=onclick, argument=1,
                           width=150, height=36, 
                           tooltip='Tooltip for button 1', selected=False, rounded=True,
                           icon='mdi-car-light-high', iconColor='black')

        b2 = Button('Test button 2', textWeight=450, on_click=onclick, argument=2,
                           width=150, height=48,
                           tooltip='Tooltip for button 2', selected=True, rounded=False)

        b3 = Button('Test button 3', textWeight=450, on_click=onclick, argument=3,
                           width=150, height=38,
                           textColor=settings.color_first,
                           tooltip='Tooltip for button 3', outlined=True, rounded=True)

        b4 = Button('Contacts', onlyText=True, textColor=settings.color_first,
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

    # Initialization
    @deprecated_init_alias(onclick='on_click', xlarge='xLarge', xsmall='xSmall', textweight='textWeight',
                           onlytext='onlyText', textcolor='textColor', iconlarge='iconLarge', iconsmall='iconSmall',
                           iconleft='iconLeft', iconcolor='iconColor', autoselect='autoSelect',
                           colorselected='colorSelected', colorunselected='colorUnselected', ondblclick='on_dblclick')
    def __init__(self, text: str,
                 on_click: Optional[Union[Callable[[], None], Callable[[dict[str, Any]], None]]] = None,
                 argument: Optional[Any] = None,  # TODO forzare a dict per **kwargs
                 width: int = 100,
                 height: int = 36,
                 selected: bool = False,
                 disabled: bool = False,
                 tooltip: str = '',
                 large: bool = False,
                 xLarge: bool = False,
                 small: bool = False,
                 xSmall: bool = False,
                 outlined: bool = False,
                 textWeight: int = 500,
                 href: Optional[str] = None,
                 target: Optional[str] = None,
                 onlyText: bool = False,
                 textColor: Optional[str] = None,
                 class_: str = "pa-0 ma-0",
                 icon: Optional[str] = None,
                 iconLarge: bool = False,
                 iconSmall: bool = False,
                 iconLeft: bool = False,
                 iconColor='black',
                 autoSelect: bool = False,
                 dark: bool = settings.dark_mode,
                 rounded: bool = settings.button_rounded,
                 tile: bool = False,
                 colorSelected: str = settings.color_first,
                 colorUnselected: str = settings.color_second,
                 on_dblclick: Optional[Union[Callable[[], None], Callable[[dict[str, Any]], None]]] = None,
                 **kwargs) -> None:

        super().__init__(**kwargs)

        self.on_click = on_click
        self.on_dblclick = on_dblclick
        self.argument = argument
        self._selected = selected
        self._disabled = disabled
        self.autoSelect = autoSelect
        self._text = text
        self.iconLarge = iconLarge
        self.iconSmall = iconSmall
        self.iconColor = iconColor
        self.colorSelected = colorSelected
        self.colorUnselected = colorUnselected

        self.iconDistance = " ml-2"

        if textColor:
            color = textColor
        else:
            color = self.colorSelected if self._selected else self.colorUnselected

        if icon is None:
            childs = [self._text]
        else:
<<<<<<< HEAD:src/vois/vuetify/button.py
            if len(self.text) == 0: self.icondistance = ""
            elif iconleft:          self.icondistance = " mr-2"
            
            icn = v.Icon(class_="pa-0 ma-0 %s" % self.icondistance, large=self.iconlarge, small=self.iconsmall, color=self.iconcolor, children=[icon])
            if iconleft:
                if len(self.text) == 0: childs = [icn]
                else:                   childs = [icn, self.text]
            else:
                if len(self.text) == 0: childs = [icn]
                else:                   childs = [self.text, icn]
            
        self.b = v.Btn(color=color, dark=dark, icon=onlytext, depressed=True, outlined=outlined, large=large, x_large=xlarge, small=small, x_small=xsmall,
                       disabled=disabled, width=width, min_width=width, height=height, min_height=height, href=href, target=target, tile=tile, 
                       children=childs, style_='font-family: %s; font-size: 17; font-weight: %d; text-transform: none' % (fontsettings.font_name, textweight), rounded=rounded)
                
        self.b.on_event('click',    self.__internal_onclick)
        self.b.on_event('dblclick', self.__internal_ondblclick)
        
        if len(tooltip) > 0: self.b.v_on = 'tooltip.on'
        self.container = v.Container(class_=class_, children=[ v.Tooltip(color=settings.tooltip_backcolor, transition="scale-transition", bottom=True, 
                                                                         v_slots=[{'name': 'activator', 'variable': 'tooltip', 'children': self.b }],
                                                                         children=[tooltip]) ])
    
    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html containing a v.Btn widget as its only child)"""
        return v.Html(tag='div',children=[self.container])
=======
            if not self._text:
                self.iconDistance = ""
            elif iconLeft:
                self.iconDistance = " mr-2"

            icn = v.Icon(class_="pa-0 ma-0 %s" % self.iconDistance, large=self.iconLarge, small=self.iconSmall,
                         color=self.iconColor, children=[icon])
            if iconLeft:
                if not self._text:
                    childs = [icn]
                else:
                    childs = [icn, self._text]
            else:
                if not self._text:
                    childs = [icn]
                else:
                    childs = [self._text, icn]

        self.b = v.Btn(textcolor=color, dark=dark, icon=onlyText, depressed=True, outlined=outlined, large=large,
                       xlarge=xLarge, small=small, x_small=xSmall,
                       disabled=disabled, width=width, min_width=width, height=height, min_height=height, href=href,
                       target=target, tile=tile,
                       children=childs,
                       style_='font-family: %s; font-size: 17; font-weight: %d; text-transform: none' % (
                           fontsettings.font_name, textWeight), rounded=rounded)

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

    def draw(self):
        warnings.warn('DeprecationWarning: The "draw" method is deprecated, please just use the object widget itself.',
                      stacklevel=2)
        return self
>>>>>>> development:src/vois/vuetify/Button.py

    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.on_click:
            if self.argument:
                self.on_click(self.argument)  # TODO switch to kwargs
            else:
                self.on_click()
        if self.autoSelect:
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
        if self._selected:
            color = self.colorSelected
        else:
            color = self.colorUnselected
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
        Creation of a button and programmatically change of its icon::
                
                from vois.vuetify import settings, button
                
                b = button.button('Test button', textweight=450, width=150, height=46,
                                  selected=True, rounded=True,
                                  icon='mdi-menu-open', iconcolor='black', iconlarge=True)
                display(b.draw())
                b.setIcon('mdi-menu')

        """
        for item in self.b.children:
            if type(item).__name__ == 'Icon':
                newicon = v.Icon(class_="pa-0 ma-0 %s" % self.iconDistance, large=self.iconLarge, small=self.iconSmall,
                                 color=self.iconColor, children=[iconname])
                self.b.children = [newicon if x == item else x for x in self.b.children]
                break

    # Change the text for the button
    def setText(self, newtext: str):
        """
        Change the text for the button

        Example
        -------
        Creation of a button and programmatically change of its icon::
                
                from vois.vuetify import settings, button
                
                b = button.button('Test button', textweight=450, width=250, height=46,
                                  selected=True, rounded=True)
                display(b.draw())
                b.setText('New button text')

        """
        warnings.warn("This method is deprecate used instead button_obj.text = 'your_new_text'", DeprecationWarning,
                      stacklevel=2)
        for item in self.b.children:
            if isinstance(item, str):
                self.b.children = [newtext if x == item else x for x in self.b.children]
                break

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        tmp = self.b.children
        tmp[tmp.index(self._text)] = value
        self.b.children = []
        self.b.children = tmp
        self._text = value


# Proposta aggiornamento componente. Liste delle cose fatte
# 1. Rimozione import relativi
# 2. Rimozione doppio import + retrocompatibile
# 3. Usare property con setting
# 4. Inserimento type checking
# 5. Cambiamento nome classe + retrocompatibile
# 6. Cambiamento nome parameteri + retrocompatibile
# 7. Risoluzione problema draw + retrocompatibile