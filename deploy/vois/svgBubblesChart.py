"""SVG bubbles chart from a pandas DataFrame."""
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
from datetime import datetime
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY

from ipywidgets import HTML, widgets, Layout
from ipyevents import Event
from IPython.display import display

import plotly.express as px

try:
    from . import colors
    from .vuetify import fontsettings
except:
    import colors
    from vuetify import fontsettings


# Returns a list of strings (splitted at ' ')
def splitstring(s, maxlen):
    nrows = int( (len(s)+maxlen-1) / maxlen )
    s = s.replace('_',' ')
    s = s.replace('-',' ')
    words = s.split(' ')

    rows = ['']
    pos = 0
    for www in words:
        if len(rows[pos]) <= maxlen - len(www):
            if len(rows[pos]) == 0:  rows[pos] = www
            else:                    rows[pos] += ' ' + www
        else:
            rows.append(www)
            pos += 1
            
    return rows

                            
# Vertical text in an SVG where X coordinate are in percentage!!!
def verticalText(text, x, y, size, color, fontfamily, weight):
    return '''
<text x="%fvw" y="%fvh" font-size="%fvh" fill="%s" font-weight="%d" style="font-family: %s; pointer-events: none; transform: rotate(90deg); transform-origin: %fvw %fvh; transform-box: view-box; overflow: visible;">%s</text>
''' % (x, y, size, color, weight, fontfamily, x, y, text)


