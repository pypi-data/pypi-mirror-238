#!/usr/bin/env python3

"""
===================================================
Created on Mon May 29 19:00:00 2023
===================================================
@author: ARXDE™
===================================================
This module contains the atmospheric domain functionality
for the lightmorphic signature analysis (adlsa)
===================================================
"""

def exosphere():
        """
        Description:
        ==========
        Located between 700 and 10,000 kilometers above Earth’s surface.
        Captures the influence of the solar wind on the extremely low density molecules present there.
        Effects of outer space particle loss is etimated.
        The orbiting satellites are not considered due to unavailable precise dynamic data.

        References:
        ==========
        """
        return 'Function not yet implemented.'

def thermosphere():
        """
        Description:
        ==========
        Located between 80 and 700 kilometers above Earth’s surface.
        It's lowest part contains the ionosphere. 
        In the estimations, it is considered water vapor-free.
        The orbiting satellites are not considered due to unavailable precise dynamic data.
           
        References:
        ==========
        """
        return 'Function not yet implemented.'

def mesosphere():
        """
        Description:
        ==========
        Located between 50 and 80 kilometers above Earth’s surface.
        No dynamic temperature corrections. The average temperature considered is about minus 85 °C.
        No dynamic meteors burning corrections due to unavailable precise dynamic data.

        References:
        ==========
        """
        return 'Function not yet implemented.'

def stratosphere():
        """
        Description:
        ==========
        Located between approximately 12 and 50 kilometers above Earth’s surface.
        Contains Earth’s ozone layer. Because of the UV radiation, the higher layers in the stratosphere are warmer.
        
        References:
        ==========
        """
        return 'Function not yet implemented.'



def troposphere():
        """
        Description:
        ==========
        Located between approximately 0 and 12 kilometers above Earth’s surface.
        It's height is lower at the poles and higher at the equator.
        Contains about 99 percent of all water vapor and aerosols.
        Compared with the other layers, it is the densest atmospheric layer.
        Estimated dynamic temperature corrections from available measured temperatures.
        No dynamic aviation corrections due to unavailable precise dynamic data.
 
        References:
        ==========
        """
        return 'Function not yet implemented.'

def prp():
        """
        Description:
        ==========
        Photonic radiation pressure.
   
        References:
        ==========
        """
        return 'Function not yet implemented.'

def aerothermoelasticity():
        """
        Description:
        ==========
        Aerothermoelasticity.
   
        References:
        ==========
        """
        return 'Function not yet implemented.'

        
def avgcm():
        """
        Description:
        ==========
        Average chemical reaction.

        References:
        ==========
        """
        return 'Function not yet implemented.'

        
if __name__ == "__main__":
    pass
else:
    print("The {} module is initialized.".format(__name__))
    from .adlsa_RO import *
