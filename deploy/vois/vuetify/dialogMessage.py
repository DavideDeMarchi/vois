"""Dialog-box to display a message for the user."""
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
    from . import dialogGeneric
except:
    import dialogGeneric

#####################################################################################################################################################
# Display a dialog containing a simple message with a title
#####################################################################################################################################################
class dialogMessage(dialogGeneric.dialogGeneric):
    """
    Dialog-box to display a message for the user.
    
    Derived class from dialogGeneric.dialogGeneric.
        
    Parameters
    ----------
    title : str, optional
        Title of the dialog-box to be displayed in the top toolbar (default is '')
    text : str, optional
        Text to display on top of the dialog-box body (default is '')
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    show : bool, optional
        Flag to immediately show the dialog-box upon creation (default is False)
    width : int or str, optional
        Width of the dialog-box. If an integer is passed the width is intended in pixels. Default is 500 pixels
    addclosebuttons : bool, optional
        If True, the dialog will have a 'close' button in the top toolbar (default is True)
    transition : str, optional
        Transition to use for the dialog display and close (default is 'dialog-fade-transition'). See: https://vuetifyjs.com/en/styles/transitions/ for a list of available transitions (substitute 'v-' with 'dialog-')
    output : ipywidgets.Output, optional
        Output widget on which the widget has to be displayed
    titleheight : str, optional
        Height of the title toolbar. It can be: 'prominent', 'dense', 'extended' or a value in pixels (default is 'dense')
            
    Example
    -------
    Creation and display of a modal dialog-box containing an error message::
        
        from vois.vuetify import dialogMessage
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        e = dialogMessage.dialogMessage(title='Error',
                                        text='''Sorry but the task could not be completed<br>
        because there are errors in the code to save in PNG format''',
                                        addclosebuttons=False,
                                        show=True, width=450, output=output)
                              
    .. figure:: figures/dialogMessage.png
       :scale: 100 %
       :alt: dialogMessage widget

       Example of a dialogMessage to display an error message to the user.
   """
        
    def __init__(self, *args, **kwargs):
        
        text = kwargs['text'].replace('<br>','\n')
        vvv = text.split('\n')
        
        # Create the content to pass to the dialogGeneric
        if len(vvv) > 0:
            ctexts = [ v.CardText(children=[vvv[0]], class_="mt-1") ] + [ v.CardText(children=[x], class_="mt-n8") for x in vvv[1:] ]
            kwargs['content'] = [v.Card(children=ctexts)]
            
        kwargs['text'] = ''
        kwargs['fullscreen'] = False
        #kwargs['addclosebuttons'] = True
        
        super().__init__(*args, **kwargs)

