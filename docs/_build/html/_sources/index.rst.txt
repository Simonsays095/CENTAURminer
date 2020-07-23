.. CENTAUR miner documentation master file, created by
   sphinx-quickstart on Wed Jul  1 10:55:48 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. include:: ../README.rst

Installation
------------

Pre-requisites
~~~~~~~~~~~~~~
   - Python version >= 3.4
   - Google chrome

Install
~~~~~~~

Install directly via pip:

.. code-block:: console

   pip install centaurminer

Dependencies
~~~~~~~~~~~~

- Selenium >= 3.141.0
- webdriver-manager >= 3.2.1

.. toctree::
   :maxdepth: 1
   :caption: Introduction

   intro_to_data_mining

.. toctree::
   :maxdepth: 1
   :caption: Documentation

   module_documentation/DOM_elements
   module_documentation/PageLocations
   module_documentation/MiningEngine
   module_documentation/Helper_functions

.. toctree::
   :maxdepth: 1
   :caption: Examples

   examples/Minimal
   examples/Fully_worked

More Information
----------------

You can get more information from the source code and the PyPi page:
   - `Source code`_
   - `PyPi page`_

.. _Source code: https://github.com/Simonsays095/CENTAURminer
.. _PyPi page: https://pypi.org/project/centaurminer/