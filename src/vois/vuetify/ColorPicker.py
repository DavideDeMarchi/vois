"""Input widget to select a color"""
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
from ipywidgets import widgets
from vois import colors
from vois.vuetify import popup
from vois.vuetify.utils.util import *
from typing import Callable, Any, Optional
import warnings


# Popup widget that, on hover, opens a card with complementary, triadic, analogous, etc. clickable colors
class colorTheoryPopup():

    # Initialisation
    def __init__(self, picker):
        
        self.picker = picker
        self._color = self.picker.color

        card_width  = 564
        card_height = 320

        self.card  = v.Card(flat=True, width=card_width, height=card_height, class_='pa-2 ma-0')
        self.popup = popup.popup(self.card, '', text=False, outlined=False, icon='mdi-palette', color='#333333', rounded=False,
                                 buttonwidth=30, buttonheight=self.picker.height+1, popupwidth=card_width, popupheight=card_height)
        self.updateCard()
        
    
    # Update the content of the card to be dispalyed when hover on the popup
    def updateCard(self):
        l_title = self.label('Color theory helpers:', width=300, weight=550)
        
        l_compl = self.label('Complementary colors:', width=160)
        c_col   = self.colorcard(self._color)
        c_compl = self.colorcard(colors.rgb2hex(colors.complementaryColor(colors.string2rgb(self._color))))

        l_tri = self.label('Triadic colors:', width=160)
        tri = [colors.rgb2hex(x) for x in colors.triadicColor(colors.string2rgb(self._color))]
        c_tri1 = self.colorcard(tri[0])
        c_tri2 = self.colorcard(tri[1])

        l_split = self.label('Split complementary col.:', width=160)
        split = [colors.rgb2hex(x) for x in colors.splitComplementaryColor(colors.string2rgb(self._color))]
        c_split1 = self.colorcard(split[0])
        c_split2 = self.colorcard(split[1])

        l_tet = self.label('Tetradic colors:', width=160)
        tet = [colors.rgb2hex(x) for x in colors.tetradicColor(colors.string2rgb(self._color))]
        c_tet1 = self.colorcard(tet[0])
        c_tet2 = self.colorcard(tet[1])
        c_tet3 = self.colorcard(tet[2])
        c_tet4 = self.colorcard(tet[3])

        l_squ = self.label('Square colors:', width=160)
        squ = [colors.rgb2hex(x) for x in colors.squareColor(colors.string2rgb(self._color))]
        c_squ1 = self.colorcard(squ[0])
        c_squ2 = self.colorcard(squ[1])
        c_squ3 = self.colorcard(squ[2])
        
        l_ana = self.label('Analogous colors:', width=160)
        ana = [colors.rgb2hex(x) for x in colors.analogousColor(colors.string2rgb(self._color))]
        c_ana1 = self.colorcard(ana[0])
        c_ana2 = self.colorcard(ana[1])

        l_mono = self.label('Monochromatic colors:', width=160)
        c_mono1 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment=-0.6)))
        c_mono2 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment=-0.4)))
        c_mono3 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment=-0.2)))
        c_mono4 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment= 0.2)))
        c_mono5 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment= 0.4)))
        c_mono6 = self.colorcard(colors.rgb2hex(colors.monochromaticColor(colors.string2rgb(self._color), increment= 0.6)))
        
        w1 = widgets.VBox([
                l_title,
                widgets.HBox([l_compl, c_col, c_compl]),
                widgets.HBox([l_tri,   c_col, c_tri1, c_tri2]),
                widgets.HBox([l_split, c_col, c_split1, c_split2]),
        ])
            
        self.card.children = [
            widgets.VBox([
                widgets.HBox([w1, v.Html(tag='div', style_='width: 84px;'), v.Img(src=colors.colorWheel, width=130, height=130)]),
                widgets.HBox([l_tet,   c_col, c_tet1, c_tet2, c_tet3, c_tet4]),
                widgets.HBox([l_squ,   c_col, c_squ1, c_squ2, c_squ3]),
                widgets.HBox([l_ana,   c_col, c_ana1, c_ana2]),
                widgets.HBox([l_mono,  c_mono1, c_mono2, c_mono3, c_col, c_mono4, c_mono5, c_mono6])
            ])
        ]
        

    # Returns the vuetify object to display
    def draw(self):
        return self.popup.draw()
        
        
    # color property
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        if isinstance(c, str):
            self._color = c
            self.updateCard()
        
        
    # disabled property
    @property
    def disabled(self):
        return self.popup.disabled
    
    @disabled.setter
    def disabled(self, flag):
        self.popup.disabled = flag
        
        
    # Creation of a label
    def label(self, text, class_='pa-0 ma-0 mr-3 mb-4', size=14, weight=400, color='#000000', width=None):
        lab = v.Html(tag='div', children=[text], class_=class_)
        if width is None: lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s; overflow: hidden;'%(size,weight,color)
        else:             lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s;  overflow: hidden; width: %dpx'%(size,weight,color,int(width))
        return lab

    
    # Create and returns a card displaying a color and clickable
    def colorcard(self, color, width=54, height=30):

        def onclick(*args):
            self.picker.color = color

        c = v.Card(flat=True, hover=True, color=color, width=width, min_width=width, max_width=width, height=height, tile=True)
        c.on_event('click',onclick)
        return c


    
