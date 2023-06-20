"""Dialog-box to ask a yes-no question to the user."""
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
from IPython.display import display
import ipyvuetify as v

try:
    from . import settings
    from . import tooltip
    from . import dialogGeneric
except:
    import settings
    import tooltip
    import dialogGeneric

    
    
#####################################################################################################################################################
# Display a dialog having "yes" and "no" buttons
#####################################################################################################################################################
class dialogYesNo(dialogGeneric.dialogGeneric):
    """
    Dialog-box to ask a yes-no question to the user.
    
    Derived class from dialogGeneric.dialogGeneric.
        
    Parameters
    ----------
    title : str, optional
        Title of the dialog-box to be displayed in the top toolbar (default is '')
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    show : bool, optional
        Flag to immediately show the dialog-box upon creation (default is False)
    width : int or str, optional
        Width of the dialog-box. If an integer is passed the width is intended in pixels. Default is 500 pixels
    addclosebuttons : bool, optional
        If True, the dialog will have a 'close' button in the top toolbar (default is True)
    transition : str, optional
        Transition to use for the dialog display and close (default is 'dialog-fade-transition'. See: https://vuetifyjs.com/en/styles/transitions/ for a list of available transitions (substitute 'v-' with 'dialog-'')
    output : ipywidgets.Output, optional
        Output widget on which the widget has to be displayed
    titleheight : str, optional
        Height of the title toolbar. It can be: 'prominent', 'dense', 'extended' or a value in pixels (default is 'dense')
    on_yes : function, optional
        Python function to call when the user clicks on the YES button. The function will receive no parameters (default is None)
    on_no : function, optional
        Python function to call when the user clicks on the NO button. The function will receive no parameters (default is None)
            
    Example
    -------
    Creation and display of a Yes-No dialog box::
        
        from vois.vuetify import dialogYesNo
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def on_yes():
            with output:
                print('YES')

        def on_no():
            with output:
                print('NO')

        dlg = dialogYesNo.dialogYesNo(title='Question',
                                      text='Confirm removal of the selected file?',
                                      titleheight=40, width=400, output=output,
                                      show=True, transition='dialog-bottom-transition',
                                      on_yes=on_yes, on_no=on_no)
                              
    .. figure:: figures/dialogYesNo.png
       :scale: 100 %
       :alt: dialogYesNo widget

       Example of a dialogYesNo to ask a yes-no question to the user.
   """
        
    def __init__(self, on_yes=None, on_no=None, *args, **kwargs):
        
        self.on_yes = on_yes
        self.on_no  = on_no
        
        # Create yes and no buttons
        byes = v.Btn(text=True, children=['Yes'])
        byes.on_event('click', self.__internal_on_yes)
        byes = tooltip.tooltip('Answer YES and close',byes)

        bno = v.Btn(text=True, children=['No'])
        bno.on_event('click', self.__internal_on_no)
        bno = tooltip.tooltip('Answer NO and close',bno)
        
        r = v.Row(no_gutters=True, justify="end", children=[byes,bno])
        
        # Create the content to pass to the dialogGeneric
        kwargs['content'] = [v.Html(tag='div', class_="pa-0 ma-4 mt-4 mb-2", children=[kwargs['text']]), r]
        kwargs['text'] = ''
        kwargs['fullscreen'] = False
        kwargs['persistent'] = True
        
        super().__init__(*args, **kwargs)

    # Cliked yes
    def __internal_on_yes(self,*args):
        self.dialog.v_model = False
        if not self.on_yes is None:
            self.on_yes()

    # Cliked no
    def __internal_on_no(self,*args):
        self.dialog.v_model = False
        if not self.on_no is None:
            self.on_no()
        