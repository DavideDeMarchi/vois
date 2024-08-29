"""Utilities functions for maps"""
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

import ipyleaflet
from ipyleaflet import basemaps, basemap_to_tiles, WidgetControl
from PIL import Image, ImageDraw
from io import BytesIO
import ipyvuetify
import ipyvuetify as v

from osgeo import ogr, osr
from jeodpp import inter       # V.I.: importing inter after GDAL seem to solve the HDF5 C errors

import requests
import math


# Symbols dimension in pixels
SMALL_SYMBOLS_DIMENSION = 30
MEDIUM_SYMBOLS_DIMENSION = 80
LARGE_SYMBOLS_DIMENSION = 256

# Base URL for generating images from symbols
SYMBOLS_URL = 'https://jeodpp.jrc.ec.europa.eu/jiplib-view?x=0&y=0&z=1&procid=%s'


#####################################################################################################################################################
# Management of basemaps and layers (see viewer.py of Lucas)
#####################################################################################################################################################

# Build a basemap that works in old and new versions of ipyleaflet
def buildBasemap(oldstyledictionary):
    return basemap_to_tiles(oldstyledictionary)


def EmptyBasemap():  # gray background
    return buildBasemap({'attribution': '',
                         'max_zoom': 21, 
                         'max_native_zoom': 21,
                         'name': 'Empty basemap',
                         'url': 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/gray.png'})


def OSM_EC():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Gisco.OSMCartoV4Composite',
                         'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Composite/EPSG3857/{z}/{x}/{y}.png'})


def CartoLabels():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Gisco.OSMCartoV4Labels',
                         'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Labels/EPSG3857/{z}/{x}/{y}.png'})


def EsriWorldImagery():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Esri.WorldImagery',
                         'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg'})


def GoogleRoadmap():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Roadmap',
                         'url': 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'})


def GoogleSatellite():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Satellite',
                         'url': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'})


def GoogleHybrid():
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Hybrid',
                         'url': 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'})


# Any ImageProcess or VectorLayer: returns an ipyleaflet.TileLayer instance
def BDAPLayer(p):
    procid = p.toLayer()
    #return ipyleaflet.TileLayer(url='https://jeodpp.jrc.ec.europa.eu/jiplib-view-dev?x={x}&y={y}&z={z}&procid=%s'%procid, max_zoom=21, max_native_zoom=21)
    return ipyleaflet.TileLayer(url='https://jeodpp.jrc.ec.europa.eu/jiplib-view?x={x}&y={y}&z={z}&procid=%s'%procid, max_zoom=21, max_native_zoom=21)


# Add the layer to a map or substitute it using the name
def addLayer(m, tLayer, name, opacity=1.0):
    removeAllPopups(m)
    alreadyPresent = False
    tLayer.name = name
    tLayer.opacity = opacity
    for layer in m.layers:
        if name == layer.name:
            m.substitute_layer(layer, tLayer)
            alreadyPresent = True
            break

    if not alreadyPresent:
        m.add_layer(tLayer)

    return tLayer


# Search for a layer of a map by name
def getLayer(m, name):
    for layer in m.layers:
        if name == layer.name:
            return layer
    return None


# Remove a layer given its name
def removeLayer(m, name):
    for layer in m.layers:
        if name == layer.name:
            m.remove_layer(layer)


# Remove all popups from the map
def removeAllPopups(m):
    for layer in reversed(m.layers):
        if isinstance(layer, ipyleaflet.leaflet.Popup):
            m.remove_layer(layer)


# Remove all layer except current basemap
def clear(m):
    baselayer = ipyleaflet.basemap_to_tiles(m.basemap)
    baselayer.base = True
    m.clear_layers()
    m.add_layer(baselayer)


# Zoom a map to a rectangle
def zoomToExtents(m, xmin, ymin, xmax, ymax, epsg=4326):

    m.fit_bounds([[ymin, xmin], [ymax, xmax]])
    return


