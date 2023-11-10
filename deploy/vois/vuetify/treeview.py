"""Simplified creation of v-treeview vuetify widget to display hierarchical data in a tree"""
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
import traitlets
import ipyvuetify as v
from ipywidgets import widgets, Layout, HTML
from IPython.display import display
import pandas as pd
import copy

try:
    from . import settings
except:
    import settings


##################################################################################################################################
# Creation of ipyvuetify Treeview
##################################################################################################################################

##################################################################################################################################
# Customized Treeview created using VuetifyTemplate
# The nodes of the tree can have a checkbox (selectable=True) and/or can be activated (activatable=True)
# The height of each node is reduced, the font is smaller and the paddings/margins are reduced
# See last cell of https://github.com/mariobuikhuizen/ipyvuetify/blob/master/examples/Examples.ipynb
##################################################################################################################################
class CustomTreeview(v.VuetifyTemplate):
    """
    Ipyvuetify template to display a custom treeview. The nodes of the tree can have a checkbox (selectable=True) and/or can be activated (activatable=True).

    Attributes
    ----------
    items : list, optional
        JSON object to represent the tree: each object has 'id' and 'name' key, 'disabled', 'isfolder' and 'icon' are optional keys (default is [])
    selectable: bool, optional
        If True the nodes of the tree have a checkbox to select them (default is True)
    activatable: bool, optional
        If True, one of the nodes of the tree can be activated (default is False)
    selected: list, optional
        List of id of the nodes that are selected on start (default is [])
    selectednames: list, optional
        List of name of the nodes that are selected at any time (default is [])
    opened: list, optional
        List of id of the nodes that are to be opened on start (default is [])
    color: str, optional
        Color for the selected nodes (default is 'blue')
    on_change: function, optional
        Python function to call when the selection of the tree items changes (default is None)
    on_activated: function, optional
        Python function to call when the active item changes (user selecting a node) (default is None)
    expand_selection_to_parents: bool, optional
        If True, also the parent nodes are returned as selected when all children are selected (default is True)
    iconsshow : bool, optional
        If True, an icon is added to each node of the tree (default is False)
    iconscolor : str, optional
        Color of the icons (default is 'blue')
    icons_folder_opened : str, optional
        Name of the icon to use for opened nodes that have children when iconsfolder is True (default 'mdi-folder-open')
    icons_folder_closed : str, optional
        Name of the icon to use for closed nodes that have children when iconsfolder is True (default 'mdi-folder')
    tooltips : bool, optional
        If True the nodes will show the tooltip (default is False)
    tooltips_chars : int, optional
        Minimum lenght of the node label to show the tooltip (default is 20)
    search : str, optional
        Filter to display only the nodes of the tree that contain the text (default is '' which means that all the nodes of the tree are displayed)
    item_height : int, optional
        Item height in pixels (default is 24)
    font_size : int, optional
        Font size in pixels (default is 15)
    icon_size : int, optional
        Icon size in pixels (default is 18)
    checkbox_size : int, optional
        Checkbox size in pixels (default is 24)
        
    Note
    ----
    This class is not intended to be called directly, but only through the functions :func:`~treeview.createTreeviewFromList` and :func:`~treeview.createTreeviewFromDF2Columns`.
    """
    
    items                       = traitlets.Any([]).tag(sync=True)                       # JSON object to represent the tree (each object has 'id' and 'name' key. 'disabled' is an optional key)
    selectable                  = traitlets.Bool(True).tag(sync=True)                    # If True the nodes of the tree have a checkbox to select them
    activatable                 = traitlets.Bool(False).tag(sync=True)                   # If True, one the nodes of the tree can be activated
    open_on_click               = traitlets.Bool(False).tag(sync=True)                   # If True, the nodes can be opened by clicking on the label
    active                      = traitlets.Any(None).tag(sync=True)                     # Id of the node that is active at start
    selected                    = traitlets.Any([]).tag(sync=True)                       # List of id of the nodes that are selected on start
    selectednames               = traitlets.Any([]).tag(sync=True)                       # List of name of the nodes that are selected at any time
    opened                      = traitlets.Any([]).tag(sync=True)                       # List of id of the nodes that are to be opened on start
    color                       = traitlets.Unicode('blue').tag(sync=True)               # Color for the selected nodes
    dark                        = traitlets.Bool(False).tag(sync=True)                   # If True show text in white
    transition                  = traitlets.Bool(False).tag(sync=True)                   # If True applies a transition when nodes are opened and closed
    on_change                   = traitlets.Any(None).tag(sync=False)                    # Name of a python function to call when the selected nodes change (user clicking in one of the checkboxes)
    on_activated                = traitlets.Any(None).tag(sync=False)                    # Name of a python function to call when the active node changes (user selecting a node)
    expand_selection_to_parents = traitlets.Bool(True).tag(sync=True)                    # If True, also the parent nodes are returned as selected when all children are selected
    search                      = traitlets.Unicode('').tag(sync=True)                   # Search string to filter the nodes
    opened_all                  = traitlets.Bool(False).tag(sync=True)                   # If True all the nodes are opened at start
    
    
    @traitlets.default('template')
    def _template(self):

        # Code to add to activate the icons
        # if item.isfolder is True, the open/closed icon is added, else the item.icon is added
        icons_template = ''
        if self.iconsshow:
            icons_template = '''
<template v-slot:prepend="{ item, open }">
      <v-icon color="%s" :disabled="item.disabled" v-if="item.isfolder">
         {{ open ? '%s' : '%s' }}
      </v-icon>
      <v-icon color="%s" :disabled="item.disabled" v-else-if="item.icon">
         {{ item.icon }}
      </v-icon>
      <v-html v-else>
      </v-html>
</template>
''' % (self.iconscolor, self.icons_folder_opened, self.icons_folder_closed, self.iconscolor)


        # Code to add to activate the tooltip
        tooltip_template = ''
        if self.tooltips:
            tooltip_template = '''
<template v-slot:label="{ item }">
    <v-tooltip bottom :disabled="item.name.length < %d">
      <template v-slot:activator="{ on, attrs }">
        <span v-bind="attrs" v-on="on">
           {{ item.name }}
        </span>
      </template>
      {{ item.name }}
    </v-tooltip>
</template>
''' % self.tooltips_chars

            
        return '''
<v-treeview 
    :selectable="selectable"
    :activatable="activatable"
    :active="[active]"
    hoverable
    dense
    :dark="dark"
    :transition="transition"
    class="pa-0 ma-0"
    :items="items"
    v-model="selected"
    :search="search"
    :open="opened"
    :open-all="opened_all"
    :color="color"
    :selected-color="color"
    :open-on-click="open_on_click"
    @input="change_selection"
    @update:active="activate"
    @update:open="onopening">
    %s
    %s
</v-treeview>

<style id="treeview-item-style">

.vuetify-styles .v-treeview-node__root {
    padding-left: 0px;
    padding-right: 0px;
}
.vuetify-styles .v-treeview--dense .v-treeview-node__root {
    min-height: %dpx;
    font-size: %dpx;
}
.vuetify-styles .v-application--is-ltr .v-treeview-node__checkbox {
    margin-left: 0px;
    margin-right: 0px;
}

.vuetify-styles .v-treeview-node__checkbox {
    width: %dpx;
}
.vuetify-styles .v-icon.v-icon {
    font-size: %dpx;
}

</style>
''' % (tooltip_template, icons_template, self.item_height, self.font_size, self.checkbox_size, self.icon_size)
    
    
    # Expand the selection to parents that have all childrens selected
    def expandSelectionToParents(self, node):
        if 'children' in node:
            sel = True
            for n in node['children']:
                self.expandSelectionToParents(n)
                if n['id'] not in self.selected: sel = False
            if sel and not node['id'] in self.selected:
                self.selected.append(node['id'])
    
    
    # Transform a list of id in a list of fullnames
    def id2Names_selected(self, node, idlist):
        if node['id'] in idlist: self.selectednames.add(node['fullname'])
        if 'children' in node:
            for n in node['children']:
                self.id2Names_selected(n,idlist)

    # Return the fullname given the id
    def id2Name(self, node, id):
        if node['id'] == id:
            return node['fullname']
        if 'children' in node:
            for n in node['children']:
                res = self.id2Name(n,id)
                if not res is None:
                    return res

                
    # Updates self.selectednames with the selected nodes
    def updateSelectedNames(self):
        if self.expand_selection_to_parents:
            for i in self.items:
                self.expandSelectionToParents(i)
        self.selected.sort()
        self.selectednames = set()
        for i in self.items:
            self.id2Names_selected(i,self.selected)
        self.selectednames = sorted(list(self.selectednames))
    
    # Manage event "input": when a checkbox of the tree is clicked
    def vue_change_selection(self, data):
        #print(data)
        self.selected = data
        if self.selectable and not self.on_change is None:
            self.updateSelectedNames()
            self.on_change(self.selectednames)
            
    # Manage the activation (selection) of a node of the tree
    def vue_activate(self, data):
        if len(data) > 0:
            self.current_active = data[0]
            if self.activatable and not self.on_activated is None:
                for i in self.items:
                    name = self.id2Name(i,data[0])
                    if not name is None:
                        self.on_activated(name)
                        break
        else:
            self.current_active = None
            if self.activatable and not self.on_activated is None:
                self.on_activated(None)

    # Called every time a node is opened or closed
    def vue_onopening(self, data):
        self.current_open = data
                
            
    # Initialization
    def __init__(self,
                 items                       = [],
                 selectable                  = True,
                 activatable                 = False,
                 open_on_click               = False,
                 active                      = None,
                 selected                    = [],
                 selectednames               = [],
                 opened                      = [],
                 color                       = 'blue',
                 dark                        = False,
                 transition                  = False,
                 on_change                   = None,
                 on_activated                = None,
                 expand_selection_to_parents = True,
                 search                      = '',
                 opened_all                  = False,
                 item_height                 = 24,     # Item height in pixels
                 font_size                   = 15,     # Font size in pixels
                 icon_size                   = 18,     # Icon size in pixels
                 checkbox_size               = 24,     # Checkbox size in pixels
                 
                 iconsshow=False,
                 iconscolor='blue',
                 icons_folder_opened='mdi-folder-open',
                 icons_folder_closed='mdi-folder',
                 tooltips=False,
                 tooltips_chars=20,
                 *args,
                 **kwargs):
        
        self.items                       = items
        self.selectable                  = selectable
        self.activatable                 = activatable
        self.open_on_click               = open_on_click
        self.active                      = active
        self.selected                    = selected
        self.selectednames               = selectednames
        self.opened                      = opened
        self.color                       = color
        self.dark                        = dark
        self.transition                  = transition
        self.on_change                   = on_change
        self.on_activated                = on_activated
        self.expand_selection_to_parents = expand_selection_to_parents
        self.search                      = search
        self.opened_all                  = opened_all
        
        self.item_height                 = item_height      # Item height in pixels
        self.font_size                   = font_size        # Font size in pixels
        self.icon_size                   = icon_size        # Icon size in pixels
        self.checkbox_size               = checkbox_size    # Checkbox size in pixels
        
        self.current_active = active
        self.current_open   = []
        
        self.iconsshow = iconsshow
        self.iconscolor = iconscolor
        self.icons_folder_opened = icons_folder_opened
        self.icons_folder_closed =icons_folder_closed
        self.tooltips = tooltips
        self.tooltips_chars = tooltips_chars
        super().__init__(*args, **kwargs)
        
        

