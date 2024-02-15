"""Display of a Pandas DataFrame in a data-table widget."""
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
import traitlets
import pandas as pd
import json

# DataTable managing click on a row. See https://github.com/mariobuikhuizen/ipyvuetify/issues/163
class datatable(v.VuetifyTemplate):
    """
    Display of a Pandas DataFrame in a data-table widget.
        
    Parameters
    ----------
    data : Pandas DataFrame, optional
        Pandas DataFrame to be displayed (default is pd.DataFrame() empty DataFrame)
    height : str, optional
        Height of the data-table widget (default is '400px')
    on_click : function, optional
        Python function to call when the user clicks on one of the rows of the data-table. The function will receive a parameter of type dict containing all the column names as keys and the clicked row data as values
    color : str, optional
        Color to use for the display of alert and warning messages (for instance if no records are present in input DataFrame) (default is 'error')
    dark : bool, optional
        If True, the error and warning messages are displayed in white color, if False they are displayed in black (default is False)
    searchshow : bool, optional
        If True, on top of the table a search field will be displayed, allowing for search (default is False)
    search : str, optional
        Initial search string to be displayed in the search field (default is ''). If searchshow is False, this argument will not be used
    title : str, optional
        In case searchshow is True, a Title can be shown on top of the datatable (default is '')
    icon : str, optional
        In case searchshow is True, an icon can be shown on the right of the datatable title (default is '')
    icon_tooltip : str, optional
        Tooltip string to be used for the icon (default is '')
    icon_color : str, optional
        Color of the icon (default is 'grey')
    icon_disabled : bool, optional
        If True, the icon will be disabled (default is False)
    font_size : str, optional
        Font size to use for the rows and headers of the datatable (default is '14px')
    font_size_title : str, optional
        Font size to use for the title of the datatable (default is '16px')
    on_icon : function, optional
        Python function to call when the user clicks on the icon on the top of the data-table. The function will receive no parameters
    unsortable_columns : list of str, optional
        List of names of columns that must not be sortable in the datatable (please note that the DataFrame column names will be displayed in capital letters in the datatable: use in this list the original column names of the DataFrame and not the capitalized names)

    Example
    -------
    Creation of a Pandas DataFrame from the 'Our World In Data' dataset on Covid-19 daily data and display of last 100 days for Italy::
        
        from vois.vuetify import datatable
        import pandas as pd
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()

        df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

        def on_click(data):
            output.clear_output()
            with output:
                print(data)

        df = df[df['location']=='Italy']
        d = datatable.datatable(data=df.tail(100), height='500px', on_click=on_click)

        display(d)
        display(output)

    .. figure:: figures/datatable.png
       :scale: 100 %
       :alt: datatable widget

       Last 100 days of Covid-19 data on Italy displayed in a datatable widget
    """
    
    headers = traitlets.List([]).tag(sync=True, allow_null=True)
    items = traitlets.List([]).tag(sync=True, allow_null=True)
    index_col = traitlets.Unicode('').tag(sync=True)
    height = traitlets.Unicode('400px').tag(sync=True)
    color = traitlets.Unicode('error').tag(sync=True)  # Color for error message in case of empty input DF
    dark = traitlets.Bool(False).tag(sync=True)
    
    searchshow = traitlets.Bool(False).tag(sync=True)
    title      = traitlets.Unicode('').tag(sync=True)
    search     = traitlets.Unicode('').tag(sync=True)
    
    icon          = traitlets.Unicode('').tag(sync=True)
    icon_tooltip  = traitlets.Unicode('').tag(sync=True)
    icon_color    = traitlets.Unicode('grey').tag(sync=True)
    icon_disabled = traitlets.Bool(False).tag(sync=True)
    
    font_size       = traitlets.Unicode('14px').tag(sync=True)
    font_size_title = traitlets.Unicode('16px').tag(sync=True)
    
    @traitlets.default('template')
    def _template(self):
        
        if self.searchshow:
            
            stricon = ''
            if len(self.icon) > 0:
                stricon = '''
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon @click="onicon()" :disabled="icon_disabled" color="%s" v-on="on"><v-icon small>%s</v-icon></v-btn>
      </template>
      <span>%s</span>
    </v-tooltip>
'''% (self.icon_color, self.icon, self.icon_tooltip)

                
            cardtitle = '''
            <v-card-title class="pa-0 ma-0 ml-2 mb-1" style="font-size: %s;">
              %s
              %s
              <v-spacer></v-spacer>
              <v-text-field class="pa-0 ma-0 mb-3" v-model="search" :color="color" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
            </v-card-title>
            ''' % (self.font_size_title, self.title, stricon)
        else:
            cardtitle = ''
        
        return '''
        <template>
        <v-card>
            %s
            <v-data-table
                dense
                hide-default-footer
                fixed-header
                :search="search"
                :height="height"
                :headers="headers"
                :items="items"
                :item-key="index_col"
                :footer-props="{'items-per-page-options': [10000000]}">
                <template v-slot:no-data> 
                  <v-alert :value="true" :color="color" :dark="dark" icon="mdi-alert">
                    No records to display
                  </v-alert>
                </template>
                <template v-slot:no-results>
                    <v-alert :value="true" :color="color" :dark="dark" icon="mdi-alert" width="80vw">
                      Your search for "{{ search }}" found no results
                    </v-alert>
                </template>

                <template v-slot:item="row">
                  <tr>
                    <td v-for="value in Object.values(row.item)"
                        @click="cell_click(row.item)"
                    >
                      {{ value }}
                    </td>
                  </tr>
                </template>

            </v-data-table>
          </v-card>
        </template>

<style>
.v-data-table > .v-data-table__wrapper > table > tbody > tr > th,
.v-data-table > .v-data-table__wrapper > table > thead > tr > th,
.v-data-table > .v-data-table__wrapper > table > tfoot > tr > th,
.v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
   font-size: %s !important;
}
</style>
''' % (cardtitle, self.font_size)
    
    on_click = None  # This must receive a function which will be called inside `self.vue_cell_click()`

    # Click on the "icon" button
    def vue_onicon(self, data):
        if not self.on_icon is None:
            self.on_icon()
    
    # Click on one row of the datatable
    def vue_cell_click(self, data):
        if not self.on_click is None:
            self.on_click(data)
    
    # Initializing
    def __init__(self, *args,
                 data=pd.DataFrame(),
                 height='400px',
                 title='',
                 dictwidth={},
                 searchshow=False,
                 search='',
                 on_click=None, 
                 on_icon=None,
                 icon='',
                 icon_tooltip='',
                 icon_color='grey',
                 icon_disabled=False,
                 font_size='14px',
                 font_size_title='16px',
                 unsortable_columns=[],
                 **kwargs):
        
        self.title = title
        self.searchshow = searchshow
        self.search = search
        
        data = data.reset_index()
        self.index_col = data.columns[0]
       
        #headers = [{"text": col, "value": col } for col in data.columns]
        headers = []
        for col in data.columns:
            
            sortable = True
            if col in unsortable_columns: 
                sortable = False
                
            h = {"text": str(col).upper(), "value": col, "sortable": sortable}
            
            if col in dictwidth:
                h["width"] = dictwidth[col]
            else:
                h["width"] = "20px"
            headers.append(h)
        #print(headers)
        
        self.headers = headers
        self.height = height
        self.on_click = on_click
        self.on_icon = on_icon
        self.icon = icon
        self.icon_tooltip = icon_tooltip
        self.icon_color = icon_color
        self.icon_disabled = icon_disabled
        self.font_size = font_size
        self.font_size_title = font_size_title
        self.items = json.loads(data.to_json(orient='records'))

        super().__init__(*args, **kwargs)
