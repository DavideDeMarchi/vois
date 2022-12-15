"""Add tooltip text to a widget: returns a "modified" widget to be used instead of the original one."""
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
    
        from vois.vuetify import tooltip, switch
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