##################################################################################################################################
# Helper class to operate on a treeview returned by the createTreeviewFromList or createTreeviewFromDF2Columns functions
##################################################################################################################################
class treeviewOperations():
    """
    Helper class to operate on a treeview returned by the :func:`~treeview.createTreeviewFromList` and :func:`~treeview.createTreeviewFromDF2Columns` functions. 
    This class allows for activation and opening/closing of nodes of the tree
    
    Attributes
    ----------
    treecard : instance of ipyvuetify Card widget
        Value returned by a call to the functions :func:`~treeview.createTreeviewFromList` and :func:`~treeview.createTreeviewFromDF2Columns`.
        
    
    Example
    -------
    Creation and display of a treeview and programmatical activation and opening of the nodes::
        
        from vois.vuetify import treeview
        from IPython.display import display
        
        treecard = treeview.createTreeviewFromList(['A','A.1','A.2','A.1.1',
                                                    'A.3.1','A.4.1.2','A.5.2.1',
                                                    'A.4.2.3.1','B','B.A'],
                                                   rootName='Root', 
                                                   activatable=True,
                                                   expand_selection_to_parents=False, 
                                                   substitutionDict={'A.1': 'A.1 new name'},
                                                   color='green',
                                                   height=350)
        display(treecard)
        
        top = treeview.treeviewOperations(treecard)
        
        # Print active node
        print(top.getActive())
        
        # Set active node
        top.setActive('A.1.1')
        
        # Set the list of opened nodes
        top.setOpened(['Root', 'A', 'A.3'])
        
    """
    
    # Initialisation
    def __init__(self, treecard):
        
        # Retrieve the underlying instance of CustomTreeview class
        self.treeview = treecard.children[0].children[0]
        
        self.doindex()

    
    # calculate indexing of the treeview nodes
    def doindex(self):
        # Dictionaries to index the three nodes
        # id2fullname    Map nodes id to the fullname                 # key: id           value : fullname of the node
        # fullname2id    Map nodes fullname to the id                 # key: fullname     value : id of the node
        # id2parentid    Map node id to the id of the parent node     # key: id           value : id of the parent node
        # id2childrenid  Map node id to the list of children ids      # key: id           value : list of id of the children nodes
        self.id2fullname   = {}
        self.fullname2id   = {}
        self.id2parentid   = {}
        self.id2childrenid = {}
        for i in self.treeview.items:
            self.__indexItems(i)
        
        
    # Internal recursive function to create the indexing of the treeview nodes
    def __indexItems(self,node):
        self.id2fullname[node['id']]       = node['fullname']
        self.fullname2id[node['fullname']] = node['id']
        if 'children' in node:
            self.id2childrenid[node['id']] = []
            for n in node['children']:
                self.id2parentid[n['id']] = node['id']
                self.id2childrenid[node['id']].append(n['id'])
                self.__indexItems(n)
        

    # Get the fullnames of the opened nodes
    def getOpened(self):
        """
        Returns the list of the fullnames of the opened nodes of the treeview
        """
        #fullnames = [self.id2fullname[x] for x in self.treeview.opened]
        fullnames = [self.id2fullname[x] for x in self.treeview.current_open]
        return fullnames

    
    # Set the nodes opened given a list of fullnames of the nodes
    def setOpened(self, fullnames):
        """
        Set the list of opened nodes of the treeview given their fullnames
        """
        ids = list(set([self.fullname2id[x] for x in fullnames]))
        self.treeview.opened = ids

        
    # Get the fullnames of the selected nodes
    def getSelected(self):
        """
        Returns the list of the fullnames of the selected nodes of the treeview
        """
        fullnames = [self.id2fullname[x] for x in self.treeview.selected]
        return fullnames
        
        
    # Set the nodes selected given a list of fullnames of the nodes
    def setSelected(self, fullnames):
        """
        Set the list of selected nodes of the treeview given their fullnames
        """
        ids = list(set([self.fullname2id[x] for x in fullnames]))
        self.treeview.selected = ids
        
        
    # Open all the nodes of the tree
    def openAll(self):
        """
        Open all the nodes of the treeview
        """
        allfullnames = list(self.fullname2id.keys())
        self.setOpened(allfullnames)

        
    # Get the fullname of the active node
    def getActive(self):
        """
        Returns the fullname of the node that is active in the treeview
        """
        nodeid = self.treeview.current_active
        if not nodeid is None:
            return self.id2fullname[nodeid]
        return None

    
    # Set the active node by passing its fullname
    def setActive(self, fullname):
        """
        Set the active node of the treeview by passing its fullname
        """
        if fullname in self.fullname2id:
            nodeid = self.fullname2id[fullname]
            self.treeview.active = nodeid
            self.treeview.current_active = nodeid
            
            # Opens all the parent nodes
            idparents = []
            while not nodeid is None:
                if nodeid in self.id2parentid:
                    nodeid = self.id2parentid[nodeid]
                    if not nodeid is None:
                        idparents.append(nodeid)
                else:
                    nodeid = None
            if not 1 in idparents:
                idparents.append(1)
            
            op = set(self.treeview.opened + idparents)
            self.treeview.opened = list(op)
            
            
    # Given the fullname of a node, returns the fullname of its first child, or None if the node has no children
    def getFirstChildFullname(self, fullname):
        """
        Given the fullname of a node, returns the fullname of its first child, or None if the node has no children
        """
        if fullname in self.fullname2id:
            nodeid = self.fullname2id[fullname]
            if nodeid in self.id2childrenid:
                return self.id2fullname[self.id2childrenid[nodeid][0]]
        return None
    
    
    # Search for a text in the nodes of the tree
    def setSearch(self, text2search=''):
        """
        Search for a text string in the nodes of the tree
        """
        self.treeview.search = text2search

        
    # Retrieve the children of a node
    def getChildren(self, nodefullname):
        """
        Returns the list of full names of the children of a node
        """
        
        # Recursive function
        def __getchildren(node, nodeid):
            if node['id'] == nodeid:
                if 'children' in node:
                    return [x['id'] for x in node['children']]

            if 'children' in node:
                for n in node['children']:
                    res = __getchildren(n, nodeid)
                    if len(res) > 0:
                        return res
            return []
        
        if nodefullname in self.fullname2id:
            nodeid = self.fullname2id[nodefullname]
            res = __getchildren(self.treeview.items[0],nodeid)
            return [self.id2fullname[x] for x in res]
        
        return []
        
        
        
    # Dynamic setting of children to nodes
    def setChildren(self, nodefullname, childrenfullnames):
        """
        Dynamically change the children of a node

        Example
        -------
        Creation and display of a treeview and programmatically add children to nodes::
        
            from vois.vuetify import treeview
            from IPython.display import display

            treecard = treeview.createTreeviewFromList(['A','A.1','A.2','B'],
                                                       separator='.',
                                                       rootName='Root',
                                                       expand_selection_to_parents=False, 
                                                       color='green',
                                                       width='500px',
                                                       height='350px',
                                                       selectable=False,
                                                       activatable=True)

            display(treecard)
            
            top = treeview.treeviewOperations(treecard)
            
            top.setChildren('A.2', ['A.2.1', 'A.2.2'])

        """
        
        # Recursive function
        def __setchildren(node, nodeid, children):
            if node['id'] == nodeid:
                node['children'] = children

            if 'children' in node:
                for n in node['children']:
                    __setchildren(n, nodeid, children)
        
        if nodefullname in self.fullname2id:
            nodeid = self.fullname2id[nodefullname]
            nextid = 1 + max(self.id2fullname.keys())
            children = []
            for name in childrenfullnames:
                c = {'id': nextid, 'name': name, 'fullname': name}
                children.append(c)
                nextid += 1
            
            root = copy.deepcopy(self.treeview.items[0])
            __setchildren(root, nodeid, children)
            self.treeview.items = [root]
            self.doindex()
    
    
