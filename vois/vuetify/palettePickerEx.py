"""Extended selection of a palette of different families (sequential, divergent, etc.)"""
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


# DOCUMENTATION ON MAPNIK:
# https://get-map.org/mapnik-lost-manual/book.pdf
# https://github.com/mapnik/mapnik-reference/blob/gh-pages/3.0.20/reference.json#L1517

from vois.vuetify import palettePicker, selectSingle, switch

import ipyvuetify as v
from ipywidgets import widgets
from IPython.display import display


# Utility: convert three integers to '#RRGGBB'
def RGB(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)
    
custompalettes = [
    { "name": "Simple", "colors": ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF']},
    
    { "name": "Dem",    "colors": [RGB(255,255,170), RGB( 39,168, 39), RGB( 11,128, 64), RGB(255,255,  0), RGB(255,186,  3),
                                   RGB(158, 30,  2), RGB(110, 40, 10), RGB(138, 94, 66), RGB(255,255,255)]},
    
    { "name": "NDVI",   "colors": [RGB(120,69,25), RGB(255,178,74), RGB(255,237,166), RGB(173,232,94),
                                   RGB(135,181,64), RGB(3,156,0), RGB(1,100,0), RGB(1,80,0)]}
]

families = ['carto', 'cmocean', 'cyclical', 'diverging', 'plotlyjs', 'qualitative', 'sequential', 'custom']



# Selection of a family and of a palette
class palettePickerEx():
    """
    Advanced selection of a palette of colors managing all the palette families and the interpolate flag
        
    Parameters
    ----------
    family : str, optional
        Family of the palette, one of these values: ['carto', 'cmocean', 'cyclical', 'diverging', 'plotlyjs', 'qualitative', 'sequential', 'custom'] (default is 'sequential')
    interpolate : bool, optional
        If True the colors are displayed as interpolated (default is True)
    width : int, optional
        Width of the widget in pixels (default is 400)
    onchange : function, optional
        Python function to call when the user selects one of the palettes. The function will as parameters the list of colors and the interpolate flag (default is None)

    Examples
    --------
    Creation of a selection widget for the palettes managing all the families::
        
        from vois.vuetify import palettePickerEx
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange(colors, interpolate):
            with output:
                print(colors, interpolate)

        p = palettePickerEx.palettePickerEx(onchange=onchange)

        display(p)
        display(output)

    .. figure:: figures/palettePickerEx.png
       :scale: 100 %
       :alt: palettePicker widget

       Example of an extended palette picker managing all the palette families and the interpolate flag
    """
    
    # Initialization
    def __init__(self, family='sequential', interpolate=True, onchange=None, width=400):
        self.family      = family
        self.interpolate = interpolate
        self.onchange    = onchange
        self.width       = width

        self.p = None
        self.sel = selectSingle.selectSingle('Family:', families, selection=family, width=200, onchange=self.onchangeFamily, marginy=1, clearable=False)
        self.sw  = switch.switch(self.interpolate, "Interpolate", onchange=self.onchangeInterpolate)

        self.p = palettePicker.palettePicker(family=self.family, custompalettes=custompalettes, label='Palette:', width=self.width, height=26, onchange=self.onchangePalette)
        self.p.value = 'Viridis'

        self.spacer = v.Html(tag='div',children=[' '], style_='width: 10px;')

    
    # Draw the widget
    def draw(self):
        r = widgets.HBox([self.sel.draw(), self.spacer, self.sw.draw()])
        return widgets.VBox([r, self.p.draw()])


    # Selection of a palette
    def onchangePalette(self):
        if not self.p is None:
            if not self.onchange is None:
                self.onchange(self.p.colors, self.interpolate)

    # Changed the family
    def onchangeFamily(self):
        self.family = self.sel.value
        if self.family == 'carto' or self.family == 'qualitative':
            self.interpolate = False
            self.sw.value = self.interpolate
        else:
            self.interpolate = True
            self.sw.value = self.interpolate
        self.p.updatePalettes(self.family,self.interpolate)
        self.p.value = self.p.images[0]['name']
        if not self.onchange is None:
            self.onchange(self.p.colors, self.interpolate)

    # Changed the interpolation flag
    def onchangeInterpolate(self, flag):
        self.interpolate = flag
        value = self.p.value
        oldonchange = self.onchange
        self.onchange = None
        self.p.updatePalettes(self.family,self.interpolate)
        self.onchange = oldonchange
        self.p.value = value
        if not self.onchange is None:
            self.onchange(self.p.colors, self.interpolate)
