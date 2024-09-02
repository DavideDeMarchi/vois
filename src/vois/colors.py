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
from PIL import Image, ImageDraw
from io import BytesIO
import math
import random
import numpy as np
import colorsys


# Force a value into [valuemin, valuemax]
def Normalize(value,valuemin,valuemax):
    if value > valuemax:
        return valuemax
    elif value < valuemin:
        return valuemin
    return value


# Returns a tuple of the complementary color (opposite color in the color wheel)
def complementaryColor(rgb):
    """
    Given a tuple color (r,g,b) returns the complementary version of the input color (see: `Complementary color meaning <https://www.color-meanings.com/complementary-colors/>`_ and `Color wheel online <https://atmos.style/color-wheel>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        Tuple of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette of a random color followed by its complementary color::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        colcomp  = colors.rgb2hex(colors.complementaryColor(colors.string2rgb(col)))
        display(colors.paletteImage([col, colcomp], interpolate=False))
    
    """
    # Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

    # Change the Hue value to the Hue opposite
    HueValue = HLS[0] * 360
    HLS[0] = ((HueValue + 180) % 360)/360

    # Convert HLS (between 0 and 1) to RGB (base 256)
    return tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(HLS[0], HLS[1], HLS[2])))


# Returs a list of two colors as rgb tuples
def triadicColor(rgb):
    """
    Given a tuple color (r,g,b) returns a list of two split triadic colors (see: `Triadic colors meaning <https://www.color-meanings.com/triadic-colors/>`_ and `Color wheel online <https://atmos.style/color-wheel>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        List of two tuples of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette showing an input random color and the two triadic colors::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        display(colors.paletteImage([col] + [colors.rgb2hex(x) for x in colors.triadicColor(colors.string2rgb(col))], interpolate=False))
    
    """
    # Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

    # Find the first triadic Hue
    FirstTriadicHue = ((HLS[0] * 360 + 120) % 360) / 360

    # Find the second triadic Hue
    SecondTriadicHue = ((HLS[0] * 360 + 240) % 360) / 360

    ColorOutput1 = [FirstTriadicHue,  HLS[1], HLS[2]]
    ColorOutput2 = [SecondTriadicHue, HLS[1], HLS[2]]

    rgb1 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput1[0],ColorOutput1[1],ColorOutput1[2])))
    rgb2 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput2[0],ColorOutput2[1],ColorOutput2[2])))

    return [rgb1, rgb2]


# Returs a list of two colors as rgb tuples
def splitComplementaryColor(rgb):
    """
    Given a tuple color (r,g,b) returns a list of two split complementary colors (see: `Split complementary colors meaning <https://www.color-meanings.com/split-complementary-colors/>`_ and `Color wheel online <https://atmos.style/color-wheel>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        List of two tuples of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette showing an input random color and the two split complementary colors::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        display(colors.paletteImage([col] + [colors.rgb2hex(x) for x in colors.splitComplementaryColor(colors.string2rgb(col))], interpolate=False))
    
    """
    # Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

    # Find the first triadic Hue
    FirstSplitComplementaryHue = ((HLS[0] * 360 + 150) % 360) / 360

    # Find the second triadic Hue
    SecondSplitComplementaryHue = ((HLS[0] * 360 + 210) % 360) / 360

    ColorOutput1 = [FirstSplitComplementaryHue,  HLS[1], HLS[2]]
    ColorOutput2 = [SecondSplitComplementaryHue, HLS[1], HLS[2]]

    rgb1 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput1[0],ColorOutput1[1],ColorOutput1[2])))
    rgb2 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput2[0],ColorOutput2[1],ColorOutput2[2])))

    return [rgb1, rgb2]


# Returs a list of four colors as rgb tuples
def tetradicColor(rgb):
    """
    Given a tuple color (r,g,b) returns a list of four tetradic colors (see: `Tetradic colors meaning <https://www.color-meanings.com/rectangular-tetradic-color-schemes/>`_ and `Color wheel online <https://atmos.style/color-wheel>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        List of four tuples of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette showing an input random color and the three tetradic colors::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        display(colors.paletteImage([col] + [colors.rgb2hex(x) for x in colors.tetradicColor(colors.string2rgb(col))], interpolate=False))
    
    """
    # Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

    # Find the first tetradic Hue
    FirstTetradicHue  = ((HLS[0] * 360 +  30) % 360) / 360

    # Find the second tetradic Hue
    SecondTetradicHue = ((HLS[0] * 360 + 150) % 360) / 360

    # Find the third tetradic Hue
    ThirdTetradicHue  = ((HLS[0] * 360 + 210) % 360) / 360

    # Find the fourth tetradic Hue
    FourthTetradicHue = ((HLS[0] * 360 + 330) % 360) / 360
    
    ColorOutput1 = [FirstTetradicHue,  HLS[1], HLS[2]]
    ColorOutput2 = [SecondTetradicHue, HLS[1], HLS[2]]
    ColorOutput3 = [ThirdTetradicHue,  HLS[1], HLS[2]]
    ColorOutput4 = [FourthTetradicHue, HLS[1], HLS[2]]

    rgb1 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput1[0],ColorOutput1[1],ColorOutput1[2])))
    rgb2 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput2[0],ColorOutput2[1],ColorOutput2[2])))
    rgb3 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput3[0],ColorOutput3[1],ColorOutput3[2])))
    rgb4 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput4[0],ColorOutput4[1],ColorOutput4[2])))

    return [rgb1, rgb2, rgb3, rgb4]


