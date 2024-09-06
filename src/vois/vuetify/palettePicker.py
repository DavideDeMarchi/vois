"""Selection of a palette of colors"""
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
import ipyvuetify as v
import inspect
import plotly.express as px
import base64
import PIL
from PIL import Image, ImageDraw
from io import BytesIO

try:
    from . import settings
    from . import selectImage
except:
    import settings
    import selectImage

    
    
#################################################################################################################
# Code repeated from colors.py
#################################################################################################################

# Utility: From (r,g,b) to '#RRGGBB'
def rgb2hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])


# Utility: From '#rrggbb' to (r,g,b)
def hex2rgb(color):
    if color[0] == '#':
        color = color[1:]
    rgb = (int(color[0:2],16), int(color[2:4],16), int(color[4:6],16))
    return rgb


# Utility: From 'rgb(a,b,c)' to (r,g,b)
def text2rgb(color):
    if color[0:4] == 'rgb(':
        rgb = color[4:].replace(')','').split(',')
        if len(rgb) >= 3:
            return ((int(rgb[0]),int(rgb[1]),int(rgb[2])))
           
    return (0,0,0)


# Utility: Convert a color string in '#rrggbb' or in 'rgb(...)' format into a tuple (r,g,b)
def string2rgb(s):
    if s[0] == '#':
        return hex2rgb(s)
    elif s[0:4] == 'rgb(':
        return text2rgb(s)
    return (0,0,0)



# colorInterpolator class
class colorInterpolator:

    # Initialization
    def __init__(self, colorlist, minValue=0.0, maxValue=100.0):

        self.minValue = minValue
        self.maxValue = maxValue
        
        self.colors = []
        for color in colorlist:
            self.colors.append(string2rgb(color))
        
        self.palette = []
        for i in range(len(self.colors)):
            if i == 0:
                self.palette.append(self.colors[i])
            else:
                c1 = self.colors[i-1]
                c2 = self.colors[i]
                
                for j in range(51):
                    w2 = float(j)/50.0
                    w1 = 1.0 - w2
                    r = int(c1[0]*w1 + c2[0]*w2)
                    g = int(c1[1]*w1 + c2[1]*w2)
                    b = int(c1[2]*w1 + c2[2]*w2)
                    self.palette.append((r,g,b))
                    
                    
    # Return '#rrggbb' color linearly interpolated 
    def GetColor(self, value):
        if value < self.minValue: value = self.minValue
        if value > self.maxValue: value = self.maxValue
        
        n = len(self.palette)
        
        v = (value - self.minValue) / (self.maxValue - self.minValue)
        idx = int(float((n-1)*v) + 0.5)

        if idx <  0: idx = 0
        if idx >= n: idx = n - 1
        
        if idx >= 0 and idx < len(self.palette):
            return rgb2hex(self.palette[idx])

        return '#FFFFFF'
        
                  
    # repr
    def __repr__(self):
        s = [str(x) for x in self.colors]
        return '-'.join(s)
        

