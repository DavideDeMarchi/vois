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
    

# Color wheel image
colorWheel = '''data:image/png;base64,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'''