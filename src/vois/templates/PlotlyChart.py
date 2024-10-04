"""Example of Plotly Chart that is centered in a v.Card"""
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
import plotly.express as px

# Vois imports
from vois.vuetify import settings, sliderFloat
from vois.templates import PageConfigurator

import warnings

warnings.filterwarnings(
    action="ignore",
    message=r"When grouping with a length-1 list-like, you will need to pass a length-1 tuple to get_group in a future version of pandas\. Pass `\(name,\)` instead of `name` to silence this warning\.",
    category=FutureWarning,
    module=r"plotly\.express\._core",
)

#####################################################################################################################################################
# Example of Plotly Chart that is centered in a v.Card
#####################################################################################################################################################
class PlotlyChart(v.Card):
    
    def __init__(self,
                 width='99%',             # Dimensions of the overall card displaying the chart
                 height='400px',
                 chart_width=500,         # Chart width in pixels
                 chart_height=250,        # Chart height in pixels
                 color_first=None,        # Main color
                 color_second=None,       # Secondary color
                 dark=None,               # Dark flag
                 **kwargs
                ):
        
        super().__init__(flat=True, tile=True, width=width, height=height,
                         style_='overflow: hidden;', class_='d-flex align-center justify-center',
                         **kwargs)
        
        # Dimensions in pixels of the chart
        self._chart_width  = chart_width
        self._chart_height = chart_height
        
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
            
        self.configure_card = None
        self.sw = self.sh = None
        self.update_properties = True

        # Ouput and clipping card
        self.output = widgets.Output(layout=Layout(width='%dpx'%self._chart_width, height='%dpx'%(50 + self._chart_height)))
        self.clip = v.Card(flat=True, tile=True, width='%dpx'%self._chart_width, height='%dpx'%self._chart_height, children=[self.output], style_='overflow: hidden;')
        
        # Sample chart
        df = px.data.iris()
        self._fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
        self._fig.update_layout(title='Sample chart', template='plotly_white', autosize=False, width=self._chart_width, height=self._chart_height, margin=dict(l=0, r=0, b=0, t=30))
        
        # Display figure in the output widget
        with self.output:
            self._fig.show()
            
        # Set the clipped Card as the children of the overall Card
        self.children = [self.clip]
        

    # Fake "draw" method
    def draw(self):
        return self
        

    # Update when chart_width or chart_height properties are set
    def update(self):
        self.output.layout.width  = '%dpx'%self._chart_width
        self.output.layout.height = '%dpx'%(50 + self._chart_height)
        self.clip.width  = '%dpx'%self._chart_width
        self.clip.height = '%dpx'%self._chart_height

        self.output.clear_output(wait=True)
        with self.output:
            display(self._fig.show())
        
        
    @property
    def content(self):
        return 'Plotly Chart'
        
    @content.setter
    def content(self, c):
        pass
    
    
    @property
    def chart_width(self):
        return self._chart_width
        
    @chart_width.setter
    def chart_width(self, w):
        self._chart_width = int(w)
        self._fig.update_layout(width=self._chart_width)
        self.update()

        if self.sw is not None:
            self.update_properties = False
            self.sw.value = self._chart_width
            self.update_properties = True
        
        
    @property
    def chart_height(self):
        return self._chart_height
        
    @chart_height.setter
    def chart_height(self, h):
        self._chart_height = int(h)
        self._fig.update_layout(height=self._chart_height)
        self.update()
        
        if self.sh is not None:
            self.update_properties = False
            self.sh.value = self._chart_height
            self.update_properties = True
        
        
        
    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        if self.sw is not None:
            self.sw.slider.color = color
            
        if self.sh is not None:
            self.sh.slider.color = color


    @property
    def color_second(self):
        return self._color_second
        
    @color_second.setter
    def color_second(self, color):
        self._color_second = color


    @property
    def dark(self):
        return self._dark
        
    @dark.setter
    def dark(self, flag):
        self._dark = flag

            
    @property
    def fig(self):
        return self._fig
        
    @fig.setter
    def fig(self, f):
        self._fig = f
        self._fig.update_layout(width=self._chart_width)
        self._fig.update_layout(height=self._chart_height)
        
        self.output.clear_output(wait=True)
        with self.output:
            display(self._fig.show())
        
        
        
        
    def changeW(self, w):
        if self.update_properties:
            self.chart_width = w
        
    def changeH(self, h):
        if self.update_properties:
            self.chart_height = h
        
        
    # Create a card instance to configure the chart dimensions in pixels
    def configure(self):
        if self.configure_card is None:
            self.configure_card = v.Card(flat=True, class_='pa-2 ma-0')
            
            self.sw = sliderFloat.sliderFloat(self._chart_width, text='Chart width in pixels:', minvalue=20.0, maxvalue=1400.0, maxint=1380, showpercentage=False, decimals=0,
                                                   labelwidth=96, sliderwidth=140, resetbutton=True, showtooltip=True, onchange=self.changeW, color=self._color_first)
            
            self.sh = sliderFloat.sliderFloat(self._chart_height, text='Chart height in pixels:', minvalue=20.0, maxvalue=800.0, maxint=780, showpercentage=False, decimals=0,
                                                   labelwidth=96, sliderwidth=140, resetbutton=True, showtooltip=True, onchange=self.changeH, color=self._color_first)
            
            self.configure_card.children = [widgets.VBox([PageConfigurator.label('Plotly chart', color='black'), self.sw.draw(), self.sh.draw()])]
            
        return self.configure_card

    
    @property
    def state(self):
        return {x: getattr(self, x) for x in ['content',
                                              'chart_width',
                                              'chart_height',
                                              'color_first',
                                              'color_second',
                                              'dark'
                                             ]}
        
    @state.setter
    def state(self, statusdict):
        for key, value in statusdict.items():
            setattr(self, key, value)
    