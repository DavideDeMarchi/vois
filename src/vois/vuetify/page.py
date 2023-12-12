"""Fullscreen page"""
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

# Imports
from IPython.display import display
from ipywidgets import widgets, Layout
import ipyvuetify as v

try:
    from . import settings
    from . import dialogGeneric
    from . import tooltip
except:
    import settings
    import dialogGeneric
    import tooltip


#####################################################################################################################################################
# Open a page in fullscreen mode
#####################################################################################################################################################
class page():
    """
    Fullsceen page with title and footer bar.
        
    Parameters
    ----------
    appname : str
        Name of the application. It will be displayed on the left side of the title bar
    title : str
        Title of the page
    output : instance of widgets.Output() class
        Output widget to be used for the opening of the fullscreen dialog that implements the page
    onclose : function, optional
        Python function to call when the user closes the page. The function will receive no parameters (default is None)
    titlecolor : str, optional
        Color to use for the title bar background (default is settings.color_first)
    titledark : bool, optional
        If True the text on the title bar will be displayed in white, otherwise in black color (defaul is True)
    titleheight : int, optional
        Height of the title bar in pixels (default is 54)
    footercolor : str, optional
        Color to use fir the footer bar background (default is settings.color_second)
    footerdark : bool, optional
        If True the text on the footer bar will be displayed in white, otherwise in black color (defaul is False)
    footerheight : int, optional
        Height of the footer bar in pixels (default is 30)
    logoappurl : str, optional
        String containing the url of the application logo, to be displayed on the left side of the title bar (default is '')
    logowidth : int, optional
        Width in pixels of the logo button (default is 40)
    on_logoapp : function, optional
        Python function to call when the user clicks on the pplication logo. The function will receive no parameters (default is None)
    copyrighttext : str, optional
        Text to display as copyright message on the footer bar (default is '')
    show_back : bool, optional
        If True a "back" button is displayed on the right side of the title bar (default is True)
    show_help : bool, optional
        If True a "help" button is displayed on the right side of the title bar (default is True)
    on_help : function, optional
        Python function to call when the user clicks the help button. The function will receive no parameters (default is None)
    logocreditsurl : str, optional
        String containing the url of the credits logo, to be displayed on the right side of the title bar (default is ''). If no url is passed, the logo of the European Commission is displayed
    show_credits : bool, optional
        If True a "credits" button is displayed on the right side of the title bar (default is True)
    on_credits : function, optional
        Python function to call when the user clicks the credits button. The function will receive no parameters (default is None)
    transition : str, optional
        Transition to be used for display and hide of the page (default is 'dialog-bottom-transition'). See: https://vuetifyjs.com/en/styles/transitions/ for a list of available transitions (substitute 'v-' with 'dialog-')
    persistent : bool, optional
        If True the page will be persistent and not close at the hitting of the "ESC" key (default is False)

    Examples
    --------
    Creation of an example page::
        
        from vois.vuetify import page
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)
        
        def onclose():
            pass

        def on_click():
            pass
            
        p = page.page('Application XYZ', 'Map page', output, onclose=onclose,
                      titlecolor='#008800', titledark=True,
                      footercolor='#cccccc', footerdark=False,
                      logoappurl='https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/BDAP_Logo1024transparent.png',
                      on_logoapp=on_click, copyrighttext='European Commission - Joint Research Centre',
                      show_back=True, show_help=True, on_help=on_click,
                      show_credits=True, on_credits=on_click)
                      
        card = p.create()
        card.children = []
        p.open()


    .. figure:: figures/page.png
       :scale: 100 %
       :alt: page widget

       Example of a page
       

    """
    
    # Click on the APP logo
    def click_on_logoapp(self, *args):
        if not self.on_logoapp is None:
            self.on_logoapp()

    # Click on the back button
    def click_on_back(self, *args):
        self.close()
    
    # Click on the help button
    def click_on_help(self, *args):
        if not self.on_help is None:
            self.on_help()
    
    # Click on the credits button
    def click_on_credits(self, *args):
        if not self.on_credits is None:
            self.on_credits()
  
    
    # Create the page and returns the card widget where the content of the page must be displayed
    def create(self):
        
        textcolor = 'black'
        if self.titledark:
            textcolor = 'white'
        
        children = []
        
        if not self.logoapp is None:
            btn_logo = v.Btn(text=True, rounded=False, ripple=False, style_='width: %dpx; height: 40px;'%self.logowidth, class_='pa-0 ma-0 ml-1', children=[self.logoapp])
            btn_logo.on_event('click', self.click_on_logoapp)
            if len(self.appname) > 0:
                children.append(tooltip.tooltip("Info on %s"%self.appname, btn_logo))
            else:
                children.append(btn_logo)
            
        if len(self.appname) > 0:
            title = v.ToolbarTitle(children=['%s:'%self.appname],  class_='pa-0 ma-0 mt-1 ml-1', style_='height: 30px; color: %s; font-size: 26;'%textcolor)
            children.append(title)
            
        if len(self.title) > 0:
            subtitle = v.ToolbarTitle(children=[self.title], class_='pa-0 ma-0 mt-1 ml-2', style_='height: 30px; color: %s; font-size: 26;'%textcolor)
            children.append(subtitle)
        
        children.append(v.Spacer())
        
        for cb in self.custom_buttons:
            iconname,tooltiptext,callback = cb
            btn = v.Btn(icon=True, class_="pa-0 ma-0 mt-1", dark=self.titledark, children=[v.Icon(children=[iconname])])
            btn.on_event('click', callback)
            children.append(tooltip.tooltip(tooltiptext, btn))
        
        if self.show_back:
            btn_back = v.Btn(icon=True, class_="pa-0 ma-0 mt-1", dark=self.titledark, children=[v.Icon(children=['mdi-arrow-left'])])
            btn_back.on_event('click', self.click_on_back)
            children.append(tooltip.tooltip("Close current page", btn_back))
            
        if self.show_help:
            btn_help = v.Btn(icon=True, class_="pa-0 ma-0 mt-1 mr-3", dark=self.titledark, children=[v.Icon(children=['mdi-help'])])
            btn_help.on_event('click', self.click_on_help)
            children.append(tooltip.tooltip("Display application help", btn_help))

        if self.show_credits:
            btn_credits = v.Btn(text=True, rounded=False, ripple=False, style_='width: 170px;  height: %dpx;'%(self.titleheight-4), class_='pa-0 ma-0 mr-1', children=[self.logoCredits])
            btn_credits.on_event('click', self.click_on_credits)
            children.append(tooltip.tooltip("Open credits info", btn_credits))
            
        self.appbar = v.AppBar(height=self.titleheight, min_height=self.titleheight, max_height=self.titleheight, color=self.titlecolor, children=children)


        # Content of the footer bar
        textcolor = 'black'
        if self.footerdark:
            textcolor = 'white'
            
        copyicon = v.Icon(class_="pa-0 ma-0 mr-2", small=True, color=textcolor, children=['mdi-copyright'])
        ctext = v.Card(flat=True, color=self.footercolor, style_='color: %s;'%textcolor, children=[self.copyrighttext])
        frow = v.Row(class_='pa-0 ma-0 mt-n2 mb-n3', justify="center", no_gutters=True, children=[copyicon,ctext])
        self.footer = v.Footer(color=self.footercolor, padless=True, children=[frow], class_='pa-0 ma-0', rounded=False,
                               height=self.footerheight, max_height=self.footerheight, min_height=self.footerheight,
                               style_='height: %dpx; overflow: hidden; border-bottom-left-radius: 0; border-bottom-right-radius: 0;'%self.footerheight)

        # Main content of the page: a card to be filled with custom content
        self.height = 'calc(100vh - %dpx)'%(self.titleheight+self.footerheight)
        self.card = v.Card(children=[], elevation=5,class_="pa-0 ma-0", style_='width: 100vw; max-width: 100vw; height: %s; max-height: %s;'%(self.height,self.height))
        return self.card
    
    
    # Open the dialog
    def open(self):
        self.dlg = dialogGeneric.dialogGeneric(title='', titleheight='0px', text='', show=True, no_click_animation=True,
                                               addclosebuttons=False, persistent=self.persistent, transition=self.transition,
                                               fullscreen=True, content=[self.appbar,self.card,self.footer], output=self.output)
        
        
    # Close the dialog
    def close(self):
        if not self.dlg is None:
            self.dlg.close()
            if not self.onclose is None:
                self.onclose()
        
        
    # Add a custom buttom to the page (before the call to create!)
    def customButtonAdd(self, iconname, tooltiptext, callback):
        self.custom_buttons.append((iconname,tooltiptext,callback))   # Each item has an icon name, a tooltip string and a callback function
    
    # Remove all custom buttons
    def customButtonClear(self):
        self.custom_buttons = []
        
    
    # Initialization
    def __init__(self,
                 appname,
                 title,
                 output,
                 onclose=None,
                 titlecolor=settings.color_first,
                 titledark=True,
                 titleheight=54,
                 footercolor=settings.color_second,
                 footerdark=False,
                 footerheight=30,
                 logoappurl='',
                 logowidth=40,
                 on_logoapp=None,
                 copyrighttext='',
                 show_back=True,
                 show_help=True,
                 on_help=None,
                 logocreditsurl='',
                 show_credits=True,
                 on_credits=None,
                 transition='dialog-bottom-transition',
                 persistent=False):

        self.dlg = None
        
        self.appname = appname
        self.title   = title
        self.output  = output
        self.onclose = onclose
        
        self.titlecolor  = titlecolor
        self.titledark   = titledark
        self.titleheight = titleheight
        
        self.footercolor  = footercolor
        self.footerdark   = footerdark
        self.footerheight = footerheight
        self.logowidth    = logowidth
        
        self.copyrighttext = copyrighttext
        self.show_back     = show_back
        self.show_help     = show_help
        self.on_help       = on_help
        self.show_credits  = show_credits
        self.on_credits    = on_credits
        self.on_logoapp    = on_logoapp
        
        self.transition    = transition
        self.persistent    = persistent
        
        self.custom_buttons = []   # Each item has an icon name, a tooltip string and a callback function
        
        if len(logoappurl) > 0:
            self.logoapp = v.Img(class_='pa-0 ma-0 mr-2', max_width=self.logowidth, src=logoappurl)
        else:
            self.logoapp = None
        
        if len(logocreditsurl) > 0:
            self.logoCredits = v.Img(class_='pa-0 ma-0 mr-2', max_width=120, src=logocreditsurl)
        else:
            self.logoCredits = v.Img(class_='pa-0 ma-0 mr-2', max_width=120, src='data:image/png;base64,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')
