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
from vois.vuetify import settings, dialogGeneric, card
from ipywidgets import widgets, Layout, HTML
from IPython.display import display
import ipyvuetify as v
import os


######################################################################################################################################################
# Check if running in Voila: /eos is not mounted...
######################################################################################################################################################
def RunningInVoila():
    return not os.path.isdir("/eos/jeodpp/data/SRS/")


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
        Width of the area where the application logo is displayed in percentage of the screen (default is 35.0)
    credits : str, optional
        Credits string to display inside the credit box on the bottom of the page (default is 'Credits Team XXX')
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
        Opacity to apply to the vois logo, in case vois_show is set to True (default is 0.4)
    titlebox_widthpercent : float, optional
        Width of the top box containing the title, in percentage of the screen width. Default is 40.0.
    titlebox_heightpercent : float, optional
        Height of the box containing the title, in percentage of the screen height. Default is 24.0.
    titlebox_toppercent : float, optional
        Top position of the box containing the title, in percentage of the screen height, measured from the top of the page. Default is 14.0.
    titlebox_opacity : float, optional
        Opacity to apply to the box containing the title (default is 0.4)
    titlebox_border : int, optional
        Border width in pixels of the box containing the title (default is 4)
    buttonbox_widthpercent : float, optional
        Width of the box containing the buttons, in percentage of the screen width. Default is 80.0.
    buttonbox_heightpercent : float, optional
        Height of the box containing the buttons, in percentage of the screen height. Default is 50.0.
    buttonbox_toppercent : float, optional
        Top position of the box containing the buttons, in percentage of the screen height, measured from the top of the page. Default is 43.0.
    creditbox_widthpercent : float, optional
        Width of the box containing the credits, in percentage of the screen width. Default is 80.0.
    creditbox_heightpercent : float, optional
        Height of the box containing the credits, in percentage of the screen height. Default is 17.0.
    creditbox_toppercent : float, optional
        Top position of the box containing the credits, in percentage of the screen height, measured from the top of the page. Default is 80.0.
    creditbox_opacity : float, optional
        Opacity to apply to the box containing the credits (default is 0.6)
    button_widthpercent : float, optional
        Width of each of the buttons, in percentage of the screen width. Default is 30.0.
    button_heightpercent : float, optional
        Height of each of the buttons, in percentage of the screen height. Default is 10.0.
    button_elevation : int, optional
        Elevation in pixels to apply to the buttons (default is 6)
    button_opacity: float, optional
        Opacity to apply to the buttons (default is 0.5)

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
                 applogo_url='https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/sampleapplogo.png',
                 applogo_widthpercent=35.0,
                 credits='Credits Team XXX',
                 creditslogo_url='https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/TransparentJRC.png',
                 text_color='#0e446e',
                 background_image=22,
                 background_filter='',
                 vois_show=True,
                 vois_opacity=0.4,
                 titlebox_widthpercent=40.0,
                 titlebox_heightpercent=24.0,
                 titlebox_toppercent=14.0,
                 titlebox_opacity=0.4,
                 titlebox_border=4,
                 buttonbox_widthpercent=80.0,
                 buttonbox_heightpercent=50.0,
                 buttonbox_toppercent=43.0,
                 creditbox_widthpercent=80.0,
                 creditbox_heightpercent=17.0,
                 creditbox_toppercent=80.0,
                 creditbox_opacity=0.6,
                 button_widthpercent=30.0,
                 button_heightpercent=10.0,
                 button_elevation=6,
                 button_opacity=0.5,
                ):

        self.output = widgets.Output(layout=Layout(width='0px', height='0px'))
        
        self.title                   = title
        self.subtitle                = subtitle
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
        
        self.buttons = []

        
        # Spacers
        self.spacer = v.Html(tag='div',children=[' '], style_='width: 16px; height: 20px;')

        # Dimension of the main title rectangle
        width = '%fvw'%self.titlebox_widthpercent
        height = '%fvh'%self.titlebox_heightpercent


        
        ######################################################################################################################################################
        # Main titles
        ######################################################################################################################################################
        html_main = '''
        <head>
            <meta charset="utf-8" />
            <link href='http://fonts.googleapis.com/css?family=PT+Sans' rel='stylesheet' type='text/css'>
            <style>
                .big {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(5.0vh, 3.7vw);
                    font-weight: 700;
                    text-shadow: -0.06vh -0.06vh 0 #fff, 0.06vh -0.06vh 0 #fff, -0.06vh 0.06vh 0 #fff, 0.06vh 0.06vh 0 #fff;
                    text-align: center;
                    line-height: 2.0;
                    color: %s;
                }
                .normal {
                    font-family: 'PT Sans', sans-serif;
                    font-size: min(2.65vh, 2.0vw);
                    font-weight: 700;
                    text-align: center;
                    line-height: 1.0;
                    color: %s;
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
        ''' % (self.text_color, self.text_color, self.applogo_widthpercent, self.title, self.subtitle, self.applogo_url)

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
        html_unit = '''
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
        </body>
        '''%(self.text_color, self.creditslogo_url, self.credits)

        cardunit = v.Card(flat=True, children=[HTML(html_unit)], style_="background-color: #ffffff00;", class_="pa-0 ma-0 mt-2")
        bcol = '#ffffff%0.2X'%(int(self.creditbox_opacity*255))
        self.hunit = v.Html(tag='div', children=[cardunit], class_="pa-0 ma-0",
                            style_='width: %fvw; height: %fvh; border: 0px solid #000000; border-radius: 12px; position: absolute; top: %fvh; left: %fvw; background-color: %s; overflow: hidden;'%(self.creditbox_widthpercent, self.creditbox_heightpercent,
                            self.creditbox_toppercent, (100.0-self.creditbox_widthpercent)/2.0, bcol))



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
        nbuttons_per_row = self.buttonbox_widthpercent // self.button_widthpercent
        
        rows = []
        
        children = []
        i = 0
        for b in self.buttons:
            c = card.card(elevation=self.button_elevation, width='%fvw'%self.button_widthpercent, imagesize="%fvh"%self.button_heightpercent, responsive=True,
                          title=b['title'], subtitle=b['subtitle'], titletooltip=b['tooltip'],
                          color='#ffffff%0.2X'%int(self.button_opacity*255), fontsizemultiplier=1.1, subtitleweight=400,
                          image=b['image'], on_click=b['onclick'], argument=b['argument'], textcolor=self.text_color)
            if len(children) > 0:
                children.append(self.spacer)
            children.append(c)
            
            i += 1
            if i >= nbuttons_per_row:
                r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2")
                rows.append(r)
                i = 0
                children = []
                
        if len(children) > 0:
            r = v.Row(justify="center", children=children, class_="pa-0 ma-0 mt-2")
            rows.append(r)
            
        hpages = v.Html(tag='div', children=rows, class_="pa-0 ma-0",
                        style_='width: %fvw; height: %fvh; position: absolute; top: %fvh; left: %fvw; background-color: #ffffff00; overflow: hidden;'%(self.buttonbox_widthpercent, self.buttonbox_heightpercent, self.buttonbox_toppercent, (100.0-self.buttonbox_widthpercent)/2.0))

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
