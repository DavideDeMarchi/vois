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
    """
    Upload local image: dialog box with image preview. Widget that simplifies the selection of an image from the local computer to be uploaded in the cloud. It features the image selection and preview into a modal dialog-box.

    Parameters
    ----------
    output : ipywidgets.Output
        Output widget on which the widget has to be displayed
    message : str, optional
        Message to display in the upload widget to guide the user (default is 'Click to select image to upload').
    label : str, optional
        Placeholder label displayed on top of the upload widget (default is 'Image:').
    accept : str, optional
        List of mime types accepted for the selection (default is 'image/png, image/jpeg, image/bmp').
    title : str, optional
        Title of the modal dialog-box (default is 'Select an image').
    color : str, optional
        Main color of the widgets (default is settings.color_first).
    dark : bool, optional
        Dark flag (default is settings.dark_mode).
    titleheight : int, optional
        Height in pixels of the title bar of the modal dialog-box (default is 40)
    width : int, optional
        Width in pixels of the modal dialog-box (default is 620)
    height : int, optional
        height in pixels of the image preview area of the modal dialog-box (default is 600)
    onOK : function, optional
        Python function to call when the user clicks on the OK button. The function will receive as parameter the url string of the selected image or the empty string if no image is selected.
    onCancel : function, optional
        Python function to call when the user clicks on the CANCEL button. The function will receive no parameters.
    
    Example
    -------
    Display of a dialog-box to enable the user to select an image from its local machine::
        
        from vois.vuetify import UploadImage
        from ipywidgets import widgets, Layout
        from IPython.display import display
        import ipyvuetify as v

        output = widgets.Output(layout=Layout(width='0px', height='0px'))
        display(output)

        debug = widgets.Output()

        def onSelectedImage(imageurl):
            debug.clear_output()
            with debug:
                display(v.Img(class_='pa-0 ma-0 mr-2', src=imageurl))

        u = UploadImage.UploadImage(output, onOK=onSelectedImage)
        u.show()

        display(debug)

    .. figure:: figures/upload_image_1.png
       :scale: 50 %
       :alt: Upload dialog widget

       UploadImage dialog box before the selection of an image
       
    .. figure:: figures/upload_image_2.png
       :scale: 50 %
       :alt: Upload dialog widget with an image selected

       UploadImage dialog box showing the preview of the selected image
    """
    
    # Initialization
    def __init__(self,
                 output,
                 message='Click to select image to upload',
                 label='Image:',
                 accept='image/png, image/jpeg, image/bmp',
                 title='Select an image',
                 color=None,
                 dark=None,
                 titleheight=40,
                 width=620,
                 height=600,
                 onOK=None,          # Called passing the url string of the selected image or the empty string if no image is selected
                 onCancel=None):     # Called with no argument
        
        self.output       = output
        self.title        = title
        self.titleheight  = titleheight
        self.width        = width
        self.height       = height
        self.onOK         = onOK
        self.onCancel     = onCancel
        
        self.color = color
        if self.color is None:
            self.color = settings.color_first
            
        self.dark = dark
        if self.dark is None:
            self.dark = settings.dark_mode
        
        cssUtils.allSettings(self.output)
        
        self.image    = None
        self.imageurl = ''
        
        self.wait = None
        
        self.preview = widgets.Output(layout=Layout(height='%dpx'%self.height))
        self.u = upload.upload(accept=accept, label=label, onchanging=self.onFileSelected, onchange=self.onFileUpload, placeholder=message, multiple=False)

        spacerY = v.Html(tag='div', style_='width: 0px; height: 20px;')
        self.content = v.Card(flat=True, class_='pa-0, ma-0 mt-n4 ml-4 mr-4', children=[widgets.VBox([self.u.draw(), spacerY, self.preview])])
        
        
    # Open the dialog-box
    def show(self):
        """
        Opens the dialog-box.
        """
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
