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
import json

# Vois imports
from vois import download
from vois.vuetify import settings, page, selectImage, Button, UploadImage, UploadJson, sliderFloat, ColorPicker, switch, selectSingle, tabs, sortableList, dialogGeneric, iconButton
from vois.vuetify import mainPage
from vois.templates import PageConfigurator


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
        
        self.updatePageEnabled = True
        
        
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
        self.logoappurl = mainImage
        
        return self.card

    
    #################################################################################################################################################
    # Create the content of the left panel
    #################################################################################################################################################
    def createLeft(self):
        
        self.labelwidth  = 160
        self.sliderwidth = 140
        
        
        maxwidth = 'calc(%s - 20px)'%LEFT_WIDTH
        self.controls = v.Card(flat=True, width=maxwidth, min_width=maxwidth, max_width=maxwidth, class_='pa-3 pt-1 ma-0', style_='overflow: auto;')
        
        netwidth = 'calc(%s - 58px)'%LEFT_WIDTH
        titwidth = 'calc(%s - 210px)'%LEFT_WIDTH
        
        self.upload = UploadImage.UploadImage(self.output, width=620)
        
        self.tftitle = v.TextField(label='Application title:', autofocus=False, v_model=self.main.title, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-6")
        self.text_color = ColorPicker(dark=False, color=self.main.text_color, width=50, height=30, rounded=False, on_change=self.text_colorChange,  offset_x=True, offset_y=False, color_theory_popup=True)
        ct  = v.Card(flat=True, children=[self.tftitle], width=titwidth, min_width=titwidth, max_width=titwidth)
        cc  = v.Card(flat=True, children=[widgets.HBox([PageConfigurator.label('Text color:', color='black', width=66), self.text_color, self.text_color.ctpopup.draw()])], class_='pa-0 ma-0 mt-4')
        cr1 = v.Card(flat=True, children=[widgets.HBox([ct, cc])], width=netwidth, max_width=netwidth)
        
        self.tfsubtitle = v.TextField(label='Application subtitle:', autofocus=False, v_model=self.main.subtitle, dense=True, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        
        
        self.tftitle.on_event(   'change',      self.titleChange)
        self.tftitle.on_event(   'click:clear', self.titleClear)
        self.tfsubtitle.on_event('change',      self.subtitleChange)
        self.tfsubtitle.on_event('click:clear', self.subtitleClear)
        
        self.titlesizepercent = sliderFloat.sliderFloat(self.main.titlesizepercent, text='Title size percent:', minvalue=0, maxvalue=200, maxint=200, showpercentage=True, decimals=0,
                                                        labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_titlesizepercent)
        self.subtitlesizepercent = sliderFloat.sliderFloat(self.main.subtitlesizepercent, text='Subtitle size percent:', minvalue=0, maxvalue=200, maxint=200, showpercentage=True, decimals=0,
                                                           labelwidth=self.labelwidth, sliderwidth=self.sliderwidth, resetbutton=True, showtooltip=True, onchange=self.on_subtitlesizepercent)
        
        self.titleshadow = switch.switch(self.main.titleshadow, 'Add shadow around application title', inset=True, dense=True, onchange=self.titleshadowChange)
        self.titleshadow_color = ColorPicker(dark=False, color=self.main.titleshadow_color, width=50, height=30, rounded=False, on_change=self.titleshadow_colorChange,  offset_x=True, offset_y=False, color_theory_popup=True)
        
        self.applogo_image_url  = Button('Select image for the application logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                         text_weight=450, on_click=self.applogo_image_load, width=netwidth, height=40,
                                         tooltip='Click to select an image to use as application logo on the title bar', selected=True, rounded=settings.button_rounded)
        self.slogowidth = sliderFloat.sliderFloat(self.main.applogo_widthpercent, text='Application logo width %:', minvalue=0.0, maxvalue=100.0, maxint=100, showpercentage=True, decimals=0,
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
        
        self.blist = sortableList.sortableList(items=self.main.buttons, dark=False, allowNew=True, itemNew=self.buttonNew, itemContent=self.buttonDisplay, onchange=self.AssignOrderToButtons,
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

        
        self.buttOpen  = iconButton.iconButton(icon='mdi-folder-open',  onclick=self.onOpen,  tooltip='Load state from file',                 margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttSave  = iconButton.iconButton(icon='mdi-content-save', onclick=self.onSave,  tooltip='Save current state to file',           margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttCode  = iconButton.iconButton(icon='mdi-file-code',    onclick=self.onCode,  tooltip='Generate and download code in Python', margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttReset = iconButton.iconButton(icon='mdi-backspace',    onclick=self.onReset, tooltip='Reset main page to default state',     margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        
        self.card_title.children = [widgets.VBox([
            self.spacerY,
            self.spacerY,
            cr1,
            self.tfsubtitle,
            self.titlesizepercent.draw(),
            self.subtitlesizepercent.draw(),
            self.applogo_image_url,
            self.slogowidth.draw(),
            self.title_width.draw(),
            self.title_height.draw(),
            self.title_top.draw(),
            self.title_opacity.draw(),
            self.title_border.draw(),
            self.titleshadow.draw(),
            widgets.HBox([PageConfigurator.label('Shadow color:', color='black'), self.titleshadow_color, self.titleshadow_color.ctpopup.draw()])
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
        
        self.controls.children = [ widgets.VBox([
            widgets.HBox([self.buttOpen.draw(), self.buttSave.draw(), self.buttCode.draw(), self.buttReset.draw()]),
            self.tabsView.draw()
        ])]
        
        self.cardLeft.children = [self.controls]

    
    
    #################################################################################################################################################
    # Create the content of the Main panel
    #################################################################################################################################################
    def createMain(self):

        self.main = mainPage.mainPage(background_image=55)
        self.updatePreview()
        
        
    #################################################################################################################################################
    # Open, Save Reset buttons
    #################################################################################################################################################
        
    # Load state from file
    def onOpen(self):
        uj = UploadJson.UploadJson(self.output, onOK=self.onSelectedState, required_attributes=['title', 'subtitle'], attributes_width=80)
        uj.show()
        
        
    # Called when the UploadJson dialog-box is closed with the OK button
    def onSelectedState(self, state):
        self.main.fromJson(state)
        self.updateWidgets()
        self.updatePreview()
            
            
        
    # Save current state to file
    def onSave(self):
        self.saveFilename = v.TextField(label='File name:', autofocus=True, v_model=self.main.title, dense=False, color=settings.color_first, clearable=False, class_="pa-0 ma-0 ml-3 mt-3 mr-3")
        dialogGeneric.dialogGeneric(title='Save and download current state...' , on_ok=self.onDoSaveState, 
                                    text='   ', color=settings.color_first, dark=settings.dark_mode,
                                    titleheight=40, width=600,
                                    show=True, addclosebuttons=True, addokcancelbuttons=True,
                                    fullscreen=False, content=[self.saveFilename], output=self.output)
        
    
    # Effective save and download of the current state
    def onDoSaveState(self):
        
        filename = self.saveFilename.v_model
        if filename[-5:] != '.json':
            filename += '.json'
        
        state = self.main.toJson()
    
        # Convert to string and download
        txt = json.dumps(state, indent=4)
        download.downloadText(txt, fileName=filename)
        
                
    # Save Python code
    def onCode(self):
        self.saveFilename = v.TextField(label='File name:', autofocus=True, v_model=self.main.title, dense=False, color=settings.color_first, clearable=False, class_="pa-0 ma-0 ml-3 mt-3 mr-3")
        dialogGeneric.dialogGeneric(title='Save and download Python code...' , on_ok=self.onDoSaveCode, 
                                    text='   ', color=settings.color_first, dark=settings.dark_mode,
                                    titleheight=40, width=600,
                                    show=True, addclosebuttons=True, addokcancelbuttons=True,
                                    fullscreen=False, content=[self.saveFilename], output=self.output)

    
    # Effective save and download of the Python code
    def onDoSaveCode(self):
        
        self.onDoSaveState()   # Saves <filename>.json
        
        with self.debug:
            jsonfile = self.saveFilename.v_model
            if jsonfile[-5:] != '.json':
                jsonfile += '.json'

            notebookfile = self.saveFilename.v_model
            notebookfile += '.ipynb'

            scallbacks = ''
            for b in self.main.buttons:
                if 'onclick' in b and isinstance(b['onclick'], str) and len(b['onclick']) > 0 and not ' ' in b['onclick']:
                    scallbacks += '''
def %s(*args):
    dialogMessage.dialogMessage(title='Clicked on button %s', titleheight=36,
                                text='Change this lines with your code',
                                addclosebuttons=True, show=True, width=400, output=output)
    
'''%(b['onclick'],b['title'])

            # Code generation
            txt = '''from vois.vuetify import settings
settings.dark_mode      = True
settings.color_first    = '#0d856d'
settings.color_second   = '#a0dcd0'
settings.button_rounded = False

from ipywidgets import widgets, HTML, Layout
from IPython.display import display
import json

from vois import cssUtils
from vois.vuetify import mainPage, dialogMessage

output = widgets.Output(layout=Layout(width='0px', height='0px'))
display(output)

cssUtils.allSettings(output)
cssUtils.switchFontSize(output,14)

m = mainPage.mainPage()

%s

with open('%s') as f:
    j = json.load(f)
    m.fromJson(j)
    
for b in m.buttons:
    if 'onclick' in b and isinstance(b['onclick'], str) and len(b['onclick']) > 0 and not ' ' in b['onclick']:
        b['onclick'] = globals()[b['onclick']]
    
m.open()'''%(scallbacks, jsonfile)

            lines = txt.split('\n')
            lines = ",\n".join(["\"%s\\n\""%x for x in lines])

            txt = '''{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "65d32196-829e-41b9-a4e4-bdb6381998e9",
   "metadata": {},
   "outputs": [],
   "source": [
    %s
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [interapro_env]",
   "language": "python",
   "name": "conda-env-interapro_env-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
'''%lines
        
            # Download .ipynb file
            download.downloadText(txt, fileName=notebookfile)
            
            
            
    # Reset page to initial state
    def onReset(self):
        self.main = mainPage.mainPage(background_image=55)
        self.updateWidgets()
        self.updatePreview()
        
        
        
    #################################################################################################################################################
    # Update widgets reading members of self.main
    #################################################################################################################################################
    def updateWidgets(self):
        
        self.updatePageEnabled = False
        
        self.tftitle.v_model    = self.main.title
        self.text_color.color   = self.main.text_color
        self.tfsubtitle.v_model = self.main.subtitle
        
        self.titlesizepercent.value    = self.main.titlesizepercent
        self.subtitlesizepercent.value = self.main.subtitlesizepercent

        self.titleshadow.value       = self.main.titleshadow
        self.titleshadow_color.color = self.main.titleshadow_color
        
        self.slogowidth.value = self.main.applogo_widthpercent
        
        self.title_width.value    = self.main.titlebox_widthpercent
        self.title_height.value   = self.main.titlebox_heightpercent
        self.title_top.value      = self.main.titlebox_toppercent
        self.title_opacity.value  = self.main.titlebox_opacity*100.0
        self.title_border.value   = self.main.titlebox_border
        
        if isinstance(self.main.background_image, int):
            self.background_image.value = self.main.background_image
        else:
            self.background_image.value = -1

        self.filter_blur.value       = '0'
        self.filter_grayscale.value  = 0
        self.filter_brightness.value = 100
        self.filter_contrast.value   = 100
        self.filter_saturate.value   = 100
        self.filter_hue.value        = 0
        self.filter_opacity.value    = 100
        self.filter_sepia.value      = 0
                                                    
        filters = self.main.background_filter.strip().split(' ')
        for f in filters:
            if '(' in f and ')' in f:
                if 'blur' in f:
                    s = f.replace('blur','').replace('(','').replace(')','').strip().replace('px','')
                    if len(s) > 0:
                        self.filter_blur.value = str(int(s))

                if 'grayscale' in f:
                    s = f.replace('grayscale','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_grayscale.value = int(s)

                if 'brightness' in f:
                    s = f.replace('brightness','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_brightness.value = int(s)

                if 'contrast' in f:
                    s = f.replace('contrast','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_contrast.value = int(s)

                if 'saturate' in f:
                    s = f.replace('saturate','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_saturate.value = int(s)

                if 'hue-rotate' in f:
                    s = f.replace('hue-rotate','').replace('(','').replace(')','').strip().replace('deg','')
                    if len(s) > 0:
                        self.filter_hue.value = int(s)

                if 'sepia' in f:
                    s = f.replace('sepia','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_sepia.value = int(s)

                if 'opacity' in f:
                    s = f.replace('opacity','').replace('(','').replace(')','').strip().replace('%','')
                    if len(s) > 0:
                        self.filter_opacity.value = int(s)
            
        
        self.buttonbox_width.value     = self.main.buttonbox_widthpercent
        self.buttonbox_height.value    = self.main.buttonbox_heightpercent
        self.buttonbox_top.value       = self.main.buttonbox_toppercent
        
        self.button_width.value        = self.main.button_widthpercent
        self.button_height.value       = self.main.button_heightpercent
        self.button_elevation.value    = self.main.button_elevation
        self.button_opacity.value      = self.main.titlebox_opacity*100.0
        self.button_titlesize.value    = float(self.main.button_titlesize.replace('vh',''))
        self.button_subtitlesize.value = float(self.main.button_subtitlesize.replace('vh',''))
        self.button_radius.value       = float(self.main.button_radius.replace('px',''))
        
        self.blist.items = self.main.buttons
        
        self.vois_show.value = self.main.vois_show
        self.vois_opacity.value = self.main.vois_opacity*100.0
        if not self.main.vois_show: self.vois_opacity.slider.disabled = True

        self.tfcredits.value = self.main.credits
        
        self.credits_width.value   = self.main.creditbox_widthpercent
        self.credits_height.value  = self.main.creditbox_heightpercent
        self.credits_top.value     = self.main.creditbox_toppercent
        self.credits_opacity.value = self.main.creditbox_opacity*100.0
        
        self.tfdisclaimer.value = self.main.disclaimer
        
        self.updatePageEnabled = True
        
        
    #################################################################################################################################################
    # Management of events in widgets
    #################################################################################################################################################
        
    # Update the preview
    def updatePreview(self):
        self.cardMain.children = [self.main.preview()]
        
        
    
    # Change application title
    def titleChange(self, *args):
        if self.updatePageEnabled:
            if self.tftitle.v_model is None: name = ''
            else:                            name = self.tftitle.v_model
            self.main.title = name
            self.updatePreview()

    def titleClear(self, *args):
        if self.updatePageEnabled:
            self.main.title = ''
            self.updatePreview()

        
    # Change application subtitle
    def subtitleChange(self, *args):
        if self.updatePageEnabled:
            if self.tfsubtitle.v_model is None: name = ''
            else:                               name = self.tfsubtitle.v_model
            self.main.subtitle = name
            self.updatePreview()

    def subtitleClear(self, *args):
        if self.updatePageEnabled:
            self.main.subtitlesizepercent = ''
            self.updatePreview()

        
    def on_titlesizepercent(self, value):
        if self.updatePageEnabled:
            self.main.titlesizepercent = value
            self.updatePreview()
    
    def on_subtitlesizepercent(self, value):
        if self.updatePageEnabled:
            self.main.subtitlesizepercent = value
            self.updatePreview()

    # Change of the text_color
    def text_colorChange(self):
        if self.updatePageEnabled:
            self.main.text_color = self.text_color.color
            self.updatePreview()

        
    # titleshadow flag
    def titleshadowChange(self, flag):
        if self.updatePageEnabled:
            self.main.titleshadow = flag
            self.updatePreview()
        
    # titleshadow_color
    def titleshadow_colorChange(self,):
        if self.updatePageEnabled:
            self.main.titleshadow_color = self.titleshadow_color.color
            self.updatePreview()
    
    
    # Selection of the application image to load from the local machine
    def applogo_image_loaded(self, imageurl):
        if self.updatePageEnabled:
            self.main.applogo_url = imageurl
            self.updatePreview()

    # Click on the button to open the dialog to select the the application image
    def applogo_image_load(self, *args):
        if self.updatePageEnabled:
            self.upload.title = 'Select image for the application logo'
            self.upload.onOK  = self.applogo_image_loaded
            self.upload.show()

        
    # Change logo width
    def logowidthChange(self, width):
        if self.updatePageEnabled:
            self.main.applogo_widthpercent = int(width)
            self.updatePreview()
        
    # titlebox_widthpercent   
    def on_titlebox_widthpercent(self, value):
        if self.updatePageEnabled:
            self.main.titlebox_widthpercent = int(value)
            self.updatePreview()

    # titlebox_heightpercent
    def on_titlebox_heightpercent(self, value):
        if self.updatePageEnabled:
            self.main.titlebox_heightpercent = int(value)
            self.updatePreview()
        
    # titlebox_toppercent
    def on_titlebox_toppercent(self, value):
        if self.updatePageEnabled:
            self.main.titlebox_toppercent = int(value)
            self.updatePreview()
        
    # titlebox_opacity
    def on_titlebox_opacity(self, value):
        if self.updatePageEnabled:
            self.main.titlebox_opacity = value/100.0
            self.updatePreview()

    # titlebox_widthpercent   
    def on_titlebox_border(self, value):
        if self.updatePageEnabled:
            self.main.titlebox_border = int(value)
            self.updatePreview()
        
        
    # Selection of the backgound image to load from the local machine
    def background_image_loaded(self, imageurl):
        if self.updatePageEnabled:
            self.main.background_image = imageurl
            self.background_image.value = -1
            self.updatePreview()

    # Click on the button to open the dialog to select the the background image
    def background_image_load(self, *args):
        if self.updatePageEnabled:
            self.upload.title = 'Select image for the application background'
            self.upload.onOK  = self.background_image_loaded
            self.upload.show()
        
        
    # Selection of a stock background image
    def background_image_selected(self):
        if self.updatePageEnabled:
            if self.background_image.value >= 0:
                self.main.background_image = self.background_image.value
                self.updatePreview()
        
        
    # Filter reset
    def onFilterReset(self):
        if self.updatePageEnabled:
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
        if self.updatePageEnabled:
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
        if self.updatePageEnabled:
            self.main.buttonbox_widthpercent = int(value)
            self.updatePreview()

    # buttonbox_heightpercent
    def on_buttonbox_heightpercent(self, value):
        if self.updatePageEnabled:
            self.main.buttonbox_heightpercent = int(value)
            self.updatePreview()
        
    # buttonbox_toppercent
    def on_buttonbox_toppercent(self, value):
        if self.updatePageEnabled:
            self.main.buttonbox_toppercent = int(value)
            self.updatePreview()

        
    # button_widthpercent
    def on_button_width(self, value):
        if self.updatePageEnabled:
            self.main.button_widthpercent = int(value)
            self.updatePreview()

    # button_heightpercent
    def on_button_height(self, value):
        if self.updatePageEnabled:
            self.main.button_heightpercent = int(value)
            self.updatePreview()

    # button_elevation
    def on_button_elevation(self, value):
        if self.updatePageEnabled:
            self.main.button_elevation = int(value)
            self.updatePreview()

    # button_opacity
    def on_button_opacity(self, value):
        if self.updatePageEnabled:
            self.main.button_opacity = value/100.0
            self.updatePreview()

    # button_titlesize
    def on_button_titlesize(self, value):
        if self.updatePageEnabled:
            self.main.button_titlesize = '%fvh'%value
            self.updatePreview()

    # button_subtitlesize
    def on_button_subtitlesize(self, value):
        if self.updatePageEnabled:
            self.main.button_subtitlesize = '%fvh'%value
            self.updatePreview()
            self.button_subtitlesize.draw(),
            
    # button_radius
    def on_button_radius(self, value):
        if self.updatePageEnabled:
            self.main.button_radius = '%dpx'%int(value)
            self.updatePreview()

        
    # Change of vois_show flag
    def vois_showChange(self, flag):
        if self.updatePageEnabled:
            self.main.vois_show = flag
            self.vois_opacity.slider.disabled = not self.main.vois_show
            self.updatePreview()
        
        
    # Change vois opacity
    def vois_opacityChange(self, opacity):
        if self.updatePageEnabled:
            self.main.vois_opacity = opacity / 100.0
            self.updatePreview()

        
    # Change credits text
    def creditsChange(self, *args):
        if self.updatePageEnabled:
            if self.tfcredits.v_model is None: name = ''
            else:                              name = self.tfcredits.v_model
            self.main.credits = name
            self.updatePreview()

    def creditsClear(self, *args):
        if self.updatePageEnabled:
            self.main.credits = ''
            self.updatePreview()
        
        
    # Selection of the credits image to load from the local machine
    def creditslogo_image_loaded(self, imageurl):
        if self.updatePageEnabled:
            self.main.creditslogo_url = imageurl
            self.updatePreview()

    # Click on the button to open the dialog to select the the credits image
    def creditslogo_image_load(self, *args):
        self.upload.title = 'Select image for the credits image'
        self.upload.onOK  = self.creditslogo_image_loaded
        self.upload.show()

        
    # Change disclaimer text
    def disclaimerChange(self, *args):
        if self.updatePageEnabled:
            if self.tfdisclaimer.v_model is None: name = ''
            else:                                 name = self.tfdisclaimer.v_model
            self.main.disclaimer = name
            self.updatePreview()

    def disclaimerClear(self, *args):
        if self.updatePageEnabled:
            self.main.disclaimer = ''
            self.updatePreview()


    # creditbox_widthpercent   
    def on_creditbox_widthpercent(self, value):
        if self.updatePageEnabled:
            self.main.creditbox_widthpercent = int(value)
            self.updatePreview()

    # creditbox_heightpercent
    def on_creditbox_heightpercent(self, value):
        if self.updatePageEnabled:
            self.main.creditbox_heightpercent = int(value)
            self.updatePreview()
        
        
    # creditbox_toppercent
    def on_creditbox_toppercent(self, value):
        if self.updatePageEnabled:
            self.main.creditbox_toppercent = int(value)
            self.updatePreview()
        
        
    # creditbox_opacity
    def on_creditbox_opacity(self, value):
        if self.updatePageEnabled:
            self.main.creditbox_opacity = value/100.0
            self.updatePreview()
        

    # Add a new button
    def buttonNew(self):
        eb = EditButton(self.output, index=len(self.main.buttons), newButton=True, onOK=self.AddNewButton)
        return None
    
    def AddNewButton(self, b):
        self.blist.doAddItem(b)
        self.updatePreview()
        
        
    # Display a button
    def buttonDisplay(self, item, index):
        
        def UpdateButton(b):
            self.main.buttons[b['index']] = b
            self.blist.items = self.main.buttons
            self.updatePreview()
            
        def onclick(*args):
            eb = EditButton(self.output, index=item['index'], title=item['title'], subtitle=item['subtitle'], tooltip=item['tooltip'], image=item['image'], onclick=item['onclick'], argument=item['argument'], newButton=False, onOK=UpdateButton)
        
        self.AssignOrderToButtons()
        lab = PageConfigurator.label(item['title'], class_='pa-0 ma-0 ml-2 mb-2', color='black')
        lab.on_event('click', onclick)
        return [lab]
        
        
    # Added or removed a button
    def buttonsUpdate(self, *args):
        if self.updatePageEnabled:
            self.updatePreview()
        
        
    # Called at each order change oand each remove of a button
    def AssignOrderToButtons(self):
        i = 0
        for b in self.main.buttons:
            b['index'] = i
            i += 1
        
        
#####################################################################################################################################################
# Create a New button or Edit info on a button
#####################################################################################################################################################
class EditButton():
    
    def __init__(self, output, index, title='', subtitle='', tooltip='', image='', onclick=None, argument=None, onOK=None, newButton=True):
        
        self.onOK = onOK
        self.upload = UploadImage.UploadImage(output, width=620)

        self.index = index
        
        self.image = image

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
                       'argument': self.arg.v_model,
                       'index':    self.index}
        
        if self.onOK is not None:
            self.onOK(self.button)
        
        
        
#####################################################################################################################################################
# Images
#####################################################################################################################################################
        
pageImage = '''data:image/png;base64,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'''

mainImage = '''data:image/png;base64,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'''
        