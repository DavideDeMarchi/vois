"""Initial page for an application"""
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
from vois.vuetify import dialogGeneric, tooltip
from ipywidgets import widgets, Layout, HTML
from IPython.display import display
import ipyvuetify as v

import base64
from io import BytesIO
import os


######################################################################################################################################################
# Check if running in Voila: check environ variable SERVER_SOFTWARE
######################################################################################################################################################
def RunningInVoila():
    return os.environ.get('SERVER_SOFTWARE','jupyter').startswith('voila')
    #return not os.path.isdir("/eos/jeodpp/data/SRS/")

    
######################################################################################################################################################
# Given a local filepath of a PNG or JPEG image, returns the interned URL to use in a v.Img ipyvuetify widget
######################################################################################################################################################
def getLocalImageURL(filepath, imagetype='jpg'):
    with open(filepath, "rb") as f:
        buffered = BytesIO(f.read())
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return 'data:image/%s;base64,'%imagetype + img_str

    
######################################################################################################################################################
# Card that displays a clickable button
######################################################################################################################################################
class buttonCard(v.Html):

    def __init__(self,
                 width='400px',
                 height='160px',
                 margins='pa-0 ma-0 pl-3',
                 color='white',
                 dark=False,
                 ripple=False,
                 disabled=False,
                 elevation=3,
                 title='Title',
                 subtitle='Subtitle',
                 image='',
                 imagesize='160px',
                 on_click=None,
                 argument=None,
                 tooltiptext='',
                 textcolor='black',
                 titleweight=500,
                 subtitleweight=400,
                 titlesize='2vh',
                 subtitlesize='1.2vh',
                 button_radius='0px',
                 **kwargs):

        super().__init__(**kwargs)
        
        self.width     = width
        self.height    = height
        self.margins   = margins
        self.color     = color
        self.dark      = dark
        self.ripple    = ripple
        self.disabled  = disabled
        self.elevation = elevation
        self.title     = title
        self.subtitle  = subtitle
                 
        self.textcolor      = textcolor
        self.titleweight    = titleweight
        self.subtitleweight = subtitleweight
        self.titlesize      = titlesize
        self.subtitlesize   = subtitlesize
        self.button_radius  = button_radius
 
        self.image = image
        if len(image) == 0: self.imagesize = '0px'
        else:               self.imagesize = imagesize
        
        self.on_click = on_click
        self.argument = argument
        
        self.tooltiptext = tooltiptext
        
        
        self.card = v.Card(width=self.width, height=self.height, color=self.color, dark=self.dark, style_='border-radius: %s;'%self.button_radius,
                           ripple=self.ripple, disabled=self.disabled, elevation=self.elevation, class_=margins)
           
        t = v.CardTitle(children=[self.title], style_='color: %s; font-weight: %d; font-size: %s; padding: 0px; padding-left: 10px; padding-top: 10px;'%(self.textcolor,self.titleweight,self.titlesize))
        
        if len(self.subtitle) > 0:
            s = v.CardSubtitle(children=[self.subtitle], style_='color: %s; font-weight: %d; font-size: %s; padding: 0px; padding-left: 10px;'%(self.textcolor,self.subtitleweight,self.subtitlesize))
        else:
            s = v.Html(tag='div', children=[''])
        
        # Set the tooltip to title and subtitle
        t = tooltip.tooltip(self.tooltiptext,t)
        s = tooltip.tooltip(self.tooltiptext,s)
        
        if len(self.image) > 0:
            img = v.Img(src=self.image, contain=True, width=self.imagesize, min_width=self.imagesize, max_width=self.imagesize, height=self.height, max_height=self.height)
            img = tooltip.tooltip(self.tooltiptext,img)
            h = v.Html(tag='div', children=[t,s], style_='max-width: calc(%s - %s);'%(self.width,self.imagesize))
            self.card.children = [v.Row(justify='space-between', children=[h,img], style_='width: %s; max-width: %s;'%(self.width,self.width))]
        else:
            self.card.children = [t,s]
        
        if self.on_click is not None:
            self.card.on_event('click', self.__internal_onclick)
            
        self.tag = 'div'
        self.children = [self.card]
        
        
    # Click on the card
    def __internal_onclick(self, *args):
        if self.argument is None:
            self.on_click()
        else:
            self.on_click(self.argument)        



