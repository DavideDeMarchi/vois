"""Upload local image: dialog box with image preview"""
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
from vois import cssUtils, colors
from vois.vuetify import settings, upload, dialogGeneric, dialogWait

# Python imports
from PIL import Image


#####################################################################################################################################################
# Upload local image: dialog box with image preview
#####################################################################################################################################################
class UploadImage():
    
    # Initialization
    def __init__(self,
                 output,
                 message='Click to select image to upload',
                 label='Image:',
                 accept='image/png, image/jpeg, image/bmp',
                 title='Select an image',
                 color=settings.color_first,
                 dark=settings.dark_mode,
                 titleheight=40,
                 width=620,
                 onOK=None,                                       # Called passing the url string of the selected image or the empty string if no image is selected
                 onCancel=None):                                  # Called with no argument
        
        self.output       = output
        self.title        = title
        self.color        = color
        self.dark         = dark
        self.titleheight  = titleheight
        self.width        = width
        self.onOK         = onOK
        self.onCancel     = onCancel
        
        cssUtils.allSettings(self.output)
        
        self.image    = None
        self.imageurl = ''
        
        self.wait = None
        
        self.preview = widgets.Output(layout=Layout(height='600px'))
        self.u = upload.upload(accept=accept, label=label, onchanging=self.onFileSelected, onchange=self.onFileUpload, placeholder=message, multiple=False)

        spacerY = v.Html(tag='div', style_='width: 0px; height: 20px;')
        self.content = v.Card(flat=True, class_='pa-0, ma-0 mt-n4 ml-4 mr-4', children=[widgets.VBox([self.u.draw(), spacerY, self.preview])])
        
        
    # Open the dialog-box
    def show(self):
        self.preview.clear_output()
        self.u.clear()
        dialogGeneric.dialogGeneric(title=self.title, on_ok=self._internal_onOK, on_cancel=self._internal_onCancel, on_close=self.onCancel,
                                    text='   ', color=self.color, dark=self.dark, titleheight=self.titleheight, width=self.width,
                                    show=True, addclosebuttons=True, addokcancelbuttons=True,
                                    fullscreen=False, content=[self.content], output=self.output)
        
    # Just after the file is selected
    def onFileSelected(self):
        self.wait = dialogWait.dialogWait(text='Uploading file...', output=self.output, color=self.color, dark=self.dark)
        

    # Selection of an image to upload
    def onFileUpload(self, files):
        # If at least one file has been selected      
        if len(files) > 0:
            self.preview.clear_output()
            for f in files:
                self.image = Image.open(f['file_obj'])
                self.imageurl = colors.image2Base64(self.image)
                with self.preview:
                    display(v.Img(src=self.imageurl))

        # No files selected
        else:
            self.image    = None
            self.imageurl = ''
            self.preview.clear_output()
    
        if self.wait is not None:
            self.wait.close()
    
    
    # Selection done
    def _internal_onOK(self):
        if self.onOK is not None:
            self.onOK(self.imageurl)
    
    # Exit without selection
    def _internal_onCancel(self):
        if self.onCancel is not None:
            self.onCancel()
