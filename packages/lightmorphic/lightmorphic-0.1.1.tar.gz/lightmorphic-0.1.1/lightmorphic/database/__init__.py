#!/usr/bin/env python3

"""
=========================================
Database sub-package (`lightmorphic.database`)
=========================================
.. currentmodule:: lightmorphic.database

This module contains the databases with the required data.

"""
__all__ = ['adlsa', 'adlsa_RO', 'edlsa', 'dlsa', 'lilsa', 'oslsa', 'tlsa']

if __name__ == "__main__":
    print("The database's __init__ module is running.")
else:
    from .atmospheric_domain import *
    from .distributions import *
    from .earth_specific_domains import *
    from .light import *
    from .outer_space_domain import *
    from .trajectories import *

