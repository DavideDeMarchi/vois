"""Utility functions for the creation of interactive maps using ipyleaflet Map."""
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
import pandas as pd
import numpy as np
import json
import random
from pathlib import Path

from ipywidgets import widgets, Layout, HTML, Label
from ipyleaflet import Map, basemaps, GeoJSON, Popup, SearchControl, WidgetControl, LegendControl, ScaleControl, FullScreenControl

try:
    from . import colors
    from . import geojsonUtils
except:
    import colors
    import geojsonUtils


###########################################################################################################################################################################
# Simplified way to create a vector layer displaying the countries of the world.
# Vector data is taken from folder data/ne_50m_admin_0_countries.geojson
# Input values to assign to countries come from a Pandas Dataframe df containing a column with iso2code and a column with values
# Returns a Map instance
###########################################################################################################################################################################
def countriesMap(df,                          # Pandas dataframe indexed on iso2_code and containing 'value' and 'label' columns
                 code_column=None,            # Name of the column containing the code of the country (None = the country code is the index of the dataframe)
                 value_column='value',        # Name of the column containing the value
                 codes_selected=[],           # codes of the countries selected
                 center=None,                 # [lat,lon] to center the map
                 zoom=None,                   # initial zoom level for the map
                 width ='99%',                # width of the map
                 height='400px',              # height of the map
                 min_width=None,              # min_width of the map
                 basemap=basemaps.OpenStreetMap.Mapnik, # Basemap to use
                 detailedcountries=False,     # If True loads the detailed country geojson
                 colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
                 stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                 stroke='#232323',            # stroke color for countries border
                 stroke_selected='#00ffff',   # stroke color for border of selected country
                 stroke_width=3.0,            # border width for countries polygons
                 decimals=2,                  # Number of decimals for the legend number display
                 minallowed_value=None,       # Minimum value allowed
                 maxallowed_value=None,       # Maximum value allowed
                 style      ={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6},    # Style to apply to the features
                 hover_style={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85}):  # Style to apply to the features when hover
    """
    Creation of an interactive map to display the countries of the world. An input Pandas DataFrame df is used to join a column of numeric values to the countries, using the iso2code (ISO 3166-2) as internal key attribute. Once the values are assigned to the countries, a graduated legend is calculated based on mean and standard deviation of the assigned values. A input list of colors is used to represent the countries given their assigned value.

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame to use for assigning values to the countries. It has to contain at least a column with numeric values.
    code_column : str, optional
        Name of the column of the Pandas DataFrame containing the unique code of the countries in the ISO-3166-2 standard. This column is used to perform the join with the internal attribute of the countries vector dataset that contains the country code. If the code_column is None, the code is taken from the index of the DataFrame, (default is None)
    value_column : str, optional
        Name of the column of the Pandas DataFrame containing the values to be assigned to the countries using the join on the ISO-3166-2 codes (default is 'value')
    codes_selected : list of strings, optional
        List of codes of countries to display as selected (default is [])
    center : tuple of (lat,lon), optional
        Geographical coordinates of the initial center of the interactive map visualization (default is None)
    zoom : int, optional
        Initial zoom level of the interactive map (default is None)
    width : str, optional
        Width of the map widget to create (default is '99%')
    height : str, optional
        Height of the map widget to create (default is '400px')
    min_width : str, optional
        Minimum width of the layout of the map widget (default is None)
    basemap : instance of basemaps type, optional
        Basemap to use as background map (default is basemaps.OpenStreetMap.Mapnik)
    detailedcountries : bool, optional
        If True loads the more detailed version of the countries dataset (default is False()
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to country polygons and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    stroke : str, optional
        Color to use for the border of countries (default is '#232323')
    stroke_selected : str, optional
        Color to use for the border of the selected countries (default is '#00ffff')
    stroke_width: float, optional
        Width of the border of the country polygons in pixels (default is 3.0)
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    style : dict, optional
        Style to apply to the features (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6})
    hover_style : dict, optional
        Style to apply to the features when hover (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85})
        
    Returns
    -------
        a ipyleaflet.Map instance

    Example
    -------
    Creation of a map displaying a random variable on 4 european countries. The numerical values assigned to each of the countries are randomly generated using numpy.random.uniform and saved into a dictionary having the country code as the key. This dict is transformed to a Pandas DataFrame with 4 rows and having 'iso2code' and 'value' as columns. The graduated legend is build using the 'inverted' Reds Plotly colorscale (low values are dark red, intermediate values are red, high values are white)::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from ipyleaflet import basemaps
        from vois import leafletMap

        countries = ['DE', 'ES', 'FR', 'IT']

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        m = leafletMap.countriesMap(df,
                                    code_column='iso2code',
                                    height='400px',
                                    stroke_width=2.0,
                                    stroke_selected='yellow',
                                    basemap=basemaps.Stamen.Terrain,
                                    colorlist=px.colors.sequential.Reds[::-1],
                                    codes_selected=['IT'],
                                    center=[43,12], zoom=5)
        display(m)
        
    .. figure:: figures/leafletCountries.png
       :scale: 100 %
       :alt: leafletCountries example

       Example of an ipyleaflet Map displaying 4 european countries.
        
    """

    if df.shape[0] <= 0:
        minvalue = 1.0
        maxvalue = 2.0
    else:
        mean = df[value_column].mean()
        if df.shape[0] <= 1:
            minvalue = mean
            maxvalue = mean
        else:
            stddev = df[value_column].std()
            valuemin = df[value_column].min()
            valuemax = df[value_column].max()

            minvalue = mean - stdevnumber*stddev
            maxvalue = mean + stdevnumber*stddev

            if minvalue < valuemin: minvalue = valuemin
            if maxvalue > valuemax: maxvalue = valuemax

        if not minallowed_value is None:
            if minvalue < minallowed_value: minvalue = minallowed_value
        if not maxallowed_value is None:
            if maxvalue > maxallowed_value: maxvalue = maxallowed_value
        
    #print(mean,stddev, minvalue, maxvalue)

    if minvalue >= maxvalue: maxvalue = minvalue + 1
    ci = colors.colorInterpolator(colorlist,minvalue,maxvalue)

    
    # Assign colors for a feature
    def interpolate_color(feature):
        code  = feature['properties']['ISO_A2_EH']
        value = feature['properties']['value']
        if code in codes_selected:
            return { 'color': stroke_selected, 'weight': stroke_width+2, 'fillColor': ci.GetColor(value) }
        else:
            return { 'color': stroke,          'weight': stroke_width, 'fillColor': ci.GetColor(value) }

    
    # Creation of the Map
    m = Map(layout=Layout(width=width, height=height), scroll_wheel_zoom=True, basemap=basemap)
    if not min_width is None:
        m.layout.min_width = min_width
    if not center is None:
        m.center = center
    if not zoom is None:
        m.zoom = zoom

    # Add map controls
    m.add_control(FullScreenControl(position="topleft"))
    m.add_control(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))
    m.add_control(ScaleControl(position='bottomright'))

    poslabel = widgets.Label(value='')
    widget_coordinate = WidgetControl(widget=poslabel, position='topright')
    m.add_control(widget_coordinate)
    
    lat = lon = 0
    def handle_interaction(**kwargs):
        nonlocal lat,lon
        if kwargs.get('type') == 'mousemove':
            lat = kwargs.get('coordinates')[0]
            lon = kwargs.get('coordinates')[1]
            poslabel.value = '{:.{prec}f}'.format(lat, prec=4) + ' - ' + '{:.{prec}f}'.format(lon, prec=4)

    m.on_interaction(handle_interaction)

   
    # Manage click on a feature
    def click_on_a_feature(*args, **kvargs):
        event   = kvargs['event']
        feature = kvargs['feature']

        code  = feature['properties']['ISO_A2_EH']
        name  = feature['properties']['NAME']
        value = feature['properties']['value']

        val = '{:.{prec}f}'.format(value, prec=decimals)
        s = name + ': ' + val
        
        pos = [lat,lon]
        message = widgets.HTML()
        message.value = "<style> p.small {line-height: 1.2; }</style><p class=\"small\">" + s + "</p>"
        popup = Popup(location=pos,child=message, close_button=True,auto_close=True,close_on_escape_key=True)
        m.add_layer(popup)
        
        
    # Add countries (taken from the setupfolder/data )
    path = Path(geojsonUtils.__file__)
    datafolder = str(path.parent.absolute()) + '/data'

    filepath = datafolder + '/ne_110m_admin_0_countries.geojson'
    if detailedcountries:
        filepath = datafolder + '/ne_50m_admin_0_countries.geojson'
    
    geojsonstr = geojsonUtils.geojsonLoadFile(filepath)

    countries = [str(x) for x in list(df[code_column])]
    values    = list(df[value_column])
    d = dict(zip(countries,values))
    geojsonnew = geojsonUtils.geojsonJoin(geojsonstr, 'ISO_A2_EH', 'value', d, innerMode=True)
    
    data = json.loads(geojsonnew)

    geo_json = GeoJSON(data=data, style=style, hover_style=hover_style, style_callback=interpolate_color)
    geo_json.on_click(click_on_a_feature)
    
    m.add_layer(geo_json)
    return m
    

    
