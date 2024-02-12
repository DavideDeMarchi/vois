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
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
    from . import fontsettings
except:
    import settings
    import fontsettings


#####################################################################################################################################################
# Button class. On click python function called when clicked
# Uses settings font to display the button text and interactivity when hover
#####################################################################################################################################################
class button():
    """
    Button widget to call a python function when clicked.
        
    Parameters
    ----------
    text : str
        Test string to be displayed on the button widget
    onclick : function, optional
        Python function to call when the user clicks on the button. The function will receive as parameter the value of the argument (default is None)
    ondblclick : function, optional
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
    xlarge : bool, optional
        Flag that sets the xlarge version of the button (default is False)
    small : bool, optional
        Flag that sets the small version of the button (default is False)
    xsmall : bool, optional
        Flag that sets the xsmall version of the button (default is False)
    outlined : bool, optional
        Flag to show the button as outlined (default is False)
    textweight : int, optional
        Weight of the text to be shown in the label (default is 500, Bold is any value greater or equal to 500)
    href : str, optional
        URL to open when the button is clicked (default is None)
    target : str, optional
        Designates the target attribute (where the URL page is opened, for instance: '_blank' to open it in a new browser tab). This should only be applied when using the href parameter (default is None)
    onlytext : bool, optional
         If True, the button will contain only the text (default is False)
    textcolor : str, optional
        Color used for the button text (default is None)
    icon: str, optional
        Name of the icon to display aside the text of the label (default is None)
    iconlarge : bool, optional
        Flag that sets the large version of the icon (default is False)
    iconsmall : bool, optional
        Flag that sets the small version of the icon (default is False)
    iconleft : bool, optional
        Flag that sets the position of the icon  to the left of the text of the label (default is False)
    iconcolor : str, optional
        Color of the icon (default is 'black')
    autoselect : bool, optional
        If True, the button becomes selected when clicked (default is False)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    rounded : bool, optional
        Flag to display the button with rounded corners (default is the value of settings.button_rounded)
    tile : bool, optional
        Flag to remove the button small border (default is False)
    colorselected : str, optional
        Color used for the button when it is selected (default is settings.color_first)
    colorunselected : str, optional
        Color used for the button when it is not selected (default is settings.color_second)
            
    Note
    ----
    All the icons from https://materialdesignicons.com/ site can be used, just by prepending 'mdi-' to their name.
    
    All the free icons from https://fontawesome.com/ site can be used, just by prepending 'fa-' to their name.
    
    
    Example
    -------
    Creation and display of a some button widgets playing with the parameters::
        
        from vois.vuetify import settings, button

        def onclick(arg=None):
            if arg==1: b1.selected = not b1.selected
            if arg==2: b2.selected = not b2.selected
            else:      b3.selected = not b3.selected

        b1 = button.button('Test button 1', textweight=300, onclick=onclick, argument=1,
                           width=150, height=36, 
                           tooltip='Tooltip for button 1', selected=False, rounded=True,
                           icon='mdi-car-light-high', iconcolor='black')

        b2 = button.button('Test button 2', textweight=450, onclick=onclick, argument=2,
                           width=150, height=48,
                           tooltip='Tooltip for button 2', selected=True, rounded=False)

        b3 = button.button('Test button 3', textweight=450, onclick=onclick, argument=3,
                           width=150, height=38,
                           textcolor=settings.color_first, 
                           tooltip='Tooltip for button 3', outlined=True, rounded=True)

        b4 = button.button('Contacts', onlytext=True, textcolor=settings.color_first,
                           width=150, height=28,
                           href='https://ec.europa.eu/info/contact_en', target="_blank",
                           tooltip='Open a URL')

        display(b1.draw())
        display(b2.draw())
        display(b3.draw())
        display(b4.draw())


    .. figure:: figures/button.png
       :scale: 100 %
       :alt: button widget

       Example of a 4 button widgets with different display modes.
   """

   
    # Initialization
    def __init__(self, text, onclick=None, argument=None, width=100, height=36, selected=False, disabled=False, tooltip='', 
                 large=False, xlarge=False, small=False, xsmall=False, outlined=False, textweight=500,
                 href=None, target=None, onlytext=False, textcolor=None,  class_="pa-0 ma-0",
                 icon=None, iconlarge=False, iconsmall=False, iconleft=False, iconcolor='black',
                 autoselect=False, dark=settings.dark_mode, rounded=settings.button_rounded, tile=False,
                 colorselected=settings.color_first, colorunselected=settings.color_second, ondblclick=None
                ):
        self.onclick    = onclick
        self.ondblclick = ondblclick
        self.argument   = argument
        self._selected  = selected
        self._disabled  = disabled
        self.autoselect = autoselect
        self.text       = text
        self.iconlarge  = iconlarge
        self.iconsmall  = iconsmall
        self.iconcolor  = iconcolor
        self.colorselected   = colorselected
        self.colorunselected = colorunselected

        self.icondistance = " ml-2"
    
        if not textcolor is None: color = textcolor
        else:
            if self._selected: color = self.colorselected
            else:              color = self.colorunselected
            
        if icon is None:
            childs = [self.text]
        else:
            if len(self.text) == 0: self.icondistance = ""
            elif iconleft:          self.icondistance = " mr-2"
            
            icn = v.Icon(class_="pa-0 ma-0 %s" % self.icondistance, large=self.iconlarge, small=self.iconsmall, color=self.iconcolor, children=[icon])
            if iconleft:
                if len(self.text) == 0: childs = [icn]
                else:                   childs = [icn, self.text]
            else:
                if len(self.text) == 0: childs = [icn]
                else:                   childs = [self.text, icn]
            
        self.b = v.Btn(color=color, dark=dark, icon=onlytext, depressed=True, outlined=outlined, large=large, xlarge=xlarge, small=small, x_small=xsmall, 
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

    
    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.onclick:
            if not self.argument is None:
                self.onclick(self.argument)
            else:
                self.onclick()
        if self.autoselect:
            self.selected = True
            
    # Manage dblclick event
    def __internal_ondblclick(self, widget=None, event=None, data=None):
        if self.ondblclick:
            if not self.argument is None:
                self.ondblclick(self.argument)
            else:
                self.ondblclick()

            
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
        if self._selected: color = self.colorselected
        else:              color = self.colorunselected
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
    def setIcon(self, iconname):
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
                newicon = v.Icon(class_="pa-0 ma-0 %s" % self.icondistance, large=self.iconlarge, small=self.iconsmall, color=self.iconcolor, children=[iconname])
                self.b.children = [newicon if x==item else x for x in self.b.children]
                break
                
    # Change the text for the button
    def setText(self, newtext):
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
        for item in self.b.children:
            if isinstance(item, str):
                self.b.children = [newtext if x==item else x for x in self.b.children]
                break                    