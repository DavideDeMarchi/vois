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
from ipywidgets import widgets, Layout
import ipyleaflet
from ipyleaflet import basemaps, basemap_to_tiles, WidgetControl, Rectangle
from PIL import Image
import ipyvuetify
import ipyvuetify as v

import requests
import math


MAPCARD_COORDINATES = 'Coordinates'
MAPCARD_OVERVIEW    = 'Overview'


#####################################################################################################################################################
# Management of basemaps and layers (see viewer.py of Lucas)
#####################################################################################################################################################

# Build a basemap that works in old and new versions of ipyleaflet
def buildBasemap(oldstyledictionary):
    return basemap_to_tiles(oldstyledictionary)


def EmptyBasemap():  # gray background
    """
    Returns a fully gray basemap TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21, 
                         'max_native_zoom': 21,
                         'name': 'Empty basemap',
                         'url': 'https://jeodpp.jrc.ec.europa.eu/services/shared/pngs/gray.png'})


def OSM_EC():
    """
    Returns a OpenStreetMap European Commission compliant TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Gisco.OSMCartoV4Composite',
                         'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Composite/EPSG3857/{z}/{x}/{y}.png'})


def CartoLabels():
    """
    Returns a TileLayer instance displaying only EC compliant labels.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Gisco.OSMCartoV4Labels',
                         'url': 'https://gisco-services.ec.europa.eu/maps/tiles/OSMCartoV4Labels/EPSG3857/{z}/{x}/{y}.png'})


def EsriWorldImagery():
    """
    Returns Esri WorldImagery TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Esri.WorldImagery',
                         'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg'})


def GoogleRoadmap():
    """
    Returns Google Roadmap TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Roadmap',
                         'url': 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'})


def GoogleSatellite():
    """
    Returns Google Satellite TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Satellite',
                         'url': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'})


