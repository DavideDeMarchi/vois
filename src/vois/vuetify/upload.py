"""Widget to upload files from the user local machine"""
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
from ipywidgets import widgets, Layout
from IPython.display import display, HTML

try:
    from . import settings
except:
    import settings

from vois.vuetify.extra import FileInput


#####################################################################################################################################################
# Upload file input
#####################################################################################################################################################
class upload():
    """
    Widget to upload files from the user local machine.
        
    Parameters
    ----------
    accept : str, optional
        String containing the comma separated list of mime types of files accepted for the upload operation (example: 'image/png, image/jpeg')
    label : str, optional
        Label displayed in the upper part of the widget (default is the empty string)
    placeholder : str, optional
        String that provides some guidance to the user (default is the empty string)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    width : str, optional
        Width of the control in pixels or in percentage (default is "100%")
    margins : str, optional
        Margins to apply to the widgets (default is "pa-0 ma-0")
    multiple : bool, optional
        Flag to enable multiple selection of files to upload (default is False)
    show_progress : bool, optional
        Flag to show a progress bar while uploading (default is True)
    onchange : function, optional
        Python function to call when the user has selected  one or more files to upload. The function will receive a parameter of type list containing the files to upload
    onchanging : function, optional
        Python function to call just after the user selects one or more files to upload. The function will receive no parameters
            
    Example
    -------
    Creation and display of a widget for the upload of images::
        
        from vois.vuetify import upload
        from IPython.display import display
        
        u = upload.upload(accept="image/png, image/jpeg, image/bmp",
                          label='Images',
                          placeholder='Click to select images to upload')
        display(u.draw())


    .. figure:: figures/upload.png
       :scale: 100 %
       :alt: upload widget

       Upload widget for selecting images to upload.
   """
    
    # Initialization
    def __init__(self, accept='', label='', placeholder='', color=settings.color_first,
                 width="100%", margins="pa-0 ma-0",
                 multiple=False, show_progress=True, onchange=None, onchanging=None):

        self._color     = color
        self.width      = width
        self.margins    = margins
        self.onchange   = onchange
        self.onchanging = onchanging
        
        self.file_input = FileInput(accept=accept, color=self._color, multiple=multiple, show_progress=show_progress, 
                                    label=label, placeholder=placeholder)
        
        self.container = v.Card(flat=True, style_="min-width: %s; width: %s;"%(self.width,self.width), class_=self.margins, children=[self.file_input])
        
        # If requested onchange management
        if not self.onchange is None:
            self.file_input.observe(self.__internal_on_file_upload, names='file_info')
        
        
    # Clear
    def clear(self):
        """Sets the widget to its initial state (no file selected)"""
        self.file_input.clear()
    
        
    # Manage onchange event
    def __internal_on_file_upload(self, change):
        if self.onchanging:
            self.onchanging()
            
        files = self.file_input.get_files()
        
        if self.onchange:
            self.onchange(files)
    
    # Returns the vuetify object to display
    def draw(self):
        """
        Returns the ipyvuetify object to display
        
        Example
        -------
        Display the upload widget::
        
            import upload
            u = upload.upload(accept="image/png, image/jpeg, image/bmp",
                              label='Images',
                              placeholder='Click to select images to upload')
            display(u.draw())
        """
        return v.Html(tag='div',children=[self.container], style_='overflow: hidden;')


    @property
    def color(self):
        """
        Get/Set the color of the upload widget
        
        Returns
        --------
        col : str
            Color of the upload widget

        Example
        -------
        Programmatically change the color::
            
            p.color = 'red'
            print(p.color)
        
        """
        return self._color
        
    @color.setter
    def color(self, col):
        self._color = col
        self.file_input.color = self._color
    