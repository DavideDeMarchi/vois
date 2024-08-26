"""Widget for the creation and editing of color palettes."""
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
import ipyvuetify as v
from ipywidgets import widgets, Layout
from IPython.display import display, HTML
import random
import base64
import json

try:
    from . import settings
    from . import sortableList
    from . import palettePicker
    from . import ColorPicker
    from . import switch
    from . import tooltip
    from . import dialogGeneric
    from . import dialogWait
    from . import dialogMessage
    from . import selectSingle
    from . import upload
except:
    import settings
    import sortableList
    import palettePicker
    import ColorPicker
    import switch
    import tooltip
    import dialogGeneric
    import dialogWait
    import dialogMessage
    import selectSingle
    import upload

    
    
# Utility to return items from a list of colors
def colorlist2Items(colors=[]):
    """
    Utility function to convert a list of colors to a list of items to pass as parameter to the :py:class:`paletteEditor.paletteEditor` class
    
    Parameters
    ----------
    colorlist : list of str, optional
        List of string representing colors in the format '#RRGGBB' (default is [])
        
    Return
    ------
        A list of items ready to be passed to the :py:class:`paletteEditor.paletteEditor` class constructor
        
    """
    return [{ "value": 0,  "class": "", "color": x } for x in colors]
    
    

# Utility: 3 integers to '#RRGGBB'
def RGB(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)
    

    
# Class paletteEditor
class paletteEditor():
    """
    Widget for the creation and editing of color palettes.
        
    Parameters
    ----------
    title : str, optional
        Title of the palette (default is '')
    items : list of dicts, optional
        List of dicts containing "value", "class" and "color" (default is [])
    interpolate : bool, optional
        Flag to control the interpolation of the colorlist: if True the palette will be displayed by adding intermediate colors (default is True)
    width : int, optional
        Width of the widget in pixels (default is 420)
    color : str, optional
        Color used for the widget (default is the color_first defined in the settings.py module)
    dark : bool, optional
        Flag to invert the text and backcolor (default is the value of settings.dark_mode)
    onchange : function, optional
        Python function to call when the user changes the order of colors or removes a color. The function will receive no parameters as input (default is None)
    buttonstooltip : bool, optional
        If True, the buttons to mode, add, remove colors and assign values to colors will have a tooltip (default is True)

    Example
    -------
    Example of a widget to create and edit a color palette::
        
        from vois.vuetify import paletteEditor
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        def onchange():
            with output:
                print('onchange!')

        p = paletteEditor(items=[], width=450, onchange=onchange)

        display(p.draw())
        display(output)

    .. figure:: figures/paletteEditor.png
       :scale: 100 %
       :alt: card widget

       Example of a widget to create and edit a color palette
    """
    
    # Initialization
    def __init__(self, title='', items=[], interpolate=True, width=420, maxheightlist=600,
                 color=settings.color_first, dark=settings.dark_mode,
                 onchange=None, buttonstooltip=True):

        self.width          = width
        self.color          = color
        self.dark           = dark
        self.onchange       = onchange
        self.buttonstooltip = buttonstooltip
        
        self.outputdialog  = widgets.Output(layout=Layout(width='0px', min_width='0px', height='0px'))
        self.outputtoolbar = widgets.Output()
        self.outputtitle   = widgets.Output()
        self.outputpalette = widgets.Output()
        self.outputlist    = widgets.Output()
        self.outputpreview = widgets.Output(layout=Layout(width='480px', min_width='480px', height='50px'))
        

        self.tfTitle = v.TextField(v_model=title, label="Title", color=self.color, class_="pa-0 ma-0 mt-3", style_="width: %dpx; max-width: %dpx"%(self.width,self.width))

        self.sp = v.Html(tag='div', class_="pa-0 ma-0 mr-3", children=[''])

        self.palette_text = ''
        
        self.tf = v.TextField(v_model="Palette", label="Palette file name", autofocus=True, 
                              color=self.color, class_="pa-0 ma-0 ml-4 mr-4")
        
        custompalettes = [
            { "name": "Simple", "colors": ['#000000', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF']},

            { "name": "Dem",    "colors": [RGB(255,255,170), RGB( 39,168, 39), RGB( 11,128, 64), RGB(255,255,  0), RGB(255,186,  3),
                                           RGB(158, 30,  2), RGB(110, 40, 10), RGB(138, 94, 66), RGB(255,255,255)]},

            { "name": "NDVI",   "colors": [RGB(120,69,25), RGB(255,178,74), RGB(255,237,166), RGB(173,232,94),
                                           RGB(135,181,64), RGB(3,156,0), RGB(1,100,0), RGB(1,80,0)]}
        ]

        families = ['carto', 'cmocean', 'cyclical', 'diverging', 'plotlyjs', 'qualitative', 'sequential', 'custom']
        family   = 'sequential'

        self.selfam = selectSingle.selectSingle('Family:', families, selection=family, width=160, onchange=self.onchangeFamily, marginy=1, clearable=False)
        self.pp = palettePicker.palettePicker(family=family, custompalettes=custompalettes, label='Palette:', height=26)

        self.upload_file = upload.upload(accept="application/json", multiple=False, show_progress=False, onchange=self.on_upload_palette,
                                         label='Palette file:', placeholder='Click to select the palette to upload', width='480px', margins="pa-0 ma-0 ml-4")
        
        # Top buttons
        self.new  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-file-outline'])])
        self.new.on_event('click', self.onnew)

        self.upload  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-folder-open-outline'])])
        self.upload.on_event('click', self.onupload)

        self.download  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-content-save'])])
        self.download.on_event('click', self.ondownload)

        self.select  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-folder-search-outline'])])
        self.select.on_event('click', self.onselect)
        
        self.revert  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-autorenew'])])
        self.revert.on_event('click', self.onrevert)

        self.random  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-palette'])])
        self.random.on_event('click', self.onrandom)
        
        with self.outputtoolbar:
            display(v.Row(no_gutters=True, style_="min-width: 300px;", justify="start", class_="pa-0 ma-0",
                          children=[tooltip.tooltip("New palette",self.new),
                                    tooltip.tooltip("Load a palette from local disk",self.upload),
                                    tooltip.tooltip("Save current palette to local disk",self.download),
                                    tooltip.tooltip("Select one of the pre-defined palettes",self.select),
                                    tooltip.tooltip("Revert palette order",self.revert),
                                    tooltip.tooltip("Assign random colors",self.random)]))
 
        with self.outputtitle:
            display(self.tfTitle)
            
        # Bottom buttons
        self.zero  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-numeric-0'])])
        self.zero.on_event('click', self.onzero)
        
        self.asc   = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-numeric-1'])])
        self.asc.on_event('click', self.onasc)
        
        self.desc  = v.Btn(icon=True, class_="mr-0", dark=self.dark, children=[v.Icon(children=['mdi-numeric-negative-1'])])
        self.desc.on_event('click', self.ondesc)
        
        self.sw = switch.switch(interpolate, "Interpolate", color=self.color, onchange=self.__internal_onchange)

        self.s = sortableList.sortableList(items=items, width=self.width, maxheightlist=maxheightlist, outlined=False, dark=self.dark,
                                           allowNew=True, itemNew=self.itemNew, itemContent=self.itemContent,
                                           bottomContent=[#self.sp,self.sp,
                                                          tooltip.tooltip("Set all values to 0",self.zero),
                                                          tooltip.tooltip("Set increasing values starting from first color",self.asc),
                                                          tooltip.tooltip("Set decreasing values starting from last color", self.desc),
                                                          tooltip.tooltip("Interpolate colors",self.sw.draw())],
                                           onchange=self.__internal_onchange,
                                           buttonstooltip=self.buttonstooltip,
                                           tooltipadd='Add new color', tooltipdown='Move color down',
                                           tooltipup='Move color up', tooltipremove='Remove color')

        self.updatePalette()
        
        with self.outputlist:
            display(self.s.draw())

            
    # Change family in the palette picker
    def onchangeFamily(self):
        family = self.selfam.value
        if family == 'carto' or family == 'qualitative':
            interpolate = False
        else:
            interpolate = True
        self.pp.updatePalettes(family,interpolate)
        
        
    # New palette
    def onnew(self, widget, event, data):
        self.s.items         = []
        self.sw.value        = True
        self.tfTitle.v_model = ''


    # Select
    def onselect(self, widget, event, data):
        def on_ok():
            dlg = dialogWait.dialogWait(text='Loading palette...', output=self.outputdialog)
            self.s.items = colorlist2Items(self.pp.colors)
            self.sw.value = self.pp.interpolate
            dlg.close()
            
        content1 = v.Row(no_gutters=True, justify="start", class_="pa-0 ma-0 ml-6", children=[self.selfam.draw()])
        content2 = v.Row(no_gutters=True, justify="start", class_="pa-0 ma-0 ml-6", children=[self.pp.draw()])

        dlg = dialogGeneric.dialogGeneric(title='Palette selection', text='Please select one of the predefined palettes:',
                                          show=True, addclosebuttons=False, width=600,
                                          addokcancelbuttons=True, on_ok=on_ok,
                                          fullscreen=False, content=[widgets.VBox([content1, content2])], output=self.outputdialog)

        
    # Called when a .json file is selected for upload
    def on_upload_palette(self, files):
        self.outputpreview.clear_output(wait=False)
        if len(files) > 0:
            f = files[0]
            self.palette_text = f['file_obj'].read().decode("utf-8")

            try:
                j = json.loads(self.palette_text)
                if ("format" in j) and ("interpolate" in j) and ("items" in j) and (j["format"] == "BDAP palette 1.0"):
                    items = j["items"]
                    interpolate = j["interpolate"]
                    colors = [x["color"] for x in items]
                    with self.outputpreview:
                        display(v.Card(outlined=True, dark=self.dark, class_="pa-0 ma-0", style_='width: 400px; max-width: 400px; height: 40px; max-height: 40px;' ,
                                children=[v.Img(class_="pa-0 ma-1", src=palettePicker.image2Base64(palettePicker.paletteImage(colors, width=360, height=29, interpolate=interpolate)))]))
                else:
                    self.upload_file.clear()
                    e = dialogMessage.dialogMessage(title='Error',
                                                    text='The uploaded file is not in the \"BDAP palette 1.0\" format',
                                                    addclosebuttons=False, show=True, width=400, output=self.outputdialog)
            except:
                self.upload_file.clear()
                e = dialogMessage.dialogMessage(title='Error',
                                                text='Cannot read the uploaded file!',
                                                addclosebuttons=False, show=True, width=400, output=self.outputdialog)
        else:
            self.palette_text = ''

    
    # Called when the file upload dialog is closed with the "OK" button
    def on_upload_ok(self):
        if len(self.palette_text) > 2:
            dlg = dialogWait.dialogWait(text='Loading palette...', output=self.outputdialog)
            try:
                j = json.loads(self.palette_text)
                if ("format" in j) and ("interpolate" in j) and ("items" in j) and (j["format"] == "BDAP palette 1.0"):
                    self.s.items, self.sw.value = j["items"], j["interpolate"]
                    if "title" in j: self.tfTitle.v_model = j["title"]
                    else:            self.tfTitle.v_model = ''
                else:
                    e = dialogMessage.dialogMessage(title='Error',
                                                    text='The uploaded file is not in the \"BDAP palette 1.0\" format',
                                                    addclosebuttons=False, show=True, width=400, output=self.outputdialog)
            except:
                e = dialogMessage.dialogMessage(title='Error',
                                                text='Cannot read the uploaded file!',
                                                addclosebuttons=False, show=True, width=400, output=self.outputdialog)
                
            dlg.close()
            
        self.palette_text = ''
        self.upload_file.clear()
            
    
    # Called when the file upload dialog is closed with the "cancel" button
    def on_upload_cancel(self):
        self.palette_text = ''
        self.upload_file.clear()
        
        
    # Upload
    def onupload(self, widget, event, data):
        self.outputpreview.clear_output()
        dlg = dialogGeneric.dialogGeneric(title='Load a palette from local disk', text='', show=True, 
                                          addclosebuttons=False, width=520,
                                          addokcancelbuttons=True, on_ok=self.on_upload_ok, on_cancel=self.on_upload_cancel,
                                          fullscreen=False, content=[self.upload_file.draw(), self.outputpreview], output=self.outputdialog)

    

    # Direct download of a .txt file containing a string
    def downloadText(self, textobj, fileName="palette.json"):
        string_bytes  = textobj.encode("ascii","ignore")
        base64_bytes  = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")

        self.outputdialog.clear_output()
        with self.outputdialog:
            display(HTML('<script>function downloadURI(uri, name) { var link = document.createElement("a"); link.download = name; link.href = uri; link.click();} downloadURI("data:application/octet-stream;charset=utf-8;base64,' + base64_string + '","' + fileName + '"); </script>'))

            
        # Download
    def ondownload(self, widget, event, data):

        def on_ok():
            items = self.s.items
            j = { "format":      "BDAP palette 1.0",
                  "interpolate": self.sw.value,
                  "items"      : items,
                  "title"      : self.tfTitle.v_model
                }
            txt = json.dumps(j)
            filename = self.tf.v_model
            if filename[-5:] != ".json": filename += ".json"
            self.downloadText(txt, fileName=filename)
        
        dlg = dialogGeneric.dialogGeneric(title='Save current palette to local disk', text='', show=True, 
                                          addclosebuttons=False, width=500,
                                          addokcancelbuttons=True, on_ok=on_ok,
                                          fullscreen=False, content=[self.tf], output=self.outputdialog)


    # Revert palette order
    def onrevert(self, widget, event, data):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        self.s.items = list(reversed(self.s.items))
        dlg.close()


    # Assign random colors
    def onrandom(self, widget, event, data):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        items = self.s.items
        for item in items:
            item['color'] = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        self.s.items = items
        dlg.close()
        
    
    
    # Set all values to zero
    def onzero(self, widget, event, data):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        items = self.s.items
        for item in items:
            item['value'] = 0
        self.s.items = items
        dlg.close()
            
        
    # Set all increasing values starting from first color
    def onasc(self, widget, event, data):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        items = self.s.items
        if len(items) > 0:
            start = items[0]['value']
            for index, item in enumerate(items):
                item['value'] = start + index
            self.s.items = items
        dlg.close()

    
    # Set all decreasing values starting from last color
    def ondesc(self, widget, event, data):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        items = self.s.items
        if len(items) > 0:
            start = items[-1]['value']
            for index, item in enumerate(items):
                item['value'] = start - len(items) + 1 + index
            self.s.items = items
        dlg.close()

    
    # Update the palette image
    def updatePalette(self):
        colors = []
        for item in self.s.items:
            colors.append(item['color'])
            
        self.outputpalette.clear_output(wait=True)
        with self.outputpalette:
            display(v.Card(outlined=True, dark=self.dark, style_='width: %dpx; max-width: %dpx; height: 40px; max-height: 40px;' %(self.width,self.width),
                    children=[v.Img(class_="pa-0 ma-1", src=palettePicker.image2Base64(palettePicker.paletteImage(colors, width=self.width-20, 
                                                                                                                  height=29, interpolate=self.sw.value)))]))
            
        
    # Creation of a new item
    def itemNew(self):
        return { "value": 0,  "class": "", "color": "#FF0000" }


    # Content of an item
    def itemContent(self, item, index):

        def onvalue(widget, event, data):
            item["value"] = int(data)

        def onclass(widget, event, data):
            item["class"] = data

        def oncolor():
            item["color"] = cp.color
            self.updatePalette()

        netw = self.width - 140
        tfvalue = v.TextField(label='Value:', value=item['value'], color=self.color, type="number", dense=True, style_="max-width: %dpx"%(int(0.25*netw)), class_="pa-0 ma-0 mt-2")
        tfvalue.on_event('input', onvalue)

        tfclass = v.TextField(label='Class:', value=item['class'], color=self.color, dense=True, style_="max-width: %dpx"%(int(0.74*netw)), class_="pa-0 ma-0 mt-2")
        tfclass.on_event('input', onclass)

        cp = colorPicker.colorPicker(color=item['color'], dark=self.dark, width=30, show_swatches=False, onchange=oncolor)

        sp = v.Html(tag='div', class_="pa-0 ma-0 mr-3", children=[''])

        return [ v.Row(class_="pa-0 ma-0 ml-2", no_gutters=True, children=[tfvalue, sp, tfclass, sp, cp.draw()]) ]


    # Manage onchange on the sortableList widget
    def __internal_onchange(self, arg=None):
        self.updatePalette()
        if self.onchange:
            self.onchange()


    # Returns the vuetify object to display
    def draw(self):
        """Returns the ipyvuetify object to display (a v.Html object displaying two output widgets)"""
        return v.Html(tag='div',children=[widgets.VBox([v.Html(tag='div',children=[''], class_='pa-0 ma-0 mb-2'),
                                                        widgets.HBox([self.outputtoolbar,self.outputdialog]),self.outputtitle,self.outputpalette,self.outputlist])])

    
    # colors property
    @property
    def colors(self):
        """
        Get/set the colors of the palette.
        
        Returns
        --------
        colorlist : list of strings in '#RRGGBB' format
            List of colors of the palette

        Example
        -------
        Get the edited palette colors::
            
            print(editor.colors)
        
        """
        return [x['color'] for x in self.s.items]


    # Set the colors
    @colors.setter
    def colors(self, colorlist):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        items = self.s.items
        for index,item in enumerate(items):
            item['color'] = colorlist[index%len(colorlist)]
        self.s.items = items
        dlg.close()
        
    
    # items property
    @property
    def items(self):
        """
        Get/set the items of the palette.
        
        Returns
        --------
        items : list of dicts
            List of dicts containing "value", "class" and "color"

        Example
        -------
        Print the edited palette items::
            
            print(editor.items)
        
        """
        return self.s.items

    
    # Set the items
    @items.setter
    def items(self, items):
        dlg = dialogWait.dialogWait(text='Updating palette...', output=self.outputdialog)
        self.s.items = items
        dlg.close()
        
        
    # title property
    @property
    def title(self):
        """
        Get/set the title of the palette.
        
        Returns
        --------
        t : str
            Title of the palette
        """
        return self.tfTitle.v_model

    
    # Set the title
    @title.setter
    def title(self, t):
        self.tfTitle.v_model = str(t)

        
    # interpolate property
    @property
    def interpolate(self):
        """
        Get/set the interpolate flag.
        
        Returns
        --------
        flag : bool
            Interpolate flag
        """
        return self.sw.value

    
    # Set the interpolate
    @interpolate.setter
    def interpolate(self, flag):
        self.sw.value = flag
        self.updatePalette()
        