"""Popup window opened at hover on a button."""
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
    from . import tooltip
except:
    import settings
    import fontsettings
    import tooltip


#####################################################################################################################################################
# Popup control
#####################################################################################################################################################
class popup:
    """
    Popup window opened at hover on a button
        
    Parameters
    ----------
    widget : any widget
        Widget to be displayed inside the popup menu
    buttontext : str
        Text to display inside the button
    buttonwidth : int, optional
        Width of the button in pixels (default is 140)
    buttonheight : int, optional
        Height of the button in pixels (default is 40)
    icon : str, optional
        Name of the icon to be displayed inside the button (default is None)
    color : str, optional
        Color used for the button (default is the color_first defined in the settings.py module)
    rounded : bool, optional
        If True the button will be rounded (default is the button_rounded defined in the settings.py module)
    outlined : bool, optional
        If True the button will be outlined (default is True)
    text : bool, optional
        If True the button will display only the text and/or the icon, with no background (default is False)
    popupwidth : int, optional
        Width of the popup window in pixels (default is 160). The popup cannot have a width smaller than the width of the button
    popupheight : int, optional
        Height of the popup window in pixels (default is 250)

    Note
    ----
    All the icons from https://materialdesignicons.com/ site can be used, just by prepending 'mdi-' to their name.
    
    All the free icons from https://fontawesome.com/ site can be used, just by prepending 'fa-' to their name.
    
    
    Example
    -------
    Creation and display of a popup window displaying a tree and opened by hovering on a button::
        
        from vois.vuetify import popup, treeview
        from IPython.display import display

        sectors = ['S%d'%x for x in range(10)]
        treecard = treeview.createTreeviewFromList(sectors,
                                                   rootName='All',
                                                   height='270px')

        p = popup.popup(treecard, 'Sectors', popupheight=270)

        display(p.draw())

    .. figure:: figures/popup.png
       :scale: 100 %
       :alt: popup widget example

       Example of a button that, on hover, opens a popup window containing a treeview
   """

    # Initialization
    def __init__(self,
                 widget,
                 buttontext,
                 buttonwidth=140,
                 buttonheight=40,
                 icon=None,
                 color=settings.color_first,
                 rounded=settings.button_rounded,
                 outlined=True,
                 text=False,
                 popupwidth=160,
                 popupheight=250):

        # The popup cannot have a width smaller than the width of the button
        if popupwidth < buttonwidth: popupwidth = buttonwidth
            
        html = v.Html(tag='div', width='%dpx'%popupwidth, height='%dpx'%popupheight, children=[widget], style_='overflow: auto;')
        card = v.Card(width='%dpx'%popupwidth, height='%dpx'%popupheight, elevation=1,
                      children=[widget], style_='overflow: auto;')
        
        children = []
        leftspace = 0
        if len(buttontext) > 0:
            children.append(buttontext)
            leftspace = 2
            
        if not icon is None:
            children.append(v.Icon(small=True, children=[icon], class_='pa-0 ma-0 ml-%d'%leftspace))
            
        self.btn = v.Btn(v_on='menuData.on', color=color, fab=False, dark=True, depressed=True, text=text,
                         disabled=False, width=buttonwidth, buttonheight=40, rounded=rounded, outlined=outlined,
                         style_='font-family: %s; font-weight: %d; text-transform: none' % (fontsettings.font_name, 450),
                         children=children)

        self.menu = v.Menu(offset_y=True, open_on_hover=True, dense=True,
                           v_slots=[{'name': 'activator', 'variable': 'menuData', 'children': self.btn, }],
                           children=[card])
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display"""
        return self.menu

