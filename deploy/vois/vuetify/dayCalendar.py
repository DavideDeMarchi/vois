"""Calendar widget showing days with events"""
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
from ipywidgets import widgets, Layout

import collections
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

try:
    from . import settings
except:
    import settings

    
    
# Given two dates as strings in YYY-MM-DD format, returns the number of weeks of covering the period between start and end day
def number_of_weeks(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date   = datetime.strptime(end,   '%Y-%m-%d').date()
    start_monday = start_date + timedelta(days=-start_date.weekday())
    end_monday   = end_date   + timedelta(days=-end_date.weekday())
    delta = end_monday - start_monday
    return 1 + delta.days // 7

#####################################################################################################################################################
# Calendar that displays days inside an interval of dates and optional events
#####################################################################################################################################################
class dayCalendar():
    """
    Input widget to display a daily calendar for a range of dates and allows for highlighting some of the days and manages the click on the days.

    Parameters
    ----------
    start : str or datetime or date instance, optional
        Initial date of the calendar as a string in format 'YYYY-MM-DD' or as an instance of datetime.datetime or datetime.date (default is today date minus one month)
    end : str or datetime or date instance, optional
        Final date of the calendar as a string in format 'YYYY-MM-DD' or as an instance of datetime.datetime or datetime.date  (default is today)
    color : str, optional
        Color to use for the highlighting of days in the calendar (default is settings.color_first)
    dark : bool, optional
        If True, the calendar will have a dark background (default is settings.dark_mode)
    days: list of str, optional
        List of days to be highlighted as strings in "YYYY-MM-DD" format (default is []). The list can contain repeated days (see show_count below).
    show_count: bool, optional
        If True, the event bar will show the number of events on each of the highlighted days (default is False)
    width : int, optional
        Width of the widget in pixels (default is 340)
    height : int, optional
        Height of the widget in pixels (default is None). If None is passed, the height will be calculated depending on the range of dates defined by start and end parameters.
    on_click : function, optional
        Python function to call when the user clicks on one day of the calendar. The function will receive as parameter a string in "YYYY-MM-DD" format. (default is None)
    on_click _event: function, optional
        Python function to call when the user clicks on the highlighting bar of one day of the calendar. The function will receive as parameter a string in "YYYY-MM-DD" format. (default is None)

    Example
    -------
    Creation of a date picker widget::
        
        from vois.vuetify import dayCalendar
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_click(day):
            with output:
                print('Clicked on ', day)

        c = dayCalendar.dayCalendar(start='2023-10-01', end='2023-10-31',
                                    days=['2023-10-10', '2023-10-20'],
                                    on_click=on_click)

        display(c.draw())
        display(output)

    .. figure:: figures/dayCalendar.png
       :scale: 100 %
       :alt: dayCalendar widget

       Example of a dayCalendar
    """
    
    
    # Initialization
    def __init__(self,
                 start=date.today() + relativedelta(months=-1), # Dates as strings in "YYYY-MM-DD" format or datetime or date instances
                 end=date.today(),
                 color=settings.color_first,                    # Color used to highlight the events
                 dark=settings.dark_mode,
                 days=[],                                       # List of strings in "YYYY-MM-DD" format to highlight some of the days
                 show_count=False,                              # If True shows in each higlighted day one char '°' for each repetition inside the days list
                 width=340,                                     # Width on pixels
                 height=None,                                   # Height in pixels
                 on_click=None,                                 # Function called at the click on a day (will receive the day as string in "YYYY-MM-DD" format as parameter)
                 on_click_event=None                            # Function called at the click on an event (will receive the day as string in "YYYY-MM-DD" format as parameter)
                ):
        
        if isinstance(start,datetime) or isinstance(start,date):
            self.start = start.strftime('%Y-%m-%d')
        else:
            self.start = start

        if isinstance(end,datetime) or isinstance(end,date):
            self.end = end.strftime('%Y-%m-%d')
        else:
            self.end = end
            
        self._color         = color
        self._days          = days
        self.show_count     = show_count
        self.width          = width
        self.height         = height
        self.on_click       = on_click
        self.on_click_event = on_click_event
        
        self.cal = v.Calendar(v_model='', start=self.start, end=self.end, now='1899-12-31', type='custom-weekly',
                              event_more=False, event_height=6, events=[], event_color=self._color, short_weekdays=True,
                              hide_header=False, show_month_on_first=True, weekdays=[1,2,3,4,5,6,0], dark=dark)                  # Week start on Monday: standard ISO!
        self.cal.on_event('input', self.__internal_on_click)
        self.cal.on_event('click:event', self.__internal_on_click_event)

        self.days2events()
        
        card_height = 53 * number_of_weeks(self.start, self.end)
        self.card = v.Card(flat=True, children=[self.cal], width=self.width, height=card_height, class_='pa-0 ma-0 mb-1')

        if self.height is None:
            self.height = 10 + card_height
            
        self.output = widgets.Output(layout=Layout(height='%dpx'%self.height))
        with self.output:
            display(self.card)
         
    
    # Convert a list of days in events for the calendar widget
    def days2events(self):
        if self.show_count:
             # See https://en.wikipedia.org/wiki/List_of_Unicode_characters
            self.events = [{'name': '\u02DA'*count, 'start': day } for day,count in collections.Counter(self._days).items()]
        else:
            self.events = [{'name': '', 'start': d} for d in list(set(self._days))]
        self.cal.events = self.events

        
    # Manage click on a day
    def __internal_on_click(self, widget, event, data):
        if not self.on_click is None:
            self.on_click(data)
        
        
    # Manage click on an event
    def __internal_on_click_event(self, widget, event, data):
        if 'event' in data:
            day = data['event']['start']
            if not self.on_click_event is None:
                self.on_click_event(day)
            
            
    # Returns the vuetify object to display (the Output widget containing the card containing the calendar)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal Output widget)"""
        return self.output

    
    # color property
    @property
    def color(self):
        """
        Get/Set the color of the highlighted days
        
        Returns
        --------
        color : str
            Color of the highlighted days in the calendar

        Example
        -------
        Programmatically change the color::
            
            cal.color = 'red'
            print(cal.color)
        
        """
        return self._color
    
    @color.setter
    def color(self, col):
        self._color = col
        self.cal.event_color = self._color
    
    
    # days property
    @property
    def days(self):
        """
        Get/Set the highlighted days
        
        Returns
        --------
        listfodays : list of strings in "YYYY-MM-DD" format
            List of days currently highlighted in the calendar

        Example
        -------
        Programmatically change the highlighted days::
            
            cal.days = ['2023-10-15', '2023-10-25']
            print(cal.days)
        
        """
        return self._days
    
    @days.setter
    def days(self, listofdays):
        self._days = listofdays
        self.days2events()