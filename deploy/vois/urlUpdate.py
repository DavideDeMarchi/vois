"""Utility functions to update the URL of the page that launched the dashboard."""
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

        from voilalibrary import urlUpdate
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
