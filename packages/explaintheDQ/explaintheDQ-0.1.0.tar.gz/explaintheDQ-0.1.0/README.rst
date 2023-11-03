==============
Explain the DQ
==============


.. image:: https://img.shields.io/pypi/v/explaintheDQ.svg
        :target: https://pypi.python.org/pypi/explaintheDQ

.. image:: https://img.shields.io/travis/eas342/explaintheDQ.svg
        :target: https://travis-ci.com/eas342/explaintheDQ

.. image:: https://readthedocs.org/projects/explaintheDQ/badge/?version=latest
        :target: https://explaintheDQ.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



This is a simple package that helps explain a DQ value for the DQ extension of JWST data.


* Free software: MIT license
* Documentation: https://explaintheDQ.readthedocs.io.


The Problem
-----------

.. image:: images/example_SCI_ext.png

.. image:: images/example_DQ_ext.png
   

"SCI": Science extension of a ::code::`_rate.fits` image.
"DQ": Data Quality (DQ) extension of a ::code:`_rate.fits` image.

Example images

This image has a some strange blocks of pixels in a 9x9 grid. If you open the DQ extension of the data, the DQ values in the pixels are marked at 3 and also as 1049603. But what does that mean? The bits are explained here:
https://jwst-pipeline.readthedocs.io/en/latest/jwst/references_general/references_general.html#data-quality-flags

but what does 1049603 mean?


What this Package Does
-----------------------
This is a bear-bones package to break down the DQ number.

.. code-block:: python

   import explaintheDQ
   explaintheDQ.DQtab(1049603)

.. code-block:: console
   
         Name        Flag Bit                 Description                
    ---------------- ----- --- -------------------------------------------
          DO_NOT_USE  True   0                      Bad pixel. Do not use.
           SATURATED False   1             Pixel saturated during exposure
            JUMP_DET False   2               Jump detected during exposure
             DROPOUT False   3                   Data lost in transmission
             OUTLIER False   4                Flagged by outlier detection
         PERSISTENCE False   5                            High persistence
            AD_FLOOR False   6                             Below A/D floor
          CHARGELOSS False   7                            Charge Migration
    UNRELIABLE_ERROR False   8            Uncertainty exceeds quoted error
         NON_SCIENCE False   9    Pixel not on science portion of detector
                DEAD False  10                                  Dead pixel
                 HOT False  11                                   Hot pixel
                WARM False  12                                  Warm pixel
              LOW_QE False  13                      Low quantum efficiency
                  RC False  14                                    RC pixel
           TELEGRAPH  True  15                             Telegraph pixel
           NONLINEAR False  16                      Pixel highly nonlinear
       BAD_REF_PIXEL False  17              Reference pixel cannot be used
       NO_FLAT_FIELD False  18               Flat field cannot be measured
       NO_GAIN_VALUE False  19                     Gain cannot be measured
         NO_LIN_CORR False  20          Linearity correction not available
        NO_SAT_CHECK False  21              Saturation check not available
     UNRELIABLE_BIAS False  22                         Bias variance large
     UNRELIABLE_DARK False  23                         Dark variance large
    UNRELIABLE_SLOPE False  24    Slope variance large (i.e., noisy pixel)
     UNRELIABLE_FLAT False  25                         Flat variance large
                OPEN False  26 Open pixel (counts move to adjacent pixels)
            ADJ_OPEN False  27                      Adjacent to open pixel
    UNRELIABLE_RESET False  28                  Sensitive to reset anomaly
     MSA_FAILED_OPEN False  29   Pixel sees light from failed-open shutter
     OTHER_BAD_PIXEL False  30                            A catch-all flag
     REFERENCE_PIXEL False  31                  Pixel is a reference pixel



So the pixel that is NaN in the rate image's SCI extension has the following characteristics.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