# Utility: Given a list of colors, returns a PIL image displaying the palette
def paletteImage(colorlist, width=400, height=40, interpolate=True):
    img = Image.new('RGBA', (width,height), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    
    if interpolate:
        ci = colorInterpolator(colorlist,0,width-1.0)

        for x in range(width):
            d.line([x,0,x,height], fill=ci.GetColor(x), width=1)
    else:
        n = len(colorlist)
        if n > 0:
            wcolor = float(width)/float(n)
            x = 0.0
            for c in colorlist:
                d.rectangle([x,0.0,x+wcolor,height], fill=c)
                x += wcolor
        
    return img


# Utility: convert a PIL image into a string containing the image in base64
def image2Base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return 'data:image/png;base64,' + img_str
    
    


# Class palettePicker
class palettePicker():
    """
    Selection of a palette of colors.
        
    Parameters
    ----------
    family : str, optional
        Family of the palette, one of these values: ['carto', 'cmocean', 'cyclical', 'diverging', 'plotlyjs', 'qualitative', 'sequential', 'custom']. If family is 'custom' the user of the widget has to pass the list of palettes to display (default is 'sequential')
    custompalettes: list of dicts containing tags: "name" and "colors", optional
        Custom palette to be selected when the family is 'custom' (default is [])
    label : str, optional
        Label to display inside the selection widget (default is '')
    interpolate : bool, optional
        If True the colors are displayed as interpolated (default is True)
    width : int, optional
        Width of the widget in pixels (default is 400)
    height : int, optional
        Height of the widget in pixels (default is 34)
    clearable : Bool, optional
        If True the selection widget will show a -x- button to clear the selection (default is True)
    color : str, optional
        Color of the selection widget (default is settings.color_first)
    onchange : function, optional
        Python function to call when the user selects one of the palettes. The function will receive no parameters (default is None)

    Examples
    --------
    Creation of a simple selection widget for the palettes::
        
        from vois.vuetify import palettePicker
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange():
            with output:
                print('changed!')

        p = palettePicker.palettePicker(onchange=onchange)

        display(p.draw())
        display(output)

    .. figure:: figures/palettePicker.png
       :scale: 100 %
       :alt: palettePicker widget

       Example of a simple palette picker
       

    Creation of a complex selection widget for the palettes that manages all the palette families::

        from vois.vuetify import palettePicker, selectSingle, switch
        import ipyvuetify as v
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        # Utility: convert three integers to '#RRGGBB'
        def RGB(r,g,b):
            return '#{:02X}{:02X}{:02X}'.format(r, g, b)

        # Custom palettes
        custompalettes = [
            { "name": "Simple",
              "colors": ['#000000', '#FF0000', '#00FF00', '#0000FF',
                         '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF']},

            { "name": "Dem",
              "colors": [RGB(255,255,170), RGB( 39,168, 39),
                         RGB( 11,128, 64), RGB(255,255,  0),
                         RGB(255,186,  3), RGB(158, 30,  2),
                         RGB(110, 40, 10), RGB(138, 94, 66),
                         RGB(255,255,255)]},

            { "name": "NDVI",
              "colors": [RGB(120,69,25),   RGB(255,178,74),
                         RGB(255,237,166), RGB(173,232,94),
                         RGB(135,181,64),  RGB(3,156,0),
                         RGB(1,100,0),     RGB(1,80,0)]}
        ]

        families = ['carto', 'cmocean', 'cyclical', 'diverging',
                    'plotlyjs', 'qualitative', 'sequential', 'custom']
                    
        family      = 'sequential'
        interpolate = True

        p = None
        def onchangePalette():
            if not p is None:
                with output:
                    print("Palette changed to", p.value, p.colors)


        def onchangeFamily():
            global family, interpolate
            family = sel.value
            if family == 'carto' or family == 'qualitative':
                interpolate = False
                sw.value = interpolate
            else:
                interpolate = True
                sw.value = interpolate
            p.updatePalettes(family,interpolate)


        def onchangeInterpolate(flag):
            global interpolate
            interpolate = flag
            p.updatePalettes(family,interpolate)


        sel = selectSingle.selectSingle('Family:', families, selection=family,
                                        width=160, onchange=onchangeFamily,
                                        marginy=1, clearable=False)
        sw  = switch.switch(interpolate, "Interpolate",
                            onchange=onchangeInterpolate)

        p = palettePicker.palettePicker(family=family, custompalettes=custompalettes,
                                        label='Palette:', height=26, onchange=onchangePalette)

        spacer = v.Html(tag='div',children=[' '], style_='width: 10px;')

        display(widgets.HBox([sel.draw(), spacer, p.draw(), spacer, sw.draw()]))
        display(output)       
    
    .. figure:: figures/palettePicker2.png
       :scale: 100 %
       :alt: palettePicker full widget

       Example of a palette picker that also manages the palette families
    """
    
    def __init__(self, family='sequential', label='', interpolate=True, width=400, height=34,
                 custompalettes=[], clearable=True,
                 color=None, onchange=None):
        
        self.family         = family
        self.custompalettes = custompalettes
        self.label          = label
        self.interpolate    = interpolate
        self.width          = width
        self.height         = height
        self.clearable      = clearable
        self.onchange       = onchange
        self.index          = -1
        
        self._color = color
        if self._color is None:
            self._color = settings.color_first
        
        self.s = selectImage.selectImage(images=[], width="%dpx"%(self.width+165),
                                         max_width=self.width, max_height=self.height,
                                         color=self._color,
                                         label=self.label,
                                         outlined=True, margins="ma-0 mr-2",
                                         clearable=self.clearable,
                                         onchange=self.__internal_onchange)
        self.updatePalettes(self.family, self.interpolate)
        
        
    # Manage onchange on the selectImage widget
    def __internal_onchange(self):
        if self.index != self.s.value:
            self.index = self.s.value
            if self.onchange:
                self.onchange()

            
    # value property
    @property
    def value(self):
        """
        Get/Set name of the selected palette.
        
        Returns
        --------
        name : str
            Name of the currently selected palette

        Example
        -------
        Set and then get the current palette name::
            
            picker.value = 'Viridis'
            print(picker.value)
        
        """
        index = self.s.value
        if index >= 0 and index < len(self.images):
            return self.images[index]['name']
        else:
            return ''
        
    
    # Select one of the palette given its name
    @value.setter
    def value(self, name):
        for img in self.images:
            if img['name'] == name:
                self.s.value = img['index']
                return
        self.s.value = -1
                


    # colors property
    @property
    def colors(self):
        """
        Get the colors of the selected palette.
        
        Returns
        --------
        colorlist : list of strings in '#RRGGBB' format
            List of colors of the selected palette

        Example
        -------
        Get the selected palette colors::
            
            print(picker.colors)
        
        """
        index = self.s.value
        if index >= 0 and index < len(self.images):
            if self.family == 'custom':
                colors = self.custompalettes[index]['colors']
            else:
                colors = eval('px.colors.' + self.family + '.' + self.images[index]['name'])
            return [rgb2hex(text2rgb(x)) if x[0:4] == 'rgb(' else x for x in colors]
        else:
            return []
    
    
    @property
    def color(self):
        """
        Get/Set the widget color.
        
        Returns
        --------
        c : str
            widget color

        Example
        -------
        Programmatically change the widget color::
            
            s.color = '#00FF00'
            print(s.color)
        
        """
        return self._color
        
    @color.setter
    def color(self, c):
        if isinstance(c, str):
            self._color = c
            self.s.color = self._color
    
    
    # Update the palettes
    def updatePalettes(self, family='sequential', interpolate=True):
        """
        Update the displayed palette by changing family and/or interpolation flag

        Parameters
        ----------
        family : str, optional
            Family of the palette, one of these values: ['carto', 'cmocean', 'cyclical', 'diverging', 'plotlyjs', 'qualitative', 'sequential'] (default is 'sequential')
        interpolate : bool, optional
            If True the colors are displayed as interpolated (default is True)
            
        """
        
        self.family      = family
        self.interpolate = interpolate
        
        if self.family == 'custom':
            self.images = [{"name": x['name'],
                            "image": image2Base64(paletteImage(x['colors'], 
                                                               width=self.width, height=self.height,
                                                               interpolate=self.interpolate))} for x in self.custompalettes]
        else:
            colorscale_names = []
            colorscale_names.extend([self.family + '.' + name for name, body
                                     in inspect.getmembers(getattr(px.colors, self.family))
                                     if isinstance(body, list) and not '_r' in name and not name == '__all__'])

            self.images = [{"name": x.split('.')[-1],
                            "image": image2Base64(paletteImage(eval('px.colors.'+x), 
                                                               width=self.width, height=self.height,
                                                               interpolate=self.interpolate))} for x in colorscale_names]
        self.s.setImages(self.images)
        self.__internal_onchange()
        
        
    # Returns the vuetify object to display (the v.selectImage)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.selectImage)"""
        return self.s

