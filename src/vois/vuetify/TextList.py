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
import ipyvuetify as v

from vois.vuetify.utils.util import *
from typing import Optional


#####################################################################################################################################################
# Testlist control
#####################################################################################################################################################
class TextList(v.Card):
    """
    Widget to vertically display a list of titles and texts strings. Each couple of title and text occupies a row.
        
    Parameters
    ----------
    titles : list of strings
        Strings to be displayed as title of each row
    texts : list of strings
        Strings to be displayed as the content of each row
    titles_bold : list of strings, optional
        List of titles whose corresponding texts should be displayed in with bold font (default is [])
    title_font_size : int, optional
        Size in pixel of the font used for the titles (default is 12)
    text_font_size : int, optional
        Size in pixel of the font used for the texts (default is 12)
    title_column : int, optional
        Number of column (out of 12) occupied by the titles (default is 4)
    text_column : int, optional
        Number of column (out of 12) occupied by the texts (default is 8)
    title_color : str, optional
        Color to use for the titles (default is 'black')
    text_color : str, optional
        Color to use for the texts (default is 'black')
    line_height_factor : float, optional
        Factor to multiply to the font-size to calculate the height of each row (default is 1.5)

    Example
    -------
    Creation and display of a widget to display some textual information::
        
        from vois.vuetify import TextList
        from IPython.display import display
        
        t = TextList(['Name', 'Surname', 'Address', 'Role'],
                              ['Davide', 'De Marchi', 'via Eduardo 34, Roccacannuccia (PE)', 'Software developer'],
                              titles_bold=['Surname'],
                              title_font_size=14,
                              text_font_size=16,
                              title_column=3,
                              text_column=10,
                              title_color='#003300',
                              text_color='#000000',
                              line_height_factor=1.4
                             )

        # Set some attributes of the card widget (margins, colors, width, etc.)
        t.class_    = 'pa-0 ma-4 ml-6 mr-8'
        t.flat      = False
        t.color     = '#e0ffe0'
        t.elevation = 8
        t.width     = '430px'

        display(t)


    .. figure:: figures/textlist.png
       :scale: 100 %
       :alt: textlist widget

       Textlist widget for displaying textual information.
   """

    deprecation_alias = dict(titlesbold='titles_bold', titlefontsize='title_font_size', textfontsize='text_font_size',
                             titlecolumn='title_column', textcolumn='text_column', titlecolor='title_color',
                             textcolor='text_color', lineheightfactor='line_height_factor')

    # Initialization
    @deprecated_init_alias(**deprecation_alias)
    def __init__(self,
                 titles: list[str],
                 texts: list[str],
                 titles_bold: Optional[list[str]] = [],
                 title_font_size: int = 12,
                 text_font_size: int = 12,
                 title_column: int = 4,
                 text_column: int = 8,
                 title_color: str = 'black',
                 text_color: str = 'black',
                 line_height_factor: float = 1.5,
                 **kwargs):
        self.title_font_size = title_font_size
        self.text_font_size = text_font_size
        self.title_column = title_column
        self.text_column = text_column
        self.title_color = title_color
        self.text_color = text_color
        self.line_height_factor = line_height_factor
        self.div = v.Divider(class_='pa-0 ma-0 ml-1 mr-1', vertical=False)
        self.update(titles, texts, titles_bold)
        self.card = self

        super().__init__(flat=True, **kwargs)

        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)

    # Update the widget with new titles and strings
    def update(self, titles, texts, titles_bold=[]):
        self.children = []
        children = []
        lineheight = "line-height: %dpx;" % (int(self.line_height_factor * (
            max(self.title_font_size, self.text_font_size))))  # To ensure vertical center alignment
        for title, text in zip(titles, texts):
            c1 = v.Col(cols=self.title_column, class_="pa-0 ma-0 ml-3",
                       children=[v.Html(tag='div', class_='pa-0 ma-0', children=[str(title)],
                                        style_='color: %s; font-weight: 450; text-transform: none; font-size: %dpx; %s' % (
                                            self.title_color, self.title_font_size, lineheight))],
                       style_="overflow: hidden;")

            if title in titles_bold:
                weight = 500
            else:
                weight = 350

            c2 = v.Col(cols=self.text_column, class_="pa-0 ma-0",
                       children=[v.Html(tag='div', class_='pa-0 ma-0',
                                        children=[str(text)],
                                        style_='color: %s; font-weight: %d; text-transform: none; font-size: %dpx; %s' % (
                                            self.text_color, weight, self.text_font_size, lineheight))],
                       style_="overflow: hidden;")
            children.append(v.Layout(class_="pa-0 ma-0", children=[c1, c2], style_="overflow: visible;"))
            children.append(self.div)

        self.children = children

    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (the internal v.Card widget)"""
        warnings.warn('The "draw" method is deprecated, please just use the object widget itself.',
                      category=DeprecationWarning,
                      stacklevel=2)
        return self