def GoogleHybrid():
    """
    Returns Google Hybrid TileLayer instance.
    """
    return buildBasemap({'attribution': '',
                         'max_zoom': 21,
                         'max_native_zoom': 21,
                         'name': 'Google.Hybrid',
                         'url': 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'})


# Any ImageProcess or VectorLayer: returns an ipyleaflet.TileLayer instance
def BDAPLayer(p):
    """
    Returns a TileLayer instance from a BDAP ImageProcess or VectorLayer instance passed as input parameter.
    """
    procid = p.toLayer()
    return ipyleaflet.TileLayer(url='https://jeodpp.jrc.ec.europa.eu/jiplib-view?x={x}&y={y}&z={z}&procid=%s'%procid, max_zoom=21, max_native_zoom=21)


# Add the layer to a map or substitute it using the name
def addLayer(m, tLayer, name, opacity=1.0):
    """
    Add or substitutes a layer given a name.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map where the layer is to be added.
    tLayer : ipyleaflet.TileLayer instance
        Layer to add to the map.
    name : str
        Name of the layer
    opacity : float, optional
        Opacity of the layer in the [0.0,1.0] range. Default is 1.0.

    Returns
    ----------
    tLayer : ipyleaflet.TileLayer instance
        The layer added to the map.
    """
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
        m.add(tLayer)

    return tLayer


# Search for a layer of a map by name
def getLayer(m, name):
    """
    Search for a layer of a map by name.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map where to search for the layer.
    name : str
        Name of the layer.

    Returns
    ----------
    tLayer : ipyleaflet.TileLayer instance
        If a layer with the name exists on the map it is returned, otherwise the function returns None.
    """
    for layer in m.layers:
        if name == layer.name:
            return layer
    return None


# Remove a layer given its name
def removeLayer(m, name):
    """
    Remove a layer from a map given its name.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map where to search for the layer.
    name : str
        Name of the layer to remove.
    """
    for layer in m.layers:
        if name == layer.name:
            m.remove(layer)


# Remove all popups from the map
def removeAllPopups(m):
    """
    Remove all instances of ipyleaflet.leaflet.Popup class present in the map.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map where the popups must be removed.
    """
    for layer in reversed(m.layers):
        if isinstance(layer, ipyleaflet.leaflet.Popup):
            m.remove(layer)


# Remove all layer except current basemap
def clear(m):
    """
    Remove all layer except current first layer from a map.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map to be cleared.
    """
    if len(m.layers) > 0:
        baselayer = m.layers[0]
    else:
        baselayer = None
    #baselayer = ipyleaflet.basemap_to_tiles(m.basemap)
    #baselayer.base = True
    m.clear_layers()
    
    if baselayer is not None:
        m.add(baselayer)


# Zoom a map to a rectangle
def zoomToExtents(m, xmin, ymin, xmax, ymax, epsg=4326):
    m.fit_bounds([[ymin, xmin], [ymax, xmax]])
    return


#####################################################################################################################################################
# Display of coordinated at mousemove on a map
#####################################################################################################################################################
# Searches the controls of the Map m to find a control added as a Widget by using its name
def getCardByName(m, name, position='topright', class_='pa-0 ma-0'):
    """
    Searches the controls of the Map m to find a control added as a Widget by using its name. If the control is not found, a new control is added to the map.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance.
    name : str
        Name of the card to search for.
    position : str, optional
        Position of the card inside the map. Valid positions are 'bottomleft', 'bottomright', 'topleft' and 'topright'. Default is 'topright'.
    class_ : str, optional
        Margins to set for the adde card (default is 'pa-0 ma-0')

    Returns
    -------
    c : v.Card instance
        The card added to the map that can be filled with any type of widgets content by setting its children property.
    """
    for control in m.controls:
        if isinstance(control, ipyleaflet.leaflet.WidgetControl):
            if isinstance(control.widget, ipyvuetify.generated.Card):
                if control.widget.active_class == name:
                    return control.widget

    # If not found: add it to the map!
    card = v.Card(flat=True, class_=class_, active_class=name)
    wc = WidgetControl(widget=card, position=position)
    m.add(wc)
    return card

    
# Remove a WidgetControl from the map given its name, if present
def removeCardByName(m, name):
    """
    Remove a WidgetControl Card from the map given its name, if present.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance.
    name : str
        Name of the card to search for.
    """
    for control in m.controls:
        if isinstance(control, ipyleaflet.leaflet.WidgetControl):
            if isinstance(control.widget, ipyvuetify.generated.Card):
                if control.widget.active_class == name:
                    m.remove(control)


#####################################################################################################################################################
# Display of coordinated at mousemove on a map
#####################################################################################################################################################
# Searches the controls of the Map m to find the coordinates control
# N.B.: the Coordinates control is a v.Card having active_class == 'Coordinates' (so that it can be retrieved from the list of m.controls)
def getCoordinatesCard(m):
    """
    Searches the controls of the Map m to find the coordinates control (where the lat/lon coordinates are displayed at mouse move) and returns a v.Card instance.
    """
    return getCardByName(m, MAPCARD_COORDINATES, 'topright')

    
# Remove the Coordinates WidgetControl from the map, if present
def removeCoordinates(m):
    """
    Remove the WidgetControl dedicated to the display of the coordinates at mouse move.
    """
    removeCardByName(m, MAPCARD_COORDINATES)

    
#####################################################################################################################################################
# Display of an overview map
#####################################################################################################################################################

# Add an overview map
def addOverview(m, color='red', position='bottomright', overviewLayer=None):
    """
    Add an overview map.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance.
    color : str, optional
        Color of the rectangle that displays the current zoom of the map inside the overview map.
    position : str, optional
        Position of the card inside the map. Valid positions are 'bottomleft', 'bottomright', 'topleft' and 'topright'. Default is 'bottomright'.
    overviewLayer : ipyleaflet.TileLayer instance, optional
        Optional layer to be displayed on the overview map (default is None).
    """

    removeCardByName(m, MAPCARD_OVERVIEW)
    
    # Create the overview map
    moverview = ipyleaflet.Map(center=[57,10], zoom=2, scroll_wheel_zoom=False, zoom_control=False, dragging=False,
                               attribution_control=False, layout=Layout(height='200px', width='200px'), max_zoom=2)

    # Add the overview layer
    if not overviewLayer is None:
        addLayer(moverview, overviewLayer, 'CustomLayer')

    # Set the card for the overview
    card = getCardByName(m, MAPCARD_OVERVIEW, position=position, class_='pa-0 ma-1')
    card.style_ = 'overflow: hidden;'
    card.children = [moverview]

    # Add the current zoom
    rect = Rectangle(color=color, fill=False, bounds=m.bounds)
    moverview.add(rect)

    # Update the rectangle at each zoom/pan on the main map
    def onMapBoundsChanged(*args):
        nonlocal rect
        newrect = Rectangle(color=color, fill=False, bounds=m.bounds)
        moverview.substitute_layer(rect, newrect)
        rect = newrect

    m.observe(onMapBoundsChanged, 'bounds')
    

# Remove the overview card from the map
def removeOverview(m):
    """
    Remove the overview map, if present.
    """
    removeCardByName(m, MAPCARD_OVERVIEW)

    
#####################################################################################################################################################
# Save a map view in a PIL image
#####################################################################################################################################################
def toImage(m):
    """
    Save the current map content as a PIL image.

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance.

    Returns
    -------
    img : PIL/Pillow image
        A raster image displaying the current content of the map.
    """

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