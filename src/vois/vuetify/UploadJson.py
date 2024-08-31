"""Upload local json file: dialog box to select and previw of some fields"""
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
from vois.vuetify import settings, upload, dialogGeneric, dialogMessage, dialogWait

# Python imports
import json


# Creation of a label
def label(text, class_='pa-0 ma-0 mt-1 mr-3', size=14, weight=400, color=settings.color_first, width=None):
    lab = v.Html(tag='div', children=[text], class_=class_)
    if width is None:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s;'%(size,weight,color)
    else:
        lab.style_ = 'font-size: %dpx; font-weight: %d; color: %s; width: %dpx'%(size,weight,color,int(width))
    return lab


#####################################################################################################################################################
# Upload local json file: dialog box to select and previw of some fields
#####################################################################################################################################################
class UploadJson():
    
    # Initialization
    def __init__(self,
                 output,
                 message='Click to select the file to upload',
                 label='File',
                 accept='application/json',
                 title='Select a file',
                 required_attributes=[],         # List of attribute names to check in selected json file and to display in the preview
                 attributes_width=100,           # width in pixel of the spavce to display the required attributes names
                 color=settings.color_first,
                 dark=settings.dark_mode,
                 titleheight=40,
                 width=800,
                 onOK=None,                      # Called passing the content of the selected file
                 onCancel=None):                 # Called with no argument
        
        self.output              = output
        self.title               = title
        self.required_attributes = required_attributes
        self.attributes_width    = attributes_width
        self.color               = color
        self.dark                = dark
        self.titleheight         = titleheight
        self.width               = width
        self.onOK                = onOK
        self.onCancel            = onCancel
        
        cssUtils.allSettings(self.output)
        
        self.json = None
        
        self.wait = None
        
        self.preview = widgets.Output(layout=Layout(height='200px'))
        self.u = upload.upload(accept=accept, label=label, onchanging=self.onFileSelected, onchange=self.onFileUpload, placeholder=message, multiple=False)

        spacerY = v.Html(tag='div', style_='width: 0px; height: 20px;')
        self.content = v.Card(flat=True, class_='pa-0, ma-0 mt-n4 ml-4 mr-4', children=[widgets.VBox([self.u.draw(), spacerY, self.preview])])
        
        
    # Open the dialog-box
    def show(self):
        self.preview.clear_output()
        self.u.clear()
        self.dlg = dialogGeneric.dialogGeneric(title=self.title, on_ok=self._internal_onOK, on_cancel=self._internal_onCancel, on_close=self.onCancel,
                                               text='   ', color=self.color, dark=self.dark, titleheight=self.titleheight, width=self.width,
                                               show=True, addclosebuttons=True, addokcancelbuttons=True,
                                               fullscreen=False, content=[self.content], output=self.output)
        self.dlg.okdisabled = True
        
        
    # Just after the file is selected
    def onFileSelected(self):
        self.wait = dialogWait.dialogWait(text='Uploading file...', output=self.output)

        
    # Selection of an image to upload
    def onFileUpload(self, files):
        # If at least one file has been selected      
        if len(files) > 0:
            
            self.preview.clear_output()
            for f in files:
                self.json = json.load(f['file_obj'])
                
                # Check the presence of the required attributes
                attributesOK = True
                for a in self.required_attributes:
                    if a not in self.json:
                        attributesOK = False
                        break
                        
                if attributesOK:
                    self.dlg.okdisabled = False
                    with self.preview:
                        for a in self.required_attributes:
                            display(widgets.HBox([label(a+':', color='black', width=self.attributes_width), label(self.json[a], color='black', weight=600)]))
                        
                else:
                    dialogMessage.dialogMessage(title='Error',
                                                text='The uploaded file has no %s attribute'%a,
                                                addclosebuttons=False, show=True, width=400, output=self.output)
                    
                    self.dlg.okdisabled = True
                    self.json = None
                    self.preview.clear_output()
                    
        # No files selected
        else:
            self.json = None
            self.preview.clear_output()

        if self.wait is not None:
            self.wait.close()
    
    
    # Selection done
    def _internal_onOK(self):
        if self.onOK is not None:
            self.onOK(self.json)
    
    # Exit without selection
    def _internal_onCancel(self):
        if self.onCancel is not None:
            self.onCancel()
