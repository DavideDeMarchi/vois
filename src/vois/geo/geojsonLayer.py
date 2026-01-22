"Geojson layer class to be displayed in a ipyleaflet.Map with selection management"
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2025
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
from ipywidgets import CallbackDispatcher
import ipyleaflet


#####################################################################################################################################################
# geojsonLayer class (fully tested for point features but almost ready for extention to polygons and polylines)
#####################################################################################################################################################
class geojsonLayer():
    
    # Initialization
    def __init__(self,
                 featureCollection,
                 style={},
                 point_style={'radius': 9, 'fillColor': "#ff0000", 'color': "#000000", 'weight': 1.5, 'opacity': 1.0, 'fillOpacity': 0.8},
                 style_callback=None,
                 hover_style={'fillColor': 'orange' , 'fillOpacity': 0.7, 'dashArray': '3', 'weight': 2.0 },
                 selection_style={},
                 selection_point_style={'radius': 10, 'color': "#ffff00", 'weight': 4.0, 'opacity': 1.0, 'fillOpacity': 0.0},
                 name='Layer',
                 on_click=None):
        
        # Feature collection to display
        self.featureCollection = featureCollection
                 
        # Styling members
        self.style                 = style
        self.point_style           = point_style
        self.style_callback        = style_callback
        self.hover_style           = hover_style
        self.selection_style       = selection_style
        self.selection_point_style = selection_point_style
        
        # Callback 
        self.on_click = on_click
       
        
        # GeoJSON layer
        self.geojson = ipyleaflet.GeoJSON(data=self.featureCollection, point_style=self.point_style, style=self.style, hover_style=self.hover_style, name=name)
        if not style_callback is None:
            self.geojson.style_callback = self.style_callback
        
        self.geojson.on_click(self.__internal_on_click)
        
        
        # Feature collection to manage the selection
        self.selection = { "type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                           "features": [ { "type": "Feature", "properties": { "name": "selected" }, "geometry": { "type": "Point", "coordinates": [ 99999, 99999 ] } } ]
                        }
        
        self.selection_geojson = ipyleaflet.GeoJSON(data=self.selection, point_style=self.selection_point_style, style=self.selection_style, hover_style=self.hover_style)

        
        # Map where the layer is added
        self.m = None

        # True if a click on the map must be skipped
        self.skip_map_click = False        
        
        
    # Add the layer to an ipyleaflet Map and manage the click to unselect a geojson feature
    def addToMap(self, m):
        self.m = m
        self.m.add(self.geojson)
        self.m.add(self.selection_geojson)
        
        self.skip_map_click = False
        self.m._interaction_callbacks = CallbackDispatcher()
        self.m.on_interaction(self.handle_interaction_map)
        

    # Handle click on the map (to unselect)
    def handle_interaction_map(self, **kwargs):
        if kwargs.get('type') == 'click':
            if not self.skip_map_click:
                self.selection['features'] = [ { "type": "Feature", "properties": { "name": "selected" }, "geometry": { "type": "Point", "coordinates": [ 99999, 99999 ] } }  ]
                newsel = ipyleaflet.GeoJSON(data=self.selection, point_style=self.selection_point_style, style=self.selection_style, hover_style=self.hover_style)
                self.m.substitute(self.selection_geojson,newsel)
                self.selection_geojson = newsel
                if not self.on_click is None:
                    self.on_click(None)
            self.skip_map_click = False
    
    
    # Select one of the features
    def selectFeature(self, feature):
        self.selection['features'] = [ { "type": "Feature", "properties": { "name": "selected" }, "geometry": feature['geometry'] }  ]
        newsel = ipyleaflet.GeoJSON(data=self.selection, point_style=self.selection_point_style, style=self.selection_style)
        self.m.substitute(self.selection_geojson,newsel)
        self.selection_geojson = newsel
        
        
    # Handle click on a geojson feature to select
    def __internal_on_click(self, event, feature, properties, id):
        if event == 'click':
            self.skip_map_click = True
            self.selectFeature(feature)
            if not self.on_click is None:
                self.on_click(feature)

        
    