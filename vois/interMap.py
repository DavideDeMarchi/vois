"""Utility functions for the creation of interactive maps using BDAP interactive library."""
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
import math

from ipywidgets import widgets, Layout
from ipyleaflet import SearchControl, WidgetControl, LegendControl, ScaleControl, FullScreenControl

try:
    from jeodpp import inter, imap
except:
    pass


try:
    from . import colors
    from . import geojsonUtils
except:
    import colors
    import geojsonUtils


# Custom identify
def CustomIdentifyPopup(map,p):
    from ipywidgets import widgets, HTML, CallbackDispatcher
    from ipyleaflet import Popup
    from IPython.display import display

    def handle_interaction_popup(**kwargs):
        if kwargs.get('type') == 'click':

            pos = [kwargs.get('coordinates')[0],kwargs.get('coordinates')[1]]
            message = widgets.HTML()

            sid = inter.identifyPointEx(p,pos[1],pos[0],4326,int(map.zoom))
            values = sid.split(': ')
            if len(values) == 2:
                values[1] = str(int(float(values[1])*100) / 100.0)
                sid = values[0] + ': ' + values[1]

            if len(sid) > 0:
                message.value = "<style> p.small {line-height: 1.2; }</style><p class=\"small\">" + sid.replace(",","<br />") + "</p>"
                popup = Popup(location=pos,child=message, close_button=True,auto_close=True,close_on_escape_key=True)
                map.add_layer(popup)

    map._interaction_callbacks = CallbackDispatcher()
    map.on_interaction(handle_interaction_popup)