###########################################################################################################################################################################
# Simplified way to create a vector layer displaying a custom geojson.
# Input values to assign to features come from a Pandas Dataframe df containing a column with unique code and a column with values
# Returns a Map instance
###########################################################################################################################################################################
def geojsonMap(df,                          # Pandas dataframe containing 'value' and 'label' columns
               geojson_path,                # Path of the geojson containing the geographic features
               geojson_attribute,           # Name of the attribute of the geojson containing the unique code
               code_column=None,            # Name of the column containing the code of the features (None = the feature code is the index of the dataframe)
               value_column='value',        # Name of the column containing the value
               codes_selected=[],           # codes of the features selected
               center=None,                 # [lat,lon] to center the map
               zoom=None,                   # initial zoom level for the map
               width ='99%',                # width of the map
               height='400px',              # height of the map
               min_width=None,              # min_width of the map
               basemap=basemaps.OpenStreetMap.Mapnik, # Basemap to use
               colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
               stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
               stroke='#232323',            # stroke color for polygons border
               stroke_selected='#00ffff',   # stroke color for border of selected polygons
               stroke_width=3.0,            # border width for polygons
               decimals=2,                  # Number of decimals for the legend number display
               minallowed_value=None,       # Minimum value allowed
               maxallowed_value=None,       # Maximum value allowed
               style      ={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6},    # Style to apply to the features
               hover_style={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85}):  # Style to apply to the features when hover
    """
    Creation of an interactive map to display a custom geojson dataset. An input Pandas DataFrame df is used to join a column of numeric values to the geojson features, using the <geojson_attribute> as the internal key attribute. Once the values are assigned to the features, a graduated legend is calculated based on mean and standard deviation of the assigned values. A input list of colors is used to represent the featuress given their assigned value.

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame to use for assigning values to features. It has to contain at least a column with numeric values.
    geojson_path : str
        Path of the geojson file to load that contains the geographic features in geojson format
    geojson_attribute : str
        Name of the attribute of the geojson dataset that contains the unique codes of the features. This attribute will be use as internal key in the join operation with the df Pandas DataFrame
    code_column : str, optional
        Name of the column of the df Pandas DataFrame containing the unique code of the features. This column is used to perform the join with the internal attribute of the geojson vector dataset that contains the unique code. If the code_column is None, the code is taken from the index of the DataFrame, (default is None)
    value_column : str, optional
        Name of the column of the Pandas DataFrame containing the values to be assigned to the features using the join on geojson unique codes (default is 'value')
    codes_selected : list of strings, optional
        List of codes of features to display as selected (default is [])
    center : tuple of (lat,lon), optional
        Geographical coordinates of the initial center of the interactive map visualization (default is None)
    zoom : int, optional
        Initial zoom level of the interactive map (default is None)
    width : str, optional
        Width of the map widget to create (default is '99%')
    height : str, optional
        Height of the map widget to create (default is '400px')
    min_width : str, optional
        Minimum width of the layout of the map widget (default is None)
    basemap : basemap instance, optional
        Basemap to use as background in the map visualization (default is basemaps.OpenStreetMap.Mapnik). See `Documentation of ipyleaflet <https://ipyleaflet.readthedocs.io/en/latest/map_and_basemaps/basemaps.html>`_ for details
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to features and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    stroke : str, optional
        Color to use for the border of polygons (default is '#232323')
    stroke_selected : str, optional
        Color to use for the border of the selected polygons (default is '#00ffff')
    stroke_width: float, optional
        Width of the border of the polygons in pixels (default is 3.0)
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    style : dict, optional
        Style to apply to the features (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6})
    hover_style : dict, optional
        Style to apply to the features when hover (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85})
        
    Returns
    -------
        a ipyleaflet.Map instance

    Example
    -------
    Creation of a map displaying a custom geojson. The numerical values assigned to each of the countries are randomly generated using numpy.random.uniform and saved into a dictionary having the country code as the key. This dict is transformed to a Pandas DataFrame with 4 rows and having 'iso2code' and 'value' as columns. The graduated legend is build using the 'inverted' Viridis Plotly colorscale::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from vois import leafletMap

        countries = ['DE', 'ES', 'FR', 'IT']

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        m = leafletMap.geojsonMap(df,
                                  './data/ne_50m_admin_0_countries.geojson',
                                  'ISO_A2_EH',   # Internal attribute used as key
                                  code_column='iso2code',
                                  height='400px',
                                  stroke_width=1.5,
                                  stroke_selected='yellow',
                                  colorlist=px.colors.sequential.Viridis[::-1],
                                  codes_selected=['IT'],
                                  center=[43,12], zoom=5)
        display(m)

    .. figure:: figures/leafletMap.png
       :scale: 100 %
       :alt: leafletMap example

       Example of an ipyleaflet Map displaying 4 european countries from a custom geojson file.
        
    """

    if df.shape[0] <= 0:
        minvalue = 1.0
        maxvalue = 2.0
    else:
        mean = df[value_column].mean()
        if df.shape[0] <= 1:
            minvalue = mean
            maxvalue = mean
        else:
            stddev = df[value_column].std()
            valuemin = df[value_column].min()
            valuemax = df[value_column].max()

            minvalue = mean - stdevnumber*stddev
            maxvalue = mean + stdevnumber*stddev

            if minvalue < valuemin: minvalue = valuemin
            if maxvalue > valuemax: maxvalue = valuemax

        if not minallowed_value is None:
            if minvalue < minallowed_value: minvalue = minallowed_value
        if not maxallowed_value is None:
            if maxvalue > maxallowed_value: maxvalue = maxallowed_value
        
    #print(mean,stddev, minvalue, maxvalue)

    if minvalue >= maxvalue: maxvalue = minvalue + 1
    ci = colors.colorInterpolator(colorlist,minvalue,maxvalue)

    
    # Assign colors for a feature
    def interpolate_color(feature):
        code  = feature['properties'][geojson_attribute]
        value = feature['properties']['value']
        if code in codes_selected:
            return { 'color': stroke_selected, 'weight': stroke_width+2, 'fillColor': ci.GetColor(value) }
        else:
            return { 'color': stroke,          'weight': stroke_width, 'fillColor': ci.GetColor(value) }

    
    # Creation of the Map
    m = Map(layout=Layout(width=width, height=height), scroll_wheel_zoom=True, basemap=basemap)
    if not min_width is None:
        m.layout.min_width = min_width
    if not center is None:
        m.center = center
    if not zoom is None:
        m.zoom = zoom

    # Add map controls
    m.add_control(FullScreenControl(position="topleft"))
    m.add_control(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))
    m.add_control(ScaleControl(position='bottomright'))

    poslabel = widgets.HTML(value='')
    widget_coordinate = WidgetControl(widget=poslabel, position='topright')
    m.add_control(widget_coordinate)
    
    lat = lon = 0
    def handle_interaction(**kwargs):
        nonlocal lat,lon
        if kwargs.get('type') == 'mousemove':
            lat = kwargs.get('coordinates')[0]
            lon = kwargs.get('coordinates')[1]
            poslabel.value = '{:.{prec}f}'.format(lat, prec=4) + ' - ' + '{:.{prec}f}'.format(lon, prec=4)

    m.on_interaction(handle_interaction)

   
    # Manage click on a feature
    def click_on_a_feature(*args, **kvargs):
        event   = kvargs['event']
        feature = kvargs['feature']

        code  = feature['properties'][geojson_attribute]
        value = feature['properties']['value']

        val = '{:.{prec}f}'.format(value, prec=decimals)
        s = code + ': ' + val
        
        pos = [lat,lon]
        message = widgets.HTML()
        message.value = "<style> p.small {line-height: 1.2; }</style><p class=\"small\">" + s + "</p>"
        popup = Popup(location=pos,child=message, close_button=True,auto_close=True,close_on_escape_key=True)
        m.add_layer(popup)
        
        
    # Add layer
    geojsonstr = geojsonUtils.geojsonLoadFile(geojson_path)

    countries = [str(x) for x in list(df[code_column])]
    values    = list(df[value_column])
    d = dict(zip(countries,values))
    geojsonnew = geojsonUtils.geojsonJoin(geojsonstr, geojson_attribute, 'value', d, innerMode=True)
    
    data = json.loads(geojsonnew)

    geo_json = GeoJSON(data=data, style=style, hover_style=hover_style, style_callback=interpolate_color)
    geo_json.on_click(click_on_a_feature)
    
    m.add_layer(geo_json)
    return m


