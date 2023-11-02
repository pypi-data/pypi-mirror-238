#!/usr/bin/env python3

"""
=========================================
Functions sub-package (`lightmorphic.functions`)
=========================================
.. currentmodule:: lightmorphic.functions

This module contains the mathematical and physical functions
that are used in the lightmorphic signal analysis.

"""
__all__ = ['isochronous_trajectory_patterns',
           'lightmorphic_functions', 'machine_learning',
           'mean_error', 'neural_network', 'shape_morphing']

if __name__ == "__main__":
    print("The functions's __init__ module is running.")
else:
    from . import shape_morphing
    from . import isochronous_trajectory_patterns
    from . import lightmorphic_functions
    from . import machine_learning
    from . import mean_error
    from . import neural_network