##################################################################################################################################
# Create a ipyvuetify Treeview from a list of names with an implicit tree structure, example: ['JRC', 'JRC.D', 'JRC.D.3', ...]
# Returns an ipyvuetify widget containing the tree
# Example:
# createTreeviewFromList(['A','A.1','A.2','A.1.1'], rootName='A')
##################################################################################################################################
def createTreeviewFromList(nameslist=[],
                           rootName='Root',
                           separator='.', 
                           select_all=True,
                           on_change=None,
                           on_activated=None,
                           expand_selection_to_parents=True,
                           displayfullname=True,
                           width='200px', height='500px',
                           elevation=0,
                           repeat_parent_as_first_child=False,
                           substitutionDict=None,
                           color=settings.color_first,
                           dark=settings.dark_mode,
                           transition=False,
                           selectable=True,
                           activatable=False,
                           active=None,
                           open_on_click=False,
                           opened=[],
                           opened_all=False,
                           selected=[],
                           disabled=[],
                           iconsshow=False,
                           iconscolor=settings.color_first,
                           iconsfolder=True,
                           icons_folder_opened='mdi-folder-open',
                           icons_folder_closed='mdi-folder',
                           iconroot=None,
                           iconsDict=None,
                           tooltips=False,
                           tooltips_chars=20,
                           item_height=24,
                           font_size=15,
                           icon_size=18,
                           checkbox_size=24):
    """
    Create a treeview form a list of strings and a separator that defines the hierarchical structure (example: ['A', 'A.1', 'A.2', 'B', 'B.3']).

    Parameters
    ----------
    nameslist : list, optional
        List of strings that contain a hierarchical structure, considering the separator character (default is [])
    rootName : str, optional
        Name to be displayed as root of the tree (default is 'Root')
    separator : str, optional
        String or character to be considered as separator for extracting the hierarchical structure from the nameslist list of strings (default is '.')
    select_all : bool, optional
        Flag to control the initial selection of all the nodes of the tree (default is True)
    on_change : function, optional
        Python function to call when the selected nodes change caused by user clicking in one of the checkboxes (default is None)
    on_activated : function, optional
        Python function to call when the active item changes (user selecting a node) (default is None)
    expand_selection_to_parents : bool, optional
        If True, also the parent nodes are returned as selected when all children are selected (default is True)
    displayfullname : bool, optional
        If True the nodes will display the full names, id False only the last part splitted by the separator (default is True)
    width : str, optional
        Width of the treeview widget (default is '200px')
    height : str, optional
        Height of the treeview widget (default is '500px')
    elevation : int, optional
        Elevation to assign to the widget (default is 0)
    repeat_parent_as_first_child : bool, optional
        If True each parent node will have a first children with its name (default is False)
    substitutionDict: dict, optional
        Dictionary to apply substitutions to the fullnames of the items extracted from the nameslist parameters (default is None)
    color : str, optional
        Color to be used as main color of the Treeview widget (default is settings.color_first)
    dark : bool, optional
        If True, the treeview widget will have a dark background (default is settings.dark_mode)
    transition : bool, optional
        If True applies a transition when nodes are opened and closed (default is False)
    selectable : bool, optional
        If True the nodes of the tree have a checkbox to select them (default is True)
    activatable : bool, optional
        If True, one of the nodes of the tree can be activated (default is False)
    active : str, optional
        Name of the node to activate on start (default is None)
    open_on_click : bool, optional
        If True, the nodes of the tree can be opened also by clicking on the node label (default is False)
    opened : list of str, optional
        List of names of the nodes to open at start (default is [])
    opened_all : bool, optional
        If True, all the tree nodes are opened at start (default is False). This setting has prevalence over the opened parameter.
    selected : list of str, optional
        List of fullnames of the nodes to select at start (default is []).
    disabled : list of str, optional
        List of fullnames of the nodes to display as disabled in the tree (default is [])
    iconsshow : bool, optional
        If True, an icon is added to each node of the tree (default is False)
    iconscolor : str, optional
        Color of the icons (default is settings.color_first)
    iconsfolder : bool, optional
        If True (and if iconsshow is True) it adds the open/closed folder icon to nodes that have children (default is True)
    icons_folder_opened : str, optional
        Name of the icon to use for opened nodes that have children when iconsfolder is True (default 'mdi-folder-open')
    icons_folder_closed : str, optional
        Name of the icon to use for closed nodes that have children when iconsfolder is True (default 'mdi-folder')
    iconroot : str, optional
        Name of the icon for the root node of the tree (default is None)
    iconsDict: dict, optional
        Dictionary to apply icons to the fullnames of the items, if iconsshow is True (default is None)
    tooltips : bool, optional
        If True the nodes will show the tooltip (default is False)
    tooltips_chars : int, optional
        Minimum lenght of the node label to show the tooltip (default is 20)
    item_height : int, optional
        Item height in pixels (default is 24)
    font_size : int, optional
        Font size in pixels (default is 15)
    icon_size : int, optional
        Icon size in pixels (default is 18)
    checkbox_size : int, optional
        Checkbox size in pixels (default is 24)

    Returns
    -------
    v.Card: ipyvuetify Card widget
        An ipyvuetify v.Card widget having a v.Html as its only child. The v.Html has a treeview.CustomTreeview widget as its only child

    Example
    -------
    Creation and display of a treeview::
    
        from vois.vuetify import treeview
        from IPython.display import display
        
        treecard = treeview.createTreeviewFromList(['A','A.1','A.2','A.1.1',
                                                    'A.3.1','A.4.1.2','A.5.2.1',
                                                    'A.4.2.3.1','B','B.A'], 
                                                   rootName='Root', 
                                                   expand_selection_to_parents=False, 
                                                   substitutionDict={'A.1': 'A.1 new name'},
                                                   color='green',
                                                   height='350px')
        display(treecard)

    .. figure:: figures/treeview1.png
       :scale: 100 %
       :alt: treeview widget

       Treeview widget created from a list of strings.
    """
    
    # Return the string to display in the tree for a node, given its fullname
    def GetNodeString(fullname):
        if displayfullname:
            return fullname
        else:
            parts = fullname.split(separator)
            if len(parts) > 0:
                return parts[-1]
            return fullname
        

    # Add a new node to the tree
    def addNode(name, parent):
        nonlocal nextid, nodes, names2id
        if not name in nodes:
            elemname = name
            if not substitutionDict is None:
                if elemname in substitutionDict:
                    elemname = substitutionDict[elemname]
            elem = {'id': nextid, 'name': GetNodeString(elemname), 'fullname': elemname }
            if name in disabled: elem['disabled'] = True
            if not iconsDict is None:
                if elemname in iconsDict:
                    elem['icon'] = iconsDict[elemname]
            names2id[elemname] = nextid
            nextid += 1
            nodes[name] = elem
            if parent != None:
                if not 'children' in parent:
                    parent['children'] = []
                    
                    if repeat_parent_as_first_child and parent['name'] != rootName:
                        firstelem = {'id': nextid, 'name': GetNodeString(parent['name']), 'fullname': parent['name'] }
                        if parent['name'] in disabled: firstelem['disabled'] = True
                        names2id[parent['name']] = nextid
                        nextid += 1
                        parent['children'].append(firstelem)
                    
                parent['children'].append(elem)
                if iconsshow and iconsfolder: parent['isfolder'] = True
                
            return elem
    
    nextid = 1
    nodes  = {}
    names2id = {}  # Convert a fullname to its id

    root = addNode(rootName,None)

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

            addNode(fullname,parent)

    # Returns the list of all the ids of the children of node
    def calculateIdsOfLeaves(node, listofids):
        if not 'children' in node:
            listofids.append(node['id'])
        else:
            for n in node['children']:
                listofids = calculateIdsOfLeaves(n,listofids)
        return listofids
    
    selectedids = []
    if select_all: selectedids = calculateIdsOfLeaves(root,[])
    else:          selectedids = [names2id[x] for x in selected if x in names2id]
    
    
    # Convert opened names to ids
    openedids = []
    if not opened_all:
        if len(opened) == 0: openedids = [1]  # Only Root is opened by default
        else:                openedids = [names2id[x] for x in opened if x in names2id]

    # Convert active name to id
    if not active is None:
        activeid = names2id[active]
    else:
        activeid = None
    
    tree = CustomTreeview(items=[root], selected=selectedids, opened=openedids, on_change=on_change, on_activated=on_activated, 
                          expand_selection_to_parents=expand_selection_to_parents, dark=dark, transition=transition, opened_all=opened_all, 
                          color=color, selectable=selectable, activatable=activatable, active=activeid, open_on_click=open_on_click,
                          tooltips=tooltips, tooltips_chars=tooltips_chars,
                          iconsshow=iconsshow, iconscolor=iconscolor, icons_folder_opened=icons_folder_opened, icons_folder_closed=icons_folder_closed,
                          item_height=item_height, font_size=font_size, icon_size=icon_size, checkbox_size=checkbox_size)
    treehtml = v.Html(tag='div', height=height, children=[tree], style_='overflow: hidden;')
    treecard = v.Card(width=width, height=height, elevation=elevation, children=[treehtml],
                      dark=dark, style_='overflow-x: visible;')
    
    return treecard




