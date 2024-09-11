"""Example of image display to use inside a Content"""
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
from ipywidgets import widgets, HTML, Layout
import ipyvuetify as v
import pandas as pd
import random

# Vois imports
from vois.vuetify import settings, Button, UploadImage
from vois.templates import PageConfigurator


#####################################################################################################################################################
# Example of image display to use inside a Content
#####################################################################################################################################################
class Image():
    
    def __init__(self,
                 output,
                 width='30vw',        # Dimensions of the image
                 height='40vh',
                 color_first=None,    # Main color
                 color_second=None,   # Secondary color
                 dark=None,           # Dark flag
                 imageurl='',         # Image to display
                 **kwargs):
        
        self.output = output
        
        self._width    = width
        self._height   = height
        self._imageurl = imageurl
        
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

        # Create the card that will contain the image
        self.card = v.Card(flat=True, tile=True, width=self._width, height=self._height,
                           style_='overflow: hidden;', class_='d-flex align-center justify-center')  # The content of the card is centered horizontally and vertically
        
        self.img = v.Img(src=self._imageurl, contain=True, width=self._width, height=self._height, position='center center')
        
        self.tf = None
        self.b  = None
        
        self.card.children = [self.img]
        
        
    # Draw th widget
    def draw(self):
        return self.card
    
    # Called when an image is selected
    def onImageSelected(self, imageurl):
        self.imageurl = imageurl
        
        
    # Selection of an image
    def onSelectImage(self, *args):
        upload = UploadImage.UploadImage(self.output, width=620)
        upload.title   = 'Select image to display'
        upload.onOK    = self.onImageSelected
        upload.color   = self._color_first
        upload.u.color = self._color_first
        upload.dark    = self._dark
        upload.show()
        
    # Changed image URL in the self.tf TextField
    def onChangedURL(self, *args):
        if self.tf.v_model is None:
            url = ''
        else:
            url = self.tf.v_model
        self.imageurl = url

        
    # Configure the SVG drawing
    def configure(self):
        
        self.tf = v.TextField(label='Image URL:', autofocus=False, v_model=None, dense=False, color=self._color_first, clearable=True, class_="pa-0 ma-0 mt-3 mb-1")
        self.tf.on_event('change', self.onChangedURL)
        
        self.b  = Button('Upload image from local computer', color_selected=self._color_first, dark=self._dark, 
                         text_weight=450, on_click=self.onSelectImage, width=300, height=40,
                         tooltip='Click to select an image to upload from you local computer', selected=True,
                         rounded=False)
        
        return v.Card(flat=True, class_='pa-2 ma-0', children=[widgets.VBox([PageConfigurator.label('Image', color='black'), self.tf, self.b])])


    @property
    def content(self):
        return 'Image'
        
    @content.setter
    def content(self, c):
        pass
    
    
    @property
    def width(self):
        return self._width
        
    @width.setter
    def width(self, w):
        self._width = w
        self.card.width = w
        self.img.width = w

        
    @property
    def height(self):
        return self._height
        
    @height.setter
    def height(self, h):
        self._height = h
        self.card.height = h
        self.img.height = h

        
    @property
    def imageurl(self):
        return self._imageurl
        
    @imageurl.setter
    def imageurl(self, url):
        self._imageurl = url
        self.img.src = self._imageurl
        
        
    @property
    def color_first(self):
        return self._color_first
        
    @color_first.setter
    def color_first(self, color):
        self._color_first = color

        if self.b is not None:
            self.b.color_selected = self._color_first
            
        if self.tf is not None:
            self.tf.color = self._color_first

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
    def state(self):
        return {x: getattr(self, x) for x in ['content',
                                              #'width',      # Will inherit from content!!!
                                              #'height',
                                              'imageurl',
                                              'color_first',
                                              'color_second',
                                              'dark'
                                             ]}
        
    @state.setter
    def state(self, statusdict):
        for key, value in statusdict.items():
            setattr(self, key, value)