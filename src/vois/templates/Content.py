"""Main content of the template1/2/3panels classes"""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2024
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

# Imports
from ipywidgets import widgets, Layout
import ipyvuetify as v

# Vois imports
from vois.vuetify import settings, toggle, selectSingle, dialogWait, sliderFloat, switch
from vois.geo import Map, mapUtils
from vois.templates import PlotlyChart, SVGdrawing, Image, PageConfigurator


# Global flag to avoid all dialogWait
dialogWaitEnabled = True

#####################################################################################################################################################
# Main content of a template1/2/3panels class
#####################################################################################################################################################
class Content(v.Card):

    # Initialization
    def __init__(self,
                 output,
                 width='50vw',            # Overall width
                 height='50vh',           # Overall height
                 splitmode=0,             # 0=single content,  1=two contents splitted vertically,   2=two contents splitted horizontally,   3=three contents,   4=four contents
                 leftwidthperc=50,        # width in percentage of left column
                 topheightperc=50,        # height in percentage of top row
                 borderwidth=2,           # Number of pixels for the border
                 linkedmaps=False,        # If True all the maps bounds are linked
                 color_first=None,        # Main color
                 color_second=None,       # Secondary color
                 dark=None,               # Dark flag
                 onStateChanged=None,     # Called just after the state property is changes
                 **kwargs):
        
        super().__init__(**kwargs)
        
        self.output         = output
        self._width         = width
        self._height        = height
        self._splitmode     = splitmode
        self._leftwidthperc = leftwidthperc
        self._topheightperc = topheightperc
        self._borderwidth   = borderwidth
        self._linkedmaps    = linkedmaps
        
        self.onStateChanged = onStateChanged
        
        self.debug = widgets.Output()
        
        # Dimensioning
        self.labelwidth   = 96
        self.togglewidth  = 46
        self.paddingrow   = 1
        
        self.spacerX = v.Html(tag='div', style_='width: 10px; height:  0px;')
        self.spacerY = v.Html(tag='div', style_='width:  0px; height: 10px;')
        self.spacer  = v.Html(tag='div', style_='width: 10px; height: 10px;')
        
        # Flag to update controls when loading the state
        self.updateWidgetsOnLoadState = False
        
        self.reset_state = {
 'splitmode': 0,
 'leftwidthperc': 50,
 'topheightperc': 50,
 'borderwidth': 2,
 'linkedmaps': False,
 'color_first': '#0d856d',
 'color_second': '#a0dcd0',
 'dark': True,
 'content1': {
    'content': 'Map',
    'show_fullscreen': True,
    'show_coordinates': True,
    'show_search': True,
    'show_scale': True,
    'show_basemaps': True,
    'show_overview': False,
    'color_first': '#0d856d',
    'color_second': '#a0dcd0',
    'dark': True,
    'basemapindex': 0,
    'center': [50, 12],
    'zoom': 5.0
    }
}
        
        # List of all the Map.Map instances
        self.maps = []
        
        # Colors of the configuration widgets
        self._color_first = color_first
        if self._color_first is None:
            self._color_first = settings.color_first
        
        self._color_second = color_second
        if self._color_second is None:
            self._color_second = settings.color_second
            
        self._dark = dark
        if self._dark is None:
            self._dark = settings.dark_mode

        # Main card
        self.card = v.Card(flat=True, color='#ffffff', tile=True,
                           width=self._width,   min_width=self._width,   max_width=self._width,
                           height=self._height, min_height=self._height, max_height=self._height)
        
        self.card1 = self.card2 = self.card3 = self.card4 = None
        self.card1children = self.card2children = self.card3children = self.card4children = None    # Widgets to display in the component cards
        
        m = Map.Map()
        self.set1(m)
        m.observe(self.onMapBoundsChanged, 'bounds')
        
        self.children = [self.card]
        
        
        # Widgets for confugure GUI
        self.toggle_splitmode = toggle.toggle(self.splitmode, ['', '', '', '', ''], dark=self._dark, icons=['mdi-border-all-variant', 'mdi-dock-right', 'mdi-view-agenda-outline', 'mdi-view-compact-outline', 'mdi-border-all'], outlined=False,
                                              tooltips=['Single area', 'Two areas splitted horizontally', 'Two areas splitted vertically', 'Three areas', 'Four areas'],
                                              onchange=self.splitmodeChange, row=True, width=self.togglewidth, height=30, justify='start', paddingrow=self.paddingrow, tile=True)

        contents = ['None', 'Map', 'Plotly Chart', 'SVG Drawing', 'Image']
        self.select1 = selectSingle.selectSingle('Content for area 1:', contents, selection='Map',  clearable=False, width=200, onchange=self.onselect1Change)
        self.select2 = selectSingle.selectSingle('Content for area 2:', contents, selection='None', clearable=False, width=200, onchange=self.onselect2Change)
        self.select2.disabled = True
        self.select3 = selectSingle.selectSingle('Content for area 3:', contents, selection='None', clearable=False, width=200, onchange=self.onselect3Change)
        self.select3.disabled = True
        self.select4 = selectSingle.selectSingle('Content for area 4:', contents, selection='None', clearable=False, width=200, onchange=self.onselect4Change)
        self.select4.disabled = True
        
        self.sliderleftwidth = sliderFloat.sliderFloat(50, text='Left column percent:', showpercentage=True, decimals=0, minvalue=0.0, maxvalue=100.0, maxint=100,
                                                       labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.leftwidthChange)
        self.sliderleftwidth.slider.disabled = True
        
        self.slidertopheight = sliderFloat.sliderFloat(50, text='Top row percent:', showpercentage=True, decimals=0, minvalue=0.0, maxvalue=100.0, maxint=100,
                                                       labelwidth=self.labelwidth-10, sliderwidth=150, resetbutton=True, showtooltip=True, onchange=self.topheightChange)
        self.slidertopheight.slider.disabled = True

        self.mapslinked = switch.switch(self._linkedmaps, 'Maps linked', inset=True, dense=True, onchange=self.linkedChange)
        self.mapslinked.disabled = True
        self.propagateBounds = True
        self.showWaitDialogOnUpdate = False

        self.selectborder = selectSingle.selectSingle('Border in pixel:', ['0', '1', '2', '3'], selection=str(self._borderwidth),  clearable=False, width=100, onchange=self.onselectBorder)

            
        self.toggle_configure = toggle.toggle(0, ['', '', '', ''], dark=self._dark, icons=['mdi-numeric-1-box-outline', 'mdi-numeric-2-box-outline', 'mdi-numeric-3-box-outline', 'mdi-numeric-4-box-outline'], outlined=False,
                                              tooltips=['Configure area 1', 'Configure area 2', 'Configure area 3', 'Configure area 4'],
                                              onchange=self.configureChange, row=True, width=self.togglewidth, height=30, justify='start', paddingrow=self.paddingrow, tile=True)
        self.toggle_configure.buttons[1].disabled = True
        self.toggle_configure.buttons[2].disabled = True
        self.toggle_configure.buttons[3].disabled = True
        
        
        self.card_configure = v.Card(flat=True)
        
        self.splitmodeChange(self.splitmode)
        self.configureChange(0)
        self.update()
        
        self.createAccessStrings()

        
    # Create strings for easy access to content
    def createAccessStrings(self):
        dnames = {
            Map.Map: 'map',
            PlotlyChart.PlotlyChart: 'chart',
            SVGdrawing.SVGdrawing:   'svg',
            Image.Image:             'image'
        }
        self.access1 = self.access2 = self.access3 = self.access4 = ''
        if self.card1children is not None: self.access1 = "self.%s1 = self.content.card1children"%dnames[type(self.card1children)]
        if self.card2children is not None: self.access2 = "self.%s2 = self.content.card2children"%dnames[type(self.card2children)]
        if self.card3children is not None: self.access3 = "self.%s3 = self.content.card3children"%dnames[type(self.card3children)]
        if self.card4children is not None: self.access4 = "self.%s4 = self.content.card4children"%dnames[type(self.card4children)]

        
    # Selection of the area to configure
    def configureChange(self, index):
        area_configure = ''
        if index == 0:
            if self.card1children is not None:
                area_configure = self.card1children.configure()
        elif index == 1:
            if self.card2children is not None:
                area_configure = self.card2children.configure()
        elif index == 2:
            if self.card3children is not None:
                area_configure = self.card3children.configure()
        elif index == 3:
            if self.card4children is not None:
                area_configure = self.card4children.configure()
        
        self.card_configure.children = [area_configure]
        
        
    # GUI interface for content selection
    def configure(self):
        return v.Card(flat=True, children=[widgets.VBox([
            self.spacerY,
            widgets.HBox([PageConfigurator.label('Split mode:', color='black', width=self.labelwidth), self.toggle_splitmode.draw()]),
            self.spacerY,
            self.sliderleftwidth.draw(),
            self.slidertopheight.draw(),
            self.spacerY,
            self.spacerY,
            widgets.HBox([self.select1.draw(), self.spacerX, self.mapslinked.draw()]),
            widgets.HBox([self.select2.draw(), self.spacerX, self.spacerX, self.selectborder.draw()]),
            self.select3.draw(),
            self.select4.draw(),
            self.spacerY,
            widgets.HBox([PageConfigurator.label('Content: ', color='black', width=self.labelwidth-40), self.toggle_configure.draw()]),
            self.spacerY,
            self.card_configure,
        ])])
        
        
    # Reset the state to the initial one
    def reset(self):
        self.state = self.reset_state
    
    
    # Selecton of the splitmode
    def splitmodeChange(self, index):
        self.splitmode = index
    

    # Change of an area content
    def changeAreaContent(self, setfunction, contentname):
        
        if self.showWaitDialogOnUpdate and dialogWaitEnabled:
            dlg = dialogWait.dialogWait(text='Updating content...', output=self.output, color=self._color_first, dark=self._dark)
        
        if contentname == 'Map':
            m = Map.Map(color_first=self._color_first, color_second=self._color_second, dark=self._dark)
            setfunction(m)
            m.observe(self.onMapBoundsChanged, 'bounds')
        elif contentname == 'Plotly Chart':
            setfunction(PlotlyChart.PlotlyChart(color_first=self._color_first, color_second=self._color_second, dark=self._dark))
        elif contentname == 'SVG Drawing':
            setfunction(SVGdrawing.SVGdrawing(color_first=self._color_first, color_second=self._color_second, dark=self._dark))
        elif contentname == 'Image':
            setfunction(Image.Image(self.output, color_first=self._color_first, color_second=self._color_second, dark=self._dark))
        else:
            setfunction(None)
            
        # Count the number of Maps and if more than 1 enable the linked switch
        self.maps = []
        if isinstance(self.card1children, Map.Map): self.maps.append(self.card1children)
        if isinstance(self.card2children, Map.Map): self.maps.append(self.card2children)
        if isinstance(self.card3children, Map.Map): self.maps.append(self.card3children)
        if isinstance(self.card4children, Map.Map): self.maps.append(self.card4children)
        
        if len(self.maps) < 2:
            self.mapslinked.disabled = True
        else:
            self.mapslinked.disabled = False
            
        self.configureChange(self.toggle_configure.value)

        self.createAccessStrings()
        
        if self.showWaitDialogOnUpdate and dialogWaitEnabled:
            dlg.close()
                       

            
    # Management of the linked state among the maps
    def onMapBoundsChanged(self, change):
        if self.propagateBounds:
            if len(self.maps) > 1:
                if self._linkedmaps:
                    inputMap = change['owner']
                    for m in self.maps:
                        if not m is inputMap:
                            self.propagateBounds = False
                            m.center = inputMap.center
                            m.zoom   = inputMap.zoom
                            self.propagateBounds = True
    
    
    # Select* change
    def onselect1Change(self):
        self.changeAreaContent(self.set1, self.select1.value)
        
    def onselect2Change(self):
        self.changeAreaContent(self.set2, self.select2.value)
        
    def onselect3Change(self):
        self.changeAreaContent(self.set3, self.select3.value)
        
    def onselect4Change(self):
        self.changeAreaContent(self.set4, self.select4.value)
                               
    
    # Change of left width
    def leftwidthChange(self, value):
        self.leftwidthperc = int(value)
    
    
    # Change of the top height
    def topheightChange(self, value):
        self.topheightperc = int(value)
    
    
    # Set the linked flag
    def linkedChange(self, flag):
        self._linkedmaps = self.mapslinked.value
        if self._linkedmaps:
            if len(self.maps) > 1:
                self.onMapBoundsChanged({'owner': self.maps[0]})
    
    
    # Selection of a border
    def onselectBorder(self):
        self.propagateBounds = False
        self.borderwidth = int(self.selectborder.value)
        self.propagateBounds = True

    
    # Returns the vuetify object to display (the v.Card)
    def draw(self):
        return self
    

    # Update all colors
    def updateColors(self):
        if self.card1children is not None: self.card1children.color_first = self._color_first
        if self.card2children is not None: self.card2children.color_first = self._color_first
        if self.card3children is not None: self.card3children.color_first = self._color_first
        if self.card4children is not None: self.card4children.color_first = self._color_first
        
        if self.card1children is not None: self.card1children.color_second = self._color_second
        if self.card2children is not None: self.card2children.color_second = self._color_second
        if self.card3children is not None: self.card3children.color_second = self._color_second
        if self.card4children is not None: self.card4children.color_second = self._color_second
        
        if self.card1children is not None: self.card1children.dark = self._dark
        if self.card2children is not None: self.card2children.dark = self._dark
        if self.card3children is not None: self.card3children.dark = self._dark
        if self.card4children is not None: self.card4children.dark = self._dark
        
        
    # Update the content when splitmode is changed
    def update(self):

        wl = 'calc(%s * %f)'%(self._width, self._leftwidthperc/100)
        wr = 'calc(%s * %f)'%(self._width, (100 - self._leftwidthperc)/100)
        ht = 'calc(%s * %f)'%(self._height, self._topheightperc/100)
        hb = 'calc(%s * %f)'%(self._height, (100 - self._topheightperc)/100)
        
        # Single content
        if self._splitmode == 0:
            self.card1 = v.Card(flag=True, tile=True, style_='overflow: hidden;',
                                width=self._width,   min_width=self._width,   max_width=self._width,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = None
            self.card3 = None
            self.card4 = None
            
            self.card.children = [self.card1]
            self.toggle_configure.value = 0
            self.toggle_configure.buttons[1].disabled = True
            self.toggle_configure.buttons[2].disabled = True
            self.toggle_configure.buttons[3].disabled = True
        
        # 2 horizontal contents
        elif self._splitmode == 1:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: %dpx solid %s; overflow: hidden;'%(self._borderwidth,self._color_first),
                                width=wl, min_width=wl, max_width=wl,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card2 = v.Card(flag=True, tile=True, 
                                width=wr, min_width=wr, max_width=wr,
                                height=self._height, min_height=self._height, max_height=self._height)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.HBox([self.card1, self.card2])]
            if self.toggle_configure.value > 1: self.toggle_configure.value = 0
            self.toggle_configure.buttons[1].disabled = False
            self.toggle_configure.buttons[2].disabled = True
            self.toggle_configure.buttons[3].disabled = True
            
            
        # 2 vertical contents
        elif self._splitmode == 2:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-bottom: %dpx solid %s; overflow: hidden;'%(self._borderwidth,self._color_first),
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, 
                                width=self._width, min_width=self._width, max_width=self._width,
                                height=hb, min_height=hb, max_height=hb)
    
            self.card3 = None
            self.card4 = None
            
            self.card.children = [widgets.VBox([self.card1, self.card2])]
            if self.toggle_configure.value > 1: self.toggle_configure.value = 0
            self.toggle_configure.buttons[1].disabled = False
            self.toggle_configure.buttons[2].disabled = True
            self.toggle_configure.buttons[3].disabled = True

        # 2 vertical contents + 1 on the right at full height
        elif self._splitmode == 3:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: %dpx solid %s; border-bottom: %dpx solid %s; overflow: hidden;'%(self._borderwidth, self._color_first,
                                                                                                                                                                                   self._borderwidth, self._color_first),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: %dpx solid %s; overflow: hidden;'%(self._borderwidth,self._color_first),
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=self._height, min_height=self._height, max_height=self._height)
            self.card4 = None
            
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), self.card3])]
            if self.toggle_configure.value > 2: self.toggle_configure.value = 0
            self.toggle_configure.buttons[1].disabled = False
            self.toggle_configure.buttons[2].disabled = False
            self.toggle_configure.buttons[3].disabled = True
            
        # 4 contents
        else:
            self.card1 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: %dpx solid %s; border-bottom: %dpx solid %s; overflow: hidden;'%(self._borderwidth, self._color_first,
                                                                                                                                                                                   self._borderwidth, self._color_first),
                                width=wl, min_width=wl, max_width=wl,
                                height=ht, min_height=ht, max_height=ht)
            self.card2 = v.Card(flag=True, tile=True, outlined=True, style_='border: 0px solid red; border-right: %dpx solid %s; overflow: hidden;'%(self._borderwidth,self._color_first),
                                width=wl, min_width=wl, max_width=wl,
                                height=hb, min_height=hb, max_height=hb)
            self.card3 = v.Card(flag=True, tile=True, style_='border: 0px solid red; border-bottom: %dpx solid %s; overflow: hidden;'%(self._borderwidth,self._color_first),
                                width=wr, min_width=wr, max_width=wr,
                                height=ht, min_height=ht, max_height=ht)
            self.card4 = v.Card(flag=True, tile=True,
                                width=wr, min_width=wr, max_width=wr,
                                height=hb, min_height=hb, max_height=hb)
            self.card.children = [widgets.HBox([widgets.VBox([self.card1, self.card2]), widgets.VBox([self.card3, self.card4])])]
            self.toggle_configure.buttons[1].disabled = False
            self.toggle_configure.buttons[2].disabled = False
            self.toggle_configure.buttons[3].disabled = False
    
        
        self.updateColors()
        
        self.set1(self.card1children)
        self.set2(self.card2children)
        self.set3(self.card3children)
        self.set4(self.card4children)
    
    
    # Set the content of cards 1,2,3,4 (can pass None or a widget that has width and height properties
    def set1(self, children=None):
        self.card1children = children
        if self.card1 is not None:
            if self.card1children is None:
                self.card1.children = []
            else:
                self.card1children.width  = self.card1.width
                self.card1children.height = self.card1.height
                self.card1.children = [self.card1children.draw()]
                self.updateColors()
    
    def set2(self, children=None):
        self.card2children = children
        if self.card2 is not None:
            if self.card2children is None:
                self.card2.children = []
            else:
                self.card2children.width  = self.card2.width
                self.card2children.height = self.card2.height
                self.card2.children = [self.card2children.draw()]
                self.updateColors()
    
    def set3(self, children=None):
        self.card3children = children
        if self.card3 is not None:
            if self.card3children is None:
                self.card3.children = []
            else:
                self.card3children.width  = self.card3.width
                self.card3children.height = self.card3.height
                self.card3.children = [self.card3children.draw()]
                self.updateColors()
    
    def set4(self, children=None):
        self.card4children = children
        if self.card4 is not None:
            if self.card4children is None:
                self.card4.children = []
            else:
                self.card4children.width  = self.card4.width
                self.card4children.height = self.card4.height
                self.card4.children = [self.card4children.draw()]
                self.updateColors()
                
                
    #####################################################################################################################################################
    # Properties
    #####################################################################################################################################################
    
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = w
        self.card.width = self._width
        self.card.min_width = self._width
        self.card.max_width = self._width
        self.update()

        
    @property
    def height(self):
        return self._height
        
    @height.setter
    def height(self, h):
        self._height = h
        self.card.height = self._height
        self.card.min_height = self._height
        self.card.max_height = self._height
        self.update()

        
    @property
    def splitmode(self):
        return self._splitmode
        
    @splitmode.setter
    def splitmode(self, sm):
        self._splitmode = int(sm)
        
        self.select2.disabled = self._splitmode == 0
        self.select3.disabled = self._splitmode < 2
        self.select3.disabled = self._splitmode < 3
        self.select4.disabled = self._splitmode < 4
        
        self.sliderleftwidth.slider.disabled = self._splitmode == 0 or self._splitmode == 2
        self.slidertopheight.slider.disabled = self._splitmode < 2

        if self.updateWidgetsOnLoadState:
            old = self.toggle_splitmode.onchange
            self.toggle_splitmode.onchange = None
            self.toggle_splitmode.value = self._splitmode
            self.toggle_splitmode.onchange = old

        self.update()

        
    @property
    def leftwidthperc(self):
        return self._leftwidthperc
        
    @leftwidthperc.setter
    def leftwidthperc(self, w):
        self._leftwidthperc = min(100, max(w, 0))
        
        if self.updateWidgetsOnLoadState:
            old = self.sliderleftwidth.onchange
            self.sliderleftwidth.onchange = None
            self.sliderleftwidth.value = self._leftwidthperc
            self.sliderleftwidth.onchange = old
        
        self.update()

        
    @property
    def topheightperc(self):
        return self._topheightperc
        
    @topheightperc.setter
    def topheightperc(self, h):
        self._topheightperc = min(100, max(h, 0))
        
        if self.updateWidgetsOnLoadState:
            old = self.slidertopheight.onchange
            self.slidertopheight.onchange = None
            self.slidertopheight.value = self._topheightperc
            self.slidertopheight.onchange = old
        
        self.update()
        
        
    @property
    def borderwidth(self):
        return self._borderwidth
        
    @borderwidth.setter
    def borderwidth(self, w):
        self._borderwidth = min(3, max(int(w), 0))
        if self.propagateBounds:
            self.selectborder.value = str(self._borderwidth)
            
        if self.updateWidgetsOnLoadState:
            old = self.selectborder.onchange
            self.selectborder.onchange = None
            self.selectborder.value = str(self._borderwidth)
            self.selectborder.onchange = old
            
        self.update()

        
    @property
    def linkedmaps(self):
        return self._linkedmaps
        
    @linkedmaps.setter
    def linkedmaps(self, flag):
        self._linkedmaps = flag
        self.mapslinked.value = self._linkedmaps

        
    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        self.toggle_splitmode.colorselected = self._color_first
        self.select1.color = self._color_first
        self.select2.color = self._color_first
        self.select3.color = self._color_first
        self.select4.color = self._color_first
        self.sliderleftwidth.color = self._color_first
        self.slidertopheight.color = self._color_first
        self.mapslinked.color = self._color_first
        self.toggle_configure.colorselected = self._color_first
        self.selectborder.color = self._color_first
        self.update()


    @property
    def color_second(self):
        return self._color_second
        
    @color_second.setter
    def color_second(self, color):
        self._color_second = color

        self.toggle_splitmode.colorunselected = self._color_second
        self.toggle_configure.colorunselected = self._color_second
        self.updateColors()

        
    @property
    def dark(self):
        return self._dark
        
    @dark.setter
    def dark(self, flag):
        self._dark = flag
        
        self.toggle_splitmode.dark = self._dark
        self.toggle_configure.dark = self._dark
        self.updateColors()

        
    @property
    def state(self):
        s = {x: getattr(self, x) for x in ['width',
                                           'height',
                                           'splitmode',
                                           'leftwidthperc',
                                           'topheightperc',
                                           'borderwidth',
                                           'linkedmaps',
                                           'color_first',
                                           'color_second',
                                           'dark'
                                          ]}
        
        if self.card1children is not None: s['content1'] = self.card1children.state
        if self.card2children is not None: s['content2'] = self.card2children.state
        if self.card3children is not None: s['content3'] = self.card3children.state
        if self.card4children is not None: s['content4'] = self.card4children.state
        return s
        
    @state.setter
    def state(self, statusdict):
        
        # To prevent other dialogWait to be opened
        self.showWaitDialogOnUpdate = False
        
        if dialogWaitEnabled:
            dlg = dialogWait.dialogWait(text='Updating content...', output=self.output, color=statusdict['color_first'], dark=statusdict['dark'])
        
        self.updateWidgetsOnLoadState = True
        
        self.card1children = self.card2children = self.card3children = self.card4children = None
        
        for key, value in statusdict.items():
            if key == 'content1':
                self.select1.value = value['content']
                self.card1children.state = value
            elif key == 'content2':
                self.select2.value = value['content']
                self.card2children.state = value
            elif key == 'content3':
                self.select3.value = value['content']
                self.card3children.state = value
            elif key == 'content4':
                self.select4.value = value['content']
                self.card4children.state = value
            else:
                setattr(self, key, value)
                
        self.update()
        
        self.updateWidgetsOnLoadState = False
        
        self.createAccessStrings()
        
        # Call the callback function
        if self.onStateChanged is not None:
            self.onStateChanged()
        
        if dialogWaitEnabled:
            dlg.close()
            
        self.showWaitDialogOnUpdate = True
        