def zoomToExtents_OLD(m, xmin, ymin, xmax, ymax, epsg=4326):
    def transformPoint(x, y, coordtrans):
        point = ogr.CreateGeometryFromWkt("POINT (%f %f)"%(x,y))
        point.Transform(coordtrans)
        pt = point.GetPoint(0)
        return pt[0], pt[1]

    def transformExtent(xmin, ymin, xmax, ymax, epsgsource, epsgtarget):
        if epsgsource == epsgtarget:
            return xmin, ymin, xmax, ymax

        source = osr.SpatialReference()
        source.ImportFromEPSG(epsgsource)
        source.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

        target = osr.SpatialReference()
        target.ImportFromEPSG(epsgtarget)
        target.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

        ct = osr.CoordinateTransformation(source, target)

        x1, y1 = transformPoint(xmin, ymin, ct)
        x2, y2 = transformPoint(xmin, ymax, ct)
        x3, y3 = transformPoint(xmax, ymin, ct)
        x4, y4 = transformPoint(xmax, ymax, ct)

        targetxmin = min(x1, x2, x3, x4)
        targetxmax = max(x1, x2, x3, x4)
        targetymin = min(y1, y2, y3, y4)
        targetymax = max(y1, y2, y3, y4)

        return targetxmin, targetymin, targetxmax, targetymax

    geoxmin, geoymin, geoxmax, geoymax = transformExtent(xmin, ymin, xmax, ymax, epsg, 4326)
    mercxmin, mercymin, mercxmax, mercymax = transformExtent(geoxmin, geoymin, geoxmax, geoymax, 4326, 3857)

    distance = mercxmax - mercxmin

    # Given a distance on a parallel, returns the number of pixels at a certain zoom level
    def pixels(distance, zoom):
        return 256 * (distance/40000000) * math.pow(2,zoom)

    # See https://gis.stackexchange.com/questions/19632/how-to-calculate-the-optimal-zoom-level-to-display-two-or-more-points-on-a-map
    zoom = 0
    while pixels(distance, zoom) < 500:
        zoom = zoom + 1

    m.center = [(geoymin+geoymax)*0.5, (geoxmin+geoxmax)*0.5]
    m.zoom = zoom


#####################################################################################################################################################
# Display of coordinated at mousemove on a map
#####################################################################################################################################################
# Searches the controls of the Map m to find a control added as a Widget by using its name
def getCardByName(m, name, position='topright', class_='pa-0 ma-0'):
    for control in m.controls:
        if isinstance(control, ipyleaflet.leaflet.WidgetControl):
            if isinstance(control.widget, ipyvuetify.generated.Card):
                if control.widget.active_class == name:
                    return control.widget

    # If not found: add it to the map!
    card = v.Card(flat=True, class_=class_, active_class=name)
    wc = WidgetControl(widget=card, position=position)
    m.add_control(wc)
    return card

    
# Remove a WidgetControl from the map given its name, if present
def removeCardByName(m, name):
    for control in m.controls:
        if isinstance(control, ipyleaflet.leaflet.WidgetControl):
            if isinstance(control.widget, ipyvuetify.generated.Card):
                if control.widget.active_class == name:
                    m.remove_control(control)


#####################################################################################################################################################
# Display of coordinated at mousemove on a map
#####################################################################################################################################################
# Searches the controls of the Map m to find the coordinates control
# N.B.: the Coordinates control is a v.Card having active_class == 'Coordinates' (so that it can be retrieved from the list of m.controls)
def getCoordinatesCard(m):
    return getCardByName(m, 'Coordinates', 'topright')

    
# Remove the Coordinates WidgetControl from the map, if present
def removeCoordinates(m):
    removeCardByName(m, 'Coordinates')


#####################################################################################################################################################
# Functions for vector layers management and display
#####################################################################################################################################################

