from vois.vuetify import settings
settings.color_first    = '#0D856D'
settings.color_second   = '#A0DCD0'
settings.button_rounded = False
settings.dark_mode      = True

from ipywidgets import widgets, HTML, Layout
from IPython.display import display
import ipyvuetify as v
import json

from vois import cssUtils
from vois.vuetify import switch, Button, dialogMessage
from vois.templates import template1panel


output = widgets.Output(layout=Layout(width='0px', height='0px'))
display(output)

cssUtils.allSettings(output)
cssUtils.switchFontSize(output,14)

# Derived page class
class samplePage(template1panel.template1panel):
    
    # Initialisation
    def __init__(self, output, **kwargs):
        super().__init__(output=output, on_logoapp=self.on_logoapp, on_help=self.on_help, on_credits=self.on_credits,
                         leftWidth=400,
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
    
        # Save reference to content items (map, charts, etc.)
        self.map1 = self.content.card1children
        self.chart2 = self.content.card2children
        self.svg3 = self.content.card3children
        

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


# Create an instance of mypage
p = samplePage(output)
p.create()

# Read the state of the page from the .json file
with open('samplePage.json') as f:
    state = json.load(f)
    p.state = state
    if 'content' in state:
        p.content.state = state['content']

# Change the content here:
    
# Open the page
p.open()