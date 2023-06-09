"""Side panel that opens on the side of the screen to show content or get user input."""
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
import ipyvuetify as v

try:
    from . import settings
    from . import tooltip
except:
    import settings
    import tooltip


#####################################################################################################################################################
# Display a side-panel with a close button
#####################################################################################################################################################
class sidePanel():
    """
    Side panel that opens on the side of the screen to show content or get user input.
        
    Parameters
    ----------
    title : str, optional
        Title to display on top of the side panel (default is '')
    text : str, optional
        String of text to display in the content of the side panel (default is '')
    width : int, optional
        Width of the panel in pixel (default is 500 pixels)
    right : bool, optional
        Flag that controls if the panel is opened on the right side of the screen (default is False)
    zindex : int, optional
        Z-index assigned to the panel (default is 9999)
    showclosebuttons : bool, optional
        Flag to display the close button in the top bar of the side panel (default is True)
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    backdark : bool, optional
        Flag that controls the background color of the panel (if True, the background will be black, elsewhere white)
    content : list of widgets, optional
        Additional content to be added to the side panel to get user input (default is [])
    output : ipywidgets.Output, optional
        Output widget on which the side panel has to be displayed
    onclose : function, optional
        Python function to call when the user closes the side panel. The function will be called withput any parameter
            
    Example
    -------
    Creation and display of a side panel::
        
        from vois.vuetify import sidePanel, slider
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def onclose():
            with output:
                print('CLOSED')

        text  = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore...'

        s = slider.slider(66,0,100)

        panel = sidePanel.sidePanel(title='Help panel', text=text,
                                    width=400, content=[s.draw()],
                                    output=output, onclose=onclose,
                                    dark=False)
        panel.show()

    .. figure:: figures/sidepanel.png
       :scale: 100 %
       :alt: sidepanel widget

       Example of a side panel containing text and a slider widget.
   """

    def __init__(self, title='', text='', width=500, right=False, zindex=9999, showclosebuttons=True, dark=settings.dark_mode, backdark=settings.dark_mode, content=[], output=None, onclose=None):
        
        self.onclose = onclose
        
        text = text.replace('<br>','\n')
        vvv = text.split('\n')

        if dark:
            buttontext = settings.textcolor_dark
            styletext = 'color: ' + settings.textcolor_dark + ';'
        else:
            buttontext = settings.textcolor_notdark
            styletext = 'color: ' + settings.textcolor_notdark + ';'

        ttitle  = v.ToolbarTitle(children=[title], style_=styletext)
        spacer  = v.Spacer()

        if showclosebuttons:
            # Close button
            bclose = v.Btn(text=True, children=['Close'], color=buttontext)
            bclose.on_event('click', self.close)
            bclose = tooltip.tooltip('Close the panel',bclose)

            # Close X button
            bx = v.Btn(icon=True, children=[v.Icon(children=['mdi-close'])], color=buttontext)
            bx.on_event('click', self.close)
            bx = tooltip.tooltip('Close the panel',bx)

            # Toolbar
            titems  = v.ToolbarItems(children=[bclose])
            toolbar = v.Toolbar(dark=True, color=settings.color_first, children=[bx,spacer,ttitle,spacer,titems])
        else:
            toolbar = v.Toolbar(dark=True, color=settings.color_first, children=[spacer,ttitle,spacer])
        
        # Dialog
        backcolor = 'white'
        if backdark: backcolor = settings.dark_background
        self.nav = v.NavigationDrawer(value=False, app=True, color=backcolor, width=width, style_='z-index:%d;' % zindex, right=right,
                                      children=[v.Card(elevation=0, children=[ toolbar, v.CardText(class_='pa-0 ma-0 mt-9', children=['']) ] + 
                                                                [ v.CardText(children=[x], class_="mt-n5") for x in vvv ] + content
                                                      )
                                               ])

        # Display of the panel
        if not output is None:
            with output:
                display(self.nav)
        
    # Open the panel
    def show(self):
        """Displays the side panel widget"""
        self.nav.value = True

    # Close the panel
    def close(self,*args):
        """Closes the side panel widget"""
        self.nav.value = False
        if self.onclose:
            self.onclose()
        
    # Returns True if the panel is open, False otherwise
    def isopen(self):
        """Queries the status of the side panel widget: returns True if the panel is displayed, False if it was closed"""
        return self.nav.value