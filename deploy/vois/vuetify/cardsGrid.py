"""Cards with title, subtitle and image displayed in rows and columns"""
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


class cardsGrid(v.VuetifyTemplate):
    """
    Cards with title, subtitle and image displayed in a grid of rows and columns.
        
    Parameters
    ----------
    cards : list of json element, one for each card to display, optional
        Each of the json elements must have this structure: { "title": "", "subtitle": "", "image": ""}, optional tags are "color", "imagesize", "icon" and "iconsize", "titletooltip"
    width : str, optional
        Width of the cards (default is '400px')
    height : str, optional
        Heigth of the cards (default is '' which means that each card has its own height defined by its content)
    cols : int, optional
        Horizontal column span [1,12] for each of the card (default is 6)
    color : str, optional
        Background color of the cards (default is 'white')
    dark : bool, optional
        If True the title and subtitle texts are displayed in white color, if False they are displayed in black (default is False)
    ripple : bool, optional
        If True the click on the card is highlighted (default is False)
    iconsize : str, optional
        Size of the area where the icon is displayed (default is '32px')
    imagesize : str, optional
        Size of the area where the image is displayed (default is '190px')
    on_click : function, optional
        Python function to call when the user clicks on the card. The function will receive as parameter the index of the clicked card. (default is None)
    responsive : bool, optional
        If True, the font size is automatically changed according to the page size (default is False)
    fontsizemultiplier : float, optional
        Multiply factor for changing the standard size of the font used for title and subtitle (default is 1.0)
    tooltipwidth : str, optional
        Max width of the tooltip window to open on hover on the cards title (default is '600px')

    Example
    -------
    Creation of a cards grid to display text and an image::
        
        from vois.vuetify import cardsGrid
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_click(index):
            with output:
                print(index)

        cards = [
           { "title": "title0", "subtitle": "subtitle0", "image": "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg", "titletooltip": "Example of card title tooltip" },
           { "title": "title1", "subtitle": "subtitle1", "image": "https://cdn.vuetifyjs.com/images/cards/road.jpg" },
           { "title": "title2", "subtitle": "subtitle2", "image": "https://cdn.vuetifyjs.com/images/cards/plane.jpg" },
           { "title": "title3", "subtitle": "subtitle3", "image": "https://cdn.vuetifyjs.com/images/cards/house.jpg" }
        ]

        g = cardsGrid.cardsGrid(cards=cards, cols=6, width='350px', imagesize='200px', on_click=on_click)

        display(g)
        display(output)

    .. figure:: figures/cardsGrid.png
       :scale: 100 %
       :alt: cardsGrid widget

       Example of a cardsGrid to display multiple cards containing texts and an images
    """
    
    cards     = traitlets.Any([]).tag(sync=True)           # Cards to display (array of json objects containing "title", "subtitle", "image" tags)
    
    width     = traitlets.Unicode('400px').tag(sync=True)  # Width of the cards
    height    = traitlets.Unicode('').tag(sync=True)       # Height of the cards
    color     = traitlets.Unicode('white').tag(sync=True)  # Background color
    cols      = traitlets.Int(6).tag(sync=True)            # Horizontal column span [1,12] for each of the card
    dark      = traitlets.Bool(False).tag(sync=True)       # Dark mode flag (if True the text is displayed in white)
    ripple    = traitlets.Bool(False).tag(sync=True)       # Ripple flag (if True the click on the card is highlighted)
    on_click  = traitlets.Any(None).tag(sync=False)        # Name of a python function to call when one of the cards is clicked (it will receive as argument the index of the clicked card)
    responsive         = traitlets.Bool(False).tag(sync=True)
    fontsizemultiplier = traitlets.Float(1.0).tag(sync=True)
    tooltipwidth = traitlets.Unicode('600px').tag(sync=True)  # Width of the tooltip


    @traitlets.default('template')
    def _template(self):
        return '''
<v-container fluid>
  <v-row dense>
    <v-col
      v-for="card,index in cards"
      :key="card.title"
      :cols="cols"
    >
        <v-card
            class="pa-0 ma-1"
            :width="width"
            :color="color"
            :dark="dark"
            :height="height"
            hover
            :ripple="ripple"
            link
            @click="clicked(index)"
        >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                  <v-row dense>
                      <v-avatar class="pa-0 ma-0 ml-3 mt-2 mr-n2" :size="card.iconsize" tile >
                          <v-img :src="card.icon"></v-img>
                      </v-avatar>
                      <div :style="card.color">
                         <v-tooltip v-if="card.titletooltip" bottom :max-width="tooltipwidth">
                            <template v-slot:activator="{ on, attrs }">
                               <v-card-title v-bind="attrs" v-on="on" class="mt-n2 mb-1" :style="fontSizeTitle" v-text="card.title"></v-card-title>
                            </template>
                            <span>{{card.titletooltip}}</span>
                         </v-tooltip>
                         <v-card-title v-else class="mt-n2 mb-1" :style="fontSizeTitle" v-text="card.title"></v-card-title>
                      </div>
                  </v-row>
                  <div :style="card.color">
                    <div :class="card.margins" :style="fontSizeSubTitle" v-html="card.subtitle"/>
                  </div>
              </div>
              <v-avatar class="ma-0" :size="card.imagesize" tile >
                  <v-img :src="card.image" contain ></v-img>
              </v-avatar>
            </div>
        </v-card>
    </v-col>
  </v-row>
</v-container>

<script>
  export default {
    computed: {
      fontSizeTitle (num)
        {
         if( this.responsive )
           {
            switch( this.$vuetify.breakpoint.name )
              {
               case 'xs': return 'font-size: ' + (0.75*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'sm': return 'font-size: ' + (1.00*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'md': return 'font-size: ' + (1.25*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'lg': return 'font-size: ' + (1.45*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'xl': return 'font-size: ' + (1.60*this.fontsizemultiplier).toFixed(3) + 'em;'
              }
           }
         else
           {
            return 'font-size: ' + (1.25*this.fontsizemultiplier).toFixed(3) + 'em;'
           }
      },
        
      fontSizeSubTitle ()
        {
         if( this.responsive )
           {
            switch( this.$vuetify.breakpoint.name )
              {
               case 'xs': return 'font-size: ' + (0.8*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'sm': return 'font-size: ' + (0.9*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'md': return 'font-size: ' + (1.0*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'lg': return 'font-size: ' + (1.1*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'xl': return 'font-size: ' + (1.2*this.fontsizemultiplier).toFixed(3) + 'em;'
              }
           }
         else
           {
            return 'font-size: ' + (1.0*this.fontsizemultiplier).toFixed(3) + 'em;'
           }
        },
    },
  }
</script>
'''

    def __init__(self, *args,
                 cards=[],
                 width='400px',
                 height='',
                 color='white',
                 cols=6,
                 dark=False,
                 ripple=False,
                 iconsize='32px',
                 imagesize='190px',
                 on_click=None,
                 responsive=False,
                 fontsizemultiplier=1.0,
                 tooltipwidth='600px',
                 **kwargs):
        
        for c in cards:
            if not "color" in c:
                if dark:
                    c["color"] = "color: white;"
                else:
                    c["color"] = "color: black;"
            else:
                c["color"] = "color: %s;" % c["color"]

            if not "iconsize" in c:
                c["iconsize"] = iconsize

            if not "icon" in c:
                c["icon"] = ""
                c["iconsize"] = '0px'

            if not "imagesize" in c:
                c["imagesize"] = imagesize

            if not "subtitle" in c or len(c["subtitle"]) == 0:
                c["margins"] = "ma-0 ml-4 mb-n3"
            else:
                c["margins"] = "ma-0 ml-4 mb-3"
                
        self.cards  = cards
        self.width  = width
        self.height = height
        self.color  = color
        self.cols   = cols
        self.dark   = dark
        self.ripple = ripple
        self.on_click = on_click
        
        self.responsive         = responsive
        self.fontsizemultiplier = fontsizemultiplier
        self.tooltipwidth = tooltipwidth
          
        super().__init__(*args, **kwargs)
        
    
    # Manage "click" event
    def vue_clicked(self, data):
        if not self.on_click is None:
            self.on_click(data)