##################################################################################################################################
# Create a flat ipyvuetify Treeview from a list of names
# Returns an ipyvuetify widget containing the tree
# Example:
# createFlatTreeview(['A','B','C','D'])
##################################################################################################################################
def createFlatTreeview(nameslist=[],
                       select_all=True,
                       on_change=None,
                       on_activated=None,
                       displayfullname=True,
                       width='200px', height='500px',
                       elevation=0,
                       color=settings.color_first,
                       dark=settings.dark_mode,
                       transition=False,
                       selectable=True,
                       activatable=False,
                       active=None,
                       selected=[],
                       disabled=[],
                       iconsshow=False,
                       iconscolor=settings.color_first,
                       iconsDict=None,
                       tooltips=False,
                       tooltips_chars=20,
                       item_height=24,
                       font_size=15,
                       icon_size=18,
                       checkbox_size=24):
    """
    Create a flat treeview form a list of strings

    Parameters
    ----------
    nameslist : list, optional
        List of strings that contain a hierarchical structure, considering the separator character (default is [])
    select_all : bool, optional
        Flag to control the initial selection of all the nodes of the tree (default is True)
    on_change : function, optional
        Python function to call when the selected nodes change caused by user clicking in one of the checkboxes (default is None)
    on_activated : function, optional
        Python function to call when the active item changes (user selecting a node) (default is None)
    displayfullname : bool, optional
        If True the nodes will display the full names, id False only the last part splitted by the separator (default is True)
    width : str, optional
        Width of the treeview widget (default is '200px')
    height : str, optional
        Height of the treeview widget (default is '500px')
    elevation : int, optional
        Elevation to assign to the widget (default is 0)
    color : str, optional
        Color to be used as main color of the Treeview widget (default is settings.color_first)
    dark : bool, optional
        If True, the treeview widget will have a dark background (default is settings.dark_mode)
    transition : bool, optional
        If True applies a transition when nodes are opened and closed (default is False)
    selectable : bool, optional
        If True the nodes of the tree have a checkbox to select them (default is True)
    activatable : bool, optional
        If True, one of the nodes of the tree can be activated (default is False)
    active : str, optional
        Name of the node to activate on start (default is None)
    selected : list of str, optional
        List of fullnames of the nodes to select at start (default is []).
    disabled : list of str, optional
        List of fullnames of the nodes to display as disabled in the tree (default is [])
    iconsshow : bool, optional
        If True, an icon is added to each node of the tree (default is False)
    iconscolor : str, optional
        Color of the icons (default is settings.color_first)
    iconsDict: dict, optional
        Dictionary to apply icons to the fullnames of the items, if iconsshow is True (default is None)
    tooltips : bool, optional
        If True the nodes will show the tooltip (default is False)
    tooltips_chars : int, optional
        Minimum lenght of the node label to show the tooltip (default is 20)
    item_height : int, optional
        Item height in pixels (default is 24)
    font_size : int, optional
        Font size in pixels (default is 15)
    icon_size : int, optional
        Icon size in pixels (default is 18)
    checkbox_size : int, optional
        Checkbox size in pixels (default is 24)

    Returns
    -------
    v.Card: ipyvuetify Card widget
        An ipyvuetify v.Card widget having a v.Html as its only child. The v.Html has a treeview.CustomTreeview widget as its only child

    Example
    -------
    Creation and display of a treeview::
    
        from vois.vuetify import treeview
        from IPython.display import display
        
        treecard = treeview.createFlatTreeview(['A','B','C','D','E'], color='green', height='150px')
        display(treecard)

    .. figure:: figures/treeview4.png
       :scale: 100 %
       :alt: flat treeview widget

       Flat treeview widget created from a list of strings.
    """
    
    
    nextid = 1
    roots = []
    names2id = {}
    for name in nameslist:
        elem = {'id': nextid, 'name': name, 'fullname': name}
        if name in disabled: elem['disabled'] = True
        if not iconsDict is None:
            if name in iconsDict:
                elem['icon'] = iconsDict[name]
        roots.append(elem)
        names2id[name] = nextid
        nextid += 1

    selectedids = []
    if select_all: selectedids = [(x+1) for x in range(nextid)]
    else:          selectedids = [names2id[x] for x in selected if x in names2id]
    
    # Convert active name to id
    if not active is None:
        activeid = names2id[active]
    else:
        activeid = None
    
    tree = CustomTreeview(items=roots, selected=selectedids, on_change=on_change, on_activated=on_activated, 
                          expand_selection_to_parents=False, dark=dark, transition=transition, 
                          color=color, selectable=selectable, activatable=activatable, active=activeid, 
                          tooltips=tooltips, tooltips_chars=tooltips_chars,
                          iconsshow=iconsshow, iconscolor=iconscolor,
                          item_height=item_height, font_size=font_size, icon_size=icon_size, checkbox_size=checkbox_size)
    treehtml = v.Html(tag='div', height=height, children=[tree], style_='overflow: hidden;')
    treecard = v.Card(width=width, height=height, elevation=elevation, children=[treehtml],
                      dark=dark, style_='overflow-x: visible;')
    
    return treecard



