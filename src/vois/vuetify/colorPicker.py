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

try:
    from . import settings
except:
    import settings


class colorPicker():
    """
    Input widget to select a color.

    Parameters
    ----------
    color : str, optional
        Initial color selected on the widget expressed in hexadecimal format '#RRGGBB' (default is '#FF0000')
    dark : bool, optional
        If True, the popup color selection will have a dark background (default is settings.dark_mode)
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
    textweight : int, optional
        Weight of the text to be shown in the button (default is 400, Bold is any value greater or equal to 500)
    onchange : function, optional
        Python function to call when the user selects a different color. The function will receive the argument parameter. If the argument is None, the function will receive no parameters. (default is None)
    argument : any, optional
        Argument to be passed to the onchange function (default is None)
    offset_x : bool, optional
        If True the popup window will be opened on the right of the color button (default is False)
    offset_y : bool, optional
        If True the popup window will be opened on the bottom of the color button (default is True)
    disabled : bool, optional
        True if the selection of the color is disabled, False otherwise (default is False)

    Example
    -------
    Creation of a color picker widget to select a color::
        
        from vois.vuetify import colorPicker
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange():
            with output:
                print('Changed to', c.color)

        c = colorPicker.colorPicker(color='#00AAFF',
                                    width=30, height=30,
                                    rounded=False, 
                                    onchange=onchange,
                                    offset_x=True,
                                    offset_y=False)

        display(c.draw())
        display(output)

    .. figure:: figures/colorPicker.png
       :scale: 100 %
       :alt: colorPicker widget

       Example of a colorPicker to select a color
    """
    
    def hex2rgb(self, color):
        if color[0] == '#':
            color = color[1:]
        rgb = (int(color[0:2],16), int(color[2:4],16), int(color[4:6],16))
        return rgb

    def textDark(self, color):
        r,g,b = self.hex2rgb(color)
        if r+g+b <= 255+128: return True
        return False
    
    
    def __init__(self, color="#FF0000", dark=settings.dark_mode, width=40, height=30, rounded=False, canvas_height=100,
                       show_canvas=True, show_mode_switch=True, show_inputs=True, show_swatches=True,
                       swatches_max_height=164, text='', textweight=400, onchange=None, argument=None,
                       offset_x=False, offset_y=True,
                       disabled=False):
        
        self._color = str(color).upper()
        self.dark = dark
        self.width   = width
        self.height  = height
        self.rounded = rounded
        self.canvas_height       = canvas_height
        self.show_canvas         = show_canvas
        self.show_mode_switch    = show_mode_switch
        self.show_inputs         = show_inputs
        self.show_swatches       = show_swatches
        self.swatches_max_height = swatches_max_height
        self.text       = text
        self.textweight = textweight
        self.onchange   = onchange
        self.argument   = argument
        self.offset_x   = offset_x
        self.offset_y   = offset_y
        self._disabled  = disabled

        if self._disabled: von = ''
        else:              von = 'menuData.on'
        self.button = v.Btn(v_on=von, depressed=True, large=False, dense=True, class_='pa-0 ma-0', color=self._color,
                            rounded=self.rounded, height=self.height, width=self.width, min_width=self.width, dark=self.textDark(self._color),
                            style_='font-weight: %d; text-transform: none' % self.textweight, children=[self.text])

        self.p = v.ColorPicker(value=self._color, flat=True, class_="pa-0 ma-0", style_="min-width: 300px;",
                               canvas_height=self.canvas_height, show_swatches=self.show_swatches, dark=self.dark,
                               swatches_max_height=self.swatches_max_height, hide_canvas=not self.show_canvas,
                               hide_mode_switch=not self.show_mode_switch, hide_inputs=not self.show_inputs)
        self.p.on_event('input', self.__internal_onchange)


        self.m = v.Menu(offset_x=self.offset_x, offset_y=self.offset_y, open_on_hover=False, dense=True, close_on_click=True, close_on_content_click=False,
                        v_slots=[{'name': 'activator', 'variable': 'menuData', 'children': self.button}],
                        children=[self.p])

        
    # Manage 'input' event
    def __internal_onchange(self, widget, event, data):
        if data.upper() != self._color.upper():
            self._color = data.upper()
            self.button.color = self._color
            self.button.dark  = self.textDark(self._color)
            if self.onchange:
                if self.argument is None:
                    self.onchange()
                else:
                    self.onchange(self.argument)
        
        
    # Returns the vuetify object to display (the v.Menu)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Menu)"""
        return self.m

    
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
            self.button.dark  = self.textDark(self._color)
            if self.onchange:
                if self.argument is None:
                    self.onchange()
                else:
                    self.onchange(self.argument)

                
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
        Programmatically change the date::
            
            picker.disabled = True
            print(picker.disabled)
        
        """
        return self._disabled

    
    @disabled.setter
    def disabled(self, flag):
        self._disabled = bool(flag)
        if self._disabled: von = ''
        else:              von = 'menuData.on'
        self.button.v_on = von
                