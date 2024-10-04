"""Upload local json file: dialog box to select and preview of some fields"""
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
    """
    Upload local json file: dialog box to select and preview of some fields. Widget that simplifies the selection of a json from the local computer to be uploaded in the cloud. It features the preview of one or more field of the json into a modal dialog-box.

    Parameters
    ----------
    output : ipywidgets.Output
        Output widget on which the widget has to be displayed
    message : str, optional
        Message to display in the upload widget to guide the user (default is 'Click to select the file to upload').
    label : str, optional
        Placeholder label displayed on top of the upload widget (default is 'File json:').
    accept : str, optional
        List of mime types accepted for the selection (default is 'application/json').
    title : str, optional
        Title of the modal dialog-box (default is 'Select a file').
    required_attributes : list of str, optional
        List of attribute names to check in selected json file and to display in the preview (default is [])
    attributes_width : int, optional
        Width in pixel of the space to display the required attributes names (default is 100)
    color : str, optional
        Main color of the widgets (default is settings.color_first).
    dark : bool, optional
        Dark flag (default is settings.dark_mode).
    titleheight : int, optional
        Height in pixels of the title bar of the modal dialog-box (default is 40)
    width : int, optional
        Width in pixels of the modal dialog-box (default is 800)
    height : int, optional
        height in pixels of the preview area of the modal dialog-box (default is 200)
    onOK : function, optional
        Python function to call when the user clicks on the OK button. The function will receive as parameter the json dictionary read from the selected file.
    onCancel : function, optional
        Python function to call when the user clicks on the CANCEL button. The function will receive no parameters.
    
    Example
    -------
    Display of a dialog-box to enable the user to select a json file from its local machine::
        
        from vois.vuetify import UploadJson
        from ipywidgets import widgets, Layout
        from IPython.display import display
        import ipyvuetify as v

        output = widgets.Output(layout=Layout(width='0px', height='0px'))
        display(output)

        debug = widgets.Output()

        def onSelectedJson(jsonitem):
            debug.clear_output()
            with debug:
                display(jsonitem)

        u = UploadJson.UploadJson(output,
                                  onOK=onSelectedJson,
                                  required_attributes=['appname', 'title'],
                                  attributes_width=80)
        u.show()

        display(debug)

    .. figure:: figures/upload_json_1.png
       :scale: 50 %
       :alt: Upload json dialog widget

       UploadImage dialog box before the selection of a json file
       
    .. figure:: figures/upload_json_2.png
       :scale: 50 %
       :alt: Upload dialog widget with a json file selected

       UploadJson dialog box showing the preview of some fields of the selected json file
    """
    
    # Initialization
    def __init__(self,
                 output,
                 message='Click to select the file to upload',
                 label='File json:',
                 accept='application/json',
                 title='Select a file',
                 required_attributes=[],         # List of attribute names to check in selected json file and to display in the preview
                 attributes_width=100,           # width in pixel of the spavce to display the required attributes names
                 color=None,
                 dark=None,
                 titleheight=40,
                 width=800,
                 height=200,
                 onOK=None,                      # Called passing the content of the selected file
                 onCancel=None):                 # Called with no argument
        
        self.output              = output
        self.title               = title
        self.required_attributes = required_attributes
        self.attributes_width    = attributes_width
        self.titleheight         = titleheight
        self.width               = width
        self.height              = height
        self.onOK                = onOK
        self.onCancel            = onCancel
        
        self.color = color
        if self.color is None:
            self.color = settings.color_first
            
        self.dark = dark
        if self.dark is None:
            self.dark = settings.dark_mode
            
        cssUtils.allSettings(self.output)
        
        self.json = None
        
        self.wait = None
        
        self.preview = widgets.Output(layout=Layout(height='%dpx'%self.height))
        self.u = upload.upload(accept=accept, label=label, onchanging=self.onFileSelected, onchange=self.onFileUpload, placeholder=message, multiple=False, color=self.color)

        spacerY = v.Html(tag='div', style_='width: 0px; height: 20px;')
        self.content = v.Card(flat=True, class_='pa-0, ma-0 mt-n4 ml-4 mr-4', children=[widgets.VBox([self.u.draw(), spacerY, self.preview])])
        
        
    # Open the dialog-box
    def show(self):
        """
        Opens the dialog-box.
        """
        self.preview.clear_output()
        self.u.clear()
        self.dlg = dialogGeneric.dialogGeneric(title=self.title, on_ok=self._internal_onOK, on_cancel=self._internal_onCancel, on_close=self.onCancel,
                                               text='   ', color=self.color, dark=self.dark, titleheight=self.titleheight, width=self.width,
                                               show=True, addclosebuttons=True, addokcancelbuttons=True,
                                               fullscreen=False, content=[self.content], output=self.output)
        self.dlg.okdisabled = True
        
        
    # Just after the file is selected
    def onFileSelected(self):
        self.wait = dialogWait.dialogWait(text='Uploading file...', output=self.output, color=self.color, dark=self.dark)

        
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
                                                addclosebuttons=True, show=True, width=400, output=self.output)
                    
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