##################################################################################################################################
# UTILITY FUNCTIONS FOR CREATING THE TREE
##################################################################################################################################

# Add a node to the tree
def addNode(name, parent, icon,
            iconsshow, iconsfolder,
            repeat_parent_as_first_child, rootName, separator,
            nextid, fullnamenodes, fullnames2id,
            disabled):

    # Calculates the fullname of a node
    def getFullname(name, parent):
        if parent: return parent['fullname'] + separator + name
        else:      return name
            
    fullname = getFullname(name,parent)
        
    if fullname in fullnamenodes:
        return fullnamenodes[fullname], nextid, fullnamenodes, fullnames2id
    else:
        elem = {'id': nextid, 'name': name, 'fullname': fullname }
        if (not icon is None) and (len(icon) > 0): elem['icon'] = icon
        if fullname in disabled: elem['disabled'] = True
                
        fullnamenodes[fullname] = elem
        fullnames2id[fullname] = nextid
        nextid += 1
        if parent != None:
            if not 'children' in parent:
                parent['children'] = []
                    
                if repeat_parent_as_first_child and parent['name'] != rootName:
                    firstelem = {'id': nextid, 'name': parent['name'], 'fullname': getFullname(parent['name'],parent) }
                    if parent['fullname'] in disabled: firstelem['disabled'] = True
                    fullnames2id[firstelem['fullname']] = nextid
                    nextid += 1
                    parent['children'].append(firstelem)
                    
            parent['children'].append(elem)
            if iconsshow and iconsfolder: parent['isfolder'] = True
        return elem, nextid, fullnamenodes, fullnames2id

    
