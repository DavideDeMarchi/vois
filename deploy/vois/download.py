"""Utility functions for downloading text and binary files"""
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

from ipywidgets import widgets, Layout
from IPython.display import display, HTML
import base64


# Output widget that needs to be visualized inside the notebook in order for the download to work!!!
output = widgets.Output(layout=Layout(width='0px', min_width='0px', height='0px', min_height='0px'))


# Direct download of a .txt file containing a string
def downloadText(textobj, fileName="download.txt"):
    """
    Download of a string as a text file.
    
    Parameters
    ----------
        textobj : str
            Text to be written in the text file to be downloaded
        fileName : str, optional
            Name of the file to download (default is "download.txt")
            
    Example
    -------
    In order to download a text file, the Output widget download.output must be displayed inside the notebook. This is required because the download operation is based on the execution of Javascript code, and this requires an Output widget displayed. After the download.output widget is visible, then the download.downloadText function can be called::
    
        from vois import download
        
        display(download.output)
        
        with download.output:
            download.downloadText('aaa bbb ccc')
    
    """

    string_bytes  = textobj.encode("ascii","ignore")
    base64_bytes  = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")

    output.clear_output()
    with output:
        display(HTML('\
<script>function downloadURI(uri, name) \
{\
    var link = document.createElement("a");\
    link.download = name;\
    link.href = uri;\
    link.click();\
}\
downloadURI("data:application/octet-stream;charset=utf-8;base64,' + base64_string + '","' + fileName + '");\
</script>'))

    output.clear_output()
        

# Direct download of an array of bytes
def downloadBytes(bytesobj, fileName="download.bin"):
    """
    Download of an array of bytes as a binary file.
    
    Parameters
    ----------
        bytesobj : bytearray or bytes object
            Bytes to be written in the binary file to be downloaded
        fileName : str, optional
            Name of the file to download (default is "download.bin")
            
    Example
    -------
    In order to download a binary file, the Output widget download.output must be displayed inside the notebook. This is required because the download operation is based on the execution of Javascript code, and this requires an Output widget displayed. After the download.output widget is visible, then the download.downloadBytes function can be called::
    
        from vois import download
        
        display(download.output)
        
        with download.output:
            download.downloadBytes(bytearray(b'ajgh lkjhl '))
    
    """

    base64_bytes  = base64.b64encode(bytesobj)
    base64_string = base64_bytes.decode("ascii")

    output.clear_output()
    with output:
        display(HTML('''
<script>function downloadURI(uri, name)
{
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    link.click();
}
downloadURI("data:application/octet-stream;charset=utf-8;base64,''' + base64_string + '","' + fileName + '");</script>'))
        
    output.clear_output()
