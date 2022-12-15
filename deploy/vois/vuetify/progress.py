"""Circular progress bar to use for lenghty operations."""
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
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.

from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
except:
    import settings


#####################################################################################################################################################
# Display a circular progress bar centered inside an output widget
#####################################################################################################################################################
class progress():
    """
    Circular progress bar to use for lenghty operations.
        
    Parameters
    ----------
    output : ipywidgets.Output
        Output widget on which the progress bar has to be displayed
    text : str, optional
        Small text to display inside the circle (default is '')
    show : bool, optional
        If True, display the progress upon creation (default is False)
    size : int, optional
        Diameter of the circle in pixels (default is 120 pixels)
    width : int, optional
        Width in pixels of the moving line (default is 15)
    outputheight : int, optional
        Height in pixels of the output widget (default is 400 pixels)
    onchange : function, optional
        Python function to call when the user selects one of the values in the list. The function will receive no parameter (use value property to retrieve the current selection)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
            
    Example
    -------
    Creation and display of a progress widget::
        
        from voilalibrary.vuetify import progress
        from ipywidgets import widgets, Layout
        from IPython.display import display

        outputheight = 500
        output = widgets.Output(layout=Layout(width='99%', height='%dpx' % (outputheight+10)))
        display(output)

        p = progress.progress(output, text='Please, wait...',
                              size=200, width=20,
                              show=True, outputheight=outputheight)
        
    To close the progress::
    
        p.close()
        

    .. figure:: figures/progress.png
       :scale: 100 %
       :alt: progress widget

       Example of progress widget displayed inside an Output.
   """
        
    def __init__(self,
                 output,                             # Output widget where the progress must be displayed
                 text='',                            # Small text inside the circle
                 show=False,                         # If True, display the progress upon creation
                 size=120,                           # Diameter of the circle in pixels
                 width=15,                           # Width of the moving line
                 outputheight=400,                   # Height in pixels of the output widget
                 color=settings.color_first):        # Color
        
        self.output = output
        self.size   = size
        self.outputheight = outputheight
        
        self.prog = v.ProgressCircular(style_='overflow: hidden;', class_='pa-0 ma-0', indeterminate=True, size=size, width=width, children=[text], color=color)

        self.nav = None
        
        if show:
            self.show()
        

    # Display the progress
    def show(self):
        """Displays the progress into the output widget"""
        if not self.output is None:
            self.output.clear_output(wait=True)
            with self.output:
                # Centered vertically and horizontally!
                h = v.Html(tag='div', style_="height: %dpx; display: flex; justify-content: center; align-content: center; align-items:center; flex-direction: column; " % self.outputheight, 
                           class_="text-center", children=[self.prog])

                display(h)

    # Display the progress as an overlay in a specific position
    def showAbsolute(self, output, left, top, zindex=9999):
        """Displays the progress as an overlay layer in a specific position
        
        Parameters
        ----------
        output : ipywidgets.Output
            Output widget to use for the display of the transparent widget
        left : str
            Position of the left side of the widget. It can be in pixels, vw, or other units.
        top : str
            Position of the top side of the widget. It can be in pixels, vh, or other units.
        zindex : int, optional
            Z-index of the progress on the page (default is 9999)
        """
        self.nav = v.NavigationDrawer(stateless=True, permanent=True, floating=True, fixed=True, left=True, color="transparent", 
                                      width="%dpx"%self.size, height="%dpx"%self.size,
                                      style_="left: %s; top: %s; z-index: %d;" % (left, top, zindex), class_="pa-0 ma-0", children=[self.prog])
        with output:
            display(self.nav)

            
    # Hide the progress
    def close(self):
        """Hides the progress by clearing the output widget content"""
        if not self.output is None:
            self.output.clear_output()

        if not self.nav is None:
            self.nav.close()
            