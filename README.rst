=========================================
Digilent's DWF Library wrapper for python
=========================================

What is this?
=============

This is a python library for controlling Analog Discovery and
Electronics Explorer series presetned by `Digilent inc.`_
This library needs Waveforms SDK.

I tested this library with Analog Discovery 2 and
`Waveforms 2015`_ in below environment.

* python 3.5.1, python 2.7.10 on OSX 10.11
* python 3.4.3, python 2.7.6 on Ubuntu 14.04LTS
* python 3.5.1 on Windows 7

I wrote this library for supporting python 2.6, 2.7, 3.3 or above.

This software is released under the MIT License, see LICENSE.txt.

.. _Digilent inc.: https://digilentinc.com/
.. _Waveforms 2015: https://reference.digilentinc.com/waveforms3


API of this library
===================

This library has two sets of API. There are Function-based API and
Class-based API.

Function-based API
~~~~~~~~~~~~~~~~~~

This API is like as C functions which supplied by Digilent. But
some modifications are applied for pythonic-way programming.

1. When error is returned by SDK, the exception ``DWFError`` is
   raised.
2. All output values, which are passed by reference, are changed
   to return-value of function.
3. Arrays of parameters are converted from/to python's list.

Examples
^^^^^^^^

SDK version check in C language is like as:

.. code:: c

  char version[32];
  FDwfGetVersion(version);
  printf("DWF version: %s\n", version);

With this library using function-based API, same code is
translated to:
  
.. code:: python

  version = dwf.FDwfGetVersion()
  print("DWF version: " + version)

.. _example code:

Another example is here. This piece of code is quoted from
``analogout_custom.c`` in Waveforms SDK sample.

.. code:: c

  HDWF hdwf;
  double rgdSamples[4096];
  for (int i = 0; i < 4096; i++) rgdSamples[i] = 2.0*i/4095-1;
  
  FDwfDeviceOpen(-1, &hdwf);
  FDwfAnalogOutNodeSet(hdwf, 0, AnalogOutNodeCarrier, true);
  FDwfAnalogOutNodeFunctionSet(hdwf, 0, AnalogOutNodeCarrier, funcCustom);
  FDwfAnalogOutNodeDataSet(hdwf, 0, AnalogOutNodeCarrier, rgdSamples, 4096);
  ...

In python with this library, like as:
  
.. code:: python
  
  rgdSamples = []
  for i in range(4096): rgdSamples.append(2.0*i/4095-1)
  
  hdwf = dwf.FDwfDeviceOpen()
  dwf.FDwfAnalogOutNodeSet(hdwf, 0, dwf.AnalogOutNodeCarrier, True)
  dwf.FDwfAnalogOutNodeFunctionSet(hdwf, 0, dwf.AnalogOutNodeCarrier, dwf.funcCustom)
  dwf.FDwfAnalogOutNodeDataSet(hdwf, 0, dwf.AnalogOutNodeCarrier, rgdSamples)
  ...


Class-based API
~~~~~~~~~~~~~~~

Class-based APIs are made from function-based APIs. Documents of
this API is now writing.

This API has below function and classes.

``DwfEnumeration()``
   Device enumeration. This function returns list of ``DwfDevice``.
``class DwfDevice``
   call ``FDwfEnum*()`` functions.
``class Dwf``
   call ``FDwfDevice*()`` functions.
``class DwfAnalogIn``
   call ``FDwfAnalogIn*()`` functions.
``class DwfAnalogOut``
   call ``FDwfAnalogOut*()`` functions.
``class DwfAnalogIO``
   call ``FDwfAnalogIO*()`` functions.
``class DwfDigitalIO``
   call ``FDwfDigitalIO*()`` functions.
``class DwfDigitalIn``
   call ``FDwfDigitalIn*()`` functions.
``class DwfDigitalOut``
   call ``FDwfDigitalOut*()`` functions.

With this API, `example code`_ is translated to

.. code:: python
  
  rgdSamples = []
  for i in range(4096): rgdSamples.append(2.0*i/4095-1)
  
  dwf_ao = dwf.DwfAnalogOut()
  dwf_ao.nodeSet(0, dwf_ao.NODE_CARRIER, True)
  dwf_ao.nodeFunctionSet(0, dwf_ao.NODE_CARRIER, dwf_ao.FUNC_CUSTOM)
  dwf_ao.nodeDataSet(0, dwf_ao.NODE_CARRIER, rgdSamples)
  ...