# Returs a list of three colors as rgb tuples
def squareColor(rgb):
    """
    Given a tuple color (r,g,b) returns a list of three square colors (see: `Color wheel online <https://atmos.style/color-wheel>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        List of three tuples of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette showing an input random color and the three tetradic colors::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        display(colors.paletteImage([col] + [colors.rgb2hex(x) for x in colors.squareColor(colors.string2rgb(col))], interpolate=False))
    
    """
    # Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

    # Find the first tetradic Hue
    FirstTetradicHue  = ((HLS[0] * 360 +  90) % 360) / 360

    # Find the second tetradic Hue
    SecondTetradicHue = ((HLS[0] * 360 + 180) % 360) / 360

    # Find the third tetradic Hue
    ThirdTetradicHue  = ((HLS[0] * 360 + 270) % 360) / 360

    ColorOutput1 = [FirstTetradicHue,  HLS[1], HLS[2]]
    ColorOutput2 = [SecondTetradicHue, HLS[1], HLS[2]]
    ColorOutput3 = [ThirdTetradicHue,  HLS[1], HLS[2]]

    rgb1 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput1[0],ColorOutput1[1],ColorOutput1[2])))
    rgb2 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput2[0],ColorOutput2[1],ColorOutput2[2])))
    rgb3 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput3[0],ColorOutput3[1],ColorOutput3[2])))

    return [rgb1, rgb2, rgb3]


# Returs a list of two colors as rgb tuples
def analogousColor(rgb):
    """
    Given a tuple color (r,g,b) returns a list of two analogous colors (see: `Analogous colors meaning <https://www.color-meanings.com/analogous-colors/>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    Returns
    -------
        List of two tuples of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette showing an input random color and the two analogous colors::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        display(colors.paletteImage([col] + [colors.rgb2hex(x) for x in colors.analogousColor(colors.string2rgb(col))], interpolate=False))
    
    """
	# Convert RGB (base 256) to HLS (between 0 and 1 )
    HLS = list(colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255))

	# Find the first analogous Hue
    FirstAnalogousHue = ((HLS[0] * 360 + 30) % 360) / 360

    # Find the second analogous Hue
    SecondAnalogousHue = ((HLS[0] * 360 - 30) % 360) / 360

    ColorOutput1 = [FirstAnalogousHue,  HLS[1], HLS[2]]
    ColorOutput2 = [SecondAnalogousHue, HLS[1], HLS[2]]

    rgb1 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput1[0],ColorOutput1[1],ColorOutput1[2])))
    rgb2 = tuple(map(lambda x: round(x * 255), colorsys.hls_to_rgb(ColorOutput2[0],ColorOutput2[1],ColorOutput2[2])))

    return [rgb1, rgb2]


# Returs a tuple of darker (negative increment) or lighter color (positive increment)
def monochromaticColor(rgb, increment=0.20):
    """
    Given a tuple color (r,g,b) returns a darker (if increment is negative) or lighter (if increment is positive) version of the input color (see: `Monochromatic colors meaning <https://www.color-meanings.com/monochromatic-color-schemes/>`_)

    Parameters
    ----------
    rgb : tuple
        Tuple of 3 integers representing the RGB components in the range [0,255]

    increment : float, optional
        Increment/decrement in lightness in [-1.0, 1.0] (default is 0.2)

    Returns
    -------
        Tuple of 3 integers representing the output RGB components in the range [0,255]
        
    Example
    -------
    Display a palette of a random color followed by its darker and lighter version::
    
        from vois import colors
        from IPython.display import display
        
        col = colors.randomColor()
        coldarker  = colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(col), increment=-0.25))
        collighter = colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(col), increment=0.25))
        display(colors.paletteImage([col, coldarker, collighter], interpolate=False))
    
    """
	# Convert RGB (base 256) to HSV (between 0 and 1)
    HSV = list(colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255))
    return tuple(map(lambda x: Normalize(round(x * 255),0,255), colorsys.hsv_to_rgb(HSV[0], HSV[1]-increment, HSV[2]+increment)))


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
    
    
