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
from IPython.display import display
from ipywidgets import widgets, HTML, Layout, CallbackDispatcher
import ipyleaflet
from ipyleaflet import SearchControl, ScaleControl, FullScreenControl, WidgetControl, Popup, Marker
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, toggle, page, iconButton, card

# Local imports
import mapUtils
import dynamicButton

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
    def __init__(self, output, onclose=None, **kwargs):
        super().__init__('Demo', 'Geospatial browse page with left, bottom and right panels', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre')

   
    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Initialize some member variables
        self.leftWidth    = LEFT_WIDTH
        self.bottomHeight = BOTTOM_HEIGHT
        self.rightWidth   = RIGHT_WIDTH
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px;'%settings.color_first
        self.map_width  = 'calc(100vw - %dpx)'%(self.leftWidth + self.rightWidth)
        self.map_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft   = v.Card(flat=True, style_=st, outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardBottom = v.Card(flat=True, style_=st + ' border-left-width: 0px; border-right-width: 0px;', outlined=True, width=self.map_width, height=self.bottomHeight, min_height=self.bottomHeight)
        self.cardRight  = v.Card(flat=True, style_=st, outlined=True, width=self.rightWidth, min_width=self.rightWidth, max_width=self.rightWidth, height=self.height)
        self.cardMap    = v.Card(flat=True, style_=st + ' border-left-width: 0px;', outlined=True, width=self.map_width, min_width=self.map_width, max_width=self.map_width, height=self.map_height)
        
        # DynamicButtons to open/close the left and bottom panels
        self.dynbLeft = dynamicButton.dynamicButton(x1='%dpx'%(self.leftWidth-45), y1='60px', x2='48px', y2='60px', onclick1=self.leftClose, onclick2=self.leftOpen)

        x = 45 + self.rightWidth
        self.dynbBottom = dynamicButton.dynamicButton(x1='calc(100vw - %dpx)'%x, y1='calc(100vh - %dpx)'%(BOTTOM_HEIGHT+35), x2='calc(100vw - %dpx)'%x, y2='calc(100vh - 40px)',
                                                      icon1='mdi-menu-down', icon2='mdi-menu-up', onclick1=self.bottomClose, onclick2=self.bottomOpen)
        
        x = self.rightWidth - 5
        self.dynbRight  = dynamicButton.dynamicButton(x1='calc(100vw - %dpx)'%x, y1='60px', x2='calc(100vw - 100px)', y2='60px', 
                                                      icon1='mdi-menu-right', icon2='mdi-menu-left', onclick1=self.rightClose, onclick2=self.rightOpen)
        
        # Creation of the contents for the panels
        self.createMap()
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
                                      self.cardMap,
                                      self.cardBottom
                                  ]),
                                  self.cardRight
                              ])
                             ]
        
        self.dynbLeft.setpos()
        
        return self.card
    
            
    # Create the content of the left panel
    def createLeft(self):
        pass
    
    # Create the content of the bottom panel
    def createBottom(self):
        pass
        
    # Create the content of the right panel
    def createRight(self):
        pass
    
    # Create the content of the Map panel
    def createMap(self):
        # Initial center and zoom of the map
        self.center = [50, 12]
        self.zoom   = 5

        # Map widget
        map_width  = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        map_height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        self.map = ipyleaflet.Map(max_zoom=21, center=self.center, zoom=self.zoom, scroll_wheel_zoom=True, 
                                  basemap=mapUtils.EmptyBasemap(), attribution_control=False, layout=Layout(width=map_width, height=map_height))
        
        mapUtils.addLayer(self.map, mapUtils.OSM_EC(),      LAYERNAME_BACKGROUND)
        mapUtils.addLayer(self.map, mapUtils.CartoLabels(), LAYERNAME_LABELS)
        layer = mapUtils.getLayer(self.map, LAYERNAME_LABELS)
        layer.opacity = 0.0
        
        
        # Add FullScreen control
        self.map.add_control(FullScreenControl(position="topright"))

        # Add Search control
        self.map.add_control(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))

        # Add Scale control
        self.map.add_control(ScaleControl(position='topleft'))

        # Add widget control to select basemaps
        self.toggleBasemap = toggle.toggle(0,
                                           ['Gisco', 'Esri', 'Google'],
                                           tooltips=['Select EC Gisco roadmap as background layer', 'Select ESRI WorldImagery as background layer', 'Select GOOGLE Satellite as background layer'],
                                           colorselected=settings.color_first, colorunselected=settings.color_second, rounded=False,
                                           dark=settings.dark_mode, onchange=self.onSelectBasemap, row=True, width=70, justify='start', paddingrow=0, tile=True)
        wcBasemap = WidgetControl(widget=self.toggleBasemap.draw(), position='bottomright')
        self.map.add_control(wcBasemap)
        
        
        # Add widget control to display geographic coordinates at mouse move
        self.cardCoordinates = v.Card(flat=True)
        wcCoordinates = WidgetControl(widget=self.cardCoordinates, position='topright')
        self.map.add_control(wcCoordinates)
        
        # Setup interaction on the map
        self.map._interaction_callbacks = CallbackDispatcher()
        self.map.on_interaction(self.handleMapInteraction)
        
        # Display the map inside its card
        self.cardMap.children = [self.map]
        

    # Manage all user interaction on the map
    def handleMapInteraction(self, **kwargs):
        if kwargs.get('type') == 'mousemove':
            lon = kwargs.get('coordinates')[1]
            lat = kwargs.get('coordinates')[0]
            self.cardCoordinates.children = [v.Html(tag='div', children=[' %.4f° N, %.4f° E'%(lat,lon)], style_='color: black;', class_='pa-0 ma-0 ml-1 mr-1')]
        #elif not self.handleInteractionStations(**kwargs):
        #    self.handleInteractionModel(**kwargs)
        
        

    # Selection of a basemap
    def onSelectBasemap(self, index):
        layer = mapUtils.getLayer(self.map, LAYERNAME_LABELS)

        if index == 1:
            basemaplayer = mapUtils.EsriWorldImagery()
            layer.opacity = 1.0
        elif index == 2:
            basemaplayer = mapUtils.GoogleHybrid()
            layer.opacity = 0.0
        else:
            basemaplayer = mapUtils.OSM_EC()
            layer.opacity = 0.0

        mapUtils.addLayer(self.map, basemaplayer, LAYERNAME_BACKGROUND)
    
    
    #################################################################################################################################################
    # Manage the opening/closing of the dynamic panels (left and bottom)
    #################################################################################################################################################
        
    # Close the left panel
    def leftClose(self):
        self.leftWidth = 0
        self.map_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width  = self.map_width
        self.cardMap.width     = self.map_width
        self.cardMap.min_width = self.map_width
        self.cardMap.max_width = self.map_width
        self.map.layout.width  = self.map_width
        

    # Open the left panel
    def leftOpen(self):
        self.leftWidth = LEFT_WIDTH
        self.map_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width  = self.map_width
        self.cardMap.width     = self.map_width
        self.cardMap.min_width = self.map_width
        self.cardMap.max_width = self.map_width
        self.map.layout.width  = self.map_width
        

    # Close the bottom panel
    def bottomClose(self):
        self.bottomHeight = 0
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMap.height = self.height
        self.map.layout.height = 'calc(%s - 1.5px)'%self.height
        

    # Open the bottom panel
    def bottomOpen(self):
        self.bottomHeight = BOTTOM_HEIGHT
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMap.height    = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.map.layout.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        

    # Close the right panel
    def rightClose(self):
        self.rightWidth = 0
        self.map_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardRight.width     = self.rightWidth
        self.cardRight.min_width = self.rightWidth
        self.cardRight.max_width = self.rightWidth
        
        self.cardBottom.width  = self.map_width
        self.cardMap.width     = self.map_width
        self.cardMap.min_width = self.map_width
        self.cardMap.max_width = self.map_width
        self.map.layout.width  = self.map_width
        
        x = 'calc(100vw - %dpx)'%(45 + self.rightWidth)
        self.dynbBottom.x1 = x
        self.dynbBottom.x2 = x
        self.dynbBottom.setpos()
        

    # Open the right panel
    def rightOpen(self):
        self.rightWidth = RIGHT_WIDTH
        self.map_width = 'calc(100vw - %dpx)'%(self.leftWidth+self.rightWidth)
        self.cardRight.width     = self.rightWidth
        self.cardRight.min_width = self.rightWidth
        self.cardRight.max_width = self.rightWidth
        
        self.cardBottom.width  = self.map_width
        self.cardMap.width     = self.map_width
        self.cardMap.width     = self.map_width
        self.cardMap.min_width = self.map_width
        self.cardMap.max_width = self.map_width
        self.map.layout.width  = self.map_width
        
        x = 'calc(100vw - %dpx)'%(45 + self.rightWidth)
        self.dynbBottom.x1 = x
        self.dynbBottom.x2 = x
        self.dynbBottom.setpos()
        