###########################################################################################################################################################################
# Simplified way to create a vector layer displaying the countries of the world.
# Vector data is taken from inter.collections.BaseData.AdministrativeUnits.Global.VirtualEarth.Countries
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
                 basemap=1,                   # Basemap to use
                 colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
                 stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                 stroke='#232323',            # stroke color for countries border
                 stroke_selected='#00ffff',   # stroke color for border of selected country
                 stroke_width=1.0,            # border width for countries polygons
                 decimals=2,                  # Number of decimals for the legend number display
                 minallowed_value=None,       # Minimum value allowed
                 maxallowed_value=None):      # Maximum value allowed
    """
    Creation of an interactive map to display the countries of the world. An input Pandas DataFrame df is used to join a column of numeric values to the countries, using the iso2code (ISO 3166-2) as internal key attribute. Once the values are assigned to the countries, a graduated legend is calculated based on mean and standard deviation of the assigned values. A input list of colors is used to represent the countries given their assigned value.

    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it is not portable in other environments! Please refer to the module :py:mod:`leafletMap` for geospatial function not related to BDAP.

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
    basemap : int, optional
        Basemap to use as background in the map visualization (default is 1). Valid values are in [1,39], see https://jeodpp.jrc.ec.europa.eu/services/processing/interhelp/3.2_map.html?highlight=basemap#inter.Map.printAvailableBasemaps for details
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to country polygons and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    stroke : str, optional
        Color to use for the border of countries (default is '#232323')
    stroke_selected : str, optional
        Color to use for the border of the selected countries (default is '#00ffff')
    stroke_width: float, optional
        Width of the border of the country polygons in pixels (default is 1.0)
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
        
    Returns
    -------
        a jeodpp.imap instance (a Map object derived from the ipyleaflet Map)

    Example
    -------
    Creation of a map displaying a random variable on 4 european countries. The numerical values assigned to each of the countries are randomly generated using numpy.random.uniform and saved into a dictionary having the country code as the key. This dict is transformed to a Pandas DataFrame with 4 rows and having 'iso2code' and 'value' as columns. The graduated legend is build using the 'inverted' Reds Plotly colorscale (low values are dark red, intermediate values are red, high values are white)::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from vois import interMap

        countries = ['DE', 'ES', 'FR', 'IT']

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        m = interMap.countriesMap(df,
                                  code_column='iso2code',
                                  height='400px',
                                  stroke_width=1.5,
                                  stroke_selected='yellow',
                                  colorlist=px.colors.sequential.Reds[::-1],
                                  codes_selected=['IT'])
        display(m)
        
    .. figure:: figures/countriesMap.png
       :scale: 100 %
       :alt: countriesMap example

       Example of an interactive map displaying 4 european countries.
            
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
    
    
    # Creation of the Map
    m = imap.Map(layout=Layout(width=width, height=height), basemap=basemap)
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
    
    # Seems not to work: to check!
    coordlabel = widgets.HTML(value='')
    widget_coordinate = WidgetControl(widget=coordlabel, position='bottomleft')
    m.add_control(widget_coordinate)
    inter.mapInteractGeneric(m, labelCoordinates=coordlabel)
    
    # Layer Countries
    v = inter.Collection(inter.collections.BaseData.AdministrativeUnits.Global.VirtualEarth.Countries)
    
    
    # Join
    countries = [str(x) for x in list(df[code_column])]
    values    = list(df[value_column])
    value_ranges = np.linspace(minvalue, maxvalue, 100)
    breaks       = list(value_ranges) # [1:]
    breaks.append(9999999999999)
    v.joinAdd('iso_a2', 'value', countries, values)   # Doesn't work in Voila!!!
    
    # Define legend
    extendedcolors = [ci.GetColor(i) for i in breaks]
    v.colorCustom(extendedcolors)
    
    v.legendSet('line', 'stroke-width', str(stroke_width))
    v.legendSet('line', 'stroke',       str(stroke))
    
    v.legendGraduated('value', 'custom', len(breaks), 2, minvalue, maxvalue, breaks)
    v.opacity(255)
    
    # Define the identify
    v.parameter('identifyField','admin value')
    v.parameter('identifyseparator', ': ')
    CustomIdentifyPopup(m, v)
    
    # Add layer to the map
    layer = m.addLayer(v.toLayer())
    
    
    # Add selected countries to the map
    if len(codes_selected) > 0:
        geoms = v.all('GEOMETRY')
        codes = v.all('iso_a2')
        for c in codes_selected:
            if c in codes:
                index = codes.index(c)
                geom = geoms[index]
                if not geom is None:
                    s = inter.VectorLayer("wkt")
                    s.geomAdd(geom)
                    s.remove('default','all')
                    s.set('line','stroke', str(stroke_selected))
                    s.set('line','stroke-width','3')
                    layersel = m.addLayer(s.toLayer(), name=c)
    
    return m
    

    
###########################################################################################################################################################################
# Load a geojson string and returns a inter.VectorLayer object
###########################################################################################################################################################################
def interGeojsonToVector(geojson):
    """
    Load a geojson string and returns a inter.VectorLayer object (see https://jeodpp.jrc.ec.europa.eu/services/processing/interhelp/3.5_vectorlayer.html)

    Parameters
    ----------
        geojson : str
            String containing data in geojson format
                
    Returns
    -------
        An instance of the inter.Vector class of the interapro library
            
    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it in not portable in other environments!
    
    """
    vector = inter.Collection(inter.collections.Vector)
    vector.fileAdd(geojson)
    return vector
    
    
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
               basemap=1,                   # Basemap to use
               colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
               stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
               stroke='#232323',            # stroke color for polygons border
               stroke_selected='#00ffff',   # stroke color for border of selected polygons
               stroke_width=1.0,            # border width for polygons
               decimals=2,                  # Number of decimals for the legend number display
               minallowed_value=None,       # Minimum value allowed
               maxallowed_value=None):      # Maximum value allowed
    """
    Creation of an interactive map to display a custom geojson dataset. An input Pandas DataFrame df is used to join a column of numeric values to the geojson features, using the <geojson_attribute> as the internal key attribute. Once the values are assigned to the features, a graduated legend is calculated based on mean and standard deviation of the assigned values. A input list of colors is used to represent the featuress given their assigned value.

    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it is not portable in other environments! Please refer to the module :py:mod:`lefletMap` for geospatial function not related to BDAP.
    
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
    basemap : int, optional
        Basemap to use as background in the map visualization (default is 1). Valid values are in [1,39], see https://jeodpp.jrc.ec.europa.eu/services/processing/interhelp/3.2_map.html?highlight=basemap#inter.Map.printAvailableBasemaps for details
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to features and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    stroke : str, optional
        Color to use for the border of countries (default is '#232323')
    stroke_selected : str, optional
        Color to use for the border of the selected countries (default is '#00ffff')
    stroke_width: float, optional
        Width of the border of the country polygons in pixels (default is 1.0)
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
        
    Returns
    -------
        a jeodpp.imap instance (a Map object derived from the ipyleaflet Map)

    Example
    -------
    Creation of a map displaying a custom geojson. The numerical values assigned to each of the countries are randomly generated using numpy.random.uniform and saved into a dictionary having the country code as the key. This dict is transformed to a Pandas DataFrame with 4 rows and having 'iso2code' and 'value' as columns. The graduated legend is build using the 'inverted' Reds Plotly colorscale (low values are dark red, intermediate values are red, high values are white)::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from vois import interMap

        countries = ['DE', 'ES', 'FR', 'IT']

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        m = interMap.geojsonMap(df,
                                './data/ne_50m_admin_0_countries.geojson',
                                'ISO_A2_EH',   # Internal attribute used as key
                                code_column='iso2code',
                                height='400px',
                                stroke_width=1.5,
                                stroke_selected='yellow',
                                colorlist=px.colors.sequential.Reds[::-1],
                                codes_selected=['IT'])
        display(m)

    .. figure:: figures/geojsonMap.png
       :scale: 100 %
       :alt: geojsonMap example

       Example of an interactive map displaying 4 european countries from a custom geojson file.

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
    
    
    # Creation of the Map
    m = imap.Map(layout=Layout(width=width, height=height), basemap=basemap)
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
    
    # Seems not to work: to check!
    coordlabel = widgets.HTML(value='')
    widget_coordinate = WidgetControl(widget=coordlabel, position='bottomleft')
    m.add_control(widget_coordinate)
    inter.mapInteractGeneric(m, labelCoordinates=coordlabel)
    
    # Layer
    geojson = geojsonUtils.geojsonLoadFile(geojson_path)
    
    
    # Join
    countries = [str(x) for x in list(df[code_column])]
    values    = list(df[value_column])
    value_ranges = np.linspace(minvalue, maxvalue, 100)
    breaks       = list(value_ranges) # [1:]
    breaks.append(9999999999999)
    
    d = dict(zip(countries,values))
    geojsonnew = geojsonUtils.geojsonJoin(geojson,geojson_attribute, 'value', d, innerMode=True)
    v = interGeojsonToVector(geojsonnew)
    
    # Define legend
    extendedcolors = [ci.GetColor(i) for i in breaks]
    v.colorCustom(extendedcolors)
    
    v.legendSet('line', 'stroke-width', str(stroke_width))
    v.legendSet('line', 'stroke',       str(stroke))
    
    v.legendGraduated('value', 'custom', len(breaks), 2, minvalue, maxvalue, breaks)
    v.opacity(255)
    
    # Define the identify
    v.parameter('identifyField',geojson_attribute + ' value')
    v.parameter('identifyseparator', ': ')
    CustomIdentifyPopup(m, v)   
    
    # Add layer to the map
    p = v.process()
    layer = m.addLayer(v.toLayer())
    
    # Add selected countries to the map
    if len(codes_selected) > 0:
        filtered = geojsonUtils.geojsonFilter(geojsonnew, geojson_attribute, codes_selected)
        if geojsonUtils.geojsonCount(filtered) > 0:
            s = inter.Collection(inter.collections.Vector)
            s.fileAdd(filtered)
            s.remove('default','all')
            s.set('line','stroke', str(stroke_selected))
            s.set('line','stroke-width','3')
            layersel = m.addLayer(s.toLayer(), name='selected')

    return m


###########################################################################################################################################################################
# Sets a bivariate legend for vector layer v
# Returns a legend in SVG string format
###########################################################################################################################################################################
def bivariateLegend(v,
                    filters1,
                    filters2,
                    colorlist1,
                    colorlist2,
                    title='',
                    title1='',
                    title2='',
                    names1=[],
                    names2=[],
                    fontsize=14,
                    fontweight=400,
                    stroke='#000000',
                    stroke_width=0.25,
                    side=100,
                    resizewidth='',
                    resizeheight=''):
    """
    Creation of a bivariate choropleth legend for a polygon vector layer. See `Bivariate Choropleth Maps: A How-to Guide <https://www.joshuastevens.net/cartography/make-a-bivariate-choropleth-map/>`_ for the idea. The function creates a legend for vector layer v based on two attributes of the layer and returns a string containing the SVG representation of the legend (that can be displayed using display(HTML(svgstring) call)

    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it is not portable in other environments! Please refer to the module :py:mod:`lefletMap` for geospatial function not related to BDAP.
    
    Parameters
    ----------
    v : instance of inter.VectorLayer class
        Vector layer instance for which the bivariate legend has to be built
    filters1 : list of strings
        List of strings defining the conditions for the classes based on the first attribute
    filters2 : list of strings
        List of strings defining the conditions for the classes based on the second attribute
    colorlist1 : list of colors
        List of colors to use for the legend on the first attribute (see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    colorlist2 : list of colors
        List of colors to use for the legend on the second attribute (see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    title : str, optional
        Main title of the legend chart (default is '')
    title1 : str, optional
        Title for the legend on the first attribute. It will be displayed vertically in the Y axis of the SVG. Default is ''.
    title2 : str, optional
        Title for the legend on the second attribute. It will be displayed horizontally in the X axis of the SVG. Default is ''.
    names1 : list of strings, optional
        List containing one string for each of the classes of the legend on the first attribute (default is [])
    names2 : list of strings, optional
        List containing one string for each of the classes of the legend on the second attribute (default is [])
    fontsize : int, optional
        Size in pixels of the font used for texts (default is 14)
    fontweight : int, optional
        Weight of the font used for title texts (default is 400)
    stroke : str, optional
        Color to use for the border of the polygons (default is '#000000')
    stroke_width : float, optional
        Width in pixels of the stroke to use for the border of the polygons (default is 0.25)
    side : int, optional
        Side in pixels of the squares displayed in the SVG legend (default is 100)
    resizewidth : str, optional
        Width of the resizing container (default is '')
    resizeheight : str, optional
        height of the resizing container (default is '')

    Returns
    -------
        a string containing SVG text to display the bivariate legend using a call to display(HTML(...))

    Example
    -------
    Creation of a bivariate choropleth legend for the polygons of the Italian provinces. The first attribute is the short name of the province (attribute 'SIGLA'), and the second attribute is the SHAPE_AREA attribute which contains the dimension in squared meters::
    
        from ipywidgets import widgets, Layout, HTML
        from IPython.display import display
        
        from jeodpp import inter, imap
        from vois import interMap, geojsonUtils
        
        # Load data on italian provinces
        geojson = geojsonUtils.geojsonLoadFile('./data/ItalyProvinces.geojson')
        vector = interMap.interGeojsonToVector(geojson)
        vector = vector.parameter("identifyfield", "SIGLA DEN_PROV SHAPE_AREA")
        vector = vector.parameter("identifyseparator", "<br>")
        
        # Create and display a Map instance
        m = imap.Map(basemap=1, layout=Layout(height='600px'))
        display(m)
        
        # Creation of the bivariate legend
        colorlist1 = ['#f3f3f3', '#eac5dd', '#e6a3d0']
        colorlist2 = ['#f3f3f3', '#c2f1d5', '#8be2ae']

        svg = interMap.bivariateLegend(vector,
                                       ["[SIGLA] < 'FE'", "[SIGLA] >= 'FE' and [SIGLA] <= 'PU'", "[SIGLA] > 'PU'"],
                                       ["[SHAPE_AREA] < 2500000000", "[SHAPE_AREA] >= 2500000000 and [SHAPE_AREA] <= 4500000000", "[SHAPE_AREA] > 4500000000 and [SHAPE_AREA] <= 7500000000", '[SHAPE_AREA] > 7500000000'],
                                       colorlist1,
                                       colorlist2,
                                       title='Example of Bivariate Choropleth',
                                       title1="Province initials",
                                       names1=['< FE', 'in [FE,PU]', '> PU'],
                                       title2="Province area",
                                       names2=['Small', 'Medium', 'Large', 'XLarge'],
                                       fontsize=24,
                                       fontweight=500)
        
        # Display of the vector layer on the map
        p = vector.process()
        m.clear()
        m.addLayer(p.toLayer())
        m.zoomToImageExtent(p)

        inter.identifyPopup(m,p)

        # Display the bivariate choropleth legend
        display(HTML(svg))
        
    .. figure:: figures/bivariate.png
       :scale: 100 %
       :alt: Example of bivariate choropleth legend

       Example of an interactive map showing polygons colored with a bivariate choropleth legend.
        
    """
    
    n1 = len(filters1)
    n2 = len(filters2)
    v.reset()
    
    width = str(stroke_width)
    
    if n1 > 1 and n2 > 1:
        ci1 = colors.colorInterpolator(colorlist1, 0.0, n1-1)
        ci2 = colors.colorInterpolator(colorlist2, 0.0, n2-1)

        displ = 2*fontsize
        h = displ + side * n1
        w = displ + side * n2
        
        ydispl = 0
        if len(title) > 0:
            ydispl = 0.8*displ
            h += displ
            
        if len(resizewidth)  <= 0: resizewidth  = '%fpx' % w
        if len(resizeheight) <= 0: resizeheight = '%fpx' % h
            
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" width="%s" height="calc(%s + 20px)" version="1.1">\n' % (w,h, resizewidth,resizeheight)
        
        if len(title) > 0:
            svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (displ+0.5*n2*side, 1.1*fontsize, 1.05*fontsize, fontweight, title)
            
        svg += '<text x="0" y="0" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" transform="translate(%f,%f) rotate(-90)">%s</text>' % (fontsize, fontweight, 0.8*fontsize, ydispl+0.5*n1*side, title1)
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (displ+0.5*n2*side, ydispl+2.1*fontsize+n1*side, fontsize, fontweight, title2)

        for f1 in filters1:
            row = filters1.index(f1)
            c1 = ci1.GetColor(row)
            
            if row < len(names1):
                svg += '<text x="0" y="0" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" transform="translate(%f,%f) rotate(-90)">%s</text>' % (0.7*fontsize, 400, 1.8*fontsize, ydispl+(n1-row-0.5)*side, names1[row])
                
            for f2 in filters2:
                col = filters2.index(f2)
                c2 = ci2.GetColor(col)
                cm = colors.darken(c1,c2)
                f = '(' + f1 + ') and ' + '(' + f2 + ')'
                #print(f, colors.string2rgb(c1), colors.string2rgb(c2), cm)
                v.set(f,'poly','fill',cm)
                v.set(f,'line','stroke',stroke)
                v.set(f,'line','stroke-width',width)
                
                svg += '<rect style="fill:%s;" x="%d" y="%d" width="%d" height="%d" stroke-width="0"><title>%s</title></rect>\n' % (cm, displ+col*side, ydispl+(n1-row-1)*side, side, side, f)

        for f2 in filters2:
            col = filters2.index(f2)
            if col < len(names2):
                svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (displ+(col+0.5)*side, ydispl+0.75*fontsize+n1*side, 0.7*fontsize, 400, names2[col])
                
        svg += '</svg>'
        return svg

    
###########################################################################################################################################################################
# Sets a simple trivariate legend (defined by 7 colors) using 3 attributes of a vector layer v
# Returns a legend in SVG string format
###########################################################################################################################################################################
def trivariateLegend(v,
                     filter1,
                     filter2,
                     filter3,
                     color1='#ff60ff',
                     color2='#ffff60',
                     color3='#60ffff',
                     color4='#ffffff',
                     title='',
                     title1='',
                     title2='',
                     title3='',
                     fontsize=14,
                     fontweight=300,
                     stroke='#000000',
                     stroke_width=0.25,
                     radius=100):
    """
    Creation of a trivariate choropleth legend for a polygon vector layer. See `Some Thoughts on Multivariate Maps <stamen.com/some-thoughts-on-multivariate-maps-ffe364342415/>`_ for the idea. The function creates a legend for vector layer v based on three attributes of the layer and returns a string containing the SVG representation of the legend (that can be displayed using display(HTML(svgstring) call).

    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it is not portable in other environments! Please refer to the module :py:mod:`lefletMap` for geospatial function not related to BDAP.
    
    Parameters
    ----------
    v : instance of inter.VectorLayer class
        Vector layer instance for which the trivariate legend has to be built
    filter1 : str
        Condition to filter the polygons on the first attribute
    filter2 : str
        Condition to filter the polygons on the second attribute
    filter3 : str
        Condition to filter the polygons on the third attribute
    color1 : str, optional
        Color to assign to polygons that satisfy the condition on the first attribute (default is '#ff80ff')
    color2 : str, optional
        Color to assign to polygons that satisfy the condition on the second attribute (default is '#ffff80')
    color3 : str, optional
        Color to assign to polygons that satisfy the condition on the third attribute (default is '#ff80ff')
    color4 : str, optional
        Color to assign to polygons that do not satisfy any of the three conditions (default is '#ffffff')
    title : str, optional
        Main title of the legend chart (default is '')
    title1 : str, optional
        Title for the legend on the first attribute (default is '')
    title2 : str, optional
        Title for the legend on the second attribute (default is '')
    title3 : str, optional
        Title for the legend on the third attribute (default is '')
    fontsize : int, optional
        Size in pixels of the font used for texts (default is 14)
    fontweight : int, optional
        Weight of the font used for title texts (default is 400)
    stroke : str, optional
        Color to use for the border of the polygons (default is '#000000')
    stroke_width : float, optional
        Width in pixels of the stroke to use for the border of the polygons (default is 0.25)
    radius : int, optional
        Radius in pixels of the circles displayed in the SVG legend (default is 100)

    Returns
    -------
        a string containing SVG text to display the trivariate legend using a call to display(HTML(...))

    Example
    -------
    Creation of a simple trivariate choropleth legend (with 7 colors) for a polygons layer containing crop data. The three attributes AL_PERC, PC_PERC and PG_PERC contain the percentage presence of the three specific crops inside the polygon::
    
        from ipywidgets import widgets, Layout, HTML
        from IPython.display import display
        
        from jeodpp import inter, imap
        from vois import interMap
        
        # Load data
        vector = inter.loadLocalVector("DEBY_2019_LandCover.shp")
        vector = vector.parameter("identifyfield", "LAU_NAME YEAR AL_PERC PC_PERC PG_PERC")
        vector = vector.parameter("identifyseparator", "<br>")
        
        # Create and display a Map instance
        m = imap.Map(basemap=60, layout=Layout(height='600px'))
        display(m)
        
        # Creation of the bivariate legend
        svg = interMap.trivariateLegend(vector,
                                        "[AL_PERC] > 60",
                                        "[PC_PERC] > 10",
                                        "[PG_PERC] > 20",
                                        '#ff60ff',
                                        '#ffff60',
                                        '#60ffff',
                                        '#ffffff55',
                                        title='Example of Trivariate Choropleth',
                                        title1="Arable Land",
                                        title2="Perm. Crop",
                                        title3="Permanent Grassland",
                                        fontsize=12,
                                        fontweight=500,
                                        radius=70)
        
        # Display of the vector layer on the map
        p = vector.process()
        m.clear()
        m.addLayer(p.toLayer())
        m.zoomToImageExtent(p)

        inter.identifyPopup(m,p)

        # Display the trivariate choropleth legend
        display(HTML(svg))
        
    .. figure:: figures/trivariate.png
       :scale: 100 %
       :alt: Example of trivariate choropleth legend

       Example of an interactive map showing polygons colored with a trivariate choropleth legend.
        
    """
    
    width = str(stroke_width)

    # Set the legend
    v.reset()
    v.set('all','poly','fill',color4)
    
    v.set(filter2,'poly','fill',color3)
    v.set(filter2,'line','stroke',stroke)
    v.set(filter2,'line','stroke-width',width)

    v.set(filter2,'poly','fill',color2)
    v.set(filter2,'line','stroke',stroke)
    v.set(filter2,'line','stroke-width',width)
    
    v.set(filter1,'poly','fill',color1)
    v.set(filter1,'line','stroke',stroke)
    v.set(filter1,'line','stroke-width',width)

    f = '(' + filter1 + ') and ' + '(' + filter2 + ')'
    c = colors.darken(color1,color2)
    v.set(f,'poly','fill',c)
    v.set(f,'line','stroke',stroke)
    v.set(f,'line','stroke-width',width)
    
    f = '(' + filter1 + ') and ' + '(' + filter3 + ')'
    c = colors.darken(color1,color3)
    v.set(f,'poly','fill',c)
    v.set(f,'line','stroke',stroke)
    v.set(f,'line','stroke-width',width)
    
    f = '(' + filter2 + ') and ' + '(' + filter3 + ')'
    c = colors.darken(color2,color3)
    v.set(f,'poly','fill',c)
    v.set(f,'line','stroke',stroke)
    v.set(f,'line','stroke-width',width)    
    
    f = '(' + filter1 + ') and ' + '(' + filter2 + ') and ' + '(' + filter3 + ')'
    c = colors.darken(color1,colors.darken(color2,color3))
    v.set(f,'poly','fill',c)
    v.set(f,'line','stroke',stroke)
    v.set(f,'line','stroke-width',width)
    
    # Create the SVG
    displ = 1.5*fontsize
    h = displ + 2.6*radius + displ
    w = displ + 2.6*radius + displ

    ydispl = 0
    if len(title) > 0:
        ydispl = 0.8*displ
        h += displ

    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">\n' % (w, h)

    if len(title) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (0.5*w, 1.1*fontsize, 1.05*fontsize, fontweight, title)

    svg += '<circle cx="%f" cy="%f" r="%f" fill="%s"></circle>'                                 % (0.333*w, 0.666*h, radius, color1)
    svg += '<circle cx="%f" cy="%f" r="%f" fill="%s" style="mix-blend-mode: darken;"></circle>' % (0.666*w, 0.666*h, radius, color2)
    svg += '<circle cx="%f" cy="%f" r="%f" fill="%s" style="mix-blend-mode: darken;"></circle>' % (0.500*w, 0.390*h, radius, color3)
    
    svg += '<text x="%f" y="%f" text-anchor="end"    font-size="%f" fill="black" font-weight="%d" >%s</text>' % (0.333*w, 0.666*h+fontsize,     fontsize, fontweight, title1)
    svg += '<text x="%f" y="%f" text-anchor="start"  font-size="%f" fill="black" font-weight="%d" >%s</text>' % (0.666*w, 0.666*h+fontsize,     fontsize, fontweight, title2)
    svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (0.500*w, 0.390*h-1.5*fontsize, fontsize, fontweight, title3)


    svg += '</svg>'
    return svg
    
    
###########################################################################################################################################################################
# Sets a complex trivariate legend for vector layer v based on three numerical attributes
# Returns a legend in SVG string format
###########################################################################################################################################################################
def trivariateLegendEx(v,
                       attribute1,
                       attribute2,
                       attribute3,
                       n=3,
                       min1=0.0,
                       max1=100.0,
                       min2=0.0,
                       max2=100.0,
                       min3=0.0,
                       max3=100.0,
                       color1='#ff80f7',
                       color2='#00d1d0',
                       color3='#cfb000',
                       color4='#ffffff',
                       title='',
                       title1='',
                       title2='',
                       title3='',
                       fontsize=14,
                       fontweight=400,
                       stroke='#000000',
                       stroke_width=0.25,
                       side=200,
                       resizewidth='',
                       resizeheight='',
                       digits=2,
                       maxticks=0,
                       showarrows=True):
    """
    Creation of a trivariate choropleth legend for a polygon vector layer. See `Choropleth maps with tricolore <https://cran.r-project.org/web/packages/tricolore/vignettes/choropleth_maps_with_tricolore.html>`_ for the idea. The function creates a legend for vector layer v based on three attributes of the layer and returns a string containing the SVG representation of the legend in the form of a triangle (that can be displayed using display(HTML(svgstring) call)

    Note
    ----
    This function is built on top of the BDAP interapro library to display dynamic geospatial dataset. For this reason it is not portable in other environments! Please refer to the module :py:mod:`lefletMap` for geospatial function not related to BDAP.
    
    Parameters
    ----------
    v : instance of inter.VectorLayer class
        Vector layer instance for which the trivariate legend has to be built
    attribute1 : str
        Name of the first numerical attribute
    attribute2 : str
        Name of the second numerical attribute
    attribute3 : str
        Name of the third numerical attribute
    n : int, optional
        Number of intervals for each of the three numerical attributes (default is 3). Accepptable values are those in the range [2,10]
    min1 : float, optional
        Minimum value for the first attribute (default is 0.0)
    max1 : float, optional
        Maximum value for the first attribute (default is 100.0)
    min2 : float, optional
        Minimum value for the second attribute (default is 0.0)
    max2 : float, optional
        Maximum value for the second attribute (default is 100.0)
    min3 : float, optional
        Minimum value for the third attribute (default is 0.0)
    max3 : float, optional
        Maximum value for the third attribute (default is 100.0)
    color1 : str, optional
        Color to assign to polygons that have the maximum value on the first attribute (default is '#ff80f7')
    color2 : str, optional
        Color to assign to polygons that have the maximum value on the second attribute (default is '#00d1d0')
    color3 : str, optional
        Color to assign to polygons that have the maximum value on the third attribute (default is '#cfb000')
    color4 : str, optional
        Color to assign to polygons that have all the three values of the attributes smaller than the corresponding minimal value (default is '#ffffff'). For this color, the transparency can be set, for instance using '#ffffff88' for partial transparency or '#ffffffff' for full transparency.
    title : str, optional
        Main title of the legend chart (default is '')
    title1 : str, optional
        Title for the legend on the first attribute. It will be displayed on the bottom side of the triangle SVG. Default is ''.
    title2 : str, optional
        Title for the legend on the second attribute. It will be displayed on the right side of the triangle SVG. Default is ''.
    title3 : str, optional
        Title for the legend on the third attribute. It will be displayed on the left side of the triangle SVG. Default is ''.
    fontsize : int, optional
        Size in pixels of the font used for texts (default is 14)
    fontweight : int, optional
        Weight of the font used for title texts (default is 400)
    stroke : str, optional
        Color to use for the border of the polygons (default is '#000000')
    stroke_width : float, optional
        Width in pixels of the stroke to use for the border of the polygons (default is 0.25)
    side : int, optional
        Dimension in pixels of one side of the triangle displayed in the SVG legend (default is 200)
    resizewidth : str, optional
        Width of the resizing container (default is '')
    resizeheight : str, optional
        height of the resizing container (default is '')
    digits : int, optional
        Number of decimal digits to use for displaying numerical values on the axis of the SVG chart (default is 2)
    maxticks: int, optional
        Maximum number of tick marks to display on each of the triangle sides. If 0 or less, the ticks for all the intervals are shown. Default is 0
    showarrows : bool, optional
        If True displays small arrows to help identify the three axes (default is True)

    Returns
    -------
        a string containing SVG text to display the trivariate legend using a call to display(HTML(...))

    Example
    -------
    Creation of a complex trivariate choropleth legend for a polygons layer containing crop data. The three attributes AL_PERC, PC_PERC and PG_PERC contain the percentage presence of the three specific crops inside the polygon::
    
        from ipywidgets import widgets, Layout, HTML
        from IPython.display import display
        
        from jeodpp import inter, imap
        from vois import interMap
        
        # Load data
        vector = inter.loadLocalVector("DEBY_2019_LandCover.shp")
        vector = vector.parameter("identifyfield", "LAU_NAME YEAR AL_PERC PC_PERC PG_PERC")
        vector = vector.parameter("identifyseparator", "<br>")
        
        # Create and display a Map instance
        m = imap.Map(basemap=60, layout=Layout(height='600px'))
        display(m)
        
        svg = interMap.trivariateLegendEx(vector,
                                          "AL_PERC",
                                          "PC_PERC",
                                          "PG_PERC",
                                          6,
                                          0.0,
                                          100.0,
                                          0.0,
                                          100.0,
                                          0.0,
                                          100.0,
                                          color1='#ff80f7',
                                          color2='#00d1d0',
                                          color3='#cfb000',
                                          color4='#ffffff00',
                                          title='Complex Trivariate Choropleth',
                                          title1="Arable Land",
                                          title2="Perm. Crop",
                                          title3="Perm. Grassl.",
                                          fontsize=18,
                                          fontweight=500,
                                          side=400,
                                          digits=0,
                                          maxticks=5,
                                          showarrows=True)


        # Display of the vector layer on the map
        p = vector.process()
        m.clear()
        m.addLayer(p.toLayer())
        m.zoomToImageExtent(p)

        inter.identifyPopup(m,p)

        # Display the trivariate choropleth legend
        display(HTML(svg))
        
        
    .. figure:: figures/trivariateex.png
       :scale: 100 %
       :alt: Example of complex trivariate choropleth legend

       Example of an interactive map showing polygons colored with a complex trivariate choropleth legend.
       
    """

    if n < 2:  n = 2
    if n > 10: n = 10
    
    # Convert colors to (r,g,b) tuples
    rgb1 = colors.string2rgb(color1)
    rgb2 = colors.string2rgb(color2)
    rgb3 = colors.string2rgb(color3)
    
    # Maximum distance among small triangles centers
    maxdistance = side * (n - 1) / float(n)
    
    # Steps on the three attributes ranges
    step1 = (max1 - min1) / n
    step2 = (max2 - min2) / n
    step3 = (max3 - min3) / n
    
    
    # Interpolate a color from 3 percentage distance values (d1,d2,d3 in [0.0,1.0])
    def colorInterpolate(d1, d2, d3):
        
        # Weights of the three colors
        w1 = 1.0 - d1
        w2 = 1.0 - d2
        w3 = 1.0 - d3
        
        wtot = w1 + w2 + w3
        if wtot <= 0.000000001:
            return color4
        
        w1 /= wtot
        w2 /= wtot
        w3 /= wtot
        
        r = int(rgb1[0]*w1 + rgb2[0]*w2 + rgb3[0]*w3)
        g = int(rgb1[1]*w1 + rgb2[1]*w2 + rgb3[1]*w3)
        b = int(rgb1[2]*w1 + rgb2[2]*w2 + rgb3[2]*w3)
        return colors.rgb2hex((r,g,b))

                    
    # Returns the list of n points at equal distance on the segment (x1,y1)->(x2,y2)
    def pointOnSegment(p1,p2, n):
        points = [p1]
        d = 1.0/float(n)
        for i in range(1,n):
            k = d*i
            x = k*p2[0] + (1.0-k)*p1[0]
            y = k*p2[1] + (1.0-k)*p1[1]
            points.append((x,y))
        points.append(p2)
        return points
        
    
    # Returns the center point of a triangle
    def center(p1, p2, p3):
        return ((p1[0]+p2[0]+p3[0])/3.0, (p1[1]+p2[1]+p3[1])/3.0)

    # Returns the distance between two points
    def distance(p1,p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    
    
    # Returns the SVG string to display a filled triangle
    def triangle(p1, p2, p3):
        c = center(p1,p2,p3)
        d1 = distance(c,P1)
        d2 = distance(c,P2)
        d3 = distance(c,P3)
        if d1 <= 0.001*side:
            d1 = 0.0
            color = color1
        else:
            if d2 <= 0.001*side:
                d2 = 0.0
                color = color2
            else:
                if d3 <= 0.001*side:
                    d3 = 0.0
                    color = color3
                else:
                    d1 /= maxdistance
                    d2 /= maxdistance
                    d3 /= maxdistance
                    color = colorInterpolate(d1,d2,d3)
        
        d = side*0.0025
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x3 = p3[0]
        y3 = p3[1]
        
        # Slightly enlarge the triangles so they overlap
        if y1 > y3:
            x1 -= d
            x2 += d
            y1 += d
            y2 += d
            y3 -= d
        else:
            x1 -= d
            x2 += d
            y1 -= d
            y2 -= d
            y3 += d
            
        return '<path d="M%f %f L%f %f L%f %f z" stroke-width="0" fill="%s"/>' % (x1,y1, x2,y2, x3,y3, color)

    
    # Maps a value x from [xmin,ymin] to [x1,x2]
    def linearMap(x,xmin,xmax, x1,x2):
        if   x <= xmin: return x1
        elif x >= xmax: return x2
        else:
            p = (x - xmin)/(xmax - xmin)
            return (1.0 - p)*x1 + p*x2
        
        
    # From a step index returns the interval on one of the attributes plus the distance from the corresponding full color
    def stepToValues(index, minvalue, maxvalue, step, attribname):
        if index == 0:
            return "[" + attribname + "] < "  + str(minvalue+step), maxdistance
        elif index >= n-1:
            return "[" + attribname + "] >= " + str(maxvalue-step), 0.0
        else:
            return "[" + attribname + "] >= " + str(minvalue+index*step) + " and [" + attribname + "] < " + str(minvalue+(index+1)*step), (n-index-1)*maxdistance/float(n)

        
    # Legend creation for the vector layer
    width = str(stroke_width)
    v.reset()
    v.set('all','poly','fill',color4)
    v.set('all','line','stroke',stroke)
    v.set('all','line','stroke-width',width)

    for i1 in range(n):
        for i2 in range(n):
            for i3 in range(n):
                filter1,d1 = stepToValues(i1, min1, max1, step1, attribute1)
                filter2,d2 = stepToValues(i2, min2, max2, step2, attribute2)
                filter3,d3 = stepToValues(i3, min3, max3, step3, attribute3)
                filterall = filter1 + " and " + filter2 + " and " + filter3
                
                if d1 <= 0.001*side:
                    d1 = 0.0
                    color = color1
                else:
                    if d2 <= 0.001*side:
                        d2 = 0.0
                        color = color2
                    else:
                        if d3 <= 0.001*side:
                            d3 = 0.0
                            color = color3
                        else:
                            d1 /= maxdistance
                            d2 /= maxdistance
                            d3 /= maxdistance
                            color = colorInterpolate(d1,d2,d3)
                v.set(filterall,'poly','fill',color)
                v.set(filterall,'line','stroke',stroke)
                v.set(filterall,'line','stroke-width',width)
    
    displ = 4*fontsize
    tside = side
    th    = side * 0.5 * math.sqrt(3.0)
    w = displ + tside + displ
    h = 0.5*displ + th + 0.5*displ
        
    if len(resizewidth)  <= 0: resizewidth  = '%fpx' % w
    if len(resizeheight) <= 0: resizeheight = '%fpx' % h
        
    ydispl = 0
    if len(title) > 0:
        ydispl = 0.8*displ
        h += displ

    x1 = displ
    x2 = x1 + tside
    x3 = 0.5*(x1+x2)
    y1 = y2 = h - displ
    y3 = y1 - th
            
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" width="%s" height="calc(%s + 20px)" version="1.1">\n' % (w,h, resizewidth,resizeheight)

    if len(title) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (x3, 1.25*fontsize, 1.05*fontsize, fontweight, title)

    # Height of the small triangles
    sh = th/float(n)
        
    # Returns the third point of a triangle having p1 and p2 as the base points
    def third(p1,p2, h):
        return (0.5*(p1[0]+p2[0]), p1[1]+h)
        
        
    # Center points of the three triangles on the three corners
    points = pointOnSegment((x1,y1),(x2,y2),n)
    pa = points[-2]
    pb = points[-1]
    pc = third(pa,pb,-sh)
    P1 = center(pa,pb,pc)
        
    points = pointOnSegment((x2,y2),(x3,y3),n)
    pa = (points[-2][0]-side/n,points[-2][1])
    pb = points[-2]
    pc = points[-1]
    P2 = center(pa,pb,pc)
        
    points = pointOnSegment((x1,y1),(x2,y2),n)
    pa = points[0]
    pb = points[1]
    pc = third(pa,pb,-sh)
    P3 = center(pa,pb,pc)

    # Creation of the small triangles
    p1 = (x1,y1)
    p2 = (x2,y2)
    for level in range(n):
        points = pointOnSegment(p1,p2,n-level)
        for i in range(n-level):
            p1 = points[i]
            p2 = points[i+1]
            svg += triangle(p1,p2,third(p1,p2,-sh))
            if i < n-level-1:
                p3 = points[i+2]
                svg += triangle(third(p1,p2,-sh),third(p2,p3,-sh),p2)

        p1 = third(points[0], points[1], -sh)
        p2 = third(points[-2],points[-1],-sh)
                
        
    # External border pf the triangle
    swidth = side/140.0
    d = side*0.005
    svg += '<path d="M%f %f L%f %f L%f %f z" stroke="black" stroke-width="%f" fill="none"/>' % (x1-d,y1+d, x2+d,y2+d, x3,y3-d, swidth)
        
        
    # Text for the three attributes
    if len(title1) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (x2, y2+2.5*fontsize, fontsize, fontweight, title1)
    if showarrows:
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (x2-2*fontsize, y2+1.45*fontsize, x2, y2+1.45*fontsize)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (x2, y2+1.45*fontsize, x2-0.2*fontsize, y2+1.25*fontsize)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (x2, y2+1.45*fontsize, x2-0.2*fontsize, y2+1.65*fontsize)
        
    if len(title2) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (x3, y3-1.1*fontsize, fontsize, fontweight, title2)
    if showarrows:
        points = pointOnSegment((x3,y3),(x2,y2),10)
        ax1 = points[0][0]+3.2*fontsize
        ax2 = points[1][0]+3.2*fontsize
        ay1 = points[0][1]+fontsize
        ay2 = points[1][1]+fontsize
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax2,ay2)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax1+0.3*fontsize,ay1)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax1-0.15*fontsize,ay1+0.3*fontsize)
        
    if len(title3) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="%d" >%s</text>' % (x1, y1+2.5*fontsize, fontsize, fontweight, title3)
    if showarrows:
        points = pointOnSegment((x1,y1),(x3,y3),10)
        ax1 = points[0][0]-2.2*fontsize
        ax2 = points[1][0]-2.2*fontsize
        ay1 = points[0][1]-fontsize
        ay2 = points[1][1]-fontsize
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax2,ay2)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax1+0.36*fontsize,ay1-0.05*fontsize)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke="black" stroke-width="1.0" fill="black"/>' % (ax1,ay1,ax1-0.15*fontsize,ay1-0.35*fontsize)
        
    # Texts on the three axes
    f = "{:.%df}" % digits
        
    nticks = n
    if maxticks > 0 and maxticks < nticks: nticks = maxticks
    points = pointOnSegment((x1,y1),(x2,y2),nticks)
    for index, p in enumerate(points):
        v = linearMap(index, 0, nticks, min1, max1)
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" fill="black" font-weight="300" >%s</text>' % (p[0], p[1]+1.1*fontsize, 0.9*fontsize, f.format(v))
        
    points = pointOnSegment((x2,y2),(x3,y3),nticks)
    for index, p in enumerate(points):
        v = linearMap(index, 0, nticks, min2, max2)
        svg += '<text x="%f" y="%f" text-anchor="start" font-size="%f" fill="black" font-weight="300" >%s</text>' % (p[0]+0.3*fontsize, p[1], 0.9*fontsize, f.format(v))
            
    points = pointOnSegment((x3,y3),(x1,y1),nticks)
    for index, p in enumerate(points):
        v = linearMap(index, 0, nticks, min3, max3)
        svg += '<text x="%f" y="%f" text-anchor="end" font-size="%f" fill="black" font-weight="300" >%s</text>' % (p[0]-0.3*fontsize, p[1], 0.9*fontsize, f.format(v))
            
        
    svg += '</svg>'
    return svg
    