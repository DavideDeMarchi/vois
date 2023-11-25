"""Map popup widget to display titles and texts in a geographic position on a ipyleaflet Map."""
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

# Widgets import
import ipyleaflet
from ipyleaflet import AwesomeIcon, DivIcon, Marker

# Python imports
from threading import Timer


#####################################################################################################################################################
# textpopup class
#####################################################################################################################################################
class textpopup():
    """
    Widget to vertically display a list of titles and texts strings as a popup on a ipyleaflet Map. Each couple of title and text occupies a row.
        
    Parameters
    ----------
    m : instance of ipyleaflet.Map class
        Map to which the popup has to be added
    lat : float
        Latitude where the popup has to be displayed (default is 0.0)
    lon : float
        Longitude where the popup has to be displayed (default is 0.0)
    titles : list of strings
        Strings to be displayed as title of each row (default is [])
    texts : list of strings
        Strings to be displayed as the content of each row (default is [])
    width : int
        Width of the popup in pixels (default is 200)
    height : int
        Height of the popup in pixel (default is None meaning that the height will be automatically calcolated)
    autoremovedelay : float
        Time in seconds for automatic remnoving of the popup (default is 0.0 which disables autoremove)
    titlesbold : list of strings, optional
        List of titles whose corresponding texts in the left column should be displayed using bold font (default is [])
    titlefontsize : int, optional
        Size in pixel of the font used for the titles (default is 12)
    textsbold : list of strings, optional
        List of titles whose corresponding texts in the right column should be displayed using bold font (default is [])
    textfontsize : int, optional
        Size in pixel of the font used for the texts (default is 12)
    titlecolor : str, optional
        Color to use for the titles (default is 'black')
    textcolor : str, optional
        Color to use for the texts (default is 'black')
    lineheightfactor : float, optional
        Factor to multiply to the font-size to calculate the height of each row (default is 1.5)

    Example
    -------
    Creation and display of a widget to display some textual information::
        
        from ipywidgets import widgets, HTML, CallbackDispatcher
        from ipyleaflet import Map
        from IPython.display import display

        from vois import textpopup

        m = Map(center=[43.66737, 12.5504], scroll_wheel_zoom=True, zoom=13)

        t = None
        def handle_interaction_popup(**kwargs):
            global t

            if kwargs.get('type') == 'click':
                lat = kwargs.get('coordinates')[0]
                lon = kwargs.get('coordinates')[1]

                textpopup.textpopup.removeAll(m)
                t = textpopup.textpopup(m, lat=lat, lon=lon, autoremovedelay=5.0,
                                        width=340, height=None, titlewidth=70,
                                        titles=['Pixel values', 'Class'],
                                        texts=['(120,34,189)', 'Woodland and Shrubland (incl. permanent crops)'],
                                        titlesbold=[],
                                        titlefontsize=11,
                                        textsbold=['Pixel'],
                                        textfontsize=11,
                                        titlecolor='darkgreen',
                                        textcolor='darkred')

        m._interaction_callbacks = CallbackDispatcher()
        m.on_interaction(handle_interaction_popup)

        display(m)

    .. figure:: figures/textpopup.png
       :scale: 100 %
       :alt: textpopup widget

       Map popup widget for displaying textual information.
   """
    
    def __init__(self,
                 m,
                 lat=0.0,
                 lon=0.0,
                 titles=[],
                 texts=[],
                 width=200,
                 height=None,
                 autoremovedelay=10.0,
                 titlesbold=[],
                 titlefontsize=12,
                 textsbold=[],
                 textfontsize=12,
                 titlewidth=50,
                 titlecolor='black',
                 textcolor='black',
                 lineheightfactor=1.1
                ):
        self.m = m
        self.autoremovedelay = autoremovedelay
    
        lineheight = "line-height: %dpx;"%(int(lineheightfactor*(max(titlefontsize,textfontsize)))) # To ensure vertical center alignment
    
        # Autocalc height
        if height is None:
            height = max(titlefontsize,textfontsize)*lineheightfactor*1.1*max(len(titles),len(texts)) + 12
    
        margin = 5
        width  += 2*margin
        height += margin
        
        self.h = '<table border="0" style="border-collapse: collapse; margin-right: %dpx; margin-left: %dpx; margin-top: %dpx; margin-bottom: 0px; display: block; width: %dpx; height: %dpx; overflow-y: auto;"><tbody>'%(margin,margin,margin, width,height)
        for i, title in enumerate(titles):
            if i < len(texts):
                text = texts[i]
            else:
                text = ''
            if title in titlesbold: tdtitle = 'th'
            else:                   tdtitle = 'td'
            if title in textsbold:  tdtext  = 'th'
            else:                   tdtext  = 'td'
            self.h += '''<tr style="border-bottom: 1px solid lightgrey;">
  <%s align="center" style="width: %dpx; font-size: %dpx; color: %s; %s">%s</%s>
  <%s align="center" style="width: %dpx; font-size: %dpx; color: %s; %s">%s</%s>
</tr>'''%(tdtitle,titlewidth,titlefontsize,titlecolor,lineheight,title,tdtitle, 
          tdtext,width-titlewidth-4*margin,textfontsize,textcolor,lineheight,text,tdtext)

        self.h += '</tbody></table>'
        
        center = (lat,lon)
        icon1 = AwesomeIcon(name='', marker_color='white', icon_color='white', spin=False)
        self.marker1 = Marker(name='textpopup', icon=icon1, location=center)

        icon2 = DivIcon(html=self.h, icon_anchor=[width/2, height+14], icon_size=[width, height])
        self.marker2 = Marker(name='textpopup', location=center, icon=icon2)
    
        self.m.add_layer(self.marker1)
        self.m.add_layer(self.marker2)
        
        # Auto-remove after some time
        if self.autoremovedelay > 0:
            self.timer = Timer(self.autoremovedelay, self.remove)
            self.timer.start()
    
    
    # Remove the textpopup from the map
    def remove(self):
        if self.autoremovedelay > 0:
            self.timer.cancel()
            
        if self.marker1 in self.m.layers:
            self.m.remove_layer(self.marker1)
        if self.marker2 in self.m.layers:
            self.m.remove_layer(self.marker2)
        
    
    # Remove all textpopups from a map
    @staticmethod
    def removeAll(m):
        for layer in reversed(m.layers):
            if isinstance(layer, ipyleaflet.leaflet.Marker) and layer.name == 'textpopup':
                m.remove_layer(layer)
