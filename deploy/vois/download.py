"""Utility functions for downloading text and binary files"""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright (C) 2022-2030 European Union (Joint Research Centre)
#
# This file is part of BDAP voilalibrary.
#
# voilalibrary is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# voilalibrary is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.

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
    
        from voilalibrary import download
        
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
    
        from voilalibrary import download
        
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
