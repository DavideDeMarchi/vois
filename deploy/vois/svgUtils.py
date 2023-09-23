"""SVG drawings for general use."""
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
from ipywidgets import HTML, widgets, Layout
from ipyevents import Event
from IPython.display import display
import math
from datetime import datetime
from textwrap import wrap

try:
    from . import colors
    from .vuetify import fontsettings
    from .vuetify import settings
except:
    import colors
    from vuetify import fontsettings
    from vuetify import settings


###########################################################################################################################################################################
# Returns a string containing the legend for a vector layer classification in SVG format
###########################################################################################################################################################################
def categoriesLegend(title, descriptions, width=200, elemHeight=38, bordercolor='black', borderWidth=2, textcolor='black',
                     colorlist=['#fef4ef', '#fdd3c0', '#fca080', '#fa6a49', '#e23026', '#b11117', '#66000c'],
                     dark=settings.dark_mode):
    """
    Creation of a legend for categories given title and descriptions of the classes.
    
    Parameters
    ----------
    title : str
        Title of the legend
    descriptions : list of strings
        Description of each of the classe of the legend. If a description contains a '\t' character, the text after it is displayed as multi-line text in smaller font
    width : int, optional
        Width in pixel of the legend (default is 200)
    elemHeight : int, optional
        Height in pixels of each of the  elements of the legend (default is 38)
    bordercolor : str, optional
        Color of the border of the legend elements (default is 'black')
    borderWidth : int, optional
        Width in pixels of the border of the legend elements (default is 2)
    textcolor : str, optional
        Color of text for the legend elements (default is 'black')
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    dark : bool, optional
        If True, the bordercolor and textcolor are set to white (default is False)
    
    Return
    ------
        a string containing SVG text to display the legend
    
    Example
    -------
    Example of the creation of an SVG drawing for a categories legend::
    
        from vois import svgUtils
        import plotly.express as px

        svg = svgUtils.categoriesLegend("Legend title",
                                        ['1:\tVery long class description that can span multiple lines and that contains no info at all',
                                         'Class 2', 'Class 3', 'Class 4'],
                                        colorlist=px.colors.sequential.Blues,
                                        width=250)
        display(HTML(svg))
        
    .. figure:: figures/categoriesLegend.png
       :scale: 100 %
       :alt: categoriesLegend example

       Example of a categories legend

    """
    
    def multilineText(x,y,width,height, text):
        return '''
<switch>
   <foreignObject x="%d" y="%d" width="%d" height="%d">
     <div style="display: table-cell; vertical-align: middle; width: %dpx; height: %dpx;">
       <p xmlns="http://www.w3.org/1999/xhtml" style="line-height: 14px; font-size: 8pt;">%s</p>
     </div>
   </foreignObject>
   <text x="%d" y="%d">Your SVG viewer cannot display html.</text>
  <title>%s</title>
</switch>''' % (x,y,width,height,width,height, text, x,y, text)
    
    if dark:
        if bordercolor=='black': bordercolor='white'
        if textcolor  =='black': textcolor  ='white'
            
    x = 0
    y = 12
    space = 4
    n = len(descriptions)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">\n' % (width, 28+n*(elemHeight+space))
    
    svg += '<text text-anchor="start" x="%d" y="%d" font-size="15" fill="%s" font-weight="500">%s</text>' % (x, y+5, textcolor, title)
    y += elemHeight/2
    
    s = colors.colorInterpolator(colorlist, 1, max(2,n))
    for i in range(n):
        col = s.GetColor(i+1)
        text = descriptions[i]
        if '\t' in text:
            value = text.split('\t')[0]
            text  = text.split('\t')[1]
            svg += '<rect style="fill:%s;" x="%d" y="%d" width="%d" height="%d" stroke="%s" stroke-width="%d"><title>%s</title></rect>\n' % (col, x+1, y, elemHeight-1, elemHeight-1, bordercolor, borderWidth, value)
            svg += '<text text-anchor="start" x="%d" y="%d" font-size="15" fill="%s" font-weight="400">%s<title>%s</title></text>' % (x+elemHeight+space, y+elemHeight/2+4, textcolor, value, text)
            if len(text) > 0: svg += multilineText(x+2*elemHeight,y-1,width-2*elemHeight-space,elemHeight+10, text)
        else:
            value = text
            svg += '<rect style="fill:%s;" x="%d" y="%d" width="%d" height="%d" stroke="%s" stroke-width="%d"><title>%s</title></rect>\n' % (col, x+1, y, elemHeight-1, elemHeight-1, bordercolor, borderWidth, text)
            svg += '<text text-anchor="start" x="%d" y="%d" font-size="15" fill="%s" font-weight="400">%s<title>%s</title></text>' % (x+elemHeight+space, y+elemHeight/2+4, textcolor, value, text)
                
        y += elemHeight + space

    svg += '</svg>'
    return svg






