"""Select widget that displays images and enables for single selection.""" 
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

try:
    from . import settings
except:
    import settings

    
class selectImage(v.VuetifyTemplate):
    """
    Select widget that displays images and enables for single selection.
        
    Parameters
    ----------
    images : list of json element, one for each image to display, optional
        Each of the json elements must have "name", and "image" tags. Optional tags are "max_width", "max_height", "margins"
    label : str, optional
        Label to show in the select widget (default is '')
    selection : int, optional
        Index of the image to display as selected in the selection widgets at start (default is -1)
    onchange : function, optional
        Python function to call when the user selects one of the images. The function will receive no parameters. (default is None)
    color : str, optional
        Main color of the selection widget (default is settings.color_first)
    outlined : bool, optional
        If True the selection widget will have a border around it (default is True)
    clearable : Bool, optional
        If True the selection widget will show a -x- button to clear the selection (default is True)
    width : str, optional
        Width of the select widget. It can be expressed as pixels (ex: "400px") or percentage (ex: "50%"). Default is "100%"
    dense : Bool, optional
        If True the items of the widgets have a reduced height (default is True)
    max_width : int, optional
        Max width in pixels of the images displayed inside the selection widget (default is 100)
    max_height : int, optional
        Max height in pixels of the images displayed inside the selection widget (default is 100)
    margins : str, optional
        Margins to apply to the images in the selection list and when displayed as selected in the widget (default is "ma-0 mr-1 mb-1")

    Example
    -------
    Creation of a select widget to select an image::
        
        from vois.vuetify import selectImage
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange():
            with output:
                print(s.value)


        images = [
              { "name": 'Image 0', "image": 'https://cdn.vuetifyjs.com/images/cards/plane.jpg'},
              { "name": 'Image 1', "image": 'https://cdn.vuetifyjs.com/images/cards/house.jpg'},
              { "name": 'Image 2', "image": 'https://cdn.vuetifyjs.com/images/cards/road.jpg'},
              { "name": 'Image 3', "image": 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg'}
        ]

        s = selectImage.selectImage(images=images, selection=1, max_height=100, onchange=onchange,
                                    label='Please select an image from the list', 
                                    outlined=True, clearable=True, margins="ma-1")

        display(s)
        display(output)
        
    .. figure:: figures/selectImage.png
       :scale: 100 %
       :alt: selectImage widget

       Example of a selectImage widget
    """
    
    images    = traitlets.Any([]).tag(sync=True)    # images to display (array of json objects containing "name", and "image" tags).
                                                    # Optional tags are "max_width", "max_height", "margins"
    selection = traitlets.Any(None).tag(sync=True)
    label     = traitlets.Unicode('').tag(sync=True)
    color     = traitlets.Unicode(settings.color_first).tag(sync=True)
    outlined  = traitlets.Bool(True).tag(sync=True)
    clearable = traitlets.Bool(True).tag(sync=True)
    dense     = traitlets.Bool(True).tag(sync=True)
    style     = traitlets.Unicode('width: %100%; max-width: 100%;').tag(sync=True)
    
    template  = traitlets.Unicode('''
<v-card style="overflow: hidden;">
  <v-select
    :value="selection"
    :v-model="selection"
    :items="images"
    :color="color"
    :clearable="clearable"
    :outlined="outlined"
    :label="label"
    class="pa-0 ma-0 mt-1 mb-n6"
    :dense="dense"
    :style="style"
    @input="input">

    <template v-slot:selection="{ item, index }">
        <v-img :class="item.margins" :src="item.image" :max-width="item.max_width"  :max-height="item.max_height" ></v-img>
        {{item.name}}
    </template>

    <template v-slot:item="{ item }">
        <v-img :class="item.margins" :src="item.image" :max-width="item.max_width"  :max-height="item.max_height" ></v-img>
        {{item.name}}
    </template>
  </v-select>
</template>

<style id="treeview-item-style">

.v-application .primary--text {
    color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000 !important;
}
.v-list .v-list-item--active { 
  background-color: #ffffff !important; 
}
.v-list .v-list-item--active .v-list-item__title {
  color: #000000 !important;
}

</style>
''').tag(sync=True)
    
    

    def __init__(self, images=[], label='', selection=-1, onchange=None,
                 color=settings.color_first, width="100%",
                 dense=True, outlined=True, clearable=True, 
                 max_width=100, max_height=100, margins="ma-0 mr-1 mb-1"):
        
        super().__init__()

        self.max_width  = max_width
        self.max_height = max_height
        self.margins    = margins
        
        i = 0
        for img in images:
            img["index"] = i
            i += 1
            if not "name" in img:
                img["name"] = ""
            if not "max_width" in img:
                img["max_width"] = str(self.max_width)
            if not "max_height" in img:
                img["max_height"] = str(self.max_height)
            if not "margins" in img:
                img["margins"] = self.margins
        
        self.images          = images
        self.label           = label
        self.onchange        = onchange
        self.color           = color
        self.dense           = dense
        self.outlined        = outlined
        self.clearable       = clearable
        self.style           = 'width: %s; max-width: %s;' % (str(width), str(width))
        self._value          = -1
        self.selection       = None
        if isinstance(selection, int) and selection >= 0 and selection < len(self.images):
            self._value = selection
            self.selection = self.images[selection]
        
        
    # Manage event "input"
    def vue_input(self, data):
        if 'index' in data:
            self._value = data['index']
        else:
            self._value = -1
        if self.onchange:
            self.onchange()

            
    # value property
    @property
    def value(self):
        """
        Get/Set the selected image index.
        
        Returns
        --------
        v : int
            index of the image currently selected

        Example
        -------
        Programmatically select one of the images given its index::
            
            sel.value = 3
            print(sel.value)
        
        """
        return self._value

    
    @value.setter
    def value(self, v):
        if isinstance(v, int) and v >= 0 and v < len(self.images):
            self._value = v
            self.selection = self.images[v]
        else:
            self._value = -1
            self.selection = ''
        if self.onchange: self.onchange()
            
            
    # Set the images
    def setImages(self, images):
        """
        Change the images to be selected.
        
        Parameters
        ----------
        images : list of json element, one for each image to display
            Each of the json elements must have "name", and "image" tags. Optional tags are "max_width", "max_height", "margins"
        """
        
        i = 0
        for img in images:
            img["index"] = i
            i += 1
            if not "name" in img:
                img["name"] = ""
            if not "max_width" in img:
                img["max_width"] = str(self.max_width)
            if not "max_height" in img:
                img["max_height"] = str(self.max_height)
            if not "margins" in img:
                img["margins"] = self.margins
        self.images = images
        
        self._value = -1
        self.selection = None
            