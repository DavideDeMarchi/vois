"""Display and selection of a list of SVG files"""
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
import traitlets
import os
import base64


# Given a path of an SVG file, it reads the content and returns a string containing a IMG tab with the SVG embedded in base64 format
def readSVGbase64(filepath, fill=None, stroke=None):
    svgtext = ''
    with open(filepath,'r') as f:
        svgtext = f.read()
        
    if (not fill is None) and (not stroke is None):
        svgtext.replace('<svg ','<svg fill="%s" stroke="%s"'%(fill,stroke))
    elif not fill is None:
        svgtext.replace('<svg','<svg fill="%s"'%fill)
    elif not stroke is None:
        svgtext.replace('<svg','<svg stroke="%s"'%stroke)

    base64_bytes  = base64.b64encode(bytes(svgtext,'utf-8'))
    base64_string = base64_bytes.decode("ascii")
    return "data:image/svg+xml;base64, %s" % base64_string


# Given a path of an SVG file, it reads the content and returns a string containing a IMG tab with the SVG embedded in base64 format
def readSVGimg(filepath, size=100):
    imgurl = readSVGbase64(filepath)
    return '<img src="%s", style="width:%dpx; height:%dpx; display: flex; justify-content: center; align-items: center; overflow: hidden;">'%(imgurl,size,size) + '</img>'


class svgsGrid(v.VuetifyTemplate):
    """
    Display of a list of SVG files in rows and columns, with possibility to select one of the SVGs.
        
    Parameters
    ----------
    filepaths : list of str
        File paths of the SVG files to display in the grid
    width : str, optional
        Width to use for the display of the SVGs (default is '80px')
    height : str, optional
        Heigth to use for the display of the SVGs (default is '100px' to accomodate for the title of the files)
    cols : int, optional
        Horizontal column span [1,12] for each of the SVGs (default is 1, meaning 12 files are displayed in every row)
    color : str, optional
        Background color of the SVGs (default is 'white')
    ripple : bool, optional
        If True the click on the SVG files is highlighted (default is False)
    svgsize : int, optional
        Size in pixel of the square area where the SVG is displayed (default is 80)
    on_click : function, optional
        Python function to call when the user clicks on one of the SVG files. The function will receive as parameter the index of the clicked SVG. (default is None)

    Example
    -------
    Creation of a grid to display and select SVG files read from a subfolder::
        
        from vois.vuetify import svgsGrid
        from ipywidgets import widgets
        from IPython.display import display
        import glob

        output = widgets.Output()

        def on_click(index):
            with output:
                print(index)

        filepaths = sorted(glob.glob("./maki/icons/*"))

        svgsize = 80
        height  = '%dpx'%(svgsize + 30)
        g = svgsGrid(filepaths=filepaths, cols=1, svgsize=svgsize,
                     height=height, ripple=True, on_click=on_click)

        display(g)
        display(output)

    .. figure:: figures/svgsGrid.png
       :scale: 100 %
       :alt: svgsGrid widget

       Example of an svgsGrid to display a list of SVG files allowing selection
    """
    
    svgitems  = traitlets.Any([]).tag(sync=True)           # SVG files to display (array of json objects containing "title" and "svg" tags)
    
    width     = traitlets.Unicode('80px').tag(sync=True)   # Width of the cards
    height    = traitlets.Unicode('100px').tag(sync=True)  # Height of the cards
    color     = traitlets.Unicode('white').tag(sync=True)  # Background color
    cols      = traitlets.Int(6).tag(sync=True)            # Horizontal column span [1,12] for each of the card
    ripple    = traitlets.Bool(False).tag(sync=True)       # Ripple flag (if True the click on the card is highlighted)
    on_click  = traitlets.Any(None).tag(sync=False)        # Name of a python function to call when one of the cards is clicked (it will receive as argument the index of the clicked card)


    @traitlets.default('template')
    def _template(self):
        return '''
<v-container fluid style="overflow: hidden;">
  <v-row dense>
    <v-col
      v-for="card,index in svgitems"
      :key="card.title"
      :cols="cols"
    >
        <v-card
            class="pa-0 ma-1"
            :width="width"
            :color="color"
            :height="height"
            hover
            :ripple="ripple"
            link
            elevation=0
            @click="clicked(index)"
        >
             <div style="display: flex; justify-content: center; align-items: center; overflow: hidden;" v-html="card.svg"/>
             <v-card-text class="pa-0 ma-0" style="font-size: 11; text-align: center;" v-html="card.title"/>
        </v-card>
    </v-col>
  </v-row>
</v-container>
'''

    def __init__(self, *args,
                 filepaths=[],
                 width='80px',
                 height='100px',
                 color='white',
                 cols=1,
                 ripple=False,
                 svgsize=80,
                 on_click=None,
                 **kwargs):
        
        self.svgitems = [{"svg": readSVGimg(x,svgsize), "title": os.path.basename(x).replace(".svg","").replace("_"," ")} for x in filepaths]
        self.width    = width
        self.height   = height
        self.color    = color
        self.cols     = cols
        self.ripple   = ripple
        self.on_click = on_click
        
        super().__init__(*args, **kwargs)
        
    
    # Manage "click" event
    def vue_clicked(self, data):
        if not self.on_click is None:
            self.on_click(data)