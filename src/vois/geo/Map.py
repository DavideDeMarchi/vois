"""Map class"""
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
from vois.vuetify import settings, toggle, switch
from vois.geo import mapUtils
from vois.templates import PageConfigurator

# Name of layers
LAYERNAME_BACKGROUND  = 'Background'
LAYERNAME_LABELS      = 'Labels'


#####################################################################################################################################################
# Map class
#####################################################################################################################################################
class Map(ipyleaflet.Map):


    # Initialization
    def __init__(self,
                 width='100%',
                 height='600px',
                 center=[50, 12],
                 zoom=5,
                 show_fullscreen=True,    # Show or Hide the fullscreen control
                 show_search=True,        # Show or Hide the Search control
                 show_scale=True,         # Show or Hide the Scale control
                 show_coordinates=True,   # Show or hide the Coordinates control
                 show_overview=False,     # Show or hide the Overview control
                 show_basemaps=True,      # Show or hide the Basemaps toggle control
                 color_first=None,        # Main color
                 color_second=None,       # Secondary color
                 dark=None,               # Dark flag
                 basemapindex=0,          # Initial basemap index (0=EC, 1=Esri, 2=Google)
                 onclick=None,            # Callback function to call on click (receives as parameter: map, lon, lat, zoom)
                 **kwargs):
        
        self._width            = width
        self._height           = height
        self._show_fullscreen  = show_fullscreen
        self._show_search      = show_search
        self._show_scale       = show_scale
        self._show_coordinates = show_coordinates
        self._show_overview    = show_overview
        self._show_basemaps    = show_basemaps
        self._onclick          = onclick
        
        self._color_first = color_first
        if self._color_first is None:
            self._color_first = settings.color_first
        
        self._color_second = color_second
        if self._color_second is None:
            self._color_second = settings.color_second
            
        self._dark = dark
        if self._dark is None:
            self._dark = settings.dark_mode
            
        self._basemapindex = basemapindex
        
        # Initial center and zoom of the map
        self.center = center
        self.zoom   = zoom

        # Card containing the widgets to configure the map appearance
        self.configure_card = None
        self.s1 = self.s2 = self.s3 = self.s4 = self.s5 = self.s6 = None
        self.update_properties = True
        
        # Map widget
        super().__init__(max_zoom=21, center=self.center, zoom=self.zoom, scroll_wheel_zoom=True, 
                         basemap=mapUtils.EmptyBasemap(), attribution_control=False, layout=Layout(width=self._width, height=self._height, margin='0px 0px 0px 0px'),
                         **kwargs)
        
        mapUtils.addLayer(self, mapUtils.OSM_EC(),      LAYERNAME_BACKGROUND)
        mapUtils.addLayer(self, mapUtils.CartoLabels(), LAYERNAME_LABELS)
        layer = mapUtils.getLayer(self, LAYERNAME_LABELS)
        layer.opacity = 0.0
        self.onSelectBasemap(self._basemapindex)
        
        self.toggleBasemap   = None
        self.cardCoordinates = None
        
        # Add FullScreen control
        self.show_fullscreen = self._show_fullscreen

        # Add Search control
        self.show_search = self._show_search

        # Add Scale control
        self.show_scale = self._show_scale

        # Add widget control to select basemaps
        self.show_basemaps = self._show_basemaps
        
        # Add overview
        self.show_overview = self._show_overview
        
        # Add widget control to display geographic coordinates at mouse move
        self.show_coordinates = self._show_coordinates
        
        # Manage interaction events
        self._interaction_callbacks = CallbackDispatcher()
        self.on_interaction(self.handleMapInteraction)
        

    # Fake "draw" method
    def draw(self):
        return self
      
    
    # Remove all layers from map
    def clear(self):
        mapUtils.clear(self)
    
    
    # Add a ipyleaflet.TileLayer to the map
    def addLayer(self, tileLayer, name=None, opacity=1.0):
        
        # if no name is passed, generate a layer name
        if name is None:
            count = len(self.layers)
            name = "layer%d"%(count+1)
            
        # In case a vectorlayer or rasterlayer is passed: call .tileLayer() to get the ipyleaflet.TileLayer instance!
        if isinstance(tileLayer, ipyleaflet.TileLayer):
            mapUtils.addLayer(self, tileLayer, name=name, opacity=opacity)
        else:
            mapUtils.addLayer(self, tileLayer.tileLayer(), name=name, opacity=opacity)
        
        
    # Manage all user interaction on the map
    def handleMapInteraction(self, **kwargs):
        
        if self._show_coordinates:
            if kwargs.get('type') == 'mousemove':
                lon = kwargs.get('coordinates')[1]
                lat = kwargs.get('coordinates')[0]
                self.cardCoordinates.children = [v.Html(tag='div', children=[' %.4f° N, %.4f° E'%(lat,lon)], style_='color: black;', class_='pa-0 ma-0 ml-1 mr-1')]
        
        if self._onclick is not None:
            if kwargs.get('type') == 'click':
                lon = kwargs.get('coordinates')[1]
                lat = kwargs.get('coordinates')[0]
                self._onclick(self, lon, lat, int(self.zoom))
        

    # Selection of a basemap
    def onSelectBasemap(self, index):
        layer = mapUtils.getLayer(self, LAYERNAME_LABELS)

        self._basemapindex = max(0, min(2, index))
        
        if self._basemapindex == 1:
            basemaplayer = mapUtils.EsriWorldImagery()
            layer.opacity = 1.0
        elif self._basemapindex == 2:
            basemaplayer = mapUtils.GoogleHybrid()
            layer.opacity = 0.0
        else:
            basemaplayer = mapUtils.OSM_EC()
            layer.opacity = 0.0

        mapUtils.addLayer(self, basemaplayer, LAYERNAME_BACKGROUND)

        
    # Change of configure widgets
    def change_fullscreen(self, flag): 
        if self.update_properties:
            self.show_fullscreen = flag
            
    def change_coordinates(self, flag):
        if self.update_properties:
            self.show_coordinates = flag
            
    def change_search(self, flag):
        if self.update_properties:
            self.show_search = flag
            
    def change_scale(self, flag):
        if self.update_properties:
            self.show_scale = flag
            
    def change_basemaps(self, flag):
        if self.update_properties:
            self.show_basemaps = flag
            
    def change_overview(self, flag):
        if self.update_properties:
            self.show_overview = flag
        
        
    # Create a card instance to configure the Map appearance and returns it
    def configure(self):
        if self.configure_card is None:
            self.configure_card = v.Card(flat=True, class_='pa-2 ma-0')
            
            self.s1 = switch.switch(self.show_fullscreen,  'Add the Fullscreen control',  inset=True, dense=True, onchange=self.change_fullscreen, color=self._color_first)
            self.s2 = switch.switch(self.show_coordinates, 'Add the Coordinates control', inset=True, dense=True, onchange=self.change_coordinates, color=self._color_first)
            self.s3 = switch.switch(self.show_search,      'Add the Search control',      inset=True, dense=True, onchange=self.change_search, color=self._color_first)
            self.s4 = switch.switch(self.show_scale,       'Add the Scale control',       inset=True, dense=True, onchange=self.change_scale, color=self._color_first)
            self.s5 = switch.switch(self.show_basemaps,    'Add the Basemaps control',    inset=True, dense=True, onchange=self.change_basemaps, color=self._color_first)
            self.s6 = switch.switch(self.show_overview,    'Add the Overview control',    inset=True, dense=True, onchange=self.change_overview, color=self._color_first)
            
            self.configure_card.children = [widgets.VBox([PageConfigurator.label('Map', color='black'), self.s1.draw(), self.s2.draw(), self.s3.draw(), self.s4.draw(), self.s5.draw(), self.s6.draw()])]
            
        return self.configure_card


    @property
    def content(self):
        return 'Map'
        
    @content.setter
    def content(self, c):
        pass
    
    
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = w
        self.layout.width = self._width

        
    @property
    def height(self):
        return self._height
        
    @height.setter
    def height(self, h):
        self._height = h
        self.layout.height = self._height

        
    @property
    def show_fullscreen(self):
        return self._show_fullscreen
        
    @show_fullscreen.setter
    def show_fullscreen(self, flag):
        self._show_fullscreen = flag

        if self.s1 is not None:
            self.update_properties = False
            self.s1.value = flag
            self.update_properties = True

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.FullScreenControl):
                self.remove(control)
                
        if self._show_fullscreen:
            self.add(FullScreenControl(position="topright"))


    @property
    def show_coordinates(self):
        return self._show_coordinates
        
    @show_coordinates.setter
    def show_coordinates(self, flag):
        self._show_coordinates = flag

        if self.s2 is not None:
            self.update_properties = False
            self.s2.value = flag
            self.update_properties = True
        
        mapUtils.removeCoordinates(self)
                
        if self._show_coordinates:
            self.cardCoordinates = mapUtils.getCoordinatesCard(self)

            
    @property
    def show_search(self):
        return self._show_search
        
    @show_search.setter
    def show_search(self, flag):
        self._show_search = flag

        if self.s3 is not None:
            self.update_properties = False
            self.s3.value = flag
            self.update_properties = True

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.SearchControl):
                self.remove(control)
                
        if self._show_search:
            self.add(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))


    @property
    def show_scale(self):
        return self._show_scale
        
    @show_scale.setter
    def show_scale(self, flag):
        self._show_scale = flag

        if self.s4 is not None:
            self.update_properties = False
            self.s4.value = flag
            self.update_properties = True

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.ScaleControl):
                self.remove(control)
                
        if self._show_scale:
            self.add(ScaleControl(position='topleft'))


    @property
    def show_basemaps(self):
        return self._show_basemaps
        
    @show_basemaps.setter
    def show_basemaps(self, flag):
        self._show_basemaps = flag

        if self.s5 is not None:
            self.update_properties = False
            self.s5.value = flag
            self.update_properties = True

        mapUtils.removeCardByName(self, 'Basemaps')
                
        if self._show_basemaps:
            c = mapUtils.getCardByName(self, 'Basemaps', position='bottomright')
            c.tile = True
            self.toggleBasemap = toggle.toggle(self._basemapindex,
                                               ['Gisco', 'Esri', 'Google'],
                                               tooltips=['Select EC Gisco roadmap as background layer', 'Select ESRI WorldImagery as background layer', 'Select GOOGLE Satellite as background layer'],
                                               colorselected=self._color_first, colorunselected=self._color_second, rounded=False,
                                               dark=self._dark, onchange=self.onSelectBasemap, row=True, width=70, justify='start', paddingrow=0, tile=True)
            c.children = [self.toggleBasemap.draw()]


    @property
    def show_overview(self):
        return self._show_overview
        
    @show_overview.setter
    def show_overview(self, flag):
        self._show_overview = flag
        mapUtils.removeOverview(self)
        
        if self.s6 is not None:
            self.update_properties = False
            self.s6.value = flag
            self.update_properties = True
                
        if self._show_overview:
            mapUtils.addOverview(self, position='bottomleft')


    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        if self.toggleBasemap is not None:
            self.toggleBasemap.colorselected = self._color_first

        if self.configure_card is not None:
            self.s1.color = self._color_first
            self.s2.color = self._color_first
            self.s3.color = self._color_first
            self.s4.color = self._color_first
            self.s5.color = self._color_first
            self.s6.color = self._color_first


    @property
    def color_second(self):
        return self._color_second
        
    @color_second.setter
    def color_second(self, color):
        self._color_second = color

        if self.toggleBasemap is not None:
            self.toggleBasemap.colorunselected = self._color_second


    @property
    def dark(self):
        return self._dark
        
    @dark.setter
    def dark(self, flag):
        self._dark = flag

        if self.toggleBasemap is not None:
            self.toggleBasemap.dark = self._dark
            
            
    @property
    def basemapindex(self):
        return self._basemapindex
        
    @basemapindex.setter
    def basemapindex(self, index):
        self.onSelectBasemap(index)

        if self.toggleBasemap is not None:
            self.toggleBasemap.value = self._basemapindex
            
            
    @property
    def state(self):
        return {x: getattr(self, x) for x in ['content',
                                              #'width',      # Will inherit from content!!!
                                              #'height',
                                              'show_fullscreen',
                                              'show_coordinates',
                                              'show_search',
                                              'show_scale',
                                              'show_basemaps',
                                              'show_overview',
                                              'color_first',
                                              'color_second',
                                              'dark',
                                              'basemapindex',
                                              'center',
                                              'zoom'
                                             ]}
        
    @state.setter
    def state(self, statusdict):
        for key, value in statusdict.items():
            setattr(self, key, value)
            
            
    @property
    def onclick(self):
        return self._onclick
        
    @onclick.setter
    def onclick(self, callback):
        self._onclick = callback
            