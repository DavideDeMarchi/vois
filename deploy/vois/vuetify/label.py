"""Label widget to display a text with an optional icon."""
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
    from . import fontsettings
except:
    import settings
    import tooltip
    import fontsettings


#####################################################################################################################################################
# Label class that can display also an icon
#####################################################################################################################################################
class label:
    """
    Label widget to display a text with an optional icon.
        
    Parameters
    ----------
    text : str
        Test string to be displayed on the label widget
    onclick : function, optional
        Python function to call when the user clicks on the label. The function will receive as parameter the value of the argument (default is None)
    argument : any, optional
        Argument to be passed to the onclick function when user click on the label (default is None)
    disabled : bool, optional
        Flag to show the label as disabled (default is False)
    textweight : int, optional
        Weight of the text to be shown in the label (default is 350, Bold is any value greater or equal to 500)
    height : int, optional
        Height of the label widget in pixels (default is 20)
    margins : int, optional
        Dimension of the margins on all directions (default is 0)
    margintop : int, optional
        Dimension of the margin on top of the label (default is None)
    icon: str, optional
        Name of the icon to display aside the text of the label (default is None)
    iconlarge : bool, optional
        Flag that sets the large version of the icon (default is False)
    iconsmall : bool, optional
        Flag that sets the small version of the icon (default is False)
    iconleft : bool, optional
        Flag that sets the position of the icon  to the left of the text of the label (default is False)
    iconcolor : str, optional
        Color of the icon (default is 'black')
    tooltip : str, optional
        Tooltip string to display when the user hovers on the label (default is None)
    textcolor : str, optional
        Color used for the label text
    backcolor : str, optional
        Color used for the background of the label
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
            

    Note
    ----
    All the icons from https://materialdesignicons.com/ site can be used, just by prepending 'mdi-' to their name.
    
    All the free icons from https://fontawesome.com/ site can be used, just by prepending 'fa-' to their name.


    Example
    -------
    Creation and display of a label widget containing an icon::
        
        from vois.vuetify import label

        lab = label.label('Test label', textweight=300, margins=2,
                          icon='mdi-car-light-high', iconcolor='red',
                          iconlarge=True, height=22)

        display(lab.draw())
    
    
    .. figure:: figures/label.png
       :scale: 100 %
       :alt: label widget

       Example of a label widget with text and an icon.
   """

   
    # Initialization
    def __init__(self, text, onclick=None, argument=None, disabled=False, textweight=350, height=20, margins=0, margintop=None, 
                 icon=None, iconlarge=False, iconsmall=False, iconleft=False, iconcolor='black', tooltip=None,
                 textcolor=None, backcolor=None, dark=settings.dark_mode):
        
        self.labeltext = text
        self.onclick   = onclick
        self.argument  = argument
        
        self.disabled   = disabled
        self.textweight = textweight
        self.height     = height
        self.margins    = margins
        self.margintop  = margintop
    
        self.icon       = icon
        self.iconleft   = iconleft
        self.iconlarge  = iconlarge
        self.iconsmall  = iconsmall
        self.iconcolor  = iconcolor

        self.tooltip    = tooltip
        
        self.textcolor  = textcolor
        self.backcolor  = backcolor
        self.dark       = dark
        
        if not self.dark is None:
            if self.dark:
                if self.backcolor is None: self.backcolor='#111111'
                if self.textcolor is None: self.textcolor='white'

        self.__createLabel()
       
        
    # Create the label
    def __createLabel(self):
        if self.icon is None:
            childs = [self.labeltext]
        else:
            childs = [self.labeltext, v.Icon(left=self.iconleft, large=self.iconlarge, small=self.iconsmall, color=self.iconcolor, children=[self.icon])]
            
        strstyle = 'font-family: %s; font-size: 10; font-weight: %d; text-transform: none;' % (fontsettings.font_name, self.textweight)
        if not self.textcolor is None:
            strstyle += 'color: %s;' % self.textcolor
        if not self.backcolor is None:
            strstyle += 'background-color: %s;' % self.backcolor
        
        self.item = v.Card(disabled=self.disabled, elevation=0, height=self.height, depressed=True, children=childs, style_=strstyle)
        if not self.tooltip is None:
            self.item = tooltip.tooltip(self.tooltip, self.item)
            
        
        # If requested onclick management
        if not self.onclick is None:
            self.item.on_event('click', self.__internal_onclick)
            
        if not self.margintop is None:
            self.container = v.Container(class_="pa-0 ma-%s mt-%s" % (str(self.margins), str(self.margintop)), children=[ self.item ])
        else:
            self.container = v.Container(class_="pa-0 ma-%s" % (str(self.margins)), children=[ self.item ])
        
        
    # Manage click event
    def __internal_onclick(self, widget=None, event=None, data=None):
        if self.onclick:
            if not self.argument is None:
                self.onclick(self.argument)
            else:
                self.onclick()
    
    # Returns the vuetify object to display (the v.Container)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Html which has a v.Container as its only child)"""
        return v.Html(tag='div',children=[self.container])
    
    
    # Get the label text
    @property
    def text(self):
        """
        Get/Set the label text.
        
        Returns
        --------
        text : str
            Text currently shown in the label

        Example
        -------
        Programmatically set the label text (needs a re-display to be visible!)::
            
            lab.text = 'New text for the label'
            display(lab.draw())
            print(lab.text)
        
        """
        return self.labeltext
   
    
    # Set the label text
    @text.setter
    def text(self, newtext):
        self.labeltext = newtext
        self.__createLabel()
            
