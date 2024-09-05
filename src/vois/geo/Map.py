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
from vois.vuetify import settings, toggle
from vois.geo import mapUtils

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
                 show_fullscreen=True,            # Show or Hide the fullscreen control
                 show_search=True,                # Show or Hide the Search control
                 show_scale=True,                 # Show or Hide the Scale control
                 show_coordinates=True,           # Show or hide the Coordinates control
                 show_overview=False,             # Show or hide the Overview control
                 show_basemaps=True,              # Show or hide the Basemaps toggle control
                 basemaps_colorselected=None,     # Colors for the basemaps selection toggle widget
                 basemaps_colorunselected=None,   # ""
                 basemaps_dark=None,              # ""
                 **kwargs):
        
        self._width            = width
        self._height           = height
        self._show_fullscreen  = show_fullscreen
        self._show_search      = show_search
        self._show_scale       = show_scale
        self._show_coordinates = show_coordinates
        self._show_overview    = show_overview
        self._show_basemaps    = show_basemaps
        
        self._basemaps_colorselected = basemaps_colorselected
        if self._basemaps_colorselected is None:
            self._basemaps_colorselected = settings.color_first
        
        self._basemaps_colorunselected = basemaps_colorunselected
        if self._basemaps_colorunselected is None:
            self._basemaps_colorunselected = settings.color_second
            
        self._basemaps_dark = basemaps_dark
        if self._basemaps_dark is None:
            self._basemaps_dark = settings.dark_mode
        
        # Initial center and zoom of the map
        self.center = center
        self.zoom   = zoom

        # Map widget
        super().__init__(max_zoom=21, center=self.center, zoom=self.zoom, scroll_wheel_zoom=True, 
                         basemap=mapUtils.EmptyBasemap(), attribution_control=False, layout=Layout(width=self._width, height=self._height, margin='0px 0px 0px 0px'),
                         **kwargs)
        
        mapUtils.addLayer(self, mapUtils.OSM_EC(),      LAYERNAME_BACKGROUND)
        mapUtils.addLayer(self, mapUtils.CartoLabels(), LAYERNAME_LABELS)
        layer = mapUtils.getLayer(self, LAYERNAME_LABELS)
        layer.opacity = 0.0
        
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

        
    # Manage all user interaction on the map
    def handleMapInteraction(self, **kwargs):
        if kwargs.get('type') == 'mousemove':
            lon = kwargs.get('coordinates')[1]
            lat = kwargs.get('coordinates')[0]
            self.cardCoordinates.children = [v.Html(tag='div', children=[' %.4f° N, %.4f° E'%(lat,lon)], style_='color: black;', class_='pa-0 ma-0 ml-1 mr-1')]
        

    # Selection of a basemap
    def onSelectBasemap(self, index):
        layer = mapUtils.getLayer(self, LAYERNAME_LABELS)

        if index == 1:
            basemaplayer = mapUtils.EsriWorldImagery()
            layer.opacity = 1.0
        elif index == 2:
            basemaplayer = mapUtils.GoogleHybrid()
            layer.opacity = 0.0
        else:
            basemaplayer = mapUtils.OSM_EC()
            layer.opacity = 0.0

        mapUtils.addLayer(self, basemaplayer, LAYERNAME_BACKGROUND)

        
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

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.FullScreenControl):
                self.remove(control)
                
        if self._show_fullscreen:
            self.add(FullScreenControl(position="topright"))

            
    @property
    def show_search(self):
        return self._show_search
        
    @show_search.setter
    def show_search(self, flag):
        self._show_search = flag

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.SearchControl):
                self.remove(control)
                
        if self._show_search:
            self.add(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))


    @property
    def show_scale(self):
        return self._show_search
        
    @show_scale.setter
    def show_scale(self, flag):
        self._show_scale = flag

        for control in self.controls:
            if isinstance(control, ipyleaflet.leaflet.ScaleControl):
                self.remove(control)
                
        if self._show_search:
            self.add(ScaleControl(position='topleft'))


    @property
    def show_basemaps(self):
        return self._show_basemaps
        
    @show_basemaps.setter
    def show_basemaps(self, flag):
        self._show_basemaps = flag

        mapUtils.removeCardByName(self, 'Basemaps')
                
        if self._show_basemaps:
            c = mapUtils.getCardByName(self, 'Basemaps', position='bottomright')
            c.tile = True
            self.toggleBasemap = toggle.toggle(0,
                                               ['Gisco', 'Esri', 'Google'],
                                               tooltips=['Select EC Gisco roadmap as background layer', 'Select ESRI WorldImagery as background layer', 'Select GOOGLE Satellite as background layer'],
                                               colorselected=self._basemaps_colorselected, colorunselected=self._basemaps_colorunselected, rounded=False,
                                               dark=self._basemaps_dark, onchange=self.onSelectBasemap, row=True, width=70, justify='start', paddingrow=0, tile=True)
            c.children = [self.toggleBasemap.draw()]


    @property
    def show_overview(self):
        return self._show_overview
        
    @show_overview.setter
    def show_overview(self, flag):
        self._show_overview = flag
        mapUtils.removeOverview(self)
                
        if self._show_overview:
            mapUtils.addOverview(self, position='bottomleft')


    @property
    def show_coordinates(self):
        return self._show_coordinates
        
    @show_coordinates.setter
    def show_coordinates(self, flag):
        self._show_coordinates = flag
        mapUtils.removeCoordinates(self)
                
        if self._show_coordinates:
            self.cardCoordinates = mapUtils.getCoordinatesCard(self)
            self._interaction_callbacks = CallbackDispatcher()
            self.on_interaction(self.handleMapInteraction)


    @property
    def basemaps_colorselected(self):
        return self._basemaps_colorselected
        
    @basemaps_colorselected.setter
    def basemaps_colorselected(self, color):
        self._basemaps_colorselected = color

        if self.toggleBasemap is not None:
            self.toggleBasemap.colorselected = self._basemaps_colorselected


    @property
    def basemaps_colorunselected(self):
        return self._basemaps_colorunselected
        
    @basemaps_colorunselected.setter
    def basemaps_colorunselected(self, color):
        self._basemaps_colorunselected = color

        if self.toggleBasemap is not None:
            self.toggleBasemap.colorunselected = self._basemaps_colorunselected


    @property
    def basemaps_dark(self):
        return self._basemaps_dark
        
    @basemaps_dark.setter
    def basemaps_dark(self, flag):
        self._basemaps_dark = flag

        if self.toggleBasemap is not None:
            self.toggleBasemap.dark = self._basemaps_dark
            