"""Input widget to select a date"""
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
from datetime import datetime

try:
    from . import settings
except:
    import settings


class datePicker():
    """
    Input widget to select a date.

    Parameters
    ----------
    date : str, optional
        Initial date selected on the input widget expressed in format 'YYYY-MM-DD' (default is None, corresponding to the today date)
    label : str, optional
        Label to be displayed inside the widget (default is '')
    dark : bool, optional
        If True, the popup date selection will have a dark background (default is settings.dark_mode)
    width : int, optional
        Width of the widget in pixels (default is 88)
    color : str, optional
        Color to use for the widget and the header of the popup window (default is settings.color_first)
    show_week : bool, optional
        If True the popup window will also show number of the week (default is False)
    onchange : function, optional
        Python function to call when the user selects a date. The function will receive no parameters. (default is None)
    offset_x : bool, optional
        If True the popup window will be opened on the right of the input field (default is False)
    offset_y : bool, optional
        If True the popup window will be opened on the bottom of the input field (default is True)
    disabled : bool, optional
        True if the selection of the date is disabled, False otherwise (default is False)
    mindate : str, optional
        Minimum selectable date (default is None)
    maxdate : str, optional
        Maximum selectable date (default is None)

    Example
    -------
    Creation of a date picker widget::
        
        from vois.vuetify import datePicker
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange():
            with output:
                print('Changed to', d.date)

        d = datePicker.datePicker(date=None, label='Start date', 
                                  offset_x=True, offset_y=False,
                                  onchange=onchange)

        display(d.draw())
        display(output)

    .. figure:: figures/datePicker.png
       :scale: 100 %
       :alt: datePicker widget

       Example of a datePicker
    """
    
    def __init__(self, date=None, label='', dark=settings.dark_mode, width=88, color=settings.color_first,
                       show_week=False, onchange=None, offset_x=False, offset_y=True,
                       disabled=False, mindate=None, maxdate=None):
        
        if date is None:
            self._date = datetime.today().strftime('%Y-%m-%d')
        else:
            self._date = date

        self.label      = label
        self.dark       = dark
        self.width      = width
        self.color      = color
        self.show_week  = show_week
        self.onchange   = onchange
        self.offset_x   = offset_x
        self.offset_y   = offset_y
        self._disabled  = disabled
        self.mindate    = mindate
        self.maxdate    = maxdate

        margins = "mb-n5"
        if len(self.label) == 0: margins = "mb-n5 mt-n2"
            
        
        if self._disabled: von = ''
        else:              von = 'menuData.on'
        self.tf = v.TextField(v_on=von, style_="max-width: %dpx; overflow: hidden;"%self.width, v_model=self._date,
                              type_="date", color=self.color, readonly=True, label=self.label, class_=margins)

        self.ctf = v.Card(flat=True, style_="max-width: %dpx; overflow: hidden;"%self.width, class_="pa-0 ma-0", children=[self.tf])

        self.p = v.DatePicker(v_model=self._date, flat=True, elevation=0, color=self.color, header_color=self.color,
                              style_="max-width: 290px;", show_week=self.show_week, dark=self.dark)
        
        if not self.mindate is None: self.p.min = self.mindate
        if not self.maxdate is None: self.p.max = self.maxdate
            
        self.p.on_event('input', self.__internal_onchange)

        self.m = v.Menu(offset_x=self.offset_x, offset_y=self.offset_y, open_on_hover=False, dense=True, close_on_click=True, close_on_content_click=False,
                        v_slots=[{'name': 'activator', 'variable': 'menuData', 'children': [self.ctf]}],
                        children=[self.p] )

        
    # Manage 'input' event
    def __internal_onchange(self, widget, event, data):
        self._date = data
        self.tf.v_model = data
        if self.onchange:
            self.onchange()
        
    # Returns the vuetify object to display (the v.Menu)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Menu)"""
        return self.m

    
    # date property
    @property
    def date(self):
        """
        Get/Set the selected date.
        
        Returns
        --------
        d : str
            date currently selected in the format 'YYYY-MM-DD'

        Example
        -------
        Programmatically change the date::
            
            picker.date = '2022-07-15'
            print(picker.date)
        
        """
        return self._date

    
    @date.setter
    def date(self, d):
        if isinstance(d, str) and len(d) == 10 and d[4] == '-' and d[7] == '-':
            self._date = d
            self.tf.v_model = self._date
            self.p.v_model  = self._date
            if self.onchange:
                self.onchange()
        else:
            self._date = None
            self.tf.v_model = self._date
            self.p.v_model  = self._date
            
            
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
        self.tf.v_on = von