# Apply a symbol to a category of a VectorLayer instance
def applySymbol(vectorlayer, rule='all', symbol=[]):
    for layer in symbol:
        style = "default"
        for member in layer:
            symbolizer, attribute, value = member
            vectorlayer.set(style, rule, symbolizer, attribute, str(value))


# Generate an image from a symbol
def symbol2Image(symbol=[], size=1, layer_type='Point', clipdimension=MEDIUM_SYMBOLS_DIMENSION, showborder=False):
    doclip = False
    if layer_type == 'Line':
        if size >= 3:    wkt = 'LINESTRING (-170 82, -100 55, -60 70, -10 38)'
        elif size == 2:  wkt = 'LINESTRING (-175 83, -158 81, -148 83, -129 81)'
        else:            wkt = 'LINESTRING (-177 84.45, -171 83.9, -167.4 84.25, -161 83.75)'
    elif layer_type == 'Polygon':
        if size >= 3:    wkt = 'POLYGON ((-170 83.85, -170 10, -10 10, -10 83.85, -170 83.85))'
        elif size == 2:  wkt = 'POLYGON ((-175 84.5, -175 78, -128.5 78, -128.5 84.5, -175 84.5))'
        else:            wkt = 'POLYGON ((-178 84.85, -178 83.2, -160.5 83.2, -160.5 84.85, -178 84.85))'
    else:
        if size >= 3:    wkt = 'POINT (-90 65)'
        elif size == 2:  wkt = 'POINT (-152 82)'
        else:            wkt = 'POINT (-169.52 84.05)'

    if size >= 3:
        if clipdimension < LARGE_SYMBOLS_DIMENSION:
            doclip = True
    elif size == 2:
        if clipdimension < MEDIUM_SYMBOLS_DIMENSION:
            doclip = True
    else:
        if clipdimension < SMALL_SYMBOLS_DIMENSION:
            doclip = True

    v = inter.Collection(inter.collections.Vector)
    v.geomAdd(wkt)
    v.remove('default', 'all')
    applySymbol(v, 'all', symbol)
    ip = v.process()
    ip.toLayer()
    url = SYMBOLS_URL % ip.getProcessID()
    response = requests.get(url)
    if len(response.content) > 5 and response.content[0] == 137 and response.content[1] == 80 and response.content[2] == 78 and response.content[3] == 71 and response.content[4] == 13:
        img = Image.open(BytesIO(response.content))
        if size == 2:
            img = img.crop((0, 0, MEDIUM_SYMBOLS_DIMENSION, MEDIUM_SYMBOLS_DIMENSION))
        elif size < 2:
            img = img.crop((0, 0, SMALL_SYMBOLS_DIMENSION, SMALL_SYMBOLS_DIMENSION))

        if doclip:
            s = img.size
            cx = s[0]/2
            cy = s[1]/2
            img = img.crop((cx-clipdimension/2, cy-clipdimension/2, cx+clipdimension/2, cy+clipdimension/2))
    else:
        # print('URL with errors:',url)
        if size >= 3:    img = Image.new("RGB", (LARGE_SYMBOLS_DIMENSION,  LARGE_SYMBOLS_DIMENSION),  (255, 255, 255))
        elif size == 2:  img = Image.new("RGB", (MEDIUM_SYMBOLS_DIMENSION, MEDIUM_SYMBOLS_DIMENSION), (255, 255, 255))
        else:            img = Image.new("RGB", (SMALL_SYMBOLS_DIMENSION,  SMALL_SYMBOLS_DIMENSION),  (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0),"Error",(0,0,0))

    # Add a thin black border
    if showborder:
        draw = ImageDraw.Draw(img)
        s = img.size
        draw.rectangle(((0, 0), (s[0]-1, s[1]-1)), outline='black')
    return img


