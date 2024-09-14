"""Button displaying an icon."""
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
# Icon Button control
#####################################################################################################################################################
class iconButton():
    """
    Button displaying an icon.
        
    Parameters
    ----------
    icon : str, optional
        Icon to display inside the button (default is 'mdi-alert-outline')
    tooltip : str, optional
        Tooltip text for the button (default is '')
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    outlined : bool, optional
        If True applies a thin border to the button (default is False)
    rounded : bool, optional
        If True the shape of the button is rounded (default is True)
    width : str, optional
        Width of the widget (default is None)
    large : bool, optional
        If True makes the button large (default is False)
    small : bool, optional
        If True makes the button small (default is False)
    x_large : bool, optional
        If True makes the button extra-large (default is False)
    x_small : bool, optional
        If True makes the button extra-small (default is False)
    margins : str, optional
        Marging apply to the button (default is 'pa-0 ma-0')
    onclick : function, optional
        Python function to call when the user clicks on the button. The function will receive no parameters
    argument : any, optional
        Argument to be passed to the onclick funtion (default is None)
    disabled : bool, optional
        If True the button will be disabled (default is False)

    Example
    -------
    Creation and display of an icon button which changes color and tooltip on click::
        
        from vois.vuetify import iconButton
        from IPython.display import display
        
        def onclick():
            if b.color == 'red':
                b.color = 'amber'
                b.tooltip = 'Click to make the icon red'
            else:
                b.color = 'red'
                b.tooltip = 'Click to make the icon yellow'

        b = iconButton.iconButton(onclick=onclick, tooltip='Initial tooltip', x_large=True)
        display(b.draw())
   """

    # Initialization
    def __init__(self, icon='mdi-alert-outline', tooltip='', color=settings.color_first,
                 outlined=False, rounded=True, width=None,
                 large=False, small=False, x_large=False, x_small=False, margins='pa-0 ma-0',
                 onclick=None, argument=None,
                 disabled=False):
        
        self.icon      = icon
        self._tooltip  = tooltip
        self._color    = color
        self.outlined  = outlined
        self.rounded   = rounded
        self.width     = width
        self.large     = large
        self.small     = small
        self.x_large   = x_large
        self.x_small   = x_small
        self.margins   = margins
        self.onclick   = onclick
        self.argument  = argument
        self._disabled = disabled
        
        self.h = v.Html(tag='div',children=[])
        
        self.__createButton()
        
        
    # Creation of the button
    def __createButton(self):
        
        flagicon = True
        if self.outlined: flagicon = False
        self.btn = v.Btn(icon=flagicon, class_=self.margins, outlined=self.outlined, rounded=self.rounded,
                         large=self.large, small=self.small, x_large=self.x_large, x_small=self.x_small,
                         dark=settings.dark_mode, color=self._color, disabled=self._disabled,
                         width=self.width, min_width=self.width, max_width=self.width,
                         children=[v.Icon(children=[self.icon],
                                          large=self.large, small=self.small,
                                          x_large=self.x_large, x_small=self.x_small)])
        if not self.width is None:
            self.btn.min_width = self.width
            self.btn.max_width = self.width
            self.btn.width     = self.width
            
        self.btn.on_event('click.stop', self.__internal_onclick)
        
        if len(self._tooltip) > 0:
            obj = tooltip.tooltip(self._tooltip,self.btn)
        else:
            obj = self.btn
            
        self.h.children = [obj]
        
        
    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.onclick:
            if not self.argument is None:
                self.onclick(self.argument)
            else:
                self.onclick()
        
    @property
    def color(self):
        """
        Get/Set the color of the button.
        """
        return self._color

    @color.setter
    def color(self, col):
        self._color = col
        self.__createButton()
        
        
    @property
    def tooltip(self):
        """
        Get/Set the tooltip of the button.
        """
        return self._tooltip

    @tooltip.setter
    def tooltip(self, tooltip):
        self._tooltip = tooltip
        self.__createButton()


    @property
    def disabled(self):
        """
        Get/Set the disabled state of the button.
        """
        return self._disabled

    @disabled.setter
    def disabled(self, flag):
        self._disabled = flag
        self.btn.disabled = self._disabled

        
    # Returns the vuetify object to display
    def draw(self):
        return self.h