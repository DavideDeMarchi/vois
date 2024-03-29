"""Widget to select the basemap to visualise on a ipyleaflet Map"""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2023
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
import ipyleaflet
from ipyleaflet import basemaps as ipybasemaps, basemap_to_tiles, LayerGroup

try:
    from jeodpp import inter
except:
    pass

import traitlets

try:
    from . import settings
    from . import treeview
except:
    import settings
    import treeview


# Empty basemap (gray background)
emptyBasemap = traitlets.Bunch({'attribution': '',
                                'max_zoom': 19, 
                                'name': 'Empty basemap',
                                'build_url':   lambda *args, **kwargs: 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/gray.png'})



# Additional attributions for the basemaps not already in ipyleaflet
basemapsAttribution = {
    'Wikimedia':                    'Wikimedia maps beta | &copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> contributors', 
    'CartoDB.PositronOnlyLabels':   '&copy; <a href="http://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions" target="_blank">CartoDB</a>',
    'CartoDB.DarkMatterOnlyLabels': '&copy; <a href="http://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions" target="_blank">CartoDB</a>',
    'CartoDB.VoyagerOnlyLabels':    '&copy; <a href="http://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions" target="_blank">CartoDB</a>',
    'OpenStreetMap.EC':             '&copy; <a href="http://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    'Google.Roadmap':               '&copy; <a href="http://www.google.com" target="_blank">Google</a>',
    'Google.Satellite':             '&copy; <a href="http://www.google.com" target="_blank">Google</a>',
    'Google.Terrain':               '&copy; <a href="http://www.google.com" target="_blank">Google</a>',
    'Google.Hybrid':                '&copy; <a href="http://www.google.com" target="_blank">Google</a>',
    'Esri.Ocean':                   'Tiles &copy; Esri — GEBCO, NOAA, National Geographic, DeLorme, HERE, Geonames.org, and other contributors', 
    'Esri.Terrain':                 'Tiles &copy; Esri — Esri, USGS, NOAA',
    'Esri.ShadedRelief':            'Tiles &copy; Esri',
    'Esri.PhysicalMap':             'Tiles &copy; Esri — U.S. National Park Service',
    'Stamen.TonerBackground':       'Map tiles by <a href=\"http://stamen.com\" target="_blank">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\" target="_blank">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a>', 
    'Stamen.TonerLite':             'Map tiles by <a href=\"http://stamen.com\" target="_blank">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\" target="_blank">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a>', 
    'Stamen.TerrainBackground':     'Map tiles by <a href=\"http://stamen.com\" target="_blank">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\" target="_blank">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a>', 
    'CyclOSM':                      '<a href=\"https://github.com/cyclosm/cyclosm-cartocss-style/releases\" title=\"CyclOSM - Open Bicycle render\" target="_blank">CyclOSM</a> | Map data: &copy; <a href=\"https://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a> contributors', 
    'CartoDB.PositronNoLabels':     '&copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\" target="_blank">CartoDB</a>', 
    'CartoDB.DarkMatterNoLabels':   '&copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\" target="_blank">CartoDB</a>', 
    'CartoDB.Voyager':              '&copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\" target="_blank">CartoDB</a>', 
    'CartoDB.VoyagerNoLabels':      '&copy; <a href=\"http://www.openstreetmap.org/copyright\" target="_blank">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\" target="_blank">CartoDB</a>', 
    'Gisco.OSMCartoComposite':      '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoBackground':     '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoLabels':         '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBlossomComposite':    '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBlossomBackground':   '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBlossomLabels':       '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMPositronComposite':   '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMPositronBackground':  '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMPositronLabels':      '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoV4Composite':    '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoV4Background':   '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoV4Labels':       '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBrightComposite':     '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBrightBackground':    '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMBrightLabels':        '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoHDMComposite':   '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoHDMBackground':  '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
    'Gisco.OSMCartoHDMLabels':      '&copy; <a href=\"https://ec.europa.eu/eurostat/web/gisco\" target="_blank">Eurostat GISCO</a>', 
  
    'BDAP.Elevation.Merit':                  '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — Yamazaki D. et al.: A high accuracy map of global terrain elevations',
    'BDAP.Elevation.Gebco':                  '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — <a href=\"https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/\" target="_blank">General Bathymetric Chart of the Oceans</a>',
    'BDAP.GridSystems.MGRS':                 '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — US Army Map Service (now NGA - National Geospatial-Intelligence Agency',
    'BDAP.GridSystems.Landsat':              '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — USGS',
    'BDAP.GridSystems.UTMgrid':              '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — ESRI',
    'BDAP.Orthoimagery.Terracolor':          '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — Earthstar Geographics LLC',
    'BDAP.GlobalForestChange.LandsatMosaic': '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — Hansen, UMD, Google, USGS, NASA',
    'BDAP.GHSL.S2Mosaic':                    '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a> — GHSL',
    'BDAP.Core003.SpotMosaic':               '&copy; Tiles served by <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\" target="_blank">EC-JRC BDAP</a>',
}


# Build a basemap that works in old and new versions of ipyleaflet
def buildBasemap(oldstyledictionary):
    if ipyleaflet.__version__ == '0.9.0':
        return oldstyledictionary
    else:
        return traitlets.Bunch({'max_zoom':    oldstyledictionary['max_zoom'],
                                'name':        oldstyledictionary['name'],
                                'attribution': oldstyledictionary['attribution'],
                                'build_url':   lambda *args, **kwargs: oldstyledictionary['url']})

    
# Given a name and an interapro collections path (example inter.collections.BaseData.Elevation.MERIT.Hillshade), returns a basemap
def buildBdapLayer(name, collectionpath):
    pBack = inter.Collection(collectionpath).process()
    procid = pBack.toLayer()
    return buildBasemap({'attribution': '&copy; <a href=\"https://jeodpp.jrc.ec.europa.eu/bdap/\">EC-JRC BDAP</a>', 
                         'max_zoom': 18,
                         'name': name,
                         'url': 'https://jeodpp.jrc.ec.europa.eu/jeodpp-inter-view/?x={x}&y={y}&z={z}&procid=%s'%procid})
    

# Given a int or a string returns a basemap
def preprocessBasemap(bm):
    if type(bm) is int or type(bm) is str:
        if bm == 1 or bm == 'OpenStreetMap.Mapnik':
            return ipybasemaps.OpenStreetMap.Mapnik
        elif bm == 2 or bm == 'OpenStreetMap.BlackAndWhite':
            return ipybasemaps.OpenStreetMap.BlackAndWhite
        elif bm == 3 or bm == 'OpenStreetMap.DE':
            return ipybasemaps.OpenStreetMap.DE
        elif bm == 4 or bm == 'OpenStreetMap.France':
            return ipybasemaps.OpenStreetMap.France
        elif bm == 5 or bm == 'OpenStreetMap.HOT':
            return ipybasemaps.OpenStreetMap.HOT
        elif bm == 6 or bm == 'OpenTopoMap':
            return ipybasemaps.OpenTopoMap
        elif bm == 7 or bm == 'OpenMapSurfer.Roads':
            return ipybasemaps.OpenMapSurfer.Roads
        elif bm == 8 or bm == 'OpenMapSurfer.Grayscale':
            return ipybasemaps.OpenMapSurfer.Grayscale
        elif bm == 9 or bm == 'Hydda.Full':
            return ipybasemaps.Hydda.Full
        elif bm == 10 or bm == 'Hydda.Base':
            return ipybasemaps.Hydda.Base
        elif bm == 11 or bm == 'Esri.WorldStreetMap':
            return ipybasemaps.Esri.WorldStreetMap
        elif bm == 12 or bm == 'Esri.DeLorme':
            return ipybasemaps.Esri.DeLorme
        elif bm == 13 or bm == 'Esri.WorldTopoMap':
            return ipybasemaps.Esri.WorldTopoMap
        elif bm == 14 or bm == 'Esri.WorldImagery':
            return ipybasemaps.Esri.WorldImagery
        elif bm == 15 or bm == 'Esri.NatGeoWorldMap':
            return ipybasemaps.Esri.NatGeoWorldMap
        elif bm == 16 or bm == 'HikeBike.HikeBike':
            return ipybasemaps.HikeBike.HikeBike
        elif bm == 17 or bm == 'Stamen.Terrain':
            return ipybasemaps.Stamen.Terrain
        elif bm == 18 or bm == 'MtbMap':
            return ipybasemaps.MtbMap
        elif bm == 19 or bm == 'CartoDB.Positron':
            return ipybasemaps.CartoDB.Positron
        elif bm == 20 or bm == 'CartoDB.DarkMatter':
            return ipybasemaps.CartoDB.DarkMatter
        elif bm == 21 or bm == 'NASAGIBS.ModisTerraTrueColorCR':
            return ipybasemaps.NASAGIBS.ModisTerraTrueColorCR
        elif bm == 22 or bm == 'NASAGIBS.ModisTerraBands367CR':
            return ipybasemaps.NASAGIBS.ModisTerraBands367CR
        elif bm == 23 or bm == 'NASAGIBS.ModisTerraBands721CR':
            return ipybasemaps.NASAGIBS.ModisTerraBands721CR
        elif bm == 24 or bm == 'NASAGIBS.ModisAquaTrueColorCR':
            return ipybasemaps.NASAGIBS.ModisAquaTrueColorCR
        elif bm == 25 or bm == 'NASAGIBS.ModisAquaBands721CR':
            return ipybasemaps.NASAGIBS.ModisAquaBands721CR
        elif bm == 26 or bm == 'NASAGIBS.ViirsEarthAtNight2012':
            return ipybasemaps.NASAGIBS.ViirsEarthAtNight2012
        elif bm == 27 or bm == 'Strava.All':
            return ipybasemaps.Strava.All
        elif bm == 28 or bm == 'Strava.Ride':
            return ipybasemaps.Strava.Ride
        elif bm == 29 or bm == 'Strava.Run':
            return ipybasemaps.Strava.Run
        elif bm == 30 or bm == 'Strava.Water':
            return ipybasemaps.Strava.Water
        elif bm == 31 or bm == 'Strava.Winter':
            return ipybasemaps.Strava.Winter
        elif bm == 33 or bm == 'Stamen.Toner':
            return ipybasemaps.Stamen.Toner
        elif bm == 34 or bm == 'Stamen.Watercolor':
            return ipybasemaps.Stamen.Watercolor
        elif bm == 35 or bm == 'Wikimedia':
            #return buildBasemap({'attribution': 'Wikimedia maps beta | &copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors', 
            #                     'max_zoom': 19,
            #                     'name': 'Wikimedia',
            #                     'url': 'https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}@2x.png'})
            return buildBdapLayer(bm, inter.collections.Basemaps.Wikimedia)  # It works as a BDAP layer!
        elif bm == 36 or bm == 'CartoDB.PositronOnlyLabels':
            return buildBasemap({'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
                                 'max_zoom': 19, 'name':
                                 'CartoDB.PositronOnlyLabels',
                                 'url': 'https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/light_only_labels/{z}/{x}/{y}.png'})
        elif bm == 37 or bm == 'CartoDB.DarkMatterOnlyLabels':
            return buildBasemap({'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
                                 'max_zoom': 19,
                                 'name': 'CartoDB.DarkMatterOnlyLabels',
                                 'url': 'https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/dark_only_labels/{z}/{x}/{y}.png'})
        elif bm == 38 or bm == 'CartoDB.VoyagerOnlyLabels':
            return buildBasemap({'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
                                 'max_zoom': 19,
                                 'name': 'CartoDB.VoyagerOnlyLabels',
                                 'url': 'https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/voyager_only_labels/{z}/{x}/{y}.png'})
        elif bm == 39 or bm == 'OpenStreetMap.EC':
            return buildBasemap({'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                                 'max_zoom': 18,
                                 'name': 'OpenStreetMap.EC',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 40 or bm == 'Google.Roadmap':
            return buildBasemap({'attribution': '&copy; <a href="http://www.google.com">Google</a>',
                                 'max_zoom': 18,
                                 'name': 'Google.Roadmap',
                                 'url': 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'})
        elif bm == 41 or bm == 'Google.Satellite':
            return buildBasemap({'attribution': '&copy; <a href="http://www.google.com">Google</a>',
                                 'max_zoom': 18,
                                 'name': 'Google.Satellite',
                                 'url': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'})
        elif bm == 42 or bm == 'Google.Terrain':
            return buildBasemap({'attribution': '&copy; <a href="http://www.google.com">Google</a>',
                                 'max_zoom': 18,
                                 'name': 'Google.Terrain',
                                 'url': 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}'})
        elif bm == 43 or bm == 'Google.Hybrid':
            return buildBasemap({'attribution': '&copy; <a href="http://www.google.com">Google</a>',
                                 'max_zoom': 18,
                                 'name': 'Google.Hybrid',
                                 'url': 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'})
        elif bm == 44 or bm == 'Esri.Ocean':
            return buildBasemap({'attribution': '&copy; <a href="http://www.esri.com">Esri</a>',
                                 'max_zoom': 18,
                                 'name': 'Esri.Ocean',
                                 'url': 'https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}'})
        elif bm == 45 or bm == 'Esri.Terrain':
            return buildBasemap({'attribution': '&copy; <a href="http://www.esri.com">Esri</a>',
                                 'max_zoom': 18,
                                 'name': 'Esri.Terrain',
                                 'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}'})
        elif bm == 46 or bm == 'Esri.ShadedRelief':
            return buildBasemap({'attribution': '&copy; <a href="http://www.esri.com">Esri</a>',
                                 'max_zoom': 18,
                                 'name': 'Esri.ShadedRelief',
                                 'url': 'https://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}'})
        elif bm == 47 or bm == 'Esri.PhysicalMap':
            return buildBasemap({'attribution': '&copy; <a href="http://www.esri.com">Esri</a>', 
                                 'max_zoom': 18,
                                 'name': 'Esri.PhysicalMap',
                                 'url': 'https://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}'})
        elif bm == 48 or bm == 'Stamen.TonerBackground':
            return buildBasemap({'attribution': 'Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>', 
                                 'max_zoom': 18,
                                 'name': 'Stamen.TonerBackground',
                                 'url': 'https://stamen-tiles-a.a.ssl.fastly.net/toner-background/{z}/{x}/{y}.png'})
        elif bm == 49 or bm == 'Stamen.TonerLite':
            return buildBasemap({'attribution': 'Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>', 
                                 'max_zoom': 18,
                                 'name': 'Stamen.TonerLite',
                                 'url': 'https://stamen-tiles-a.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png'})
        elif bm == 50 or bm == 'Stamen.TerrainBackground':
            return buildBasemap({'attribution': 'Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>', 
                                 'max_zoom': 18,
                                 'name': 'Stamen.TerrainBackground',
                                 'url': 'https://stamen-tiles-a.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png'})
        elif bm == 51 or bm == 'CyclOSM':
            return buildBasemap({'attribution': '<a href=\"https://github.com/cyclosm/cyclosm-cartocss-style/releases\" title=\"CyclOSM - Open Bicycle render\">CyclOSM</a> | Map data: &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors', 
                                 'max_zoom': 18,
                                 'name': 'CyclOSM',
                                 'url': 'https://a.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png'})
        elif bm == 52 or bm == 'Stadia.AlidadeSmooth':
            return buildBasemap({'attribution': '&copy; <a href=\"https://stadiamaps.com/\">Stadia Maps</a>, &copy; <a href=\"https://openmaptiles.org/\">OpenMapTiles</a> &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors', 
                                 'max_zoom': 18,
                                 'name': 'Stadia.AlidadeSmooth',
                                 'url': 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}'})
        elif bm == 53 or bm == 'Stadia.AlidadeSmoothDark':
            return buildBasemap({'attribution': '&copy; <a href=\"https://stadiamaps.com/\">Stadia Maps</a>, &copy; <a href=\"https://openmaptiles.org/\">OpenMapTiles</a> &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors', 
                                 'max_zoom': 18,
                                 'name': 'Stadia.AlidadeSmoothDark',
                                 'url': 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}'})
        elif bm == 54 or bm == 'Stadia.OSMBright':
            return buildBasemap({'attribution': '&copy; <a href=\"https://stadiamaps.com/\">Stadia Maps</a>, &copy; <a href=\"https://openmaptiles.org/\">OpenMapTiles</a> &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors', 
                                 'max_zoom': 18,
                                 'name': 'Stadia.OSMBright',
                                 'url': 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}'})
        elif bm == 55 or bm == 'Stadia.Outdoors':
            return buildBasemap({'attribution': '&copy; <a href=\"https://stadiamaps.com/\">Stadia Maps</a>, &copy; <a href=\"https://openmaptiles.org/\">OpenMapTiles</a> &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors', 
                                 'max_zoom': 18,
                                 'name': 'Stadia.Outdoors',
                                 'url': 'https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}'})
        elif bm == 56 or bm == 'CartoDB.PositronNoLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\">CartoDB</a>', 
                                 'max_zoom': 18,
                                 'name': 'CartoDB.PositronNoLabels',
                                 'url': 'https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png'})
        elif bm == 57 or bm == 'CartoDB.DarkMatterNoLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\">CartoDB</a>', 
                                 'max_zoom': 18,
                                 'name': 'CartoDB.DarkMatterNoLabels',
                                 'url': 'https://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png'})
        elif bm == 58 or bm == 'CartoDB.Voyager':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\">CartoDB</a>', 
                                 'max_zoom': 18,
                                 'name': 'CartoDB.Voyager',
                                 'url': 'https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png'})
        elif bm == 59 or bm == 'CartoDB.VoyagerNoLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &copy; <a href=\"http://cartodb.com/attributions\">CartoDB</a>', 
                                 'max_zoom': 18,
                                 'name': 'CartoDB.VoyagerNoLabels',
                                 'url': 'https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png'})
        elif bm == 60 or bm == 'Gisco.OSMCartoComposite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoComposite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 61 or bm == 'Gisco.OSMCartoBackground':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoBackground',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoBackground/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 62 or bm == 'Gisco.OSMCartoLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoLabels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoLabels/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 63 or bm == 'Gisco.OSMBlossomComposite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBlossomComposite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBlossomComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 64 or bm == 'Gisco.OSMBlossomBackground':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBlossomBackground',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBlossomBackground/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 65 or bm == 'Gisco.OSMBlossomLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBlossomLabels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBlossomLabels/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 66 or bm == 'Gisco.OSMPositronComposite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMPositronComposite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMPositronComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 67 or bm == 'Gisco.OSMPositronBackground':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMPositronBackground',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMPositronBackground/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 68 or bm == 'Gisco.OSMPositronLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMPositronLabels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMPositronLabels/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 69 or bm == 'Gisco.OSMCartoV4Composite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoV4Composite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Composite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 70 or bm == 'Gisco.OSMCartoV4Background':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoV4Background',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Background/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 71 or bm == 'Gisco.OSMCartoV4Labels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoV4Labels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Labels/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 72 or bm == 'Gisco.OSMBrightComposite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBrightComposite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBrightComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 73 or bm == 'Gisco.OSMBrightBackground':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBrightBackground',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBrightBackground/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 74 or bm == 'Gisco.OSMBrightLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMBrightLabels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMBrightLabels/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 75 or bm == 'Gisco.OSMCartoHDMComposite':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoHDMComposite',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoHDMComposite/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 76 or bm == 'Gisco.OSMCartoHDMBackground':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoHDMBackground',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoHDMBackground/EPSG3857/{z}/{x}/{y}.png'})
        elif bm == 77 or bm == 'Gisco.OSMCartoHDMLabels':
            return buildBasemap({'attribution': '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a> &amp; ESTAT', 
                                 'max_zoom': 18,
                                 'name': 'Gisco.OSMCartoHDMLabels',
                                 'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoHDMLabels/EPSG3857/{z}/{x}/{y}.png'})
        
        # Additional basemaps from BDAP
        elif bm == 'BDAP.Elevation.Merit':
            return buildBdapLayer(bm, inter.collections.BaseData.Elevation.MERIT.Hillshade)
        elif bm == 'BDAP.Elevation.Gebco':
            return buildBdapLayer(bm, inter.collections.BaseData.Elevation.GEBCO.Hillshade)
        elif bm == 'BDAP.GridSystems.MGRS':
            return buildBdapLayer(bm, inter.collections.BaseData.GeographicalGridSystems.MGRS)
        elif bm == 'BDAP.GridSystems.Landsat':
            return buildBdapLayer(bm, inter.collections.BaseData.GeographicalGridSystems.Landsat_WRS2_Descending)
        elif bm == 'BDAP.GridSystems.UTMgrid':
            return buildBdapLayer(bm, inter.collections.BaseData.GeographicalGridSystems.UTMgrid)
        elif bm == 'BDAP.Orthoimagery.Terracolor':
            return buildBdapLayer(bm, inter.collections.BaseData.Orthoimagery.Terracolor)
        elif bm == 'BDAP.GlobalForestChange.LandsatMosaic':
            return buildBdapLayer(bm, inter.collections.BaseData.Landcover.GFC_UMD.Version_1_7.last)
        elif bm == 'BDAP.GHSL.S2Mosaic':
            return buildBdapLayer(bm, inter.collections.Products.Mosaics.Global.GHS_composite_S2_L1C_2017_2018_GLOBE_R2020A)
        elif bm == 'BDAP.Core003.SpotMosaic':
            return buildBdapLayer(bm, inter.collections.Products.Mosaics.Europe.Core003.Seamline)

    return bm


# Retuns the list of all the basemap names
def basemapList(addBDAPbasemaps=True, removeBasemaps=[]):
    c = inter.ImageCollection("BASEMAP")
    names = list(c.listBasemaps())
    
    # Remove basemaps not working
    names.remove('OpenStreetMap.BlackAndWhite')
    names.remove('HikeBike.HikeBike')
    names.remove('Hydda.Base')
    names.remove('Hydda.Full')
    names.remove('OpenRailwayMap')
    names.remove('OpenMapSurfer.Grayscale')
    names.remove('OpenMapSurfer.Roads')
    names.remove('Stadia.AlidadeSmooth')
    names.remove('Stadia.AlidadeSmoothDark')
    names.remove('Stadia.OSMBright')
    names.remove('Stadia.Outdoors')
    
    # Remove basemaps not wanted by the caller
    for bm in removeBasemaps:
        if bm in names:
            names.remove(bm)
    
    # Add BDAP basemaps
    if addBDAPbasemaps:
        names.append('BDAP.Elevation.Merit')
        names.append('BDAP.Elevation.Gebco')
        names.append('BDAP.GridSystems.MGRS')
        names.append('BDAP.GridSystems.Landsat')
        names.append('BDAP.GridSystems.UTMgrid')
        names.append('BDAP.Orthoimagery.Terracolor')
        names.append('BDAP.GlobalForestChange.LandsatMosaic')
        names.append('BDAP.GHSL.S2Mosaic')
        names.append('BDAP.Core003.SpotMosaic')
        
    names = sorted(names)
    return names


# Assign an attribution to a TileLayer if it doesn't already have it
def assignAttribution(bm, tilelayer):
    if len(tilelayer.attribution) <= 0: 
        if bm in basemapsAttribution:
            tilelayer.attribution = basemapsAttribution[bm]


# Given an int, a string or a basemaps object returns a tile layer to add to an ipyleaflet map
def basemapTileLayer(bm):
    base = preprocessBasemap(bm)

    # basemaps that need a background
    if bm in ['BDAP.Elevation.Merit', 'BDAP.GridSystems.MGRS', 'BDAP.GridSystems.Landsat', 'BDAP.GridSystems.UTMgrid', 
              'BDAP.Orthoimagery.Terracolor', 'BDAP.GHSL.S2Mosaic', 'BDAP.Core003.SpotMosaic']:

        backbm = 'Gisco.OSMCartoComposite'
        back = preprocessBasemap(backbm)
        tileback = basemap_to_tiles(back)
        assignAttribution(backbm,tileback)
        
        tilebase = basemap_to_tiles(base)
        assignAttribution(bm,tilebase)
        tilelayer = LayerGroup(name=bm,layers=(tileback,tilebase))
    else:
        tilelayer = basemap_to_tiles(base)
        assignAttribution(bm,tilelayer)

    tilelayer.base = True
    return tilelayer



# Clear the map
def map_clear(m):
    emptyLayer = basemap_to_tiles(emptyBasemap)
    emptyLayer.base = True
    
    m.clear()
    m.add_layer(emptyLayer)
    m.layers = (m.layers[1],)
    
    
# Change the basemap for a map and returns the layer
def map_setbasemap(m, bm=None):
    if bm is None:
        layer = basemap_to_tiles(emptyBasemap)
        layer.base = True
    else:
        layer = basemapTileLayer(bm)
    newlayers = [layer] + list(m.layers[1:])
    m.layers = tuple(newlayers)
   
    return layer

    
#####################################################################################################################################################
# Basemaps selection widget class
#####################################################################################################################################################
class basemaps():
    """
    Treeview widget to select a basemap for an ipyleaflet map.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance on which the selected basemap has to be set as backdrop layer
    color : str, optional
        Color to use for the widget (default is settings.color_first)
    dark : bool, optional
        If True, the widget will have a dark background (default is settings.dark_mode)
    width : int, optional
        Width of the widget in pixels (default is 320)
    height : int, optional
        Height of the widget in pixels (default is 650)
    addBDAPbasemaps : bool, optional
        If True the treeview will contain also some BDAP layers selectable as basemaps (default is True)
    removeBasemaps : list of str, optional
        List of basemaps names to be removed from the widget (default is [])
    rootName: str, optional
        Name to use as the root node of the basemaps treeview (default is 'Basemaps')
    onchange : function, optional
        Python function to call when the user selects a different basemap. The function will receive no parameters. (default is None)
        
    Example
    -------
    Creation of a basemap selection widget::
        
        from jeodpp import inter, imap
        from ipywidgets import widgets, Layout

        from vois.vuetify import basemaps

        height = 650

        m = imap.Map(layout=Layout(height='%dpx'%height))

        b = basemaps.basemaps(m, height=height, dark=False)

        display(widgets.HBox([b.draw(),m]))

    .. figure:: figures/basemaps.png
       :scale: 100 %
       :alt: basemaps widget

       Example of a basemaps selection widget
    """
    
    def __init__(self,
                 m,
                 color=settings.color_first,
                 dark=settings.dark_mode,
                 width=320,
                 height=650,
                 addBDAPbasemaps=True,
                 removeBasemaps=[],
                 rootName='Basemaps',
                 onchange=None):
        
        self.m        = m
        self.color    = color
        self.dark     = dark
        self.width    = width
        self.height   = height
        self.onchange = onchange
        
        self.name = 'OpenStreetMap.EC'
        self.basemap_layer = basemapTileLayer(self.name)
    
        self.treecard = treeview.createTreeviewFromList(basemapList(addBDAPbasemaps=addBDAPbasemaps,removeBasemaps=removeBasemaps),
                                                        rootName=rootName, separator='.', 
                                                        expand_selection_to_parents=False,  substitutionDict={},
                                                        color=self.color, dark=self.dark, width=self.width, height=self.height, 
                                                        on_activated=self.__on_activated, selectable=False, activatable=True, 
                                                        active='OpenStreetMap.EC', opened=['Basemaps', 'OpenStreetMap'],
                                                        displayfullname=False, disabled=[])

        self.top = treeview.treeviewOperations(self.treecard)

        self.reset()
        
        
    # Set the default basemap
    def reset(self):
        """
        Set the default basemap (OpenStreetMap.EC)
        """
        self.name = 'OpenStreetMap.EC'
        self.__on_activated(self.name)
        

    # Manage activation of a node of the tree: change the basemap on the self.m map instance
    def __on_activated(self, arg):
        firstchild = self.top.getFirstChildFullname(arg)
        if firstchild:  # if the activated node has children: activate its first child
            self.top.setActive(firstchild)
        else:
            self.name = arg
            self.basemap_layer = map_setbasemap(self.m, arg)
            if not self.onchange is None:
                self.onchange()

            
    # Returns the vuetify object to display (the treeview widget)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Card containing the treeview)"""
        return self.treecard
            
        
    # current_layer property
    @property
    def current_layer(self):
        """
        Get the currently select layer (instance of ipyleaflet.leaflet.TileLayer class or ipyleaflet.leaflet.LayerGroup class)
        """
        return self.basemap_layer

    
    # value property: get and sets the current name of the basemap
    @property
    def value(self):
        """
        Get/Set the active basemap name.
        
        Returns
        --------
        name : str
            Name of the basemap

        Example
        -------
        Programmatically select one of the basemaps and print the value selected::
            
            b.value = 'Esri.WorldImagery'
            print(b.value)
        
        """
        return self.name
    
    # Set the current basemap by passing a name
    @value.setter
    def value(self, name):
        self.name = name
        self.__on_activated(self.name)
    
        