###########################################################################################################################################################################
# Returns svg string containing a vertical graduated/colors legend
###########################################################################################################################################################################
def graduatedLegend(df,                          # Pandas dataframe indexed on code_column and containing 'value' and 'label' columns
                    code_column=None,            # Name of the column containing the code of the country (None = the country code is the index of the dataframe)
                    value_column='value',        # Name of the column containing the value
                    label_column='label',        # Name of the column containing the label
                    dictnames=None,              # Dict to convert codes to names
                    codes_selected=[],           # codes of the countries selected
                    colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
                    stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                    fill='#f1f1f1',              # fill color for countries
                    stroke_selected='#00ffff',   # stroke color for border of selected country
                    decimals=2,                  # Number of decimals for the legend number display
                    minallowed_value=None,       # Minimum value allowed
                    maxallowed_value=None,       # Maximum value allowed
                    hoveronempty=False,          # If True highlights polygon on hover even if no value present in input df for the polygon
                    legendtitle='',              # Title to add to the legend (top)
                    legendunits='',              # Units of measure to add to the legend (bottom)
                    fontsize=20,
                    width=200,
                    height=600,
                    bordercolor='black',
                    textcolor='black',
                    dark=False):
    """
    Creation of graduated legend in SVG format. Given a Pandas DataFrame in the same format of the one in input to :py:func:`interMap.geojsonMap` function, this functions generates an SVG drawing displaying a graduated colors legend. 

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame to use for assigning values to features. It has to contain at least a column with numeric values.
    code_column : str, optional
        Name of the column of the df Pandas DataFrame containing the unique code of the features. This column is used to perform the join with the internal attribute of the geojson vector dataset that contains the unique code. If the code_column is None, the code is taken from the index of the DataFrame, (default is None)
    value_column : str, optional
        Name of the column of the Pandas DataFrame containing the values to be assigned to the features using the join on geojson unique codes (default is 'value')
    label_column : str, optional
        Name of the column of the Pandas DataFrame containing the label to be assigned to the features using the join on geojson unique codes (default is 'label')
    dictnames : dict, optional
        Dictionary to convert codes to names when displaying the selection (default is None)
    codes_selected : list of strings, optional
        List of codes of features to display as selected (default is [])
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to features and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    fill : str, optional
        Fill color to use for the features that are not joined (default is '#f1f1f1')
    stroke_selected : str, optional
        Color to use for the selected features (default is '#00ffff')
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    hoveronempty : bool, optional
        If True highlights polygon on hover even if no value present in input df for the feature (default is False)
    legendtitle : str, optional
        Title to add on top of the legend (default is '')
    legendunits : str, optional
        Units of measure to add to the bottom of the legend (default is '')
    fontsize : int, optional
        Size in pixels of the font used for texts (default is 20)
    width : int, optional
        Width of the SVG drawing in pixels (default is 200)
    height : int, optional
        Height of the SVG drawing in pixels (default is 600)
    bordercolor : str, optional
        Color for lines and rects of the legend (default is 'black')
    textcolor : str, optional
        Color for texts of the legend (default is 'black')
    dark : bool, optional
        If True, the bordercolor and textcolor are set to white (default is False)
        
    Returns
    -------
        a string containing SVG text to display the graduated legend

    Example
    -------
    Creation of a SVG drawing to display a graduated legend. Input is prepared in the same way of the example provided for the :py:func:`interMap.geojsonMap` function::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from vois import svgMap, svgUtils

        countries = svgMap.country_codes

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        svg = svgUtils.graduatedLegend(df, code_column='iso2code',
                                       codes_selected=['IT', 'FR', 'CH'],
                                       stroke_selected='red',
                                       colorlist=px.colors.sequential.Viridis[::-1],
                                       stdevnumber=2.0,
                                       legendtitle='2020 Total energy consumption',
                                       legendunits='KTOE per 100K inhabit.',
                                       fontsize=18,
                                       width=340, height=600)
        display(HTML(svg))

    .. figure:: figures/graduatedLegend.png
       :scale: 100 %
       :alt: graduatedLegend example

       Example of a graduatedLegend in SVG
        
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

    if dark:
        if bordercolor=='black': bordercolor='white'
        if textcolor  =='black': textcolor  ='white'
    
    # Positioning of the legend
    w = width // 5
    x1 = (width-w)/2
    x2 = x1 + w
    wlineette = width // 20
    
    #y1 = height // 18
    y1 = 2*fontsize
    h = height - int(1.5*y1)
    if len(legendunits) > 0:
        h -= y1//2
    y2 = y1 + h
    
    barthickness = width/120
    fontsize1 = fontsize - 1
    fontsize2 = fontsize - 2
    
    # Calculate the legend in SVG format
    svg = '''
<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" version="1.1">
  <style type="text/css">
     @import url('%s');
''' % (width,height,fontsettings.font_url)

    # Colors indexed by iso2_code of countries
    polycolors = {}    # Fill color of the polygon
    polyclass  = {}    # class to assign to the polygon ("country" or "")
    polybary   = {}    # Y coordinate of the bar on the legend highlighted when hover on a country
    polyover   = {}    # True if a value is outside of the legend
    polyname   = {}    # Name assigned to the polygon
    
    country_codes = df[code_column].unique()
    
    for c in country_codes:
        polycolors[c] = fill
        polybary[c]   = -1000
        polyover[c]   = False
        
        if hoveronempty:
            polyclass[c] = 'country'
        else:
            polyclass[c] = ''
        
    # Set colors for all the countries
    for index, row in df.iterrows():
        if code_column is None: code = index
        else:                   code = row[code_column]

        polyname[code] = code
        if not dictnames is None and code in dictnames:
            polyname[code] = dictnames[code]
            
        value = row[value_column]
        polycolors[code] = ci.GetColor(value)
        polyclass[code]  = 'country'

        if label_column in df:
            v = row[label_column]
        else:
            v = str(value)
                
        y = y2 - (y2-y1) * (value - minvalue) / (maxvalue - minvalue)
        if y < y1: y = y1
        if y > y2: y = y2
        polybary[code] = y
        
        if value < minvalue or value > maxvalue:
            polyover[code] = True
            
    #print(minvalue,maxvalue, y1, y2)
        
    # Add color for every polygon
    for c in country_codes:
        svg += 'svg #%s { fill: %s; }\n' % (c, polycolors[c])
        
    svg += '</style>'

    
    # Legend on the right
    if len(legendtitle) > 0:
        svg += '<text x="%d" y="%d" text-anchor="middle" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s</text>' % (x1+w/2.0, y1-fontsize, fontsize, fontsettings.font_name, textcolor, legendtitle)
        
    if len(legendunits) > 0:
        svg += '<text x="%d" y="%d" text-anchor="middle" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s</text>' % (x1+w/2.0, int(y2+fontsize*1.5), fontsize2, fontsettings.font_name, textcolor, legendunits)
        
    svg += '<rect x="%d" y="%d" width="%d" height="%d" style="fill:none; stroke-width:%f; stroke:%s;" />' % (x1, y1, w, h+1, barthickness*2, bordercolor)
    
    y = y2
    for i in range(h):
        value = maxvalue - (y - y1) * (maxvalue - minvalue) / (y2 - y1)
        svg += '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:%f" />' % ( x1,y,x2,y, ci.GetColor(value), barthickness )
        y -= 1
        
    svg += '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s; stroke-width:%f" />' % ( x2,y2+3,x2+wlineette,y2+3, bordercolor, barthickness/2.0 )
    svg += '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s; stroke-width:%f" />' % ( x2,y1-2,x2+wlineette,y1-2, bordercolor, barthickness/2.0 )
    
    valmin = '{:.{prec}f}'.format(minvalue, prec=decimals)
    svg += '<text x="%d" y="%d" font-size="%f" font-family="%s" fill="%s">%s</text>' % (x2+wlineette+5, y2+fontsize2/3, fontsize1, fontsettings.font_name, textcolor, valmin)
    
    valmax = '{:.{prec}f}'.format(maxvalue, prec=decimals)
    svg += '<text x="%d" y="%d" font-size="%f" font-family="%s" fill="%s">%s</text>' % (x2+wlineette+5, int(y1+fontsize2*0.4), fontsize1, fontsettings.font_name, textcolor, valmax)
    
    valmed = '{:.{prec}f}'.format((minvalue+maxvalue)/2.0, prec=decimals)
    if valmed != valmin and valmed != valmax:
        y = (y1+y2)/2.0
        svg += '<line x1="%d" y1="%f" x2="%d" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%d" y="%d" font-size="%f" font-family="%s" fill="%s">%s</text>' % (x2+wlineette+5, y+fontsize2/3, fontsize1, fontsettings.font_name, textcolor, valmed)
        
    val = '{:.{prec}f}'.format(minvalue + 3.0*(maxvalue-minvalue)/4.0, prec=decimals)
    if val != valmed and val != valmax:
        y = y1+(y2-y1)/4.0
        svg += '<line x1="%d" y1="%f" x2="%d" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%d" y="%d" font-size="%f" font-family="%s" fill="%s">%s</text>' % (x2+wlineette+5, y+fontsize2/3, fontsize1, fontsettings.font_name, textcolor, val)
        
    val = '{:.{prec}f}'.format(minvalue + (maxvalue-minvalue)/4.0, prec=decimals)
    if val != valmin and val != valmed:
        y = y1+3.0*(y2-y1)/4.0
        svg += '<line x1="%d" y1="%f" x2="%d" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%d" y="%d" font-size="%f" font-family="%s" fill="%s">%s</text>' % (x2+wlineette+5, y+fontsize2/3, fontsize1, fontsettings.font_name, textcolor, val)
    
    
    # Add horizontal lines in the legend for the selected countries
    for code in codes_selected:
        if code in country_codes:
            if polybary[code] >= y1 and polybary[code] <= y2:
                svg += '<text x="%f" y="%f" text-anchor="end" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s<title>%s</title></text>' % (x1-wlineette/2, polybary[code]+fontsize2/3, fontsize2, fontsettings.font_name, textcolor, polyname[code], polyname[code])

                dash = ''
                if polyover[code]:
                    dash = 'stroke-dasharray="%f,%f"' % (wlineette*1.1, wlineette*0.5)
                svg += '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s; stroke-width:%f" %s />' % (x1, polybary[code], x2, polybary[code], stroke_selected, barthickness, dash)
    
    svg += '</svg>'
    return svg




###########################################################################################################################################################################
# Returns svg string containing a vertical graduated/colors legend
###########################################################################################################################################################################
def graduatedLegendVWVH(df,                          # Pandas dataframe indexed on code_column and containing 'value' and 'label' columns
                    code_column=None,            # Name of the column containing the code of the country (None = the country code is the index of the dataframe)
                    value_column='value',        # Name of the column containing the value
                    label_column='label',        # Name of the column containing the label
                    codes_selected=[],           # codes of the countries selected
                    colorlist=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],   # default color scale
                    stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                    fill='#f1f1f1',              # fill color for countries
                    stroke_selected='#00ffff',   # stroke color for border of selected country
                    decimals=2,                  # Number of decimals for the legend number display
                    minallowed_value=None,       # Minimum value allowed
                    maxallowed_value=None,       # Maximum value allowed
                    hoveronempty=False,          # If True highlights polygon on hover even if no value present in input df for the polygon
                    legendtitle='',              # Title to add to the legend (top)
                    legendunits='',              # Units of measure to add to the legend (bottom)
                    fontsize=20,
                    width=20.0,
                    height=40.0,
                    bordercolor='black',
                    textcolor='black',
                    dark=False):
    """
    Creation of graduated legend in SVG format. Given a Pandas DataFrame in the same format of the one in input to :py:func:`interMap.geojsonMap` function, this functions generates an SVG drawing displaying a graduated colors legend. 

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame to use for assigning values to features. It has to contain at least a column with numeric values.
    code_column : str, optional
        Name of the column of the df Pandas DataFrame containing the unique code of the features. This column is used to perform the join with the internal attribute of the geojson vector dataset that contains the unique code. If the code_column is None, the code is taken from the index of the DataFrame, (default is None)
    value_column : str, optional
        Name of the column of the Pandas DataFrame containing the values to be assigned to the features using the join on geojson unique codes (default is 'value')
    label_column : str, optional
        Name of the column of the Pandas DataFrame containing the label to be assigned to the features using the join on geojson unique codes (default is 'label')
    codes_selected : list of strings, optional
        List of codes of features to display as selected (default is [])
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Plasma, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    stdevnumber : float, optional
        The correspondance between the values assigned to features and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the country values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    fill : str, optional
        Fill color to use for the features that are not joined (default is '#f1f1f1')
    stroke_selected : str, optional
        Color to use for the border of the selected features (default is '#00ffff')
    decimals : int, optional
        Number of decimals for the legend numbers display (default is 2)
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    hoveronempty : bool, optional
        If True highlights polygon on hover even if no value present in input df for the feature (default is False)
    legendtitle : str, optional
        Title to add on top of the legend (default is '')
    legendunits : str, optional
        Units of measure to add to the bottom of the legend (default is '')
    fontsize : int, optional
        Size in pixels of the font used for texts (default is 20)
    width : float, optional
        Width of the SVG drawing in vw units (default is 20.0)
    height : float, optional
        Height of the SVG drawing in vh units (default is 40.0)
    bordercolor : str, optional
        Color for lines and rects of the legend (default is 'black')
    textcolor : str, optional
        Color for texts of the legend (default is 'black')
    dark : bool, optional
        If True, the bordercolor and textcolor are set to white (default is False)
        
    Returns
    -------
        a string containing SVG text to display the graduated legend

    Example
    -------
    Creation of a SVG drawing to display a graduated legend. Input is prepared in the same way of the example provided for the :py:func:`interMap.geojsonMap` function::
        
        import numpy as np
        import pandas as pd
        import plotly.express as px
        from vois import svgMap, svgUtils

        countries = svgMap.country_codes

        # Generate random values and create a dictionary: key=countrycode, value=random in [0.0,100.0]
        d = dict(zip(countries, list(np.random.uniform(size=len(countries),low=0.0,high=100.0))))

        # Create a pandas dataframe from the dictionary
        df = pd.DataFrame(d.items(), columns=['iso2code', 'value'])

        svg = svgUtils.graduatedLegend(df, code_column='iso2code',
                                       codes_selected=['IT', 'FR', 'CH'],
                                       stroke_selected='red',
                                       colorlist=px.colors.sequential.Viridis[::-1],
                                       stdevnumber=2.0,
                                       legendtitle='2020 Total energy consumption',
                                       legendunits='KTOE per 100K inhabit.',
                                       fontsize=18,
                                       width=340, height=600)
        display(HTML(svg))

    .. figure:: figures/graduatedLegend.png
       :scale: 100 %
       :alt: graduatedLegend example

       Example of a graduatedLegend in SVG
        
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

    if dark:
        if bordercolor=='black': bordercolor='white'
        if textcolor  =='black': textcolor  ='white'

    # Sizable dimensioning
    svgwidth = 100.0
    aspectratio = 0.5*height / width   # In landscape mode, usually the height is half the width dimension!!!
    svgheight = svgwidth * aspectratio
            
    # Positioning of the legend
    w = svgwidth / 5.0
    x1 = (svgwidth-w)/2
    x2 = x1 + w
    wlineette = svgwidth / 25.0
    
    #y1 = height // 18
    y1 = 2*fontsize
    h = svgheight - 1.5*y1
    if len(legendunits) > 0:
        h -= y1/2.0
    y2 = y1 + h
    
    barthickness = width/50.0
    fontsize1 = fontsize*0.92
    fontsize2 = fontsize*0.85
    
    # Calculate the legend in SVG format
    preserve = 'xMidYMid meet'
    svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" viewBox="0 0 %f %f" preserveAspectRatio="%s" width="%fvw" height="%fvh">' % (svgwidth,svgheight, preserve, width,height)
    
    svg += '''
  <style type="text/css">
     @import url('%s');
''' % fontsettings.font_url

    # Colors indexed by iso2_code of countries
    polycolors = {}    # Fill color of the polygon
    polyclass  = {}    # class to assign to the polygon ("country" or "")
    polybary   = {}    # Y coordinate of the bar on the legend highlighted when hover on a country
    
    country_codes = df[code_column].unique()
    
    for c in country_codes:
        polycolors[c] = fill
        polybary[c]   = -1000
        if hoveronempty:
            polyclass[c] = 'country'
        else:
            polyclass[c] = ''
        
    # Set colors for all the countries
    for index, row in df.iterrows():
        if code_column is None: code = index
        else:                   code = row[code_column]
        value = row[value_column]
        polycolors[code] = ci.GetColor(value)
        polyclass[code]  = 'country'

        if label_column in df:
            v = row[label_column]
        else:
            v = str(value)
                
        y = y2 - (y2-y1) * (value - minvalue) / (maxvalue - minvalue)
        if y < y1: y = y1
        if y > y2: y = y2
        polybary[code] = y
        
    #print(minvalue,maxvalue, y1, y2)
        
    # Add color for every polygon
    for c in country_codes:
        svg += 'svg #%s { fill: %s; }\n' % (c, polycolors[c])
        
    svg += '</style>'

    
    # Legend on the right
    if len(legendtitle) > 0:
        svg += '<text x="%d" y="%d" text-anchor="middle" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s</text>' % (x1+w/2.0, y1-fontsize, fontsize, fontsettings.font_name, textcolor, legendtitle)
        
    if len(legendunits) > 0:
        svg += '<text x="%f" y="%f" text-anchor="middle" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s</text>' % (x1+w/2.0, y2+fontsize*1.5, fontsize2, fontsettings.font_name, textcolor, legendunits)
        
    svg += '<rect x="%f" y="%f" width="%f" height="%f" style="fill:none; stroke-width:%f; stroke:%s;" />' % (x1, y1, w, h, barthickness*4.0, bordercolor)
    
    y = y1
    while y <= y2:
        value = maxvalue - (y - y1) * (maxvalue - minvalue) / (y2 - y1)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s;stroke-width:%f" />' % ( x1,y,x2,y, ci.GetColor(value), barthickness )
        y += 0.06666
        
    svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y2,x2+wlineette,y2, bordercolor, barthickness/2.0 )
    svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y1,x2+wlineette,y1, bordercolor, barthickness/2.0 )

    xtext = x2 + wlineette*1.25
    
    valmin = '{:.{prec}f}'.format(minvalue, prec=decimals)
    svg += '<text x="%f" y="%f" font-size="%f" font-family="%s" fill="%s">%s</text>' % (xtext, y2+fontsize2/3, fontsize1, fontsettings.font_name, textcolor, valmin)
    
    valmax = '{:.{prec}f}'.format(maxvalue, prec=decimals)
    svg += '<text x="%f" y="%f" font-size="%f" font-family="%s" fill="%s">%s</text>' % (xtext, int(y1+fontsize2*0.4), fontsize1, fontsettings.font_name, textcolor, valmax)
    
    valmed = '{:.{prec}f}'.format((minvalue+maxvalue)/2.0, prec=decimals)
    if valmed != valmin and valmed != valmax:
        y = (y1+y2)/2.0
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%f" y="%f" font-size="%f" font-family="%s" fill="%s">%s</text>' % (xtext, y+fontsize2/3.0, fontsize1, fontsettings.font_name, textcolor, valmed)
        
    val = '{:.{prec}f}'.format(minvalue + 3.0*(maxvalue-minvalue)/4.0, prec=decimals)
    if val != valmed and val != valmax:
        y = y1+(y2-y1)/4.0
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%f" y="%f" font-size="%f" font-family="%s" fill="%s">%s</text>' % (xtext, y+fontsize2/3.0, fontsize1, fontsettings.font_name, textcolor, val)
        
    val = '{:.{prec}f}'.format(minvalue + (maxvalue-minvalue)/4.0, prec=decimals)
    if val != valmin and val != valmed:
        y = y1+3.0*(y2-y1)/4.0
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % ( x2,y,x2+wlineette,y, bordercolor, barthickness/2.0 )
        svg += '<text x="%f" y="%f" font-size="%f" font-family="%s" fill="%s">%s</text>' % (xtext, y+fontsize2/3.0, fontsize1, fontsettings.font_name, textcolor, val)
    
    
    # Add horizontal lines in the legend for the selected countries
    for code in codes_selected:
        if code in country_codes:
            if polybary[code] >= y1 and polybary[code] <= y2:
                svg += '<text x="%f" y="%f" text-anchor="end" font-size="%f" font-family="%s" font-weight="bold" fill="%s">%s</text>' % (x1-wlineette/2, polybary[code]+fontsize2/3, fontsize2, fontsettings.font_name, textcolor, code)
                svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:%s; stroke-width:%f" />' % (x1, polybary[code], x2, polybary[code], stroke_selected, barthickness*3.0)
    
    svg += '</svg>'
    return svg