###########################################################################################################################################################################
# Bubbles chart visualization of 3 discrete variables + a size
###########################################################################################################################################################################
class svgBubblesChart:
    """
    Creation of a bubbles chart given an input DataFrame. It is a convenient chart for representing a numerical value that depends on 3 discrete variables. It displays a bi-dimensional grid where the unique values of the x column are displayed on the X axis, while the unique values of the y column are displayed on the Y axis. Inside each cell of the grid, a group of bubbles is displayed, one for each distinct value of the color column, while the size of the circles is proportional to the numerical value read from the size column. See the below example on a mushrooms dataset (taken from https://www.kaggle.com/datasets/uciml/mushroom-classification). The SVG chart has the x coordinates expressed in vw coordinates and the y coordinates expressed in vh coordinates. Cliks on the legend is managed so that individual color categories can be excluded from the chart.
    
    Parameters
    ----------
    df : pandas DataFrame
        Input DataFrame
    xcolumn : str
        Name of the DataFrame column containing the values to be displayed on the X axis
    ycolumn : str
        Name of the DataFrame column containing the values to be displayed on the X axis
    sizecolumn : str
        Name of the DataFrame column containing the numerical values to be used to size the bubbles
    colorcolumn : str
        Name of the DataFrame column containing the values to be used to give a color to the bubbles and to display the color legend
    width : float, optional
        Width of the chart in vw units (default is 100.0)
    height : float, optional
        Height of the chart in vh units (default is 50.0)
    xstart : float, optional
        X coordinate on vw units where the grid starts (default is 6.0). This value can be used to leave more or less space to the Y axis strings
    strokewidth : int, optional
        Width in pixels of the stroke to use for the bubbles (default is 1)
    strokecolor : str, optional
        Color of the stroke to use for the bubbles (default is '#ffffff')
    backcolor : str, optional
        Background color of the grid (default is '#aaaaaa')
    backlinecolor : str, optional
        Color of the lines defining the cells of the grid (default id '#888888')
    bubblecolors : list of colors, optional
        List of colors to use for the bubble. Each color is assigned to one of the unique values of the color column of the input DataFrame (default is px.colors.qualitative.Dark2)
    textcolor : str, optional
        Color to use for the texts, chart title, axis titles, axis values, etc. (default is 'black')
    textweight : int, optional
        Weight of the text (default is 400). The chart title, the axis titles and the legend title will be displayed with weight equal to textweight+100
    fontsize : float, optional
        Size of the standard font to use for values displayed in the X and Y axis in vh coordinates (default is 1.1vh). The chart title, the axis titles and the legend title will be displayed with sizes proportional to the fontsize parameter (up to two times for the chart title)
    xtextangle : float, optional
        Angle to use for the rotation of values displayed on the X axis (default is 0.0)
    title : str, optional
        Title of the chart (default is '')
    mode : str, optional
        Mode to use for the placement of bubbles inside the cells of the grid. Possible values are 'spread' (circles are horizontally displaced), 'concentric' (all circles have their centre in the  center of the cell) or 'tangent' (circles are all tangent on the center-bottom point of the cell). Default is 'spread'.
    legendrows : int, optional
         Number of rows to use for the legend (default is 2)
    legenditemwidth : int, optional
        Width in percent of the total width of each item of the legend (default is 10)
            
    Returns
    -------
        an instance of widgets.Output with the svg chart displayed in it

    Example
    -------
    Creation of a SVG bubble chart chart to display some of the columns of the mushroom dataset (see https://www.kaggle.com/datasets/uciml/mushroom-classification)::

        from IPython.display import display
        import pandas as pd
        import plotly.express as px
        colorlist = px.colors.qualitative.Dark2
        from vois import svgBubblesChart

        df = pd.read_csv('https://jeodpp.jrc.ec.europa.eu/services/shared/csv/mushrooms.csv')

        xcolumn     = 'cap-shape'
        ycolumn     = 'cap-surface'
        colorcolumn = 'habitat'
        sizecolumn  = 'count'
        dfgrouped = df.groupby([xcolumn, ycolumn, colorcolumn]).size().reset_index(name=sizecolumn)

        dfgrouped.columns = ['Shape', 'Cap surface', 'Mushroom habitat:', 'count']

        b = svgBubblesChart.svgBubblesChart(dfgrouped,
                                            height=50.0,
                                            xcolumn=dfgrouped.columns[0], 
                                            ycolumn=dfgrouped.columns[1],
                                            colorcolumn=dfgrouped.columns[2],
                                            sizecolumn=dfgrouped.columns[3], 
                                            strokewidth=1,
                                            strokecolor='#ffffff', 
                                            backcolor='#f0f0f0',
                                            backlinecolor='#000000',
                                            bubblecolors=colorlist,
                                            fontsize=1.1,
                                            title='Mushrooms analysis',
                                            mode='spread')
        display(b.draw())
        display(HTML(b.getlegendsvg()))
        
    .. figure:: figures/bubblechart.png
       :scale: 100 %
       :alt: svgBubblesChart example

       Example of an interactive bubbles chart in SVG
        
    """

    # Initialization: width in vw units, height in vhunits
    def __init__(self, df, xcolumn, ycolumn, sizecolumn, colorcolumn, width=100.0, height=50.0, xstart=6.0, 
                 strokewidth=1, strokecolor='#ffffff', backcolor='#aaaaaa', backlinecolor='#888888', 
                 bubblecolors=px.colors.qualitative.Dark2,
                 textcolor='black', textweight=400, fontsize=1.1, xtextangle=0.0, title='',
                 mode='spread',            # 'spread' or 'concentric' or 'tangent'
                 legendrows=2,             # Number of rows to use for the legend
                 legenditemwidth=10,       # Width in percent of each item of the legend
                ):
        
        self.df                = df
        self.xcolumn           = xcolumn
        self.ycolumn           = ycolumn
        self.sizecolumn        = sizecolumn
        self.colorcolumn       = colorcolumn
        if not self.colorcolumn is None and len(self.colorcolumn) <= 0: self.colorcolumn = None
        self.width             = width
        self.height            = height
        self.strokewidth       = strokewidth
        self.strokecolor       = strokecolor
        self.backcolor         = backcolor
        self.backlinecolor     = backlinecolor
        self.colorlist         = [colors.rgb2hex(colors.string2rgb(x)) for x in bubblecolors]   # Convert all colors to '#rrggbb' format !!!
        self.textcolor         = textcolor
        self.textweight        = textweight
        self.fontsize          = fontsize
        self.xtextangle        = xtextangle
        self.title             = title
        self.mode              = mode
        self.legendrows        = legendrows
        self.legenditemwidth   = legenditemwidth
        

        self.nrows   = self.df.shape[0]
        self.xvalues = sorted(list(self.df[self.xcolumn].unique()))
        self.yvalues = sorted(list(self.df[self.ycolumn].unique()))
        self.nx      = len(self.xvalues)
        self.ny      = len(self.yvalues)

        self.maxlenx = 20    # Max number of characters in xvalues: otherwise --> split
        self.maxleny = 12    # Max number of characters in yvalues: otherwise --> split
        
        if len(self.xvalues) > 15: self.maxlenx = 12
        nrows = 1
        for xvalue in self.xvalues:
            if len(xvalue) > self.maxlenx:
                rows = splitstring(xvalue,self.maxlenx)
                if len(rows) > nrows: nrows = len(rows)
        
        self.xvaluesindex = {}
        for x in self.xvalues: self.xvaluesindex[x] = self.xvalues.index(x)
        
        self.yvaluesindex = {}
        for y in self.yvalues: self.yvaluesindex[y] = self.yvalues.index(y)
            

        self.colorvalues = []
        self.ncolors = 0
        self.display = []
        if not self.colorcolumn is None:
            self.colorvalues = sorted(list(self.df[self.colorcolumn].unique()))
            self.ncolors     = len(self.colorvalues)
            self.display     = [True] * self.ncolors  # Flag to display or not a series

            
        self.legenditemheight  = 3.5
        self.titlefontsize     = self.fontsize*2
        #self.totalheight       = self.fontsize + self.height + (min(self.legendrows,self.ncolors) + 1)*self.legenditemheight + 1.4
            
        self.minvalue = 0.0
        if self.nrows > 0:
            self.maxvalue = float(self.df[self.sizecolumn].max())
        else:
            self.maxvalue = 0.0
            
            
        self.ystart   = 0.08 + self.fontsize*3                # In vh
        self.yend     = self.height - self.fontsize*2- (min(self.legendrows,self.ncolors) + 1)*self.legenditemheight
        
        self.xstart = xstart     # In vw
        self.xend   = self.width
        if self.nx > 0:
            self.xspace = (self.xend - self.xstart) / float(self.nx)
        else:
            self.xspace = 0.0
        
            
        if self.ny > 0:
            self.yspace = (self.yend - self.ystart) / float(self.ny)
        else:
            self.yspace = 0.0

        #self.rmax = min(self.xspace, self.yspace)
        self.rmax = self.yspace/2.0 - 0.1
        self.rmin = self.rmax/20.0
        
        # Create Output and Event
        self.out = widgets.Output(layout=Layout(width='calc(%fvw + 10px)'%self.width, height='calc(%fvh + 20px)'%self.height, margin='0px 0px 0px 0px'))  #, border='1px dashed green'))
        self.event = Event(source=self.out, watched_events=['click']) #, 'dblclick'])
        self.event.on_dom_event(self.handle_event)
        
        self.debug = widgets.Output()
        

    # Management of 'click' event on the SVG Output
    def handle_event(self, event):
        x = event['relativeX']
        y = event['relativeY']
        w = event['boundingRectWidth']
        h = event['boundingRectHeight']
        xp = self.width  * (x / w)
        yp = self.height * (y / h)
            
        # Click on a legend item
        if yp >= self.yend:

            for i in range(len(self.legendpos)):
                xitem = self.legendpos[i][0]
                yitem = self.legendpos[i][1]-1.5

                if yp >= yitem and yp <= yitem+self.legenditemheight and xp >= xitem and xp <= (xitem+1.5):
                    item = i
                    if item >= 0 and item < len(self.display):
                        if event['type'] == 'click':
                            self.display[item] = not self.display[item]
                        self.draw()
                    break
        
            
    # Return radius from a size value
    def getradius(self, size):
        if (self.maxvalue-self.minvalue) < 0.001: return self.rmax
        return self.rmin + (self.rmax - self.rmin) * (size - self.minvalue)/(self.maxvalue-self.minvalue)
    
    
    
    # Returns an SVG for the size legend
    def getlegendsvg(self):
        """
        Returns a string containing the SVG legend for the sizes of the circles.
        """
        titlefontsize = self.fontsize*1.4
        y = self.rmax + 2*titlefontsize
        fontsize = self.rmax/4.0
        
        sidetext = False
        if fontsize < 1.0:
            sidetext = True
            fontsize = 1.0
            w = self.yspace*1.3
        else:
            w = self.yspace
            
        h = w * 2.2
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0" y="0" width="%fvw" height="%fvh">' % (w,h)
        
        x = w/2.0
        svg += '<text text-anchor="middle" x="%fvw"  y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">Size legend:</text>' % (x-0.01, titlefontsize+0.6, titlefontsize,
                                                                                                                                                           self.textcolor, fontsettings.font_name, self.textweight+100)

            
        if sidetext:
            svg += '<text text-anchor="start" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x+self.rmax-0.3, y+fontsize/2-0.2, fontsize,
                                                                                                                                                    self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue))
        else:
            svg += '<text text-anchor="middle" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x-0.01,y+fontsize/2-0.2, fontsize, self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue))
        svg += '<circle cx="%fvw" cy="%fvh" r="%fvh" style="fill:none; stroke:black; stroke-width:1.5; opacity:1.0;"></circle>' % (x,y, self.rmax)
        
        if sidetext:
            y += self.rmax * 1.8
            svg += '<text text-anchor="start" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x+self.rmax-0.3,y+fontsize/2-0.2, fontsize, 
                                                                                                                                                   self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue/2.0))
        else:
            y += self.rmax * 1.65
            svg += '<text text-anchor="middle" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x-0.01,y+fontsize/2-0.2, fontsize,
                                                                                                                                                    self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue/2.0))
        svg += '<circle cx="%fvw" cy="%fvh" r="%fvh" style="fill:none; stroke:black; stroke-width:1.5; opacity:1.0;"></circle>' % (x,y, self.rmax/2.0)


        if sidetext:
            y += self.rmax * 1.0
            svg += '<text text-anchor="start" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x+self.rmax-0.3, y+fontsize/2-0.2, fontsize, 
                                                                                                                                                   self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue/4.0))
        else:
            y += self.rmax * 0.85
            svg += '<text text-anchor="middle" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%d</text>' % (x-0.01,y+fontsize/2-0.2, fontsize,
                                                                                                                                                    self.textcolor, fontsettings.font_name, self.textweight, int(self.maxvalue/4.0))
        svg += '<circle cx="%fvw" cy="%fvh" r="%fvh" style="fill:none; stroke:black; stroke-width:1.5; opacity:1.0;"></circle>' % (x,y, self.rmax/4.0)
        
        svg += '</svg>'
        return svg
    
    
    # Return the SVG code
    def getsvg(self):
        svg = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0vw" y="0vh" width="%fvw" height="%fvh">' % (self.width, self.height)
        
        svg += '''
                <style type="text/css">
                   @import url('%s');
                   .fullrow:hover { stroke: #000044; stroke-dasharray: 3.5,3.5; cursor: pointer; !important; }
                </style>
               ''' % (fontsettings.font_url)

        
        # Title text
        if len(self.title) > 0:
            svg += '<text text-anchor="middle" x="%fvw"  y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % ((self.xstart+self.xend)/2.0, self.fontsize*1.75, self.titlefontsize, 
                                                                                                                                                   self.textcolor, fontsettings.font_name, self.textweight+100, self.title)
        
        # Text for the axis
        svg += verticalText(self.ycolumn, 0.4, self.ystart, 1.75*self.fontsize, self.textcolor, fontsettings.font_name, self.textweight+100)
        svg += '<text text-anchor="end" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (self.xstart, (self.fontsize + self.yend + 0.3), 1.75*self.fontsize, 
                                                                                                                                                self.textcolor, fontsettings.font_name, self.textweight+100, self.xcolumn)

        
        # Background
        svg += '<rect x="%fvw" y="%fvh" width="%fvw" height="%fvh" fill="%s" fill-opacity="1.0"></rect>' % (self.xstart, self.ystart, self.xend-self.xstart, self.yend-self.ystart, self.backcolor)
        
                
        # Vertical back lines and xaxis texts
        x = self.xstart
        for xvalue in self.xvalues:
            svg += '<line style="pointer-events:none; stroke:%s; stroke-width:0.2" x1="%fvw" y1="%fvh" x2="%fvw" y2="%fvh"></line>' % (self.backlinecolor, x, self.ystart, x, self.yend)
            if self.xtextangle == 0.0:
                if len(xvalue) <= self.maxlenx:
                    svg += '<text text-anchor="middle" x="%fvw"  y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (x + 0.5*self.xspace, self.yend+self.fontsize+0.3, self.fontsize, 
                                                                                                                                                         self.textcolor, fontsettings.font_name, self.textweight, xvalue)
                else:
                    rows = splitstring(xvalue,self.maxlenx)
                    y = 0
                    for r in rows:
                        svg += '<text text-anchor="middle" x="%fvw"  y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (x + 0.5*self.xspace, self.yend+self.fontsize+3+y, self.fontsize, 
                                                                                                                                                             self.textcolor, fontsettings.font_name, self.textweight, r)
                        y += self.fontsize
                    
            else:
                svg += '''
                        <svg x="%fvw" y="%fvh" overflow="visible">
                            <text style="pointer-events: none" text-anchor="end" x="0vw"  y="0vh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d" transform="rotate(%f)">%s</text>
                        </svg>
                ''' % (x + 0.5*self.xspace, self.yend+self.fontsize+0.3, self.fontsize, self.textcolor, fontsettings.font_name, self.textweight, self.xtextangle, xvalue)
                
            x += self.xspace
        svg += '<line style="pointer-events:none; stroke:%s; stroke-width:0.2" x1="%fvw" y1="%fvh" x2="%fvw" y2="%fvh"></line>' % (self.backlinecolor, x, self.ystart, x, self.yend)
            
            
        # Horizontal back lines and y axis texts
        y = self.ystart
        for yvalue in self.yvalues:
            svg += '<line style="pointer-events:none; stroke:%s; stroke-width:0.2" x1="%fvw" y1="%fvh" x2="%fvw" y2="%fvh"></line>' % (self.backlinecolor, self.xstart, y, self.xend, y)
            if len(yvalue) <= self.maxleny:
                svg += '<text text-anchor="end" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (self.xstart*0.92, y + 0.5*self.yspace, self.fontsize, 
                                                                                                                                                      self.textcolor, fontsettings.font_name, self.textweight, yvalue)
            else:
                rows = splitstring(yvalue,self.maxleny)
                dy = -self.fontsize*(len(rows)/2 - 1)
                for r in rows:
                    svg += '<text text-anchor="end" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (self.xstart*0.92, y + 0.5*self.yspace+dy, self.fontsize, 
                                                                                                                                                         self.textcolor, fontsettings.font_name, self.textweight, r)
                    dy += self.fontsize
                        
            y += self.yspace
        svg += '<line style="pointer-events:none; stroke:%s; stroke-width:0.2" x1="%fvw" y1="%fvh" x2="%fvw" y2="%fvh"></line>' % (self.backlinecolor, self.xstart, y, self.xend, y)


        # Cycle on all combinations of (x,y) values to display circles
        for xvalue in self.xvalues:
            for yvalue in self.yvalues:

                df = self.df[(self.df[self.xcolumn]==xvalue) & (self.df[self.ycolumn]==yvalue)].sort_values(by=[self.sizecolumn], ascending=False)
                
                # Cycle on circles sorted by descending dimension
                if df.shape[0] > 0:
                    ix = self.xvaluesindex[xvalue]
                    iy = self.yvaluesindex[yvalue]
                    x = self.xstart + self.xspace*(ix + 0.5)
                    y = self.ystart + self.yspace*(iy + 0.5)
                
                    dx = 0
                    dxnext = self.xspace/min(max(3.0,df.shape[0]), 8.0)
                    maxsize = df.iloc[0]['count']
                    maxr = self.getradius(maxsize)
                    for index, row in df.iterrows():
                        size = row[self.sizecolumn]
                        color = self.colorlist[0]
                        tooltip = xvalue + '/' + yvalue + ': ' + str(int(size))
                        
                        if self.mode == 'spread':
                            opacity = 0.7
                        else:
                            opacity = 1.0
                        
                        dodisplay = True
                        if self.ncolors > 0:
                            colorvalue = row[self.colorcolumn]
                            if colorvalue in self.colorvalues:
                                icolor = self.colorvalues.index(colorvalue)
                                color = self.colorlist[icolor % len(self.colorlist)]
                                if self.display[icolor]:
                                    tooltip = xvalue + '/' + yvalue + '/' + colorvalue + ': ' + str(int(size))
                                else:
                                    dodisplay = False

                        if dodisplay:
                            r = self.getradius(size)
                            yc = y
                            if self.mode == 'tangent': yc = y+maxr-r
                            svg += '<circle class="fullrow" cx="%fvw" cy="%fvh" r="%fvh" style="fill:%s; stroke:%s; stroke-width:%f; opacity:%f;"><title>%s</title></circle>' % (x+dx,yc, r, color, self.strokecolor,self.strokewidth, opacity, tooltip)

                        if self.mode == 'spread':
                            if dx == 0:  dx -= dxnext
                            elif dx < 0: dx = -dx
                            else:
                                dx = -dx - dxnext
                                dxnext = dxnext / 2.0

        
        # Display the legend
        self.legendpos = []

        y = self.yend + self.legenditemheight*1.1
        x = self.xstart
       
        svg += '<text text-anchor="start" x="%fvw"  y="%fvh" font-size="%fvh" fill="%s" style="font-family: %s;" font-weight="%d">%s</text>' % (x, y+self.fontsize*1.56, self.fontsize*1.75, 
                                                                                                                                                self.textcolor, fontsettings.font_name, self.textweight+100, self.colorcolumn)
        y = self.yend + 2*self.legenditemheight
        dx = self.legenditemwidth
        if self.ncolors > 0:
            maxlen = len(max(self.colorvalues, key=len))
            dx = max(maxlen*0.75,dx)
       
        for i in range(self.ncolors):
            icolor = i % len(self.colorlist)
            color = self.colorlist[icolor]
            name = self.colorvalues[i]

            if self.display[i]: opacity = 1.0
            else:               opacity = 0.3333
            svg += '<rect class="fullrow" style="cursor: pointer;" width="1.35vw" height="%fvh" x="%fvw" y="%fvh" fill="%s" fill-opacity="%f"><title>%s</title></rect>' % (2.7*self.legenditemheight/5, x, y, color, opacity, name)
            svg += '<text text-anchor="start" x="%fvw" y="%fvh" font-size="%fvh" fill="%s" fill-opacity="%f" style="font-family: %s;" font-weight="%d">%s</text>' % (x+1.6, y+self.fontsize*1.5, self.fontsize*1.5, 
                                                                                                                                                                  self.textcolor, opacity, fontsettings.font_name, self.textweight, name)
            
            self.legendpos.append([x,y])
                                  
            y += self.legenditemheight
            if (i+1) % self.legendrows == 0:
                y = self.yend + 2*self.legenditemheight
                x += dx

            
        svg += '</svg>'
        return svg

    
    # Returns Output widget containing the line chart
    def draw(self):
        self.out.clear_output(wait=True)
        with self.out:
            self.svg_picture = self.getsvg()
            display(HTML(self.svg_picture))
            #display(self.debug)

        return self.out
    
    

