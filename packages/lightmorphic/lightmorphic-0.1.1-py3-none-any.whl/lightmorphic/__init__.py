#!/usr/bin/env python3

"""
lightmorphic: A scientific lightmorphic computing package for Python
======================================================================
Contents
--------------
The lightmorphic signal analysis toolkit has the following components:

Subpackages
-------------------
Before using any of these subpackages you must import them.
For example, ``from lightmorphic.ct import *``.
::
 constants: Physical and mathematical constants and units
 database: Database with the required data
 functions: Specific functions
 spectrograms: Results as spectrograms

 Public API in the main Lightmorphic namespace
---------------------------------------------------------------------
::
 __version__: Show lightmorphic version string
 show_config: Show lightmorphic build configuration
 test: Run lightmorphic unittests
"""
import sys
if sys.version_info < (3, 10):
    raise ImportError("Python version 3.10 or above is required to run the lightmorphic SW package.")
del sys

__all__ = [
        'database',
        'constants',
        'functions',
        'spectrograms',
        'main'
        ]

if __name__ == "__main__":
    print("The lightmorphic's __init__ module is running")
else:
    print('~'*100)
    from .database import *
    from .constants import ct
    from .functions import (isochronous_trajectory_patterns, lightmorphic_functions, machine_learning, mean_error, neural_network, shape_morphing)
    from .spectrograms import spectrograms_plot
    print('~'*100)
    from .main import *


