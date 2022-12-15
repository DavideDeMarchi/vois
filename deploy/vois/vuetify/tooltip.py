"""Add tooltip text to a widget: returns a "modified" widget to be used instead of the original one."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright (C) 2022-2030 European Union (Joint Research Centre)
#
# This file is part of BDAP voilalibrary.
#
# voilalibrary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# voilalibrary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.

import ipyvuetify as v

try:
    from . import settings
except:
    import settings


#####################################################################################################################################################
# Add tooltip text to a widget: returns a "modified" widget to be used instead of the original one
#####################################################################################################################################################
def tooltip(text, widget):
    """
    Add a tooltip to a widget.

    Parameters
    ----------
    text : str
        Text of the tooltip
    widget: ipyvuetify widget
        Instance of the widget to which the tooltip has to be added
        
    Returns
    -------
    v.Item
        An ipyvuetify v.Item widget having a v.Tooltip as its only child

    Example
    -------
    Add a tooltip to a switch widget::
    
        from voilalibrary.vuetify import tooltip, switch
        from IPython.display import display

        s = switch.switch(True, "Activate the notification")
        t = tooltip.tooltip('Select to activate the notification of events to the user', s.draw())
        display(t)
        
    .. figure:: figures/tooltip.png
       :scale: 100 %
       :alt: tooltip widget

       Tooltip added to a switch widget.
    """
    if len(text) > 0:
        widget.v_on = 'tooltip.on'
        item = v.Item(class_="pa-0 ma-0", 
                      children=[ v.Tooltip(color=settings.tooltip_backcolor, transition="scale-transition", bottom=True, left=True,
                                           v_slots=[{'name': 'activator', 'variable': 'tooltip', 'children': widget }],
                                           children=[text]) ])
        return item
    else:
        #return widget
        
        # Tooltip present but not activated
        #widget.v_on = 'tooltip.on'
        item = v.Item(class_="pa-0 ma-0", 
                      children=[ v.Tooltip(color=settings.tooltip_backcolor, transition="scale-transition", bottom=True, left=True,
                                           v_slots=[{'name': 'activator', 'variable': 'tooltip', 'children': widget }],
                                           children=[text]) ])
        return item

