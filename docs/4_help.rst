.. image:: figures/vois_horizontal_small.png

|

.. _Help:

*********************************
Sources of documentation and help
*********************************

This documentation is written using the `sphinx <http://www.sphinx-doc.org>`_ tool.

====================
Online documentation
====================

This documentation is available in the source code under the docs directory (details on how to compile can be found in the README.md file). There is an online version in html format available on this `website <https://jeodpp.jrc.ec.europa.eu/services/shared/vois/index.html>`_.

The documentation is divided in three main parts:

* :ref:`Introduction`: Introduction explaining the organization of the vois library package and its modules.

* :ref:`Tutorial`: A tutorial to guide you through the first steps of using vois library by using a step by step example dashboard.

* :ref:`Reference`: A manual describing all functions and methods available in vois library


=================
Notebook examples
=================

Each of the modules of the vois library is accompanied by a Jupyter Notebook having the same name in the examples/notebooks folder.
In the notebook the functions of the module can be tested with simple lines of code that illustrate, through examples, how the classes and functions can be used.

.. note::

    In the notebooks the python module to be tested can be imported in two different ways.
    
    1. %run <modulename>.py

          This method "executes" the content of the python module in the notebook context. Classes and methods of the module can be called without prepending the modulename. This method is used to avoid the restart of the python kernel when the content of the python module is changed. By re-executing the notebook cell that contains the %run directive, the updated content is already available, without the need to shutdown and restart the notebook. It is suggested that this method is used only during the development of the vois library itself, and not in thedevelopment of users' dashboards.
          
          Example::
    
            %run button.py
            b = button('Test button')
            display(b.draw())
    
    2. import <modulename>

          This method imports the content of the python module: classes and methods of the module must be called by prepending the modulename.
          
          Example::
          
            import button
            b = button.button('Test button')
            display(b.draw())

====================
Inline documentation
====================

In addition to the online help pages, there is the inline documentation. 

To get help on a class, e.g. :py:class:`button.button`::

    from vois.vuetify import button
    help(button.button)

To get help on a class method, e.g., :py:meth:`app.app.snackbar`::

    from vois.vuetify import app
    help(app.app.snackbar)

To get help on a function, e.g., :py:func:`geojsonUtils.geojsonJson`::

    from vois import geojsonUtils
    help(geojsonUtils.geojsonJson)
