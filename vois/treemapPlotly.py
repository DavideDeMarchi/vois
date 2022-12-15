"""Utility functions to prepare data for Plotly Treemap, Sunburst and Icicle plots."""
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

##################################################################################################################################
# Creation of a plotly treemap
##################################################################################################################################

# Node class to construct the treemap: stores a name and a float value
class TreemapNode():
    
    def __init__(self, name, value=0.0):
        self.name  = name
        self.value = value
        
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
    

##################################################################################################################################
# Creation of Treemap to be displayed with Plotly
##################################################################################################################################

##################################################################################################################################
# Create a treemap from a list of names with an implicit tree structure, example: ['JRC', 'JRC.D', 'JRC.D.3', ...]
# Returns 3 lists to be input to Plotly treemap: labels, parents, values!
# The values for intermediate nodes are calculated automatically
#
# Example:
# valuefor = {'A.1.1': 10.0, 'A.2': 5.0}
# labels, parents, values = createTreemapFromList(['A','A.1','A.2','A.1.1'], rootName='A', valuefor=valuefor)
#
# import plotly.graph_objects as go
# fig = go.Figure()
# fig.add_trace(go.Treemap(ids=labels, labels=labels, parents=parents, values=values, branchvalues='total', maxdepth=3, root_color="lightgrey"))
# fig.add_trace(go.Sunburst(ids=labels, labels=labels, parents=parents, values=values, branchvalues='total', maxdepth=3, root_color="lightgrey"))
# fig.show()
##################################################################################################################################
def createTreemapFromList(nameslist=[], rootName='Root', separator='.', valuefor={}):
    """
    Preprocessing of a list of strings having a hierarchical structure (defined by a separator, e.g. '.'), in view of the display of a Plotly Treemap, Sunburst or Icicle chart. Each node of the tree will have a 'dimension' that influences the way to display it (the space occupied, or the size, etc.)
    
    Parameters
    ----------
    nameslist : list of strings, optional
        List of strings to preprocess. The hierarchical structure is defined by the separator character. Default is []
    rootName : str, optional
        Name to assign to the root node of the hierarchical structure (default is 'Root')
    separator : str, optional
        Separator character that defines the hierarchical structure (default is '.')
    valuefor : dict, optional
        Dictionary to assign a numerical value to each node of the tree (default is {})
        
        
    Return
    ------
        a tuple of 3 elements: labels, parents, values
        labels is a list of the names of the nodes
        parents is the list of the parents of each of the nodes
        values is the list of numerical values assigned to each of the node (and summed up in the parent-son relation)
        These 3 lists can be given as input to the plotly.graph_objects.Treemap/Sunburst/Icicle functions
    
    Example
    -------
    Creation of a Treemap chart in Plotly using numerical data associated to JRC units and directorates::
    
        import plotly.graph_objects as go
        from vois import treemapPlotly

        valuefor = {'JRC.A.1': 3.0, 'JRC.A.2': 5.0, 'JRC.B.1': 12.0, 'JRC.B.2': 7.0,
                    'JRC.B.3': 3.0, 'JRC.C.1': 7.0, 'JRC.C.2': 2.0}

        labels, parents, values = treemapPlotly.createTreemapFromList(['JRC.A','JRC.A.1',
                                                                       'JRC.A.2','JRC.B.1',
                                                                       'JRC.B.2','JRC.B.3',
                                                                       'JRC.C.1','JRC.C.2',],
                                                                      rootName='JRC',
                                                                      valuefor=valuefor)

        fig = go.Figure()
        fig.add_trace(go.Treemap(ids=labels, labels=labels, parents=parents, values=values,
                                 branchvalues='total', maxdepth=3, root_color="lightgrey"))
        fig.update_layout(margin=dict(t=38, l=0, r=0, b=10), height=400,
                          hoverlabel=dict(bgcolor="#eee", align="left"),
                          title={'text': "JRC units", 'y':0.96, 'x':0.5, 
                                 'xanchor': 'center', 'yanchor': 'top'})

        fig.show()    
    
    .. figure:: figures/treemap.png
       :scale: 100 %
       :alt: treemap example

       Display of a Plotly Treemap extracted from a list of strings separated by '.'
       
    """

    # Add a node to a tree-node
    def addNode(name, value, parent):
        nonlocal nodes, parent_of
        if not name in nodes:
            elem = TreemapNode(name, value=value)

            nodes[name] = elem
            parent_of[name] = parent
            
            while parent != None:
                parent.value += value
                parent = parent_of[parent.name]
                
            return elem
    
    nodes     = {}
    parent_of = {}

    root = addNode(rootName,0.0,None)

    # Manage an implicit tree with separator!
    for name in nameslist:
        parts = name.split(separator)
        fullname = ''
        for part in parts:
            parentname = fullname
            if len(fullname) == 0: fullname += part
            else:                  fullname += separator + part

            parent = root
            if parentname in nodes: parent = nodes[parentname]

            value = 0.0
            if fullname in valuefor: value = valuefor[fullname]
            addNode(fullname,value,parent)

    #return nodes, parent_of

    labels  = []
    parents = []
    values  = []
    for key, value in nodes.items():
        labels.append(key)
        pname = str(parent_of[key])
        if pname == 'None':    parents.append(None)
        else:                  parents.append(pname)
        values.append(value.value)

    return labels, parents, values
