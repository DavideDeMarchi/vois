"""Interactive page configurator"""
# Author(s): Davide.De-Marchi@ec.europa.eu
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
from ipywidgets import widgets
import ipyvuetify as v
import json

# Vois imports
from vois import colors, download
from vois.vuetify import settings, toggle, ColorPicker, sliderFloat, UploadImage, UploadJson, Button, switch, tooltip, iconButton, dialogGeneric
from vois.templates import template1panel, template2panels, template3panels


# Change style of a label
def labelchange(lab, size=14, weight=400, color=settings.color_first, width=None):
    if width is None:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s;'%(size,weight,color)
    else:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s; width: %dpx'%(size,weight,color,int(width))
    
# Creation of a label
def label(text, class_='pa-0 ma-0 mt-1 mr-3', size=14, weight=400, color=settings.color_first, width=None):
    lab = v.Html(tag='div', children=[text], class_=class_)
    labelchange(lab, size, weight, color, width)
    return lab

    
#####################################################################################################################################################
# Interactive page configurator widget
#####################################################################################################################################################
class PageConfigurator(v.Html):

    # Initialization
    def __init__(self, output, **kwargs):

        super().__init__(**kwargs)

        self.debug = widgets.Output()
        
        # Default state
        self.reset_state = {
            'appname':           'My app',
            'title':             'My page',
            'titlecolor':        '#0d856d',
            'titledark':         True,
            'titleheight':       54,
            'titleimageurl':     '',
            'footercolor':       '#a0dcd0',
            'footerdark':        False,
            'footerheight':      30,
            'copyrighttext':     'European Commission - Joint Research Centre',
            'show_back':         True,
            'left_back':         True,
            'show_help':         True,
            'show_credits':      True,
            'logoappurl':        'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/BDAP_Logo1024transparent.png',
            'logocreditsurl':    'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/EC-JRC-logo_horizontal_EN_neg_transparent-background.png',
            'logowidth':         40,
            'creditswidth':      120,
            'transition':        'dialog-bottom-transition',
        
            # Custom properties
            'panelsvalue':       0,
            'titledarkvalue':    2,
            'footerlinkedvalue': 0,
            'footerdarkvalue':   2
        }
        
        
        
        self.output = output
        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')

        self.card = v.Card(flat=True, width=template1panel.LEFT_WIDTH, min_width=template1panel.LEFT_WIDTH, max_width=template1panel.LEFT_WIDTH,
                           height='400px', class_='pa-2 pt-4 ma-0', style_='overflow: auto;')

        # Widgets
        self.labelwidth   = 110
        self.togglewidth  = 50
        self.paddingrow   = 1
        self.biglabelsize = 15
        
        self.appname   = v.TextField(label='Application name:', autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.pagetitle = v.TextField(label='Page title:',       autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.buttOpen  = iconButton.iconButton(icon='mdi-folder-open',  onclick=self.onOpen,  tooltip='Load state from file', large=True)
        self.buttSave  = iconButton.iconButton(icon='mdi-content-save', onclick=self.onSave,  tooltip='Save current state to file', large=True)
        self.buttReset = iconButton.iconButton(icon='mdi-backspace',    onclick=self.onReset, tooltip='Reset page to default state', large=True)
        
        self.cardappname = v.Card(flat=True, width=template1panel.LEFT_WIDTH, max_width=template1panel.LEFT_WIDTH-80,
                                  children=[widgets.HBox([self.appname, self.buttOpen.draw(), self.buttSave.draw(), self.buttReset.draw()])])
        
        self.appname.on_event(  'change',      self.appnameChange)
        self.appname.on_event(  'click:clear', self.appnameClear)
        self.pagetitle.on_event('change',      self.pagetitleChange)
        self.pagetitle.on_event('click:clear', self.pagetitleClear)
        
        
        self.panelsLabel  = label('Page format: ', size=self.biglabelsize, weight=500, width=self.labelwidth)
        self.togglePanels = toggle.toggle(self.reset_state['panelsvalue'],
                                          ['1', '2', '3'],
                                          tooltips=['Page with 1 left panel', 'Page with 2 panels: left and bottom', 'Page with 3 panels: left, bottom and right'],
                                          dark=True, onchange=self.onSelectedTemplate, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)

        
        self.titlecolor  = ColorPicker(color=settings.color_first,  width=50, height=30, rounded=False, on_change=self.titlecolorChange,  offset_x=True, offset_y=False)        
        self.footercolor = ColorPicker(color=settings.color_second, width=50, height=30, rounded=False, on_change=self.footercolorChange, offset_x=True, offset_y=False)        
        
        self.footerlinked = toggle.toggle(self.reset_state['footerlinkedvalue'], ['', '', '', ''], dark=True, icons=['mdi-link-off', 'mdi-link-variant', 'mdi-link-variant-minus', 'mdi-link-variant-plus'], outlined=False,
                                          tooltips=['Free selection of footer color', 'Footer color is the complementary of the title color',
                                                    'Footer color is a darker version of the title color', 'Footer color is a lighter version of the title color'],
                                          onchange=self.footerlinkedChange, row=True, width=self.togglewidth-20, height=30, justify='start', paddingrow=self.paddingrow, tile=True)
        
        self.titledark = toggle.toggle(self.reset_state['titledarkvalue'], ['', '', ''], dark=True, icons=['mdi-alpha-w-box-outline', 'mdi-alpha-b-box-outline', 'mdi-auto-fix'],
                                       tooltips=['Display text in white color on the title bar', 'Display text in black color on the title bar', 'Automatically select text color for the title bar'],
                                       onchange=self.titledarkChange, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)

        self.footerdark = toggle.toggle(self.reset_state['footerdarkvalue'], ['', '', ''], dark=True, icons=['mdi-alpha-w-box-outline', 'mdi-alpha-b-box-outline', 'mdi-auto-fix'],
                                        tooltips=['Display text in white color on the footer bar', 'Display text in black color on the footer bar', 'Automatically select text color for the footer bar'],
                                        onchange=self.footerdarkChange, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)
        
        self.titleheight = sliderFloat.sliderFloat(self.reset_state['titleheight'], text='Title bar height:', minvalue=20.0, maxvalue=180.0, maxint=160, showpercentage=False, decimals=0,
                                                   labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.titleheightChange)
        
        self.footerheight = sliderFloat.sliderFloat(self.reset_state['footerheight'], text='Footer bar height:', minvalue=16.0, maxvalue=80.0, maxint=64, showpercentage=False, decimals=0,
                                                    labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.footerheightChange)
        
        self.upload = UploadImage.UploadImage(self.output, width=620)
        
        self.titleimageurl  = Button('Select background image for the title bar', color_selected=settings.color_first, dark=settings.dark_mode, 
                                     text_weight=450, on_click=self.titleimageurlClick, width=template1panel.LEFT_WIDTH-10, height=40,
                                     tooltip='Click to select an image to use as background on the title bar', selected=True, rounded=False)

        self.logoappurl     = Button('Select image for the application logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                     text_weight=450, on_click=self.logoappurlClick, width=template1panel.LEFT_WIDTH-10, height=40,
                                     tooltip='Click to select an image to use as application logo on the left side of the title bar', selected=True, rounded=False)
        
        self.logowidth = sliderFloat.sliderFloat(self.reset_state['logowidth'], text='Application logo width:', minvalue=20.0, maxvalue=200.0, maxint=180, showpercentage=False, decimals=0,
                                                 labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.logowidthChange)
        
        self.logocreditsurl = Button('Select image for the credits logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                     text_weight=450, on_click=self.logocreditsurlClick, width=template1panel.LEFT_WIDTH-10, height=40,
                                     tooltip='Click to select an image to use as credits logo on the right side of the title bar', selected=True, rounded=False)
        
        self.creditswidth = sliderFloat.sliderFloat(self.reset_state['creditswidth'], text='Credits logo width:', minvalue=20.0, maxvalue=300.0, maxint=280, showpercentage=False, decimals=0,
                                                 labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.creditswidthChange)

        self.show_back    = switch.switch(self.reset_state['show_back'],    'Show Back button',        inset=True, dense=True, onchange=self.onshow_backChange)
        self.left_back    = switch.switch(self.reset_state['left_back'],    'Back button on the Left', inset=True, dense=True, onchange=self.onleft_backChange)
        self.show_help    = switch.switch(self.reset_state['show_help'],    'Show Help button',        inset=True, dense=True, onchange=self.onshow_helpChange)
        self.show_credits = switch.switch(self.reset_state['show_credits'], 'Show Credits logo',       inset=True, dense=True, onchange=self.onshow_creditsChange)
        
        self.copyrighttext = v.TextField(label='Copyright text:', autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.copyrighttext.on_event('change',      self.copyrighttextChange)
        self.copyrighttext.on_event('click:clear', self.copyrighttextClear)
        
        self.card.children = [widgets.VBox([
                                 self.cardappname,
                                 self.pagetitle,
                                 self.spacerY,
                                 widgets.HBox([self.panelsLabel, self.togglePanels.draw()]),
                                 self.spacerY,
                                 self.spacerY,
                                 widgets.HBox([label('Title bar color:',  color='black', width=self.labelwidth), self.titlecolor, self.spacerX, label('Link:', color='black', width=30), self.footerlinked.draw()]),
                                 self.spacerY,
                                 widgets.HBox([label('Footer bar color:', color='black', width=self.labelwidth), self.footercolor]),
                                 self.spacerY,
                                 widgets.HBox([label('Title bar text:',   color='black', width=self.labelwidth), self.titledark.draw()]),
                                 self.spacerY,
                                 widgets.HBox([label('Footer bar text:',  color='black', width=self.labelwidth), self.footerdark.draw()]),
                                 self.spacerY,
                                 self.titleheight.draw(),
                                 self.spacerY,
                                 self.footerheight.draw(),
                                 self.spacerY,
                                 self.titleimageurl,
                                 self.spacerY,
                                 self.logoappurl,
                                 self.logowidth.draw(),
                                 self.spacerY,
                                 self.logocreditsurl,
                                 self.creditswidth.draw(),
                                 self.spacerY,
                                 widgets.HBox([tooltip.tooltip('Add a back button in the title bar to close the page',self.show_back.draw()),
                                               tooltip.tooltip('Position the back button on the left side of the title bar',self.left_back.draw())]),
                                 widgets.HBox([tooltip.tooltip('Add a help button in the title bar',self.show_help.draw()),
                                               tooltip.tooltip('Display credits logo on the right side of the title bar',self.show_credits.draw())]),
                                 self.spacerY,
                                 self.copyrighttext,
                                ])
                             ]
        
        # Set v.Html members
        self.tag = 'div'
        self.children = [self.card]
        
        # Initial page
        self.saveFilename = None
        self.page = None
        self.onSelectedTemplate(self.reset_state['panelsvalue'])
        
        # Set the initial state
        self.page.state = self.reset_state
        
        # Initialise widgets
        self.appname.v_model       = self.page.appname
        self.pagetitle.v_model     = self.page.title
        self.copyrighttext.v_model = self.page.copyrighttext
        
        
        

    # Load state from file
    def onOpen(self):
        uj = UploadJson.UploadJson(self.output, onOK=self.onSelectedState, required_attributes=['appname', 'title'], attributes_width=80,
                                   color=self.page.titlecolor, dark=self.page.titledark)
        uj.show()
        
    # Called when the UploadJson dialo-box is closed with the OK button
    def onSelectedState(self, state):

        with self.debug:
            
            # Set the page state (does a refresh if the page is open)
            self.page.state = state
        
            # Set the state of the confuguration widgets
            self.togglePanels.value    = state['panelsvalue']
            self.appname.v_model       = self.page.appname
            self.pagetitle.v_model     = self.page.title
            self.titlecolor.color      = self.page.titlecolor
            self.titledark.value       = state['titledarkvalue']
            self.titleheight.value     = self.page.titleheight
            self.footercolor.color     = self.page.footercolor
            self.footerlinked.value    = state['footerlinkedvalue']
            self.footerdark.value      = state['footerdarkvalue']
            self.footerheight.value    = self.page.footerheight
            self.show_back.value       = self.page.show_back
            self.left_back.value       = self.page.left_back
            self.show_help.value       = self.page.show_help
            self.show_credits.value    = self.page.show_credits
            self.logowidth.value       = self.page.logowidth
            self.creditswidth.value    = self.page.creditswidth
            self.copyrighttext.v_model = self.page.copyrighttext
        
        
    # Save current state to file
    def onSave(self):
        
        self.saveFilename = v.TextField(label='File name:', autofocus=True, v_model=self.page.appname + '_' + self.page.title, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 ml-3 mt-3 mr-3")

        dlg = dialogGeneric.dialogGeneric(title='Save and download current state...' , on_ok=self.onDoSave, 
                                          text='   ', color=self.page.titlecolor, dark=self.page.titledark,
                                          titleheight=40, width=600,
                                          show=True, addclosebuttons=True, addokcancelbuttons=True,
                                          fullscreen=False, content=[self.saveFilename], output=self.output)
        
    
    # Effective save and download of the current state
    def onDoSave(self):
        
        filename = self.saveFilename.v_model
        if filename[-5:] != '.json':
            filename += '.json'
        
        # Read the state from the page
        state = self.page.state
    
        # Add dditional states from the PageCOnfigurator
        state['panelsvalue']       = self.togglePanels.value
        state['titledarkvalue']    = self.titledark.value
        state['footerlinkedvalue'] = self.footerlinked.value
        state['footerdarkvalue']   = self.footerdark.value
    
        # Convert to string and download
        txt = json.dumps(state)
        download.downloadText(txt, fileName=filename)
            
            
    # Reset page to initial state
    def onReset(self):
        self.onSelectedState(self.reset_state)
            
            
    # Forced close
    def on_force_close(self, *args):
        self.output.clear_output()

        
    # Selection of 1, 2 or 3 panels template
    def onSelectedTemplate(self, index):

        # Default state (back button on the left and JEODPP logo as application logo
        statusdict = {
            'left_back'  : True,
            'logoappurl' : 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/BDAP_Logo1024transparent.png'
        }
        
        # Read the state and close the current page
        if self.page is not None:
            statusdict = self.page.state
            self.page.close()

        # Create the instance of the page with the requested number of panels
        if index == 0:
            self.page = template1panel.template1panel(self.output)
        elif index == 1:
            self.page = template2panels.template2panels(self.output)
        else:
            self.page = template3panels.template3panels(self.output)
            
        self.page.customButtonAdd('mdi-delete', 'Click here to force page closing', self.on_force_close)
            
        # Create the page widgets and display the PageConfigurator in the left panel
        self.page.create()
        self.page.cardLeft.children = [self]

        # Set the state
        self.page.state = statusdict

        self.page.toggleBasemap.dark            = self.page.titledark
        self.page.toggleBasemap.colorselected   = self.page.titlecolor
        self.page.toggleBasemap.colorunselected = self.page.footercolor
        
        self.titleimageurl.color_selected  = self.page.titlecolor
        self.titleimageurl.dark            = self.page.titledark
        
        self.logoappurl.color_selected     = self.page.titlecolor
        self.logoappurl.dark               = self.page.titledark

        self.logocreditsurl.color_selected = self.page.titlecolor
        self.logocreditsurl.dark           = self.page.titledark
        
        # Open the page with minimal transition
        self.page.transition = 'dialog-top-transition'
        self.page.open()
        if 'transition' in statusdict:
            self.page.transition = statusdict['transition']
        else:
            self.page.transition = 'dialog-bottom-transition'

        # Dimension the left card
        self.card.height = self.card.min_height = self.card.max_height = self.page.height

        
    # Change of the titlecolor property
    def titlecolorChange(self):
        color = self.titlecolor.color

        # page color
        self.page.titlecolor = color
        
        # widgets color
        self.appname.color                    = color
        self.pagetitle.color                  = color
        self.buttOpen.color                   = color
        self.buttSave.color                   = color
        self.buttReset.color                  = color
        self.page.toggleBasemap.colorselected = color
        self.togglePanels.colorselected       = color
        self.titledark.colorselected          = color
        self.footerdark.colorselected         = color
        self.footerlinked.colorselected       = color
        self.titleheight.slider.color         = color
        self.footerheight.slider.color        = color
        self.titleimageurl.b.color            = color
        self.logoappurl.b.color               = color
        self.logocreditsurl.b.color           = color
        self.logowidth.slider.color           = color
        self.creditswidth.slider.color        = color
        self.copyrighttext.color              = color
        self.show_back.switch.color           = color
        self.left_back.switch.color           = color
        self.show_help.switch.color           = color
        self.show_credits.switch.color        = color
        self.titledarkChange(self.titledark.value)
                
        # labels color
        labelchange(self.panelsLabel, size=self.biglabelsize, weight=500, color=color, width=self.labelwidth)
        
        # Auto calculate footer color
        if self.footerlinked.index == 1:     # complementary
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            complementary = colors.complementaryColor(colortuple)
            self.footercolor.color = colors.rgb2hex(complementary)

        elif self.footerlinked.index == 2:   # monochrome darker
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            monochrome = colors.monochromaticColor(colortuple, -0.3)
            self.footercolor.color = colors.rgb2hex(monochrome)

        elif self.footerlinked.index == 3:   # monochrome lighter
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            monochrome = colors.monochromaticColor(colortuple, 0.3)
            self.footercolor.color = colors.rgb2hex(monochrome)
            
        
    # Change of the footercolor property
    def footercolorChange(self):
        color = self.footercolor.color
        
        # page color
        self.page.footercolor = color

        # widgets color
        self.page.toggleBasemap.colorunselected = color
        self.togglePanels.colorunselected       = color
        self.titledark.colorunselected          = color
        self.footerdark.colorunselected         = color
        self.footerlinked.colorunselected       = color
        self.footerdarkChange(self.footerdark.value)
                
        
    # Change of the titledark property
    def titledarkChange(self, index):

        # White text color
        if index == 0:
            flag = True

        # Black text color
        elif index == 1:
            flag = False
        
        # Auto color depending on title bar color
        else:
            color = self.titlecolor.color
            colortuple = colors.string2rgb(color)
            if colors.isColorDark(colortuple):
                flag = True
            else:
                flag = False

        self.page.titledark          = flag
        self.togglePanels.dark       = flag
        self.titledark.dark          = flag
        self.footerdark.dark         = flag
        self.footerlinked.dark       = flag
        self.titleimageurl.dark      = flag
        self.logoappurl.dark         = flag
        self.logocreditsurl.dark     = flag
        self.page.toggleBasemap.dark = flag
        self.footercolor.dark_text   = flag
                
            
    # Change of the footerdark property
    def footerdarkChange(self, index):

        # White text color
        if index == 0:
            self.page.footerdark = True
        
        # Black text color
        elif index == 1:
            self.page.footerdark = False
        
        # Auto color depending on title bar color
        else:
            color = self.footercolor.color
            colortuple = colors.string2rgb(color)
            if colors.isColorDark(colortuple):
                self.page.footerdark = True
            else:
                self.page.footerdark = False
                
                
    # Change of the footerlinked toggle
    def footerlinkedChange(self, index):
        self.footercolor.disabled = index > 0
        self.titlecolorChange()
        
        
    # Change of the title bar height
    def titleheightChange(self, height):
        self.page.titleheight = int(height)
    
    
    # Change of the footer bar height
    def footerheightChange(self, height):
        self.page.footerheight = int(height)
        
        
    # Change application name
    def appnameChange(self, *args):
        if self.appname.v_model is None: name = ''
        else:                            name = self.appname.v_model
        self.page.appname = name

    def appnameClear(self, *args):
        self.page.appname = ''
            
    # Change page title
    def pagetitleChange(self, *args):
        if self.pagetitle.v_model is None: name = ''
        else:                              name = self.pagetitle.v_model
        self.page.title = name

    def pagetitleClear(self, *args):
        self.page.title = ''
            
            
    # Click on the button to open the dialog to select the title bar image
    def titleimageurlClick(self, *args):
        self.upload.title   = 'Select background image for the title bar'
        self.upload.onOK    = self.titleimageurlSelected
        self.upload.color   = self.titlecolor.color
        self.upload.u.color = self.titlecolor.color
        self.upload.dark    = self.page.titledark
        self.upload.show()
        
    # Selection of the title bar image
    def titleimageurlSelected(self, imageurl):
        self.page.titleimageurl = imageurl
        
        
    # Click on the button to open the dialog to select the logoappurl
    def logoappurlClick(self, *args):
        self.upload.title   = 'Select image for the application logo'
        self.upload.onOK    = self.logoappurlSelected
        self.upload.color   = self.titlecolor.color
        self.upload.u.color = self.titlecolor.color
        self.upload.dark    = self.page.titledark
        self.upload.show()
        
    # Selection of the logoappurl
    def logoappurlSelected(self, imageurl):
        self.page.logoappurl = imageurl
        
        
    # Click on the button to open the dialog to select the logocreditsurl
    def logocreditsurlClick(self, *args):
        self.upload.title   = 'Select image for the credits logo'
        self.upload.onOK    = self.logocreditsurlSelected
        self.upload.color   = self.titlecolor.color
        self.upload.u.color = self.titlecolor.color
        self.upload.dark    = self.page.titledark
        self.upload.show()
        
    # Selection of the logocreditsurl
    def logocreditsurlSelected(self, imageurl):
        self.page.logocreditsurl = imageurl
        
    # Change logo width
    def logowidthChange(self, width):
        self.page.logowidth = int(width)
    
    # Change credits width
    def creditswidthChange(self, width):
        self.page.creditswidth = int(width)
        

    # Change copyright text
    def copyrighttextChange(self, *args):
        if self.copyrighttext.v_model is None: name = ''
        else:                                  name = self.copyrighttext.v_model
        self.page.copyrighttext = name

    def copyrighttextClear(self, *args):
        self.page.copyrighttext = ''
        
    
    # show_back change
    def onshow_backChange(self, flag):
        self.page.show_back = flag

    # left_back change
    def onleft_backChange(self, flag):
        self.page.left_back = flag

    # show_help change
    def onshow_helpChange(self, flag):
        self.page.show_help = flag

    # show_credits change
    def onshow_creditsChange(self, flag):
        self.page.show_credits = flag
        