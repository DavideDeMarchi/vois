"""General settings for ipyvuetify widgets."""
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

#########################################################################################################################################
# Graphical settings for vuetify widgets
#########################################################################################################################################

# Main settings
dark_mode = False            # If False then the foreground color is 'black', otherwise it is 'white'
"""
Flag to control the dark_mode of all the vuetify widgets.

If this flag is False, the foreground color used for text is 'black, otherwise it is 'white'
"""


button_rounded = True             # If True the buttons have rounded borders
"""
Flag to control the appearance of all button widgets (also in the toggle module or inside the title and footer bars).

If True, the buttons will have rounded borders, if False, the buttons will have squared borders. 

The :py:class:`button.button` class has an optional parameter **rounded** that can be used to force a single button to be rounded or squared. This setting will have influence on all the buttons created without expliciting setting the **rounded** parameter. 

Example of changing the appearance of all buttons to be rounded::

    from vois.vuetify import settings, button
    settings.button_rounded = True

    import importlib
    importlib.reload(button)

    b = button.button('Round button', width=200, selected=True)
    display(b.draw())

.. figure:: figures/RoundButton.png
   :scale: 100 %
   :alt: RoundButton

   Example of a round button


Example of changing the appearance of all buttons to be squared::

    from vois.vuetify import settings, button
    settings.button_rounded = False

    import importlib
    importlib.reload(button)

    b = button.button('Squared button', width=200, selected=True)
    display(b.draw())

.. figure:: figures/SquaredButton.png
   :scale: 100 %
   :alt: RoundButton

   Example of a squared button

.. note::

    The usage of **importlib.reload** is needed to reload the button module after the settings.button_rounded flag is changed

"""


color_first = '#f8bd1a'        # Primary color (for instance used for selected buttons)
"""
Primary color to be used for all the widgets of the vuetify package (for instance the buttons that have the selected state True will have this color as background color)

"""


color_second = '#efefef'        # Secondary color (for instance used for buttons not selected)
"""
Secondary color to be used for all the widgets of the vuetify package (for instance the buttons that have the selected state False will have this color as background color)
"""


textcolor_dark       = 'white'    # Text color when the background is dark
textcolor_notdark    = 'black'    # Text color when the background is not dark

tooltip_backcolor    = '#999999'  # Back color for tooltips


dark_background      = '#1e1e1e'  # Back color when dark mode is True

# Colors YELLOW
#color_first  = '#f8bd1a'     # Primary color (for instance used for selected buttons)
#color_second = '#efefef'     # Secondary color (for instance used for buttons not selected)

# Colors BLU
#color_first  = '#2196f3'     # Primary color (for instance used for selected buttons)
#color_second = '#95cffb'     # Secondary color (for instance used for buttons not selected)

# Colors GREEN
#color_first  = '#b7ec1c'     # Primary color (for instance used for selected buttons)
#color_second = '#9ebf00'     # Secondary color (for instance used for buttons not selected)

# Colors BLU EUROPEAN COMMISSION
#color_first  = '#254aa5'     # Primary color (for instance used for selected buttons)
#color_second = '#254aa5'     # Secondary color (for instance used for buttons not selected)


# Other derived settings
select_textcolor = textcolor_notdark

# Color for text on labels
label_textcolor  = select_textcolor

# Color of lines
line_color = select_textcolor


