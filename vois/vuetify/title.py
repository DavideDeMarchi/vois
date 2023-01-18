"""Class that implements a title bar that can be used as a simple main interface for a dashboard."""
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
# Display a title panel with some buttons
#####################################################################################################################################################
class title():
    """
    Class that implements a title bar that can be used as a simple main interface for a dashboard.
        
    Parameters
    ----------
    text : str, optional
        Text to display in the title widget
    textweight : int, optional
        Weight of the title text (default is 500)
    height : int, optional
        Height of the title bar in pixels (default is 85 pixels)
    color : str, optional
        Background color of the title bar (default is the color_first defined in the settings.py module)
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    buttons : list of strings, optional
        List of strings to be used as text of the buttons to display below the title bar main text
    onclick : function, optional
        Python function to call when the user clicks on one of the buttons. The function will receive a parameter of string containing the name of the button clicked 
    menu : bool, optional
        Flag that controls the display of a menu icon on the left side of the title bar (default is True)
    menumarginy : int, optional
        Vertical displace of the menu icon from the top of the title bar (default is 2)
    onmenuclick :
        Python function to call when the user clicks on the menu icon. The function will receive no parameters
    logo : str, optional
        String conaining the URL of the logo image to display on the right side of the title bar
    logowidth : int, optional
        Width in pixels of the area where the logo has to be displayed
    logomarginy : int, optional
        Vertical displace of the logo from the top of the title bar (default is 0)
    output : ipywidgets.Output, optional
        Output widget on which the title bar has to be displayed

    Example
    -------
    Creation and display of a title bar with additional buttons and left menu icon::
        
        from vois.vuetify import title
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def onclick(arg):
            with output:
                print(arg)

        def onmenu():
            with output:
                print('MENU')

        f = title.title(text='Title text to display', color='amber',
                        menu=True, onmenuclick=onmenu,
                        buttons=['Home', 'About Us', 'Team', 'Services', 'Blog', 'Contact Us'],
                        logo='https://jeodpp.jrc.ec.europa.eu/services/shared/home/images/JRCBigDataPlatform2.png',
                        logomarginy=6, menumarginy=4,
                        height=80, onclick=onclick, output=output)

    .. figure:: figures/title.png
       :scale: 100 %
       :alt: title widget

       Example of a title bar.
    """
    
    def __init__(self, text='', textweight=500, buttons=[], menu=True, onmenuclick=None, dark=settings.dark_mode, height=85, color=settings.color_first, onclick=None,
                 logo='https://jeodpp.jrc.ec.europa.eu/services/shared/Notebooks/images/European_Commission.svg', logowidth=100, logomarginy=0, menumarginy=2,
                 output=None):
        
        self.onclick     = onclick
        self.onmenuclick = onmenuclick
        
        if dark:
            textcol = settings.textcolor_dark
        else:
            textcol = settings.textcolor_notdark
        
        s = 'font-family: %s; font-size: 30px; font-weight: %d; text-transform: none; overflow: hidden;' % (fontsettings.font_name, textweight)
        h = v.Html(tag='div', style_=s, children=[text])
        
        c = v.Col(color=color, class_="pa-0 ma-0 mt-n1 mb-n2 text-center %s--text" % textcol, cols="12", children=[h])
    
        self.buttons_text = buttons
        self.buttons = [v.Btn(color=textcol, text=True, rounded=True, class_='my-2', children=[x]) for x in self.buttons_text]
        for b in self.buttons:
            b.on_event('click', self.__internal_onclick)
            
        if menu:
            m = v.Btn(icon=True, dark=dark, children=[v.Icon(children=['mdi-menu'])])
            m.on_event('click', self.__internal_onmenu)
        else:
            m = v.Spacer()

        r = v.Row(class_='pa-0 ma-0 mb-n2', justify="center", no_gutters=True, children=self.buttons, style_='overflow: hidden;')

        img = v.Img(src=logo, class_='pa-0 ma-0 mt-%d mr-1'%logomarginy, max_width=logowidth)
        c0 = v.Col(cols="1",  children=[m], class_='pa-0 ma-0 ml-1 mr-n1 mt-%d' % menumarginy)
        c1 = v.Col(cols="10", children=[c,r])
        c2 = v.Col(cols="1",  children=[img], class_='pa-0 ma-0 mt-1')
        rfull = v.Row(class_='pa-0 ma-0', no_gutters=True, children=[c0,c1,c2], style_='overflow: hidden;')
        
        self.f = v.Footer(color=color, padless=True, children=[rfull], style_='overflow: hidden;')
        if not height is None:
            self.f.height = height
        
        # Display of the footer
        if not output is None:
            with output:
                display(self.f)
        
    # Manage click on the buttons
    def __internal_onclick(self,widget,event,data):
        i = self.buttons.index(widget)
        if not self.onclick is None:
            self.onclick(self.buttons_text[i])

    # Manage click on the menu
    def __internal_onmenu(self, *args):
        if not self.onmenuclick is None:
            self.onmenuclick()
            