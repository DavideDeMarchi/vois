"""Widget to manage the layers Table Of Content for a ipyleaflet Map"""
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
import ipyleaflet
import base64
import json

try:
    from jeodpp import inter
except:
    pass

try:
    from . import settings
    from . import sortableList
    from . import switch
    from . import tooltip
    from . import dialogGeneric
    from . import selectSingle
    from . import tabs
    from . import palettePicker
    from . import paletteEditor
    from . import upload
    from . import dialogWait
    from . import dialogMessage
except:
    import settings
    import sortableList
    import switch
    import tooltip
    import dialogGeneric
    import selectSingle
    import tabs
    import palettePicker
    import paletteEditor
    import upload
    import dialogWait
    import dialogMessage

    

#####################################################################################################################################################
# interapro Layer class
#####################################################################################################################################################
class interaproLayer():
    """
    A Layer to be visualized by interapro
    """

    def __init__(self,
                 name, visible=True, opacity=1.0,
                 path=None,
                 file=None,
                 epsg=None,
                 nodata=None,
                 colorfile=None,
                 colortable=None,
                 colormap=None,
                 valuemap=None,
                 colorscheme=None,
                 colorcustom=None,
                 scalemin=None,
                 scalemax=None,
                 interpolate=None,
                 bands=None,
                 rmin=None,
                 rmax=None,
                 gmin=None,
                 gmax=None,
                 bmin=None,
                 bmax=None):
        self.name        = str(name)
        self.visible     = bool(visible)
        self.opacity     = float(opacity)
        self.path        = path
        self.file        = file
        self.epsg        = epsg
        self.nodata      = nodata
        self.colorfile   = colorfile
        self.colortable  = colortable
        self.colormap    = colormap
        self.valuemap    = valuemap
        self.colorscheme = colorscheme
        self.colorcustom = colorcustom
        self.scalemin    = scalemin
        self.scalemax    = scalemax
        self.interpolate = interpolate
        self.bands       = bands
        self.rmin        = rmin
        self.rmax        = rmax
        self.gmin        = gmin
        self.gmax        = gmax
        self.bmin        = bmin
        self.bmax        = bmax
        
        
        self.colorscheme_reverse = False
        if not self.colorscheme is None:
            if self.colorscheme[:3] == 'inv':
                self.colorscheme_reverse = True
                self.colorscheme = self.colorscheme[3:]
                
        if self.interpolate is None or len(self.interpolate) == 0:
            self.interpolate = 'NEAREST'
        
        self.items  = []  # for discrete mode
        self.colors = []  # for continuous mode
        
        self.predefined = 0
        if not self.colormap is None:
            self.mode = 0   # discrete values
            self.getItems(self.colormap,self.valuemap)
        else:
            self.mode = 1   # continuous values
            if not self.colorcustom is None:
                self.predefined = 1
                self.colors = self.colorcustom.split(',')
            

    # Direct download of a .txt file containing a string
    def downloadText(self, textobj, output, fileName="layer.json"):
        string_bytes  = textobj.encode("ascii","ignore")
        base64_bytes  = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")

        output.clear_output()
        with output:
            display(HTML('<script>function downloadURI(uri, name) { var link = document.createElement("a"); link.download = name; link.href = uri; link.click();} downloadURI("data:application/octet-stream;charset=utf-8;base64,' + base64_string + '","' + fileName + '"); </script>'))
            
            
            
    # Calculate self.items from a colormap and a valuemap string
    def getItems(self, colormapstr, valuemapstr):
        self.items = []

        dcolor = {}
        dvalue = {}
        
        if colormapstr and len(colormapstr) > 0:
            try:
                dcolor = eval(colormapstr)
            except:
                dcolor = {}
                
        if valuemapstr and len(valuemapstr) > 0:
            try:
                dvalue = eval(valuemapstr)
            except:
                dvalue = {}
                
        for key,value in dcolor.items():
            item = { "value": key,  "class": "", "color": value }
            if key in dvalue:
                item["class"] = dvalue[key]
            self.items.append(item)
        
        
    # Return a ipyleaflet.TileLayer instance
    def tileLayer(self):
        """
        Return a ipyleaflet.TileLayer instance
        """
        if not self.path is None :
            if isinstance(self.path , str):
                coll = inter.Collection(eval(self.path))
            else:
                coll = inter.Collection(self.path)
        else:
            coll = inter.ImageCollection("SIMPLE")
            if not self.file is None:
                coll.parameter('file',self.file)
            if not self.epsg is None:
                coll.parameter('epsg',str(self.epsg))
            if not self.nodata is None:
                coll.parameter('nodata',str(self.nodata))
            if not self.colorfile is None and len(self.colorfile) > 0:
                coll.parameter('colorfile',str(self.colorfile))
            if not self.colortable is None and len(self.colortable) > 0:
                coll.parameter('colortable',str(self.colortable))
            if not self.colormap is None and len(self.colormap) > 0:
                coll.parameter('colormap',str(self.colormap))
            if not self.valuemap is None and len(self.valuemap) > 0:
                coll.parameter('valuemap',str(self.valuemap))
            if not self.colorscheme is None and len(self.colorscheme) > 0:
                coll.parameter('colorscheme',str(self.colorscheme))
            if not self.colorcustom is None and len(self.colorcustom) > 0:
                coll.parameter('colorcustom',str(self.colorcustom))
            if not self.scalemin is None:
                coll.parameter('scalemin',str(self.scalemin))
            if not self.scalemax is None:
                coll.parameter('scalemax',str(self.scalemax))
            if not self.interpolate is None:
                coll.parameter('interpolate',str(self.interpolate))
            if not self.bands is None:
                coll.parameter('bands',str(self.bands))
            if not self.rmin is None:
                coll.parameter('rmin',str(self.rmin))
            if not self.rmax is None:
                coll.parameter('rmax',str(self.rmax))
            if not self.gmin is None:
                coll.parameter('gmin',str(self.gmin))
            if not self.gmax is None:
                coll.parameter('gmax',str(self.gmax))
            if not self.bmin is None:
                coll.parameter('bmin',str(self.bmin))
            if not self.bmax is None:
                coll.parameter('bmax',str(self.bmax))

        p = coll.process()
        procid = p.toLayer()
        #p.printProcess()
        return ipyleaflet.TileLayer(name=self.name, visible=self.visible, opacity=self.opacity, url='https://jeodpp.jrc.ec.europa.eu/jeodpp-inter-view/?x={x}&y={y}&z={z}&procid=%s'%procid)
        
        
    # Save layer info into a dictionary (for downloading it as a .json file)
    def toDict(self):
        d = { "format": "BDAP layer 1.0" }
        
        if not self.path is None:
            d['path'] = str(self.path)
        else:
            if not self.file is None:
                d['file'] = self.file
            if not self.epsg is None:
                d['epsg'] = self.epsg
            if not self.nodata is None:
                d['nodata'] = self.nodata
            if not self.colorfile is None and len(self.colorfile) > 0:
                d['colorfile'] = self.colorfile
            if not self.colortable is None and len(self.colortable) > 0:
                d['colortable'] = self.colortable
            if not self.colormap is None and len(self.colormap) > 0:
                d['colormap'] = self.colormap
            if not self.valuemap is None and len(self.valuemap) > 0:
                d['valuemap'] = self.valuemap
            if not self.colorscheme is None and len(self.colorscheme) > 0:
                d['colorscheme'] = self.colorscheme
            if not self.colorcustom is None and len(self.colorcustom) > 0:
                d['colorcustom'] = self.colorcustom
            if not self.scalemin is None:
                d['scalemin'] = self.scalemin
            if not self.scalemax is None:
                d['scalemax'] = self.scalemax
            if not self.interpolate is None:
                d['interpolate'] = self.interpolate
            if not self.bands is None:
                d['bands'] = self.bands
            if not self.rmin is None:
                d['rmin'] = self.rmin
            if not self.rmax is None:
                d['rmax'] = self.rmax
            if not self.gmin is None:
                d['gmin'] = self.gmin
            if not self.gmax is None:
                d['gmax'] = self.gmax
            if not self.bmin is None:
                d['bmin'] = self.bmin
            if not self.bmax is None:
                d['bmax'] = self.bmax
                  
        return d

    
    # Load layer info from a dictionary (for uploading it from a .json file)
    def fromDict(self, d):
        self.name        = ''
        self.visible     = True
        self.opacity     = 1.0
        self.path        = None
        self.file        = None
        self.epsg        = None
        self.nodata      = None
        self.colorfile   = None
        self.colortable  = None
        self.colormap    = None
        self.valuemap    = None
        self.colorscheme = None
        self.colorcustom = None
        self.scalemin    = None
        self.scalemax    = None
        self.interpolate = None
        self.bands       = None
        self.rmin        = None
        self.rmax        = None
        self.gmin        = None
        self.gmax        = None
        self.bmin        = None
        self.bmax        = None
        
        if d['format'] == "BDAP layer 1.0":
            if 'path' in d and len(d['path']) > 0:
                self.path = d['path']
            else:
                if 'file' in d:
                    self.file = d['file']
                if 'epsg' in d:
                    self.epsg = d['epsg']
                if 'nodata' in d:
                    self.nodata = d['nodata']
                if 'colorfile' in d and len(d['colorfile']) > 0:
                    self.colorfile = d['colorfile']
                if 'colortable' in d and len(d['colortable']) > 0:
                    self.colortable = d['colortable']
                if 'colormap' in d and len(d['colormap']) > 0:
                    self.colormap = d['colormap']
                if 'valuemap' in d and len(d['valuemap']) > 0:
                    self.valuemap = d['valuemap']
                if 'colorscheme' in d and len(d['colorscheme']) > 0:
                    self.colorscheme = d['colorscheme']
                if 'colorcustom' in d and len(d['colorcustom']) > 0:
                    self.colorcustom = d['colorcustom']
                if 'scalemin' in d:
                    self.scalemin = d['scalemin']
                if 'scalemax' in d:
                    self.scalemax = d['scalemax']
                if 'interpolate' in d:
                    self.interpolate = d['interpolate']
                if 'bands' in d:
                    self.bands = d['bands']
                if 'rmin' in d:
                    self.rmin = d['rmin']
                if 'rmax' in d:
                    self.rmax = d['rmax']
                if 'gmin' in d:
                    self.gmin = d['gmin']
                if 'gmax' in d:
                    self.gmax = d['gmax']
                if 'bmin' in d:
                    self.bmin = d['bmin']
                if 'bmax' in d:
                    self.bmax = d['bmax']
                    
            self.colorscheme_reverse = False
            if not self.colorscheme is None:
                if self.colorscheme[:3] == 'inv':
                    self.colorscheme_reverse = True
                    self.colorscheme = self.colorscheme[3:]

            if self.interpolate is None or len(self.interpolate) == 0:
                self.interpolate = 'NEAREST'

            self.items  = []  # for discrete mode
            self.colors = []  # for continuous mode

            self.predefined = 0
            if not self.colormap is None:
                self.mode = 0   # discrete values
                self.getItems(self.colormap,self.valuemap)
            else:
                self.mode = 1   # continuous values
                if not self.colorcustom is None:
                    self.predefined = 1
                    self.colors = self.colorcustom.split(',')

    
    # Open a dialog-box to edit the layer
    def edit(self, output, outdebug, onok=None, oncancel=None):
        """
        Open a dialog-box to edit the layer
        """
        
        pconteditor = None
        outscheme  = widgets.Output(layout=Layout(width='90%', height='80px'))
        outpalette = widgets.Output(layout=Layout(width='90%', height='80px'))
        
        outdiscrete   = widgets.Output(layout=Layout(width='95%', height='130px'))
        outcontinuous = widgets.Output(layout=Layout(width='95%', height='130px'))

        btnEditDisc = v.Btn(icon=True, class_="pa-0 ma-0 mt-4", children=[v.Icon(children=['mdi-palette-outline'])])
        btnEditCont = v.Btn(icon=True, class_="pa-0 ma-0 mt-4", children=[v.Icon(children=['mdi-palette-outline'])])
        
        tf_colormap = v.TextField(label='Colormap:', v_model=self.colormap, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4", style_='width: 650px; max-width: 650px;')
        tf_valuemap = v.TextField(label='Valuemap:', v_model=self.valuemap, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4", style_='width: 650px; max-width: 650px;')
        
        
        # Selected a discrete palette
        def on_palette_discrete_ok():
            self.items = pconteditor.items
            tf_colormap.v_model = str(dict([ (x['value'],x['color']) for x in self.items]))
            tf_valuemap.v_model = str(dict([ (x['value'],x['class']) for x in self.items]))
                
        # Edit of a discrete palette
        def onEditDiscrete(widget, event, data): 
            nonlocal pconteditor
            #with outdebug:
            #    print(tf_colormap.v_model)
            self.getItems(tf_colormap.v_model,tf_valuemap.v_model)
            pconteditor = paletteEditor.paletteEditor(items=self.items, width=450, interpolate=False)
    
            dlg = dialogGeneric.dialogGeneric(title='Discrete palette editor', text='', show=True, 
                                              addclosebuttons=True, width=560, persistent=True, 
                                              addokcancelbuttons=True, on_ok=on_palette_discrete_ok,
                                              fullscreen=False, content=[pconteditor.draw()], output=output)
        
        # Selected a continuous palette
        def on_palette_continuous_ok():
            self.colors = pconteditor.colors
            outpalette.clear_output(wait=True)
            with outpalette:
                c = v.Card(outlined=True, class_="pa-0 ma-0 mt-3", style_='width: 400px; max-width: 400px; height: 40px; max-height: 40px;' ,
                               children=[v.Img(class_="pa-0 ma-1", src=palettePicker.image2Base64(palettePicker.paletteImage(self.colors, width=360, height=29, interpolate=True)))])
                display(widgets.HBox([c,spacer,tooltip.tooltip("Edit palette",btnEditCont)]))
        
        
        # Edit a continuous palette
        def onEditContinuous(widget, event, data):
            nonlocal pconteditor
            items = paletteEditor.colorlist2Items(self.colors)
            pconteditor = paletteEditor.paletteEditor(items=items, width=450, interpolate=True)
    
            dlg = dialogGeneric.dialogGeneric(title='Continuous palette editor', text='', show=True, 
                                              addclosebuttons=True, width=560, persistent=True, 
                                              addokcancelbuttons=True, on_ok=on_palette_continuous_ok,
                                              fullscreen=False, content=[pconteditor.draw()], output=output)
        
                
        btnEditDisc.on_event('click', onEditDiscrete)
        btnEditCont.on_event('click', onEditContinuous)
            
        spacer = v.Html(tag='div',children=[' '], style_='width: 15px;')
        
        outcolorschema = widgets.Output(layout=Layout(width='330px', height='66px'))

        layer_text = ''
        
        # Called when a .json file is selected for upload
        def on_upload_layer(files):
            nonlocal layer_text
            if len(files) > 0:
                f = files[0]
                layer_text = f['file_obj'].read().decode("utf-8")

                try:
                    j = json.loads(layer_text)
                    if ("format" in j) and (j["format"] == "BDAP layer 1.0"):
                        pass
                    else:
                        upload_file.clear()
                        e = dialogMessage.dialogMessage(title='Error',
                                                        text='The uploaded file is not in the \"BDAP layer 1.0\" format',
                                                        addclosebuttons=False, show=True, width=400, output=output)
                except:
                    upload_file.clear()
                    e = dialogMessage.dialogMessage(title='Error',
                                                    text='Cannot read the uploaded file!',
                                                    addclosebuttons=False, show=True, width=400, output=output)
            else:
                layer_text = ''
        
        upload_file = upload.upload(accept="application/json", multiple=False, show_progress=False, onchange=on_upload_layer,
                                    label='Layer file:', placeholder='Click to select the layer to upload', width='480px', margins="pa-0 ma-0 ml-4")
        
        # Display of the selected color scheme
        def display_colorschema(arg=None):
            outcolorschema.clear_output()
            if not self.colorscheme is None:
                with outcolorschema:
                    colorscheme = ss_colorscheme.value
                    if s_reverse.value:
                        colorscheme = 'inv' + colorscheme
                    display(HTML("<br/>"))
                    display(HTML(inter.colorSchemaLegend(colorscheme, Height=25)))
                
                
        # Save values from widgets to self. members
        def widgets2members():
            with outdebug:
                if len(tf_path.v_model) > 0:
                    try:
                        self.path = 'inter.' + tf_path.v_model.replace('inter.','')
                    except:
                        self.path = None
                else:
                    self.path = None
                self.name        = tf_name.v_model
                self.file        = tf_file.v_model
                self.epsg        = ss_epsg.value
                self.nodata      = float(tf_nodata.v_model)
                self.scalemin    = float(tf_scalemin.v_model)
                self.scalemax    = float(tf_scalemax.v_model)
                self.interpolate = ss_interpolate.value
                self.colorfile   = tf_colorfile.v_model
                self.colortable  = tf_colortable.v_model

                self.colorscheme_reverse = s_reverse.value
                if tmode.value == 0:  # Discrete
                    self.colormap = tf_colormap.v_model
                    self.valuemap = tf_valuemap.v_model
                else:                  # Continuous
                    self.colormap = None
                    self.valuemap = None

                    if tscheme.value == 0: # Predefined schemas
                        self.colorscheme = ss_colorscheme.value
                        if self.colorscheme_reverse:
                            self.colorscheme = 'inv' + self.colorscheme
                        self.colorcustom = None
                    else:                  # Custom palette
                        self.colorscheme = None
                        self.colorcustom = ','.join(self.colors)
            
                if s_rgb.value:
                    self.bands = str(ss_bandR.value) + '#' + str(ss_bandG.value) + '#' + str(ss_bandB.value)
                    self.rmin = float(tf_rmin.v_model)
                    self.rmax = float(tf_rmax.v_model)
                    self.gmin = float(tf_gmin.v_model)
                    self.gmax = float(tf_gmax.v_model)
                    self.bmin = float(tf_bmin.v_model)
                    self.bmax = float(tf_bmax.v_model)
                else:
                    self.bands = None
                    self.rmin = None
                    self.rmax = None
                    self.gmin = None
                    self.gmax = None
                    self.bmin = None
                    self.bmax = None
           
        
        # load self. members to widgets
        def members2widgets():
            with outdebug:
                pathvalue = ''
                if not self.path is None: pathvalue = str(self.path)
                tf_path.v_model = pathvalue

                tf_name.v_model       = self.name
                tf_file.v_model       = self.file
                ss_epsg.value         = self.epsg
                tf_nodata.v_model     = self.nodata
                tf_scalemin.v_model   = self.scalemin
                tf_scalemax.v_model   = self.scalemax
                ss_interpolate.value  = self.interpolate
                tf_colorfile.v_model  = self.colorfile
                tf_colortable.v_model = self.colortable

                tmode.value   = self.mode
                tscheme.value = self.predefined
                s_reverse.value = self.colorscheme_reverse
                if self.colormap and len(self.colormap) > 0:  # Discrete
                    tf_colormap.v_model = self.colormap
                    tf_valuemap.v_model = self.valuemap
                else:                  # Continuous
                    tf_colormap.v_model = None
                    tf_valuemap.v_model = None

                    if self.colorscheme and len(self.colorscheme) > 0: # Predefined schemas
                        if self.colorscheme[:3] == 'inv':
                            self.colorscheme_reverse = True
                            s_reverse.value = self.colorscheme_reverse
                            self.colorscheme = self.colorscheme[3:]
                        ss_colorscheme.value = self.colorscheme
            
                if self.bands and len(self.bands) > 0:
                    v = self.bands.split('#')
                    if len(v) >= 3:
                        ss_bandR.value = v[0]
                        ss_bandG.value = v[1]
                        ss_bandB.value = v[2]
                tf_rmin.v_model = self.rmin
                tf_rmax.v_model = self.rmax
                tf_gmin.v_model = self.gmin
                tf_gmax.v_model = self.gmax
                tf_bmin.v_model = self.bmin
                tf_bmax.v_model = self.bmax

                    
        # Exit with OK: update the values
        def edit_onok():
            widgets2members()
            if onok:
                onok()
                    
        
        # Manage rgb switch
        def on_rgb(arg=None):
            disabled = True
            if s_rgb.value: disabled = False
            ss_bandR.disabled = disabled
            ss_bandG.disabled = disabled
            ss_bandB.disabled = disabled
            tf_rmin.disabled = disabled
            tf_rmax.disabled = disabled
            tf_gmin.disabled = disabled
            tf_gmax.disabled = disabled
            tf_bmin.disabled = disabled
            tf_bmax.disabled = disabled
            

        # Control disable state when path is entered
        def onpathchanged(widget, event, data):
            disabled = False
            if tf_path.v_model and len(tf_path.v_model) > 0: disabled = True
            tf_file.disabled = disabled
            ss_epsg.disabled = disabled
            tf_nodata.disabled = disabled
            tf_scalemin.disabled = disabled
            tf_scalemax.disabled = disabled
            ss_interpolate.disabled = disabled
            tf_colorfile.disabled = disabled
            tf_colortable.disabled = disabled
            tscheme.disabled = disabled
            tmode.disabled = disabled
            ss_colorscheme.disabled = disabled
            s_reverse.disabled = disabled
            btnEditDisc.disabled = disabled
            btnEditCont.disabled = disabled
            tf_colormap.disabled = disabled
            tf_valuemap.disabled = disabled
            s_rgb.disabled = disabled

            if (not disabled) and (not s_rgb.value): disabled = True
            ss_bandR.disabled = disabled
            ss_bandG.disabled = disabled
            ss_bandB.disabled = disabled
            tf_rmin.disabled = disabled
            tf_rmax.disabled = disabled
            tf_gmin.disabled = disabled
            tf_gmax.disabled = disabled
            tf_bmin.disabled = disabled
            tf_bmax.disabled = disabled
            
            
        # Called when the file upload dialog is closed with the "OK" button
        def on_upload_ok():
            nonlocal layer_text
            
            if len(layer_text) > 2:
                dlg = dialogWait.dialogWait(text='Loading layer...', output=output)
                try:
                    d = json.loads(layer_text)
                    if ("format" in d)  and (d["format"] == "BDAP layer 1.0"):
                        self.fromDict(d)
                        members2widgets()
                    else:
                        e = dialogMessage.dialogMessage(title='Error',
                                                        text='The uploaded file is not in the \"BDAP layer 1.0\" format',
                                                        addclosebuttons=False, show=True, width=400, output=output)
                except:
                    e = dialogMessage.dialogMessage(title='Error',
                                                    text='Cannot read the uploaded file!',
                                                    addclosebuttons=False, show=True, width=400, output=output)

                dlg.close()

            layer_text = ''
            upload_file.clear()


            
        # Called when the file upload dialog is closed with the "cancel" button
        def on_upload_cancel():
            upload_file.clear()

        
        # Upload
        def onupload(widget, event, data):
            dlg = dialogGeneric.dialogGeneric(title='Load a layer from local disk', text='', show=True, 
                                              addclosebuttons=False, width=520,
                                              addokcancelbuttons=True, on_ok=on_upload_ok, on_cancel=on_upload_cancel,
                                              fullscreen=False, content=[upload_file.draw()], output=output)

        
        # Download
        def ondownload(widget, event, data):

            def on_ok():
                widgets2members()
                d = self.toDict()
                txt = json.dumps(d)
                filename = tf.v_model
                if filename[-5:] != ".json": filename += ".json"
                self.downloadText(txt, fileName=filename, output=output)

            tf = v.TextField(v_model="Layer", label="Layer file name", autofocus=True, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4")
                
            dlg = dialogGeneric.dialogGeneric(title='Save current layer to local disk', text='', show=True, 
                                              addclosebuttons=False, width=500,
                                              addokcancelbuttons=True, on_ok=on_ok,
                                              fullscreen=False, content=[tf], output=output)
            
        
        with outdebug:
            pathvalue = ''
            if not self.path is None: pathvalue = str(self.path)

            tf_name      = v.TextField(label='Layer name:',         v_model=self.name, color=settings.color_first, class_="pa-0 ma-0 mt-7 ml-4 mr-4", autofocus=True)
            btnupload    = v.Btn(icon=True, class_="mr-0", children=[v.Icon(children=['mdi-folder-open-outline'])])
            btndownload  = v.Btn(icon=True, class_="mr-0", children=[v.Icon(children=['mdi-content-save'])])
            btnupload.on_event('click', onupload)
            btndownload.on_event('click', ondownload)
            r0 = v.Row(no_gutters=True, justify="space-between", children=[tf_name, btnupload, btndownload], class_="pa-0 ma-0")

        
            tf_path        = v.TextField(label='Collections Path:',   v_model=pathvalue, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4")
            tf_path.on_event('input', onpathchanged)

            tf_file        = v.TextField(label='File:',               v_model=self.file, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4")
            ss_epsg        = selectSingle.selectSingle(label='Epsg:', values=['3857', '4326', '3035'], selection=str(self.epsg), width=180, newvalues_enabled=True, newvalues_type='number', clearable=False)
            tf_nodata      = v.TextField(label='Nodata:',             v_model=self.nodata,   type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 110px; max-width: 120px")
            tf_scalemin    = v.TextField(label='Scalemin:',           v_model=self.scalemin, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 110px; max-width: 120px")
            tf_scalemax    = v.TextField(label='Scalemax:',           v_model=self.scalemax, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 110px; max-width: 120px")
            ss_interpolate = selectSingle.selectSingle(label='Interpolation:',
                                                       values=['NEAREST', 'BILINEAR', 'CUBIC', 'CUBICSPLINE', 'LANCZOS', 'AVERAGE', 'MODE', 'MAX', 'MIN', 'MED'],
                                                       selection=self.interpolate, width=200, newvalues_enabled=False, clearable=False)
            r1             = v.Row(no_gutters=True, justify="space-between", children=[ss_epsg.draw(),tf_nodata, tf_scalemin, tf_scalemax, ss_interpolate.draw()], class_="pa-0 ma-0 ml-4 mr-4")
            tf_colorfile   = v.TextField(label='Color file:',         v_model=self.colorfile,  color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4")
            tf_colortable  = v.TextField(label='Color table file:',   v_model=self.colortable, color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4")

            coll = inter.ImageCollection("SIMPLE")
            colorschemes = coll.listColorSchemes()
            ss_colorscheme = selectSingle.selectSingle(label='Color scheme:', values=colorschemes, selection=self.colorscheme, width=220, newvalues_enabled=False, marginy=4, clearable=False, onchange=display_colorschema)
            s_reverse = switch.switch(self.colorscheme_reverse, 'Reverse color order', inset=True, dense=True, onchange=display_colorschema)
            
            tscheme = tabs.tabs(self.predefined, ['Predefined color schemes', 'Custom color palette'], contents=[outscheme,outpalette], row=True)
        
            display_colorschema()
                                 
            outscheme.clear_output(wait=True)
            with outscheme:
                display(widgets.HBox([ss_colorscheme.draw(),spacer,v.Row(no_gutters=True, justify="start", children=[s_reverse.draw()], class_="pa-0 ma-0 mt-3"),spacer,outcolorschema]))
           
        
            outpalette.clear_output(wait=True)
            with outpalette:
                c = v.Card(outlined=True, class_="pa-0 ma-0 mt-3", style_='width: 400px; max-width: 400px; height: 40px; max-height: 40px;' ,
                               children=[v.Img(class_="pa-0 ma-1", src=palettePicker.image2Base64(palettePicker.paletteImage(self.colors, width=360, height=29, interpolate=True)))])
                display(widgets.HBox([c,spacer,tooltip.tooltip("Edit palette",btnEditCont)]))
                
            outdiscrete.clear_output(wait=True)
            with outdiscrete:
                display(widgets.HBox([btnEditDisc,spacer,widgets.VBox([tf_colormap,tf_valuemap])]))
            
            outcontinuous.clear_output(wait=True)
            with outcontinuous:
                display(tscheme.draw())
                
            tmode = tabs.tabs(self.mode, ['Discrete values', 'Continuous values'], contents=[outdiscrete,outcontinuous], row=False)
            r2 = v.Row(no_gutters=True, justify="start", children=[tmode.draw()], class_="pa-0 ma-0 ml-4 mr-4")
            
            
            s_rgb = switch.switch(self.colorscheme_reverse, 'RGB', inset=True, dense=True, onchange=on_rgb)
            bands = [str(x) for x in range(1,11)]
            ss_bandR = selectSingle.selectSingle(label='R:', values=bands, selection="1", width=75, newvalues_enabled=True, newvalues_type='number', clearable=False)
            ss_bandG = selectSingle.selectSingle(label='G:', values=bands, selection="2", width=75, newvalues_enabled=True, newvalues_type='number', clearable=False)
            ss_bandB = selectSingle.selectSingle(label='B:', values=bands, selection="3", width=75, newvalues_enabled=True, newvalues_type='number', clearable=False)
            tf_rmin = v.TextField(label='Rmin:', v_model=self.rmin, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            tf_rmax = v.TextField(label='Rmax:', v_model=self.rmax, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            tf_gmin = v.TextField(label='Gmin:', v_model=self.gmin, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            tf_gmax = v.TextField(label='Gmax:', v_model=self.gmax, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            tf_bmin = v.TextField(label='Bmin:', v_model=self.bmin, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            tf_bmax = v.TextField(label='Bmax:', v_model=self.bmax, type='number', color=settings.color_first, class_="pa-0 ma-0 ml-4 mr-4 mt-2", style_="width: 65px; max-width: 65px")
            r3 = v.Row(no_gutters=True, justify="start", children=[s_rgb.draw(), spacer, ss_bandR.draw(),spacer,ss_bandG.draw(),spacer,ss_bandB.draw(),
                                                                   tf_rmin,tf_rmax,tf_gmin,tf_gmax,tf_bmin,tf_bmax], class_="pa-0 ma-0 ml-4 mr-4")
            on_rgb()
            
            dlg = dialogGeneric.dialogGeneric(title='Edit Layer', text='', show=True,
                                              addclosebuttons=False, width=1000, persistent=True,
                                              addokcancelbuttons=True, on_ok=edit_onok, on_cancel=oncancel,
                                              fullscreen=False, content=[r0, tf_path, tf_file, r1, tf_colorfile, tf_colortable, r2, r3], output=output)
        

#####################################################################################################################################################
# Layers TOC widget class
#####################################################################################################################################################
class layers():
    """
    Widget to manage the layers Table Of Content for a ipyleaflet Map

    Parameters
    ----------
    m : ipyleaflet.Map instance
        Map instance to connect to the layers widget
    color : str, optional
        Color to use for the widget (default is settings.color_first)
    dark : bool, optional
        If True, the widget will have a dark background (default is settings.dark_mode)
    width : int, optional
        Width of the widget in pixels (default is 320)

    Example
    -------
    Creation of a layers management widget::
        
        import ipyleaflet
        from jeodpp import inter, imap
        from ipywidgets import widgets, Layout

        from vois.vuetify import layers

        # Given a collection path returns a ipyleaflet.TileLayer
        def tileLayer(name, collectionpath):
            p = inter.Collection(collectionpath).process()
            procid = p.toLayer()
            return ipyleaflet.TileLayer(name=name, url='https://jeodpp.jrc.ec.europa.eu/jeodpp-inter-view/?x={x}&y={y}&z={z}&procid=%s'%procid)

        layer1 = tileLayer('Merit DEM',    inter.collections.BaseData.Elevation.MERIT.Hillshade)
        layer2 = tileLayer('Corine 2018',  inter.collections.BaseData.Landcover.CLC2018)
        layer3 = tileLayer('Gisco Labels', inter.collections.Basemaps.Gisco.OSMCartoLabels)

        height = 500
        m = imap.Map(layout=Layout(height='%dpx'%height))

        m.add_layer(layer1)
        m.add_layer(layer2)
        m.add_layer(layer3)

        ly = layers.layers(m, width=400, dark=False)

        display(widgets.HBox([ly.draw(),m]))

    .. figure:: figures/layers.png
       :scale: 100 %
       :alt: layers widget

       Example of a layers management widget
    """
    
    def __init__(self, m, color=settings.color_first, dark=settings.dark_mode, width=400):
        self.map    = m
        self.color  = color
        self.dark   = dark
        self.width  = width
        
        # Retrieve non-base layers from the map and assign a unique layerid
        self.layers = []
        self.nextlayerid = 0
        for index,layer in enumerate(self.map.layers):
            if not layer.base:
                self.layers.insert(0, { "name":     layer.name,
                                        "base":     layer.base,
                                        "visible":  layer.visible,
                                        "opacity":  layer.opacity,
                                        "mapindex": index,              # Index of the layer in the map
                                        "layerid":  self.nextlayerid})  # Unique layer identifier (unmutable)
                self.nextlayerid += 1

        # Calculate indexing of the layers: self.layerid2mapindex and self.mapindex2layerid
        self.indexLayers()

       
        # Create the sortableList widget
        self.s = sortableList.sortableList(items=self.layers, width=width, dark=dark,
                                           allowNew=True, newOnTop=True, buttonstooltip=True,
                                           itemNew=self.layerNew,
                                           itemContent=self.layerContent,
                                           onmovedown=self._onmovedown,
                                           onmoveup=self._onmoveup,
                                           onremoving=self._onremoving,
                                           onremoved=self._onremoved)
        
        self.outservice = widgets.Output(layout=Layout(width='0px', height='0px'))
        self.debug      = widgets.Output()

    # Calculate indexing of the layers: self.layerid2mapindex and self.mapindex2layerid
    def indexLayers(self):
        self.layerid2mapindex = {}
        self.mapindex2layerid = {}
        mapindex = len(self.layers)
        for layer in self.layers:
            layer['mapindex'] = mapindex
            mapindex -= 1
            self.layerid2mapindex[layer['layerid'] ] = layer['mapindex']
            self.mapindex2layerid[layer['mapindex']] = layer['layerid']
        
        
    # Manage movedown event
    def _onmovedown(self, index):
        a = self.layers[index]['mapindex']
        b = self.layers[index+1]['mapindex']
        layerlist = list(self.map.layers)
        layerlist[b], layerlist[a] = layerlist[a], layerlist[b]
        self.map.layers = tuple(layerlist)
        self.indexLayers()

    # Manage moveup event
    def _onmoveup(self, index):
        a = self.layers[index]['mapindex']
        b = self.layers[index-1]['mapindex']
        layerlist = list(self.map.layers)
        layerlist[b], layerlist[a] = layerlist[a], layerlist[b]
        self.map.layers = tuple(layerlist)
        self.indexLayers()

    # Manage pre-remove event
    def _onremoving(self, index):
        indexinmap = self.layers[index]['mapindex']
        self.map.layers = self.map.layers[:indexinmap] + self.map.layers[indexinmap+1:]
       
    # Manage post-remove event
    def _onremoved(self, index):
        self.indexLayers()

        
    # Add the new edited layer to the map
    def addNewLayer(self):
        with self.debug:
            mapindex = len(self.map.layers)
            layerid  = self.nextlayerid
            self.nextlayerid += 1

            # Define the new item of the sortableList
            newItem = { "name":     self.newlayer.name,
                        "base":     False,
                        "visible":  self.newlayer.visible,
                        "opacity":  self.newlayer.opacity,
                        "mapindex": mapindex,
                        "layerid":  layerid
                  }
            
            # Add the new item to the sortableList widget
            self.s.doAddItem(newItem)
            
            # Add the new layer to the map
            self.map.add_layer(self.newlayer.tileLayer())

            # Add element to the index dicts
            self.layerid2mapindex[layerid] = mapindex
            self.mapindex2layerid[mapindex] = layerid
            
        
        
    # Creation of a new layer
    def layerNew(self):
        self.newlayer = interaproLayer('Population 2020', visible=True, opacity=1.0,
                                       file='/eos/jeodpp/data/base/Population/GLOBAL/WorldPop/VER1-0/Data/VRT/MOSAIC_ppp_prj_2020.vrt',
                                       epsg=4326,
                                       nodata=-99999.0,
                                       colorscheme='RdYlGn_mixed',
                                       scalemin=0.0,
                                       scalemax=15.0)
        self.newlayer.edit(self.outservice, self.debug, onok=self.addNewLayer)
        return None
            

    
    # Content of a layer
    def layerContent(self, layer, index):
        
        # Toggle visibility of the layer
        def onvisible(flag):
            layerid  = layer['layerid']
            mapindex = self.layerid2mapindex[layerid]
            layer['visible'] = not layer['visible']
            self.map.layers[mapindex].visible = layer['visible']
        
        # Change opacity of a layer
        def onopacity(widget, event, data):
            layerid  = layer['layerid']
            mapindex = self.layerid2mapindex[layerid]
            layer['opacity'] = opacity.v_model/10.0
            self.map.layers[mapindex].opacity = layer['opacity']
            
            
        visible = switch.switch(layer['visible'], '', onchange=onvisible, inset=True, dense=True)
        
        opacity = v.Slider(v_model=int(10*layer['opacity']),
                           dense=True, xsmall=True, 
                           ticks=True, thumb_size=10, dark=self.dark,
                           color=self.color, track_color="grey",
                           class_="pa-0 ma-0 ml-5 mr-5 mt-3 mb-n1",
                           style_='max-width: 140px; width: 140px;',
                           min=0, max=10, vertical=False, height=32)
        opacity.on_event('input', onopacity)
        htmlopacity = v.Card(dark=self.dark, children=[v.Html(tag='div', children=[opacity], style_='overflow: hidden;')])

        m = v.Menu(offset_y=True, open_on_hover=False, dense=True, dark=self.dark, 
                   v_slots=[{
                            'name': 'activator',
                            'variable': 'menuData',
                            'children': v.Btn(v_on='menuData.on', icon=True, depressed=True, 
                                              large=False, dense=True, class_='pa-0 ma-0',
                                              children=[v.Icon(color='#aaaaaa', children=['mdi-opacity'])]),
                           }],
                   children=[htmlopacity] )
        
        bcolor = v.Btn(icon=True, depressed=True, 
                       large=False, dense=True, class_='pa-0 ma-0',
                       children=[v.Icon(color='#aaaaaa', children=['mdi-palette-outline'])])
        
        name = v.CardSubtitle(class_="pa-0 ma-0 ml-1 mt-2 mb-2", children=[layer['name']])

        spacer  = v.Html(tag='div',children=[' '], style_='width: 3px; height: 44px;')
        
        return [ v.Row(class_="pa-0 ma-0", no_gutters=True, 
                       children=[tooltip.tooltip('Hide/Show the layer', visible.draw()),
                                 tooltip.tooltip('Layer colors',bcolor),
                                 spacer,
                                 tooltip.tooltip('Layer opacity',m),
                                 spacer,
                                 name]) ]

    
    # Returns the vuetify object to display (the treeview widget)
    def draw(self):
        """Returns the ipyvuetify object to display (the internal card containing the widgets)"""
        #return widgets.VBox([self.outservice, self.s.draw()])
        return widgets.VBox([self.outservice, self.s.draw(), self.debug])