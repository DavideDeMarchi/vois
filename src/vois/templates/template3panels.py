"""Template page with left, bottom and right panels"""
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
from ipywidgets import widgets, HTML, Layout, CallbackDispatcher
import ipyleaflet
from ipyleaflet import SearchControl, ScaleControl, FullScreenControl, WidgetControl
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, toggle, page
from vois.templates import dynamicButton, Content

# Panels dimensioning
LEFT_WIDTH    = 400      # Width  in pixels of the left bar
BOTTOM_HEIGHT = 240      # Height in pixels of the bottom bar
RIGHT_WIDTH   = 480      # Width  in pixels of the right panel

# Name of layers
LAYERNAME_BACKGROUND  = 'Background'
LAYERNAME_LABELS      = 'Labels'


#####################################################################################################################################################
# Template page with left, bottom and right panels
#####################################################################################################################################################
class template3panels(page.page):

    
    # Initialization
    def __init__(self, output, onclose=None, leftWidth=LEFT_WIDTH, bottomHeight=BOTTOM_HEIGHT, rightWidth=RIGHT_WIDTH, **kwargs):
        super().__init__('Demo', 'Geospatial page with left, bottom and right panels', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre', **kwargs)

        # Initialize member variables
        self.init_leftWidth    = self.leftWidth    = leftWidth
        self.init_bottomHeight = self.bottomHeight = bottomHeight
        self.init_rightWidth   = self.rightWidth   = rightWidth

   
    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%settings.color_first
        self.main_width  = 'calc(100vw - %dpx)'%(self.leftWidth + self.rightWidth)
        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft   = v.Card(flat=True, style_=st, outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardBottom = v.Card(flat=True, style_=st + ' border-left-width: 0px; border-top-width: 0px;', outlined=True, width=self.main_width, height=self.bottomHeight, min_height=self.bottomHeight)
        self.cardRight  = v.Card(flat=True, style_=st + ' border-left-width: 0px;', outlined=True, width=self.rightWidth, min_width=self.rightWidth, max_width=self.rightWidth, height=self.height)
        self.cardMain   = v.Card(flat=True, style_=st + ' border-left-width: 0px;', outlined=True, width=self.main_width, min_width=self.main_width, max_width=self.main_width, height=self.main_height)
        
        # DynamicButtons to open/close the left and bottom panels
        self.dynbLeft = dynamicButton.dynamicButton(x1='%dpx'%(self.leftWidth-45), y1='64px', x2='48px', y2='64px', onclick1=self.leftClose, onclick2=self.leftOpen)

        x = 45 + self.rightWidth
        self.dynbBottom = dynamicButton.dynamicButton(x1='calc(100vw - %dpx)'%x, y1='calc(100vh - %dpx)'%(BOTTOM_HEIGHT+35), x2='calc(100vw - %dpx)'%x, y2='calc(100vh - 40px)',
                                                      icon1='mdi-menu-down', icon2='mdi-menu-up', onclick1=self.bottomClose, onclick2=self.bottomOpen)
        
        x = self.rightWidth - 5
        self.dynbRight  = dynamicButton.dynamicButton(x1='calc(100vw - %dpx)'%x, y1='64px', x2='calc(100vw - 100px)', y2='64px', 
                                                      icon1='mdi-menu-right', icon2='mdi-menu-left', onclick1=self.rightClose, onclick2=self.rightOpen)
        
        # Creation of the contents for the panels
        self.createMain()
        self.createLeft()
        self.createBottom()
        self.createRight()
        
        # Compose the panels
        self.card.children = [self.dynbLeft.draw(),
                              self.dynbBottom.draw(),
                              self.dynbRight.draw(),
                              widgets.HBox([
                                  self.cardLeft,
                                  widgets.VBox([
                                      self.cardMain,
                                      self.cardBottom
                                  ]),
                                  self.cardRight
                              ])
                             ]
        
        self.dynbLeft.setpos()
        
        return self.card
    
            
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
        page.page.titlecolor.fset(self, color)   # call super() property setter

        # Set the color of the panels outline!
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%color
        self.cardLeft.style_   = st
        self.cardBottom.style_ = st + ' border-left-width: 0px; border-top-width: 0px;'
        if self.leftWidth == 0:
            self.cardRight.style_  = st + ' border-left-width: 1px;'
        else:
            self.cardRight.style_  = st + ' border-left-width: 0px;'
        self.cardMain.style_ = st + ' border-left-width: 0px;'
        
        # Set the color of the dynamicButton
        self.dynbLeft.color   = color
        self.dynbBottom.color = color
        self.dynbRight.color  = color
        
        # Set the color first
        self.content.color_first = color
        
        
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
        page.page.footercolor.fset(self, color)   # call super() property setter

        # Set the color second
        self.content.color_second = color

                
    @property
    def titleheight(self):
        return self._titleheight
        
    @titleheight.setter
    def titleheight(self, height):
        page.page.titleheight.fset(self, height)   # call super() property setter

        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft.height  = self.height
        self.cardRight.height = self.height
        self.cardMain.height  = self.main_height
        
        self.content.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight)
        
        d = self._titleheight - 54
        newy = '%dpx'%(64+d)
        self.dynbLeft.y1 = self.dynbLeft.y2 = newy
        self.dynbLeft.setpos()
        self.dynbRight.y1 = self.dynbRight.y2 = newy
        self.dynbRight.setpos()
        

    @property
    def footerheight(self):
        return self._footerheight
        
    @footerheight.setter
    def footerheight(self, height):
        page.page.footerheight.fset(self, height)   # call super() property setter

        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft.height  = self.height
        self.cardRight.height = self.height
        self.cardMain.height  = self.main_height
        
        self.content.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight)
        
        d = self._titleheight - 54
        newy = '%dpx'%(64+d)
        self.dynbLeft.y1 = self.dynbLeft.y2 = newy
        self.dynbLeft.setpos()
        self.dynbRight.y1 = self.dynbRight.y2 = newy
        self.dynbRight.setpos()
        
        d = self._footerheight - 30
        self.dynbBottom.y1 = 'calc(100vh - %dpx)'%(BOTTOM_HEIGHT+35+d)
        self.dynbBottom.y2 = 'calc(100vh - %dpx)'%(40+d)
        self.dynbBottom.setpos()
        
        
    # Create the content of the left panel
    def createLeft(self):
        pass
    
    # Create the content of the bottom panel
    def createBottom(self):
        pass
        
    # Create the content of the right panel
    def createRight(self):
        pass
    
    # Create the content of the Main panel
    def createMain(self):

        # Create the content instance
        self.content = Content.Content(output=self.output, width='calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth), height='calc(%s - %fpx)'%(self.height,self.bottomHeight), onStateChanged=self.onStateChanged)
        
        # Display the content inside the main card
        self.cardMain.children = [self.content]
    
    
    # Display the configuration GUI
    def configure(self):
        return self.content.configure()

        
    # Called when the state changes
    def onStateChanged(self):
        pass

    
    #################################################################################################################################################
    # Manage the opening/closing of the dynamic panels (left and bottom)
    #################################################################################################################################################
        
    # Close the left panel
    def leftClose(self):
        self.leftWidth = 0
        self.main_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width   = self.main_width
        self.cardMain.width     = self.main_width
        self.cardMain.min_width = self.main_width
        self.cardMain.max_width = self.main_width
        self.content.width      = self.main_width
        
        self.titlecolor = self._titlecolor  # Set left border to right panel
        

    # Open the left panel
    def leftOpen(self):
        self.leftWidth = self.init_leftWidth
        self.main_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width   = self.main_width
        self.cardMain.width     = self.main_width
        self.cardMain.min_width = self.main_width
        self.cardMain.max_width = self.main_width
        self.content.width      = self.main_width
        
        self.titlecolor = self._titlecolor  # Remove left border to right panel
        

    # Close the bottom panel
    def bottomClose(self):
        self.bottomHeight = 0
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMain.height = self.height
        self.content.height  = self.height
        

    # Open the bottom panel
    def bottomOpen(self):
        self.bottomHeight = self.init_bottomHeight
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMain.height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.content.height  = 'calc(%s - %fpx)'%(self.height,self.bottomHeight)
        

    # Close the right panel
    def rightClose(self):
        self.rightWidth = 0
        self.main_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardRight.width     = self.rightWidth
        self.cardRight.min_width = self.rightWidth
        self.cardRight.max_width = self.rightWidth
        
        self.cardBottom.width   = self.main_width
        self.cardMain.width     = self.main_width
        self.cardMain.min_width = self.main_width
        self.cardMain.max_width = self.main_width
        self.content.width      = self.main_width
        
        x = 'calc(100vw - %dpx)'%(45 + self.rightWidth)
        self.dynbBottom.x1 = x
        self.dynbBottom.x2 = x
        self.dynbBottom.setpos()
        

    # Open the right panel
    def rightOpen(self):
        self.rightWidth = self.init_rightWidth
        self.main_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardRight.width     = self.rightWidth
        self.cardRight.min_width = self.rightWidth
        self.cardRight.max_width = self.rightWidth
        
        self.cardBottom.width   = self.main_width
        self.cardMain.width     = self.main_width
        self.cardMain.width     = self.main_width
        self.cardMain.min_width = self.main_width
        self.cardMain.max_width = self.main_width
        self.content.width      = self.main_width
        
        x = 'calc(100vw - %dpx)'%(45 + self.rightWidth)
        self.dynbBottom.x1 = x
        self.dynbBottom.x2 = x
        self.dynbBottom.setpos()
        
