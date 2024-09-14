"""IconButton to copy text to the clipboard."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2024
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
from IPython.display import HTML as ipyHTML
import ipyvuetify as v

from vois.vuetify import settings, iconButton
            
###########################################################################################################################################################################
# Icon button to copy a text to the clipboard
###########################################################################################################################################################################
class IconClipboard(v.Html):
    """
    IconButton to copy text to the clipboard.
        
    Parameters
    ----------
    output : ipywidgets.Output
        Output widget to be used to execute javacript code to copy the text to the clipboard
    text : str, optional
        Text to be copied to the clipboard (default is '', it can be changed using the 'text' property)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    outlined : bool, optional
        If True applies a thin border to the button (default is False)
    rounded : bool, optional
        If True the shape of the button is rounded (default is True)
    width : str, optional
        Width of the widget (default is None)
    large : bool, optional
        If True makes the button large (default is False)
    small : bool, optional
        If True makes the button small (default is False)
    x_large : bool, optional
        If True makes the button extra-large (default is False)
    x_small : bool, optional
        If True makes the button extra-small (default is False)
    margins : str, optional
        Marging apply to the button (default is 'pa-0 ma-0')
    tooltip : str, optional
        Tooltip text for the button (default is 'Click to copy text to the clipboard')

    Example
    -------
    Creation and display of an icon button to copy some text content to the clipboard::
        
        from vois.vuetify import IconClipboard
        from IPython.display import display
        
        b = IconClipboard()
        display(b)
        
        b.text = 'Text to copy to the clipboard'
   """
    
    def __init__(self,
                 output,
                 text='',
                 color=None,
                 outlined=False,
                 rounded=True,
                 width=None,
                 large=False,
                 small=False,
                 x_large=False,
                 x_small=False,
                 margins='pa-0 ma-0',
                 tooltip='Click to copy text to the clipboard',
                 **kwargs
                ):
        
        super().__init__(**kwargs)
        
        self.output = output
        
        self._text = text

        self._color = color
        if self._color is None:
            self._color = settings.color_first
        
        self.b = iconButton.iconButton(icon='mdi-content-copy', color=self._color, onclick=self.onclick, tooltip=tooltip,
                                       outlined=outlined, rounded=rounded, width=width,
                                       large=large, small=small, x_large=x_large, x_small=x_small, margins=margins, disabled=len(self._text)==0)

        self.tag = 'div'
        self.children = [self.b.draw()]

        
    # "old" draw
    def draw(self):
        return self
        

    # Manage click event
    def onclick(self):
        with self.output:
            display(ipyHTML('''
<script>
navigator.clipboard.writeText("%s");
//navigator.clipboard.readText().then((clipText) => (console.log("clipboard: "+clipText)))
</script>'''%self._text))
    
    
    @property
    def text(self):
        return self._text
        
    @text.setter
    def text(self, t):
        self._text = t.replace("\n","\\"+"n")   # V.I. Need to have two separate character "\" + "n" if a text with newline is copied to the clipboard!!!
        
        self.b.disabled = len(self._text)==0
