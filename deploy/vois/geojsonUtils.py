"""Utility functions to manage geospatial vector data in geojson format."""
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
# limitations under the Licence.import json
import json

# Given a geojson string, returns a json object after having tested that the input string contains a valid geojson
def geojsonJson(geojson):
    """
    Given a geojson string, returns a json dictionary after having tested that the input string contains a valid geojson
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
            
    Returns
    -------
        Json dictionary
        
    Raises
    ------
        Exception if the input string is not in geojson format
    
    """
    j = json.loads(geojson)
    
    if j.get('type', None) != 'FeatureCollection':
        raise Exception('Sorry, input string does not look like GeoJSON')
        
    if type(j.get('features', None)) != list:
        raise Exception('Sorry, input string does not contains GeoJSON features')
        
    return j



# Load a geojson from file, testing that it contains a valid geojson
# Returns a string
def geojsonLoadFile(filepath):
    """
    Load a geojson content from file, testing that it contains valid geojson data
    
    Parameters
    ----------
        filepath : str
            File path of the geojson file to load
            
    Returns
    -------
        File content as a geojson string
        
    Example
    -------
    Load a geojson from file, print the geojson string::
    
        from vois import geojsonUtils
        
        geojson = geojsonUtils.geojsonLoadFile('./data/example.geojson')

        print(geojson)
        
    .. figure:: figures/geojsonLoad.png
       :scale: 100 %
       :alt: Geojson example geojsonLoadFile

       Read a geojson file and print its content

    """

    with open(filepath,"r") as f:
        geojson = f.read()

    j = geojsonJson(geojson)
    return json.dumps(j)



# Given a geojson string, returns the number of features
def geojsonCount(geojson):
    """
    Given a geojson string, returns the number of features
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
            
    Returns
    -------
        Integer corresponding to the number of features in the input geojson string
    """
    
    j = geojsonJson(geojson)
    return len(j['features'])


# Given a geojson string, returns the list of the attribute names of the features
def geojsonAttributes(geojson):
    """
    Given a geojson string, returns the list of the attribute names of the features
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
            
    Returns
    -------
        List of strings containing the names of the attributes of the features in the input geojson string

    Example
    -------
    Load a geojson from file and print the names of its attributes::
    
        from vois import geojsonUtils
        
        geojson = geojsonUtils.geojsonLoadFile('./data/example.geojson')

        print('Attributes = ', geojsonUtils.geojsonAttributes(geojson))
        
    .. figure:: figures/geojsonAttributes.png
       :scale: 100 %
       :alt: Geojson example geojsonAttributes

       Read a geojson file and print the names of its attributes
       
    """
    
    j = geojsonJson(geojson)
    
    features = j['features']
    attributes = set()
    for f in features:
        attributes.update(f['properties'].keys())
        
    return list(attributes)
    

# Given a geojson string, returns the list of values of the attribute attributeName for all the features
def geojsonAll(geojson, attributeName):
    """
    Given a geojson string, returns the list of values of the attribute attributeName for all the features
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
        attributeName : str
            Name of one of the attributes
            
    Returns
    -------
        List containing the values of the attribute for all the features of the input geojson dataset

    Example
    -------
    Load a geojson from file and print all the values of one if its attributes::
    
        from vois import geojsonUtils
        
        geojson = geojsonUtils.geojsonLoadFile('./data/example.geojson')

        print('Values = ', geojsonUtils.geojsonAll(geojson,'ha'))
        
    .. figure:: figures/geojsonAll.png
       :scale: 100 %
       :alt: Geojson example geojsonAll

       Read a geojson file and print the values of one of its attributes for all the features of the dataset
       
    """        
    
    j = geojsonJson(geojson)
    
    features = j['features']
    attributes = set()
    values = [f['properties'][attributeName] if attributeName in f['properties'] else None for f in features]
    return values


# Add a field to a geojson by joining a python dictionary through match with the field named keyname.
# If innerMode is True, the output geojson will only keep the joined features, otherwise all the original features are returned
# Returns the modified geojson
def geojsonJoin(geojson, keyname, addedfieldname, keytovaluedict, innerMode=False):
    """
    Add a field to a geojson by joining a python dictionary through match with the field named keyname.
    If innerMode is True, the output geojson will only keep the joined features, otherwise all the original features are returned
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
        keyname : str
            Name of the attribute of the input geojson to use as internal key for the join operation
        addedfieldname : str
            Name of the attribute to add to the input geojson as a result of the join operation
        keytovaluedict : dict
            Dictionary (key-value pairs) to use as joined values. The keys of the <keytovaluedict> are used as foreign keys to match the values of the <keyname> attribute of the input geojson. When a match is found, the attribute <addedfieldname> is added to the corresponding feature having the value read from the <keytovaluedict>
        innerMode : bool, optional
            If innerMode is True, the output geojson will only keep the successfully joined features, otherwise all the original features are returned
            
    Returns
    -------
        a string containing the modified geojson after the join operation
        
    Example
    -------
    Load a geojson from file, print some information on attributes and values of the features, then join the features with a dictionary::
    
        from vois import geojsonUtils
        
        # Load a geojson file
        geojson = geojsonUtils.geojsonLoadFile('./data/example.geojson')

        # Add a new field by joining with a dictionary (with innerMode flag set to True)
        keytovalue = { 37661: 'aaa', 37662: 'bbb'}
        geojsonnew = geojsonUtils.geojsonJoin(geojson,'id', 'value', keytovalue, innerMode=True)
        
        # Print the 'value' attribute values for the joined geojson dataset
        print('Joined values =', geojsonUtils.geojsonAll(geojsonnew,'value'))

    .. figure:: figures/geojsonJoin.png
       :scale: 100 %
       :alt: Geojson example

       Result of the Join operation
       
    """

    j = geojsonJson(geojson)

    # Feature collection to return
    res = {
        "type": "FeatureCollection",
        "features": []
    }

    if 'crs' in j:
        res['crs'] = j['crs']
        
    for f in j['features']:
        if 'properties' in f:
            if keyname in f['properties']:
                key = f['properties'][keyname]
                if key in keytovaluedict:
                    value = keytovaluedict[key]
                    f['properties'][addedfieldname] = value
                    if innerMode:
                        res['features'].append(f)
        if not innerMode:
            res['features'].append(f)
        
    return json.dumps(res)


# Filter a geojson by keeping only the features for which <fieldname> has value <fieldvalue> (fieldvalue can be also a list!)
# Returns the modified geojson
def geojsonFilter(geojson, fieldname, fieldvalue):
    """
    Filter a geojson by keeping only the features for which <fieldname> has value <fieldvalue> (fieldvalue can be also a list)
    
    Parameters
    ----------
        geojson : str
            String containing data in geojson format
        fieldname : str
            Name of one of the attributes of the input geojson
        fieldvalue : single value or list of values
            Comparison value. Only the input features having this value on the <fieldname> attribute are kept in the output geojson returned
            
    Returns
    -------
        a string containing the modified geojson containing only the features that pass the filter operation
    """        

    j = geojsonJson(geojson)

    # Feature collection to return
    res = {
        "type": "FeatureCollection",
        "features": []
    }

    if 'crs' in j:
        res['crs'] = j['crs']
        
    for f in j['features']:
        if 'properties' in f:
            if fieldname in f['properties']:
                fvalue = f['properties'][fieldname]
                if (type(fieldvalue) is list and fvalue in fieldvalue) or (fvalue == fieldvalue):
                    res['features'].append(f)
        
    return json.dumps(res)