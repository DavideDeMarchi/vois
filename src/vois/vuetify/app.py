"""App class to easily define the structure of a typical Voilà dashboard."""
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
from ipywidgets import widgets, Layout
from IPython.display import display, HTML
from IPython.core.display import HTML as ipyhtml   # V. I. for urlOpen to work!!!
import base64
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from random import randrange
from datetime import datetime
import ipyvuetify as v

try:
    from . import settings
    from . import fontsettings
    from . import sidePanel
    # from . import Button
    from . import footer
    from . import snackbar
    from . import dialogMessage
    from . import dialogYesNo
    from . import dialogWait
    from . import dialogGeneric
    from . import fab
    from . import queryStrings
except:
    import settings
    import fontsettings
    import sidePanel
    # import Button
    import footer
    import snackbar
    import dialogMessage
    import dialogYesNo
    import dialogWait
    import dialogGeneric
    import fab
    import queryStrings

from vois.vuetify import Button
    
# Convert a measure in string (if int or float --> pixels units)
def measure2str(value):
    if isinstance(value, int):
        return '%dpx' % value
    elif isinstance(value, float):
        return '%fpx' % value
    else:
        return value

#####################################################################################################################################################
# A fully customizable App framework for Voilà
#####################################################################################################################################################
class app():
    """
    App class to easily define the basic structure of a typical Voilà dashboard.
    
    An app instance displays a series of ipywidgets.Output() widgets to ease the usage of messages/dialog-boxes/etc, through these methods:
    
    :func:`~app.snackbar`
    :func:`~app.dialogMessage`
    :func:`~app.dialogYesNo`
    :func:`~app.dialogGeneric`
    :func:`~app.dialogWaitOpen`
    :func:`~app.dialogWaitClose`
    :func:`~app.fab`
    :func:`~app.downloadText`
    :func:`~app.downloadBytes`
    :func:`~app.urlOpen`
    :func:`~app.urlParameter`
    :func:`~app.urlParameter`

    The main content of the dashboard should be displayed in the **app.outcontent** Output widget that completely fills the empty space of the dashboard between the title bar and the footer bar.
    
    Parameters
    ----------
    title : str, optional
        Main title of the application to be displayed on the title bar (default is 'Title of the dashboard')
    titlesvg : str, optional
        SVG string to use as application title when the title string is empty (default is '')
    titlesvgclass : str, optional
        Class margins and padding to apply to the titlesvg drawing (default is 'pa-0 ma-0')
    titlecredits : str, optional
        Credits string to be displayed on the right side of the title bar (default is '')
    titlecredits2 : str, optional
        Secondary credits string to be displayed on the right side of the title bar (default is '')
    titlestyle : str, optional
        CSS style to apply to the main title of the dashboard (default is '', an example could be: 'font-family: "Times New Roman", Times, serif; font-weight: bold; font-size: 22px;')
    titlespacestyle : str, optional
        CSS style to apply to the space at the left of the title (default is 'width: 50px; min-width: 50px;'). It can be useful to move the title more on the centre of the title bar, by providing a titlespacestyle like 'width: 200px;'
    titleheight : int, optional
        Height of the title bar in pixels (default is 70 pixels)
    totalheight : int, optional
        Total height in pixels of the page (default is 985 pixels which is coherent with a FullHD screen dimension)
    dark : bool, optional
        If True the title text color is settings.textcolor_dark, if False it is settings.textcolor_nodark (default is settings.dark_mode)
    backcolor : str, optional
        Background color of the title bar (default is settings.color_second)
    titlewidth : str, optional
        Width of the part of the title bar  that contains the main title of the dashboard (default is '600px', other values could be, for instance: '50%')
    footercolor : str, optional
        Background color to use for the footer bar displayed in the bottom part of the screen (default is 'lightgrey')
    backgroundimageurl : str, optional
        URL of the optional image to display as background of the title bar (default is None)
    backgroundimageposition : str, optional
        Defines the way the backgroundimage in the title is cropped (default is 'center center'). See `Vuetify.js v-img <https://vuetifyjs.com/en/api/v-img/#props-position>`_  and `CSS background-position documentation <https://developer.mozilla.org/en-US/docs/Web/CSS/background-position>`_ for help.
    logourl : str, optional
        URL of the image or SVG to use as a logo in the right end side of the title bar (default is European Commission logo)
    logomaxwidth : int, optional
        Maximum width in pixels of the logo image (default is 80 pixels)
    logomaxheight : int, optional
        Maximum height in pixels of the logo image (default is 60 pixels)
    titletabs : list of strings, optional
        List of tabs to be added to the title bar as the main visualization options of the dashboard (default is ['Tab 1', 'Tab 2', 'Tab 3'])
    titletabsactive : int, optional
        Index of the tab to activate at start (default is 0)
    titletabsstile : str, optional
        CSS style to apply to the tabs in the title bar (default is 'font-weight: bold;')
    titletabsactiveparameter : str, optional
        Name of the URL parameter to read for setting the activetab (default is None)
    titletabscolor : str, optional
        Color of the selected tab in the title tabs (default is settings.color_first)
    titletabsdark : bool, optional
        If True the text color of unselected tabs is settings.textcolor_dark, if False it is settings.textcolor_nodark (default is False)
    footertext : str, optional
        Text to display in the footer tab (default is '<current year> - Joint Research Centre')
    footerbuttons : list of strings, optional
        List of strings containing the caption of the buttons to display in the footer tab (default is ['Home', 'About Us', 'Team', 'Services', 'Blog', 'Contact Us'])
    footerheight : int or float or str optional
        Height of the footer bar. If an integer or a float is passed, the height is intended in pixels units, otherwise a string containing the units must be passed (example: '4vh'). Default is 68 for 68 pixels
    footercopyright : bool, optional
        If True adds the copyright symbol to the footer text (default is True)
    footerdark : bool, optional
        If True the footer text color is settings.textcolor_dark, if False it is settings.textcolor_nodark (default is settings.dark_mode)
    footercredits : str, optional
        Text for footer credits button (default is '')
    footercreditstooltip : str, optional
        Tooltip for the footer credits button (default is '')
    footercreditsurl : str, optional
        URL to open when the user clicks on the footer credits button (default is '')
    sidepaneltitle : str, optional
        Title of the left side panel (default is 'Settings')
    sidepanelwidth : int, optional
        Width in pixels of the left side panel (default is 400). If the size is 0, the icon to open the sidepanel will not be added to the title bar
    sidepaneltext : str, optional
        Text to display in the left side panel (default is '')
    sidepanelcontent : list of ipywidgets, optional
        List of ipywidgets object to display in the left side panel (default is [])
    sidepaneldark : bool, optional
        If True the title text color of the sidePanel is black, otehrwise is white (default is settings.dark_mode)
    sidepanelbackdark : bool, optional
        If True the background color of the sidePanel is black, otehrwise is white (default is settings.dark_mode)
    minipanelicons : list of strings, optional
        List of string containing the names of the icons to display in the minipanel that is displayed on the left side of the footer tab (default is [])
    minipaneltooltips : list of strings, optional
        List of tooltips to set for the icons of the minipanel (default is [])
    minipanelopen : bool, optional
        If True the minipanel is dopened on startup of the app (default is False)
    minipanellarge : bool, optional
        If True, the minipanel icons are displayed in the large version (default is True)
    minipanelbuttoncolor : str, optional
         Color of the 'three vertical points icon' that opens/closes the minipanel (default is the textcolor_notdark defined in the settings.py module)
    minipaneliconscolor : str, optional
         Color of the icons in the minipanel (default is the textcolor_notdark defined in the settings.py module)
    onclicktab : function, optional
        Python function to call when the user clicks on one of the tabs of the title bar. The function will receive a parameter of type string containing the text of the tab
    onclickcredits : function, optional
        Python function to call when the user clicks on the credits button on the title bar. The function will receive no parameters
    onclickcredits2 : function, optional
        Python function to call when the user clicks on the secondary credits button on the title bar. The function will receive no parameters
    onclicklogo : function, optional
        Python function to call when the user clicks on the logo image on the title bar. The function will receive no parameters
    onclickfooter : function, optional
        Python function to call when the user clicks on one of the buttons of the footer bar. The function will receive a parameter of type string containing the text of the button
    onclickminipanel : function, optional
        Python function to call when the user clicks on one of the icons of the minipanel in the footer bar. The function will receive a parameter of type int containing the index of the icon
    fullscreen : bool, optional
        If True the app will be displayed in fullscreen mode (default is False). In fullscreen mode the app will occupy all the available space on the web page (the titlebar will be aligned on top, the footer bar will be aligned on the bottom of the page, and the outcontent will occupy all the intermediate space between the title bar and the footer bar, irrescpective of the value passed in the totalheight parameter), and the positioning of the elements will be fully responsive.
        
        
    Attributes
    ----------
    outcontent : ipywidgets.Output instance
        This is the output widget where the content of the application can be displayed

        To visually highlight the app.outcontent Output widget, this line of code can be executed::

            g_app.outcontent.layout.border = '1px solid lightgrey'

        After the execution of that line, the border of the g_app.outcontent will be visible. To reset the border to the empty line, this line of code can be executed::

            g_app.outcontent.layout.border = ''


    Example
    -------
    Creation of an app class to define the structure of a Voilà dashboard::
      
        from vois.vuetify import app, settings
        import ipyvuetify as v
        
        # Change global settings
        settings.dark_mode      = False
        settings.color_second   = '#68aad2'
        settings.color_first    = '#1c4056'
        settings.button_rounded = False

        # Click on a tab of the title
        def on_click_tab(arg):
            g_app.snackbar(arg)

        # Click on the credits text
        def on_click_credits():
            g_app.snackbar('CREDITS')

        # Click on the logo
        def on_click_logo():
            g_app.snackbar('LOGO')

        # Click on the footer buttons
        def on_click_footer(arg):
            g_app.snackbar(arg)

        # Click on the footer minipanel
        def on_click_minipanel(index):
            g_app.snackbar(str(index))


        g_app = app.app(title='Energy consumption example dashboard',
                        titlecredits='Created by Unit I.3',
                        titlewidth='60%',
                        footercolor='#1c4056',
                        titletabs=['Chart', 'Table', 'Static Map', 'Dynamic Map'],
                        titletabscolor='#60b3e8',
                        dark=True,
                        footerdark=True,
                        footercredits='Data credits',
                        footercreditstooltip='Eurostat - European Commission',
                        footercreditsurl='https://ec.europa.eu/eurostat/data/database',
                        backcolor='#1c4056',
                        sidepaneltitle='Help',
                        sidepaneltext='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                        sidepanelcontent=[v.Icon(class_='pa-0 ma-0 ml-2', children=['mdi-help'])],
                        sidepaneldark=True,
                        sidepanelbackdark=False,
                        minipanelicons=['mdi-chart-bar', 'mdi-table-large',
                                        'mdi-map-legend', 'mdi-file-chart-outline'],
                        minipaneltooltips=['Download Chart', 'Download Table',
                                           'Download Map', 'Generate Report in Word'],
                        minipanelbuttoncolor='white',
                        onclickminipanel=on_click_minipanel,
                        onclicktab=on_click_tab,
                        onclickcredits=on_click_credits,
                        onclicklogo=on_click_logo,
                        onclickfooter=on_click_footer)

        g_app.show()
        
    .. figure:: figures/app.png
       :scale: 100 %
       :alt: app widget

       App structure example

   """
        
    def __init__(self, 
                 title='Title of the dashboard',
                 titlesvg='',
                 titlesvgclass='pa-0 ma-0',
                 titlecredits='',
                 titlecredits2='',
                 titlestyle='',      # 'font-family: "Times New Roman", Times, serif; font-weight: bold; font-size: 22px;'
                 titlespacestyle='width: 50px; min-width: 50px;',
                 titleheight=70,
                 totalheight=985,
                 dark=settings.dark_mode,
                 backcolor=settings.color_second,
                 titlewidth= '600px',    # '50%'
                 footercolor='lightgrey',
                 backgroundimageurl=None,     #'https://picsum.photos/id/1050/1920/1080?grayscale'
                 backgroundimageposition='center center',
                 logourl='https://jeodpp.jrc.ec.europa.eu/services/shared/Notebooks/images/European_Commission.svg',
                 logomaxwidth  = 80,
                 logomaxheight = 60,

                 titletabs=['Tab 1', 'Tab 2', 'Tab 3'],
                 titletabsdark=False,
                 titletabsactive=0,                       # Index of the tab to activate at start
                 titletabsstile='font-weight: bold;',     #'font-family: "Times New Roman", Times, serif; font-weight: bold;'
                 titletabsactiveparameter=None,           # Name of the URL parameter to read for setting the activetab 
                 titletabscolor=settings.color_first,     # Color of the active tab in the title tabs
                 

                 footertext='%d - Joint Research Centre'%(datetime.now().year),
                 footerbuttons=['Home', 'About Us', 'Team', 'Services', 'Blog', 'Contact Us'],
                 footerheight=68,
                 footercopyright=True,
                 footerdark=False,
                 footercredits='',           # Text for footer credits button
                 footercreditstooltip='',    # Tooltip for the footer credits button
                 footercreditsurl='',        # URL to open when the user click on the footer credits button

                 sidepaneltitle='Settings',
                 sidepanelwidth=400,
                 sidepaneltext='',
                 sidepanelcontent=[],
                 sidepaneldark=settings.dark_mode,
                 sidepanelbackdark=settings.dark_mode,
                 
                 minipanelicons=[],          # See footer.py
                 minipaneltooltips=[],
                 minipanelopen=False,
                 minipanellarge=True,
                 minipanelbuttoncolor=settings.textcolor_notdark,
                 minipaneliconscolor=settings.textcolor_notdark,

                 onclicktab=None,            # Function with 1 string argument string containing the text of the tab
                 onclickcredits=None,        # Function with 0 arguments
                 onclickcredits2=None,       # Function with 0 arguments
                 onclicklogo=None,           # Function with 0 arguments
                 onclickfooter=None,         # Function with 1 string argument string containing the text of the button
                 onclickminipanel=None,      # Function with 1 string argument integer containing the index of the icon
                 fullscreen=False):          # If True the App will fill all the page!
        
        # Storing input parameters
        self.title = title
        self.titlecredits = titlecredits
        self.titlecredits2 = titlecredits2
        self.titlestyle = titlestyle
        self.titleheight = measure2str(titleheight)
        self.totalheight = measure2str(totalheight)
        self.dark = dark
        self.backcolor = backcolor
        self.titlewidth = measure2str(titlewidth)
        self.footercolor = footercolor
        self.backgroundimageurl = backgroundimageurl
        self.backgroundimageposition = backgroundimageposition
        self.logourl = logourl
        self.logomaxwidth = logomaxwidth
        self.logomaxheight = logomaxheight

        self.titletabsstile = titletabsstile
        self.titletabs = titletabs
        self.titletabsactive = titletabsactive
        self.titletabsactiveparameter = titletabsactiveparameter
        self.titletabscolor = titletabscolor

        self.footertext = footertext
        self.footerbuttons = footerbuttons
        self.footerheight = measure2str(footerheight)
        self.footercopyright = footercopyright
        self.footerdark = footerdark
        self.footercredits=footercredits
        self.footercreditstooltip=footercreditstooltip
        self.footercreditsurl=footercreditsurl

        self.sidepaneltitle = sidepaneltitle
        self.sidepanelwidth = sidepanelwidth
        self.sidepaneltext = sidepaneltext
        self.sidepanelcontent = sidepanelcontent
        self.sidepaneldark = sidepaneldark
        self.sidepanelbackdark = sidepanelbackdark

        self.onclicktab = onclicktab
        self.onclickcredits = onclickcredits
        self.onclickcredits2 = onclickcredits2
        self.onclicklogo = onclicklogo
        self.onclickfooter = onclickfooter
        
        self.fullscreen = fullscreen
        
        self.content_vbackground = None     # v.Html object to display an image in the background
        self.content_panels_dict = {}       # Dict to retrieve panels by name
        self.content_panels      = []       # List of panels to overlay to the background
        
        
        if self.dark:
            buttontext = settings.textcolor_dark
            styletext = 'color: ' + settings.textcolor_dark + ';'
        else:
            buttontext = settings.textcolor_notdark
            styletext = 'color: ' + settings.textcolor_notdark + ';'
        
        self.contentheight = 'calc(calc(%s - %s) - %s)' % (self.totalheight, self.titleheight, self.footerheight)

        # Creation of Output widgets
        self.outservice   = widgets.Output(layout=Layout(width='0px', height='0px'))  # Available for the user
        self.outdialogs   = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for snackbars, fab and dialogs
        self.outdownload  = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for downloads
        self.outfabs      = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for fabs
        self.outurlopen   = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for urlOpen
        self.outurlupdate = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for urlUpdate
        self.outplotly    = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for initializing plotly
        self.outpanel     = widgets.Output(layout=Layout(width='0px', height='0px'))  # Used for the side panel
        self.outpanels    = widgets.Output(layout=Layout(width='0px', height='0px'))  # used for the panels 
        
        if self.fullscreen:
            self.outcontent  = widgets.Output(layout=Layout(width='100vw', height='calc(calc(100vh - %s) - %s)' % ( self.titleheight, self.footerheight) ) )
        else:
            self.outcontent  = widgets.Output(layout=Layout(width='99.7%', height=self.contentheight))

        self.outfooter = widgets.Output(layout=Layout(width='99.7%', height='calc(%s + 6px)' % self.footerheight))

        # One instance of the dialogWait
        self.waitdlg = None
        
        # Read the parameters passed on the URL 
        self.parameters = queryStrings.readParameters()
        if not self.titletabsactiveparameter is None:
            self.titletabsactive = int(self.urlParameter(self.titletabsactiveparameter, self.titletabsactive))
                
        
        # Side panel
        self.panel = sidePanel.sidePanel(title=self.sidepaneltitle, text=self.sidepaneltext, content=self.sidepanelcontent,
                                         dark=self.sidepaneldark, backdark=self.sidepanelbackdark,
                                         width=self.sidepanelwidth, right=False, output=self.outpanel, zindex=9999, onclose=self.__internal_panelclosed)

        # App bar containing NavIcon, Title, Tabs, Credits and Logo
        if self.sidepanelwidth > 0:
            self.abi = v.AppBarNavIcon(style_=styletext)
            self.abi.on_event('click', self.__internal_onclickNavIcon)
            self.abih = v.Html(tag='div', class_="pa-0 ma-0 ml-2", children=[self.abi], style_='overflow: hidden; %s' % titlespacestyle)
        else:
            self.abih = v.Html(tag='div', class_="pa-0 ma-0", children=[' '], style_='overflow: hidden; %s' % titlespacestyle)

        if len(titlesvg) > 0:
            outsvg = widgets.Output()
            with outsvg:
                display(HTML(titlesvg))
            self.abt = v.ToolbarTitle(children=[outsvg], class_=titlesvgclass, style_='%s %s' % (styletext, self.titlestyle) )
        else:
            self.abt = v.ToolbarTitle(children=[self.title], style_='%s %s' % (styletext, self.titlestyle) )
            
        
        if self.onclickcredits is None:
            self.credits = v.Btn(text=True, color=buttontext, dark=self.dark, children=[self.titlecredits], rounded=settings.button_rounded, style_='text-transform: none; cursor: initial;')
        else:
            self.credits = v.Btn(text=True, color=buttontext, dark=self.dark, children=[self.titlecredits], rounded=settings.button_rounded, style_='text-transform: none;')
            self.credits.on_event('click', self.__internal_onclickCredits)

        self.credits2 = v.Html(tag='div', children=[''])
        if len(self.titlecredits2) > 0:
            if self.onclickcredits2 is None:
                self.credits2 = v.Btn(text=True, color=buttontext, dark=self.dark, children=[self.titlecredits2], rounded=settings.button_rounded, style_='text-transform: none; cursor: initial;')
            else:
                self.credits2 = v.Btn(text=True, color=buttontext, dark=self.dark, children=[self.titlecredits2], rounded=settings.button_rounded, style_='text-transform: none;')
                self.credits2.on_event('click', self.__internal_onclickCredits2)
            
        self.tlist = []
        for t in self.titletabs:
            telem = v.Tab(style_='%s %s' % ('', self.titletabsstile), children=[t])
            telem.on_event('click', self.__internal_onclickTab)
            self.tlist.append(telem)
        self.tabs = v.Tabs(v_model=self.titletabsactive, dark=titletabsdark, color=self.titletabscolor, background_color='transparent', 
                           align_with_title=True, children=self.tlist, height=self.titleheight, min_height=self.titleheight, max_height=self.titleheight)

        s = v.Spacer()
        logostyle = ''
        if not self.onclicklogo is None: logostyle = 'cursor: pointer;'
        self.logoimg = v.Img(src=self.logourl, class_='pa-0 ma-0', style_=logostyle, contain=True, height=self.logomaxheight, width=self.logomaxwidth, max_height=self.logomaxheight, max_width=self.logomaxwidth)
        self.logoimg.on_event('click', self.__internal_onclickLogo)
        
        card1 = v.Card(height=titleheight, color='transparent', elevation=0, children=[self.abih],    class_="d-flex align-center")
        card2 = v.Card(height=titleheight, color='transparent', elevation=0, children=[self.abt],     class_="d-flex align-center", style_='overflow: hidden; width: %s;' % self.titlewidth)
        card3 = v.Card(height=titleheight, color='transparent', elevation=0, children=[self.tabs],    class_="d-flex align-center")
        card4 = v.Card(height=titleheight, color='transparent', elevation=0, children=[self.credits, self.credits2], class_="d-flex align-center")
        card5 = v.Card(height=titleheight, color='transparent', elevation=0, children=[self.logoimg], class_="d-flex align-center mr-1")
        
        if len(self.titletabs) > 0:
            r = v.Row(justify="space-between", children=[card1,card2,card3,s,card4,card5], class_="pa-0 ma-0")
        else:
            r = v.Row(justify="space-between", no_gutters=True, children=[card1,card2,s,card4,card5], class_="pa-0 ma-0")
        if (not self.backgroundimageurl is None) and (len(self.backgroundimageurl) > 0):
            self.appbar = v.Img(src=self.backgroundimageurl, position=self.backgroundimageposition, children=[r], class_='pa-0 ma-0', style_='height: %s; overflow: hidden;' % self.titleheight, max_height=self.titleheight)
        else:
            self.appbar = v.Footer(color=backcolor, padless=True, children=[r], class_='pa-0 ma-0', style_='height: %s; overflow: hidden;' % self.titleheight, max_height=self.titleheight)

    
        # Footer
        if len(self.footerbuttons) > 0:
            self.f = footer.footer(text=self.footertext, color=self.footercolor, copyright=self.footercopyright, dark=self.footerdark,
                                   minipanelicons=minipanelicons, minipaneltooltips=minipaneltooltips, minipanelopen=minipanelopen,
                                   minipanellarge=minipanellarge, minipanelbuttoncolor=minipanelbuttoncolor, 
                                   minipaneliconscolor=minipaneliconscolor, onclickminipanel=onclickminipanel,
                                   footercredits=self.footercredits, footercreditstooltip=self.footercreditstooltip, onclickcredits=self.__internal_onclickFooterCredits,
                                   buttons=self.footerbuttons, marginy=2, height=self.footerheight, onclick=self.onclickfooter) #, output=self.outfooter)
        else:
            self.f = footer.footer(text=self.footertext, color=self.footercolor, copyright=self.footercopyright, dark=self.footerdark,
                                   minipanelicons=minipanelicons, minipaneltooltips=minipaneltooltips, minipanelopen=minipanelopen,
                                   minipanellarge=minipanellarge, minipanelbuttoncolor=minipanelbuttoncolor, 
                                   minipaneliconscolor=minipaneliconscolor, onclickminipanel=onclickminipanel,
                                   footercredits=self.footercredits, footercreditstooltip=self.footercreditstooltip, onclickcredits=self.__internal_onclickFooterCredits,
                                   marginy=2, height=self.footerheight, onclick=self.onclickfooter) #, output=self.outfooter)


        # Initialize Plotly with a 0x0 chart!
        with self.outplotly:
            data = {'name': ['mike', 'mike', 'cindy', 'cindy'],
                    'week': ['Week 1', 'Week 2', 'Week 1', 'Week 2'],
                    'perc': [0.45, 0.15, 0.25, 0.28]}
            df = pd.DataFrame(data)
            fig = px.bar(df, x="name", y="perc", color="week", title="", barmode='stack')
            fig.show()
    
    
    # Set the background image for the outcontent
    def contentBackground(self, imageUrl=None):
        """
        Sets the background image for the outcontent output widget

        Parameters
        ----------
        imageUrl : str, optional
            URL of the optional image to display as background of the outcontent output widget (default is None)
        """
        if imageUrl is None:
            self.content_vbackground = None
            self.outcontent.clear_output()
        else:
            self.content_vbackground = v.Html(tag='div', children=[''], class_="pa-0 ma-0", style_="width: 100vw; height: %s; border: 0px solid red; background-image: url('%s'); ; background-repeat: repeat;" % (self.outcontent.layout.height, imageUrl))
            self.outcontent.clear_output()
            with self.outcontent:
                display(self.content_vbackground)


    # Remove all panels
    def contentResetPanels(self):
        """
        Resets the list of panels to display on top of the outcontent output widget
        """
        self.content_panels_dict = {}
        self.content_panels      = []
        self.outpanels.clear_output()
        if (not self.content_vbackground is None) :
            self.content_vbackground.children = []

            
    # Adds a new panel
    def contentAddPanel(self, width, height, left, top, border='1px solid black', backcolor='white', name='', number=None,
                              title='', titleround=False, titlewidth='8vw', titleheight='2.4vh', titlefontsize='1.8vh', titlefontweight=500,
                              icon='', icontooltip='', iconcolor='black', icononclick=None):
        """
        Adds a new panel to overlay on top of the outcontent output widget.
        
        Parameters
        ----------
        width : str
            Width of the panel (can be in any CSS coordinates, examples: '300px', '40vw' or 'calc(100vw - 600px)')
        height : str
            Height of the panel (can be in any CSS coordinates, examples: '300px', '40vh' or 'calc(100vh - 400px)')
        left : str
            Position of the panel from the left border of the outcontent output widget (can be in any CSS coordinates, examples: '300px' or '10vw')
        top : str
            Position of the panel from the top border of the outcontent output widget (can be in any CSS coordinates, examples: '300px' or '10vh')
        border : str, optional
            Border of the panel (default is '1px solid black')
        backcolor : str, optional
            Background color of the panel (default is 'white'). Please be aware that colors different from 'white' work badly if used for panels that will contain ipywidgets or ipyvuetify widgets. Transparent colors (for example: #ffffff00) or semi-transparent colors (for example: #ffffff55) work well if the panel contains only one of the SVG charts of the vois library (svhHeatmap, svgBubblesChart, etc.)
        name : str, optional
            Name of the panel (default is '')
        number : int, optional
            Number to assign to the panel, to generate unique CSS class names (default is None which means that the number is automatically generated)
        title : str, optional
            Title to show in the top-left border of the panel (default is '')
        titleround : bool, optional
            If True the sides of the title are rounded (default is False)
        titlewidth : str, optional
            Width of the title area (default is '8vw')
        titleheight : str, optional
            Height of the title area (default is '2.4vh')
        titlefontsize : str, optional
            Size of the font to use to display the title (default is '1.8vh')
        titlefontweight : int, optional
            Weight of the font to use to display the title (default is 500)
        icon : str, optional
            Name of an icon to display in the title bar of the panel (default is None)
        icontooltip : str, optional
            Tooltip to show when hover on the icon (default is '')
        iconcolor : str, optional
            Color of the icon (default is 'black')
        icononclick : function, optional
            Python function to call when the user clicks on the icon. The function will receive as parameter the name of the panel (default is None)
        """
        out = widgets.Output(layout=Layout(width=width, height=height, border=border))
        if number is None: num = randrange(999999)
        else:              num = int(Number)
        classname = "%s_panel_out_%d" % (name,num)
        out.add_class(classname)
        out.clear_output()
        with self.outpanels:
            display(HTML('<style> .%s { background-color: %s !important; }</style>' % (classname, backcolor) ))
        panel = v.Html(tag='div', children=[out], class_="pa-0 ma-0", style_='width: %s; height: %s; border: none; position: absolute; top: %s; left: %s;' % (width, height, top, left))
        self.content_panels.append(panel)
        if len(name) > 0:
            self.content_panels_dict[name] = [panel]
        
        if len(title) > 0 :
            radius = "0px 0px 0px 0px"
            if titleround :
                radius = "4px 4px 0px 0px"
            border   = 'border-radius: %s; border: %s; border-style: solid solid none solid;' % (radius, border)
            position = 'position: absolute; top: calc(%s - %s); left: %s;' % (top, titleheight, left)
            
            children = [title]
            b = None
            if len(icon) > 0:
                b = Button('', textcolor='#ffffff00', onclick=icononclick, argument=name, width=36, small=False, disabled=False, height=titleheight, outlined=False,
                                  tooltip=icontooltip, selected=False, icon=icon, iconleft=True, iconcolor=iconcolor, rounded=False)
                children = [v.Row(no_gutters=True, justify="space-between", children=[title,b.draw()])]
            
            titlecard = v.Card(width=titlewidth, elevation=0, color=backcolor, children=children,
                               style_='font-family: %s; line-height: %s; font-size: %s; font-weight: %d; padding-left: 8px; text-align: start; %s %s' % (fontsettings.font_name, titleheight, titlefontsize, titlefontweight, border, position) )
            self.content_panels.append(titlecard)
            if len(name) > 0:
                self.content_panels_dict[name].append(titlecard)
            
        return out

    

    # Change settings of an existing panel given its name
    def contentSetPanel(self, name, width, height, left, top, border='1px solid black', backcolor='white',
                             titleround=False, titlewidth='8vw', titleheight='2.4vh', titlefontsize='1.8vh', titlefontweight=500,
                             icon='', icontooltip='', iconcolor='black', icononclick=None):
        """
        Change position, sizing and colors of a panel given its name.
        
        Parameters
        ----------
        name : str
            Name of the panel to modify
        width : str
            Width of the panel (can be in any CSS coordinates, examples: '300px', '40vw' or 'calc(100vw - 600px)')
        height : str
            Height of the panel (can be in any CSS coordinates, examples: '300px', '40vh' or 'calc(100vh - 400px)')
        left : str
            Position of the panel from the left border of the outcontent output widget (can be in any CSS coordinates, examples: '300px' or '10vw')
        top : str
            Position of the panel from the top border of the outcontent output widget (can be in any CSS coordinates, examples: '300px' or '10vh')
        border : str, optional
            Border of the panel (default is '1px solid black')
        backcolor : str, optional
            Background color of the panel (default is 'white'). Please be aware that colors different from 'white' work badly if used for panels that will contain ipywidgets or ipyvuetify widgets. Transparent colors (for example: #ffffff00) or semi-transparent colors (for example: #ffffff55) work well if the panel contains only one of the SVG charts of the vois library (svhHeatmap, svgBubblesChart, etc.)
        titleround : bool, optional
            If True the sides of the title are rounded (default is False)
        titlewidth : str, optional
            Width of the title area (default is '8vw')
        titleheight : str, optional
            Height of the title area (default is '2.4vh')
        titlefontsize : str, optional
            Size of the font to use to display the title (default is '1.8vh')
        titlefontweight : int, optional
            Weight of the font to use to display the title (default is 500)
        icon : str, optional
            Name of an icon to display in the title bar of the panel (default is None)
        icontooltip : str, optional
            Tooltip to show when hover on the icon (default is '')
        iconcolor : str, optional
            Color of the icon (default is 'black')
        icononclick : function, optional
            Python function to call when the user clicks on the icon. The function will receive as parameter the name of the panel (default is None)
        """
        if name in self.content_panels_dict:
            panellist = self.content_panels_dict[name]
            panel     = panellist[0]
            titlecard = None
            if len(panellist) > 1:
                titlecard = panellist[1]
                
            if not titlecard is None and type(titlecard.children[0]) == v.generated.Row:
                title = titlecard.children[0].children[0]
            else:
                title = titlecard.children[0]
                
            if not titlecard is None:
                if len(icon) > 0:
                    b = Button('', textcolor='#ffffff00', onclick=icononclick, argument=name, width=36, small=False, disabled=False, height=titleheight, outlined=False,
                                      tooltip=icontooltip, selected=False, icon=icon, iconleft=True, iconcolor=iconcolor, rounded=False)
                    titlecard.children = [v.Row(no_gutters=True, justify="space-between", children=[title,b.draw()])]
                else:
                    titlecard.children = [title]
            
            classname = panel.children[0]._dom_classes[0]
            with self.outpanels:
                display(HTML('<style> .%s { background-color: %s !important; }</style>' % (classname, backcolor) ))
            panel.children[0].layout = Layout(width=width, height=height, border=border)
            panel.style_ = 'width: %s; height: %s; border: none; position: absolute; top: %s; left: %s;' % (width, height, top, left)
            panel.color = backcolor
            if not titlecard is None:
                radius = "0px 0px 0px 0px"
                if titleround :
                    radius = "4px 4px 0px 0px"
                border   = 'border-radius: %s; border: %s; border-style: solid solid none solid;' % (radius, border)
                position = 'position: absolute; top: calc(%s - %s); left: %s;' % (top, titleheight, left)
                titlecard.color  = backcolor
                titlecard.width  = titlewidth
                titlecard.style_ = 'font-family: %s; line-height: %s; font-size: %s; font-weight: %d; padding-left: 8px; text-align: start; %s %s' % (fontsettings.font_name, titleheight, titlefontsize, titlefontweight, border, position)

                
    
    # Display the app
    def show(self):
        """Display the app"""
        if (not self.content_vbackground is None) and (len(self.content_panels) > 0):
            self.content_vbackground.children = self.content_panels
            
        # Fix Firefox bug with white areas: with this fix all v.Img objects MUST declare the width and height to work correctly
        with self.outdialogs:
            display(HTML('<style>.v-responsive__sizer { padding-bottom: 0px !important; }</style>'))
            
        if self.fullscreen:
            outFullscreen = widgets.Output(layout=Layout(width='100vw', height='100vh'))
            #outFullscreen.add_class('box')
            with self.outdialogs:
                display(HTML('<style>.jp-OutputPrompt { min-width: 0px; border: 0px; }</style>'))
            with outFullscreen:
                display(self.appbar)
                display(widgets.HBox([self.outservice,self.outdialogs,self.outdownload,self.outfabs,self.outurlopen,self.outurlupdate,self.outplotly,self.outpanel,self.outpanels]))
                display(self.outcontent)
                display(self.f.draw())
                
            run_in_voila = True
            try:
                from voila.utils import get_query_string
            except:
                run_in_voila = False
                    
            transition = 'dialog-fade-transition'
            persistent = False
            if run_in_voila: persistent = True

            background = v.Card(children=[outFullscreen])
            dialog = v.Dialog(v_model=True, fullscreen=True, transition=transition, persistent=persistent, no_click_animation=True, children=[background], style_='z-index:20001;')
            display(dialog)
        else:
            display(self.appbar)
            display(widgets.HBox([self.outservice,self.outdialogs,self.outdownload,self.outfabs,self.outurlopen,self.outurlupdate,self.outplotly,self.outpanel]))
            display(self.outcontent)
            #display(self.outfooter)
            display(self.f.draw())

    # Sets the active tab
    def setActiveTab(self, index):
        """Set the active tab of the title bar of the app"""
        if index >= 0 and index < len(self.tlist):
            self.titletabsactive = index
            self.tabs.v_model = self.titletabsactive
        
    # Manage click on the navigation icon to open the side panel
    def __internal_onclickNavIcon(self, *args):
        self.panel.show()
    
    # Manage click on the logo
    def __internal_onclickLogo(self, *args):
        if not self.onclicklogo is None:
            self.onclicklogo()
            
    # Manage click on the title tabs 
    def __internal_onclickTab(self, widget, event, data):
        if self.onclicktab:
            i = self.tlist.index(widget)
            self.onclicktab(self.titletabs[i])
            
    # Manage click on the title credits button
    def __internal_onclickCredits(self, widget, event, data):
        if not self.onclickcredits is None:
            self.onclickcredits()
        
    # Manage click on the title credits2 button
    def __internal_onclickCredits2(self, widget, event, data):
        if not self.onclickcredits2 is None:
            self.onclickcredits2()
            
    # When the panel has bee closed
    def __internal_panelclosed(self):
        self.outpanel.clear_output()
        with self.outpanel:
            display(self.panel.nav)
            
    # Manage click on the footer credits button
    def __internal_onclickFooterCredits(self, *args):
        if len(self.footercreditsurl) > 0:
            self.urlOpen(self.footercreditsurl, target='_blank')
        
        
    # Display something in the service Output of this application
    def display(self, arg):
        """Display something in the service Output of this application"""
        with self.outservice:
            display(arg)

            
    # Display a message in a snackbar
    def snackbar(self, *args, **kwargs):
        """Display a message in a snackbar. See :func:`~snackbar.snackbar` for the list of parameters."""
        #if not 'color' in kwargs: kwargs['show'] = 
        kwargs['show']   = True
        kwargs['output'] = self.outdialogs
        snackbar.snackbar(*args, **kwargs)
        
    # Display a dialogMessage
    def dialogMessage(self, *args, **kwargs):
        """Display a dialogMessage. See :func:`~dialogMessage.dialogMessage` for the list of parameters."""
        kwargs['show']   = True
        kwargs['output'] = self.outdialogs
        dialogMessage.dialogMessage(*args, **kwargs)
        
    # Display a dialogYesNo
    def dialogYesNo(self, *args, **kwargs):
        """Display a dialogYesNo. See :func:`~dialogYesNo.dialogYesNo` for the list of parameters."""
        kwargs['show']   = True
        kwargs['output'] = self.outdialogs
        dialogYesNo.dialogYesNo(*args, **kwargs)
        
    # Display a dialogGeneric
    def dialogGeneric(self, *args, **kwargs):
        """Display a dialogGeneric. See :func:`~dialogGeneric.dialogGeneric` for the list of parameters."""
        kwargs['show']   = True
        kwargs['output'] = self.outdialogs
        dialogGeneric.dialogGeneric(*args, **kwargs)
        
    # Open a dialogWait
    def dialogWaitOpen(self, *args, **kwargs):
        """Open a dialogWait. See :func:`~dialogWait.dialogWait` for the list of parameters."""
        kwargs['output'] = self.outdialogs
        self.waitdlg = dialogWait.dialogWait(*args, **kwargs)

    # Close the dialogWait
    def dialogWaitClose(self):
        """Close the dialogWait. See :func:`~dialogWait.dialogWait.close`."""
        if not self.waitdlg is None:
            self.waitdlg.close()
            self.waitdlg = None
        
        
    # Open a fab button
    def fab(self, *args, **kwargs):
        """Open a fab button. See :func:`~fab.fab` for the list of parameters."""
        kwargs['output'] = self.outfabs
        return fab.fab(*args, **kwargs)
        
            
    # Direct download of a .txt file containing a string
    def downloadText(self, textobj, fileName="download.txt"):
        """Direct download of a .txt file containing a string.
        
        Parameters
        ----------
        textobj : str
            Text to write in the file to be downloaded
        fileName : str, optional
            Name of the file that is to be downloaded (default is 'download.txt')

        Example
        -------
        If g_app is an instance of the app class, this code will download a text file containing the passed string::

            g_app.downloadText('aaa bbb ccc')
        """

        string_bytes  = textobj.encode("ascii","ignore")
        base64_bytes  = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")

        self.outdownload.clear_output()
        with self.outdownload:
            display(HTML('<script>function downloadURI(uri, name) { var link = document.createElement("a"); link.download = name; link.href = uri; link.click();} downloadURI("data:application/octet-stream;charset=utf-8;base64,' + base64_string + '","' + fileName + '"); </script>'))
        self.outdownload.clear_output()


    # Direct download of an array of bytes
    def downloadBytes(self, bytesobj, fileName="download.bin"):
        """Direct download of an array of bytes.
        
        Parameters
        ----------
        bytesobj : bytes-like object
            Bytes to write in the file to be downloaded
        fileName : str, optional
            Name of the file that is to be downloaded (default is 'download.bin')

        Example
        -------
        If g_app is an instance of the app class, this code will download a binary file containing the passed bytes::

            g_app.downloadBytes(b'ajgh lkjhl ')
        """
        base64_bytes  = base64.b64encode(bytesobj)
        base64_string = base64_bytes.decode("ascii")

        self.outdownload.clear_output()
        with self.outdownload:
            display(HTML('<script>function downloadURI(uri, name){ var link = document.createElement("a"); link.download = name; link.href = uri; link.click();} downloadURI("data:application/octet-stream;charset=utf-8;base64,''' + base64_string + '","' + fileName + '");</script>'))
        self.outdownload.clear_output()
            
            
    # Open a web page in another tab
    def urlOpen(self, url, target='_blank'):
        """Open a web page in another tab.
        
        Parameters
        ----------
        url : str
            URL of the page to be opened
        target : str, optional
            Target of the open operation (default is '_blank' which means that the page will be opened in a new browser's tab)

        Example
        -------
        If g_app is an instance of the app class, this code will open a new tab in the browser::

            g_app.urlOpen('https://www.google.com')
        """
        js = '<script type=\"text/javascript\">window.open("%s", "%s");</script>' % (url,target)
        with self.outurlopen:
            display(ipyhtml(js))
                
                
    # Read the parameters passed on the URL 
    def urlParameter(self, parameterName, parameterDefaultValue=''):
        """Read the parameters passed on the URL.
        
        Parameters
        ----------
        parameterName : str
            name of the parameter to read from the URL that launched the Voilà dashboard
        parameterDefaultValue : str, optional
            Default value of the parameter, in case it is not present in the URL that launched the Voilà dashboard (default is '')

        Example
        -------
        If g_app is an instance of the app class, this code print the value of an URL parameter::

            print(g_app.urlParameter('activetab'))
        """
        return self.parameters.get(parameterName, [parameterDefaultValue])[0]
        
            
    # Update the visualized URL in the browser
    def urlUpdate(self, url):
        """Update the URL visualized in the top bar of the browser.
        
        Parameters
        ----------
        url : str
            Partial url to add to the current browser's page key/values

        Example
        -------
        If g_app is an instance of the app class, this code will add a key=value to the URL of the application::

            g_app.urlUpdate('?test=3')
        """
        
        js = "<script>window.history.replaceState({ additionalInformation: 'Updated the URL with JS' }, '', '%s');</script>" % url
        with self.outurlupdate:
                display(HTML(js))
