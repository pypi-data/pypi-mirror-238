pyCOCAP
=======

.. image:: /pics/COCAP_small.png
   :width: 500px
   :align: center
   :alt: COCAP logo

|

**pyCOCAP** is the Python interface to the common COCAP database.


Installation
------------

Using the Package Installer for Python PIP, you can install this interface with
following command

.. code-block:: none

    pip install pycocap


Usage
-----

Once the package is installed it is as easy as this to get the COCAP data for
example the reported case numbers for Sweden and the stringency index for the
UK.

.. code-block:: python

    import pycocap as pyc
    cases = pyc.cases('Sweden')
    npi = pyc.npi('United Kingdom', 'stringency')

If you want to get multiple NPIs into one DataFrame, you can do following

.. code-block:: python

    npis = pyc.npis('Germany', ['school closing', 'dept relief', 'facial coverings'])

Defining the start and end dates of the timeseries can be done with Python's
standard `date` objects

.. code-block:: python

    from datetime import date
    deaths = pyc.death('Canada', start_date=date(2020, 5, 16), end_date=date(2021, 1, 15))

You can also use this to expand the timeseries and at the same time choose
with which value to fill gaps

.. code-block:: python

    deaths = pyc.death('Canada', start_date=date(2019, 11, 1), fill_value=0)


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Requirements
------------

* `pandas >= 1.4.0 <https://pandas.pydata.org/>`_
* `requests >= 2.27.1 <https://requests.readthedocs.io/en/latest/>`_


Contact
-------

You can get in touch with me via `e-mail <lennart.schueler@ufz.de>`_ or have a
look at the `source code <https://gitlab.hzdr.de/cocap/pycocap>`_ and open
issues there.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
