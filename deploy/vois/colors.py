"""Utility functions and classes to manage colors and color interpolation."""
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
import base64
import PIL
from PIL import Image, ImageDraw
from io import BytesIO
import math
import random
import numpy as np


# Returns True if the (r,g,b) color id dark
def isColorDark(rgb):
    """
    Returns True if the color (r,g,b) is dark

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]
       
    """
    [r,g,b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if hsp > 127.5:
        return False
    else:
        return True

# Returns the Multiply blend of two colors strings
def multiply(color1,color2):
    """
    Returns the Multiply blend of two colors strings
    """
    rgb1 = string2rgb(color1)
    rgb2 = string2rgb(color2)
    norm1 = [x/255.0 for x in rgb1]
    norm2 = [x/255.0 for x in rgb2]
    return rgb2hex(tuple([int(255.0*x[0]*x[1]) for x in zip(norm1,norm2)]))


# Returns the Darken blend of two colors strings
def darken(color1,color2):
    """
    Returns the Darken blend of two colors strings
    """
    rgb1 = string2rgb(color1)
    rgb2 = string2rgb(color2)
    return rgb2hex(tuple([min(x[0],x[1]) for x in zip(rgb1,rgb2)]))


# Return a random color in the '#rrggbb' format
def randomColor():
    """
    Returns a random color in the '#rrggbb' format
    """
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return rgb2hex((r,g,b))


# Utility: From (r,g,b) to '#rrggbb'
def rgb2hex(rgb):
    """
    Converts from a color represented as a (r,g,b) tuple to a hexadecimal string representation of the color '#rrggbb'

    Parameters
    ----------
    rgb : tuple of 3 int values
        Input color described by its RGB components as 3 integer values in the range [0,255]
        
    Returns
    -------
        A string containing the color represented as hexadecimals in the '#rrggbb' format
        
    Example
    -------
    Convert a color from (r,g,b) to '#rrggbb'::
    
        from vois import colors
        print( colors.rgb2hex( (255,0,0) ) )
        
    """
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


# Utility: From '#rrggbb' to (r,g,b)
def hex2rgb(color):
    """
    Converts from a hexadecimal string representation of the color '#rrggbb' to a (r,g,b) tuple

    Parameters
    ----------
    color : string
        A string containing the color represented as hexadecimals in the '#rrggbb' format
        
    Returns
    -------
        Tuple of 3 integers representing the RGB components in the range [0,255]
        
    Example
    -------
    Convert a color from '#rrggbb' to (r,g,b)::

        from vois import colors
        print( colors.hex2rgb( '#ff0000' ) )
        
    """
    if color[0] == '#':
        color = color[1:]
    rgb = (int(color[0:2],16), int(color[2:4],16), int(color[4:6],16))
    return rgb


# Utility: From 'rgb(a,b,c)' to (r,g,b)
def text2rgb(color):
    """
    Converts from string representation of the color 'rgb(r,g,b)' to a (r,g,b) tuple

    Parameters
    ----------
    color : string
        A string containing the color represented in the 'rgb(r,g,b)' format
        
    Returns
    -------
        Tuple of 3 integers representing the RGB components in the range [0,255]
        
    Example
    -------
    Convert a color from 'rgb(r,g,b)' to (r,g,b)::
    
        from vois import colors
        print( colors.text2rgb( 'rgb(255,0,0)' ) )
        
    """
    if color[0:4] == 'rgb(':
        rgb = color[4:].replace(')','').split(',')
        if len(rgb) >= 3:
            return ((int(rgb[0]),int(rgb[1]),int(rgb[2])))
           
    return (0,0,0)


# Utility: Convert a color string in '#rrggbb' or in 'rgb(...)' format into a tuple (r,g,b)
def string2rgb(s):
    """
    Converts from string representation of the color 'rgb(r,g,b)' or '#rrggbb' to a (r,g,b) tuple

    Parameters
    ----------
    color : string
        A string containing the color represented in the 'rgb(r,g,b)' format or in the '#rrggbb' format
        
    Returns
    -------
        Tuple of 3 integers representing the RGB components in the range [0,255]
    """
    if s[0] == '#':
        return hex2rgb(s)
    elif s[0:4] == 'rgb(':
        return text2rgb(s)
    return (0,0,0)



# colorInterpolator class
class colorInterpolator:
    """
    Class to perform color interpolation given a list of colors and a numerical range [minvalue,maxvalue]. The list of colors is considered as a linear range spanning from minvalue to maxvalue and the method :py:meth:`colors.colorInterpolator.GetColor` can be used to calculate any intermediate color by passing as input any numeric value.

    Parameters
    ----------
    colorlist : list of strings representing colors in 'rgb(r,g,b)' or '#rrggbb' format
        Input list of colors
    minvalue: float, optional
        Minimum value for the interpolation (default is 0.0)
    maxvalue: float, optional
        Maximum numerical value for the interpolation (default is 100.0)
        
    Examples
    --------
    Creation of a color interpolator from a list of custom colors::
    
        from vois import colors
        
        colorlist = ['rgb(247,251,255)',
                     'rgb(198,219,239)',
                     'rgb(107,174,214)', 
                     'rgb(33,113,181)',
                     'rgb(8,48,107)']
        c = colors.colorInterpolator(colorlist)
        print( c.GetColor(50.0) )
    
    Creation of a color interpolator using one of the Plotly library predefined colorscales (see `Plotly sequential color scales <https://plotly.com/python/builtin-colorscales/#builtin-sequential-color-scales>`_ and `Plotly qualitative color sequences <https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express>`_ )::
    
        import plotly.express as px
        from vois import colors
        
        c = colors.colorInterpolator(px.colors.sequential.Viridis, 0.0, 100.0)
        print( c.GetColor(33.3) )
               
               
    To visualize a color palette from a list of colors, the :py:func:`colors.paletteImage` function can be used::
    
        from vois import colors
        import plotly.express as px

        img = colors.paletteImage(px.colors.sequential.Blues, width=400, height=40)
        display(img)

    .. figure:: figures/paletteImage.png
       :scale: 100 %
       :alt: Plotly colorscale

       Display of a Plotly colorscale.
    """

    # Initialization
    def __init__(self, colorlist, minValue=0.0, maxValue=100.0):

        self.minValue = minValue
        self.maxValue = maxValue
        
        self.colors = [string2rgb(color) for color in colorlist]
        
                    
    # Return '#rrggbb' color linearly interpolated 
    def GetColor(self, value):
        """
        Returns a color in the '#rrggbb' format linearly interpolated in the [minvalue,maxvalue] range
        
        Parameters
        ----------
        value : float
            Numeric value for which the color has to be calculated
                
        Returns
        -------
        A string containing the color represented as hexadecimals in the '#rrggbb' format
            
        """
        if self.minValue >= self.maxValue:  # Avoid division by zero!
            return rgb2hex(self.palette[-1])
        
        if value < self.minValue: value = self.minValue
        if value > self.maxValue: value = self.maxValue
        
        n = len(self.colors)
        
        a = list(np.linspace(self.minValue, self.maxValue, n))
        i2 = next(x[0] for x in enumerate(a) if x[1] >= value)
        i1 = i2 - 1
        
        d1 = abs(value - a[i1])
        d2 = abs(a[i2] - value)
        d = d1 + d2
        w1 = 1.0 - d1/d
        w2 = 1.0 - w1
        
        c1 = self.colors[i1]
        c2 = self.colors[i2]

        r = int(c1[0]*w1 + c2[0]*w2)
        g = int(c1[1]*w1 + c2[1]*w2)
        b = int(c1[2]*w1 + c2[2]*w2)
       
        return rgb2hex((r,g,b))
        
        
    # Interpolate colors and returns a list of num_classes colors
    def GetColors(self, num_classes):
        """
        Returns a list of colors in the '#rrggbb' format covering all the input colors
        
        Parameters
        ----------
        num_classes : int
            Number of colors to interpolate
                
        Returns
        -------
        A list of strings containing the colors represented as hexadecimals in the '#rrggbb' format
        """
        if num_classes >= 2:
            return [self.GetColor(perc) for perc in np.linspace(self.minValue, self.maxValue, num_classes)]
        
        return self.colors
               
        
        
    # repr
    def __repr__(self):
        s = [str(x) for x in self.colors]
        return '-'.join(s)
        

# Utility: Given a list of colors, returns a PIL image displaying the palette
def paletteImage(colorlist, width=400, height=40, interpolate=True):
    """
    Given a list of colors, calculates and returns a PIL image displaying the color palette.
        
    Parameters
    ----------
    colorlist : list of strings representing colors in 'rgb(r,g,b)' or '#rrggbb' format
        Input list of colors
    width : int, optional
        Width in pixel of the image (default is 400)
    height : int, optional
        Height in pixel of the image (default is 40)
    interpolate : bool, optional
        If True the colors of the list are interpolated, if False, only the color in the list are displayed (default is True)
                
    Returns
    -------
    A PIL image displaying the color palette

    Examples
    --------
    Creation of a color palette image from a list of colors::
    
        from vois import colors
        import plotly.express as px

        img = colors.paletteImage(px.colors.sequential.Viridis, width=400, height=40)
        display(img)

    .. figure:: figures/plotlycolorscale.png
       :scale: 100 %
       :alt: Plotly colorscale

       Display of a Plotly colorscale.
    """
    img = Image.new('RGBA', (width,height), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    
    if interpolate:
        ci = colorInterpolator(colorlist,0,width-1.0)

        for x in range(width):
            d.line([x,0,x,height], fill=ci.GetColor(x), width=1)
    else:
        n = len(colorlist)
        wcolor = float(width)/float(n)
        x = 0.0
        for c in colorlist:
            d.rectangle([x,0.0,x+wcolor,height], fill=c)
            x += wcolor
        
    return img


# Utility: convert a PIL image into a string containing the image in base64
def image2Base64(img):
    """
    Given a PIL image, returns a string containing the image in base64 format
        
    Parameters
    ----------
    img : PIL image
        Input PIL image
                
    Returns
    -------
    A string containing the image in base64 format

    """
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return 'data:image/png;base64,' + img_str
    
    
