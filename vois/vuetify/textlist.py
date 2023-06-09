"""Widget to display text strings vertically aligned."""
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
except:
    import settings


#####################################################################################################################################################
# Testlist control
#####################################################################################################################################################
class textlist():
    """
    Widget to vertically display a list of titles and texts strings. Each couple of title and text occupies a row.
        
    Parameters
    ----------
    titles : list of strings
        Strings to be displayed as title of each row
    texts : list of strings
        Strings to be displayed as the content of each row
    titlesbold : list of strings, optional
        List of titles whose corresponding texts should be displayed in with bold font (default is [])
    titlefontsize : int, optional
        Size in pixel of the font used for the titles (default is 12)
    textfontsize : int, optional
        Size in pixel of the font used for the texts (default is 12)
    titlecolumn : int, optional
        Number of column (out of 12) occupied by the titles (default is 4)
    textcolumn : int, optional
        Number of column (out of 12) occupied by the texts (default is 8)
    titlecolor : str, optional
        Color to use for the titles (default is 'black')
    textcolor : str, optional
        Color to use for the texts (default is 'black')
    lineheightfactor : float, optional
        Factor to multiply to the font-size to calculate the height of each row (default is 1.5)

    Example
    -------
    Creation and display of a widget to display some textual information::
        
        from vois.vuetify import textlist
        from IPython.display import display
        
        t = textlist.textlist(['Name', 'Surname', 'Address', 'Role'],
                              ['Davide', 'De Marchi', 'via Eduardo 34, Roccacannuccia (PE)', 'Software developer'],
                              titlesbold=['Surname'],
                              titlefontsize=14,
                              textfontsize=16,
                              titlecolumn=3,
                              textcolumn=10,
                              titlecolor='#003300',
                              textcolor='#000000',
                              lineheightfactor=1.4
                             )

        # Set some attributes of the card widget (margins, colors, width, etc.)
        t.card.class_    = 'pa-0 ma-4 ml-6 mr-8'
        t.card.flat      = False
        t.card.color     = '#e0ffe0'
        t.card.elevation = 8
        t.card.width     = '430px'

        display(t.draw())


    .. figure:: figures/textlist.png
       :scale: 100 %
       :alt: textlist widget

       Textlist widget for displaying textual information.
   """

    # Initialization
    def __init__(self,
                 titles,
                 texts,
                 titlesbold=[],
                 titlefontsize=12,
                 textfontsize=12,
                 titlecolumn=4,
                 textcolumn=8,
                 titlecolor='black',
                 textcolor='black',
                 lineheightfactor=1.5):
        self.titlefontsize    = titlefontsize
        self.textfontsize     = textfontsize
        self.titlecolumn      = titlecolumn
        self.textcolumn       = textcolumn
        self.titlecolor       = titlecolor
        self.textcolor        = textcolor
        self.lineheightfactor = lineheightfactor
        self.div  = v.Divider(class_='pa-0 ma-0 ml-1 mr-1', vertical=False)
        self.card = v.Card(flat=True)
        self.update(titles, texts, titlesbold)
        
        
    # Update the widget with new titles and strings
    def update(self, titles, texts, titlesbold=[]):
        self.card.children = []
        children = []
        lineheight = "line-height: %dpx;"%(int(self.lineheightfactor*(max(self.titlefontsize,self.textfontsize)))) # To ensure vertical center alignment
        for title,text in zip(titles, texts):
            c1 = v.Col(cols=self.titlecolumn,  class_="pa-0 ma-0 ml-3",
                        children=[v.Html(tag='div', class_='pa-0 ma-0', children=[str(title)],
                                        style_='color: %s; font-weight: 450; text-transform: none; font-size: %dpx; %s'%(self.titlecolor, self.titlefontsize,lineheight))],
                        style_="overflow: hidden;")

            if title in titlesbold: weight = 500
            else:                   weight = 350

            c2 = v.Col(cols=self.textcolumn,  class_="pa-0 ma-0",
                       children=[v.Html(tag='div', class_='pa-0 ma-0', 
                                        children=[str(text)], 
                                        style_='color: %s; font-weight: %d; text-transform: none; font-size: %dpx; %s'%(self.textcolor, weight,self.textfontsize,lineheight))],
                       style_="overflow: hidden;")
            children.append(v.Layout(class_="pa-0 ma-0", children=[c1,c2], style_="overflow: visible;"))
            children.append(self.div)

        self.card.children = children
        
   
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Card widget)"""
        return self.card

