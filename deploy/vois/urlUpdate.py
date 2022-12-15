"""Utility functions to update the URL of the page that launched the dashboard."""
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
from IPython.display import display, HTML
            
# Update the visualized URL in the browser
def urlUpdate(url, output):
    """
    Update the URL visualized in the top bar of the browser.
    
    Parameters
    ----------
    url : str
        Partial url to add to the current browser's page key/values

    Example
    -------
    Add a key/value pair to the current browser URL::

        from vois import urlUpdate
        from ipywidgets import widgets, Layout
        from IPython.display import display

        output = widgets.Output(layout=Layout(width='0px', height='0px'))
        display(output)
        
        urlUpdate.urlUpdate('?test=3', output)
    
    Note
    ----
        If the dashboard is created using the :class:`app.app` class, it is preferable to use the function :func:`app.app.urlUpdate` that doesn't need the output parameter and uses the Output widget created inside the app instance itself (and invisible to the users)
    
    """
    js = "<script>window.history.replaceState({ additionalInformation: 'Updated the URL with JS' }, '', '%s');</script>" % url
    with output:
            display(HTML(js))
