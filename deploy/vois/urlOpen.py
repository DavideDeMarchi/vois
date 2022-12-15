"""Utility functions to open a web page."""
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.

from IPython.core.display import HTML as ipyhtml   # V. I. for urlOpen to work!!!

# Open a web page in another tab
def urlOpen(url, output, target='_blank'):
    """
    Opean a web page in another tab of the browser
    
    Parameters
    ----------
    url : str
        URL of the page to open
    output : instance of ipywidgets.Output() class
        Output widget where the javascript code to open the new page is executed
    target : str, optional
        Target of the open operation (default is '_blank' which means that the page will be opened in a new browser's tab)
        
    Example
    -------
    Open Google page in another tab of the browser::
    
        from voilalibrary import urlOpen
        from ipywidgets import widgets, Layout
        from IPython.display import display

        output = widgets.Output(layout=Layout(width='0px', height='0px'))
        display(output)
        
        urlOpen.urlOpen('https://www.google.com', output, target='_blank')
    
        
    Note
    ----
        If the dashboard is created using the :class:`app.app` class, it is preferable to use the function :func:`app.app.urlOpen` that doesn't need the output parameter and uses the Output widget created inside the app instance itself (and invisible to the users)
    
    """
    
    js = '''
<script type=\"text/javascript\">
window.open("%s", "%s");
</script>
''' % (url, target)
        
    with output:
        display(ipyhtml(js))
