"""mainPage Configurator"""
# Author(s): Davide.De-Marchi@ec.europa.eu, Edoardo.Ramalli@ec.europa.eu
# Copyright © European Union 2024
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
from ipywidgets import widgets, HTML
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, page, selectImage, Button, UploadImage, sliderFloat, ColorPicker, switch

# Local imports
import mainPage
import PageConfigurator


# Panels dimensioning
LEFT_WIDTH = '30vw'


#####################################################################################################################################################
# mainPage Configurator
#####################################################################################################################################################
class MainConfigurator(page.page):


    # Initialization
    def __init__(self, output, onclose=None, leftWidth=LEFT_WIDTH, **kwargs):
        super().__init__('mainPage', 'Visual configurator', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre', left_back=True, **kwargs)

        # Initialize member variables
        self.leftWidth = leftWidth

        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')
        
    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%settings.color_first
        self.main_width  = 'calc(100vw - %s)'%self.leftWidth
        self.main_height = self.height
        self.cardLeft   = v.Card(flat=True, style_=st + 'border-right-width: 0px;', outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardMain   = v.Card(flat=True, style_=st + 'display: flex; justify-content: center; align-items: center;', outlined=True, width=self.main_width, height=self.main_height, color='#eeeeee')
        
        # Creation of the contents for the panels
        self.createMain()
        self.createLeft()
        
        # Compose the panels
        self.card.children = [ widgets.HBox([self.cardLeft, self.cardMain]) ]
        
        return self.card

    
    #################################################################################################################################################
    # Create the content of the left panel
    #################################################################################################################################################
    def createLeft(self):
        
        self.labelwidth  = 170
        self.sliderwidth = 150
        
        
        maxwidth = 'calc(%s - 0px)'%LEFT_WIDTH
        self.controls = v.Card(flat=True, width=maxwidth, min_width=maxwidth, max_width=maxwidth, class_='pa-3 pt-4 ma-0', style_='overflow: auto;')
        
        netwidth = 'calc(%s - 38px)'%LEFT_WIDTH
        titwidth = 'calc(%s - 170px)'%LEFT_WIDTH
        
        self.upload = UploadImage.UploadImage(self.output, width=620)
        
        self.tftitle = v.TextField(label='Application title:', autofocus=False, v_model=self.main.title, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.text_color = ColorPicker(dark=False, color=self.main.text_color, width=50, height=30, rounded=False, on_change=self.text_colorChange,  offset_x=True, offset_y=False)
        ct  = v.Card(flat=True, children=[self.tftitle], width=titwidth, min_width=titwidth, max_width=titwidth)
        cc  = v.Card(flat=True, children=[widgets.HBox([PageConfigurator.label('Text color:', color='black', width=66), self.text_color])], class_='pa-0 ma-0 mt-4')
        cr1 = v.Card(flat=True, children=[widgets.HBox([ct, cc])], width=netwidth, max_width=netwidth)
        
        self.tfsubtitle = v.TextField(label='Application subtitle:', autofocus=False, v_model=self.main.subtitle, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        
        
        self.tftitle.on_event(   'change',      self.titleChange)
        self.tftitle.on_event(   'click:clear', self.titleClear)
        self.tfsubtitle.on_event('change',      self.subtitleChange)
        self.tfsubtitle.on_event('click:clear', self.subtitleClear)
        
        self.applogo_image_url  = Button('Select image for the application logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                         text_weight=450, on_click=self.applogo_image_load, width=netwidth, height=40,
                                         tooltip='Click to select an image to use as application logo on the title bar', selected=True, rounded=settings.button_rounded)
        self.logowidth = sliderFloat.sliderFloat(self.main.applogo_widthpercent, text='Application logo width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                 labelwidth=self.labelwidth-10, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.logowidthChange)
        
        self.backgroundLabel = PageConfigurator.label('Background image: ')
        self.background_image_url = Button('Select image to use for the application background', color_selected=settings.color_first, dark=settings.dark_mode, 
                                           text_weight=450, on_click=self.background_image_load, width=netwidth, height=40,
                                           tooltip='Click to select an image to use as application background', selected=True, rounded=settings.button_rounded)
        
        images = [{ "name": 'Image %d'%x, "image": 'https://jeodpp.jrc.ec.europa.eu/services/shared/wallpapers/%d.jpg'%x, "max_width": 150, "max_height": 100 } for x in range(60)]
        self.background_image = selectImage.selectImage(images=images, selection=55, onchange=self.background_image_selected, width=netwidth,
                                                        label='Please select a stock image from the list', max_height=100, dense=True, outlined=True, clearable=True, margins="ma-0 mt-2 mr-1")

        
        self.vois_show = switch.switch(self.main.vois_show, 'Show vois credits', inset=True, dense=True, onchange=self.vois_showChange)
        self.vois_opacity = sliderFloat.sliderFloat(self.main.vois_opacity*100.0, text='vois opacity %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                    labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth-50, resetbutton=True, showtooltip=True, onchange=self.vois_opacityChange)
        if not self.main.vois_show: self.vois_opacity.slider.disabled = True

        self.tfcredits = v.TextField(label='Credits text:', autofocus=False, v_model=self.main.credits, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.tfcredits.on_event('change',      self.creditsChange)
        self.tfcredits.on_event('click:clear', self.creditsClear)
        
        self.creditslogo_url  = Button('Select image for credits box', color_selected=settings.color_first, dark=settings.dark_mode, 
                                         text_weight=450, on_click=self.creditslogo_image_load, width=netwidth, height=40,
                                         tooltip='Click to select an image to use as credits logo on the bottom bar', selected=True, rounded=settings.button_rounded)
        
        self.controls.children = [widgets.VBox([
            cr1,
            self.tfsubtitle,
            self.applogo_image_url,
            self.logowidth.draw(),
            self.backgroundLabel,
            self.background_image_url,
            self.spacerY,
            self.background_image,
            widgets.HBox([v.Card(flat=True, children=[self.vois_show.draw()], class_='pa-0 ma-0 mt-2 mr-9'), self.vois_opacity.draw()]),
            self.tfcredits,
            self.creditslogo_url,
        ])]
        
        self.cardLeft.children = [self.controls]

    
    #################################################################################################################################################
    # Create the content of the Main panel
    #################################################################################################################################################
    def createMain(self):

        self.main = mainPage.mainPage(background_image=55)
        self.updatePreview()
        
        
    # Update the preview
    def updatePreview(self):
        self.cardMain.children = [self.main.preview()]
        
    
    
    # Change application title
    def titleChange(self, *args):
        if self.tftitle.v_model is None: name = ''
        else:                            name = self.tftitle.v_model
        self.main.title = name
        self.updatePreview()

    def titleClear(self, *args):
        self.main.title = ''
        self.updatePreview()

        
    # Change application subtitle
    def subtitleChange(self, *args):
        if self.tfsubtitle.v_model is None: name = ''
        else:                               name = self.tfsubtitle.v_model
        self.main.subtitle = name
        self.updatePreview()

    def subtitleClear(self, *args):
        self.main.subtitle = ''
        self.updatePreview()
        
        
    # Change of the text_color
    def text_colorChange(self):
        self.main.text_color = self.text_color.color
        self.updatePreview()
        
        
    # Selection of the application image to load from the local machine
    def applogo_image_loaded(self, imageurl):
        self.main.applogo_url = imageurl
        self.updatePreview()

    # Click on the button to open the dialog to select the the application image
    def applogo_image_load(self, *args):
        self.upload.title = 'Select image for the application logo'
        self.upload.onOK  = self.applogo_image_loaded
        self.upload.show()

        
    # Change logo width
    def logowidthChange(self, width):
        self.main.applogo_widthpercent = int(width)
        self.updatePreview()
        
        
    # Selection of the backgound image to load from the local machine
    def background_image_loaded(self, imageurl):
        self.main.background_image = imageurl
        self.updatePreview()

    # Click on the button to open the dialog to select the the background image
    def background_image_load(self, *args):
        self.upload.title = 'Select image for the application background'
        self.upload.onOK  = self.background_image_loaded
        self.upload.show()
        
        
    # Selection of a stock backkround image
    def background_image_selected(self):
        self.main.background_image = self.background_image.value
        self.updatePreview()
        
        
    # Change of vois_show flag
    def vois_showChange(self, flag):
        self.main.vois_show = flag
        self.vois_opacity.slider.disabled = not self.main.vois_show
        self.updatePreview()
        
        
    # Change vois opacity
    def vois_opacityChange(self, opacity):
        self.main.vois_opacity = opacity / 100.0
        self.updatePreview()

        
    # Change credits text
    def creditsChange(self, *args):
        if self.tfcredits.v_model is None: name = ''
        else:                              name = self.tfcredits.v_model
        self.main.credits = name
        self.updatePreview()

    def creditsClear(self, *args):
        self.main.credits = ''
        self.updatePreview()
        
        
    # Selection of the credits image to load from the local machine
    def creditslogo_image_loaded(self, imageurl):
        self.main.creditslogo_url = imageurl
        self.updatePreview()

    # Click on the button to open the dialog to select the the credits image
    def creditslogo_image_load(self, *args):
        self.upload.title = 'Select image for the credits image'
        self.upload.onOK  = self.creditslogo_image_loaded
        self.upload.show()
