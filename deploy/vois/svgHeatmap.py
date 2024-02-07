"""SVG heatmap chart from a pandas DataFrame."""
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
from textwrap import wrap
from ipywidgets import HTML, widgets, Layout
from ipyevents import Event

try:
    from . import colors
    from .vuetify import fontsettings
except:
    import colors
    from vuetify import fontsettings

    
    
# Utility function to word-wrap a long text
def wordwrap(x, maxcharperline=80):
    return '<br>'.join(['<br>'.join(wrap(block, width=maxcharperline)) for block in x.splitlines()])



# Vertical text in SVG
def verticalText(text, x, y, size, color, fontfamily, weight):
    return '''
<text x="0" y="0" font-size="%f" fill="%s" font-weight="%d" style="font-family: %s; pointer-events: none;" transform="translate(%f,%f) rotate(-90)">%s</text>
''' % (size, color, weight, fontfamily, x, y, text)


###########################################################################################################################################################################
# Generic heatmap chart from a pandas dataframe containing only numbers (rows names are taken from the index). Returns an Output widget
###########################################################################################################################################################################
def heatmapChart(df,
                 width=100.0,             # width in vw coordinates
                 height=50.0,             # height in vh coordinates
                 hTitle=5.0,              # height of the Title bar
                 wTitle=15.0,             # width of the left space for row titles
                 columnTitleMaxChar=40,   # Max number of chars for the column names (longer names are split)
                 textRows='Row',
                 textColumns='Column',
                 textValues='Value',
                 title='Heatmap',
                 fontsize=1.0,
                 colorlist=['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)', 'rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)'],
                 textcolor='black',
                 textweight=400,
                 backcolor= 'white',
                 highlitecolor='#426bb4',
                 highliteback='#dddddd',
                 minvalue=0.0,
                 maxvalue=1.0,
                 decimals=2):
    """
    Creation of a heatmap chart given an input DataFrame containing only numbers. The index strings and column names are taken as names for rows and columns. The SVG chart has x coordinates expressed in vw coordinates and the y coordinates expressed invh coordinates. Rows and columns of the chart can be selected and the chart will be sorted on decreasing values (when a column is selected, the rows are sorted, and viceversa)
    
    Parameters
    ----------
    df : pandas DataFrame
        Input DataFrame containing only numbers
    width : float, optional
        Width of the chart in vw units (default is 100.0)
    height : float, optional
        Height of the chart in vh units (default is 50.0)
    hTitle : float, optional
        Height of the Title bar in percentage on the height of the chart (default is 5.0)
    wTitle : float, optional
        Width of the left space for row titles in percentage of the width pf the chart (default is 15.0)
    columnTitleMaxChar : int, optional
        Max number of chars for the column names (longer names are splitted), (default is 40)
    textRows : str, optional
        Title for the rows (default is 'Row')
    textColumns : str, optional
        Title for the columns (default is 'Column')
    textValues : str, optional
        Text to label the values in the tooltip when the mouse is over a cell of the chart (default is 'Value')
    title : str, optional
        Title of the chart (default is 'Heatmap')
    fontsize : float, optional
        Size of the standard font to use for values displayed in the X and Y axis in vh coordinates (default is 1.0vh). The chart title and the axis titles will be displayed with sizes proportional to the fontsize parameter (up to two times for the chart title)
    colorlist : list of colors, optional
        List of colors to assign to the country polygons (default is the Plotly px.colors.sequential.Blues, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    textcolor : str, optional
        Color to use for rows and columns text (default is 'black')
    textweight : int, optional
        Weight of the text (default is 400). The chart title and the axis titles will be displayed with weight equal to textweight+100
    backcolor : str, optional
        Background color (default is 'white')
    highlitecolor : str, optional
        Color to use for displaying text of the selected row and colum (default is '#426bb4')
    highliteback : str, optional
        Color to use as background of the selected row and column (default is '#dddddd')
    minvalue : float, optional
        Minimum value of the DataFrame cells to be used for color assignment (default is 0.0)
    maxvalue : float, optional
        Minimum value of the DataFrame cells to be used for color assignment (default is 1.0)
    decimals : int, optional
        Number of decimals for the tooltip display of cell values (default is 2)
            
    Returns
    -------
        an instance of widgets.Output with the svg chart displayed in it

    Example
    -------
    Creation of a SVG heatmap chart to display a matrix of random numbers::

        from IPython.display import display
        import pandas as pd
        import numpy as np
        from vois import svgHeatmap
        
        df = pd.DataFrame(np.random.random((20,50)))
        display(svgHeatmap.heatmapChart(df, wTitle=7.0, hTitle=70)
        
    .. figure:: figures/heatmap.png
       :scale: 100 %
       :alt: svgHeatmap example

       Example of an interactive heatmap chart in SVG
        
    """
    
    # Dimension in SVG coordinates
    svgwidth = 100.0
    aspectratio = 0.5*height / width   # In landscape mode, usually the height is half the width dimension!!!
    svgheight = svgwidth * aspectratio

    if maxvalue <= minvalue: maxvalue = minvalue + 1.0
        
    # original df
    dfunsorted = df.copy()
    
    nrows = df.shape[0]
    hrow = (svgheight-hTitle)/nrows
    
    highlitecolumn = ''
    highliterow    = ''
    
    titlefontsize = fontsize*2
    
    #preserve = 'none'
    preserve = 'xMidYMid meet'
    
    # Calculates the SVG string
    def getSVG():
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" viewBox="0 0 %f %f" preserveAspectRatio="%s" width="%fvw" height="%fvh">' % (svgwidth,svgheight, preserve, width,height)

        svg += '''
        <style type="text/css">
           @import url('%s');
            .cell:hover { cursor: pointer; stroke: #000044; stroke-width:0.1; stroke-dasharray:0.15,0.15; !important; }
        </style>
        ''' % (fontsettings.font_url)

        # Names of row titles in the first column
        rowTitles = list(df.index)
        y = hTitle
        for r in rowTitles:

            tcolor     = textcolor
            tweight    = textweight
            bcolor     = backcolor
            if r == highliterow:
                tcolor  = highlitecolor
                tweight = textweight + 100
                bcolor = highliteback
            svg += '<rect fill="%s" width="%f" height="%f" x="0.01" y="%f"></rect>' % (bcolor, wTitle*0.995, hrow*0.95, y+0.2)
            svg += '<text style="pointer-events: none" text-anchor="end" x="%f" y="%f" font-size="%f" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (wTitle-0.1, y+hrow/2.0+0.5, fontsize, 
                                                                                                                                                                        tcolor, fontsettings.font_name, tweight, r)
            y += hrow
            

        # Calculate color interpolator
        ci = colors.colorInterpolator(colorlist, minvalue, maxvalue)

        # Cells
        y = hTitle-0.01
        wcolumn = (svgwidth-wTitle) / len(df.columns)
        w = 0.9 * wcolumn

        wmod = w
        if wmod > 3.0: wmod = 3.0

        svg += '<rect fill="%s" width="%f" height="%f" x="0.01" y="%f" ></rect>' % (backcolor, wTitle-0.02, hTitle-0.01, 0.01)

        # Column names
        textangle = -90.0   # -45.0
        x = wTitle
        y = hTitle-0.01
        for c in df.columns:

            c = str(c)
            tcolor  = textcolor
            tweight = textweight
            bcolor  = backcolor

            if c == str(highlitecolumn):
                tcolor  = highlitecolor
                tweight = textweight + 100
                bcolor  = highliteback

            svg += '<rect fill="%s" width="%f" height="%f" x="%f" y="%f" ><title>%s</title></rect>' % (bcolor,w*1.05, hTitle-2.4, x, 2.5, c)

            if len(c) <= columnTitleMaxChar:
                svg += verticalText(c, x+w/2+0.2, y, fontsize, tcolor, fontsettings.font_name, tweight)
            else:
                text = wordwrap(c,columnTitleMaxChar)
                lines = text.split('<br>')

                if len(lines) == 2:
                    dx = wmod/3.5
                    cx = x + w/2
                    xx = cx - dx/3 + 0.35
                else:
                    dx = wmod/3.5
                    cx = x + w/2
                    xx = cx - 2*dx/3 + 0.15
                    
                for r in lines:
                    svg += verticalText(r, xx, y, fontsize, tcolor, fontsettings.font_name, tweight)
                    xx += dx


            x += wcolumn

        # Cells
        y = hTitle-0.01
        for r in df.index:
            x = wTitle
            for c in df.columns:
                value = df.at[r, c]
                color = ci.GetColor(value)
                svg += '<rect stroke-width="0.0" style="fill:%s;"  x="%f" width="%f" height="%f" y="%f"></rect>' % (color, x, w*1.2, hrow*1.2, y+0.25)

                x += wcolumn

            y += hrow


        # Cell highlights
        y = hTitle-0.01
        for r in df.index:
            sr = str(r)
            ptext = wordwrap(sr)

            x = wTitle
            for c in df.columns:
                sc = str(c)
                value = df.at[r, c]
                color = ci.GetColor(value)
                svalue = '{:.{prec}f}'.format(value, prec=decimals)
                svg += '<rect class="cell" stroke-width="0.0" style="fill:#ffffff00;"  x="%f" width="%f" height="%f" y="%f"><title>%s: %s\n%s: %s\n%s = %s</title></rect>' \
                       % (x, w*1.1, hrow, y+0.25, textRows, ptext, textColumns, sc, textValues, svalue)

                x += wcolumn

            y += hrow

            
        # Title texts
        svg += '<text style="pointer-events: none" text-anchor="end"    x="%f" y="%f" font-size="%f" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (wTitle-0.2, hTitle-0.1, fontsize*1.75, textcolor,
                                                                                                                                                                       fontsettings.font_name, textweight+100, textRows)
        svg += '<text style="pointer-events: none" text-anchor="end"    x="%f" y="%f" font-size="%f" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (wTitle-0.2, hTitle/2+fontsize, fontsize*1.75, textcolor,
                                                                                                                                                                       fontsettings.font_name, textweight+100, textColumns)
        svg += '<text dominant-baseline="middle"   text-anchor="middle" x="%f" y="%f" font-size="%f" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (svgwidth/2.0, 1.2, fontsize*2.0, textcolor,
                                                                                                                                                                       fontsettings.font_name, textweight+100, title)


        # Highlight of the big rect
        svg += '<rect class="cell" fill="#ffffff00" width="%f" height="%f" x="0.01" y="%f" ><title>Click to deselect rows and columns</title></rect>' % (wTitle-0.02, hTitle-0.01, 0.01)
        
        # Highlights of row titles in the first column
        y = hTitle
        for r in rowTitles:
            svg += '<rect class="cell" fill="#ffffff00" width="%f" height="%f" x="0.01" y="%f"><title>%s</title></rect>' % (wTitle*0.995, hrow*0.95, y+0.2, r)
            y += hrow
            
            
        # Highlight column names
        x = wTitle
        y = hTitle-0.01
        for c in df.columns:
            c = str(c)
            svg += '<rect class="cell" fill="#ffffff00" width="%f" height="%f" x="%f" y="%f" ><title>%s</title></rect>' % (w*1.05, hTitle-2.4, x, 2.5, c)
            x += wcolumn
            
        
        svg += '</svg>'
        return svg

    
    
    # Update the chart
    def updateChart():
        output.clear_output(wait=True)
        with output:
            display(HTML(getSVG()))
        
    
    #debug = widgets.Output()
    
    
    # Pixels to add to the output Widget in order to not see the scrollbars
    added_pixels_width  = 20
    added_pixels_height = 20
    
    
    # Management of 'click' event on the HEATMAP Output
    def handle_event_heatmap(event):
        nonlocal df, highlitecolumn, highliterow
        
        x = event['relativeX'] - added_pixels_width/2 - 2
        y = event['relativeY']
        w = event['boundingRectWidth']  - added_pixels_width
        h = event['boundingRectHeight'] - added_pixels_height
        ar = float(h) / float(w)
        
        # Calculate dimension and bounding box of chart in pixels
        if ar > aspectratio:
            chartw = w
            charth = w * aspectratio
            xmin   = 0
            xmax   = chartw
            ymin   = (h - charth)/2
            ymax   = ymin + charth
        else:
            charth = h
            chartw = h / aspectratio
            xmin   = (w - chartw)/2
            xmax   = xmin + chartw
            ymin   = 0
            ymax   = charth


        # Calculate position in percentage on the chart area in pixels
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            xp = 100.0 * (x-xmin) / float(chartw)
            yp = 100.0 * (y-ymin) / float(charth) - 1.0

            wTitlePercent = 100.0*wTitle/svgwidth
            hTitlePercent = 100.0*hTitle/svgheight

            nrows = df.shape[0]
            ncols = df.shape[1]
            
            wcol = (100.0 - wTitlePercent)/ncols
            hrow = (100.0 - hTitlePercent)/nrows
            
            #debug.clear_output()
            #with debug:
                #print('chartw=',chartw, '    charth=',charth, '      aspectratio=',aspectratio, '     ar=',ar)
                #print('xmin=',xmin,'   ymin=',ymin, '    xmax=',xmax,'   ymax=',ymax)
                #print('wcol=',wcol, '    hrow=',hrow)
                #print('xp=',xp,'    yp=',yp,'    wTitlePercent=',wTitlePercent, '    hTitlePercent=',hTitlePercent)
        
                
            # Click on the reset column
            if xp >= 0 and xp <= wTitlePercent and yp >= 0.0 and yp <= hTitlePercent:
                #with debug:
                #    print("RESET!")
                df = dfunsorted.copy()
                highlitecolumn = ''
                highliterow    = ''
                updateChart()
                
            # Click on a column
            elif yp >= 2.4 and yp <= hTitlePercent:
                if yp >= 8.0 and xp >= wTitlePercent:
                    #with debug:
                    #    print("COL!", int((xp - wTitlePercent) / wcol))
                    icol = int((xp - wTitlePercent) / wcol)
                    if icol >= 0 and icol < ncols:
                        highlitecolumn = df.columns[icol]
                        df = df.sort_values(highlitecolumn, ascending=False)  # Sort rows by descending values in one column
                        updateChart()
                        
            # Click on a row
            elif yp > hTitlePercent:
                if xp >= 0.0 and xp <= wTitlePercent:
                    #with debug:
                    #    print("ROW!", int((yp - hTitlePercent) / hrow))
                    irow = int((yp - hTitlePercent) / hrow)
                    if irow >= 0 and irow < nrows:
                        highliterow = df.index[irow]
                        df = df.sort_values(highliterow, axis=1, ascending=False)  # Sort columns by descending values in one row
                        updateChart()
                
    
    # Create the output widget
    output = widgets.Output(layout=Layout(width= 'calc(%fvw + %dpx)' % (width,added_pixels_width), 
                                          height='calc(%fvh + %dpx)' % (height,added_pixels_height),
                                          margin='0px 0px 0px 0px')) #border='1px dashed green'))
    
    # Create the Event manager
    dh = Event(source=output, watched_events=['click'])
    dh.on_dom_event(handle_event_heatmap)

    updateChart()
        
    return output #, debug
