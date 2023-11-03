=============================
django-jsnlog
=============================

.. image:: https://badge.fury.io/py/django-jsnlog.svg
    :target: https://badge.fury.io/py/django-jsnlog

A django integration for client side logging for javascript with JSNLog https://jsnlog.com/.

Documentation
-------------

The full documentation is at https://django-jsnlog.readthedocs.io.

Quickstart
----------

Install django-jsnlog::

    pip install django-jsnlog

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'jsnlog',
        ...
    )

Add django-jsnlog's URL patterns:

.. code-block:: python

    urlpatterns += [
        path(r'jsnlog.logger', include('jsnlog.urls')),
    ]

Add django-jsnlog's javascript files to your template:

.. code-block:: html

    ...
    <script type="text/javascript" src="{% static 'jsnlog/js/jsnlog.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'jsnlog/js/django-jsnlog.js' %}"></script>
    ...

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
