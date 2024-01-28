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

from random import randint

try:
    from . import settings
    from . import fontsettings
except:
    import settings
    import fontsettings


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
    icon_small : bool, optional
        If True the icon will be small (default is True)
    icon_large : bool, optional
        If True the icon will be small (default is False)
    margins : int, optional
        Dimension of the margins on all directions (default is 0)
    margintop : int, optional
        Dimension of the margin on top of the label (default is None)
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
    open_on_hover : bool, optional
        If True the popup opens/closes when hovering the button, otherwise it opens/closes on click on the button (default is True)
    close_on_click : bool, optional
        Designates if popup should close on outside click (default is True)
    close_on_content_click : bool, optional
        Designates if popup should close when its content is clicked  (default is True)
    title: str, optional
        Text to add at the top of the popup (default is '')
    show_close_button : bool, optional
        If True a close icon button is displayed on the top-right side of the popup to ease the closing of the popup (default is False). It can be useful mainly when close_on_click is set to False.

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
                 icon_small=True,
                 icon_large=False,
                 margins=0,
                 margintop=None,
                 color=settings.color_first,
                 rounded=settings.button_rounded,
                 outlined=True,
                 text=False,
                 popupwidth=160,
                 popupheight=250,
                 open_on_hover=True,
                 close_on_click=True,
                 close_on_content_click=True,
                 title='',
                 show_close_button=False):

        # The popup cannot have a width smaller than the width of the button
        if popupwidth < buttonwidth: popupwidth = buttonwidth
            
        # Add a close button on top
        children = [widget]
        if show_close_button or len(title)> 0:
            
            if show_close_button:
                def onclick(*args):
                    self.menu.v_model = False
                    
                bclose = v.Btn(icon=True, small=True, children=[v.Icon(small=True, children=['mdi-close'])])
                bclose.on_event('click', onclick)
            else:
                bclose = v.Html(tag='div',children=[''])
            
            htitle = v.Html(tag='div',children=[title], class_='pa-0 ma-1', style_='width: %dpx; height: 1px;'%(popupwidth-38))
                                
            r = v.Row(no_gutters=True, justify="start", children=[htitle,bclose], class_='pa-0 ma-0')
            children = [r, widget]
            popupheight += 30
            
        card = v.Card(width='%dpx'%popupwidth, height='%dpx'%popupheight, elevation=1, children=children, style_='overflow: auto;')
        
        children = []
        leftspace = 0
        flagicon = not icon is None
        if len(buttontext) > 0:
            children.append(buttontext)
            leftspace = 2
            flagicon = False
            
        if not icon is None:
            children.append(v.Icon(small=icon_small, large=icon_large, children=[icon], class_='pa-0 ma-0 ml-%d'%leftspace))
            
        if not margintop is None:
            class_ = "pa-0 ma-%s mt-%s" % (str(margins), str(margintop))
        else:
            class_ = "pa-0 ma-%s" % (str(margins))
            
        variable = 'menuData%d' % randint(1,999999)
        
        btn = v.Btn(v_on='%s.on'%variable, color=color, fab=False, dark=True, depressed=True, icon=flagicon, text=text, class_=class_,
                    disabled=False, width=buttonwidth, max_width=buttonwidth, height=buttonheight, rounded=rounded, outlined=outlined,
                    style_='font-family: %s; font-weight: %d; text-transform: none' % (fontsettings.font_name, 450),
                    children=children)
        
        self.menu = v.Menu(v_model=False, offset_y=True, open_on_hover=open_on_hover, dense=True, internal_activator=True,
                           close_on_click=close_on_click, close_on_content_click=close_on_content_click,
                           v_slots=[{'name': 'activator', 'variable': variable, 'children': btn }],
                           children=[card], style_='overflow: hidden;')
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display"""
        return self.menu