# Given a node: returns 
def calculateIdsOfLeaves(node, listofids=[]):
    if not 'children' in node:
        listofids.append(node['id'])
    else:
        for n in node['children']:
            listofids = calculateIdsOfLeaves(n,listofids)
    return listofids
    

    
##################################################################################################################################
# Create a ipyvuetify Treeview from two columns of a DataFrame
# Returns an ipyvuetify widget containing the tree
# Example:
# createTreeviewFromDF2Columns(df, 'col1', 'col2', rootName='A')
##################################################################################################################################
def createTreeviewFromDF2Columns(df,
                                 columnName1,
                                 columnName2,
                                 rootName='Root',
                                 separator='.',
                                 select_all=True,
                                 on_change=None,
                                 on_activated=None,
                                 expand_selection_to_parents=True,
                                 width='200px', height='500px',
                                 elevation=0,
                                 repeat_parent_as_first_child=False,
                                 color=settings.color_first,
                                 dark=settings.dark_mode,
                                 transition=False,
                                 selectable=True,
                                 activatable=False,
                                 active=None,
                                 open_on_click=False,
                                 opened=[],
                                 opened_all=False,
                                 selected=[],
                                 disabled=[],
                                 iconsshow=False,
                                 iconscolor=settings.color_first,
                                 iconsfolder=True,
                                 icons_folder_opened='mdi-folder-open',
                                 icons_folder_closed='mdi-folder',
                                 iconroot=None,
                                 iconscolumnName1=None,
                                 iconscolumnName2=None,
                                 tooltips=False,
                                 tooltips_chars=20,
                                 item_height=24,
                                 font_size=15,
                                 icon_size=18,
                                 checkbox_size=24):
    """
    Create a two levels treeview form the strings contained in two columns of a Pandas DataFrame.

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame containing at least two columns of type string
    columnName1 : str
        Name of the column of the Pandas DataFrame df containing the parent strings
    columnName2 : str
        Name of the column of the Pandas DataFrame df containing the child strings
    rootName : str, optional
        Name to be displayed as root of the tree (default is 'Root')
    separator : str, optional
        String or character to be considered as separator for calculating the fullname of a node (default is '.'). The full name of a node is the concatenation of the path to reach the node, using the separator character
    select_all : bool, optional
        Flag to control the initial selection of all the nodes of the tree (default is True)
    on_change : function, optional
        Python function to call when the selected nodes change caused by user clicking in one of the checkboxes (default is None). The function receives as argument a list of all the fullnames of the selected nodes
    on_activated : function, optional
        Python function to call when the active item changes (user selecting a node) (default is None)
    expand_selection_to_parents : bool, optional
        If True, also the parent nodes are returned as selected when all children are selected (default is True)
    width : str, optional
        Width of the treeview widget (default is '200px')
    height : int, optional
        Height of the treeview widget (default is '500px')
    elevation : int, optional
        Elevation to assign to the widget (default is 0)
    repeat_parent_as_first_child : bool, optional
        If True each parent node will have a first children with its name (default is False)
    color : str, optional
        Color to be used as main color of the Treeview widget (default is settings.color_first)
    dark : bool, optional
        If True, the treeview widget will have a dark background (default is settings.dark_mode)
    transition : bool, optional
        If True applies a transition when nodes are opened and closed (default is False)
    selectable : bool, optional
        If True the nodes of the tree have a checkbox to select them (default is True)
    activatable : bool, optional
        If True, one of the nodes of the tree can be activated (default is False)
    active : str, optional
        Fullname of the node to activate on start (default is None). The full name of a node is the concatenation of the path to reach the node, using the separator character
    open_on_click : bool, optional
        If True, the nodes of the tree can be opened also by clicking on the node label (default is False)
    opened : list of str, optional
        List of fullnames of the nodes to open at start (default is []). The full name of a node is the concatenation of the path to reach the node, using the separator character
    opened_all : bool, optional
        If True, all the tree nodes are opened at start (default is False). This setting has prevalence over the opened parameter.
    selected : list of str, optional
        List of fullnames of the nodes to select at start (default is []). The full name of a node is the concatenation of the path to reach the node, using the separator character
    disabled : list of str, optional
        List of fullnames of the nodes to display as disabled in the tree (default is [])
    iconsshow : bool, optional
        If True, an icon is added to each node of the tree (default is False)
    iconscolor : str, optional
        Color of the icons (default is settings.color_first)
    iconsfolder : bool, optional
        If True (and if iconsshow is True) it adds the open/closed folder icon to nodes that have children (default is True)
    icons_folder_opened : str, optional
        Name of the icon to use for opened nodes that have children when iconsfolder is True (default 'mdi-folder-open')
    icons_folder_closed : str, optional
        Name of the icon to use for closed nodes that have children when iconsfolder is True (default 'mdi-folder')
    iconroot : str, optional
        Name of the icon for the root node of the tree (default is None)
    iconscolumnName1 : str, optional
        Name of the DataFrame column that contains the icon name for the node on the first level of the tree (default is None)
    iconscolumnName2 : str, optional
        Name of the DataFrame column that contains the icon name for the node on the second level of the tree (default is None)
    tooltips : bool, optional
        If True the nodes will show the tooltip (default is False)
    tooltips_chars : int, optional
        Minimum lenght of the node label to show the tooltip (default is 20)
    item_height : int, optional
        Item height in pixels (default is 24)
    font_size : int, optional
        Font size in pixels (default is 15)
    icon_size : int, optional
        Icon size in pixels (default is 18)
    checkbox_size : int, optional
        Checkbox size in pixels (default is 24)

    Returns
    -------
    v.Card
        An ipyvuetify v.Card widget having a v.Html as its only child. The v.Html has a treeview.CustomTreeview widget as its only child

    Example
    -------
    Creation of a treeview from a simple Pandas DataFrame::
    
        from vois.vuetify import treeview
        import pandas as pd

        table = [['parent', 'child'], ['John', 'Mary'], ['John', 'Peter'], 
                                      ['Ann', 'Hellen'], ['Ann', 'Sue'], ['Ann', 'Claire']]
        headers = table.pop(0)
        df = pd.DataFrame(table, columns=headers)
        display(df)
        
        def on_change(arg):
            print(arg)
            
        treecard = treeview.createTreeviewFromDF2Columns(df, headers[0], headers[1], 
                                                         rootName='Families',
                                                         on_change=on_change)
        display(treecard)
        
    .. figure:: figures/treeview2.png
       :scale: 100 %
       :alt: treeview widget

       Treeview widget created from a Pandas DataFrame.
    """

    nextid = 1          # id of the next node
    fullnamenodes = {}  # All the nodes inserted, key is the fullname of the node
    fullnames2id  = {}  # Convert a fullname to its id
    
    if len(rootName) == 0: rootName = 'Root'
    root, nextid, fullnamenodes, fullnames2id = addNode(rootName,None,iconroot, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)

    # Create the tree from two columns of a df
    for index,row in df.iterrows():
        parentname = str(row[columnName1])
        name       = str(row[columnName2])

        parenticon = None
        if iconsshow and (not iconscolumnName1 is None) and (iconscolumnName1 in row): parenticon = str(row[iconscolumnName1])
        parent, nextid, fullnamenodes, fullnames2id = addNode(parentname, root, parenticon, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)
        
        icon = None
        if iconsshow and (not iconscolumnName2 is None) and (iconscolumnName2 in row): icon = str(row[iconscolumnName2])
        elem, nextid, fullnamenodes, fullnames2id = addNode(name,parent,icon, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)

        
    # List of selected ids
    selectedids = []
    if select_all: selectedids = calculateIdsOfLeaves(root)
    else:          selectedids = [fullnames2id[x] for x in selected if x in fullnames2id]
        
        
    # Convert opened fullnames to ids
    openedids = []
    if not opened_all:
        if len(opened) == 0: openedids = [1]  # Only Root is opened by default
        else:                openedids = [fullnames2id[x] for x in opened if x in fullnames2id]
        
    # Convert active fullname to id
    if not active is None and active in fullnames2id:
        activeid = fullnames2id[active]
    else:
        activeid = None
    
    #import json
    #print(json.dumps(root, indent=4))
    
    tree = CustomTreeview(items=[root], selected=selectedids, opened=openedids, on_change=on_change, on_activated=on_activated, 
                          expand_selection_to_parents=expand_selection_to_parents, dark=dark, transition=transition, opened_all=opened_all, 
                          color=color, selectable=selectable, activatable=activatable, active=activeid, open_on_click=open_on_click,
                          tooltips=tooltips, tooltips_chars=tooltips_chars,
                          iconsshow=iconsshow, iconscolor=iconscolor, icons_folder_opened=icons_folder_opened, icons_folder_closed=icons_folder_closed,
                          item_height=item_height, font_size=font_size, icon_size=icon_size, checkbox_size=checkbox_size)
            
    treehtml = v.Html(tag='div',height=height, children=[tree], style_='overflow: hidden;')
    treecard = v.Card(width=width, height=height, elevation=elevation, children=[treehtml],
                      dark=dark, style_='overflow-x: visible;')
    
    return treecard


