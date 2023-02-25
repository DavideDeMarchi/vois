"""Vertically aligned list of customizable cards with items that can be moved, added and removed."""
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
from ipywidgets import widgets, Layout
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
    from . import tooltip
except:
    import settings
    import tooltip


#####################################################################################################################################################
# Vertically aligned list of customizable cards with items that can be moved, added and removed.
#####################################################################################################################################################
class sortableList:
    """
    Vertically aligned list of customizable cards with items that can be moved, added and removed.
                
    Parameters
    ----------
    items : list of dicts, optional
        List of items to display in the list (default is [])
    width : int, optional
        Width of widget in pixels (default is 400)
    outlined : bool, optional
        Flag to show each of the items with a border (default is True)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    allowNew : bool, optional
        If True, a 'plus' button is displayed that allows for adding new items (default is True)
    newOnTop: bool, optional
        If True, the '+' button adds a new item in first position on the items list (default False, new items are added as last in the items list)
    newButtonOnTop: bool, optional
        If True, the '+' button is displayed on top of the first item, otherwise it is displayed below the last item (default is False, the '+' button is on the bottom)
    itemNew : function, optional
        Python function called when a new items is added. The function is called with no arguments and it must return the dict initialized with the new item content (default is None). As an alternative, the function can return None, but then the real adding of the new item must be done by directly calling the doAddItem method
    itemContent : function, optional
        Python function called when an item is displayed. The function is called with an item as its first argument and the index (position of the item) as second argument. The function must return a list containing the ipyvuetify widgets to display the item content (default is None)
    bottomContent : list of ipyvuetify widgets, optional
        Additional widgets content to display in the bottom line (containing the 'plus' button), aligned to the right (default is [])
    onchange : function, optional
        Python function to call when the user changes the order of items or removes an item. The function will receive no parameters as input (default is None)
    onmovedown : function, optional
        Python function to call when the user moves one item down. The function will receive as parameter the zero-based index, before the move, of the moved item (default is None)
    onmoveup : function, optional
        Python function to call when the user moves one item up. The function will receive as parameter the zero-based index, before the move, of the moved item (default is None)
    onremoving : function, optional
        Python function to call when the user is about to remove an item. The function will receive as parameter the zero-based index of the item that is going to be removed (default is None)
    onremoved : function, optional
        Python function to call just after the user removes an item. The function will receive as parameter the zero-based index of the removed item (default is None)
    onadded : function, optional
        Python function to call just after a new item is added. The function will receive as parameter the zero-based index of the new item (default is None)
    buttonstooltip : bool, optional
        If True, the buttons to mode, add, remove items will have a tooltip (default is False)
    tooltipadd : str, optional
        Tooltip text for the "add" button (default is 'Add new')
    tooltipdown : str, optional
        Tooltip text for the "move down" buttons (default is 'Move down')
    tooltipup : str, optional
        Tooltip text for the "move up" buttons (default is 'Move up')
    tooltipremove : str, optional
        Tooltip text for the "remove" buttons (default is 'Remove')
    activatable : bool, optional
        If True the items can be activated by clicking on them (default is False)
    ondeactivated : function, optional
        Python function to call just after an item that was the active one, is deactivated. The function will receive as parameter the zero-based index of the deactivated item (default is None)
    onactivated : function, optional
        Python function to call just after an item becomes the active one (or by user-clicking or by setting the active property). The function will receive as parameter the zero-based index of the active item (default is None)


    Examples
    --------
    Simple list displaying static text::
        
        from vois.vuetify import sortableList
        from ipywidgets import widgets
        from IPython.display import display
        import ipyvuetify as v

        items = [{ "name": 'Jane Adams',   "email": 'jane@adams.com'   },
                 { "name": 'Paul Davis',   "email": 'paul@davis.com'   },
                 { "name": 'Amanda Brown', "email": 'amanda@brown.com' }
                ]


        # Creation of a new item
        def itemNew():
            return {"name": "new", "email": "empty"}


        # Content of an item
        def itemContent(item, index):
            return [
                v.CardSubtitle(class_="mb-n4", children=[item['name']]),
                v.CardText(    class_="mt-n2", children=[item['email']])
            ]

        s = sortableList.sortableList(items=items, dark=False, allowNew=True,
                                      itemNew=itemNew, itemContent=itemContent)
        display(s.draw())
    
    
    .. figure:: figures/sortableList1.png
       :scale: 100 %
       :alt: label widget

       Example of a simple sortableList displaying static text


    Example of a sortable list displaying editable text, boolean and date values (using the :py:class:`datePicker.datePicker` class)::
        
        from vois.vuetify import sortableList, datePicker, switch, tooltip
        from ipywidgets import widgets
        from IPython.display import display
        import ipyvuetify as v

        output = widgets.Output()

        items = [
            { "name": "Paul",    "surname": "Dockery",  "married": False, "date": "" },
            { "name": "July",    "surname": "Winters",  "married": True,  "date": "1997-07-28" },
            { "name": "David",   "surname": "Forest",   "married": True,  "date": "1999-03-03" },
            { "name": "Dorothy", "surname": "Landmann", "married": False, "date": "" }
        ]

        dark = False

        # Called when an item is moved or deleted
        def onchange():
            with output:
                print('Changed!')


        # Creation of a new item
        def itemNew():
            return { "name": "", "surname": "", "married": False, "date": "" }


        # Remove all items
        def itemRemoveAll(widget, event, data):
            s.items = []

        reset = v.Btn(icon=True, children=[v.Icon(children=['mdi-playlist-remove'])])
        reset.on_event('click', itemRemoveAll)


        # Content of an item
        def itemContent(item, index):

            def onname(widget, event, data):
                item["name"] = int(data)

            def onsurname(widget, event, data):
                item["surname"] = data

            def onmarried(flag):
                item["married"] = flag
                dp.disabled = not flag
                if not flag:
                    item["date"] = ''
                    dp.date = None

            def ondate():
                item["date"] = dp.date

            tfname = v.TextField(label='Name:', value=item['name'],
                                 color='amber', dense=True,
                                 style_="max-width: 70px", class_="pa-0 ma-0 mt-2")
            tfname.on_event('input', onname)

            tfsurname = v.TextField(label='Surname:', value=item['surname'],
                                    color='amber', dense=True, 
                                    style_="max-width: 100px", class_="pa-0 ma-0 mt-2")
            tfsurname.on_event('input', onsurname)

            sw = switch.switch(item['married'], "Married", onchange=onmarried)

            dp = datePicker.datePicker(date=item['date'], dark=dark, width=88, 
                                       onchange=ondate, offset_x=True, offset_y=False)
            dp.disabled = not item['married']

            sp = v.Html(tag='div', class_="pa-0 ma-0 mr-3", children=[''])

            return [ v.Row(class_="pa-0 ma-0 ml-2", no_gutters=True,
                           children=[tfname, sp, tfsurname, sp, sw.draw(), sp, dp.draw()]) ]


        s = sortableList.sortableList(items=items,
                                      width=520,
                                      outlined=False,
                                      dark=dark,
                                      allowNew=True,
                                      itemNew=itemNew,
                                      itemContent=itemContent,
                                      bottomContent=[tooltip.tooltip("Remove all persons",
                                                                     reset)],
                                      onchange=onchange,
                                      buttonstooltip=True)
        display(s.draw())
        display(output)

    .. figure:: figures/sortableList2.png
       :scale: 100 %
       :alt: label widget

       Example of a sortableList to edit textual, boolean and date values on persons.
    """

   
    # Initialization
    def __init__(self, items=[], width=400, maxheightlist=10000, outlined=True, dark=settings.dark_mode,
                 allowNew=True, newOnTop=False, newButtonOnTop=False, itemNew=None, itemContent=None, bottomContent=[],
                 onchange=None, onmovedown=None, onmoveup=None, onremoving=None, onremoved=None, onadded=None, buttonstooltip=False,
                 tooltipadd='Add new', tooltipdown='Move down', tooltipup='Move up', tooltipremove='Remove',
                 activatable=False, ondeactivated=None, onactivated=None):
        
        self._items         = items
        self.width          = width
        self.outlined       = outlined
        self.dark           = dark

        self.allowNew       = allowNew
        self.newOnTop       = newOnTop
        self.newButtonOnTop = newButtonOnTop
        self.itemNew        = itemNew
        self.itemContent    = itemContent
        
        self.bottomContent  = bottomContent
        
        self.onchange       = onchange
        self.buttonstooltip = buttonstooltip
        self.tooltipadd     = tooltipadd
        self.tooltipdown    = tooltipdown
        self.tooltipup      = tooltipup
        self.tooltipremove  = tooltipremove
        self.onmovedown     = onmovedown
        self.onmoveup       = onmoveup
        self.onremoving     = onremoving
        self.onremoved      = onremoved
        self.onadded        = onadded
        
        self.activatable    = activatable
        self.ondeactivated  = ondeactivated
        self.onactivated    = onactivated
        self.activeindex    = -1
        
        self.output     = v.Card(flat=True, max_height='%dpx'%maxheightlist, children=[])
        self.outputplus = v.Card(flat=True, children=[])

        self.cards    = []
        self.bdowns   = []
        self.bups     = []
        self.bremoves = []

        # Create the + button to add a new item
        self.style = "min-width: %dpx; max-width: %dpx" %(self.width,self.width)
        if self.allowNew:
            self.plusbutton = v.Btn(icon=True, dark=self.dark, children=[v.Icon(children=['mdi-plus'])])
            self.plusbutton.on_event('click', self.onadd)
            if self.buttonstooltip:
                self.outputplus.children = [v.Row(no_gutters=True, style_=self.style, justify='space-between',
                                                  children=[tooltip.tooltip(self.tooltipadd, self.plusbutton)] + self.bottomContent)]
            else:
                self.outputplus.children = [v.Row(no_gutters=True, style_=self.style, justify='space-between',
                                                  children=[self.plusbutton] + self.bottomContent)]
            

        # Add all the items
        for index, item in enumerate(self._items):
            self.additem(item, index==0, index==len(self._items)-1)

        if self.activatable: bottomspace = 'mb-2'
        else:                bottomspace = ''
        self.col = v.Col(class_="pa-0 ma-0 %s"%bottomspace, children=self.cards)
        self.output.children = [self.col]
        

    # Click on + button
    def onadd(self, widget, event, data):
        if self.itemNew:
            item = self.itemNew()
            if not item is None:
                self.doAddItem(item)
                if not self.onadded is None:
                    if self.newOnTop:
                        self.onadded(0)
                    else:
                        self.onadded(len(self.cards)-1)

                        
    # Effective add of a new item
    def doAddItem(self, item):
        """
        Manual adding of a new item
        """
        if self.newOnTop:
            if len(self.bups) > 0: self.bups[0].disabled = False
            self._items.insert(0,item)

            if self.activeindex >= 0:
                self.activeindex += 1
            
            self.additem(item, True, len(self.cards)==0, onTop=True)
        else:
            if len(self.bdowns) > 0: self.bdowns[-1].disabled = False
            self._items.append(item)
            self.additem(item, len(self.cards)==0, True)
                
        if self.activatable: bottomspace = 'mb-2'
        else:                bottomspace = ''
        self.col = v.Col(class_="pa-0 ma-0 %s"%bottomspace, children=self.cards)
        self.output.children = [self.col]
        if self.onchange:
            self.onchange()


    # Update the disabled state of the buttons
    def update_buttons(self):
        for i in range(len(self.bdowns)): self.bdowns[i].disabled  = False
        if len(self.bdowns)>0:            self.bdowns[-1].disabled = True
        for i in range(len(self.bups)):   self.bups[i].disabled = False
        if len(self.bups)>0:              self.bups[0].disabled = True


    # Move item down
    def ondown(self, widget, event, data):
        index = self.bdowns.index(widget)
        
        wasactive = False
        if index == self.activeindex:
            wasactive = True
            
        changewithactive = False
        if index+1 == self.activeindex:
            changewithactive = True
            
        a = index
        b = index + 1
        self.updateCard(self._items[a], a)
        self.updateCard(self._items[b], b)
        self._items[b],   self._items[a]   = self._items[a],   self._items[b]
        self.cards[b],    self.cards[a]    = self.cards[a],    self.cards[b]
        self.bdowns[b],   self.bdowns[a]   = self.bdowns[a],   self.bdowns[b]
        self.bups[b],     self.bups[a]     = self.bups[a],     self.bups[b]
        self.bremoves[b], self.bremoves[a] = self.bremoves[a], self.bremoves[b]
        self.update_buttons()
        if self.activatable: bottomspace = 'mb-2'
        else:                bottomspace = ''
        self.col = v.Col(class_="pa-0 ma-0 %s"%bottomspace, children=self.cards)
        self.output.children = [self.col]
        
        if self.onchange:
            self.onchange()
        if self.onmovedown:
            self.onmovedown(index)
            
        if wasactive:
            self.active = index + 1
        elif changewithactive:
            self.active = index


    # Move item up
    def onup(self, widget, event, data):
        index = self.bups.index(widget)
        
        wasactive = False
        if index == self.activeindex:
            wasactive = True
            
        changewithactive = False
        if index-1 == self.activeindex:
            changewithactive = True
            
        a = index - 1
        b = index
        self.updateCard(self._items[a], a)
        self.updateCard(self._items[b], b)
        self._items[b],   self._items[a]   = self._items[a],   self._items[b]
        self.cards[b],    self.cards[a]    = self.cards[a],    self.cards[b]
        self.bdowns[b],   self.bdowns[a]   = self.bdowns[a],   self.bdowns[b]
        self.bups[b],     self.bups[a]     = self.bups[a],     self.bups[b]
        self.bremoves[b], self.bremoves[a] = self.bremoves[a], self.bremoves[b]
        self.update_buttons()
        if self.activatable: bottomspace = 'mb-2'
        else:                bottomspace = ''
        self.col = v.Col(class_="pa-0 ma-0 %s"%bottomspace, children=self.cards)
        self.output.children = [self.col]
        
        if self.onchange:
            self.onchange()
        if self.onmoveup:
            self.onmoveup(index)

        if wasactive:
            self.active = index - 1
        elif changewithactive:
            self.active = index

            
    # Remove item
    def ondel(self, widget, event, data):
        index = self.bremoves.index(widget)
        if self.onremoving:
            self.onremoving(index)
            
        if index == self.activeindex:
            if not self.ondeactivated is None:
                self.ondeactivated(self.activeindex)
            self.activeindex = -1
        elif index <= self.activeindex:
            self.activeindex -= 1
            
        del self._items[index]
        del self.cards[index]
        del self.bdowns[index]
        del self.bups[index]
        del self.bremoves[index]
        self.col.children = self.col.children[:index] + self.col.children[index+1 :]
        self.update_buttons()
        self.output.children = [self.col]
        
        if self.onchange:
            self.onchange()
        if self.onremoved:
            self.onremoved(index)


    # Update the card for an item given its index
    def updateCard(self, item, index):
        if self.itemContent:
            c = self.col.children[index]
            c.children = [c.children[0]] + self.itemContent(item,index)
        
    
    # Management of click on an item card
    def __internal_onclick(self, widget=None, event=None, data=None):
        if widget in self.cards:
            index = self.cards.index(widget)
            if self.activatable:
                self.active = index
        
    
    # Add an item to the lists 
    def additem(self, item, isfirst, islast, onTop=False):
        if self.itemContent:
            bdown   = v.Btn(icon=True, class_="mr-n3", disabled=islast,  children=[v.Icon(small=True, children=['mdi-arrow-down'])])
            bup     = v.Btn(icon=True, class_="mr-n3", disabled=isfirst, children=[v.Icon(small=True, children=['mdi-arrow-up'])])
            bremove = v.Btn(icon=True, children=[v.Icon(small=True, children=['mdi-close'])])

            if onTop:
                self.bdowns.insert(0,bdown)
                self.bups.insert(0,bup)
                self.bremoves.insert(0,bremove)
            else:
                self.bdowns.append(bdown)
                self.bups.append(bup)
                self.bremoves.append(bremove)

            bdown.on_event('click.stop', self.ondown)
            bup.on_event('click.stop', self.onup)
            bremove.on_event('click.stop', self.ondel)

            if self.buttonstooltip:
                buttons = [tooltip.tooltip(self.tooltipdown,   bdown),
                           tooltip.tooltip(self.tooltipup,     bup),
                           tooltip.tooltip(self.tooltipremove, bremove)]
            else:
                buttons = [bdown,bup,bremove]
                
            if self.activatable: ripple = True
            else:                ripple = False
                
            if onTop:
                index = 0
            else:
                index = len(self.cards)
                
            if self.activatable:
                bottom = "mb-2"
            else:
                bottom = ""
                
            c = v.Card(outlined=self.outlined, dark=self.dark, flat=True, dense=True, class_="pa-0 ma-0 mt-1 %s"%bottom, style_=self.style, ripple=ripple, raised=False,
                       children=[v.CardTitle(class_="justify-end pa-0 ma-0 mt-n1 mb-n5", children=buttons)] + self.itemContent(item,index))
            c.on_event('click', self.__internal_onclick)

            if onTop:
                self.cards.insert(0,c)
            else:
                self.cards.append(c)

    
    
    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (a v.Html object displaying two output widgets)"""
        if self.allowNew:
            if self.newButtonOnTop:
                return v.Html(tag='div',children=[widgets.VBox([self.outputplus,self.output])])
            else:
                return v.Html(tag='div',children=[widgets.VBox([self.output,self.outputplus])])
        else:
            return self.output
    
    
    # Get the items
    @property
    def items(self):
        """
        Get/Set the updated items.
        
        Returns
        --------
        items : list of dicts
            List of items in their updated position

        """
        return self._items
            
    # Set the items
    @items.setter
    def items(self, items):
        self._items = items
        
        self.cards    = []
        self.bdowns   = []
        self.bups     = []
        self.bremoves = []
        
        self.activeindex = -1

        # Add all the items
        for index, item in enumerate(self._items):
            self.additem(item, index==0, index==len(self._items)-1)

        if self.activatable: bottomspace = 'mb-2'
        else:                bottomspace = ''
        self.col = v.Col(class_="pa-0 ma-0 %s"%bottomspace, children=self.cards)
        self.output.children = [self.col]
            
        if self.onchange:
            self.onchange()

    # Get the index of the active item
    @property
    def active(self):
        """
        Get/Set the active item.
        
        Returns
        --------
        index : int
            index of the active item

        """
        return self.activeindex
            
    # Set the active item
    @active.setter
    def active(self, index):
        if index >= 0 and index < len(self.cards):
            if self.activeindex >= 0:
                self.cards[self.activeindex].raised = False
                if not self.ondeactivated is None:
                    self.ondeactivated(self.activeindex)

            self.activeindex = index
            self.cards[self.activeindex].raised = True
            if not self.onactivated is None:
                self.onactivated(self.activeindex)
            