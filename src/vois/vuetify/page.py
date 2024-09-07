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
    titleimageurl : str, optional
        String containing the url of the title bar backbround image (default is '')
    footercolor : str, optional
        Color to use fir the footer bar background (default is settings.color_second)
    footerdark : bool, optional
        If True the text on the footer bar will be displayed in white, otherwise in black color (defaul is False)
    footerheight : int, optional
        Height of the footer bar in pixels (default is 30)
    logoappurl : str, optional
        String containing the url of the application logo, to be displayed on the left side of the title bar (default is '')
    logowidth : int, optional
        Width in pixels of the application logo button (default is 40)
    on_logoapp : function, optional
        Python function to call when the user clicks on the pplication logo. The function will receive no parameters (default is None)
    copyrighttext : str, optional
        Text to display as copyright message on the footer bar (default is '')
    show_back : bool, optional
        If True a "back" button is displayed in the title bar (default is True)
    left_back : bool, optional
        If True the "back" button is displayed on the left side of the title bar (default is False)
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
        try:
            self.close()
        except:
            pass
    
    # Click on the help button
    def click_on_help(self, *args):
        if not self.on_help is None:
            self.on_help()
    
    # Click on the credits button
    def click_on_credits(self, *args):
        if not self.on_credits is None:
            self.on_credits()


    # Internal method to create the childrens of the self.appbar instance
    def _create_appbar_children(self):
        textcolor = 'black'
        if self._titledark:
            textcolor = 'white'
        
        children = []
        
        if not self.logoapp is None:
            btn_logo = v.Btn(text=True, rounded=False, ripple=False, style_='width: %dpx; height: 40px;'%self._logowidth, class_='pa-0 ma-0 ml-1', children=[self.logoapp])
            btn_logo.on_event('click', self.click_on_logoapp)
            if len(self._appname) > 0:
                children.append(tooltip.tooltip("Info on %s"%self._appname, btn_logo))
            else:
                children.append(btn_logo)
            
        self.toolbarTitle = None
        if len(self._appname) > 0:
            self.toolbarTitle = v.ToolbarTitle(children=['%s:'%self._appname],  class_='pa-0 ma-0 mt-1 ml-1', style_='height: 30px; color: %s; font-size: 26;'%textcolor)
            children.append(self.toolbarTitle)
            
        self.toolbarSubtitle = None
        if len(self._title) > 0:
            self.toolbarSubtitle = v.ToolbarTitle(children=[self._title], class_='pa-0 ma-0 mt-1 ml-2', style_='height: 30px; color: %s; font-size: 26;'%textcolor)
            children.append(self.toolbarSubtitle)
        
        children.append(v.Spacer())
        
        self.buttons = []
        for cb in self.custom_buttons:
            iconname,tooltiptext,callback = cb
            btn = v.Btn(icon=True, class_="pa-0 ma-0 mt-1", dark=self._titledark, children=[v.Icon(children=[iconname])])
            btn.on_event('click', callback)
            self.buttons.append(btn)
            children.append(tooltip.tooltip(tooltiptext, btn))
        
        self.btn_back = None
        if self._show_back:
            self.btn_back = v.Btn(icon=True, class_="pa-0 ma-0 mt-1", dark=self._titledark, children=[v.Icon(children=['mdi-arrow-left'])])
            self.btn_back.on_event('click', self.click_on_back)
            elem = tooltip.tooltip("Close current page", self.btn_back)
            if self._left_back:
                children.insert(0, elem)
            else:
                children.append(elem)
        
        self.btn_help = None
        if self._show_help:
            self.btn_help = v.Btn(icon=True, class_="pa-0 ma-0 mt-1 mr-3", dark=self._titledark, children=[v.Icon(children=['mdi-help'])])
            self.btn_help.on_event('click', self.click_on_help)
            children.append(tooltip.tooltip("Display application help", self.btn_help))

        self.btn_credits = None
        if self._show_credits:
            self.btn_credits = v.Btn(text=True, rounded=False, ripple=False, style_='width: 170px;  height: %dpx;'%(self._titleheight-4), class_='pa-0 ma-0 mr-1', children=[self.logoCredits])
            self.btn_credits.on_event('click', self.click_on_credits)
            children.append(tooltip.tooltip("Open credits info", self.btn_credits))
        
        return children

    
    # Create the page and returns the card widget where the content of the page must be displayed
    def create(self):
        self.appbar = v.AppBar(height=self._titleheight, min_height=self._titleheight, max_height=self._titleheight, color=self._titlecolor,
                               children=self._create_appbar_children())

        if len(self._titleimageurl) > 0:
            self.appbar.src = self._titleimageurl


        # Content of the footer bar
        textcolor = 'black'
        if self._footerdark:
            textcolor = 'white'
            
        self.copyicon = v.Icon(class_="pa-0 ma-0 mr-2", small=True, color=textcolor, children=['mdi-copyright'])
        self.ctext = v.Card(flat=True, color=self._footercolor, style_='color: %s;'%textcolor, children=[self._copyrighttext])
        frow = v.Row(class_='pa-0 ma-0 mt-n2 mb-n3', justify="center", no_gutters=True, children=[self.copyicon,self.ctext])
        self.footer = v.Footer(color=self._footercolor, padless=True, children=[frow], class_='pa-0 ma-0', rounded=False,
                               height=self._footerheight, max_height=self._footerheight, min_height=self._footerheight,
                               style_='height: %dpx; overflow: hidden; border-bottom-left-radius: 0; border-bottom-right-radius: 0;'%self._footerheight)

        # Main content of the page: a card to be filled with custom content
        self.height = 'calc(100vh - %dpx)'%(self._titleheight+self._footerheight)
        self.card = v.Card(children=[], elevation=5,class_="pa-0 ma-0", style_='width: 100vw; max-width: 100vw; height: %s; max-height: %s;'%(self.height,self.height))
        return self.card
    
    
    # Open the dialog
    def open(self):
        self.dlg = dialogGeneric.dialogGeneric(title='', titleheight='0px', text='', show=True, no_click_animation=True,
                                               addclosebuttons=False, persistent=self.persistent, transition=self._transition,
                                               fullscreen=True, content=[self.appbar,self.card,self.footer], output=self.output)
        
        
    # Close the dialog
    def close(self):
        try:
            if not self.dlg is None:
                self.dlg.close()
                if not self.onclose is None:
                    self.onclose()
        except:
            pass
        
        self.dlg = None
        
    
    # Quick open and close of the page (to be called when the titleheight or the footerheight is changed)
    def refresh(self):
        if self.dlg is not None:
            self.close()
            oldtransition = self.transition
            self.transition = 'dialog-top-transition'
            self.open()
            self.transition = oldtransition
        
        
    # Add a custom buttom to the page (before the call to create!)
    def customButtonAdd(self, iconname, tooltiptext, callback):
        self.custom_buttons.append((iconname,tooltiptext,callback))   # Each item has an icon name, a tooltip string and a callback function
    
    # Remove all custom buttons
    def customButtonClear(self):
        self.custom_buttons = []
        
        
    #####################################################################################################################################################
    # Properties
    #####################################################################################################################################################
    @property
    def appname(self):
        """
        Get/Set the name of the application (displayed on the left side of the title bar)
        
        Returns
        --------
        name : str
            Name of the application

        Example
        -------
        Programmatically change the name of the application::
            
            p.appname = 'New app name'
            print(p.appname)
        
        """
        return self._appname
        
    @appname.setter
    def appname(self, name):
        self._appname = str(name)
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def title(self):
        """
        Get/Set the title of the page (displayed on the left side of the title bar)
        
        Returns
        --------
        title : str
            Title of the page

        Example
        -------
        Programmatically change the title of the page::
            
            p.title = 'New title'
            print(p.title)
        
        """
        return self._title
        
    @title.setter
    def title(self, title):
        self._title = str(title)
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def titlecolor(self):
        """
        Get/Set the color of the title bar
        
        Returns
        --------
        color : str
            Color of the title bar

        Example
        -------
        Programmatically change the color::
            
            p.titlecolor = 'red'
            print(p.titlecolor)
        
        """
        return self._titlecolor
        
    @titlecolor.setter
    def titlecolor(self, color):
        self._titlecolor = color
        self.appbar.color = self._titlecolor
        
        
    @property
    def titledark(self):
        """
        Get/Set the text color of the title bar
        
        Returns
        --------
        flag : bool
            If True the text on the title bar will be displayed in white, otherwise in black color

        Example
        -------
        Programmatically change the text color::
            
            p.titledark = True
            print(p.titledark)
        
        """
        return self._titledark
        
    @titledark.setter
    def titledark(self, flag):
        self._titledark = flag
        for btn in self.buttons:
            btn.dark = self._titledark

        if not self.btn_back is None:
            self.btn_back.dark = self._titledark
        if not self.btn_help is None:
            self.btn_help.dark = self._titledark
        
        textcolor = 'black'
        if self._titledark:
            textcolor = 'white'
            
        if not self.toolbarTitle is None:
            self.toolbarTitle.style_ = 'height: 30px; color: %s; font-size: 26;'%textcolor
        
        if not self.toolbarSubtitle is None:
            self.toolbarSubtitle.style_ = 'height: 30px; color: %s; font-size: 26;'%textcolor
            
            
    @property
    def titleheight(self):
        """
        Get/Set the height of the title bar
        
        Returns
        --------
        height : int
            Height of the title bar in pixels

        Example
        -------
        Programmatically change the title bar height::
            
            p.titleheight = 80
            print(p.titleheight)
        
        """
        return self._titleheight
        
    @titleheight.setter
    def titleheight(self, height):
        self._titleheight = height
        if self._titleheight < 20:  self._titleheight = 20
        if self._titleheight > 200: self._titleheight = 200
        self.appbar.height = self.appbar.min_height = self.appbar.max_height = self._titleheight
        
        if not self.btn_credits is None:
            self.btn_credits.style_ = 'width: 170px;  height: %dpx;'%(self._titleheight-4)
            
        self.height = 'calc(100vh - %dpx)'%(self._titleheight+self._footerheight)
        self.card.style_ = 'width: 100vw; max-width: 100vw; height: %s; max-height: %s;'%(self.height,self.height)
            
            
    @property
    def titleimageurl(self):
        """
        Get/Set the image to display on the title bar
        
        Returns
        --------
        imageurl : str
            String containing the url of the title bar backbround image

        Example
        -------
        Programmatically change the title bar background image::
            
            p.titleimageurl = 'https://.....'
            print(p.titleimageurl)
        
        """
        return self._titleimageurl
        
    @titleimageurl.setter
    def titleimageurl(self, imageurl):
        self._titleimageurl = str(imageurl)

        if len(self._titleimageurl) > 0:
            self.appbar.src = self._titleimageurl
        else:
            self.appbar.src = None

            
    @property
    def footercolor(self):
        """
        Get/Set the color of the footer bar
        
        Returns
        --------
        color : str
            Color of the footer bar

        Example
        -------
        Programmatically change the color::
            
            p.footercolor = 'red'
            print(p.footercolor)
        
        """
        return self._footercolor
        
    @footercolor.setter
    def footercolor(self, color):
        self._footercolor = color
        self.ctext.color  = self._footercolor
        self.footer.color = self._footercolor
            
            
    @property
    def footerdark(self):
        """
        Get/Set the text color of the footer bar
        
        Returns
        --------
        flag : bool
            If True the text on the footer bar will be displayed in white, otherwise in black color

        Example
        -------
        Programmatically change the text color::
            
            p.footerdark = True
            print(p.footerdark)
        
        """
        return self._footerdark
        
    @footerdark.setter
    def footerdark(self, flag):
        self._footerdark = flag
        
        textcolor = 'black'
        if self._footerdark:
            textcolor = 'white'
            
        self.copyicon.color = textcolor
        self.ctext.style_   = 'color: %s;'%textcolor
            
            
    @property
    def footerheight(self):
        """
        Get/Set the height of the footer bar
        
        Returns
        --------
        height : int
            Height of the footer bar in pixels

        Example
        -------
        Programmatically change the footer bar height::
            
            p.footerheight = 20
            print(p.footerheight)
        
        """
        return self._footerheight
        
    @footerheight.setter
    def footerheight(self, height):
        self._footerheight = height
        if self._footerheight < 20:  self._footerheight = 16
        if self._footerheight > 200: self._footerheight = 200
        self.footer.height = self.footer.min_height = self.footer.max_height = self._footerheight
        self.footer.style_ = 'height: %dpx; overflow: hidden; border-bottom-left-radius: 0; border-bottom-right-radius: 0;'%self._footerheight
        
        self.height = 'calc(100vh - %dpx)'%(self._titleheight+self._footerheight)
        self.card.style_ = 'width: 100vw; max-width: 100vw; height: %s; max-height: %s;'%(self.height,self.height)

        
    @property
    def copyrighttext(self):
        """
        Get/Set the copyright text to display on the footer bar
        
        Returns
        --------
        text : str
            Text to display as copyright message on the footer bar

        Example
        -------
        Programmatically change the copyright text::
            
            p.copyrighttext = 'Founded by EU'
            print(p.copyrighttext)
        
        """
        return self._copyrighttext
        
    @copyrighttext.setter
    def copyrighttext(self, text):
        self._copyrighttext = text
        self.ctext.children = [self._copyrighttext]
        

    @property
    def show_back(self):
        """
        Show or hide the back button in the title bar
        
        Returns
        --------
        flag : bool
            If True a "back" button is displayed in the title bar

        Example
        -------
        Programmatically change the presence of the back button in the title bar::
            
            p.show_back = False
            print(p.show_back)
        
        """
        return self._show_back
        
    @show_back.setter
    def show_back(self, flag):
        self._show_back = flag
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def left_back(self):
        """
        Get/Set the flag that controls the position of the back button in the title bar
        
        Returns
        --------
        flag : bool
            If True the "back" button is displayed on the left side of the title bar

        Example
        -------
        Programmatically change the position of the back button in the title bar::
            
            p.left_back = False
            print(p.left_back)
        
        """
        return self._left_back
        
    @left_back.setter
    def left_back(self, flag):
        self._left_back = flag
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def show_help(self):
        """
        Show or hide the help button in the title bar
        
        Returns
        --------
        flag : bool
            If True a "help" button is displayed in the title bar

        Example
        -------
        Programmatically change the presence of the help button in the title bar::
            
            p.show_help = False
            print(p.show_help)
        
        """
        return self._show_help
        
    @show_help.setter
    def show_help(self, flag):
        self._show_help = flag
        self.appbar.children = self._create_appbar_children()

        
    @property
    def show_credits(self):
        """
        Show or hide the credits image in the title bar
        
        Returns
        --------
        flag : bool
            If True a "credits" button with an image is displayed in the title bar

        Example
        -------
        Programmatically change the presence of the credits button in the title bar::
            
            p.show_credits = False
            print(p.show_credits)
        
        """
        return self._show_credits
        
    @show_credits.setter
    def show_credits(self, flag):
        self._show_credits = flag
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def logoappurl(self):
        """
        Get/Set the image to display as the application logo on the left side of the title bar
        
        Returns
        --------
        imageurl : str
            String containing the url of application logo image

        Example
        -------
        Programmatically change the application logo in the title bar::
            
            p.logoappurl = 'data:image/png;base64,...'
            print(p.logoappurl)
        
        """
        return self._logoappurl
        
    @logoappurl.setter
    def logoappurl(self, imageurl):
        self._logoappurl = str(imageurl)
        
        if len(self._logoappurl) > 0:
            self.logoapp = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._logowidth, src=self._logoappurl)
        else:
            self.logoapp = None
        
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def logocreditsurl(self):
        """
        Get/Set the image to display as the application credits on the right side of the title bar
        
        Returns
        --------
        imageurl : str
            String containing the url of application credits image

        Example
        -------
        Programmatically change the application credits in the title bar::
            
            p.logocreditsurl = 'data:image/png;base64,...'
            print(p.logocreditsurl)
        
        """
        return self._logocreditsurl
        
    @logocreditsurl.setter
    def logocreditsurl(self, imageurl):
        self._logocreditsurl = str(imageurl)
        
        if len(self._logocreditsurl) == 0:
            self._logocreditsurl = 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/EC-JRC-logo_horizontal_EN_neg_transparent-background.png'

        self.logoCredits = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._creditswidth, src=self._logocreditsurl)
        self.appbar.children = self._create_appbar_children()
        
               
    @property
    def logowidth(self):
        """
        Get/Set the width of the application logo button in the title bar
        
        Returns
        --------
        width : int
            Width of the application logo button in pixels

        Example
        -------
        Programmatically change the application logo button width::
            
            p.logowidth = 20
            print(p.logowidth)
        
        """
        return self._logowidth
        
    @logowidth.setter
    def logowidth(self, width):
        self._logowidth = width

        if len(self._logoappurl) > 0:
            self.logoapp = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._logowidth, src=self._logoappurl)
        else:
            self.logoapp = None
        
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def creditswidth(self):
        """
        Get/Set the width of the application credits button in the title bar
        
        Returns
        --------
        width : int
            Width of the application credits button in pixels

        Example
        -------
        Programmatically change the application credits button width::
            
            p.creditswidth = 20
            print(p.creditswidth)
        
        """
        return self._creditswidth
        
    @creditswidth.setter
    def creditswidth(self, width):
        self._creditswidth = width
        self.logoCredits = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._creditswidth, src=self._logocreditsurl)
        self.appbar.children = self._create_appbar_children()
        
        
    @property
    def transition(self):
        """
        Get/Set the transition mode to use for the opening of the page. Possible values are: 'dialog-bottom-transition', 'dialog-top-transition' or 'dialog-transition'
        
        Returns
        --------
        mode : str
            Transition mode, one of 'dialog-bottom-transition', 'dialog-top-transition' or 'dialog-transition'

        Example
        -------
        Programmatically change the transition mode::
            
            p.transition = 'dialog-transition'
            print(p.transition)
        
        """
        return self._transition
        
    @transition.setter
    def transition(self, mode):
        self._transition = mode
        
        
    @property
    def state(self):
        """
        Get/Set the multiple properties of the page
        
        Returns
        --------
        statusdict : dict
            Dictionary containing one or more properties

        Example
        -------
        Programmatically set some of the properties of a page::
            
            p.state = {'transition': 'dialog-top-transition', 'title': 'new title'}
            print(p.state)
        
        """
        return {x: getattr(self, x) for x in ['appname',
                                              'title',
                                              'titlecolor',
                                              'titledark',
                                              'titleheight',
                                              'titleimageurl',
                                              'footercolor',
                                              'footerdark',
                                              'footerheight',
                                              'copyrighttext',
                                              'show_back',
                                              'left_back',
                                              'show_help',
                                              'show_credits',
                                              'logoappurl',
                                              'logocreditsurl',
                                              'logowidth',
                                              'creditswidth',
                                              'transition'
                                             ]}
        
    @state.setter
    def state(self, statusdict):
        for key, value in statusdict.items():
            if key != 'content':
                setattr(self, key, value)
            
        doRefresh = False
        if 'titleheight' in statusdict:
            if statusdict['titleheight'] != self.titleheight:
                doRefresh = True
            
        if 'footerheight' in statusdict:
            if statusdict['footerheight'] != self.footerheight:
                doRefresh = True
        
        if doRefresh:
            self.refresh()
        
        
    #####################################################################################################################################################
    # Initialization
    #####################################################################################################################################################
    def __init__(self,
                 appname,
                 title,
                 output,
                 onclose=None,
                 titlecolor=settings.color_first,
                 titledark=True,
                 titleheight=54,
                 titleimageurl='',
                 footercolor=settings.color_second,
                 footerdark=False,
                 footerheight=30,
                 logoappurl='',
                 logowidth=40,
                 on_logoapp=None,
                 copyrighttext='',
                 show_back=True,
                 left_back=False,
                 show_help=True,
                 on_help=None,
                 logocreditsurl='',
                 creditswidth=120,
                 show_credits=True,
                 on_credits=None,
                 transition='dialog-bottom-transition',
                 persistent=False):

        self.dlg = None
        
        self._appname = appname
        self._title   = title
        self.output   = output
        self.onclose  = onclose
        
        self._titlecolor    = titlecolor
        self._titledark     = titledark
        self._titleheight   = titleheight
        self._titleimageurl = titleimageurl
        
        self._footercolor  = footercolor
        self._footerdark   = footerdark
        self._footerheight = footerheight
        
        self._copyrighttext = copyrighttext
        self._show_back     = show_back
        self._left_back     = left_back
        self._show_help     = show_help
        self.on_help        = on_help
        self._show_credits  = show_credits
        self.on_credits     = on_credits
        self.on_logoapp     = on_logoapp
        
        self._transition    = transition
        self.persistent     = persistent
        
        self.custom_buttons = []   # Each item has an icon name, a tooltip string and a callback function
        
        self._logowidth      = logowidth
        self._creditswidth   = creditswidth
        
        self._logoappurl     = logoappurl
        self._logocreditsurl = logocreditsurl
        
        if len(self._logoappurl) > 0:
            self.logoapp = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._logowidth, src=self._logoappurl)
        else:
            self.logoapp = None
        
        if len(self._logocreditsurl) == 0:
            self._logocreditsurl = 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/EC-JRC-logo_horizontal_EN_neg_transparent-background.png'
        self.logoCredits = v.Img(class_='pa-0 ma-0 mr-2', max_width=self._creditswidth, src=self._logocreditsurl)
