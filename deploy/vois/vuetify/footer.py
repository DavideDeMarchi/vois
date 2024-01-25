"""Footer bar to be displayed at the bottom of a Voilà dashboard."""
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
# Display a footer panel with some buttons
#####################################################################################################################################################
class footer():
    """
    Footer bar to be displayed at the bottom of a Voilà dashboard.
        
    Parameters
    ----------
    text : str, optional
        Text message to display in the bottom line of the footer bar (default is '')
    copyright : bool, optional
        Flag to display a copyright symbol in the bottom line of the footer bar (default is False)
    buttons : list of strings, optional
        List of strings to use for adding a row of buttons (default is []])
    color : str, optional
        Background color of the title bar (default is the main color defined in the settings.py module)
    dark : bool, optional
        Flag that controls the color of the text in foreground: if True, the text will be displayed in white, elsewhere in black (default is the value of settings.dark_mode)
    height : int or float or str optional
        Height of the footer bar. If an integer or a float is passed, the height is intended in pixels units, otherwise a string containing the units must be passed (example: '4vh'). Default is 68 for 68 pixels
    marginy : int, optional
        Vertical displace of the first row of the bar from the top (default is 2)
    onclick : function, optional
        Python function to call when the user clicks on one of the buttons. The function will receive a parameter of type str containing the text of the clicked button
    output : ipywidgets.Output, optional
        Output widget on which the footer bar has to be displayed
    minipanelicons : list of strings, optional
        Names of optional icons to display in the minipanel at the left side of the footer bar
    minipaneltooltips : list of strings, optional
        Tooltips of optional icons to display in the minipanel at the left side of the footer bar
    minipanelopen : bool, optional
        If True the minipanel is initially displayed already opened (default is False)
    minipanellarge : bool, optional
        If True the icons in theminipanel are displayed with greater dimension (default is True)
    minipanelbuttontooltip: str, optional
        Text of the tooltip to show when hover on the minipanel open icon (default is 'Additional functions')
    minipanelbuttoncolor : str, optional
        Color of the icon that opens/closes the minipanel (default is the textcolor_notdark defined in the settings.py module)
    minipaneliconscolor : str, optional
        Color of the icons inside the minipanel (default is the textcolor_notdark defined in the settings.py module)
    footercredits : str, optional
        Text for footer credits button (default is '')
    footercreditstooltip : str, optional
        Tooltip for the footer credits button (default is '')
    onclickcredits : function, optional
        Python function to call when the user clicks on the credits button. The function will be called with 0 parameters
    onclickminipanel : function, optional
        Python function to call when the user clicks on one of the icons of the minipanel. The function will receive a parameter of type int containing the index of the clicked icon in the range from 0 to len(minipanelicons)-1
            
    Example
    -------
    Creation and display of a footer bar::
        
        from vois.vuetify import footer
        from ipywidgets import widgets
        from IPython.display import display
        from datetime import datetime

        output = widgets.Output()
        display(output)

        def onclick(arg):
            with output:
                print(arg)

        def onclickminipanel(index):
            with output:
                print(index)

        def onclickcredits():
            with output:
                print('CREDITS')

        f = footer.footer(text='%d - Joint Research Centre'%(datetime.now().year), color='lightgrey',
                          minipanelicons=['fa-truck', 'mdi-heart', 'mdi-magnify'],
                          minipaneltooltips=['Function 1', 'Function 2', 'Function 3'], 
                          minipanellarge=True, minipanelopen=True,
                          onclickminipanel=onclickminipanel,
                          footercredits='Data credits',
                          footercreditstooltip='Eurostat - European Commission',
                          onclickcredits=onclickcredits,
                          buttons=['Home', 'About Us', 'Services', 'Contact Us'],
                          height=68, marginy=2,
                          onclick=onclick,
                          output=output)
                  
    .. figure:: figures/footer.png
       :scale: 100 %
       :alt: footer widget

       Footer bar with buttons and minipanel.
       
    Note
    ----
    The footer component is used inside the :py:class:`app.app` class. If the main interface of a dashboard is created using an instance of the :py:class:`app.app` class, the parameters for customising the footer bar can be passed in the construction of the **app** instance.
    
   """
        
    def __init__(self, text='', copyright=False, buttons=[], dark=settings.dark_mode, height=68, marginy=2, color=settings.color_first, 
                 minipanelicons=[], minipaneltooltips=[], minipanelopen=False,
                 minipanellarge=True, minipanelbuttontooltip='Additional functions',
                 minipanelbuttoncolor=settings.color_first, minipaneliconscolor=settings.textcolor_notdark,
                 footercredits='',        # Text for footer credits button
                 footercreditstooltip='', # Tooltip for the footer credits button
                 onclickcredits=None,     # Function with 0 parameters
                 onclickminipanel=None,   # Function with 1 string argument integer containing the index of the icon
                 onclick=None,            # Function with 1 string argument integer containing the text of the button
                 output=None):
        
        self.onclick = onclick
        self.onclickminipanel = onclickminipanel
        self.onclickcredits = onclickcredits
        
        if dark:
            textcol = settings.textcolor_dark
            if minipaneliconscolor == settings.textcolor_notdark:
                minipaneliconscolor = settings.textcolor_dark
        else:
            textcol = settings.textcolor_notdark
            
        members = [text]
        if copyright:
            icon = v.Icon(class_="pa-0 ma-0 mr-2", small=True, color=textcol, children=['mdi-copyright'])
            members = [icon,text]

        if len(minipanelicons) > 0:
            if len(buttons) == 0:
                c = v.Col(color=color, class_="pa-0 ma-0 mt-%d text-center %s--text" % (marginy+4,textcol), cols="12", children=members)
            else:
                c = v.Col(color=color, class_="pa-0 ma-0 text-center %s--text" % (textcol), cols="12", children=members)
        else:
            c = v.Col(color=color, class_="pa-0 ma-0 mt-%d text-center %s--text" % (marginy,textcol), cols="12", children=members)
    
        self.buttons_text = buttons
        self.buttons = [v.Btn(color=textcol, text=True, rounded=settings.button_rounded, class_='my-2', children=[x]) for x in self.buttons_text]
        for b in self.buttons:
            b.on_event('click', self.__internal_onclick)
            
        r = v.Row(class_='pa-0 ma-0 mt-n2 mb-n3', justify="center", no_gutters=True, children=self.buttons)

        if self.onclickcredits is None or len(footercredits) == 0:
            self.credits = v.Btn(text=True, color=textcol, dark=dark, children=[footercredits], rounded=settings.button_rounded, disabled=True, style_='text-transform: none; cursor: initial;')
        else:
            self.credits = v.Btn(text=True, color=textcol, dark=dark, children=[footercredits], rounded=settings.button_rounded, style_='text-transform: none;')
            self.credits.on_event('click', self.__internal_onclickCredits)
        if len(footercreditstooltip) > 0:
            self.credits = tooltip.tooltip(footercreditstooltip,self.credits)

        # Minipanel
        largeicon = minipanellarge
        panelwidth = 40
        iconclass = "pa-0 ma-0 mr-1"
        panelw  = (panelwidth)*(len(minipanelicons))
        panelh = panelwidth-panelwidth/10
        if largeicon:
            panelwidth = 50
            iconclass = "pa-0 ma-0 mr-2"
            panelw  = (panelwidth)*(len(minipanelicons)) - 16
            panelh = panelwidth-12

        self.minipanel_btn = [v.Btn(icon=True, class_=iconclass, children=[v.Icon(large=largeicon, color=minipaneliconscolor, children=[x])]) for x in minipanelicons]
        for b in self.minipanel_btn:
            b.on_event('click', self.__internal_onclick_minipanel)
        minipanel_tb = [tooltip.tooltip(x,y) for x,y in zip(minipaneltooltips,self.minipanel_btn)]
        
        if len(self.minipanel_btn) > 0:
            if isinstance(height, int) or isinstance(height, float):
                hhh = '%fpx' % height
            else:
                hhh = str(height)
            y = 'calc(calc(%s - %dpx) / 2)' % (hhh,panelh)
            navDrawer = v.NavigationDrawer(v_model=minipanelopen, children=[v.Row(justify="center", no_gutters=True, children=minipanel_tb)],
                                           width="%dpx"%panelw, height="%dpx"%panelh,
                                           floating=True, fixed=True, absolute=True, style_="left:40px; top:%s; z-index:999;"%y)
            navDrawer.mini_variant = True
            navDrawer.expand_on_hover = False
            navDrawer.width = panelw
            navDrawer.mini_variant_width = panelw
            
            toolBarButton = v.Btn(icon=True, class_='pa-0 ma-0 ml-1', children=[v.Icon(children=['mdi-dots-vertical'])])
            def on_click(widget, event, data):
                navDrawer.v_model = not navDrawer.v_model
                if navDrawer.v_model: toolBarButton.color = minipanelbuttoncolor
                else:                 toolBarButton.color = textcol
                    
            if navDrawer.v_model: toolBarButton.color = minipanelbuttoncolor
            else:                 toolBarButton.color = textcol
                
            toolBarButton.on_event('click', on_click)
            tbt = tooltip.tooltip(minipanelbuttontooltip,toolBarButton)
            c1 = v.Col(cols="1", align_self="center", children=[tbt, navDrawer])
            c2 = v.Col(cols="10",children=[r,c])
            c3 = v.Col(cols="1", align_self="right", children=[self.credits])
            footercontent = [v.Row(justify="start", no_gutters=True, children=[c1,c2,c3])]
        else:
            if len(self.buttons) > 0:
                c2 = v.Col(cols="11",children=[r,c])
            else:
                c2 = v.Col(cols="11",children=[c])
            c3 = v.Col(cols="1", align_self="right", children=[self.credits])
            footercontent = [v.Row(justify="start", no_gutters=True, children=[c2,c3])]
        
        hhh = '68px'
        if not height is None:
            if isinstance(height, int) or isinstance(height, float):
                hhh = '%fpx' % height
            else:
                hhh = height
                
        self.f = v.Footer(color=color, padless=True, children=footercontent, class_='pa-0 ma-0', style_='height: %s; overflow: hidden;'%hhh)
        
        # Display of the footer
        if not output is None:
            with output:
                display(self.f)

    # Returns the vuetify object to display (the v.Footer)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html which has a v.Footer as its only child)"""
        return v.Html(tag='div',children=[self.f])
                
    # Manage click on the buttons
    def __internal_onclick(self,widget,event,data):
        i = self.buttons.index(widget)
        if not self.onclick is None:
            self.onclick(self.buttons_text[i])
            
            
    # Manage click on the minipanel icons
    def __internal_onclick_minipanel(self,widget,event,data):
        i = self.minipanel_btn.index(widget)
        if not self.onclickminipanel is None:
            self.onclickminipanel(i)

            
    # Manage click on the title credits button
    def __internal_onclickCredits(self, widget, event, data):
        if not self.onclickcredits is None:
            self.onclickcredits()
            
    