"""Read parameters passed in the URL of the Voila dashboard"""
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
# along with voilalibrary.  If not, see <https://www.gnu.org/licenses/>.from IPython.display import display

def readParameters():
    """
    Read parameters passed in the URL of the Voilà dashboard.
        
    Returns
    --------
    parameters : dictionary
        Dictionary containing key-values for all the URL passed to the Voilà page
        
    Example
    -------
    Read URL parameters and get value of one of the parameters::
    
        from voilalibrary.vuetify import queryStrings
        
        parameters = queryStrings.readParameters()
        activetab = parameters.get('activetab', ['chart'])[0]
        print(activetab)
        
    """
    import os
    import json
    run_in_voila = True
    try:
        from voila.utils import get_query_string
    except:
        run_in_voila = False

    from urllib.parse import parse_qs

    
    if run_in_voila:
        query_string = get_query_string()   # New in Voilà 0.3.0
    else:
        query_string = os.environ.get('QUERY_STRING', '')

    parameters = parse_qs(query_string)
    return parameters
