"""Widget to display a quick message to the user in an overlapping window that will disappear after a timeout"""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright (C) 2022-2030 European Union (Joint Research Centre)
#
# This file is part of BDAP voilalibrary.
#
# voilalibrary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# voilalibrary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.from IPython.display import display

import ipyvuetify as v
import textwrap

try:
    from . import settings
except:
    import settings


#####################################################################################################################################################
# Display a quick message to a user
#####################################################################################################################################################
class snackbar():
    """
    Widget to display a quick message to the user in an overlapping window that will disappear after a timeout.
        
    Parameters
    ----------
    title : str, optional
        Title of the message
    text : str, optional
        Text of the message
    show : bool, optional
        Flag to control the immediate show of the message to the user (default is True)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    wrapwidth : int optional
        Number of chars for each line of the message (default is 80)
    timeout : int, optional
        Timeout in milliseconds before the widget disappears (default is 10000, 10 seconds)
    output : ipywidgets.Output, optional
        Output widget on which the snackbar has to be displayed
            
    Example
    -------
    Creation and display of a snackbar message::
        
        from voilalibrary.vuetify import snackbar
        from ipywidgets import widgets

        title = 'Title of the message'
        text  = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore...'

        s = snackbar.snackbar(title=title, text=text, show=True, wrapwidth=40, timeout=3000)
        s.draw()

    .. figure:: figures/snackbar.png
       :scale: 100 %
       :alt: snackbar widget

       Example of a snackbar message
   """

    def __init__(self, title='', text='', show=False, color=settings.color_first, dark=settings.dark_mode, wrapwidth=80, timeout=10000, output=None):
        
        if dark:
            buttontext = settings.textcolor_dark
            styletext = 'color: ' + settings.textcolor_dark + ';'
        else:
            buttontext = settings.textcolor_notdark
            styletext = 'color: ' + settings.textcolor_notdark + ';'
        
        bclose = v.Btn(text=True, children=['Close'], color=buttontext)
        bclose.on_event('click', self.__onclose)

        a = textwrap.wrap(text=text, width=wrapwidth)
       
        textlines = [v.CardTitle(class_="pa-0 ma-0", style_=styletext, children=[title])] + [v.CardText(class_="pa-0 ma-0", style_=styletext, children=[x]) for x in a]
        col = v.Col(cols=12, children=textlines)

        self.snack = v.Snackbar(v_model=show, timeout=timeout, color=color, multiline=True, vertical=True, dark=dark, children=[col, bclose])
        
        # Display of the pane;
        if not output is None:
            with output:
                display(self.snack)

                
    def __onclose(self, *args):
        self.snack.v_model = False
        

    # Returns the vuetify object to display (the v.Snackbar)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Snackbar widget)"""
        return self.snack
   
    def show(self):
        """Shows the snackbar message"""
        self.snack.v_model = True
        
    def close(self):
        """Closes the snackbar message"""
        self.snack.v_model = False