###########################################################################################################################################################################
# https://www.smashingmagazine.com/2019/01/html5-svg-fill-animation-css3-vanilla-javascript/
# Small circle with animation: returns a widgets.Output object with the SVG displayed on it
###########################################################################################################################################################################
def SmallCircle(text1, text2, percentage, forecolor="#308040", backcolor=None, textcolor='white', dimension=300.0, fontsize=16.0, textsize=0.0):
    """
    Display of a circle graphics displaying a text and a percentage value. It shows an animation to reach the requested percentage of the full circle.
    
    Parameters
    ----------
    text1 : str
        First string of text to display inside the circle (usually a brief description of the variable displayed)
    text2 : str
        Second string of text to display inside the circle (usually the numercal value)
    percentage : float
        Value in percentage to be displayed
    forecolor : str, optional
        Color to use for the circle border (default is '#308040')
    backcolor : str, optional
        Color to use for the interior of the circle (default is None, so a lighter color is generated from the forecolor)
    textcolor : str, optional
        Color to use for text (default is 'white')
    dimension : int or float or str, optional
        Side of the drawing. If an integer or a float is passed, the size is intended in pixels units, otherwise a string containing the units must be passed (example: '4vh'). The default is 300.0 for 300 pixels
    textsize : float, optional
        Text dimension in pixels (default is 0.0 which means that it is automatically calculated from the dimension of the drawing)
        
    Returns
    -------
        an ipywidgets.Output instance with the circle already displayed inside
        
    Example
    -------
    Example of a circle to represent a percentage with an animation::
    
        from vois import svgUtils
        from random import randrange

        percentage = randrange(1000)/10.0
        svgUtils.SmallCircle('Green<br>deal',
                             '%.1f%%' % percentage,
                             percentage,
                             forecolor="#308040",
                             dimension=200)    
    
    .. figure:: figures/smallCircle.png
       :scale: 100 %
       :alt: smallCircle example

       Example of an animated SVG to graphically represent a percentage value
    
    """

    def circumference(r):
        return 2.0 * r * math.pi
    
    def complementaryColor(color):
        if color[0] == '#':
            color = color[1:]
        rgb = (color[0:2], color[2:4], color[4:6])
        comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
        return '#' + ''.join(comp)

    def lighterColor(color):
        if color[0] == '#':
            color = color[1:]
        rgb = (color[0:2], color[2:4], color[4:6])
        comp = ['%02X' % min(255,int(int(a, 16)*1.5)) for a in rgb]
        return '#' + ''.join(comp)

    if backcolor is None:
        backcolor = lighterColor(forecolor)
        
    tooltip = text1.replace('<br>',' ') + ': ' + text2
    if percentage < 0.0:   percentage = 0.0
    if percentage > 100.0: percentage = 100.0
    
    r = 44
    circle = circumference(r)
    #value = 276.46015351590177  # empty
    #value = 0.0                 # full
    value = 0.01 * (100.0 - percentage)*circle
    seconds = 1.0 + (circle - value) / circle
    
    svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 100 100" xml:space="preserve">'

    # CSS styling
    svg += '''
        <style type="text/css">
           @import url('%s');
        </style>
    ''' % (fontsettings.font_url)

        
    svg += '<circle fill="%s" cx="50" cy="50" r="44"><title>%s</title></circle>' % (backcolor,tooltip)
    svg += '<circle fill="none" stroke="#f1f1f1" stroke-width="10" stroke-mitterlimit="0" cx="50" cy="50" r="%d"><title>%s</title></circle>' % (r,tooltip)
    svg += '''
        <circle fill="none" stroke="%s" stroke-width="10.5" stroke-mitterlimit="0" cx="50" cy="50" r="%d" stroke-dasharray="%d" stroke-dashoffset="%d" stroke-linecap="butt" transform="rotate(-90 ) translate(-100 0)">
            <animate attributeName="stroke-dashoffset" values="%d;%d;%d" dur="%fs"></animate>
            <title>%s</title>
        </circle>
    ''' % (forecolor, r, circle, value, circle, value, value, seconds, tooltip)
    

    vtext = text1.split('<br>')
    maxlen = 0
    for t in vtext:
        if len(t) > maxlen: maxlen = len(t)

    if textsize <= 0:  size = 1.0 * 10.0 / float(maxlen)
    else:              size = textsize
        
    if size > 0.9: size = 0.9
    if size < 0.4: size = 0.4
    
    h = int(14 * size)
    y = 47 - (len(vtext)-1)*h
    for t in vtext:
        svg += '<text font-size="%.2fem" text-anchor="middle" x="50" y="%d" fill="%s" font-weight="bold" style="font-family: %s;">%s<title>%s</title></text>' % (size,y, textcolor, fontsettings.font_name,t,tooltip)
        y += h
        
    svg += '<text font-size="1em" text-anchor="middle" x="50" y="62" fill="%s" font-weight="bold" style="font-family: %s;">%s<title>%s</title></text>' % (textcolor, fontsettings.font_name, text2, tooltip)
    
    svg += '</svg>'
    
    # Create an output widget and display SVG in it
    if isinstance(dimension, int):
        w = '%dpx' % dimension
    elif isinstance(dimension, float):
        w = '%fpx' % dimension
    else:
        w = str(dimension)
    out = widgets.Output(layout=Layout(width=w, height='calc(%s + 14px)' % w))

    with out:
        display(HTML(svg))
        
    return out



