"""The switch widget provides users the ability to choose between two distinct values."""
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
from vois.vuetify.utils.util import *
from typing import Callable, Optional


#####################################################################################################################################################
# Switch control
#####################################################################################################################################################
class Switch(v.Html):
    """
    The switch widget provides users the ability to choose between two distinct values.

    Parameters
    ----------
    flag : int
        Initial value of the switch
    label : str
        Text to display on the left of the switch widget
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    inset : bool, optional
        Flag to enlarge switch track to encompass the thumb (default is True)
    dense : bool, optional
        If True, the widget is displayed with smaller dimensions (default is False)
    onchange : function, optional
        Python function to call when the user clicks on the switch. The function will receive a parameter of type bool containing the status of the switch flag
            
    Example
    -------
    Creation and display of a switch widget::
        
        from vois.vuetify import switch
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(value):
            with output:
                print(value)

        s = switch.switch(True, "Label of the switch", inset=True, onchange=onchange)

        display(s.draw())
        display(output)

    .. figure:: figures/switch.png
       :scale: 100 %
       :alt: switch widget

       Switch widget with inset flag True.
   """
    deprecation_alias = dict(onchange='on_change')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 flag: int,
                 label: str,
                 color: str = None,
                 inset: bool = True,
                 dense: bool = False,
                 on_change: Optional[Callable[[bool], None]] = None,
                 **kwargs):

        super().__init__(**kwargs)

        from vois.vuetify import settings

        self.on_change = on_change

        self._color = settings.color_first if color is None else color

        self.switch = v.Switch(v_model=bool(flag),
                               dense=dense,
                               flat=True,
                               label=label,
                               color=self._color,
                               inset=inset,
                               class_="pa-0 ma-0 ml-3 mt-2 mb-n3",
                               disabled=False)

        self.tag = 'div'
        self.children = [self.switch]
        self.style_ = 'overflow: hidden;'

        # If requested onchange management
        if self.on_change is not None:
            self.switch.on_event('change', self.__internal_onchange)

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Get the value
    @property
    def value(self):
        """
        Get/Set the status of the switch.
        
        Returns
        --------
        flag : bool
            Status of the switch

        Example
        -------
        Programmatically set the switch status and print it::
            
            t.value = True
            print(t.value)
        
        """
        return self.switch.v_model

    # Set the value of the switch
    @value.setter
    def value(self, flag):
        self.switch.v_model = bool(flag)
        if self.on_change:
            self.on_change(self.switch.v_model)

    # Manage onchange event
    def __internal_onchange(self, widget=None, event=None, data=None):
        if self.on_change:
            self.on_change(self.switch.v_model)

    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html that has a v.Switch widget as its only child)"""
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self

    # disabled property
    @property
    def disabled(self):
        """
        Get/Set the disabled state.
        """
        return self.switch.disabled

    @disabled.setter
    def disabled(self, flag):
        self.switch.disabled = flag

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
            self.switch.color = self._color
