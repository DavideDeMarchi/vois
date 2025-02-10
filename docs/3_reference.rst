.. image:: figures/vois_horizontal_small.png

|

.. _Reference:

Reference manual
================

Setup
-----

The vois library can be installed by executing: **pip install vois**


Packages
--------

The vois library is grouped in these packages:

+----------------------------------+-----------------------------------------------------------------------+
| :ref:`General package <General>` | Contains modules that define utilities functions and classes of       |
|                                  |                                                                       |
|                                  | general use (geojson, maps, svg, etc.)                                |
+----------------------------------+-----------------------------------------------------------------------+
| :ref:`Vuetify package <Vuetify>` | Contains modules that define classes to simplify the creation of      |
|                                  |                                                                       |
|                                  | GUI elements using ipyvuetify widgets                                 |
+----------------------------------+-----------------------------------------------------------------------+
| :ref:`Geo package <Geo>`         | Contains modules that enable the display of geospatial content on an  |
|                                  |                                                                       |
|                                  | interactive Map                                                       |
+----------------------------------+-----------------------------------------------------------------------+
     
     
.. _General:

General package
^^^^^^^^^^^^^^^

 The **General** package is made up of these modules:
 
 
.. autosummary::
    :nosignatures:

 colors
 download
 eucountries
 geojsonUtils
 interMap
 ipytrees
 leafletMap
 svgBarChart
 svgBubblesChart
 svgGraph
 svgHeatmap
 svgMap
 svgPackedCirclesChart
 svgRankChart
 svgUtils
 textpopup
 treemapPlotly
 urlOpen
 urlUpdate

To use the modules of the **General** package they have to be imported using code like::
 
    from vois import colors
    print( colors.string2rgb('#ff00bb') )


.. _Vuetify:

Vuetify package
^^^^^^^^^^^^^^^

 The **Vuetify** package is made up of these modules:

.. autosummary::
    :nosignatures:

 app
 basemaps
 Button
 card
 cardsGrid
 ColorPicker
 datatable
 DatePicker
 DayCalendar
 dialogGeneric
 dialogMessage
 dialogWait
 dialogYesNo
 fab
 fontsettings
 footer
 iconButton
 IconClipboard
 Label
 layers
 mainPage
 menu
 MultiSwitch
 page
 paletteEditor
 palettePicker
 palettePickerEx
 popup
 Progress
 queryStrings
 Radio
 rangeSlider
 rangeSliderFloat
 selectImage
 selectMultiple
 selectSingle
 settings
 sidePanel
 slider
 sliderFloat
 snackbar
 sortableList
 svgsGrid
 switch
 Tabs
 TextList
 title
 Toggle
 tooltip
 treeview
 upload
 UploadImage
 UploadJson
 
 
To use the modules of the **Vuetify** package they have to be imported using code like::

    from vois.vuetify import app
    a = app.app()
    a.show()


.. _Geo:

Geo package
^^^^^^^^^^^^^^^

 The **Geo** package is made up of these modules:

.. autosummary::
    :nosignatures:

 Map
 mapUtils
 


Modules
-------

.. toctree::
   :maxdepth: 5

   3.1_referenceGeneral
   3.2_referenceVuetify
   3.3_referenceGeo

