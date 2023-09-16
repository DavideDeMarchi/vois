"""SVG RankChart to display vertically aligned rectangles."""
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
# Display labels ranked by numerical value and manage selection by click using ipyevents
# All horizontal measures are in vw units, all vertical measures are in vh units
###########################################################################################################################################################################
def svgRankChart(title='Ranking of labels',
                 width=20.0,
                 height=90.0,
                 names=[],
                 values=[],
                 splitnamelenght=40,
                 addposition=True,
                 fontsize=1.1,
                 titlecolor='black',
                 textweight=400,
                 colorlist=['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)','rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)'], # Blues inverted
                 fixedcolors=False,
                 enabledeselect=False,
                 selectfirstatstart=True,
                 selectcolor='red',
                 hovercolor='yellow',
                 stdevnumber=2.0,             # Number of stddev to calculate (minvalue,maxvalue) range
                 minallowed_value=None,       # Minimum value allowed
                 maxallowed_value=None,       # Maximum value allowed
                 on_change=None):             # Function to call when the selected name is changed
    """
    Creation of a chart given a list of labels and corresponding numerical values. The labels are ordered according to the decreasing values and displayed as a vertical list of rectangles. Click on the rectangles is managed by calling a custom python function.
    
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
    splitnamelenght : int, optional
        Maximum number of characters to display in a row. If the name length is higher, it is splitted in two rows (default is 40)
    addposition : bool, optional
        If True, the position is added in front of the name (starting from 1 and determined by the accompanying value). Default is True
    fontsize : float, optional
        Size of the standard font to use for names in vh coordinates (default is 1.1vh). The chart title will be displayed with sizes proportional to the fontsize parameter (up to two times for the chart title)
    titlecolor : str, optional
        Color to use for the chart title (default is 'black')
    textweight : int, optional
        Weight of the text written inside the rectangles (default is 400). The chart title will be displayed with weight equal to textweight+100
    colorlist : list of colors, optional
        List of colors to assign to the rectangles based on the numerical values (default is the inverted Plotly px.colors.sequential.Blues, see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )
    fixedcolors : bool, optional
        If True, the list of colors is assigned to the values in their original order (and colorlist must contain the same number of elements!). Default is False
    enabledeselect : bool, optional
        If True, a click on a selected element deselects it, and the on_change function is called with None as argument (default is False)
    selectfirstatstart : bool, optional
        If True, at start the rectangle corresponding to the greatest value is selected (default is True)
    selectcolor : str, optional
        Color to use for the border of the selected rectangle (default is 'red')
    hovercolor : str, optional
        Color to use for the border on hovering the rectangles (default is 'yellow')
    stdevnumber : float, optional
        The correspondance between the values and the colors list is done by calculating a range of values [min,max] to linearly map the values to the colors. This range is defined by calculating the mean and standard deviation of the values and applying this formula [mean - stdevnumber*stddev, mean + stdevnumber*stddev]. Default is 2.0
    minallowed_value : float, optional
        Minimum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    maxallowed_value : float, optional
        Maximum value allowed, to force the calculation of the [min,max] range to map the values to the colors
    on_change: function, optional
        Python function to call when the selection of the rectangle items changes (default is None). The function is called with a tuple as unique argument. The tuple will contain (name, value, originalposition) of the selected rectangle
            
    Returns
    -------
        an instance of widgets.Output with the svg chart displayed in it

    Example
    -------
    Creation of a SVG chart to display some names ordered by correspondent values::

        from IPython.display import display
        from ipywidgets import widgets
        from vois import svgRankChart
        import numpy as np
        import plotly.express as px

        # List of sentences
        names = ['European society needs to grasp the opportunities brought by the digital transformation', 
                 'A deep transformation such as the one facilitated by digital technologies',
                 'The progress needs to be evenly distributed across all regions',
                 'Over the next decade the EU economy and society need to undergo a profound transformation',
                 'The design of green and digital policy actions needs to consider socio-economic and territorial impacts',
                 'The EU supports the shift to a sustainable and resilient growth model',
                 'Address the challenges arising from the demographic transition',
                 'Geospatial data and methods are (usually) globally applicable',
                 'Considerable EU investments',
                 'The acceleration of the implementation of the Fit for 55 package',
                 'To become climate-neutral by 2050, Europe needs to decarbonise',
                 'Efforts need to be intensified in the harder-to-decarbonise sectors',
                 'The Commission recently decided to better understand the environment interface',
                 'One Health was already recognised by the Commission as an emerging priority',
                 'Achieving sustainability requires a holistic, well-coordinated approach',
                 'The conflict in Ukraine is endangering food security and has implications for food supply chains',
                 'The food system is composed of sub-systems and interacts with other key systems',
                 'The future of the EU and its position in the world will be influenced by population trajectories',
                 'Policymakers are often asked to react quickly to new circumstances',
                 'Obtaining economic benefit from natural resources whilst maintaining natural capital',
                 'We must be able to create EU policies that  decouple resource use from economic development',
                 'Robust, resilient and innovative EU economy is a necessary condition for ensuring the well-being'
                 ]

        # Randomly generated values for each sentence
        values = np.random.uniform(low=0.5, high=25.0, size=(len(names,)))

        debug = widgets.Output()
        display(debug)

        def on_change(arg):
            with debug:
                print(arg)

        out = svgRankChart.svgRankChart(names=names,
                                        values=values,
                                        width=20.0,
                                        height=90.0,
                                        splitnamelenght=45,
                                        addposition=False,
                                        fontsize=1.3,
                                        selectfirstatstart=False,
                                        colorlist=px.colors.sequential.Viridis,
                                        hovercolor='blue',
                                        on_change=on_change)
        display(out)
        
    .. figure:: figures/rankchart.png
       :scale: 100 %
       :alt: svgRankChart example

       Example of an interactive and ordered list of rectangles
        
    """

    if len(names) == 0:
        return None
    
    if len(names) != len(values):
        print("Names and values lists have different number of elements!")
        return None
    
    if fixedcolors and len(names) != len(colorlist):
        print("Names and colorlist lists have different number of elements!")
        return None
    
    
    # Returns 2 strings from 1
    def splitString(s):
        pos = len(s)//2
        spaces = [i for i, ltr in enumerate(s) if ltr == ' ']
        if len(spaces) > 0:
            bestpos = min(spaces, key=lambda x:abs(x-pos))
            s1 = s[:bestpos]
            s2 = s[bestpos+1:]
            return s1,s2
        return s,''
    
    fontsize *= 3.0
    svgwidth = 100.0
    aspectratio = 0.5*height / width   # In landscape mode, usually the height is half the width dimension!!!
    svgheight = svgwidth * aspectratio
    
    titlefontsize = fontsize * 1.75

    hTitle = 1.2*titlefontsize
    helem = (svgheight-hTitle)/len(names)
    x = 0.1
    y = hTitle

    name2color = {}
    if fixedcolors:
        name2color.update(zip(names,colorlist))
        
        
    numbers = range(1,len(names)+1)
    ordered = sorted(zip(names,values,numbers), key=lambda x: -x[1]) # Reverse order
    
    selected = -1
    if selectfirstatstart: 
        selected = ordered[0][2]

    #preserve = 'none'
    preserve = 'xMidYMid meet'
    
    def createSVG():
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" viewBox="0 0 %f %f" preserveAspectRatio="%s" width="%fvw" height="%fvh">' % (svgwidth,svgheight, preserve, width,height)

        svg += '''
    <style type="text/css">
         @import url('%s');
         .prio:hover {cursor: pointer; stroke-width: 1.0; stroke: %s; }
    </style>     
    ''' % (fontsettings.font_url,hovercolor)
    
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
            if minvalue < minallowed_value: minvalue = minallowed_value
        if not maxallowed_value is None:
            if maxvalue > maxallowed_value: maxvalue = maxallowed_value

        if minvalue >= maxvalue: maxvalue = minvalue + 1
        ci = colors.colorInterpolator(colorlist,minvalue,maxvalue)

        svg += '<text x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d">%s</text>' % (svgwidth/2.0, 2.2*titlefontsize/3.0, fontsettings.font_name, titlefontsize, titlecolor, textweight+100, title)
        x = 0.1
        y = hTitle

        i = 0
        for name,value,pos in ordered:
                
            if fixedcolors:
                col = name2color[name]
            else:
                col = ci.GetColor(value)
                
            if colors.isColorDark(colors.string2rgb(col)): textcol = 'white'
            else:                                          textcol = 'black'

            if pos==selected:
                strokew = 1.0
                stroke  = selectcolor
            else:
                strokew = 0.2
                stroke  = 'black'

            spos = ''
            if addposition: spos = str(pos) + '. '
                
            svg += '<rect class="prio" x="%f" y="%f" width="%f" height="%f" fill="%s" stroke-width="%f" stroke="%s"><title>%s%s: %d%%</title></rect>' % (x, y, svgwidth-0.2, helem-0.5, col, strokew, stroke, spos, name, int(value*100.0+0.5))
            if len(name) >= splitnamelenght:
                s1,s2 = splitString(name)
                svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d">%s%s</text>' % (svgwidth/2, y+fontsize, fontsettings.font_name, fontsize, textcol, textweight, spos, s1)
                svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d">%s</text>' % (svgwidth/2, y+2*fontsize, fontsettings.font_name, fontsize, textcol, textweight, s2)
            else:
                svg += '<text style="pointer-events: none" x="%f" y="%f" text-anchor="middle" font-family="%s" font-size="%f" fill="%s" font-weight="%d">%s%s</text>' % (svgwidth/2, y+1.5*fontsize, fontsettings.font_name, fontsize, textcol, textweight, spos, name)
            y += helem
            i += 1

        svg += '</svg>'
        return svg
    
    # Pixels to add to the output Widget in order to not see the scrollbars
    added_pixels_width  = 20
    added_pixels_height = 20
    
    # Create an output widget and display SVG in it
    out = widgets.Output(layout=Layout(width='calc(%fvw + %dpx)'%(width,added_pixels_width), height='calc(%fvh + %dpx)'%(height,added_pixels_height), margin='0px 0px 0px 0px')) #border='1px dashed green'))

    svg = createSVG()
    with out:
        display(HTML(svg))

    # Add an event manager to the out Output widgets
    d = Event(source=out, watched_events=['click'])

    #debug = widgets.Output()

    # Manage click event
    def handle_event(event):
        nonlocal selected
        x = event['relativeX']
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
        if y >= ymin and y <= ymax:
            yp = 100.0 * (y-ymin) / float(charth) - 1.0
            hTitlePercent = 100.0*hTitle/svgheight
            hrect = (100.0 - hTitlePercent)/float(len(names))
            #with debug:
            #    print(yp,hTitlePercent,hrect)
            
            if yp >= hTitlePercent*0.9:
                elem = ordered[int((yp-hTitlePercent)//hrect)]
                #with debug:
                #    print(yp, hTitlePercent, helem, elem)
        
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
    
    d.on_dom_event(handle_event)

    if selectfirstatstart and (not on_change is None):
        on_change(ordered[0])   # Tuple containing (name, value, originalposition)
    
    return out#, debug