"""Read parameters passed in the URL of the Voila dashboard"""
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
    
        from vois.vuetify import queryStrings
        
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