# Change color of a symbol and returns the modified symbol
def setColor(symbol, color='#ff0000', fillColor='#ff0000', fillOpacity=1.0, strokeColor='#ffff00', strokeWidth=0.5, scalemin=None, scalemax=None):
    newsymbol = []
    for layer in symbol:
        newlayer = []
        for member in layer:
            symbolizer,attribute,value = member

            if value == 'COLOR':
                value = color

            if value == 'FILL-COLOR':
                value = fillColor

            if value == 'FILL-OPACITY':
                value = fillOpacity

            if value == 'STROKE-COLOR':
                value = strokeColor

            if value == 'STROKE-WIDTH':
                value = strokeWidth

            if value == 'SCALE-MIN':
                value = scalemin

            if value == 'SCALE-MAX':
                value = scalemax

            if value is not None:
                newlayer.append((symbolizer,attribute,value))

        newsymbol.append(newlayer)

    return newsymbol


#####################################################################################################################################################
# Save a map view in a PIL image
#####################################################################################################################################################
def toImage(m):

    # Bounds and zoom of the current view
    (latmin, lonmin), (latmax, lonmax) = m.bounds
    zoom = m.zoom

    # URLs of all the Tilelayer on the map
    baseUrls = [x.url for x in m.layers if type(x) == ipyleaflet.leaflet.TileLayer]

    # Opacities
    opacities = [x.opacity for x in m.layers if type(x) == ipyleaflet.leaflet.TileLayer]

    # Convert lat/lon/zoom to xtile,ytile.
    # See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    def latlon2tile(lat_deg, lon_deg, zoom):
        lat_rad = (lat_deg * math.pi) / 180.0
        n = math.pow(2,zoom)
        xtile = n * ((lon_deg + 180.0) / 360.0)
        ytile = n * (1 - (math.log(math.tan(lat_rad) + 1.0/math.cos(lat_rad)) / math.pi)) / 2
        return xtile, ytile

    xtile1f, ytile2f = latlon2tile(latmin, lonmin, zoom)
    xtile2f, ytile1f = latlon2tile(latmax, lonmax, zoom)

    xtile1 = int(xtile1f)
    xtile2 = int(xtile2f)
    ytile1 = int(ytile1f)
    ytile2 = int(ytile2f)

    # Amount of pixels to crop on each side
    dx1 = 256*(xtile1f-xtile1)
    dx2 = 256*(xtile2+1-xtile2f)
    dy1 = 256*(ytile1f-ytile1)
    dy2 = 256*(ytile2+1-ytile2f)

    dx1 = round(dx1*100)//100
    dx2 = round(dx2*100)//100
    dy1 = round(dy1*100)//100
    dy2 = round(dy2*100)//100

    # Number of tiles
    nx = xtile2 - xtile1 + 1
    ny = ytile2 - ytile1 + 1

    # Dimension of the overall image
    w = 256 * nx
    h = 256 * ny
    imageTotal = Image.new(mode="RGBA", size=(w,h))

    # Substitute x,y,z into a TileService URL
    def url(baseurl, x, y, zoom):
        return baseurl.replace('{x}', str(int(x))).replace('{y}', str(int(y))).replace('{z}', str(int(zoom)))

    # Cycle on all tiles and compose the overall image
    for x in range(nx):
        xt = xtile1 + x
        xpos = x*256
        for y in range(ny):
            yt = ytile1 + y
            ypos = y*256
            for baseurl, opacity in zip(baseUrls, opacities):
                image = Image.open(requests.get(url(baseurl, xt, yt, zoom), stream=True).raw)
                image = image.convert('RGBA')

                if opacity < 1.0:
                    # Split image in 4 channels
                    (r, g, b, a) = image.split()

                    # Change the alpha channel
                    # See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.eval
                    a = Image.eval(a, lambda px: opacity*px)

                    # Merge 4 channels
                    image = Image.merge('RGBA', (r, g, b, a))

                # Transparent paste!!!
                # See https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
                imageTotal.paste(image, (xpos, ypos), mask=image)

    # Crop the image
    area_crop = (dx1, dy1, w-dx2, h-dy2)
    return imageTotal.crop(area_crop)