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
from ipywidgets import widgets, HTML, Layout
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, page, selectImage, Button, UploadImage, sliderFloat, ColorPicker, switch, selectSingle, tabs, sortableList, dialogGeneric

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
        super().__init__('mainPage', 'Visual configurator', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre',
                         left_back=True, **kwargs)

        # Initialize member variables
        self.leftWidth = 'calc(%s - 2px)'%leftWidth

        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')
        
        self.debug = widgets.Output()
        
        
    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: auto;'%settings.color_first
        self.main_width  = 'calc(100vw - %s)'%self.leftWidth
        self.main_height = self.height
        self.cardLeft   = v.Card(flat=True, style_=st + 'border-right-width: 0px;', outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardMain   = v.Card(flat=True, style_=st + 'display: flex; justify-content: center; align-items: center;', outlined=True, width=self.main_width, height=self.main_height, color='#eeeeee')
        
        # Creation of the contents for the panels
        self.createMain()
        self.createLeft()
        
        # Compose the panels
        self.card.children = [ widgets.HBox([self.cardLeft, self.cardMain]) ]
        
        # Set the logo
        self.logowidth  = 70
        self.logoappurl = mainPage.getLocalImageURL('./graphics/main.png')
        
        return self.card

    
    #################################################################################################################################################
    # Create the content of the left panel
    #################################################################################################################################################
    def createLeft(self):
        
        self.labelwidth  = 160
        self.sliderwidth = 140
        
        
        maxwidth = 'calc(%s - 20px)'%LEFT_WIDTH
        self.controls = v.Card(flat=True, width=maxwidth, min_width=maxwidth, max_width=maxwidth, class_='pa-3 pt-4 ma-0', style_='overflow: auto;')
        
        netwidth = 'calc(%s - 58px)'%LEFT_WIDTH
        titwidth = 'calc(%s - 190px)'%LEFT_WIDTH
        
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
                                                 labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.logowidthChange)
        
        
        self.title_width   = sliderFloat.sliderFloat(self.main.titlebox_widthpercent, text='Title box width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlebox_widthpercent)
        self.title_height  = sliderFloat.sliderFloat(self.main.titlebox_heightpercent, text='Title box height %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlebox_heightpercent)
        self.title_top     = sliderFloat.sliderFloat(self.main.titlebox_toppercent, text='Title box top %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlebox_toppercent)
        self.title_opacity = sliderFloat.sliderFloat(self.main.titlebox_opacity*100.0, text='Title box opacity %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlebox_opacity)
        self.title_border  = sliderFloat.sliderFloat(self.main.titlebox_border, text='Title box border (px):', minvalue=0.0, maxvalue=10.0, maxint=10, showpercentage=False, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlebox_border)
        
        self.background_image_url = Button('Select image for the application background', color_selected=settings.color_first, dark=settings.dark_mode, 
                                           text_weight=450, on_click=self.background_image_load, width=netwidth, height=40,
                                           tooltip='Click to select an image to use as application background', selected=True, rounded=settings.button_rounded)
        
        images = [{ "name": '%d'%x, "image": 'https://jeodpp.jrc.ec.europa.eu/services/shared/wallpapers/%d.jpg'%x, "max_width": 150, "max_height": 100 } for x in range(60)]
        self.background_image = selectImage.selectImage(images=images, selection=55, onchange=self.background_image_selected, width='380px',
                                                        label='Please select a stock image from the list', max_height=100, dense=True, outlined=True, clearable=True, margins="ma-0 mt-2 mr-1")

        self.filter_enabled = True
        self.filter_reset = Button('Reset all filters', color_selected=settings.color_first, dark=settings.dark_mode, 
                                    text_weight=450, on_click=self.onFilterReset, width=190, height=40,
                                    tooltip='Click to reset all filters for the background image', selected=True, rounded=settings.button_rounded)
        
        
        self.filter_blur = selectSingle.selectSingle('Blur:', ['0', '1', '2', '3', '4', '5', '6'], selection='0', width=80, clearable=False, onchange=self.onFilterChange)
        
        self.filter_grayscale = sliderFloat.sliderFloat(0, text='Grayscale:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)
        
        self.filter_brightness = sliderFloat.sliderFloat(100, text='Brightness:', minvalue=0.0, maxvalue=200.0, maxint=200, showpercentage=True, decimals=0,
                                                         labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)

        self.filter_contrast = sliderFloat.sliderFloat(100, text='Contrast:', minvalue=0.0, maxvalue=200.0, maxint=200, showpercentage=True, decimals=0,
                                                       labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)

        self.filter_saturate = sliderFloat.sliderFloat(100, text='Saturate:', minvalue=0.0, maxvalue=200.0, maxint=200, showpercentage=True, decimals=0,
                                                      labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)
        
        self.filter_hue = sliderFloat.sliderFloat(0, text='Hue:', minvalue=0.0, maxvalue=360.0, maxint=360, showpercentage=True, decimals=0,
                                                  labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)
        
        self.filter_opacity = sliderFloat.sliderFloat(100, text='Opacity:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                      labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)
        
        self.filter_sepia = sliderFloat.sliderFloat(0, text='Sepia:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                      labelwidth=self.labelwidth-70, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.onFilterChange)
        
        
        self.buttonbox_width  = sliderFloat.sliderFloat(self.main.buttonbox_widthpercent, text='Button box width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_buttonbox_widthpercent)
        self.buttonbox_height = sliderFloat.sliderFloat(self.main.buttonbox_heightpercent, text='Button box height %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_buttonbox_heightpercent)
        self.buttonbox_top    = sliderFloat.sliderFloat(self.main.buttonbox_toppercent, text='Button box top %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_buttonbox_toppercent)

        
        self.button_width  = sliderFloat.sliderFloat(self.main.button_widthpercent, text='Buttons width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_width)
        self.button_height = sliderFloat.sliderFloat(self.main.button_heightpercent, text='Buttons height %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_height)
        self.button_elevation = sliderFloat.sliderFloat(self.main.button_elevation, text='Buttons elevation:', minvalue=0.0, maxvalue=10.0, maxint=10, showpercentage=False, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_elevation)
        self.button_opacity = sliderFloat.sliderFloat(self.main.titlebox_opacity*100.0, text='Buttons opacity %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                      labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_opacity)
        self.button_titlesize = sliderFloat.sliderFloat(float(self.main.button_titlesize.replace('vh','')), text='Buttons title size:', minvalue=0.1, maxvalue=4.0, maxint=39, showpercentage=False, decimals=1,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_titlesize)
        self.button_subtitlesize = sliderFloat.sliderFloat(float(self.main.button_subtitlesize.replace('vh','')), text='Buttons subtitle size:', minvalue=0.1, maxvalue=4.0, maxint=39, showpercentage=False, decimals=1,
                                                           labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_subtitlesize)
        self.button_radius = sliderFloat.sliderFloat(float(self.main.button_radius.replace('px','')), text='Button radius (px):', minvalue=0.0, maxvalue=20.0, maxint=20, showpercentage=False, decimals=0,
                                                     labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_button_radius)
        
        self.blist = sortableList.sortableList(items=self.main.buttons, dark=False, allowNew=True, itemNew=self.buttonNew, itemContent=self.buttonDisplay,
                                               onadded=self.buttonsUpdate, onremoved=self.buttonsUpdate, onmovedown=self.buttonsUpdate, onmoveup=self.buttonsUpdate)
        
        self.vois_show = switch.switch(self.main.vois_show, 'Show vois credits', inset=True, dense=True, onchange=self.vois_showChange)
        self.vois_opacity = sliderFloat.sliderFloat(self.main.vois_opacity*100.0, text='vois opacity:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                    labelwidth=90, sliderwidth=100, resetbutton=True, showtooltip=True, onchange=self.vois_opacityChange)
        if not self.main.vois_show: self.vois_opacity.slider.disabled = True

        self.tfcredits = v.TextField(label='Credits text:', autofocus=False, v_model=self.main.credits, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.tfcredits.on_event('change',      self.creditsChange)
        self.tfcredits.on_event('click:clear', self.creditsClear)
        
        self.creditslogo_url  = Button('Select image for credits box', color_selected=settings.color_first, dark=settings.dark_mode, 
                                       text_weight=450, on_click=self.creditslogo_image_load, width=netwidth, height=40,
                                       tooltip='Click to select an image to use as credits logo on the bottom bar', selected=True, rounded=settings.button_rounded)
        
        self.credits_width   = sliderFloat.sliderFloat(self.main.creditbox_widthpercent, text='Credits box width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                       labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_creditbox_widthpercent)
        self.credits_height  = sliderFloat.sliderFloat(self.main.creditbox_heightpercent, text='Credits box height %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                       labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_creditbox_heightpercent)
        self.credits_top     = sliderFloat.sliderFloat(self.main.creditbox_toppercent, text='Credits box top %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                       labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_creditbox_toppercent)
        self.credits_opacity = sliderFloat.sliderFloat(self.main.creditbox_opacity*100.0, text='Credits box opacity %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
                                                       labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_creditbox_opacity)
        
        self.tfdisclaimer = v.TextField(label='Disclaimer:', autofocus=False, v_model=self.main.disclaimer, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.tfdisclaimer.on_event(   'change',      self.disclaimerChange)
        self.tfdisclaimer.on_event(   'click:clear', self.disclaimerClear)
        
        
        # Tabs to group controls
        self.card_title      = v.Card(flat=True)
        self.card_background = v.Card(flat=True)
        self.card_buttons    = v.Card(flat=True)
        self.card_credits    = v.Card(flat=True)
        self.card_vois       = v.Card(flat=True)
        self.tabsView = tabs.tabs(0, ['Title', 'Background', 'Buttons', 'Credits', 'Vois'],
                                  contents=[self.card_title, self.card_background, self.card_buttons, self.card_credits, self.card_vois],
                                  dark=False, onchange=None, row=True)

        self.card_title.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            cr1,
            self.tfsubtitle,
            self.applogo_image_url,
            self.logowidth.draw(),
            self.title_width.draw(),
            self.title_height.draw(),
            self.title_top.draw(),
            self.title_opacity.draw(),
            self.title_border.draw()
        ])]
        
        self.card_background.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            self.background_image_url,
            self.spacerY,
            self.spacerY,
            self.background_image,
            self.spacerY,
            self.spacerY,
            widgets.HBox([self.filter_reset, self.spacerX, self.spacerX, self.spacerX, self.filter_blur.draw()]), 
            self.filter_grayscale.draw(),
            self.filter_brightness.draw(),
            self.filter_contrast.draw(),
            self.filter_saturate.draw(),
            self.filter_hue.draw(),
            self.filter_sepia.draw(),
            self.filter_opacity.draw()
        ])]
        
        
        self.card_buttons.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            self.buttonbox_width.draw(),
            self.buttonbox_height.draw(),
            self.buttonbox_top.draw(),
            self.button_width.draw(),
            self.button_height.draw(),
            self.button_elevation.draw(),
            self.button_opacity.draw(),
            self.button_titlesize.draw(),
            self.button_subtitlesize.draw(),
            self.button_radius.draw(),
            PageConfigurator.label('Buttons:'),
            self.blist.draw()
        ])]
        
        
        self.card_credits.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            self.tfcredits,
            self.spacerY,
            self.creditslogo_url,
            self.spacerY,
            self.spacerY,
            self.tfdisclaimer,
            self.spacerY,
            self.spacerY,
            self.credits_width.draw(),
            self.credits_height.draw(),
            self.credits_top.draw(),
            self.credits_opacity.draw()
        ])]
        
        
        self.card_vois.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            self.vois_show.draw(),
            self.spacerY,
            self.vois_opacity.draw()
        ])]
        
        self.controls.children = [self.tabsView.draw()]
        
        self.cardLeft.children = [self.controls]

    
    
    #################################################################################################################################################
    # Create the content of the Main panel
    #################################################################################################################################################
    def createMain(self):

        self.main = mainPage.mainPage(background_image=55)
        self.updatePreview()
        
        
        
    #################################################################################################################################################
    # Management of events in widgets
    #################################################################################################################################################
        
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
        
    # titlebox_widthpercent   
    def on_titlebox_widthpercent(self, value):
        self.main.titlebox_widthpercent = int(value)
        self.updatePreview()

    # titlebox_heightpercent
    def on_titlebox_heightpercent(self, value):
        self.main.titlebox_heightpercent = int(value)
        self.updatePreview()
        
    # titlebox_toppercent
    def on_titlebox_toppercent(self, value):
        self.main.titlebox_toppercent = int(value)
        self.updatePreview()
        
    # titlebox_opacity
    def on_titlebox_opacity(self, value):
        self.main.titlebox_opacity = value/100.0
        self.updatePreview()

    # titlebox_widthpercent   
    def on_titlebox_border(self, value):
        self.main.titlebox_border = int(value)
        self.updatePreview()
        
        
    # Selection of the backgound image to load from the local machine
    def background_image_loaded(self, imageurl):
        self.main.background_image = imageurl
        self.background_image.value = -1
        self.updatePreview()

    # Click on the button to open the dialog to select the the background image
    def background_image_load(self, *args):
        self.upload.title = 'Select image for the application background'
        self.upload.onOK  = self.background_image_loaded
        self.upload.show()
        
        
    # Selection of a stock background image
    def background_image_selected(self):
        if self.background_image.value >= 0:
            self.main.background_image = self.background_image.value
            self.updatePreview()
        
        
    # Filter reset
    def onFilterReset(self):
        self.filter_enabled = False
        self.filter_blur.value       = '0'
        self.filter_grayscale.value  = 0
        self.filter_brightness.value = 100
        self.filter_contrast.value   = 100
        self.filter_saturate.value   = 100
        self.filter_hue.value        = 0
        self.filter_opacity.value    = 100
        self.filter_sepia.value      = 0
        self.filter_enabled = True
        self.onFilterChange()
        
        
    # Filter change
    def onFilterChange(self, *args):
        if self.filter_enabled:
            filter = ''

            n = int(self.filter_blur.value)
            if n > 0: filter += 'blur(%dpx) '%n

            n = int(self.filter_grayscale.value)
            if n > 0: filter += 'grayscale(%d%%) '%n

            n = int(self.filter_brightness.value)
            if n != 100: filter += 'brightness(%d%%) '%n

            n = int(self.filter_contrast.value)
            if n != 100: filter += 'contrast(%d%%) '%n

            n = int(self.filter_saturate.value)
            if n != 100: filter += 'saturate(%d%%) '%n
            
            n = int(self.filter_hue.value)
            if n != 0: filter += 'hue-rotate(%ddeg) '%n

            n = int(self.filter_sepia.value)
            if n != 0: filter += 'sepia(%d%%) '%n
            
            n = int(self.filter_opacity.value)
            if n != 100: filter += 'opacity(%d%%) '%n

            self.main.background_filter = filter
            self.updatePreview()
        
        
    # buttonbox_widthpercent   
    def on_buttonbox_widthpercent(self, value):
        self.main.buttonbox_widthpercent = int(value)
        self.updatePreview()

    # buttonbox_heightpercent
    def on_buttonbox_heightpercent(self, value):
        self.main.buttonbox_heightpercent = int(value)
        self.updatePreview()
        
    # buttonbox_toppercent
    def on_buttonbox_toppercent(self, value):
        self.main.buttonbox_toppercent = int(value)
        self.updatePreview()

        
    # button_widthpercent
    def on_button_width(self, value):
        self.main.button_widthpercent = int(value)
        self.updatePreview()

    # button_heightpercent
    def on_button_height(self, value):
        self.main.button_heightpercent = int(value)
        self.updatePreview()

    # button_elevation
    def on_button_elevation(self, value):
        self.main.button_elevation = int(value)
        self.updatePreview()

    # button_opacity
    def on_button_opacity(self, value):
        self.main.button_opacity = value/100.0
        self.updatePreview()

    # button_titlesize
    def on_button_titlesize(self, value):
        self.main.button_titlesize = '%fvh'%value
        self.updatePreview()

    # button_subtitlesize
    def on_button_subtitlesize(self, value):
        self.main.button_subtitlesize = '%fvh'%value
        self.updatePreview()
        self.button_subtitlesize.draw(),
            
    # button_radius
    def on_button_radius(self, value):
        self.main.button_radius = '%dpx'%int(value)
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

        
    # Change disclaimer text
    def disclaimerChange(self, *args):
        if self.tfdisclaimer.v_model is None: name = ''
        else:                                 name = self.tfdisclaimer.v_model
        self.main.disclaimer = name
        self.updatePreview()

    def disclaimerClear(self, *args):
        self.main.disclaimer = ''
        self.updatePreview()


    # creditbox_widthpercent   
    def on_creditbox_widthpercent(self, value):
        self.main.creditbox_widthpercent = int(value)
        self.updatePreview()

    # creditbox_heightpercent
    def on_creditbox_heightpercent(self, value):
        self.main.creditbox_heightpercent = int(value)
        self.updatePreview()
        
        
    # creditbox_toppercent
    def on_creditbox_toppercent(self, value):
        self.main.creditbox_toppercent = int(value)
        self.updatePreview()
        
        
    # creditbox_opacity
    def on_creditbox_opacity(self, value):
        self.main.creditbox_opacity = value/100.0
        self.updatePreview()
        

    # Add a new button
    def buttonNew(self):
        eb = EditButton(self.output, newButton=True, onOK=self.AddNewButton)
        return None
    
    def AddNewButton(self, b):
        self.blist.doAddItem(b)
        self.updatePreview()
        
        
    # Display a button
    def buttonDisplay(self, item, index):
        
        def UpdateButton(b):
            self.main.buttons[index] = b
            self.blist.items = self.main.buttons
            self.updatePreview()
            
        def onclick(*args):
            eb = EditButton(self.output, title=item['title'], subtitle=item['subtitle'], tooltip=item['tooltip'], image=item['image'], onclick=item['onclick'], argument=item['argument'], newButton=False, onOK=UpdateButton)
            
        lab = PageConfigurator.label(item['title'], class_='pa-0 ma-0 ml-2 mb-2', color='black')
        lab.on_event('click', onclick)
        return [lab]
        
    # Added or removed a button
    def buttonsUpdate(self, *args):
        self.updatePreview()
        
        
        
#####################################################################################################################################################
# Create a New button or Edit info on a button
#####################################################################################################################################################
class EditButton():
    
    def __init__(self, output, title='', subtitle='', tooltip='', image='', onclick=None, argument=None, onOK=None, newButton=True):
        
        self.onOK = onOK
        self.upload = UploadImage.UploadImage(output, width=620)

        self.image = ''

        self.tit    = v.TextField(label='Title:',          autofocus=True,  v_model=title,    dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.subtit = v.TextField(label='Subtitle:',       autofocus=False, v_model=subtitle, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.ttip   = v.TextField(label='Tooltip:',        autofocus=False, v_model=tooltip,  dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.oncl   = v.TextField(label='On click call:',  autofocus=False, v_model=onclick,  dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.arg    = v.TextField(label='Argument:',       autofocus=False, v_model=argument, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")

        b = Button('Select image for the button', color_selected=settings.color_first, dark=settings.dark_mode, 
                   text_weight=450, on_click=self.onSelectImage, width=570, height=40,
                   tooltip='Click to select an image to display on the button', selected=True, rounded=settings.button_rounded)

        c = v.Card(flat=True, children=[widgets.VBox([self.tit, self.subtit, self.ttip, self.oncl, self.arg, b])], class_='pa-4 ma-0')

        if newButton: dialogtitle = 'New button'
        else:         dialogtitle = 'Edit button'
        dlg = dialogGeneric.dialogGeneric(title=dialogtitle,
                                          text='',
                                          show=True, addclosebuttons=True, width=600,
                                          addokcancelbuttons=True, on_ok=self.AddedButton,
                                          fullscreen=False, content=[c], output=output)
        
        return None
        
        
    def onImageLoaded(self, imageurl):
        self.image = imageurl


    def onSelectImage(self):
        self.upload.title = 'Select image for the button'
        self.upload.onOK  = self.onImageLoaded
        self.upload.show()

    def AddedButton(self):
        self.button = {'title':    self.tit.v_model,
                       'subtitle': self.subtit.v_model,
                       'tooltip':  self.ttip.v_model,
                       'image':    self.image,
                       'onclick':  self.oncl.v_model,
                       'argument': self.arg.v_model}
        
        if self.onOK is not None:
            self.onOK(self.button)
        