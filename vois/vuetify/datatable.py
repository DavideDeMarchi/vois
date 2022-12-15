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
        If True the error and warning messages are displayed in white color, if False they are displayed in black (default is False)
            
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
    template = traitlets.Unicode('''
        <template>
        <v-card>
            <v-data-table
                dense
                hide-default-footer
                fixed-header
                :height="height"
                :headers="headers"
                :items="items"
                :item-key="index_col"
                :footer-props="{'items-per-page-options': [1000000]}"
            >
                <template v-slot:no-data> 
                  <v-alert :value="true" :color="color" :dark="dark" icon="mdi-alert">
                    No rows to display
                  </v-alert>
                </template>
                <template v-slot:no-results>
                    <v-alert :value="true" :color="color" :dark="dark" icon="mdi-alert">
                      Your search for "{{ search }}" found no results.
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
        </template>''').tag(sync=True)
    
    on_click = None  # This must receive a function which will be called inside `self.vue_cell_click()`

    def vue_cell_click(self, data):
        self.on_click(data)
    
    
    def __init__(self, *args, data=pd.DataFrame(), height='400px', on_click=None, **kwargs):
        super().__init__(*args, **kwargs)

        data = data.reset_index()
        self.index_col = data.columns[0]
        headers = [{"text": col, "value": col } for col in data.columns]
        headers[0].update({'align': 'left', 'sortable': True})
        self.headers = headers
        self.height = height
        self.on_click = on_click
        self.items = json.loads(data.to_json(orient='records'))
