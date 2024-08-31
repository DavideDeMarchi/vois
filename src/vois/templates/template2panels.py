"""Template page with left and bottom panels"""
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

# Local imports
import mapUtils
import dynamicButton

# Panels dimensioning
LEFT_WIDTH    = 400      # Width  in pixels of the left bar
BOTTOM_HEIGHT = 240      # Height in pixels of the bottom bar

# Name of layers
LAYERNAME_BACKGROUND  = 'Background'
LAYERNAME_LABELS      = 'Labels'


                
#####################################################################################################################################################
# Template page with left and bottom panels
#####################################################################################################################################################
class template2panels(page.page):

    
    # Initialization
    def __init__(self, output, onclose=None, **kwargs):
        super().__init__('Demo', 'Geospatial page with left and bottom panel', output, onclose=onclose, copyrighttext='European Commission - Joint Research Centre', **kwargs)

   
    #################################################################################################################################################
    # Create the page and returns the card widget where the content of the page must be displayed
    #################################################################################################################################################
    def create(self):
        super().create()
        
        # Initialize some member variables
        self.leftWidth    = LEFT_WIDTH
        self.bottomHeight = BOTTOM_HEIGHT
        
        # Cards for the panels
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%settings.color_first
        self.main_width  = 'calc(100vw - %dpx)'%self.leftWidth
        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft   = v.Card(flat=True, style_=st, outlined=True, width=self.leftWidth, min_width=self.leftWidth, max_width=self.leftWidth, height=self.height)
        self.cardBottom = v.Card(flat=True, style_=st + ' border-left-width: 0px; border-top-width: 0px;', outlined=True, width=self.main_width, height=self.bottomHeight, min_height=self.bottomHeight)
        self.cardMain   = v.Card(flat=True, style_=st + ' border-left-width: 0px;', outlined=True, width=self.main_width, height=self.main_height)
        
        # DynamicButtons to open/close the left and bottom panels
        self.dynbLeft   = dynamicButton.dynamicButton(x1='%dpx'%(self.leftWidth-45), y1='64px', x2='48px', y2='64px', onclick1=self.leftClose, onclick2=self.leftOpen)
        self.dynbBottom = dynamicButton.dynamicButton(x1='calc(100vw - 45px)', y1='calc(100vh - %dpx)'%(BOTTOM_HEIGHT+35), x2='calc(100vw - 45px)', y2='calc(100vh - 40px)',
                                                      icon1='mdi-menu-down', icon2='mdi-menu-up', onclick1=self.bottomClose, onclick2=self.bottomOpen)
        
        # Creation of the contents for the panels
        self.createMain()
        self.createLeft()
        self.createBottom()
        
        # Compose the panels
        self.card.children = [self.dynbLeft.draw(),
                              self.dynbBottom.draw(),
                              widgets.HBox([
                                  self.cardLeft,
                                  widgets.VBox([
                                      self.cardMain,
                                      self.cardBottom
                                  ])
                              ])
                             ]
        
        return self.card
    

    @property
    def titlecolor(self):
        return self._titlecolor
        
    @titlecolor.setter
    def titlecolor(self, color):
        page.page.titlecolor.fset(self, color)   # call super() property setter

        # Set the color of the panels outline!
        st = 'border-radius: 0px; border-color: %s; border-width: 1px; overflow: hidden;'%color
        self.cardLeft.style_   = st
        self.cardBottom.style_ = st + ' border-left-width: 0px; border-top-width: 0px;'
        self.cardMain.style_   = st + ' border-left-width: 0px;'

        # Set the color of the dynamicButton
        self.dynbLeft.color   = color
        self.dynbBottom.color = color
        
        # Set the color of basemaps toggle
        for b in self.toggleBasemap.buttons:
            b.color_selected = color
            if b._selected:
                b.b.color = color
                
    @property
    def footercolor(self):
        return self._footercolor
        
    @footercolor.setter
    def footercolor(self, color):
        page.page.footercolor.fset(self, color)   # call super() property setter

        # Set the color of basemaps toggle
        for b in self.toggleBasemap.buttons:
            b.color_unselected = color
            if not b._selected:
                b.b.color = color
                
        
    @property
    def titleheight(self):
        return self._titleheight
        
    @titleheight.setter
    def titleheight(self, height):
        page.page.titleheight.fset(self, height)   # call super() property setter

        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft.height = self.height
        self.cardMain.height = self.main_height
        
        self.map.layout.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        
        d = self._titleheight - 54
        newy = '%dpx'%(64+d)
        self.dynbLeft.y1 = self.dynbLeft.y2 = newy
        self.dynbLeft.setpos()
        

    @property
    def footerheight(self):
        return self._footerheight
        
    @footerheight.setter
    def footerheight(self, height):
        page.page.footerheight.fset(self, height)   # call super() property setter

        self.main_height = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.cardLeft.height = self.height
        self.cardMain.height = self.main_height
        
        self.map.layout.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        
        d = self._titleheight - 54
        newy = '%dpx'%(64+d)
        self.dynbLeft.y1 = self.dynbLeft.y2 = newy
        self.dynbLeft.setpos()
        
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
        
    # Create the content of the Main panel
    def createMain(self):
        # Initial center and zoom of the map
        self.center = [50, 12]
        self.zoom   = 5

        # Map widget
        main_width  = 'calc(100vw - %dpx)'%self.leftWidth
        main_height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        self.map = ipyleaflet.Map(max_zoom=21, center=self.center, zoom=self.zoom, scroll_wheel_zoom=True, 
                                  basemap=mapUtils.EmptyBasemap(), attribution_control=False, layout=Layout(width=main_width, height=main_height, margin='0px 0px 0px 0px'))
        
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
        
        # Display the map inside the main card
        self.cardMain.children = [self.map]
        

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
        self.main_width  = '100vw'
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width = '100vw'
        self.cardMain.width   = self.main_width
        self.map.layout.width = self.main_width
        

    # Open the left panel
    def leftOpen(self):
        self.leftWidth = LEFT_WIDTH
        self.main_width = 'calc(100vw - %dpx)'%self.leftWidth
        self.cardLeft.width     = self.leftWidth
        self.cardLeft.min_width = self.leftWidth
        self.cardLeft.max_width = self.leftWidth
        
        self.cardBottom.width = self.main_width
        self.cardMain.width   = self.main_width
        self.map.layout.width = self.main_width
        

    # Close the bottom panel
    def bottomClose(self):
        self.bottomHeight = 0
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMain.height = self.height
        self.map.layout.height = 'calc(%s - 1.5px)'%self.height
        

    # Open the bottom panel
    def bottomOpen(self):
        self.bottomHeight = BOTTOM_HEIGHT
        self.cardBottom.height     = self.bottomHeight
        self.cardBottom.min_height = self.bottomHeight
        
        self.cardMain.height   = 'calc(%s - %dpx)'%(self.height,self.bottomHeight)
        self.map.layout.height = 'calc(%s - %fpx)'%(self.height,self.bottomHeight+1.5)
        
