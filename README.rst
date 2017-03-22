mit_moira
=========

A Python library for accessing MIT's Moira_ system.
This library uses the SOAP API, which has a few unusual limitations, and
requires X.509 client certificates for access.

.. _Moira: http://kb.mit.edu/confluence/display/istcontrib/Moira+Overview

Usage
-----

.. code-block:: python

    from mit_moira import Moira

    # Initialize Moira client with X.509 certificate and private key file
    moira = Moira("path/to/x509.cert", "path/to/x509.pem")
