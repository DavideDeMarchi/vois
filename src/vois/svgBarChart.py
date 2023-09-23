"""SVG BarChart to display interactive vertical bars."""
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

import statistics

try:
    from . import colors
    from .vuetify import fontsettings
except:
    import colors
    from vuetify import fontsettings

    
    
###########################################################################################################################################################################
# Display vertical bar chart allowing click event management on bars
# All horizontal measures are in vw units, all vertical measures are in vh units
###########################################################################################################################################################################
def svgBarChart(title='',
                width=30.0,
                height=40.0,
                names=[],
                values=[],
                stddevs=None,
                dictnames=None,
                selectedname=None,
                fontsize=1.1,
                titlecolor='black',
                barstrokecolor='black',
                xaxistextcolor='black',
                xaxistextsizemultiplier=1.0,
                xaxistextangle=0.0,
                xaxistextextraspace=0.0,
                yaxistextextraspace=5.0,
                xaxistextdisplacey=0.0,
                valuestextsizemultiplier=0.7,
                valuestextangle=0.0,
                strokew_axis=0.2,
                strokew_horizontal_lines=0.06,
                strokecol_axis="#bbbbbb",
                strokecol_horizontal_lines="#dddddd",
                showvalues=False,
                textweight=400,
                colorlist=['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)','rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)'], # Blues inverted
                colors_on_minmax_values=True,
                fixedcolors=False,
                enabledeselect=False,
                selectcolor='red',
                showselection=False,
                hovercolor='yellow',
                valuedigits=4,
                barpercentwidth=90.0,
                stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                minallowed_value=None,       # Minimum value allowed
                maxallowed_value=None,       # Maximum value allowed
                yaxis_min=None,              # Set to force y axis interval
                yaxis_max=None,
                on_change=None):             # Function to call when the selected name is changed
    """
    Creation of a vertical bar chart given a list of labels and corresponding numerical values. Click on the rectangles is managed by calling a custom python function.
    
    Parameters
    ----------
    title : str, optional
        Title of the chart (default is 'Ranking of labels')
    width : float, optional
        Width of the chart in vw units (default is 20.0)
    height : float, optional
        Height of the chart in vh units (default is 90.0)
    names : list of str, optional
        List of names to display inside the rectangles (default is [])
    values : list of float, optional
        List of numerical values of the same length of the names list (default is [])
    stddevs : list of float, optional
        List of numerical values representing the standard deviation of the values, to be displayed on top of the columns (default is None)
    dictnames : dict, optional
        Dictionary to convert codes to names when displaying the selection (default is None)
    selectedname : str, optional
        Name of the selected item (default is None)
    fontsize : float, optional
        Size of the standard font to use for names in vh coordinates (default is 1.1vh). The chart title will be displayed with sizes proportional to the fontsize parameter (up to two times for the chart title)
    titlecolor : str, optional
        Color to use for the chart title (default is 'black')
    barstrokecolor : str, optional
        Color for the bars border (default is 'black')
    xaxistextcolor: str, optional
        Color of labels on the X axis (default is 'black')
    xaxistextsizemultiplier: float, optional
        Multiplier factor to calculate the x axis label size from the default fontsize (default is 1.0)
    xaxistextangle : float, optional
        Angle in degree to rotate x axis labels (default is 0.0)
    xaxistextextraspace : float, optional
        Extra space to reserve to xaxis labels (default is 0.0)
    yaxistextextraspace : float, optional
        Extra space to reserve to yaxis labels in percentage (default is 5.0)
    xaxistextdisplacey : float, optional
        Positional displace in y coordinate to apply to the xaxis labels (default is 0.0)
    valuestextsizemultiplier : float, optional
        Multiplier factor to calculate the values text size from the default fontsize (default is 0.7)
    valuestextangle : float, optional
        Angle in degree to rotate the values text on top of the bars (default is 0.0)
    strokew_axis : float, optional
        Stroke width of the lines that define the x and y axis (default is 0.2)
    strokew_horizontal_lines : float, optional
        Stroke width of the secondary horizontal lines starting from the y axis (default is 0.06)
    strokecol_axis : str, optional
        Color to use for the lines of the x and y axis (default is "#bbbbbb")
    strokecol_horizontal_lines : str, optional
        Color to use for the secondary horizontal lines starting from the y axis (default is "#dddddd")
    showvalues: bool, optional
        If True the value of each bar is shown on top of the bar (default is False)
    textweight : int, optional
        Weight of the text written inside the rectangles (default is 400). The chart title will be displayed with weight equal to textweight+100
    colorlist : list of colors, optional
        List of colors to assign to the rectangles based on the numerical values (default is the inverted Plotly px.colors.sequential.Blues, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    fixedcolors : bool, optional
        If True, the list of colors is assigned to the values in their original order (and colorlist must contain the same number of elements!). Default is False
    colors_on_minmax_values: bool, optional
        If True, the colors are stretched on the min and max effective values, otherwise on the minallowed,maxallowed values range (default is True)
    enabledeselect : bool, optional
        If True, a click on a selected element deselects it, and the on_change function is called with None as argument (default is False)
    selectcolor : str, optional
        Color to use for the border of the selected rectangle (default is 'red')
    showselection : bool, optional
        If True, the currently selected bar is framed with the selection color (default is False)
    hovercolor : str, optional
        Color to use for the border on hovering the rectangles (default is 'yellow')
    valuedigits: int, optional
        Number of digits to use for the display of the values (default is 4)
    barpercentwidth: float, optional
        Percentage of element width occupied by the bar. The remaining percentage of the element width is the space before the next element. Default is 90.0.
    stdevnumber : float, optional
        The correspondance between the values and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    yaxis_min : float, optional
        Minimum value displayed on the y axis (default is None)
    yaxis_max : float, optional
        Maximum value displayed on the y axis (default is None)
    on_change: function, optional
        Python function to call when the selection of the rectangle items changes (default is None). The function is called with a tuple as unique argument. The tuple will contain (name, value, originalposition) of the selected rectangle
            
    Returns
    -------
        an instance of widgets.Output with the svg chart displayed in it

    Example
    -------
    Creation of a SVG chart to display a vertical bar chart::

        from IPython.display import display
        from ipywidgets import widgets
        import numpy as np
        import plotly.express as px
        from vois import eucountries as eu
        from vois import svgBarChart

        # Names of EU countries
        names  = [c.iso2code for c in eu.countries.EuropeanUnion()]

        # Randomly generated values for each country
        values = np.random.uniform(low=0.1, high=1.0, size=(len(names)))

        # Randomly generated stdevs for each country
        stddevs = np.random.uniform(low=0.01, high=0.2, size=(len(names)))

        debug = widgets.Output()
        display(debug)

        def on_change(arg):
            with debug:
                print(arg)

        out = svgBarChart.svgBarChart(title='Sample Bar Chart',
                                      names=names,
                                      values=values,
                                      stddevs=stddevs,
                                      width=39.0,
                                      height=35.0,
                                      fontsize=0.7,
                                      barstrokecolor='#44444400',
                                      xaxistextcolor='#666666',
                                      showvalues=True,
                                      colorlist=px.colors.sequential.Viridis,
                                      hovercolor='blue',
                                      stdevnumber=100.0,
                                      valuedigits=2,
                                      barpercentwidth=90.0,
                                      enabledeselect=True,
                                      showselection=False,
                                      minallowed_value=0.0,
                                      on_change=on_change)

        display(out)

    .. figure:: figures/barchart.png
       :scale: 100 %
       :alt: svgBarChart example

       Example of an interactive vertical bars chart
        
    """

    if len(names) == 0:
        return None
    
    if len(names) != len(values):
        print("Names and values lists have different number of elements!")
        return None
    
    if (not stddevs is None) and (len(names) != len(stddevs)):
        print("Names and standard deviations lists have different number of elements!")
        return None
    
    fontsize *= 3.0
    svgwidth = 100.0
    aspectratio = 0.5*height / width   # In landscape mode, usually the height is half the width dimension!!!
    svgheight = svgwidth * aspectratio
    
    titlefontsize = fontsize * 1.3

    hTitle = 1.4*titlefontsize

    name2color = {}
    if fixedcolors:
        name2color.update(zip(names,colorlist))
        
        
    numbers = range(0,len(names))
    ordered = list(zip(names,values,numbers))
    
    selected = -1
    if not selectedname is None:
        if selectedname in names:
            selected = names.index(selectedname)

    mean = statistics.mean(values)
    if len(names) <= 1:
        minvalue = mean
        maxvalue = mean
    else:
        stddev = statistics.stdev(values)
        valuemin = min(values)
        valuemax = max(values)

        minvalue = mean - stdevnumber*stddev
        maxvalue = mean + stdevnumber*stddev

        if minvalue < valuemin: minvalue = valuemin
        if maxvalue > valuemax: maxvalue = valuemax

    if not minallowed_value is None:
        minvalue = minallowed_value
    if not maxallowed_value is None:
        maxvalue = maxallowed_value

    if minvalue >= maxvalue: maxvalue = minvalue + 1
    
    if colors_on_minmax_values:
        ci = colors.colorInterpolator(colorlist,min(values),max(values))
    else:
        ci = colors.colorInterpolator(colorlist,minvalue,maxvalue)
    
    if (not yaxis_min is None) and (not yaxis_max is None):
        if yaxis_min < yaxis_max:
            minvalue = yaxis_min
            maxvalue = yaxis_max
   
    xstart = yaxistextextraspace
    xend   = 99.0
    xtext = xstart - 0.8                        # X right coordinate for Y axis texts
    x0 = xstart - 0.6                           # X corresponding to X axis origin
    x1 = xend   + 0.99
    y0 = svgheight - xaxistextextraspace - 0.7*hTitle + strokew_axis  # Y corresponding to Y axis origin
    y1 = 0.5*hTitle
    welem = (xend - xstart)/len(names)
    welemnet = (barpercentwidth/100.0)*welem
    
    f = "{:.%df}" % valuedigits
    
    # Convert a numerical value to an height in svg coordinates
    def value_to_height(value):
        return (svgheight - xaxistextextraspace - 1.7*hTitle) * (value - minvalue)/(maxvalue - minvalue)
    
    # Given a numerical value of one of the bar, returns the y svg coordinates of the rectangle
    def rect_ycoords(value):
        helem = value_to_height(value)
        y = svgheight - xaxistextextraspace - 0.7*hTitle - helem
        return y, helem
        
    #debug = widgets.Output()

    
    # Create the SVG drawing and returns a string
    def createSVG():
        preserve = 'xMidYMid meet'
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" viewBox="0 0 %f %f" preserveAspectRatio="%s" width="%fvw" height="%fvh">' % (svgwidth,svgheight, preserve, width,height)

        svg += '''
    <style type="text/css">
         @import url('%s');
         .barhover:hover {cursor: pointer; stroke-width: %f; stroke: %s; }
    </style>     
    ''' % (fontsettings.font_url, strokew_axis, hovercolor)
    
        ###svg += '<rect x="0.0" y="0.0" width="%f" height="%f" fill="none" stroke-width="0.2" stroke="red"></rect>' % (svgwidth,svgheight)
        
        # Title
        svg += '<text x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d">%s</text>' % (svgwidth/2.0, 2.2*titlefontsize/3.0, fontsettings.font_name, titlefontsize, titlecolor, textweight+100, title)

        # X axis
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,y0, x1,y0, strokew_axis, strokecol_axis)
        svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="end" font-family="%s" font-size="%f" fill="%s" font-weight="400">%s</text>' % (xtext, y0+fontsize*0.15, fontsettings.font_name, fontsize*0.65, xaxistextcolor, f.format(minvalue))
        
        # Y axis
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,y0, x0, y1, strokew_axis, strokecol_axis)
        
        # Horizontal lines
        ymax, helem = rect_ycoords(maxvalue)        
        dy = (y0 - ymax)/4.0
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,ymax, x1, ymax, strokew_horizontal_lines, strokecol_horizontal_lines)
        svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="end" font-family="%s" font-size="%f" fill="%s" font-weight="400">%s</text>' % (xtext, ymax+fontsize*0.25, fontsettings.font_name, fontsize*0.65, xaxistextcolor, f.format(maxvalue))
        
        y = ymax + dy
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,y, x1, y, strokew_horizontal_lines, strokecol_horizontal_lines)
        svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="end" font-family="%s" font-size="%f" fill="%s" font-weight="400">%s</text>' % (xtext, y+fontsize*0.25, fontsettings.font_name, fontsize*0.65, xaxistextcolor, f.format(0.75*(maxvalue-minvalue)))
        
        y = 0.5*(ymax + y0)
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,y, x1, y, strokew_horizontal_lines, strokecol_horizontal_lines)
        svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="end" font-family="%s" font-size="%f" fill="%s" font-weight="400">%s</text>' % (xtext, y+fontsize*0.25, fontsettings.font_name, fontsize*0.65, xaxistextcolor, f.format(0.5*(maxvalue-minvalue)))
        
        y = ymax + 3.0*dy
        svg += '<line x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x0,y, x1, y, strokew_horizontal_lines, strokecol_horizontal_lines)
        svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="end" font-family="%s" font-size="%f" fill="%s" font-weight="400">%s</text>' % (xtext, y+fontsize*0.25, fontsettings.font_name, fontsize*0.65, xaxistextcolor, f.format(0.25*(maxvalue-minvalue)))
       
    
        # Vertical bars
        x = xstart
        for name,value,pos in ordered:
                
            if fixedcolors:  col = name2color[name]
            else:            col = ci.GetColor(value)
                
            if showselection and pos==selected:
                strokew = strokew_axis
                stroke  = selectcolor
            else:
                strokew = strokew_axis*0.3
                stroke  = barstrokecolor

            y, helem = rect_ycoords(value)

            tooltip = f.format(value)
            if not stddevs is None:
                stddev = stddevs[pos]
                tooltip += ' ± %s'%f.format(stddev)

            xt = x+0.5*welemnet
            yt = svgheight + xaxistextdisplacey - xaxistextextraspace
            rotation = ''
            if xaxistextangle != 0.0:
                rotation = 'dominant-baseline="central" transform="rotate(%f, %f, %f)"'%(xaxistextangle,xt,yt)
                
            fullname = name
            if not dictnames is None and name in dictnames:
                fullname = dictnames[name]
                
            svg += '<rect class="barhover" x="%f" y="%f" width="%f" height="%f" fill="%s" stroke-width="%f" stroke="%s"><title>%s: %s</title></rect>' % (x, y, welemnet, helem, col, strokew, stroke, fullname, tooltip)
            
            svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d" %s>%s</text>' % (xt, yt, fontsettings.font_name, fontsize*xaxistextsizemultiplier,
                                                                                                                                                                      xaxistextcolor, textweight, rotation, name)
            
            if not stddevs is None:
                stddev = stddevs[pos]
                
                h = value_to_height(stddev)
                svg += '<line style="pointer-events: none" x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x+0.5*welemnet,y-h, x+0.5*welemnet, y+h, strokew_axis, strokecol_axis)    
                svg += '<line style="pointer-events: none" x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x+0.2*welemnet,y-h, x+0.8*welemnet, y-h, strokew_axis, strokecol_axis)    
                svg += '<line style="pointer-events: none" x1="%f" y1="%f" x2="%f" y2="%f" stroke-width="%f" stroke="%s"/>' % (x+0.2*welemnet,y+h, x+0.8*welemnet, y+h, strokew_axis, strokecol_axis)    
            
            if showvalues:
                xt = x+0.5*welemnet
                yt = y-0.1*fontsize
                rotation = ''
                if valuestextangle != 0.0:
                    rotation = 'dominant-baseline="central" transform="rotate(%f, %f, %f)"'%(valuestextangle,xt,yt)
                svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="500" %s>%s</text>' % (xt, yt, fontsettings.font_name, fontsize*valuestextsizemultiplier, xaxistextcolor, rotation, f.format(value))
                
            x += welem

        svg += '</svg>'
        return svg
    
    # Pixels to add to the output Widget in order to not see the scrollbars
    added_pixels_width  = 30
    added_pixels_height = 30
    
    # Create an output widget and display SVG in it
    out = widgets.Output(layout=Layout(width='calc(%fvw + %dpx)'%(width,added_pixels_width), height='calc(%fvh + %dpx)'%(height,added_pixels_height), margin='0px 0px 0px 0px')) #, border='1px dashed green'))

    svg = createSVG()
    with out:
        display(HTML(svg))

    # Add an event manager to the out Output widgets
    d = Event(source=out, watched_events=['click'])

    # Manage click event
    def handle_event(event):
        nonlocal selected
        
        # Given an event returns the x,y coordinates in [0,svgwidth] for x and [0,svgheight] for y
        def event_to_svg_coordinates(event):

            # Distance from the drawing to the border of the output widget (given the 30 pixels added!!!)
            dx_left   = 2.0
            dx_right  = 28.0
            dy_top    = 5.0
            dy_bottom = 27.0

            x = event['relativeX']
            y = event['relativeY']
            w = event['boundingRectWidth']
            h = event['boundingRectHeight']

            wnet = w - dx_left - dx_right
            hnet = h - dy_top  - dy_bottom

            # If the point is outside of the SVG rectangle
            if x < dx_left or x > dx_left+wnet or y < dy_top  or y > dy_top+hnet:
                return -1.0, -1.0

            xcorr = x - dx_left
            xp    = xcorr / wnet

            ycorr = y - dy_top
            yp    = ycorr / hnet

            return xp*svgwidth, yp*svgheight

            
        xsvg,ysvg = event_to_svg_coordinates(event)
       
        # Test on X coordinate
        if xsvg >= xstart and xsvg <= xend:
            pos = int((xsvg-xstart)//welem)
            
            xmin = xstart + pos*welem
            xmax = xmin + welemnet

            if xsvg >= xmin and xsvg <= xmax:    # Test on net width of the column
                
                value = values[pos]
                ymin, helem = rect_ycoords(value)
                ymax = ymin + helem
                
                if ysvg >= ymin and ysvg <= ymax:
                    elem = ordered[pos]
                    if enabledeselect:
                        if elem[2] == selected:
                            selected = -1
                        else:
                            selected = elem[2]
                    else:
                        selected = elem[2]
                            
                    out.clear_output(wait=True)
                    with out:
                        svg = createSVG()
                        display(HTML(svg))

                    if not on_change is None:
                        if selected < 0:
                            on_change(None)
                        else:
                            on_change(elem)   # Tuple containing (name, value, originalposition)

                    if not showselection:
                        selected = -1
                            
    d.on_dom_event(handle_event)

    return out #, debug