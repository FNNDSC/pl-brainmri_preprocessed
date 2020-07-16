pl-brainmri_preprocessed
================================

.. image:: https://badge.fury.io/py/brainmri_preprocessed.svg
    :target: https://badge.fury.io/py/brainmri_preprocessed

.. image:: https://travis-ci.org/FNNDSC/brainmri_preprocessed.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/brainmri_preprocessed

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-brainmri_preprocessed

.. contents:: Table of Contents


Abstract
--------

A app to demonstrate the various results of GE pipeline


Synopsis
--------

.. code::

    python brainmri_preprocessed.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        [--copySpec <copySpec>]                                     \
        <inputDir>
        <outputDir> 

Description
-----------

``brainmri_preprocessed.py`` is a ChRIS-based application that...

Arguments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.
    
    [--copySpec]
    If specified, copies only specific directories
    
    


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install brainmri_preprocessed

and run with

.. code:: bash

    brainmri_preprocessed.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    brainmri_preprocessed.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-brainmri_preprocessed brainmri_preprocessed.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-brainmri_preprocessed brainmri_preprocessed.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------

Check available pre-processed data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get a listing of the internal tree of already processed and available FreeSurfer choices:

.. code:: bash


    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-brainmri_preprocessed brainmri_preprocessed.py                    \
            -T ../preprocessed                                          \
            /incoming /outgoing


Simulate a processing delay
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To simulate a processing delay, specify some time in seconds:

.. code:: bash


    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-brainmri_preprocessed brainmri_preprocessed.py                    \
            -P 20                                                       \
            /incoming /outgoing
            
            

Copy only specific folders
~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
 To copy only 'input_data' & 'ground_truth_slices'

.. code:: bash


docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-brainmri_preprocessed brainmri_preprocessed.py                    \
        -c input,truth                                     \
        /incoming /outgoing           