###########################################################################################################################################################################
# Simplified way to create a vector layer displaying a custom geojson with a categorical map on an attribute of the geojson
# Returns a Map instance
###########################################################################################################################################################################
def geojsonCategoricalMap(geojson_path,                # Path of the geojson containing the geographic features
                          geojson_attribute,           # Name of the attribute of the geojson containing the attribute to use for assigning the colors
                          center=None,                 # [lat,lon] to center the map
                          zoom=None,                   # initial zoom level for the map
                          width ='99%',                # width of the map
                          height='400px',              # height of the map
                          min_width=None,              # min_width of the map
                          basemap=basemaps.OpenStreetMap.Mapnik, # Basemap to use
                          colormap={},                 # dictionary containing geojson_attribute values as keys and colors as values
                          stroke='#232323',            # stroke color for polygons border
                          stroke_width=3.0,            # border width for polygons
                          fill='#aaaaaa',              # default fill color for polygons
                          style      ={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6},    # Style to apply to the features
                          hover_style={'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85}):  # Style to apply to the features when hover
    """
    Creation of an interactive map to display a custom geojson dataset where colors are assigned to feature based on the values of an internal attribute of the input geojson file. The colormap parameter is a dictionary with keys corresponding to all the unique values of the internal attribute, which are mapped to the colors to use for representing each class.

    Parameters
    ----------
    geojson_path : str
        Path of the geojson file to load that contains the geographic features in geojson format
    geojson_attribute : str
        Name of the attribute of the geojson dataset that contains the thematisatio attribute of the features. This attribute will be used to retrieve the colors to assign to the features using the colormap parameter
    center : tuple of (lat,lon), optional
        Geographical coordinates of the initial center of the interactive map visualization (default is None)
    zoom : int, optional
        Initial zoom level of the interactive map (default is None)
    width : str, optional
        Width of the map widget to create (default is '99%')
    height : str, optional
        Height of the map widget to create (default is '400px')
    min_width : str, optional
        Minimum width of the layout of the map widget (default is None)
    basemap : basemap instance, optional
        Basemap to use as background in the map visualization (default is basemaps.OpenStreetMap.Mapnik). See `Documentation of ipyleaflet <https://ipyleaflet.readthedocs.io/en/latest/map_and_basemaps/basemaps.html>`_ for details
    colormap : dictionary containing geojson_attribute values as keys and colors as values
        Colors to assign to each distinct value of the geojson_attribute
    stroke : str, optional
        Color to use for the border of polygons (default is '#232323')
    stroke_width: float, optional
        Width of the border of the polygons in pixels (default is 3.0)
    fill : str, optional
        Default fill color to use for the polygons (default is '#aaaaaa')
    style : dict, optional
        Style to apply to the features (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.6})
    hover_style : dict, optional
        Style to apply to the features when hover (default is {'opacity': 1, 'dashArray': '0', 'fillOpacity': 0.85})
        
    Returns
    -------
        a ipyleaflet.Map instance

    Example
    -------
    Creation of a map displaying a custom geojson with data on landuse. The colors are assigned to the polygons based on the values of the 'fclass' attribute of the input geojson file. The colormap parameter is a dictionary with keys corresponding to all the unique landuse classes, which are mapped to the colors of a Plotly discrete color scale (see `Color Sequences in Plotly Express <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_)::
        
        import plotly.express as px
        from IPython.display import display
        from ipywidgets import widgets, Layout
        from vois import leafletMap, svgUtils, geojsonUtils

        # Load landuse example and get unique landuse classes
        filepath = './data/landuse.geojson'
        geojson = geojsonUtils.geojsonLoadFile(filepath)
        landuses = sorted(list(set(geojsonUtils.geojsonAll(geojson,'fclass'))))

        # Create a colormap (dictionary that maps landuses to colors)
        colors   = px.colors.qualitative.Dark24
        colormap = dict(zip(landuses, colors))

        m = leafletMap.geojsonCategoricalMap(filepath,
                                             'fclass',
                                             stroke_width=1.0,
                                             stroke='black', 
                                             colormap=colormap,
                                             width='79%',
                                             height='700px',
                                             center=[51.005,13.6],
                                             zoom=12,
                                             basemap=basemaps.CartoDB.Positron,
                                             style={'opacity': 1, 'dashArray': '0', 'fillOpacity': 1})
        
        outlegend = widgets.Output(layout=Layout(width='230px',height='680px'))
        with outlegend:
            display(HTML(svgUtils.categoriesLegend("Landuse legend",
                                                   landuses,
                                                   colorlist=colors[:len(landuses)])))
        widgets.HBox([m,outlegend])
        
    .. figure:: figures/leafletMapCat.png
       :scale: 100 %
       :alt: leafletMap example

       Example of an ipyleaflet Map displaying 4 european countries from a custom geojson file.
        
    """

    # Assign colors for a feature
    def get_color(feature):
        code  = feature['properties'][geojson_attribute]
        if code in colormap:
            return { 'color': stroke, 'weight': stroke_width, 'fillColor': colormap[code] }
        else:
            return { 'color': stroke, 'weight': stroke_width, 'fillColor': fill }
    
    # Creation of the Map
    m = Map(layout=Layout(width=width, height=height), scroll_wheel_zoom=True, basemap=basemap)
    if not min_width is None:
        m.layout.min_width = min_width
    if not center is None:
        m.center = center
    if not zoom is None:
        m.zoom = zoom

    # Add map controls
    m.add_control(FullScreenControl(position="topleft"))
    m.add_control(SearchControl(position="topleft",url='https://nominatim.openstreetmap.org/search?format=json&q={s}',zoom=12))
    m.add_control(ScaleControl(position='bottomright'))

    poslabel = widgets.HTML(value='')
    widget_coordinate = WidgetControl(widget=poslabel, position='topright')
    m.add_control(widget_coordinate)
    
    lat = lon = 0
    def handle_interaction(**kwargs):
        nonlocal lat,lon
        if kwargs.get('type') == 'mousemove':
            lat = kwargs.get('coordinates')[0]
            lon = kwargs.get('coordinates')[1]
            poslabel.value = '{:.{prec}f}'.format(lat, prec=4) + ' - ' + '{:.{prec}f}'.format(lon, prec=4)

    m.on_interaction(handle_interaction)

   
    # Manage click on a feature
    def click_on_a_feature(*args, **kvargs):
        event   = kvargs['event']
        feature = kvargs['feature']

        code  = feature['properties'][geojson_attribute]
        
        pos = [lat,lon]
        message = widgets.HTML()
        message.value = "<style> p.small {line-height: 1.2; }</style><p class=\"small\">" + code + "</p>"
        popup = Popup(location=pos,child=message, close_button=True,auto_close=True,close_on_escape_key=True)
        m.add_layer(popup)
        
        
    # Add layer
    geojsonstr = geojsonUtils.geojsonLoadFile(geojson_path)
    data = json.loads(geojsonstr)

    geo_json = GeoJSON(data=data, style=style, hover_style=hover_style, style_callback=get_color)
    geo_json.on_click(click_on_a_feature)
    
    m.add_layer(geo_json)
    return m
