"""Floating-action-button to be displayed in absolute mode on the page. It will display a menu when hovered."""
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

from ipywidgets import HTML, widgets, Layout
from IPython.display import display

try:
    from . import settings
    from . import fontsettings
    from . import Button
    from . import label
    from . import tooltip
except:
    import settings
    import fontsettings
    import Button
    import label
    import tooltip


#########################################################################################################################################
# Class to manage a customizable FAB menu
#########################################################################################################################################
class fab():
    """
    Floating-action-button to be displayed in absolute mode on the page. It will display a menu when hovered.
        
    Parameters
    ----------
    left : int or string, optional
        Absolute left position of the button (example: '800px' or '90%' or 750)
    top : int or string, optional
        Absolute top position of the button (example: '100px' or '10%' or 120)
    items : list of strings, optional
        Strings to be displayed as text of the options (default is [])
    onclick : list of function, optional
        Python functions to call when the user clicks on one of the items. One function for each of the items (default is [])
    tooltipitems : list of strings, optional
        Tooltip text for the items (default is [])
    iconsmall : bool, optional
        Flag to display the icon in small dimension (default is True)
    menumode : bool, optional
        Flag to display the options as dropdown menu. If False, the items are displayed as horizontally displaced toggle buttons (default is True)
    width : int, optional
        Width in pixel of the toggle buttons when menumode is False (default is 200)
    height : int, optional
        Height in pixel of the toggle buttons when menumode is False (default is 36)
    textcolor : str, optional
        Color to be used for the text of the buttons when menumode is False (default is None)
    selected : bool, optional
        If True the buttons have the settings.color_first as background (default is False)
    disabled : bool, optional
        If True the buttons are disabled (default is False)
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    large : bool, optional
        Flag that displays the fab button larger
    small : bool, optional
        Flag that displays the fab button smaller
    xsmall : bool, optional
        Flag that displays the fab button extra smaller
    outlined : bool, optional
        Flag that displays the fab button outlined
    textweight : int, optional
        Weight of the text to be shown in the label (default is 500, Bold is any value greater or equal to 500)
    zindex : int, optional
        Z-index of the fab button (default is 9999)
    output : ipywidgets.Output, optional
        Output widget on which the widget has to be displayed

    Example
    -------
    Creation and display of two fab widgets for the selection among 3 options::
        
        from vois.vuetify import fab
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def on1():
            with output:
                print('selected 1')

        def on2():
            with output:
                print('selected 2')

        def on3():
            with output:
                print('selected 3')

        b1 = fab.fab(left='70%', top='150px',
                     items=['Option 1', 'Option 2', 'Option 3'],
                     tooltipitems=['Tooltip for Option 1'],
                     onclick=[on1,on2,on3], menumode=True,
                     width=180, selected=True,
                     dark=True, zindex=100, output=output)

        b2 = fab.fab(left='70%', top='250px',
                     items=['Option 1', 'Option 2', 'Option 3'],
                     tooltipitems=['Tooltip for Option 1'],
                     onclick=[on1,on2,on3], menumode=False,
                     width=180, selected=True,
                     dark=True, zindex=100, output=output)
                     
        b1.seticon('mdi-arrow-left-bold')
        b2.seticon('mdi-arrow-left',1)
        
        
    .. figure:: figures/fab.png
       :scale: 100 %
       :alt: fab widget

       Fab widget for selecting alternative options using a menu.

    .. figure:: figures/fab2.png
       :scale: 100 %
       :alt: fab widget as toggle buttons

       Fab widget for selecting alternative options using toggle buttons.
    """
    
   
    # Initialization
    def __init__(self, left=100, top=100, items=[], onclick=[], icon='mdi-arrow-down-thick', tooltipitems=[], iconsmall=True, menumode=True, 
                 width=200, height=36, textcolor=None, selected=False, disabled=False,  
                 dark=settings.dark_mode, large=False, small=False, xsmall=False, outlined=False, textweight=500, zindex=9999,
                 output=None):
        
        # Positioning
        self.left   = left
        self.top    = top
        self.zindex = zindex
        
        # Callback functions to call
        self.onclick  = onclick
        self.menumode = menumode
        self.width    = width
        
        self.nav = None

        self.iconsmall = iconsmall
        self.iconcolor = settings.textcolor_notdark
        if dark: self.iconcolor = settings.textcolor_dark
        
        if self.menumode:
            # Strings for the items to add to the menu
            self.items = items

            # Items in the menu
            self.listitems = []
            i = 0
            for item in items:
                li = v.ListItem(children=[item])
                li.on_event( 'click', self.__on_item_clicked)

                if type(tooltipitems) is list and i < len(tooltipitems):
                    li = tooltip.tooltip(tooltipitems[i],li)
                    
                self.listitems.append(li)
                i += 1

            # Creation of the menu
            self.button = v.Btn(v_on='menuData.on', color=settings.color_first, fab=True, dark=settings.dark_mode, depressed=True,
                                x_small=True, disabled=False, width=40, height=40, rounded=True, 
                                children=[v.Icon(small=self.iconsmall, color=self.iconcolor, children=[str(icon)])])
            
            self.menu = v.Menu(offset_y=True, open_on_hover=True, dense=True, v_slots=[{
                                              'name': 'activator',
                                              'variable': 'menuData',
                                              'children': self.button,
                                            }],
                          children=[v.List(children=self.listitems)] )
        else:
            # Strings for the buttons
            self.items = items
            
            if not textcolor is None: color = textcolor
            else:
                if selected: color = settings.color_first
                else:        color = settings.color_second
            
            # Buttons
            self.listitems = []
            self.buttons   = []
            i = 0
            for item in items:
                content = [item]
                if type(icon) is list and i < len(icon):
                    content.append(v.Icon(small=self.iconsmall, color=self.iconcolor, children=[icon[i]]))

                b = v.Btn(color=color, dark=dark, icon=False, depressed=True, outlined=outlined, large=large, small=small, x_small=xsmall, 
                          disabled=disabled, width=width-38, height=height, fab=True,
                          children=content, style_='font-family: %s; font-size: 17; font-weight: %d; text-transform: none' % (fontsettings.font_name, textweight), rounded=True)
                
                b.on_event( 'click', self.__on_item_clicked)
                self.buttons.append(b)
                
                if type(tooltipitems) is list and i < len(tooltipitems):
                    bt = tooltip.tooltip(tooltipitems[i],b)
                else:
                    bt = b
                
                self.listitems.append(bt)
                i += 1
            
            
        # Display of the panel
        if not output is None:
            with output:
                self.show(True)
    
    # Manage click menu item
    def __on_item_clicked(self, widget=None, event=None, data=None):
        txt = widget.children[0]
        if txt in self.items:
            index = self.items.index(txt)
            if index >= 0 and index < len(self.onclick):
                self.onclick[index]()
    
    # Set the icon of one of the buttons
    def seticon(self, iconname, index=0):
        """Set a different icon for the fab button"""
        if self.menumode:
            self.button.children = [v.Icon(small=self.iconsmall, color=self.iconcolor, children=[str(iconname)])]
        else:
            if index >= 0 and index < len(self.buttons):
                self.buttons[index].children = [self.buttons[index].children[0], v.Icon(small=self.iconsmall, color=self.iconcolor, children=[str(iconname)])]

                
    # Set the tooltip of one of the buttons (only if tooltip is already present and not in menumode!)
    def settooltip(self, text, index=0):
        """Change the tooltip text of one of the buttons"""
        if not self.menumode:
            if index >= 0 and index < len(self.listitems):
                if isinstance(self.listitems[index].children[0], v.generated.Tooltip):
                    self.listitems[index].children[0].children = [text]
        

        
    # Display/Hide the fab button
    def show(self, flag=True):
        """Show/hide the fab button"""
        if flag:
            if self.menumode:            
                self.nav = v.NavigationDrawer(stateless=True, permanent=True, floating=True, fixed=True, left=True, color="transparent", 
                                              width="'100px'", height="'100px'",
                                              style_="left:%s; top:%s; z-index:%d;" % (self.left,self.top,self.zindex), class_="pa-0 ma-0", children=[self.menu])
            else:
                # Add an element between any element of a list !!!
                def intersperse(lst, item):
                    result = [item] * (len(lst) * 2 - 1)
                    result[0::2] = lst
                    return result
                
                #buttons = intersperse(self.listitems, label.label('').draw())
                buttons = self.listitems
                
                if len(self.listitems) > 1: w = len(self.listitems)*(self.width - 30)
                else:                       w = self.width
                r = v.Row(no_gutters=True, justify="space-between", children=buttons)
                self.nav = v.NavigationDrawer(stateless=True, permanent=True, floating=True, fixed=True, left=True, color="transparent", 
                                              width='%dpx'%w, height='100px',
                                              style_="left:%s; top:%s; z-index:%d;" % (self.left,self.top,self.zindex), class_="pa-0 ma-0", children=[r])
                
            display(self.nav)
        else:
            if not self.nav is None:
                self.nav.close()
                
                
    # Close/hide the fab button
    def close(self):
        """Close/hide the fab button"""
        if not self.nav is None:
            self.nav.close()
            
        
