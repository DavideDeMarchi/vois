"""Generic modal dialog-box to ask input from the user."""
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
    from . import tooltip
    from . import settings
except:
    import tooltip
    import settings
    

#####################################################################################################################################################
# Display a generic dialog with a close button (and possibly fullscreen)
#####################################################################################################################################################
class dialogGeneric():
    """
    Generic modal dialog-box to ask input from the user.
        
    Parameters
    ----------
    title : str, optional
        Title of the dialog-box to be displayed in the top toolbar (default is '')
    text : str, optional
        Text to display on top of the dialog-box body (default is '')
    color: str, optional
        Color of the title bar of the dialog (default is settings.color_first)
    dark : bool, optional
        Flag that controls the color of the text in foreground (if True, the text will be displayed in white, elsewhere in black)
    show : bool, optional
        Flag to immediately show the dialog-box upon creation (default is False)
    content: list of ipyvuetify widgets, optional
        List of ipyvuietify widgets to be displayed in the body of the dialog-box (default is [])
    width : int or str, optional
        Width of the dialog-box. If an integer is passed the width is intended in pixels. Default is 500 pixels
    fullscreen : bool, optional
        If True, the dialog-box is opened in fullscreen mode (default is False)
    persistent : bool, optional
        If True, clicking outside of the dialog or pressing esc key will not deactivate it (default is False)
    no_click_animation : bool, optional
        If True, disables the bounce effect when clicking outside of a dialog's content when using the persistent property (default is False)
    addclosebuttons : bool, optional
        If True, the dialog will have a 'close' button in the top toolbar (default is True)
    addokcancelbuttons : bool, optional
        If True, the dialog will have 'ok' and 'cancel' buttons in the bottom row (default is False)
    on_ok : function, optional
        Python function to call when the user clicks on the OK button. The function will receive no parameters (default is None)
    on_cancel : function, optional
        Python function to call when the user clicks on the CANCEL button. The function will receive no parameters (default is None)
    on_close : function, optional
        Python function to call when the user clicks on the CLOSE button. The function will receive no parameters (default is None)
    transition : str, optional
        Transition to use for the dialog display and close (default is 'dialog-fade-transition'. See: https://vuetifyjs.com/en/styles/transitions/ for a list of available transitions (substitute 'v-' with 'dialog-'')
    output : ipywidgets.Output, optional
        Output widget on which the widget has to be displayed
    titleheight : str, optional
        Height of the title toolbar. It can be: 'prominent', 'dense', 'extended' or a value in pixels (default is 'dense')
    custom_icon : str, optional
        Name of the optional icon to display in the top toolbar (default is '')
    custom_tooltip : str, optional
        Tooltip to display when hovering on the custom icon in the top toolbar (default is '')
    custom_icon_onclick : function, optional
        Python function to call when the user clicks on the custom icon on the topbar. The function will receive no parameters (default is None)
            
    Example
    -------
    Creation and display of a modal dialog-box containing a switch widget::
        
        from vois.vuetify import dialogGeneric, switch
        from ipywidgets import widgets
        from IPython.display import display

        output = widgets.Output()
        display(output)

        def on_s_change(value):
            with output:
                print(value)

        s = switch.switch(True, 'PNG format', onchange=on_s_change)

        dlg = dialogGeneric.dialogGeneric(title='Settings',
                                          text='Please select the format for download:',
                                          show=True, addclosebuttons=True, width=600, 
                                          fullscreen=False, content=[s.draw()], output=output)
                                  
    .. figure:: figures/dialogGeneric.png
       :scale: 100 %
       :alt: dialogGeneric widget

       Example of a dialogGeneric containing a switch widget.
   """
        
    def __init__(self, title='', text='', color=settings.color_first, dark=settings.dark_mode, show=False, content=[], width=500, fullscreen=False,
                 persistent=False, no_click_animation=False, 
                 addclosebuttons=True, addokcancelbuttons=False, on_ok=None, on_cancel=None, on_close=None,
                 transition='dialog-fade-transition', output=None, titleheight="dense", customclass="",
                 custom_icon='', custom_tooltip='', custom_icon_onclick=None):
        
        self.on_ok     = on_ok
        self.on_cancel = on_cancel
        self.on_close  = on_close
        
        self.custom_icon_onclick = custom_icon_onclick
        
        text = text.replace('<br>','\n')
        vvv = text.split('\n')

        if dark:
            buttontext = settings.textcolor_dark
            styletext = 'color: ' + settings.textcolor_dark + ';'
        else:
            buttontext = settings.textcolor_notdark
            styletext = 'color: ' + settings.textcolor_notdark + ';'

        # Close button
        if addclosebuttons:
            bclose = v.Btn(text=True, children=['Close'], color=buttontext)
            bclose.on_event('click', self.close)
            bclose = tooltip.tooltip('Close the dialog',bclose)
        else:
            bclose = ''

        # Close X button
        if addclosebuttons:
            bx = v.Btn(icon=True, children=[v.Icon(children=['mdi-close'])], color=buttontext)
            bx.on_event('click', self.close)
            bx = tooltip.tooltip('Close the dialog',bx)
        else:
            bx = ''

        # Custom icon on the top toolbar
        if len(custom_icon) > 0:
            bi = v.Btn(icon=True, children=[v.Icon(children=[custom_icon])], color=buttontext)
            bi.on_event('click', self.oncustomicon)
            if len(custom_tooltip) > 0:
                bi = tooltip.tooltip(custom_tooltip,bi)
        else:
            bi = ''
            
            
        # OK and Cancel buttons
        if addokcancelbuttons:
            self.bok = v.Btn(text=True, children=['OK'])
            self.bok.on_event('click', self.__internal_on_ok)

            self.bcancel = v.Btn(text=True, children=['Cancel'])
            self.bcancel.on_event('click', self.__internal_on_cancel)

            r = [v.Row(no_gutters=True, justify="end", class_="pa-0 ma-0 mt-4", children=[self.bok,self.bcancel])]
        else:
            self.bok     = None
            self.bcancel = None
            r = []
            
        # Toolbar
        ttitle  = v.ToolbarTitle(children=[title], style_=styletext)
        spacer  = v.Spacer()
        titems  = v.ToolbarItems(children=[bi,bclose])
        toolbar = v.Toolbar(height=titleheight, dark=dark, color=color, children=[bx,ttitle,spacer,titems])
        
        # Dialog
        clist = [toolbar]
        if len(text) > 0:
            clist += [ v.CardText(class_='pa-0 ma-0 mt-9', children=['']) ]
            clist += [ v.CardText(children=[x], class_="mt-n5") for x in vvv ]
        clist += content + r
        
        if type(width)==int:
            swidth = "%dpx"%width
        else:
            swidth = str(width)
        self.dialog = v.Dialog(width=swidth, v_model=show, fullscreen=fullscreen, transition=transition,
                               persistent=persistent, no_click_animation=no_click_animation,
                               style_="background-color: transparent; z-index:20001;", 
                               content_class=customclass,
                               children=[v.Card(children=clist)])
        
        # Display of the dialog
        if not output is None:
            with output:
                display(self.dialog)
                
        
    # Open the dialog
    def show(self):
        """Open the dialog."""
        self.dialog.v_model = True

    # Close the dialog
    def close(self, *args):
        """Close the dialog."""
        self.dialog.v_model = False
        if not self.on_close is None:
            self.on_close()

    # Click on the custom icon
    def oncustomicon(self, *args):
        if not self.custom_icon_onclick is None:
            self.custom_icon_onclick()
        

    # Cliked ok
    def __internal_on_ok(self,*args):
        self.dialog.v_model = False
        if not self.on_ok is None:
            self.on_ok()

    # Cliked cancel
    def __internal_on_cancel(self,*args):
        self.dialog.v_model = False
        if not self.on_cancel is None:
            self.on_cancel()

    # Enable/disable the ok button
    @property
    def okdisabled(self):
        """
        Get/Set the disabled status of the ok button.
        
        Returns
        --------
        flag : bool
            True if the ok button is disabled, False otherwise

        Example
        -------
        Programmatically set the disabled status and print it::
            
            dlg.okdisabled = True
            print(dlg.okdisabled)
        
        """
        if self.bok is None:
            return True
        else:
            return self.bok.disabled
    
    
    # Set the disabled status of the ok button
    @okdisabled.setter
    def okdisabled(self, flag):
        if not self.bok is None:
            self.bok.disabled = bool(flag)
        