#####################################################################################################################################################
# Main page o the application
#####################################################################################################################################################
class mainPage():
    """
    Initial page of an application. The page contains a box for the title/subtitle/logo of the application, a box containing one or more buttons, each of them calling a callback function, and a box containing credits information. All these boxes are horizontally centered inside the page, while their vertical position can be customized (by default the title is on top, the buttons in central position and the credit box is at the bottom of the page).
        
    Parameters
    ----------
    title : str, optional
        Title of the page (default is 'Application main title')
    subtitle : str, optional
        Subtitle of the page (default is 'Subtitle to be displayed below the main title')
    applogo_url : str, optional
        Url of the application logo (default is a sample logo)
    applogo_widthpercent : float, optional
        Width of the area where the application logo is displayed in percentage of the screen (default is 20.0)
    titlesizepercent: int, optional
        Font size used for the main page title, in percentage compared to the standard dimension (default is 100, change to e.g. 80 for a smaller font, 120 for a bigger one)
    subtitlesizepercent: int, optional
        Font size used for the main page subtitle, in percentage compared to the standard dimension (default is 100, change to e.g. 80 for a smaller font, 120 for a bigger one)
    credits : str, optional
        Credits string to display inside the credit box on the bottom of the page (default is 'Unit T.4, Data Visualisation Team')
    creditslogo_url : str, optional
        Url of the image to display inside the credit box on the bottom of the page (default is 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/TransparentJRC.png')
    text_color : str, optional
        Color to use for text (title, subtitle, credits, buttons text, etc.). Default is '#0e446e'.
    background_image : str or int, optional
        Image to use as fullscreen background. If an integer in the range [0,59] is passed, one of the sixty predefined wallpapers is used, otherwise any image URL can be used (default is 22)
    background_filter : str, optional
        CSS image filter to apply to the background image (default is ''). See https://developer.mozilla.org/en-US/docs/Web/CSS/filter for a list of available filters.
    vois_show : bool, optional
        Is True, a credit to the vois library is displayed in the top-right side of the page (default is True)
    vois_opacity : float, optional
        Opacity to apply to the vois logo, in case vois_show is set to True (default is 0.1)
    titlebox_widthpercent : float, optional
        Width of the top box containing the title, in percentage of the screen width. Default is 40.0.
    titlebox_heightpercent : float, optional
        Height of the box containing the title, in percentage of the screen height. Default is 24.0.
    titlebox_toppercent : float, optional
        Top position of the box containing the title, in percentage of the screen height, measured from the top of the page. Default is 12.0.
    titlebox_opacity : float, optional
        Opacity to apply to the box containing the title (default is 0.4)
    titlebox_border : int, optional
        Border width in pixels of the box containing the title (default is 2)
    buttonbox_widthpercent : float, optional
        Width of the box containing the buttons, in percentage of the screen width. Default is 80.0.
    buttonbox_heightpercent : float, optional
        Height of the box containing the buttons, in percentage of the screen height. Default is 50.0.
    buttonbox_toppercent : float, optional
        Top position of the box containing the buttons, in percentage of the screen height, measured from the top of the page. Default is 43.0.
    creditbox_widthpercent : float, optional
        Width of the box containing the credits, in percentage of the screen width. Default is 80.0.
    creditbox_heightpercent : float, optional
        Height of the box containing the credits, in percentage of the screen height. Default is 25.0.
    creditbox_toppercent : float, optional
        Top position of the box containing the credits, in percentage of the screen height, measured from the top of the page. Default is 74.0.
    creditbox_opacity : float, optional
        Opacity to apply to the box containing the credits (default is 0.0)
    button_widthpercent : float, optional
        Width of each of the buttons, in percentage of the screen width. Default is 22.0.
    button_heightpercent : float, optional
        Height of each of the buttons, in percentage of the screen height. Default is 10.0.
    button_elevation : int, optional
        Elevation in pixels to apply to the buttons (default is 6)
    button_opacity: float, optional
        Opacity to apply to the buttons (default is 0.5)
    button_titlesize: str, optional
        Font size to use for the buttons title (default is '2.0vh')
    button_subtitlesize: str, optional
        Font size to use for the buttons subtitle (default is '1.2vh')
    button_radius: str, optional
        Border radius for the buttons area (default is '0px' which means completely squared buttons)
    disclaimer: str, optional
        Text to display at the bottom of the creditbox (default is the empty string)

    Examples
    --------
    Creation of a main page with 6 buttons displaying random images from https://picsum.photos/::
        
        from vois.vuetify import mainPage
        from random import randrange
        
        def onclick1():
            print("Clicked Function 1")

        m = mainPage.mainPage(title='mainPage demo',
                              subtitle='Showcase how easy is to create a front page for an app',
                              credits="vois library development team",
                              titlebox_widthpercent=50, titlebox_opacity=0.2, titlebox_border=0,
                              vois_show=True, vois_opacity=0.1,
                              button_widthpercent=23, button_heightpercent=14, button_elevation=16, button_opacity=0.6,
                              background_image=55,
                              background_filter='blur(2px) brightness(1.2) contrast(0.7) sepia(0.05) saturate(1.2)',
                              creditbox_opacity=0,
                              text_color='#222222')

        m.addButton('Function 1',
                    subtitle='Launch calculation of ...',
                    tooltip='Tooltip text to display on hover',
                    image='https://picsum.photos/seed/%d/200/200'%randrange(1000),
                    onclick=onclick1)

        for i in range(2,7): m.addButton('Function %d'%i, image='https://picsum.photos/seed/%d/200/200'%randrange(1000))

        m.open()


    .. figure:: figures/mainPage.png
       :scale: 100 %
       :alt: mainPage widget

       Example of a mainPage
       

    """

    # Initialization
    def __init__(self,
                 title='Application main title',
                 subtitle='Subtitle to be shown below the main title',
                 titlesizepercent=100,
                 subtitlesizepercent=100,
                 applogo_url='https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/sampleapplogo.png',
                 applogo_widthpercent=20.0,
                 credits='Unit T.4, Data Visualisation Team',
                 creditslogo_url='https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/TransparentJRC.png',
                 text_color='#0e446e',
                 background_image=22,
                 background_filter='',
                 vois_show=True,
                 vois_opacity=0.1,
                 titlebox_widthpercent=40.0,
                 titlebox_heightpercent=24.0,
                 titlebox_toppercent=12.0,
                 titlebox_opacity=0.4,
                 titlebox_border=2,
                 titleshadow=True,
                 titleshadow_color='#ffffff',
                 buttonbox_widthpercent=80.0,
                 buttonbox_heightpercent=50.0,
                 buttonbox_toppercent=43.0,
                 creditbox_widthpercent=80.0,
                 creditbox_heightpercent=25.0,
                 creditbox_toppercent=74.0,
                 creditbox_opacity=0.,
                 button_widthpercent=22.0,
                 button_heightpercent=10.0,
                 button_elevation=6,
                 button_opacity=0.5,
                 button_titlesize='2.0vh',
                 button_subtitlesize='1.2vh',
                 button_radius='0px',
                 disclaimer='The contents of this viewer are intended solely for the use of the Commission and may not be reproduced, distributed, or communicated outside the Commission in any format without explicit prior written consent'):

        self.output = widgets.Output(layout=Layout(width='0px', height='0px'))
        
        self.title                   = title
        self.subtitle                = subtitle
        self.titlesizepercent        = titlesizepercent
        self.subtitlesizepercent     = subtitlesizepercent
        self.applogo_url             = applogo_url
        self.applogo_widthpercent    = applogo_widthpercent
        self.credits                 = credits
        self.creditslogo_url         = creditslogo_url
        self.text_color              = text_color
        self.background_image        = background_image
        self.background_filter       = background_filter
        self.vois_show               = vois_show
        self.vois_opacity            = vois_opacity

        self.titlebox_widthpercent   = titlebox_widthpercent
        self.titlebox_heightpercent  = titlebox_heightpercent
        self.titlebox_toppercent     = titlebox_toppercent
        self.titlebox_opacity        = titlebox_opacity
        self.titlebox_border         = titlebox_border
                         
        self.titleshadow             = titleshadow
        self.titleshadow_color       = titleshadow_color

        self.buttonbox_widthpercent  = buttonbox_widthpercent
        self.buttonbox_heightpercent = buttonbox_heightpercent
        self.buttonbox_toppercent    = buttonbox_toppercent
        
        self.creditbox_widthpercent  = creditbox_widthpercent
        self.creditbox_heightpercent = creditbox_heightpercent
        self.creditbox_toppercent    = creditbox_toppercent
        self.creditbox_opacity       = creditbox_opacity
        
        self.button_widthpercent     = button_widthpercent
        self.button_heightpercent    = button_heightpercent
        self.button_elevation        = button_elevation
        self.button_opacity          = button_opacity
        self.button_titlesize        = button_titlesize
        self.button_subtitlesize     = button_subtitlesize
        self.button_radius           = button_radius
        
        self.disclaimer              = disclaimer
        
        self.buttons = []

        self.spacer = v.Html(tag='div',children=[' '], style_='width: 16px; height: 20px;')
        

    # Add a button
    def addButton(self, title, subtitle='', tooltip='', image='', onclick=None, argument=None):
        """
        Add a button to the page
        
        Parameters
        ----------
        title : str
            Title of the button
        subtitle : str, optional
            Subtitle of the button (default is '')
        tooltip : str, optional
            Tooltip to show when hovering the button title (default is '')
        image : str, optional
            Image to show on the right side of the button (default is '')
        onclick : function, optional
            Python function to call when the user clicks on the button. The function will receive the argument value as parameter if it is not None, otherwise it will be calle with no parameters. Default is None
        argument : any, optional
            Argument to pass to the onclick python function (default is None)
            
        """
        self.buttons.append({'title':    title,
                             'subtitle': subtitle,
                             'tooltip':  tooltip,
                             'image':    image,
                             'onclick':  onclick,
                             'argument': argument})
        
        
    # Display the page as a fullscreen dialog-box
    def open(self):
        """Open the page"""
        
        # Dimension of the main title rectangle
        width = '%fvw'%self.titlebox_widthpercent
        height = '%fvh'%self.titlebox_heightpercent

        ######################################################################################################################################################
        # Main titles
        ######################################################################################################################################################
        if self.titleshadow:
            tts = 'text-shadow: -0.06vh -0.06vh 0 %s, 0.06vh -0.06vh 0 %s, -0.06vh 0.06vh 0 %s, 0.06vh 0.06vh 0 %s;'%(self.titleshadow_color,self.titleshadow_color,self.titleshadow_color,self.titleshadow_color)
        else:
            tts = ''
            
        html_main = '''
        <head>
            <meta charset="utf-8" />
            <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
            <style>
                .big {
                    font-family: 'PT Sans', sans-serif;
                    font-size: calc(%f * min(5.0vh, 3.7vw));
                    font-weight: 700;
                    %s
                    text-align: center;
                    line-height: 2.0;
                    color: %s !important; 
                }
                .normal {
                    font-family: 'PT Sans', sans-serif;
                    font-size: calc(%f *min(2.65vh, 2.0vw));
                    font-weight: 700;
                    text-align: center;
                    line-height: 1.0;
                    color: %s !important;
                }
                .responsive4 {
                    width: %fvh;
                    vertical-align: middle;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <div class="big">
                %s
            </div>

            <div class="normal">
                %s
            </div>

            <div class="normal">
                <br/>
                <img src="%s" alt="" class="responsive4">
            </div>
        </body>
        ''' % (self.titlesizepercent*0.01, tts, self.text_color, self.subtitlesizepercent*0.01, self.text_color, self.applogo_widthpercent, self.title, self.subtitle, self.applogo_url)

        cardmain = v.Card(flat=True, children=[HTML(html_main)], style_="background-color: #ffffff00;")

        bcol = '#ffffff%0.2X'%(int(self.titlebox_opacity*255))
        self.hmain = v.Html(tag='div', children=[cardmain], class_="pa-0 ma-0",
                            style_='width: %s; height: %s; border: %dpx solid %s; border-radius: 12px; position: absolute; top: %fvh; left: %fvw; background-color: %s; overflow: hidden;'%(width,height, self.titlebox_border, self.text_color,
                                                                                                                                                                                           self.titlebox_toppercent, (100.0-self.titlebox_widthpercent)/2.0,
                                                                                                                                                                                           bcol))


        ######################################################################################################################################################
        # Credit to vois
        ######################################################################################################################################################
        if self.vois_show:
            html_vois = '''
            <head>
                <meta charset="utf-8" />
                <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
                <style>
                    .normal2 {
                        font-family: 'PT Sans', sans-serif;
                        font-size: min(2.20vh, 1.5vw);
                        font-weight: 700;
                        text-align: center;
                        line-height: 1.0;
                        color: %s;
                    }
                    .responsive2 {
                        width: 10vw;
                        vertical-align: middle;
                        height: auto;
                        background-color: #ffffff%0.2X;
                        padding: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="normal2">
                    <br/>
                    <span style="">created using the: </span>
                    <img src="https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/vois_horizontal_big.png" alt="" class="responsive2">
                </div>
            </body>
            ''' % (self.text_color, int(self.vois_opacity*255))

            cardvois = v.Card(flat=True, children=[HTML(html_vois)], style_="background-color: #ffffff00;")

            self.hvois = v.Html(tag='div', children=[cardvois], class_="pa-0 ma-0",
                                style_='width: 34vw; height: 11vh; border: 0px solid #000000; border-radius: 12px; position: absolute; top: 1vh; left: 65vw; background-color: #ffffff00; overflow: hidden;')
        else:
            self.hvois = ''



        ######################################################################################################################################################
        # Logo and credits
        ######################################################################################################################################################
        html_credits = '''
        <head>
            <meta charset="utf-8" />
            <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
            <style>
                .normal3 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(2.0vh, 1.4vw);
                    font-weight: 700;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
                    overflow: hidden;
                }
                .normal4 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(1.3vh, 0.9vw);
                    font-weight: 400;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
                    overflow: hidden;
                }
                .responsive3 {
                    width: 14vw;
                    vertical-align: middle;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <div class="normal3">
                <img src="%s" alt="" class="responsive3">
            </div>
            <div class="normal3">
                <br/>
                %s
            </div>
            <div class="normal4">
                <br/>
                %s
            </div>
        </body>
        '''%(self.text_color, self.text_color, self.creditslogo_url, self.credits, self.disclaimer)

        cardunit = v.Card(flat=True, children=[HTML(html_credits)], style_="background-color: #ffffff00;", class_="pa-0 ma-0 mt-2")
        bcol = '#ffffff%0.2X'%(int(self.creditbox_opacity*255))
        self.hunit = v.Html(tag='div', children=[cardunit], class_="pa-0 ma-0",
                            style_='width: %fvw; height: %fvh; border: 0px solid #000000; border-radius: 12px; position: absolute; top: %fvh; left: %fvw; background-color: %s; overflow: hidden;'%(self.creditbox_widthpercent, self.creditbox_heightpercent,
                            self.creditbox_toppercent, (100.0-self.creditbox_widthpercent)/2.0, bcol))
        
        nbuttons_per_row = self.buttonbox_widthpercent // self.button_widthpercent
        
        rows = []
        
        children = []
        i = 0
        for b in self.buttons:
            c = buttonCard(elevation=self.button_elevation, width='%fvw'%self.button_widthpercent, 
                           height="%fvh"%self.button_heightpercent, imagesize="%fvh"%self.button_heightpercent,
                           title=b['title'], subtitle=b['subtitle'], tooltiptext=b['tooltip'],
                           color='#ffffff%0.2X'%int(self.button_opacity*255), subtitleweight=400,
                           image=b['image'], on_click=b['onclick'], argument=b['argument'], button_radius=self.button_radius,
                           textcolor=self.text_color, titlesize=self.button_titlesize, subtitlesize=self.button_subtitlesize)
            
            if len(children) > 0:
                children.append(self.spacer)
                children.append(self.spacer)
            children.append(c)
            
            i += 1
            if i >= nbuttons_per_row:
                r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2 mb-6")
                rows.append(r)
                i = 0
                children = []
                
        if len(children) > 0:
            r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2")
            rows.append(r)
            
        hpages = v.Html(tag='div', children=rows, class_="pa-0 ma-0",
                        style_='width: %fvw; height: %fvh; position: absolute; top: %fvh; left: %fvw; background-color: #ffffff00; overflow: hidden;'%(self.buttonbox_widthpercent, self.buttonbox_heightpercent,
                                                                                                                                                       self.buttonbox_toppercent, (100.0-self.buttonbox_widthpercent)/2.0))

        ######################################################################################################################################################
        # Background image
        ######################################################################################################################################################
        if isinstance(self.background_image, int):
            url = 'https://jeodpp.jrc.ec.europa.eu/services/shared/wallpapers/%d.jpg'%self.background_image
        else:
            url = self.background_image

        # See: https://css-tricks.com/perfect-full-page-background-image/
        self.back = v.Html(tag='div', children=[], class_="pa-0 ma-0",
                           style_='''
        width: 100vw; height: 100vh; 
        background-image: url('%s'); no-repeat center center fixed;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
        filter: %s;
        '''%(url,self.background_filter))

        display(self.output)
        
        self.dlg = dialogGeneric.dialogGeneric(title='', titleheight='0px', text='', show=True, addclosebuttons=False, 
                                               persistent=RunningInVoila(), no_click_animation=True,    # In JEO-lab the page closes with the "ESC" key!!!
                                               fullscreen=True, content=[self.back, self.hmain, self.hvois, hpages, self.hunit], output=self.output)
        
        

        
    
    # Close the dialog
    def close(self):
        """Close the page"""
        self.page = None
        if not self.dlg is None:
            self.dlg.close()

            
            
    ######################################################################################################################################################
    # Open the main page in preview mode (70% of the fullscreen dimensions!): returns a v.Card widget
    ######################################################################################################################################################
    def preview(self):
        """Open the page in preview mode"""
        
        # Dimension of the main title rectangle
        width = '%f%%'%self.titlebox_widthpercent
        height = '%f%%'%self.titlebox_heightpercent

        if self.titleshadow:
            tts = 'text-shadow: -0.042vh -0.042vh 0 %s, 0.042vh -0.042vh 0 %s, -0.042vh 0.042vh 0 %s, 0.042vh 0.042vh 0 %s;'%(self.titleshadow_color,self.titleshadow_color,self.titleshadow_color,self.titleshadow_color)
        else:
            tts = ''
            
        html_main = '''
        <head>
            <meta charset="utf-8" />
            <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
            <style>
                .big7 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: calc(%f * min(3.5vh, 2.59vw));
                    font-weight: 700;
                    %s
                    text-align: center;
                    line-height: 2.0;
                    color: %s;
                }
                .normal7 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: calc(%f * min(1.855vh, 1.4vw));
                    font-weight: 700;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
                }
                .responsive7 {
                    width: %fvh;
                    vertical-align: middle;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <div class="big7">
                %s
            </div>

            <div class="normal7">
                %s
            </div>

            <div class="normal7">
                <br/>
                <img src="%s" alt="" class="responsive7">
            </div>
        </body>
        ''' % (self.titlesizepercent*0.01, tts, self.text_color, self.subtitlesizepercent*0.01, self.text_color, self.applogo_widthpercent, self.title, self.subtitle, self.applogo_url)

        cardmain = v.Card(flat=True, children=[HTML(html_main)], style_="background-color: #ffffff00;")

        bcol = '#ffffff%0.2X'%(int(self.titlebox_opacity*255))
        hmain = v.Html(tag='div', children=[cardmain], class_="pa-0 ma-0",
                       style_='width: %s; height: %s; border: %dpx solid %s; border-radius: 12px; position: absolute; top: %f%%; left: %f%%; background-color: %s; overflow: hidden;'%(width,height, self.titlebox_border, self.text_color,
                                                                                                                                                                                       self.titlebox_toppercent, (100.0-self.titlebox_widthpercent)/2.0,
                                                                                                                                                                                       bcol))
        
        
        ######################################################################################################################################################
        # Credit to vois
        ######################################################################################################################################################
        if self.vois_show:
            html_vois = '''
            <head>
                <meta charset="utf-8" />
                <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
                <style>
                    .normal27 {
                        font-family: 'PT Sans', sans-serif;
                        font-size: min(1.54vh, 1.05vw);
                        font-weight: 700;
                        text-align: center;
                        line-height: 1.0;
                        color: %s;
                    }
                    .responsive27 {
                        width: 7vw;
                        vertical-align: middle;
                        height: auto;
                        background-color: #ffffff%0.2X;
                        padding: 7px;
                    }
                </style>
            </head>
            <body>
                <div class="normal27">
                    <br/>
                    <span style="">created using the: </span>
                    <img src="https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/vois_horizontal_big.png" alt="" class="responsive27">
                </div>
            </body>
            ''' % (self.text_color, int(self.vois_opacity*255))

            cardvois = v.Card(flat=True, children=[HTML(html_vois)], style_="background-color: #ffffff00;")

            hvois = v.Html(tag='div', children=[cardvois], class_="pa-0 ma-0",
                                style_='width: 34%; height: 11%; border: 0px solid #000000; border-radius: 12px; position: absolute; top: 1%; left: 65%; background-color: #ffffff00; overflow: hidden;')
        else:
            hvois = ''



        ######################################################################################################################################################
        # Logo and credits
        ######################################################################################################################################################
        html_credits = '''
        <head>
            <meta charset="utf-8" />
            <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
            <style>
                .normal37 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(1.4vh, 0.98vw);
                    font-weight: 700;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
                    overflow: hidden;
                }
                .normal47 {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(0.91vh, 0.63vw);
                    font-weight: 400;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
                    overflow: hidden;
                }
                .responsive37 {
                    width: 9.8vw;
                    vertical-align: middle;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <div class="normal37">
                <img src="%s" alt="" class="responsive37">
            </div>
            <div class="normal37">
                <br/>
                %s
            </div>
            <div class="normal47">
                <br/>
                %s
            </div>
        </body>
        '''%(self.text_color, self.text_color, self.creditslogo_url, self.credits, self.disclaimer)

        cardunit = v.Card(flat=True, children=[HTML(html_credits)], style_="background-color: #ffffff00;", class_="pa-0 ma-0 mt-2")
        bcol = '#ffffff%0.2X'%(int(self.creditbox_opacity*255))
        hunit = v.Html(tag='div', children=[cardunit], class_="pa-0 ma-0",
                       style_='width: %f%%; height: %f%%; border: 0px solid #000000; border-radius: 12px; position: absolute; top: %f%%; left: %f%%; background-color: %s; overflow: hidden;'%(self.creditbox_widthpercent, self.creditbox_heightpercent,
                       self.creditbox_toppercent, (100.0-self.creditbox_widthpercent)/2.0, bcol))
        
        
        nbuttons_per_row = self.buttonbox_widthpercent // self.button_widthpercent
        
        rows = []
        
        children = []
        i = 0
        for b in self.buttons:
            c = buttonCard(elevation=self.button_elevation, width='%fvw'%(0.7*self.button_widthpercent), 
                           height="%fvh"%(0.7*self.button_heightpercent), imagesize="%fvh"%(0.7*self.button_heightpercent),
                           title=b['title'], subtitle=b['subtitle'], tooltiptext=b['tooltip'],
                           color='#ffffff%0.2X'%int(self.button_opacity*255), subtitleweight=400,
                           image=b['image'], on_click=b['onclick'], argument=b['argument'], button_radius=self.button_radius,
                           textcolor=self.text_color, titlesize='calc(0.7 * %s)'%self.button_titlesize, subtitlesize='calc(0.7 * %s)'%self.button_subtitlesize)
            
            if len(children) > 0:
                children.append(self.spacer)
                children.append(self.spacer)
            children.append(c)
            
            i += 1
            if i >= nbuttons_per_row:
                r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2 mb-6")
                rows.append(r)
                i = 0
                children = []
                
        if len(children) > 0:
            r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2")
            rows.append(r)
            
        hpages = v.Html(tag='div', children=rows, class_="pa-0 ma-0",
                        style_='width: %f%%; height: %f%%; position: absolute; top: %f%%; left: %f%%; background-color: #ffffff00; overflow: hidden;'%(self.buttonbox_widthpercent, self.buttonbox_heightpercent,
                                                                                                                                                       self.buttonbox_toppercent, (100.0-self.buttonbox_widthpercent)/2.0))
        
        # Background image
        if isinstance(self.background_image, int):
            url = 'https://jeodpp.jrc.ec.europa.eu/services/shared/wallpapers/%d.jpg'%self.background_image
        else:
            url = self.background_image

        # See: https://css-tricks.com/perfect-full-page-background-image/
        back = v.Html(tag='div', children=[], class_="pa-0 ma-0",style_='''
        width: 70vw; height: 70vh; 
        background-image: url('%s'); no-repeat center center fixed;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
        filter: %s;
        '''%(url,self.background_filter))

        return v.Card(children=[back, hmain, hvois, hpages, hunit], width='70vw', style_='border-radius: 0px;')
    
    
        
    ######################################################################################################################################################
    # Save the configuration into a JSON file
    ######################################################################################################################################################
    def toJson(self):

        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'titlesizepercent': self.titlesizepercent,
            'subtitlesizepercent': self.subtitlesizepercent,
            'applogo_widthpercent': self.applogo_widthpercent,
            'credits': self.credits,
            'text_color': self.text_color,
            'background_image': self.background_image,
            'background_filter': self.background_filter,
            'vois_show': self.vois_show,
            'vois_opacity': self.vois_opacity,

            'titlebox_widthpercent': self.titlebox_widthpercent,
            'titlebox_heightpercent': self.titlebox_heightpercent,
            'titlebox_toppercent': self.titlebox_toppercent,
            'titlebox_opacity': self.titlebox_opacity,
            'titlebox_border': self.titlebox_border,

            'titleshadow': self.titleshadow,
            'titleshadow_color': self.titleshadow_color,

            'buttonbox_widthpercent': self.buttonbox_widthpercent,
            'buttonbox_heightpercent': self.buttonbox_heightpercent,
            'buttonbox_toppercent': self.buttonbox_toppercent,

            'creditbox_widthpercent': self.creditbox_widthpercent,
            'creditbox_heightpercent': self.creditbox_heightpercent,
            'creditbox_toppercent': self.creditbox_toppercent,
            'creditbox_opacity': self.creditbox_opacity,

            'button_widthpercent': self.button_widthpercent,
            'button_heightpercent': self.button_heightpercent,
            'button_elevation': self.button_elevation,
            'button_opacity': self.button_opacity,
            'button_titlesize': self.button_titlesize,
            'button_subtitlesize': self.button_subtitlesize,
            'button_radius': self.button_radius,

            'disclaimer': self.disclaimer,

            'buttons': self.buttons,

            'applogo_url': self.applogo_url,
            'creditslogo_url': self.creditslogo_url,
        }

    
    ######################################################################################################################################################
    # Read the configuration into a JSON file
    ######################################################################################################################################################
    def fromJson(self, j):

            self.title = j['title']
            self.subtitle = j['subtitle']
            self.titlesizepercent = j['titlesizepercent']
            self.subtitlesizepercent = j['subtitlesizepercent']
            self.applogo_url = j['applogo_url']
            self.applogo_widthpercent = j['applogo_widthpercent']
            self.credits = j['credits']
            self.creditslogo_url = j['creditslogo_url']
            self.text_color = j['text_color']
            self.background_image = j['background_image']
            self.background_filter = j['background_filter']
            self.vois_show = j['vois_show']
            self.vois_opacity = j['vois_opacity']

            self.titlebox_widthpercent = j['titlebox_widthpercent']
            self.titlebox_heightpercent = j['titlebox_heightpercent']
            self.titlebox_toppercent = j['titlebox_toppercent']
            self.titlebox_opacity = j['titlebox_opacity']
            self.titlebox_border = j['titlebox_border']

            self.titleshadow = j['titleshadow']
            self.titleshadow_color = j['titleshadow_color']

            self.buttonbox_widthpercent = j['buttonbox_widthpercent']
            self.buttonbox_heightpercent = j['buttonbox_heightpercent']
            self.buttonbox_toppercent = j['buttonbox_toppercent']

            self.creditbox_widthpercent = j['creditbox_widthpercent']
            self.creditbox_heightpercent = j['creditbox_heightpercent']
            self.creditbox_toppercent = j['creditbox_toppercent']
            self.creditbox_opacity = j['creditbox_opacity']

            self.button_widthpercent = j['button_widthpercent']
            self.button_heightpercent = j['button_heightpercent']
            self.button_elevation = j['button_elevation']
            self.button_opacity = j['button_opacity']
            self.button_titlesize = j['button_titlesize']
            self.button_subtitlesize = j['button_subtitlesize']
            self.button_radius = j['button_radius']

            self.disclaimer = j['disclaimer']

            self.buttons = j['buttons']
    