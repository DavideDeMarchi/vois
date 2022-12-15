"""Utility functions to open a web page."""
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
    
        from vois import urlOpen
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
