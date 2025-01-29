"""Widget to select a float value"""
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
from IPython.display import display
from ipywidgets import widgets
import ipyvuetify as v

from vois.vuetify.utils.util import *

from vois.vuetify import settings, tooltip
from typing import Callable, Any, Union, Optional


#####################################################################################################################################################
# sliderFloat control
#####################################################################################################################################################
class SliderFloat(v.Row):
    """
    Compound widget to select a float value in a specific range.

    Parameters
    ----------
    value : float, optional
        Initial value of the slider (default is 1.0)
    min_value : float, optional
        Minimum value of the slider (default is 0.0)
    max_value : float, optional
        Maximum value of the slider (default is 1.0)
    text : str, optional
        Text to display on the left of the slider (default is 'Select')
    show_percentage : bool, optional
        If True, the widget will write the current value as a percentage inside the allowed range and will append the % sign to the right of the current value (default is True)
    decimals : int, optional
        Number of decimal digits to use in case show_percentage is False (default is 2)
    max_int : int, optional
        Maximum integer number for the underlining integer slider (defines the slider sensitivity). Default value is None, meaning it will be automatically calculated
    label_width : int, optional
        Width of the label part of the widgets in pixels (default is 0, meaning it is automatically calculated based on the provided label text)
    slider_width : int, optional
        Width in pixels of the slider component of the widget (default is 200)
    reset_button: bool, optional
        If True a reset button is displayed, allowing for resetting the widget to its initial value (default is False)
    show_tooltip: bool, optional
        If True the up and down buttons will have a tooltip (default is False)
    on_change : function, optional
        Python function to call when the changes the value of the slider. The function will receive a single parameter, containing the new value of the slider in the range from minvalue to maxvalue (default is None)
    color : str, optional
        Color of the widget (default is settings.color_first)
    editable : bool, optional
        If True the label can be edited by clicking on it (default is False)
    editable_width : int, optional
        If the slider is editable, set the width of the v.TextField widget to enter the value (default is 90)

    Example
    -------
    Creation and display of a slider widget to select an opacity value in the range [0.0, 1.0]::

        from vois.vuetify import sliderFloat
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_change(value):
            with output:
                print(value)

        o = SliderFloat(0.8, text='Fill opacity:', min_value=0.0, max_value=1.0, on_change=on_change)

        display(o)
        display(output)

    .. figure:: figures/sliderFloat.png
       :scale: 100 %
       :alt: opacity widget

       Example of a slider widget to select a floating point value.
   """

    deprecation_alias = dict(showpercentage='show_percentage', minvalue='min_value', maxvalue='max_value',
                             onchange='on_change', maxint='max_int', labelwidth='label_width',
                             sliderwidth='slider_width', resetbutton='reset_button', showtooltip='show_tooltip',
                             editableWidth='editable_width')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 value: Union[int, float] = 1.0,
                 min_value: Union[int, float] = 0.0,
                 max_value: Union[int, float] = 1.0,
                 text: str = 'Select',
                 show_percentage: bool = True,
                 decimals: int = 2,
                 max_int: Optional[int] = None,
                 label_width: int = 0,
                 slider_width: int = 200,
                 reset_button: bool = False,
                 show_tooltip: bool = False,
                 on_change: Optional[Callable[[float], None]] = None,
                 color: str = None,
                 editable: bool = False,
                 editable_width: int = 90,
                 **kwargs):

        super().__init__(**kwargs)

        from vois.vuetify import settings

        self.on_change = on_change

        self.editable = editable
        self.editable_width = editable_width

        self.min_value = min_value
        self.max_value = max_value
        self.show_percentage = show_percentage
        self.decimals = decimals

        self._color = color
        if self._color is None:
            self._color = settings.color_first

        if max_int is None:
            if self.decimals <= 1:
                self.max_int = 10
            elif self.decimals == 2:
                self.max_int = 100
            elif self.decimals == 3:
                self.max_int = 1000
            elif self.decimals == 4:
                self.max_int = 10000
            else:
                self.max_int = 100000
        else:
            self.max_int = max_int

        self.postchar = ''
        if self.show_percentage:
            self.postchar = '%'

        self.label_width = label_width
        self.slider_width = slider_width
        self.reset_button = reset_button

        self.int_initial_value = self.float2integer(value)

        # self.label  = label.label(text, textweight=400, margins=0, margintop=4, height=22)

        if self.label_width > 0:
            spx = '%dpx' % self.label_width
            style = 'width: %s; min-width: %s; max-width: %s;' % (spx, spx, spx)
        else:
            style = ''
        self.label = v.Html(tag='div', children=[text], class_='pa-0 ma-0 mt-4', style_=style)
        self.slider = v.Slider(v_model=self.int_initial_value,
                               dense=True, xsmall=True,
                               ticks=False, thumb_size=10, dark=settings.dark_mode,
                               color=self._color, track_color="grey",
                               class_="pa-0 ma-0 ml-5 mr-4 mt-3 mb-n1",
                               style_='max-width: %dpx; width: %dpx;' % (self.slider_width, self.slider_width),
                               min=0, max=self.max_int, vertical=False, height=32)
        self.slider.on_event('input', self.on_input)
        self.slider.on_event('change', self.on_slider_change)

        self.field_value = v.TextField(autofocus=True, hide_details=True, single_line=True, hide_spin_buttons=False,
                                       dense=True, outlined=True, color=settings.color_first, type="number",
                                       class_='pa-0 ma-0 mt-2')
        self.c_field_value = v.Card(flat=True, children=[self.field_value], width=self.editable_width,
                                    max_width=self.editable_width)
        self.field_value.on_event('change', self.on_change_field_value)
        self.field_value.on_event('blur', self.on_change_field_value)

        if self.show_percentage:
            self.label_value = v.Html(tag='div', children=[str(self.int_initial_value) + self.postchar],
                                      class_='pa-0 ma-0 mt-4')
        else:
            self.label_value = v.Html(tag='div',
                                      children=['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar],
                                      class_='pa-0 ma-0 mt-4')

        self.label_value.on_event('click', self.on_value_change)

        if self.reset_button:
            self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0',
                             children=[v.Icon(color='grey', children=['mdi-menu-right'])])
            self.bup.on_event('click', self.on_up)
            self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-4',
                              style_="overflow: hidden;")
            if show_tooltip:
                self.cup = tooltip.tooltip("Increase", self.cup)

            self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0',
                             children=[v.Icon(color='grey', children=['mdi-menu-left'])])
            self.bdn.on_event('click', self.on_dn)
            self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-4',
                              style_="overflow: hidden;")
            if show_tooltip:
                self.cdn = tooltip.tooltip("Decrease", self.cdn)

            self.bres = v.Btn(icon=True, x_small=True, rounded=False, elevation=0, width=15, height=15,
                              class_='pa-0 ma-0', children=[v.Icon(color='grey', children=['mdi-close'])])
            self.bres.on_event('click', self.on_reset)
            self.cres = v.Card(children=[self.bres], elevation=0, class_='pa-0 ma-0 mr-1 mt-4',
                               style_="overflow: hidden;")
            if show_tooltip:
                self.cres = tooltip.tooltip("Reset value", self.cres)

            self.buttons = widgets.HBox([self.cdn, self.cres, self.cup])
        else:
            self.bup = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0',
                             children=[v.Icon(color='grey', children=['mdi-menu-up'])])
            self.bup.on_event('click', self.on_up)
            self.cup = v.Card(children=[self.bup], elevation=0, class_='pa-0 ma-0 mr-1 mt-2',
                              style_="overflow: hidden;")
            if show_tooltip:
                self.cup = tooltip.tooltip("Increase", self.cup)

            self.bdn = v.Btn(icon=True, small=True, rounded=False, elevation=0, width=15, height=20, class_='pa-0 ma-0',
                             children=[v.Icon(color='grey', children=['mdi-menu-down'])])
            self.bdn.on_event('click', self.on_dn)
            self.cdn = v.Card(children=[self.bdn], elevation=0, class_='pa-0 ma-0 mr-1 mt-n1',
                              style_="overflow: hidden;")
            if show_tooltip:
                self.cdn = tooltip.tooltip("Decrease", self.cdn)

            self.buttons = widgets.VBox([self.cup, self.cdn])

        self.justify = 'start'
        self.class_ = 'pa-0 ma-0'
        self.no_gutters = True
        self.children = [self.label, self.slider, self.buttons, self.label_value]
        self.style_ = "overflow: hidden;"

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

        # When carriage return on the self.field_value or an external click

    def on_change_field_value(self, *args):
        self.row.children = [self.label, self.slider, self.buttons, self.label_value]
        self.value = float(self.field_value.v_model)
        self.field_value.v_model = self.value

    # On click on the self.labelvalue: display the self.field_value
    def on_value_change(self, *args):
        if self.editable and not self.slider.disabled:
            self.field_value.v_model = self.value
            self.row.children = [self.label, self.slider, self.buttons, self.c_field_value]

    # Input event on the slider
    def on_input(self, *args):
        if self.show_percentage:
            value = self.slider.v_model
            self.label_value.children = [str(value) + self.postchar]
        else:
            value = self.integer2float(self.slider.v_model)
            self.label_value.children = ['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar]

    # Input change on the slider
    def on_slider_change(self, *args):
        if self.show_percentage:
            value = self.slider.v_model
            self.label_value.children = [str(value) + self.postchar]
        else:
            value = self.integer2float(self.slider.v_model)
            self.label_value.children = ['{:.{prec}f}'.format(value, prec=self.decimals) + self.postchar]

        if not self.on_change is None:
            self.on_change(self.integer2float(self.slider.v_model))
        self.bup.disabled = self.slider.v_model >= self.max_int
        self.bdn.disabled = self.slider.v_model <= 0

    # Click on the up button
    def on_up(self, *args):
        if self.slider.v_model < self.max_int:
            self.slider.v_model = self.slider.v_model + 1
            self.on_slider_change()

    # Click on the down button
    def on_dn(self, *args):
        if self.slider.v_model > 0:
            self.slider.v_model = self.slider.v_model - 1
            self.on_slider_change()

    def on_reset(self, *args):
        self.slider.v_model = self.int_initial_value
        self.on_slider_change()

    # Conversion of float value [minvalue,maxvalue] to integer in [0,self.maxint]
    def float2integer(self, value):
        return int(self.max_int * (max(self.min_value, min(self.max_value, float(value))) - self.min_value) / (
                self.max_value - self.min_value))

    # Conversion of integer value [0,self.maxint] to float in [0.0,1.0]
    def integer2float(self, value):
        return ((self.max_value - self.min_value) * float(value)) / float(self.max_int) + self.min_value

    # Draw the widget
    def draw(self):
        """Returns the ipyvuetify object to display (a v.Row widget)"""
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self

    # Get the slider value
    @property
    def value(self):
        """
        Get/Set the slider value.

        Returns
        --------
        value : float
            Current value of the slider

        Example
        -------
        Programmatically set the slider value

            s.value = 0.56

        """
        return self.integer2float(self.slider.v_model)

    # Set the slider value
    @value.setter
    def value(self, new_value):
        if new_value < self.min_value:
            new_value = self.min_value
        if new_value > self.max_value:
            new_value = self.max_value

        int_value = self.float2integer(new_value)
        self.slider.v_model = int_value
        self.on_slider_change()

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
            self.slider.color = self._color
