"""Utility functions for the creation ipytrees from hierarchical data."""
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
from traitlets import Float
from ipytree import Tree, Node
from IPython.display import display
import pandas as pd
import numpy as np


##################################################################################################################################
# Creation of ipytree
##################################################################################################################################

# Node of the tree that stores a float value (Very slow!!!)
class DataNode(Node):
    value = Float(0.0)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
# Handle click on a node
def basic_handle_click(event):
    if event['new']:
        print(event.owner.value)

        
        
##################################################################################################################################
# Create a ipytree from a list of names with an implicit tree structure, example: ['JRC', 'JRC.D', 'JRC.D.3', ...]
# EXAMPLE:
# def pippo(event):
#     if event['new']:
#         print(event.owner.value)
#         
# tree, nodes, parent_of = createIpytreeFromList(['A','A.1','A.2','A.1.1'], rootName='A', valuefor={'A.1.1': 10.0}, handle_click=pippo)
# display(tree)
##################################################################################################################################
def createIpytreeFromList(nameslist=[], rootName='', separator='.', valuefor={}, handle_click=basic_handle_click, select_root=False):
    """
    Create a ipytree from a list of names with an implicit tree structure, example: ['JRC', 'JRC.D', 'JRC.D.3', ...]
    
    Parameters
    ----------
        nameslist : list of strings, optional
            List of strings that contain a hierarchical structure, considering the separator character (default is [])
        rootName: str, optional
            Name to be displayed as root of the tree (default is '')
        separator: str, optional
            String or character to be considered as separator for extracting the hierarchical structure from the nameslist list of strings (default is '.')
        valuefor : dict, optional
            Dictionary to assign a numerical value to each node of the tree (default is {})
        handle_click : function, optional
            Python function to call when the selected nodes change caused by user clicking (default is ipytree.basic_handle_click)
        select_root : bool, optional
            If True the root node is selected at start (default is False)
        
    Returns
    -------
        A tuple of 3 elements: the tree instance, a dict containing the info on the nodes, a dict containing the parent of each of the nodes
    
    
    Example
    -------
    Example of the creation of a ipytree from a list of strings with hierarchy defined by the '.' character::
    
        from vois import ipytrees
        
        def onclick(event):
            if event['new']:
                print(event.owner, event.owner.value)

        tree, n, p = ipytrees.createIpytreeFromList(['A','A.1','A.2',
                                                    'A.1.1','A.3.1',
                                                    'A.4.1.2','A.5.2.1',
                                                    'A.4.2.3.1','B','B.A'],
                                                    rootName='Directorates',
                                                    valuefor={'A.1.1': 10.0,
                                                              'A.3.1': 5.0},
                                                    handle_click=onclick)
        display(tree)
        
    .. figure:: figures/ipytree.png
       :scale: 100 %
       :alt: ipytrees example

       Ipytree produced by the example code
       
    """
    
    # Add a node to a tree-node
    def addNode(name, value, parent):
        nonlocal nodes, parent_of
        if not name in nodes:
            elem = DataNode(name, value=value)
            elem.open_icon_style  = 'info'
            elem.close_icon_style = 'info'
            elem.show_icon = False
            elem.opened = False
            elem.observe(handle_click, 'selected')
            parent.add_node(elem)
            nodes[name] = elem
            parent_of[name] = parent
            while parent != tree:
                parent.value += value
                parent = parent_of[parent.name]
            return elem
    
    nodes     = {}
    parent_of = {}
    tree = Tree(stripes=False)
    root = tree
    if len(rootName) > 0:
        root = addNode(rootName,0.0,tree)

    # Manage an implicit tree with separator!
    for name in nameslist:
        parts = name.split(separator)
        fullname = ''
        for part in parts:
            parentname = fullname
            if len(fullname) == 0: fullname += part
            else:                  fullname += '.' + part

            parent = root
            if parentname in nodes: parent = nodes[parentname]

            value = 0.0
            if fullname in valuefor: value = valuefor[fullname]
            addNode(fullname,value,parent)

    if rootName in nodes:            
        root = nodes[rootName]
        root.opened = True
        
        if select_root:
            root.selected = True
        
    return tree, nodes, parent_of
    
    
    
##################################################################################################################################
# Create a ipytree from two columns of a Dataframe. An optional third column containing a numeric value can be used
##################################################################################################################################
def createIpytreeFromDF2Columns(df, colindexLabels1, colindexLabels2, colindexValues=-1, rootName='', handle_click=basic_handle_click, select_root=False):
    """
    Create a two level ipytree from two columns of a Pandas DataFrame
    
    Parameters
    ----------
        df : Pandas DataFrame
            Input Pandas DataFrame
        colindexLabels1 : int
            Index of the column that contains the labels of the first level of the tree
        colindexLabels2 : int
            Index of the column that contains the labels of the second level of the tree
        colindexValues : int, optional
            Index of the column that contains the values for the nodes of the tree
        rootName: str, optional
            Name to be displayed as root of the tree (default is '')
        handle_click : function, optional
            Python function to call when the selected nodes change caused by user clicking (default is ipytree.basic_handle_click)
        select_root : bool, optional
            If True the root node is selected at start (default is False)
        
    Returns
    -------
        A tuple of 3 elements: the tree instance, a dict containing the info on the nodes, a dict containing the parent of each of the nodes
        
    """

    # Add a node to a tree-node
    def addNode(name, value, parent):
        nonlocal nodes, parent_of
        if not name in nodes:
            elem = DataNode(name, value=value)
            elem.open_icon_style  = 'info'
            elem.close_icon_style = 'info'
            elem.show_icon = False
            elem.opened = False
            elem.observe(handle_click, 'selected')
            parent.add_node(elem)
            nodes[name] = elem
            parent_of[name] = parent
            while parent != tree:
                parent.value += value
                parent = parent_of[parent.name]
            return elem
    
    nodes     = {}
    parent_of = {}
    tree = Tree(stripes=False)
    root = tree
    if len(rootName) > 0:
        root = addNode(rootName,0.0,tree)

    # Create the tree from two columns of a df
    for index,row in df.iterrows():
        parentname = str(row[colindexLabels1])
        name       = str(row[colindexLabels2])
        value = 0.0
        if colindexValues >= 0: value = float(row[colindexValues])

        addNode(parentname, 0.0, root)
        parent = nodes[parentname]
        addNode(name,value,parent)

    root.opened = True
    if select_root:
        root.selected = True

    return tree, nodes, parent_of