###########################################################################################################################################################################
# https://mirellavanteulingen.nl/blog/svg-charts-animations.html
# Pie chart with animation: returns a widgets.Output object with the SVG displayed on it + the svg text 
###########################################################################################################################################################################

# Enumeration
class FillPercentage():
    fill100 = 0
    fill75  = 1
    fill60  = 2
    fill50  = 3
    fill40  = 4

def AnimatedPieChart(values=[10.0, 25.0, 34.0, 24.0, 23.0], colors=['#2d82c2', '#95cb92', '#e7ee99', '#ffde88', '#ff945a', '#e34e4f'], labels=None, duration=0.75, # Seconds
                     fillpercentage=FillPercentage.fill60, backcolor="#f1f1f1", dimension=400,
                     textcolor=settings.select_textcolor, fontsize=15, textweight=400, decimals=1,
                     centertext='', centercolor=settings.select_textcolor, centerfontsize=18, centertextweight=500,
                     onclick=None, additional_argument=None, is_selected=False, displayvalues=True):
    """
    Creation of an animated pie chart in SVG format. Given an array of float values, and optional labels, the function draws a pie chart that fills its slices with a short animation. An ipywidgets.Output instance is returned, which has the SVG chart displayed in it. By passing a value to the onclick parameter, it is possible to manage the click event on the slices of the pie, providing interactivity to the drawing. The capture of the click event is done using the `ipyevents library <https://github.com/mwcraig/ipyevents>`_ .
    
    Parameters
    ----------
    values : list of float values, optional
        List of float values that represent the relative dimension of each of the slices (default is [10.0, 25.0, 34.0, 24.0, 23.0])
    colors : list of strings representing colors, optional
        Colors to use for each of the slices of the pie (default is ['#2d82c2', '#95cb92', '#e7ee99', '#ffde88', '#ff945a', '#e34e4f'])
    labels, list of strings, optional
        Labels for each of the slices of the pie (default is None)
    duration : float, optional
        Duration in seconds of the animation (default is 0.75 seconds)
    fillpercentage : int, optional (in 0,1,2,3,4)
        Amount of the circle that is filled by the slices (default is 2 which means 60%)
    backcolor : str, optional
        Background color of the pie (default is '#f1f1f1')
    dimension : int or float or str, optional
        Side of the drawing. If an integer or a float is passed, the size is intended in pixels units, otherwise a string containing the units must be passed (example: '4vh'). Th default is 400.0 for 400 pixels
    textcolor : str, optional
        Color of text
    fontsize : int, optional
        Dimension of text in pixels (default is 15)
    textweight : int, optional
        Weight of text (default is 400, >= 500 is Bold)
    decimals : int, optional
        Number of decimal to use for the display of numbers (default is 1)
    centertext : str, optional
        Text string to display at the center of the pie (default is '')
    centercolor : str, optional
        Color to use for the central text
    centerfontsize : int, optional
        Text dimension for the text displayed at the center of the pie
    centertextweight : int, optional
        Weight of central text (default is 500, >= 500 is Bold)
    onclick : function, optional
        Python function to call when the user clicks on one of the slices of the pie. The function will receive as first parameter the index of the clicked slice, and the additional_argument as second parameter
    additional_argument : any, optional
        Additional parameter passed to the onclick function when the user clicks on one of the slices of the pie (default is None)
    is_selected : bool, optional
        Flag to select the pie chart (default is False)
    displayvalues: bool, optional
        If True each slide of the pie will display, inside parenthesis, the corresponding value (default is True)
   
    
    Return
    ------
        a tuple containing an instance of ipywidgets.Output() widget, and a string containing the SVG code of the drawing
    
    Example
    -------
    Example of a pie chart::
    
        from vois import svgUtils
        import plotly.express as px
        from ipywidgets import widgets

        debug = widgets.Output()
        display(debug)

        def onclick(arg):
            with debug:
                print('clicked %s' % arg)

        out, txt = svgUtils.AnimatedPieChart(values=[10.0, 25.0, 18.0, 20.0, 9.5],
                                             labels=['Option<br>1', 'Option<br>2', 
                                                     'Option 3', 'Option 4',
                                                     'Others'], 
                                             centerfontsize=28,
                                             fontsize=16, textweight=400,
                                             colors=px.colors.qualitative.D3,
                                             backcolor='#dfdfdf',
                                             centertext='Example Pie',
                                             onclick=onclick,
                                             dimension=380.0,
                                             duration=1.0)
        display(out)    


    .. figure:: figures/pieChart2.png
       :scale: 100 %
       :alt: pieChart example

       Example of an animated SVG to graphically represent a pie chart
    """
    
    

    # From polar to cartesian coordinates
    def polar2cart(r, phi):
        arad = math.radians(-phi)
        x = r * math.cos(arad)
        y = r * math.sin(arad)
        return x,-y

    # From cartesian to polar coordinates: returns r, theta(degrees)`
    def cart2polar(x,y):
        return math.hypot(x,y), math.degrees(math.atan2(y,x))

    # Calculate text position: returns x,y
    def textPosition(angle, r):
        while angle > 360: angle -= 360
        while angle < 0: angle += 360
        return polar2cart(r, angle)

        
    if fillpercentage == FillPercentage.fill100:
        textdistance = 120
        width = 100.0
    elif fillpercentage == FillPercentage.fill75:
        textdistance = 125
        width = 75.0
    elif fillpercentage == FillPercentage.fill60:
        textdistance = 140
        width = 60.0
    elif fillpercentage == FillPercentage.fill50:
        textdistance = 150
        width = 50.0
    else:
        textdistance = 170
        width = 40.0

    svgdimension = 400
    
    # Centre and external radius of the circle
    cx = svgdimension/2
    cy = svgdimension/2
    externalradius = svgdimension/2
    
    # Internal Radius
    r = 200.0 - width
    stroke = width * 2.0 - 10.0
    
    
    
    # Percentages calculation
    tot = sum(values)
    perc = [100.0*x/tot for x in values]
        

    # Pre-processing of all labels
    if not labels is None:
        for i in range(len(labels)):
            labels[i] = labels[i].replace('-',' ').replace('_',' ')
    
    
    # Calculation of all coordinates and dimensioning: key is the index of the sector, from 0 to len(values)-1
    coordinates = {}

    startangle = -90.0
    for i in range(len(perc)):
        angle = 360.0 * perc[i] / 100.0

        # Sorry!
        if fillpercentage == FillPercentage.fill100:
            span  = 628.8 * perc[i] / 100.0
        elif fillpercentage == FillPercentage.fill75:
            span  = 790.0 * perc[i] / 100.0
        elif fillpercentage == FillPercentage.fill60:
            span  = 890.0 * perc[i] / 100.0
        elif fillpercentage == FillPercentage.fill50:
            span  = 945.0 * perc[i] / 100.0
        else:
            span  = 1010.0 * perc[i] / 100.0
                
        color = colors[i % len(colors)]
        color_no_answer = '#757575'

        strvalue = '{:.{prec}f}'.format(perc[i], prec=decimals)

        if not labels is None and i < len(labels):
            if displayvalues:
                text = '%s<br>%s%%<br>(%s)' % (labels[i],strvalue,values[i])
            else:
                text = '%s<br>%s%%' % (labels[i],strvalue)
                     
            
            if text[:9] == 'no answer' or text[:12] == 'no<br>answer': color = color_no_answer    # Request for same color for all the "no answer" slices
            #print(text)
        else:
            if displayvalues:
                text = strvalue + '<br>(' + str(values[i])+ ')'
            else:
                text = strvalue
        
        fulltext = centertext + ': ' + text.replace('<br>',' ')
        tooltip = '<title>%s</title>' % (fulltext)
            
        x,y = textPosition(startangle+angle/2.0, textdistance)

        svgtext = ''
        if perc[i] > 5.0:

            vtext = text.split('<br>')
            y -= fontsize * (len(vtext) - 1.0)

            svgtext = '<text id="text" class="portion-text" style="pointer-events: none" font-size="%f" text-anchor="middle" x="%f" y="%f" fill="%s" font-weight="%f" style="font-family: %s;">' % (fontsize, x+200,y+225, textcolor, textweight, fontsettings.font_name)

            for t in vtext:
                svgtext += '<tspan x="%f" dy="%f">%s</tspan>' % (x+200, fontsize, t)

            svgtext += '</text>'

                
        coordinates[i] = {
                          'startangle': startangle,
                          'angle'     : angle,
                          'span'      : span,
                          'color'     : color,
                          'text'      : text,
                          'tooltip'   : tooltip,
                          'x'         : x,
                          'y'         : y,
                          'svgtext'   : svgtext
                         }

        startangle += angle


    underline = ''
    if is_selected:
        class_name       = 'portion-out'
        underline        = 'text-decoration="underline"'
        centertextweight = 700
        #centercolor      = settings.color_first
    else:
        class_name = 'portion'
        
        
        
    # Creation of the SVG
    def createSVG():
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 %d %d" xml:space="preserve">' % (svgdimension,svgdimension)

        # CSS styling
        svg += '''
            <style type="text/css">
               @import url('%s');
               .portion:hover , .portion:hover + .portion-text {
                    cursor: pointer;
                    stroke-width: %f;
                    font-weight: %d;
                    text-decoration: underline;
                    }
            </style>
        ''' % (fontsettings.font_url, stroke*1.1, textweight+0)


        # Back circle
        strclass  = ''
        if is_selected:
            strclass = 'class="portion-out"'
        svg += '<circle %s fill="%s" cx="200" cy="200" r="200" />' % ( strclass, backcolor )
        
        if is_selected:
            svg += '<circle %s fill="%s" cx="200" cy="200" r="85" />' % ( strclass, settings.color_first )


        # Animated circles
        svgtextall = ''
            
        for i in range(len(perc)):
            angle      = coordinates[i]['angle']
            startangle = coordinates[i]['startangle']
            span       = coordinates[i]['span']

            color   = coordinates[i]['color']
            text    = coordinates[i]['text']
            tooltip = coordinates[i]['tooltip']

            x = coordinates[i]['x']
            y = coordinates[i]['y']

            # Text
            svgtext = coordinates[i]['svgtext']
            svgtextall += svgtext

            # Circle sector
            if duration <= 0.0:
                svg += '''
                        <circle class="%s" cx="%d" cy="%d" r="%f" transform="rotate(%f, 200, 200)" stroke-dasharray="%d, 1000" fill="none" stroke-width="%f" stroke="%s" stroke-linecap="butt">%s</circle>
                            %s
                ''' % (class_name, cx,cy, r, startangle, int(span), stroke, color, tooltip, svgtext)
            else:
                svg += '''
                        <circle class="%s" cx="%d" cy="%d" r="%f" transform="rotate(%f, 200, 200)" stroke-dasharray="0, 1000" fill="none" stroke-width="%f" stroke="%s" stroke-linecap="butt">
                            <animate attributeName="stroke-dasharray" dur="%fs" to="%d,1000" fill="freeze" />%s</circle>
                            %s
                ''' % (class_name, cx,cy, r, startangle, stroke, color, duration, int(span), tooltip, svgtext)

        # Center text
        svg += '<text style="pointer-events: none" font-size="%f" text-anchor="middle" x="200" y="%d" fill="%s" font-weight="%f" %s style="font-family: %s;">%s</text>' % (centerfontsize, 200+fontsize/4, centercolor, centertextweight, underline, fontsettings.font_name, centertext)
                

        # Display text again so that it is always visible!!!
        svg += svgtextall

        svg += '</svg>'
        return svg
    
    
    # Create an output widget and display SVG in it
    if isinstance(dimension, int):
        w = '%dpx' % dimension
    elif isinstance(dimension, float):
        w = '%fpx' % dimension
    else:
        w = str(dimension)
    out = widgets.Output(layout=Layout(width=w, height='calc(%s + 14px)' % w))

    
    svg = createSVG()
    with out:
        display(HTML(svg))
        
    # Add an event manager to the out Output widgets
    d = Event(source=out, watched_events=['click'])

    cx = svgdimension/2.0
    cy = svgdimension/2.0
    radius = svgdimension/2.0
    
    if fillpercentage == FillPercentage.fill100:
        rmin = 0.0
    elif fillpercentage == FillPercentage.fill75:
        rmin = radius * 0.25
    elif fillpercentage == FillPercentage.fill60:
        rmin = radius * 0.40
    elif fillpercentage == FillPercentage.fill50:
        rmin = radius * 0.50
    else:
        rmin = 1.0

    
    # Convert clik angle to startangle values
    def clickangle2startangle(a):
        # Convert in [0,360)
        if a < 0:
            a += 360.0
            
        # Invert direction
        sa = -a
        
        # Take inside interval [-90,270)
        if sa < -90.0:
            sa += 360.0
            
        return sa
        
        
    def handle_event(event):
            
        if is_selected:

            # Call callback function
            if not onclick is None:
                if not additional_argument is None:
                    onclick(-1, additional_argument)
                else:
                    onclick(-1)
                
            out.clear_output(wait=True)
            with out:
                display(HTML(createSVG()))

        else:
            x = event['relativeX']
            y = event['relativeY']
            w = event['boundingRectWidth']
            h = event['boundingRectHeight']
            xp = (x / w) * svgdimension
            yp = (y / h) * svgdimension
            px = xp - cx
            py = cy - yp
            
            #with out:
            #    print(x,y, xp,yp )
                
            clickdist,clickangle = cart2polar(px,py)
            if clickdist >= rmin and clickdist <= radius:
                sa = clickangle2startangle(clickangle)
                #with out:
                #    print(clickangle, sa)
                    
                for i in range(len(perc)):
                    angle      = coordinates[i]['angle']
                    startangle = coordinates[i]['startangle']
                
                    if sa >= startangle and sa <= startangle+angle:

                        # Call callback function
                        if not onclick is None:
                            if not additional_argument is None:
                                onclick(i, additional_argument)
                            else:
                                onclick(i)
                            
                        #out.clear_output(wait=True)
                        #with out:
                        #    display(HTML(createSVG()))
                            
                        break
       
    d.on_dom_event(handle_event)
    return out, svg




