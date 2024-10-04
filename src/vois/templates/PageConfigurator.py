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
from vois.vuetify import settings, toggle, ColorPicker, sliderFloat, UploadImage, UploadJson, Button, switch, tooltip, iconButton, dialogGeneric, selectSingle, tabs
from vois.templates import template1panel, template2panels, template3panels
from vois import cssUtils


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
            'footerdarkvalue':   2,
            'button_rounded':    False,
            'transitionvalue':   'Bottom'
        }
        
        
        
        self.output = output
        self.spacerX = v.Html(tag='div', style_='width: 10px; height: 0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 6px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')

        self.card = v.Card(flat=True, width=template1panel.LEFT_WIDTH, min_width=template1panel.LEFT_WIDTH, max_width=template1panel.LEFT_WIDTH,
                           height='400px', class_='pa-2 pt-4 ma-0', style_='overflow: auto;')

        # Widgets
        self.labelwidth   = 96
        self.togglewidth  = 46
        self.paddingrow   = 1
        self.biglabelsize = 15
        
        self.appname   = v.TextField(label='Application name:', autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3")
        self.buttOpen  = iconButton.iconButton(icon='mdi-folder-open',  onclick=self.onOpen,  tooltip='Load state from file',                      margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttSave  = iconButton.iconButton(icon='mdi-content-save', onclick=self.onSave,  tooltip='Save current state to file',                margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttCode  = iconButton.iconButton(icon='mdi-file-code',    onclick=self.onCode,  tooltip='Generate and download page code in Python', margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        self.buttReset = iconButton.iconButton(icon='mdi-backspace',    onclick=self.onReset, tooltip='Reset page to default state',               margins='pa-0 ma-0 mt-3 mr-2', color=settings.color_first)
        
        self.cardappname = v.Card(flat=True, width=template1panel.LEFT_WIDTH-46, max_width=template1panel.LEFT_WIDTH-46,
                                  children=[widgets.HBox([self.appname, self.buttOpen.draw(), self.buttSave.draw(), self.buttCode.draw(), self.buttReset.draw()])])
        
        self.pagetitle  = v.TextField(label='Page title:', autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3 mr-3", style_='width: 246px; min_width: 246px;')
        self.transition = selectSingle.selectSingle('Open animation:', ['None', 'Dialog', 'Bottom'], selection='Bottom', clearable=False, width=120, onchange=self.transitionChange)
        
        self.cardpagetitle = v.Card(flat=True, width=template1panel.LEFT_WIDTH, max_width=template1panel.LEFT_WIDTH,
                                    children=[widgets.HBox([self.pagetitle, self.transition.draw()])])
        
        self.appname.on_event(  'change',      self.appnameChange)
        self.appname.on_event(  'click:clear', self.appnameClear)
        self.pagetitle.on_event('change',      self.pagetitleChange)
        self.pagetitle.on_event('click:clear', self.pagetitleClear)
        
        
        self.panelsLabel  = label('Page format: ', size=self.biglabelsize, weight=500, width=self.labelwidth)
        self.togglePanels = toggle.toggle(self.reset_state['panelsvalue'],
                                          ['1', '2', '3'],
                                          tooltips=['Page with 1 left panel', 'Page with 2 panels: left and bottom', 'Page with 3 panels: left, bottom and right'],
                                          dark=True, onchange=self.onSelectedTemplate, row=True, width=self.togglewidth, justify='start', paddingrow=self.paddingrow, tile=True)

        
        self.titlecolor  = ColorPicker(dark=False, color=settings.color_first,  width=50, height=30, rounded=False, on_change=self.titlecolorChange,  offset_x=True, offset_y=False, color_theory_popup=True)
        self.footercolor = ColorPicker(dark=False, color=settings.color_second, width=50, height=30, rounded=False, on_change=self.footercolorChange, offset_x=True, offset_y=False, color_theory_popup=True)
        
        self.rounded = switch.switch(self.reset_state['button_rounded'], 'Rounded buttons', inset=True, dense=True, onchange=self.onroundedChange)
        
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
                                     text_weight=450, on_click=self.titleimageurlClick, width=template1panel.LEFT_WIDTH-16, height=40,
                                     tooltip='Click to select an image to use as background on the title bar', selected=True, rounded=self.reset_state['button_rounded'])

        self.logoappurl     = Button('Select image for the application logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                     text_weight=450, on_click=self.logoappurlClick, width=template1panel.LEFT_WIDTH-16, height=40,
                                     tooltip='Click to select an image to use as application logo on the left side of the title bar', selected=True, rounded=self.reset_state['button_rounded'])
        
        self.logowidth = sliderFloat.sliderFloat(self.reset_state['logowidth'], text='Application logo width:', minvalue=20.0, maxvalue=200.0, maxint=180, showpercentage=False, decimals=0,
                                                 labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.logowidthChange)
        
        self.logocreditsurl = Button('Select image for the credits logo', color_selected=settings.color_first, dark=settings.dark_mode, 
                                     text_weight=450, on_click=self.logocreditsurlClick, width=template1panel.LEFT_WIDTH-16, height=40,
                                     tooltip='Click to select an image to use as credits logo on the right side of the title bar', selected=True, rounded=self.reset_state['button_rounded'])
        
        self.creditswidth = sliderFloat.sliderFloat(self.reset_state['creditswidth'], text='Credits logo width:', minvalue=20.0, maxvalue=300.0, maxint=280, showpercentage=False, decimals=0,
                                                 labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.creditswidthChange)

        self.show_back    = switch.switch(self.reset_state['show_back'],    'Show Back button',        inset=True, dense=True, onchange=self.onshow_backChange)
        self.left_back    = switch.switch(self.reset_state['left_back'],    'Back button on the Left', inset=True, dense=True, onchange=self.onleft_backChange)
        self.show_help    = switch.switch(self.reset_state['show_help'],    'Show Help button',        inset=True, dense=True, onchange=self.onshow_helpChange)
        self.show_credits = switch.switch(self.reset_state['show_credits'], 'Show Credits logo',       inset=True, dense=True, onchange=self.onshow_creditsChange)
        
        self.copyrighttext = v.TextField(label='Copyright text:', autofocus=False, v_model=None, dense=False, color=settings.color_first, clearable=True, class_="pa-0 ma-0 mt-3")
        self.copyrighttext.on_event('change',      self.copyrighttextChange)
        self.copyrighttext.on_event('click:clear', self.copyrighttextClear)
        
        self.card_appearance = v.Card(flat=True)
        self.card_content    = v.Card(flat=True)
        self.tabsView = tabs.tabs(0, ['Appearance', 'Content'], contents=[self.card_appearance, self.card_content], dark=False, onchange=None, row=True)
        
        self.card_appearance.children = [widgets.VBox([
                                 self.spacerY,
                                 self.spacerY,
                                 widgets.HBox([label('Title bar color:',  color='black', width=self.labelwidth), self.titlecolor, self.titlecolor.ctpopup.draw(), self.spacerX, label('Link:', color='black', width=30), self.footerlinked.draw()]),
                                 self.spacerY,
                                 widgets.HBox([label('Footer color:',     color='black', width=self.labelwidth), self.footercolor, self.footercolor.ctpopup.draw(), self.spacerX, self.rounded.draw()]),
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
        
        self.card.children = [widgets.VBox([
                                 self.cardappname,
                                 self.cardpagetitle,
                                 self.spacerY,
                                 widgets.HBox([self.panelsLabel, self.togglePanels.draw()]),
                                 self.spacerY,
                                 self.tabsView.draw()
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
        
        # Set the content initial state
        self.page.content.state = self.page.content.reset_state
        
        # Initialise widgets
        self.appname.v_model       = self.page.appname
        self.pagetitle.v_model     = self.page.title
        self.copyrighttext.v_model = self.page.copyrighttext
        
        
    # Load state from file
    def onOpen(self):
        uj = UploadJson.UploadJson(self.output, onOK=self.onSelectedState, required_attributes=['appname', 'title'], attributes_width=80,
                                   color=self.page.titlecolor, dark=self.page.titledark)
        uj.show()
        
        
    # Called when the UploadJson dialog-box is closed with the OK button
    def onSelectedState(self, state):

        with self.debug:
            
            # Close to avoid many visual updates
            self.page.close()
            
            # Set the page state (does a refresh if the page is open)
            self.page.state = state
            
            # Set the content state
            if 'content' in state:
                self.page.content.state = state['content']
            else:
                self.page.content.reset()

            #print('BEFORE:')
            #print('state.footercolor', state['footercolor'])
            #print('page.footercolor ', self.page.footercolor)
            #print('footercolor.color', self.footercolor.color)
            
            # Set the state of the confuguration widgets
            self.togglePanels.value    = state['panelsvalue']
            self.appname.v_model       = self.page.appname
            self.pagetitle.v_model     = self.page.title
            self.footerlinked.value    = state['footerlinkedvalue']
            self.titledark.value       = state['titledarkvalue']
            self.titleheight.value     = self.page.titleheight
            self.footerdark.value      = state['footerdarkvalue']
            self.footerheight.value    = self.page.footerheight
            self.show_back.value       = self.page.show_back
            self.left_back.value       = self.page.left_back
            self.show_help.value       = self.page.show_help
            self.show_credits.value    = self.page.show_credits
            self.logowidth.value       = self.page.logowidth
            self.creditswidth.value    = self.page.creditswidth
            self.copyrighttext.v_model = self.page.copyrighttext
            self.rounded.value         = state['button_rounded']
            if 'transitionvalue' in state:
                self.transition.value = state['transitionvalue']
            else:
                self.transition.value = 'Bottom'
                
            self.footercolor.color     = state['footercolor']
            self.titlecolor.color      = state['titlecolor']
        
            #print('AFTER:')
            #print('state.footercolor', state['footercolor'])
            #print('page.footercolor ', self.page.footercolor)
            #print('footercolor.color', self.footercolor.color)
            
            # Re-open at the end
            #self.page.open()
            
            
        
    # Save current state to file
    def onSave(self):
        self.saveFilename = v.TextField(label='File name:', autofocus=True, v_model=self.page.appname + '_' + self.page.title, dense=False, color=self.page.titlecolor, clearable=False, class_="pa-0 ma-0 ml-3 mt-3 mr-3")
        dialogGeneric.dialogGeneric(title='Save and download current state...' , on_ok=self.onDoSaveState, 
                                    text='   ', color=self.page.titlecolor, dark=self.page.titledark,
                                    titleheight=40, width=600,
                                    show=True, addclosebuttons=True, addokcancelbuttons=True,
                                    fullscreen=False, content=[self.saveFilename], output=self.output)
        
    
    # Effective save and download of the current state
    def onDoSaveState(self):
        
        filename = self.saveFilename.v_model
        if filename[-5:] != '.json':
            filename += '.json'
        
        # Read the state from the page
        state = self.page.state
    
        # Add additional states from the PageConfigurator
        state['panelsvalue']       = self.togglePanels.value
        state['titledarkvalue']    = self.titledark.value
        state['footerlinkedvalue'] = self.footerlinked.value
        state['footerdarkvalue']   = self.footerdark.value
        state['button_rounded']    = self.rounded.value
        state['trainsitionvalue']  = self.transition.value
        
        # Save content
        state['content'] = self.page.content.state
    
        # Convert to string and download
        txt = json.dumps(state, indent=4)
        download.downloadText(txt, fileName=filename)
            
    
    # Save Python page code
    def onCode(self):
        self.saveFilename = v.TextField(label='Class name:', autofocus=True, v_model=self.page.appname + '_' + self.page.title, dense=False, color=self.page.titlecolor, clearable=False, class_="pa-0 ma-0 ml-3 mt-3 mr-3")
        dialogGeneric.dialogGeneric(title='Save and download Python code...' , on_ok=self.onDoSaveCode, 
                                    text='   ', color=self.page.titlecolor, dark=self.page.titledark,
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
                
            classname = self.saveFilename.v_model
            pythonfile = classname
            pythonfile += '.py'

            notebookfile = classname
            notebookfile += '.ipynb'

            
            # Access to the content items
            access_strings = []
            if len(self.page.content.access1) > 0: access_strings.append(self.page.content.access1)
            if len(self.page.content.access2) > 0: access_strings.append(self.page.content.access2)
            if len(self.page.content.access3) > 0: access_strings.append(self.page.content.access3)
            if len(self.page.content.access4) > 0: access_strings.append(self.page.content.access4)
            access = '\n        '.join(access_strings)

            
            # Selection of the base class
            if self.togglePanels.value == 0:
                baseclass = 'template1panel'
                dimensioning = 'leftWidth=400,'
                otherCreationOverload = ''
            elif self.togglePanels.value == 1:
                baseclass = 'template2panels'
                dimensioning = 'leftWidth=400, bottomHeight=240,'
                otherCreationOverload = '''

    # Create widgets on the Bottom panel
    def createBottom(self):
        super().createBottom()
'''                
            else:
                baseclass = 'template3panels'
                dimensioning = 'leftWidth=400, bottomHeight=240, rightWidth=480,'
                otherCreationOverload = '''

    # Create widgets on the Bottom panel
    def createBottom(self):
        super().createBottom()
    

    # Create widgets on the Right panel
    def createRight(self):
        super().createRight()
'''                

            # Code generation
            txt = '''from vois.vuetify import settings
settings.color_first    = '%s'
settings.color_second   = '%s'
settings.button_rounded = %s
settings.dark_mode      = %s

from ipywidgets import widgets, HTML, Layout
from IPython.display import display
import ipyvuetify as v
import json

from vois import cssUtils
from vois.vuetify import switch, Button, dialogMessage
from vois.templates import %s, Content

Content.dialogWaitEnabled = False

output = widgets.Output(layout=Layout(width='0px', height='0px'))
display(output)

cssUtils.allSettings(output)
cssUtils.switchFontSize(output,14)

# Derived page class
class %s(%s.%s):
    
    # Initialisation
    def __init__(self, output, **kwargs):
        super().__init__(output=output, on_logoapp=self.on_logoapp, on_help=self.on_help, on_credits=self.on_credits,
                         %s
                         **kwargs)

    # Clicked the application logo
    def on_logoapp(self):
        dialogMessage.dialogMessage(title='Info on ' + self.appname, titleheight=36,
                                    text='Text to customise for info on the application<br>Add text here or open a PDF file',
                                    addclosebuttons=True, show=True, width=400, output=self.output)
        
    # Clicked the 'Help' button
    def on_help(self):
        dialogMessage.dialogMessage(title='Help', titleheight=36,
                                    text='Text to customise for the application help<br>Add text here or open a PDF file',
                                    addclosebuttons=True, show=True, width=400, output=self.output)
    
    # Clicked the credits logo
    def on_credits(self):
        dialogMessage.dialogMessage(title='Credits for ' + self.appname, titleheight=36,
                                    text='Text to customise for the credits info<br>Add text here or open a PDF file',
                                    addclosebuttons=True, show=True, width=400, output=self.output)
                                    
                                    
    # Create the content of the Main panel
    def createMain(self):
        super().createMain()


    # Overload the method called when the state changes
    def onStateChanged(self):
    
        # Save reference to content items (maps, charts, etc.)
        %s
        

    # Create sample widgets on the Left panel
    def createLeft(self):
        super().createLeft()

        # Create sample widgets
        spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')
        lab = v.Html(tag='div', children=['Place here your widgets:'], class_='pa-0 ma-0 ml-4 mt-4 mb-3')
        sw  = switch.switch(True, 'Sample switch', inset=True, dense=True, onchange=None)
        b   = Button('Sample button with icon and tooltip', on_click=None, width=360, height=42,
                     tooltip='Tooltip for button', selected=True, icon='mdi-cogs')
        
        # Add widgets to Left card
        self.cardLeft.children = [widgets.VBox([lab, 
                                                sw.draw(), 
                                                spacer,
                                                widgets.HBox([spacer, b])
                                               ])]
%s

# Create an instance of mypage
p = %s(output)
p.create()

# Read the state of the page from the .json file
with open('%s') as f:
    state = json.load(f)
    p.state = state
    if 'content' in state:
        p.content.state = state['content']

# Change the content here:
    
# Open the page
p.open()'''%(self.titlecolor.color, self.footercolor.color, str(self.rounded.value), str(self.page.titledark),
             baseclass, classname, baseclass, baseclass, 
             dimensioning, access, otherCreationOverload, classname, jsonfile)
        
            # Convert to string and download .py file
            download.downloadText(txt, fileName=pythonfile)

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
        self.tabsView.value = 0
        self.onSelectedState(self.reset_state)
            

    # Forced close
    def on_force_close(self, *args):
        self.output.clear_output()    # V.I.!!! removes double draw of popups!!!
        cssUtils.allSettings(self.output)
        cssUtils.switchFontSize(self.output,14)

        
    # Selection of 1, 2 or 3 panels template
    def onSelectedTemplate(self, index):

        with self.debug:
            # Default state (back button on the left and JEODPP logo as application logo
            statusdict = {
                'left_back'  : True,
                'logoappurl' : 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/BDAP_Logo1024transparent.png'
            }

            contentdict = { 'color_first':  settings.color_first,
                            'color_second': settings.color_second,
                            'dark':         settings.dark_mode
            }


            # Read the state and close the current page
            if self.page is not None:
                statusdict  = self.page.state
                contentdict = self.page.content.state
                contentdict['color_first']  = statusdict['titlecolor']
                contentdict['color_second'] = statusdict['footercolor']
                contentdict['color_dark']   = statusdict['titledark']
                del contentdict['width']
                del contentdict['height']
                self.page.close()

            # Create the instance of the page with the requested number of panels
            if index == 0:
                self.page = template1panel.template1panel(self.output, onclose=self.on_force_close)
            elif index == 1:
                self.page = template2panels.template2panels(self.output, onclose=self.on_force_close)
            else:
                self.page = template3panels.template3panels(self.output, onclose=self.on_force_close)

            self.page.customButtonAdd('mdi-delete', 'Click here to force page closing', self.on_force_close)

            # Create the page widgets and display the PageConfigurator in the left panel
            self.page.create()
            self.page.cardLeft.children = [self]

            self.card_content.children = [self.page.configure()]

            # Set the state
            self.page.state         = statusdict
            self.page.content.state = contentdict

            self.page.content.dark         = self.page.titledark
            self.page.content.color_first  = self.page.titlecolor
            self.page.content.color_second = self.page.footercolor

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

        
    # Change the transition mode
    def transitionChange(self):
        if self.transition.value == 'None':
            self.page.transition = 'dialog-top-transition'
        elif self.transition.value == 'Dialog':
            self.page.transition = 'dialog-transition'
        else:
            self.page.transition = 'dialog-bottom-transition'
        

    # Change of the titlecolor property
    def titlecolorChange(self):
        color = self.titlecolor.color

        # page color
        self.page.titlecolor = color
        
        # widgets color
        self.appname.color              = color
        self.pagetitle.color            = color
        self.transition.color           = color
        self.buttOpen.color             = color
        self.buttSave.color             = color
        self.buttCode.color             = color
        self.buttReset.color            = color
        self.page.content.color_first   = color
        self.togglePanels.colorselected = color
        self.titledark.colorselected    = color
        self.footerdark.colorselected   = color
        self.footerlinked.colorselected = color
        self.titleheight.slider.color   = color
        self.footerheight.slider.color  = color
        self.titleimageurl.b.color      = color
        self.logoappurl.b.color         = color
        self.logocreditsurl.b.color     = color
        self.logowidth.slider.color     = color
        self.creditswidth.slider.color  = color
        self.copyrighttext.color        = color
        self.show_back.switch.color     = color
        self.left_back.switch.color     = color
        self.show_help.switch.color     = color
        self.show_credits.switch.color  = color
        self.rounded.switch.color       = color
        self.tabsView.color             = color
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
        self.page.content.color_second     = color
        self.togglePanels.colorunselected  = color
        self.titledark.colorunselected     = color
        self.footerdark.colorunselected    = color
        self.footerlinked.colorunselected  = color
        self.footerdarkChange(self.footerdark.value)
                
            
    # Button rounded flag
    def onroundedChange(self, flag):
        self.titleimageurl.rounded  = flag
        self.logoappurl.rounded     = flag
        self.logocreditsurl.rounded = flag
    
        
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

        self.page.titledark         = flag
        self.togglePanels.dark      = flag
        self.titledark.dark         = flag
        self.footerdark.dark        = flag
        self.footerlinked.dark      = flag
        self.titleimageurl.dark     = flag
        self.logoappurl.dark        = flag
        self.logocreditsurl.dark    = flag
        self.page.content.dark      = flag
        self.footercolor.dark_text  = flag
                
            
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
        