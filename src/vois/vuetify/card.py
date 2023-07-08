"""Simple card with title, subtitle and image."""
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


class card(v.VuetifyTemplate):
    """
    Simple card displaying title, subtitle and an image.
        
    Parameters
    ----------
    width : str, optional
        Width of the card (default is '400px')
    color : str, optional
        Background color of the card (default is 'white')
    dark : bool, optional
        If True the title and subtitle texts are displayed in white color, if False they are displayed in black (default is False)
    ripple : bool, optional
        If True the click on the card is highlighted (default is False)
    elevation : int, optional
        Elevation of the card over the background of the page (default is 3)
    title : str, optional
        Title of the card (default is 'Title')
    subtitle : str, optional
        Subtitle of the card (default is 'Subtitle')
    icon : str, optional
        URL of the image to display as an icon before the card title (default is '')
    iconsize : str, optional
        Size of the area where the icon is displayed (default is '32px')
    image : str, optional
        URL of the image to display in the right side of the card (default is '')
    imagesize : str, optional
        Size of the area where the image is displayed (default is '190px')
    on_click : function, optional
        Python function to call when the user clicks on the card. The function will receive no parameters. (default is None)
    argument : any, optional
        Argument to pass to the on_click python function (default is None)
    responsive : bool, optional
        If True, the font size is automatically changed according to the page size (default is False)
    fontsizemultiplier : float, optional
        Multiply factor for changing the standard size of the font used for title and subtitle (default is 1.0)
    backgroundimageurl : str, optional
        URL of the optional image to display as background of the card (default is '')
    tooltip : str, optional
        Text to display as tooltip of the whole card (default is '')
    titletooltip : str, optional
        Text to display as tooltip of the card title (default is '')
    focusedopacity : float, optional
        Opacity of the card background when the card is clicked (has focus). Default is 0.1
    textcolor : str, optional
        Color of the text (default is 'black')
    titleweight : int, optional
        Font weight for the title (default is 700)
    subtitleweight : int, optional
        Font weight for the subtitle (default is 400)

    Example
    -------
    Creation of a card to display text and an image::
        
        from vois.vuetify import card
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def on_click():
            with output:
                print('clicked!')

        subtitle = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi...'
        width = 600

        c = card.card(elevation=5, width='600px', title='Sample dataset', subtitle=subtitle,
                      image='https://cdn.vuetifyjs.com/images/cards/halcyon.png', on_click=on_click)

        display(c)
        display(output)

    .. figure:: figures/card.png
       :scale: 100 %
       :alt: card widget

       Example of a card with text and an image
    """
    
    width      = traitlets.Unicode('400px').tag(sync=True)
    height     = traitlets.Unicode('').tag(sync=True)
    color      = traitlets.Unicode('white').tag(sync=True)
    dark       = traitlets.Bool(False).tag(sync=True)
    ripple     = traitlets.Bool(False).tag(sync=True)       # Ripple flag (if True the click on the card is highlighted)
    disabled   = traitlets.Bool(False).tag(sync=True)
    elevation  = traitlets.Int(5).tag(sync=True)
    title      = traitlets.Unicode('Title').tag(sync=True)
    subtitle   = traitlets.Unicode('Subtitle').tag(sync=True)
    icon       = traitlets.Unicode('').tag(sync=True)
    iconsize   = traitlets.Unicode('32px').tag(sync=True)
    image      = traitlets.Unicode('').tag(sync=True)
    imagesize  = traitlets.Unicode('190px').tag(sync=True)
    on_click   = traitlets.Any(None).tag(sync=False)
    argument   = traitlets.Any(None).tag(sync=False)
    responsive = traitlets.Bool(False).tag(sync=True)
    fontsizemultiplier = traitlets.Float(1.0).tag(sync=True)
    backgroundimageurl = traitlets.Unicode('').tag(sync=True)
    
    subtitlemargins = traitlets.Unicode('ma-0 ml-4 mb-4 mt-0 mr-4').tag(sync=True)
    focusedopacity  = traitlets.Float(0.1).tag(sync=True)
    textcolor       = traitlets.Unicode('black').tag(sync=True)
    titleweight     = traitlets.Int(700).tag(sync=True)
    subtitleweight  = traitlets.Int(400).tag(sync=True)

    
    @traitlets.default('template')
    def _template(self):
        
        pre  = ''
        ttip = ''
        post = ''
        
        if len(self.tooltip) > 0:
            pre  = '<v-hover v-slot="{ hover }">'
            ttip = '<v-tooltip attach allow-overflow absolute center bottom z-index=99999 v-model="hover"><span>%s</span></v-tooltip>' % self.tooltip
            post = '</v-hover>'

        title_pre  = ''
        title_att  = ''
        title_post = ''
        
        if len(self.titletooltip) > 0:
            title_pre  = '<v-tooltip bottom max-width="%s"><template v-slot:activator="{ on, attrs }">' % str(self.width)
            title_att  = 'v-bind="attrs" v-on="on"'
            title_post = '</template><span>%s</span></v-tooltip>' % self.titletooltip
                  

        return '''
%s

  <v-card
    class="pa-1 ma-1"
    :width="width"
    :height="height"
    :color="color"
    :dark="dark"
    raised
    hover
    :elevation="elevation"
    :ripple="ripple"
    :disabled="disabled"
    @click="clicked"
    style="overflow: hidden;"
    :img="backgroundimageurl"
  >
      <div class="d-flex flex-no-wrap justify-space-between">
        %s
        <div>
            <v-row dense>
                <v-avatar class="pa-0 ma-0 ml-3 mt-2 mr-n2" :size="iconsize" tile >
                    <v-img :src="icon"></v-img>
                </v-avatar>
                
                %s
                <v-card-title %s class="mt-n2 mb-1" :style="fontSizeTitle" v-text="title"></v-card-title>
                %s
            </v-row>
          <div :class="subtitlemargins" :style="fontSizeSubTitle" v-html="subtitle"/>
      </div>
      <v-avatar class="ma-n1" :size="imagesize" tile >
         <v-img :src="image" contain></v-img>
      </v-avatar>
    </div>
  </v-card>
%s

<script>
  export default {
    computed: {
      fontSizeTitle ()
        {
         if( this.responsive )
           {
            switch( this.$vuetify.breakpoint.name )
              {
               case 'xs': return 'color: %s; font-weight: %d; font-size: ' + (0.75*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'sm': return 'color: %s; font-weight: %d; font-size: ' + (1.00*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'md': return 'color: %s; font-weight: %d; font-size: ' + (1.25*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'lg': return 'color: %s; font-weight: %d; font-size: ' + (1.45*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'xl': return 'color: %s; font-weight: %d; font-size: ' + (1.60*this.fontsizemultiplier).toFixed(3) + 'em;'
              }
           }
         else
           {
            return 'colors: %s; font-weight: %d; font-size: ' + (1.25*this.fontsizemultiplier).toFixed(3) + 'em;'
           }
      },
        
      fontSizeSubTitle ()
        {
         if( this.responsive )
           {
            switch( this.$vuetify.breakpoint.name )
              {
               case 'xs': return 'color: %s; font-weight: %d; font-size: ' + (0.8*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'sm': return 'color: %s; font-weight: %d; font-size: ' + (0.9*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'md': return 'color: %s; font-weight: %d; font-size: ' + (1.0*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'lg': return 'color: %s; font-weight: %d; font-size: ' + (1.1*this.fontsizemultiplier).toFixed(3) + 'em;'
               case 'xl': return 'color: %s; font-weight: %d; font-size: ' + (1.2*this.fontsizemultiplier).toFixed(3) + 'em;'
              }
           }
         else
           {
            return 'color: %s; font-weight: %d; font-size: ' + (1.0*this.fontsizemultiplier).toFixed(3) + 'em;'
           }
        },
    },
  }
</script>

<style>
.vuetify-styles .v-card--link:focus::before {
  opacity: %f;
}
</style>


''' % (pre,ttip, title_pre,title_att,title_post, post,
       self.textcolor,self.titleweight,    self.textcolor,self.titleweight,    self.textcolor,self.titleweight,    self.textcolor,self.titleweight,    self.textcolor,self.titleweight,    self.textcolor,self.titleweight, 
       self.textcolor,self.subtitleweight, self.textcolor,self.subtitleweight, self.textcolor,self.subtitleweight, self.textcolor,self.subtitleweight, self.textcolor,self.subtitleweight, self.textcolor,self.subtitleweight, 
       self.focusedopacity)
    
    def __init__(self,
                 *args,
                 width='400px',
                 height='',
                 color='white',
                 dark=False,
                 ripple=False,
                 disabled=False,
                 elevation=3,
                 title='Title',
                 subtitle='Subtitle',
                 icon='',
                 iconsize='32px',
                 image='',
                 imagesize='190px',
                 on_click=None,
                 argument=None,
                 responsive=False,
                 fontsizemultiplier=1.0,
                 backgroundimageurl='',
                 tooltip='',
                 titletooltip='',
                 focusedopacity=0.1,     # Opacity for the background when the card is clicked (has focus)
                 textcolor='black',
                 titleweight=700,
                 subtitleweight=400,
                 **kwargs):

        self.tooltip        = tooltip
        self.titletooltip   = titletooltip
        self.focusedopacity = focusedopacity
        self.textcolor      = textcolor
        self.titleweight    = titleweight
        self.subtitleweight = subtitleweight
 
        self.width     = width
        self.height    = height
        self.color     = color
        self.dark      = dark
        self.ripple    = ripple
        self.disabled  = disabled
        self.elevation = elevation
        self.title     = title
        self.subtitle  = subtitle
        if len(self.subtitle) == 0:
            self.subtitlemargins = 'ma-0 ml-4 mb-n4 mt-0'

        self.icon = icon
        if len(icon) == 0: self.iconsize = '0px'
        else:              self.iconsize = iconsize
        
        self.image = image
        if len(image) == 0: self.imagesize = '0px'
        else:               self.imagesize = imagesize
        
        self.on_click = on_click
        self.argument = argument
        
        self.responsive         = responsive
        self.fontsizemultiplier = fontsizemultiplier
        self.backgroundimageurl = backgroundimageurl
        
        super().__init__(*args, **kwargs)
    
    # Manage event "click"
    def vue_clicked(self, data):
        if not self.on_click is None:
            if self.argument is None:
                self.on_click()
            else:
                self.on_click(self.argument)