class ColorPicker(v.Menu):
    """
    Input widget to select a color.

    Parameters
    ----------
    color : str, optional
        Initial color selected on the widget expressed in hexadecimal format '#RRGGBB' (default is '#FF0000')
    dark : bool, optional
        If True, the popup color selection will have a dark background (default is settings.dark_mode)
    dark_text : bool, optional
        If True, the text on the colored button is displayed in white, if False in black. If dark_text is None, the color of the text is automatically selected based on the currently selected color (default is None)
    width : int, optional
        Width of the widget in pixels (default is 40)
    height : int, optional
        Height of the widget in pixels (default is 30)
    rounded : bool, optional
        If True the color widget is displayed as a round button (default is False)
    canvas_height : int, optional
        Height of the canvas displayed on top of the popup window to select the colors (default is True)
    show_canvas : bool, optional
        If True the popup window will show the color canvas (default is True)
    show_mode_switch : bool, optional
        If True the popup window will show mode switch control among RGB, HSL and HAX (default is True)
    show_inputs : bool, optional
        If True the popup window will show the input field for the color components (default is True)
    show_swatches : bool, optional
        If True the popup window will show the color swatches (default is True)
    swatches_max_height : int, optional
        Height in pixels of the swatches area in the popup window (default is 164)
    text : str, optional
        Text to display in the color button (default is '')
    text_weight : int, optional
        Weight of the text to be shown in the button (default is 400, Bold is any value greater or equal to 500)
    on_change : function, optional
        Python function to call when the user selects a different color. The function will receive the argument parameter. If the argument is None, the function will receive no parameters. (default is None)
    argument : any, optional
        Argument to be passed to the onchange function (default is None)
    offset_x : bool, optional
        If True the popup window will be opened on the right of the color button (default is False)
    offset_y : bool, optional
        If True the popup window will be opened on the bottom of the color button (default is True)
    disabled : bool, optional
        True if the selection of the color is disabled, False otherwise (default is False)
    color_theory_popup : bool, optional
        If True a popup window (self.ctpopup) is created to show the complementary, analogous, etc.. colors on hover (default is False)

    Example
    -------
    Creation of a color picker widget to select a color::
        
        from vois.vuetify import ColorPicker
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_change():
            with output:
                print('Changed to', c.color)

        c = ColorPicker(color='#00AAFF',
                        width=30, height=30,
                        rounded=False,
                        on_change=on_change,
                        offset_x=True,
                        offset_y=False)

        display(c)
        display(output)

    .. figure:: figures/colorPicker.png
       :scale: 100 %
       :alt: colorPicker widget

       Example of a colorPicker to select a color
    """

    def hex2rgb(self, color):
        if color[0] == '#':
            color = color[1:]
        rgb = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
        return rgb

    def textDark(self, color):
        r, g, b = self.hex2rgb(color)
        if r + g + b <= 255 + 128:
            return True
        return False

    deprecation_alias = dict(textweight='text_weight', onchange='on_change')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 color: str = "#FF0000",
                 dark: bool = None,
                 dark_text: bool = None,
                 width: int = 40,
                 height: int = 30,
                 rounded: bool = False,
                 canvas_height: int = 100,
                 show_canvas: bool = True,
                 show_mode_switch: bool = True,
                 show_inputs: bool = True,
                 show_swatches: bool = True,
                 swatches_max_height: int = 164,
                 text: str = '',
                 text_weight: int = 400,
                 on_change: Optional[Callable[[], None]] = None,
                 argument: Optional[Any] = None,
                 offset_x: bool = False,
                 offset_y: bool = True,
                 disabled: bool = False,
                 color_theory_popup: bool = False):

        from vois.vuetify import settings

        self._color = str(color).upper()
        self.dark = dark if dark is not None else settings.dark_mode
        self._dark_text = dark_text
        self.width = width
        self.height = height
        self.rounded = rounded
        self.canvas_height = canvas_height
        self.show_canvas = show_canvas
        self.show_mode_switch = show_mode_switch
        self.show_inputs = show_inputs
        self.show_swatches = show_swatches
        self.swatches_max_height = swatches_max_height
        self.text = text
        self.text_weight = text_weight
        self.on_change = on_change
        self.argument = argument
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._disabled = disabled
        
        self.ctpopup = None
        if color_theory_popup:
            self.ctpopup = colorTheoryPopup(self)

        if self._disabled:
            von = ''
        else:
            von = 'menuData.on'
            
        if self._dark_text is None:
            darktext = self.textDark(self._color)
        else:
            darktext = self._dark_text
            
        self.button = v.Btn(v_on=von, depressed=True, large=False, dense=True, class_='pa-0 ma-0', color=self._color,
                            rounded=self.rounded, height=self.height, width=self.width, min_width=self.width, dark=darktext,
                            style_='font-weight: %d; text-transform: none' % self.text_weight, children=[self.text])

        self.p = v.ColorPicker(value=self._color, flat=True, class_="pa-0 ma-0", style_="min-width: 300px;",
                               canvas_height=self.canvas_height, show_swatches=self.show_swatches, dark=self.dark,
                               swatches_max_height=self.swatches_max_height, hide_canvas=not self.show_canvas,
                               hide_mode_switch=not self.show_mode_switch, hide_inputs=not self.show_inputs)
        self.p.on_event('input', self.__internal_onchange)

        super().__init__(offset_x=self.offset_x, offset_y=self.offset_y, open_on_hover=False, dense=True,
                         close_on_click=True, close_on_content_click=False,
                         v_slots=[{'name': 'activator', 'variable': 'menuData', 'children': self.button}],
                         children=[self.p])

        self.children = [self.p]

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Manage 'input' event
    def __internal_onchange(self, widget, event, data):
        if data.upper() != self._color.upper():
            self._color = data.upper()
            self.button.color = self._color
            if self.ctpopup is not None:
                self.ctpopup.color = self._color
            if self._dark_text is None:
                self.button.dark = self.textDark(self._color)
            if self.on_change:
                if self.argument is None:
                    self.on_change()
                else:
                    self.on_change(self.argument)

    # Returns the vuetify object to display (the v.Menu)
    def draw(self):
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self

    # color property
    @property
    def color(self):
        """
        Get/Set the selected color.
        
        Returns
        --------
        c : str
            color currently selected

        Example
        -------
        Programmatically change the color::
            
            picker.color = '#00FF00'
            print(picker.color)
        
        """
        return self._color

    @color.setter
    def color(self, c):
        if isinstance(c, str):
            self._color = c
            self.p.value = self._color
            self.button.color = self._color
            if self.ctpopup is not None:
                self.ctpopup.color = self._color
            if self._dark_text is None:
                self.button.dark = self.textDark(self._color)
            if self.on_change:
                if self.argument is None:
                    self.on_change()
                else:
                    self.on_change(self.argument)

    # disabled property
    @property
    def disabled(self):
        """
        Get/Set the disabled state of the widget.
        
        Returns
        --------
        flag : bool
            True if the widget is disabled, False otherwise

        Example
        -------
        Programmatically change the disabled state::
            
            picker.disabled = True
            print(picker.disabled)
        
        """
        return self._disabled

    @disabled.setter
    def disabled(self, flag):
        self._disabled = bool(flag)
        if self._disabled:
            von = ''
            self.button.children = ['⊗']   # Visual change to let the user know that the widget is disabled
        else:
            von = 'menuData.on'
            self.button.children = [self.text]
        self.button.v_on = von
        
        if self.ctpopup is not None:
            self.ctpopup.disabled = self._disabled

        
    # dark_text property
    @property
    def dark_text(self):
        """
        Get/Set the dark flag for the button that displayes the selected color. If True, the text on the colored button is displayed in white, if False in black. If dark_text is None, the color of the text is automatically selected based on the currently selected color
        
        Returns
        --------
        flag : bool
            If True, the text on the colored button is displayed in white, if False in black. If dark_text is None, the color of the text is automatically selected based on the currently selected color

        Example
        -------
        Programmatically change the dark_text property::
            
            picker.dark_text = True
            print(picker.dark_text)
        
        """
        return self._dark_text

    @dark_text.setter
    def dark_text(self, flag):
        self._dark_text = bool(flag)
        
        if self._dark_text is None:
            darktext = self.textDark(self._color)
        else:
            darktext = self._dark_text
        self.button.dark = darktext
        