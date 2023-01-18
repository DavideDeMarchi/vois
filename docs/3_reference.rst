.. image:: figures/vois_horizontal_small.png

|

.. _Reference:

Reference manual
================

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
 svgBubblesChart
 svgGraph
 svgHeatmap
 svgMap
 svgPackedCirclesChart
 svgRankChart
 svgUtils
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
 button
 card
 cardsGrid
 colorPicker
 datatable
 datePicker
 dialogGeneric
 dialogMessage
 dialogWait
 dialogYesNo
 fab
 fontsettings
 footer
 label
 layers
 menu
 multiSwitch
 paletteEditor
 palettePicker
 progress
 queryStrings
 radio
 rangeSlider
 selectImage
 selectMultiple
 selectSingle
 settings
 sidePanel
 slider
 snackbar
 sortableList
 svgsGrid
 switch
 tabs
 title
 toggle
 tooltip
 treeview
 upload
 
 
To use the modules of the **Vuetify** package they have to be imported using code like::

    from vois.vuetify import app
    a = app.app()
    a.show()


Modules
-------

.. toctree::
   :maxdepth: 5

   3.1_referenceGeneral
   3.2_referenceVuetify