##################################################################################################################################
# Create a ipyvuetify Treeview from three columns of a DataFrame
# Returns an ipyvuetify widget containing the tree
# Example:
# createTreeviewFromDF3Columns(df, 'col1', 'col2', 'col3', rootName='A')
##################################################################################################################################
def createTreeviewFromDF3Columns(df,
                                 columnName1,
                                 columnName2,
                                 columnName3,
                                 rootName='Root',
                                 separator='.',
                                 select_all=True,
                                 on_change=None,
                                 on_activated=None,
                                 expand_selection_to_parents=True,
                                 width='200px', height='500px',
                                 elevation=0,
                                 repeat_parent_as_first_child=False,
                                 color=settings.color_first,
                                 dark=settings.dark_mode,
                                 transition=False,
                                 selectable=True,
                                 activatable=False,
                                 active=None,
                                 open_on_click=False,
                                 opened=[],
                                 opened_all=False,
                                 selected=[],
                                 disabled=[],
                                 iconsshow=False,
                                 iconscolor=settings.color_first,
                                 iconsfolder=True,
                                 icons_folder_opened='mdi-folder-open',
                                 icons_folder_closed='mdi-folder',
                                 iconroot=None,
                                 iconscolumnName1=None,
                                 iconscolumnName2=None,
                                 iconscolumnName3=None,
                                 tooltips=False,
                                 tooltips_chars=20,
                                 item_height=24,
                                 font_size=15,
                                 icon_size=18,
                                 checkbox_size=24):
    """
    Create a three levels treeview form the strings contained in three columns of a Pandas DataFrame.

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame containing at least two columns of type string
    columnName1 : str
        Name of the column of the Pandas DataFrame df containing the parent strings
    columnName2 : str
        Name of the column of the Pandas DataFrame df containing the child strings
    columnName3 : str
        Name of the column of the Pandas DataFrame df containing the sub-child strings
    rootName : str, optional
        Name to be displayed as root of the tree (default is 'Root')
    separator : str, optional
        String or character to be considered as separator for calculating the fullname of a node (default is '.'). The full name of a node is the concatenation of the path to reach the node, using the separator character
    select_all : bool, optional
        Flag to control the initial selection of all the nodes of the tree (default is True)
    on_change : function, optional
        Python function to call when the selected nodes change caused by user clicking in one of the checkboxes (default is None). The function receives as argument a list of all the fullnames of the selected nodes
    on_activated : function, optional
        Python function to call when the active item changes (user selecting a node) (default is None)
    expand_selection_to_parents : bool, optional
        If True, also the parent nodes are returned as selected when all children are selected (default is True)
    width : str, optional
        Width of the treeview widget (default is '200px')
    height : int, optional
        Height of the treeview widget (default is '500px')
    elevation : int, optional
        Elevation to assign to the widget (default is 0)
    repeat_parent_as_first_child : bool, optional
        If True each parent node will have a first children with its name (default is False)
    color : str, optional
        Color to be used as main color of the Treeview widget (default is settings.color_first)
    dark : bool, optional
        If True, the treeview widget will have a dark background (default is settings.dark_mode)
    transition : bool, optional
        If True applies a transition when nodes are opened and closed (default is False)
    selectable : bool, optional
        If True the nodes of the tree have a checkbox to select them (default is True)
    activatable : bool, optional
        If True, one of the nodes of the tree can be activated (default is False)
    active : str, optional
        Fullname of the node to activate on start (default is None). The full name of a node is the concatenation of the path to reach the node, using the separator character
    open_on_click : bool, optional
        If True, the nodes of the tree can be opened also by clicking on the node label (default is False)
    opened : list of str, optional
        List of fullnames of the nodes to open at start (default is []). The full name of a node is the concatenation of the path to reach the node, using the separator character
    opened_all : bool, optional
        If True, all the tree nodes are opened at start (default is False). This setting has prevalence over the opened parameter.
    selected : list of str, optional
        List of fullnames of the nodes to select at start (default is []). The full name of a node is the concatenation of the path to reach the node, using the separator character
    disabled : list of str, optional
        List of fullnames of the nodes to display as disabled in the tree (default is [])
    iconsshow : bool, optional
        If True, an icon is added to each node of the tree (default is False)
    iconscolor : str, optional
        Color of the icons (default is settings.color_first)
    iconsfolder : bool, optional
        If True (and if iconsshow is True) it adds the open/closed folder icon to nodes that have children (default is True)
    icons_folder_opened : str, optional
        Name of the icon to use for opened nodes that have children when iconsfolder is True (default 'mdi-folder-open')
    icons_folder_closed : str, optional
        Name of the icon to use for closed nodes that have children when iconsfolder is True (default 'mdi-folder')
    iconroot : str, optional
        Name of the icon for the root node of the tree (default is None)
    iconscolumnName1 : str, optional
        Name of the DataFrame column that contains the icon name for the node on the first level of the tree (default is None)
    iconscolumnName2 : str, optional
        Name of the DataFrame column that contains the icon name for the node on the second level of the tree (default is None)
    iconscolumnName3 : str, optional
        Name of the DataFrame column that contains the icon name for the node on the third level of the tree (default is None)
    tooltips : bool, optional
        If True the nodes will show the tooltip (default is False)
    tooltips_chars : int, optional
        Minimum lenght of the node label to show the tooltip (default is 20)
    item_height : int, optional
        Item height in pixels (default is 24)
    font_size : int, optional
        Font size in pixels (default is 15)
    icon_size : int, optional
        Icon size in pixels (default is 18)
    checkbox_size : int, optional
        Checkbox size in pixels (default is 24)

    Returns
    -------
    v.Card
        An ipyvuetify v.Card widget having a v.Html as its only child. The v.Html has a treeview.CustomTreeview widget as its only child

    Example
    -------
    Creation of a treeview from a simple Pandas DataFrame::
    
        from vois.vuetify import treeview
        import pandas as pd

        table = [['parent', 'child', 'nephew'], ['John', 'Mary', 'Johnny'], ['John', 'Peter', 'Lisa'], 
                                                ['Ann', 'Hellen', 'July'], ['Ann', 'Sue', 'Hellen'],
                                                ['Ann', 'Claire', 'Pieter']]
        headers = table.pop(0)
        df = pd.DataFrame(table, columns=headers)
        display(df)
        
        def on_change(arg):
            print(arg)
            
        treecard = treeview.createTreeviewFromDF3Columns(df, headers[0], headers[1], headers[2], 
                                                         rootName='Families',
                                                         on_change=on_change)
        display(treecard)
        
    .. figure:: figures/treeview3.png
       :scale: 100 %
       :alt: treeview widget

       Treeview widget created from a Pandas DataFrame.
    """

    
    
    nextid = 1          # id of the next node
    fullnamenodes = {}  # All the nodes inserted, key is the fullname of the node
    fullnames2id  = {}  # Convert a fullname to its id
    
    if len(rootName) == 0: rootName = 'Root'
    root, nextid, fullnamenodes, fullnames2id = addNode(rootName,None,iconroot, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)

    # Create the tree from 3 columns of a df
    for index,row in df.iterrows():
        parentname = str(row[columnName1])
        name       = str(row[columnName2])
        subname    = str(row[columnName3])

        parenticon = None
        if iconsshow and (not iconscolumnName1 is None) and (iconscolumnName1 in row): parenticon = str(row[iconscolumnName1])
        parent, nextid, fullnamenodes, fullnames2id = addNode(parentname, root, parenticon, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)
        
        icon = None
        if iconsshow and (not iconscolumnName2 is None) and (iconscolumnName2 in row): icon = str(row[iconscolumnName2])
        elem, nextid, fullnamenodes, fullnames2id = addNode(name,parent,icon, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)

        icon = None
        if iconsshow and (not iconscolumnName3 is None) and (iconscolumnName3 in row): icon = str(row[iconscolumnName3])
        elem, nextid, fullnamenodes, fullnames2id = addNode(subname,elem,icon, iconsshow,iconsfolder,repeat_parent_as_first_child,rootName,separator,nextid,fullnamenodes,fullnames2id,disabled)
        
        
    # List of selected ids
    selectedids = []
    if select_all: selectedids = calculateIdsOfLeaves(root)
    else:          selectedids = [fullnames2id[x] for x in selected if x in fullnames2id]
        
        
    # Convert opened fullnames to ids
    openedids = []
    if not opened_all:
        if len(opened) == 0: openedids = [1]  # Only Root is opened by default
        else:                openedids = [fullnames2id[x] for x in opened if x in fullnames2id]
        
    # Convert active fullname to id
    if not active is None and active in fullnames2id:
        activeid = fullnames2id[active]
    else:
        activeid = None
    
    #import json
    #print(json.dumps(root, indent=4))
    
    tree = CustomTreeview(items=[root], selected=selectedids, opened=openedids, on_change=on_change, on_activated=on_activated, 
                          expand_selection_to_parents=expand_selection_to_parents, dark=dark, transition=transition, opened_all=opened_all, 
                          color=color, selectable=selectable, activatable=activatable, active=activeid, open_on_click=open_on_click,
                          tooltips=tooltips, tooltips_chars=tooltips_chars,
                          iconsshow=iconsshow, iconscolor=iconscolor, icons_folder_opened=icons_folder_opened, icons_folder_closed=icons_folder_closed,
                          item_height=item_height, font_size=font_size, icon_size=icon_size, checkbox_size=checkbox_size)
    
    treehtml = v.Html(tag='div',height=height, children=[tree], style_='overflow: hidden;')
    treecard = v.Card(width=width, height=height, elevation=elevation, children=[treehtml],
                      dark=dark, style_='overflow-x: visible;')
    
    return treecard