###########################################################################################################################################################################
# Title
###########################################################################################################################################################################
def svgTitle(title='Dashboard title', subtitle1='Subtitle1', subtitle2='Subtitle2', xline=290):
    """
    Creation of a simple title for a dashboard in SVG format
    
    Parameters
    ----------
    title : str, optional
        Title of the dashboard (default is 'Dashboard title')
    subtitle1 : str, optional
        First line of the subtitle (default is 'Subtitle1')
    subtitle2 : str, optional
        Second line of the subtitle (default is 'Subtitle2')
    xline : int, optional
        X position of a vertical line to divide title from subtitles (default is 290)
        
    Returns
    -------
        a string containing a SVG drawing that spans 100% of the width and 46 pixels in height
        
    Example
    -------
    Example of a title and logo SVG::
    
        from vois import svgUtils
        from ipywidgets import HTML, widgets, Layout

        outTitle = widgets.Output(layout=Layout(width='99%',                   height='64px'))
        outLogo  = widgets.Output(layout=Layout(width='1%', min_width='110px', height='82px'))

        outTitle.clear_output()
        with outTitle:
            display(HTML(svgUtils.svgTitle()))

        outLogo.clear_output()
        with outLogo:
            display(HTML(svgUtils.svgLogo()))

        display(widgets.HBox([outTitle,outLogo]))
        
    .. figure:: figures/svgTitle.png
       :scale: 100 %
       :alt: svgTitle example

       Example of a simple svgTitle and svgLogo
        
    Note
    ----
    This function is completely superseeded by the more complete examples of dashboard titles available using the :py:class:`title.title` or :py:class:`app.app`
    
    """
    svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="100%" height="46" xml:space="preserve">'

    LastData = datetime.today().strftime('%d %b %Y')

    svg += '<text x="0" y="36" font-size="40" fill="%s" font-weight="400">%s</text>' % (settings.label_textcolor,title)
    
    svg += '<line x1="%d" y1="0" x2="%d" y2="38" style="stroke:%s;stroke-width:1.0" />' % (xline, xline, settings.line_color)
    
    svg += '<text x="%d" y="20" font-size="18" fill="%s" font-weight="400">%s</text>' % (xline+15, settings.label_textcolor, subtitle1)
    svg += '<text x="%d" y="38" font-size="18" fill="%s" font-weight="400">%s</text>' % (xline+15, settings.label_textcolor, subtitle2)

    svg += '<text x="60%%" y="24" text-anchor="middle" font-size="26" fill="%s" font-weight="400">%s</text>' % (settings.label_textcolor, LastData)
    svg += '<text x="60%%" y="40" text-anchor="middle" font-size="12" fill="%s" font-weight="400">Last data update</text>' % (settings.label_textcolor)

    svg += '<line x1="0" y1="45" x2="100%%" y2="45" style="stroke:%s;stroke-width:0.3" />' % (settings.line_color)

    svg += '</svg>'
    return svg




###########################################################################################################################################################################
# Logo
###########################################################################################################################################################################
def svgLogo():
    """
    Creation of a simple SVG to display the logo of the European Commission
    
    Returns
    -------
        a string containing a SVG drawing that spans for 68 pixels in width and 44 pixels in height
        
    Example
    -------
    See example provided for the :py:func:`svgUtils.svgTitle` function

    Note
    ----
    This function is completely superseeded by the more complete examples of dashboard titles available using the :py:class:`title.title` or :py:class:`app.app`
    
    """
    svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="68px" height="44px" xml:space="preserve">'
    svg += '<image href="https://jeodpp.jrc.ec.europa.eu/services/shared/Notebooks/images/European_Commission.svg" x="0" y="1" width="68" height="44" />'
    svg += '</svg>'
    return svg

