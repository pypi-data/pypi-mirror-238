#!/usr/bin/env python3
"""
==========================================================================================
Updated: 11-IX-2023
==========================================================================================
@author: ARXDE™
==========================================================================================
This module contains the basic mathematical and physical constants used by the lightmorphic applications.
They are not intended to be comprehensive.
==========================================================================================
"""
class supsub():
    def __init__(self):
        pass
    
    @staticmethod
    def sup(self):
        superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return str(self).translate(superscript)
    
    @staticmethod
    def sub(self):
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(self).translate(subscript)
    
"""
==========================================================================================
"""
class bipm():
    def __init__(self):
        pass

    @staticmethod
    def caesium_hyperfine_frequency():
        """
        Description:
        ==========
        The unperturbed ground state hyperfine transition frequency
        of the caesium-133 atom, with units hertz, Hz = s⁻¹

        Returns: (9192631770,'Hz')
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (9192631770,'Hz')

    @staticmethod
    def c():
        """
        Description:
        ==========
        Speed of light in vacuum, with units meters per second, in vacuum

        Returns: 299792458,'m/s'
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (299792458,'m/s')

    @staticmethod    
    def h():
        """
        Description:
        ==========
        Planck constant, with units joule*second, J =  kg m² s⁻²

        Returns: 6.62607015*10**(-34),'J*s'
        
        """
        return (6.62607015*10**(-34),'J*s')

    @staticmethod
    def e():
        """
        Description:
        ==========
        Elementary charge, with units C = coulomb, C = A*s

        Returns: 1.602176634*10**(-19),'C'
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (1.602176634*10**(-19),'C')

    @staticmethod    
    def k():
        """
        Description:
        ==========
        Boltzmann constant, with units Joule/kelvin

        Returns: 1.380649*10**(-23),'J/K'
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (1.380649*10**(-23),'J/K')

    @staticmethod    
    def N_A():
        """
        Description:
        ==========
        Avogadro constant, with units1/mole

        Returns: 6.02214076*10**23,'mol⁻¹'
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (6.02214076*10**23,'mol⁻¹')

    @staticmethod    
    def K_cd():
        """
        Description:
        ==========
        Luminous efficacy of monochromatic radiation of frequency 540 x 10**12 Hz,
        with units lumen per Watt

        Returns: 683,'lm/W'
        
        References:
        ==========
        [1] https://www.bipm.org/en/measurement-units/si-defining-constants
        """
        return (683,'lm/W')
    
"""
==========================================================================================
"""
class bipm_drv():
    def __init__(self):
        """Units derived from BIPM values."""
        pass
    
    @staticmethod       
    def T():
        """
        Description: 
        ==========
        The unit for time, derived from: 9192631770/caesium_hyperfine_frequency

        Returns: 's'
        
        References:
        ==========
        [2] https://www.bipm.org/en/si-base-units/second
        """
        return 's'

    @staticmethod       
    def L():
        """
        Description: 
        ==========
        The unit for length, derived from (c/299792458)*s
        
        Returns: 'm'
        
        References: 
        ==========
        [3] https://www.bipm.org/en/si-base-units/metre
        """
        return 'm'

    @staticmethod       
    def M():
        """
        Description: 
        ==========
        The unit for mass, derived from (h/6.62607015*10**(-34))*m**(-2)*s

        Returns: 'kg'
        
        References:
        ==========
        [4] https://www.bipm.org/en/si-base-units/kilogram
        """
        return 'kg'

    @staticmethod       
    def EC():
        """
        Description: 
        ==========
        The unit for electric current, derived from 1/1.602176634*10(-19) elementary charges per second

        Returns: 'A'
        
        References:
        ==========
        [5] https://www.bipm.org/en/si-base-units/ampere
        """
        return 'A'

    @staticmethod       
    def TEMP():
        """
        Description: 
        ==========
        The unit for temperature, derived from the temperature change
        for a thermal energy kT equal to 1.380649*10(-23) J,
        with Celsius zero value T_0 = 273,15 K = 0 °C

        Returns: 'K'
        
        References:
        ==========
        [6] https://www.bipm.org/en/si-base-units/kelvin
        """
        return 'K'

    @staticmethod       
    def MOL():
        """
        Description: 
        ==========
        The unit for the amount of substance, derived from 6.02214076*10**23/Avogadro constant

        Returns: 'mol'
        
        References:
        ==========
        [7] https://www.bipm.org/en/si-base-units/mole
        """
        return 'mol'

    @staticmethod           
    def CD():
        """
        Description: 
        ==========
        The unit for the luminous intensity, derived from (K_cd/683)*kg*(m**2)*(s**(-3))*(sr**(-1))

        Returns: 'cd'
        
        References:
        ==========
        [8] https://www.bipm.org/en/si-base-units/candela
        """
        return 'cd'
        
    """
==========================================================================================
"""
class oth(supsub):
    def __init__(self):
        """Other units."""
        pass

    @staticmethod    
    def radian():
        """
        Description:  
        ==========
        The 2D angle or the plan angle
        
        base units: rad = m/m
        derived units: ---
        symbol: rad
        """
        return ('m/m', '---', 'rad')

    @staticmethod    
    def steradian():
        """
        Description: 
        ==========
        The 3D angle or the solid angle

        base units: sr = m²/m²
        derived units: ---
        symbol: sr
        """
        return ('m'+supsub.sup(2)+'/'+'m'+supsub.sup(2), '---', 'sr')

    @staticmethod    
    def hertz():
        """
        Description: 
        ==========
        The frequency
        
        base units: Hz = s⁻¹
        derived units: ---
        symbol: Hz
        """
        return ('s'+'\u207b'+supsub.sup(1), '---', 'Hz')

    @staticmethod    
    def newton():
        """
        Description: 
        ==========
        The force
        
        base units: N = kg m s⁻²
        derived units: ---
        symbol: N
        """
        return ('kg m s'+'\u207b'+supsub.sup(2), '---', 'N')

    @staticmethod    
    def pascal():
        """
        Description: 
        ==========
        The pressure
        
        base units: Pa = kg m⁻¹ s⁻²
        derived units: N/m²
        symbol: Pa
        """
        return ('kg m'+'\u207b'+supsub.sup(1) + ' s'+'\u207b'+supsub.sup(2), 'N/'+'m'+supsub.sup(2), 'Pa')

    @staticmethod    
    def joule():
        """
        Description: 
        ==========
        The energy, work done or heat quantity
        
        base units: J = kg m² s⁻²
        derived units: N m
        symbol: J
        """
        return ('kg m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(2), 'N m ', 'J')

    @staticmethod    
    def watt():
        """
        Description: 
        ==========
        The power, energy flux
        
        base units: W = kg m² s⁻³
        derived units: J/s
        symbol: W
        """
        return ('kg m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(3), 'J/s ', 'W')

    @staticmethod    
    def coulomb():
        """
        Description: 
        ==========
        The electrical charge
        
        base units: C = A s
        derived units: ---
        symbol: C
        """
        return ('A s', '--- ', 'C')

    @staticmethod    
    def volt():
        """
        Description: 
        ==========
        The electrical potential
        
        base units: V = kg m² s⁻³A⁻¹
        derived units: W/A
        symbol: V
        """
        return ('kg m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(3) + 'A'+'\u207b'+supsub.sup(1), 'W/A ', 'V')

    @staticmethod    
    def farad():
        """
        Description: 
        ==========
        The electrical capacitance
        
        base units: F = kg⁻¹ m⁻² s⁴ A²
        derived units: C/V
        symbol: F
        """
        return ('kg'+'\u207b'+supsub.sup(1) + ' m'+'\u207b'+supsub.sup(2) + ' s' + supsub.sup(4) + ' A'+supsub.sup(2), 'C/V', 'F')

    @staticmethod    
    def ohm():
        """
        Description: 
        ==========
        The electrical resistance
        
        base units: \u03A9 = kg m² s⁻³ A⁻²
        derived units: V/A
        symbol: \u03A9
        """
        return ('kg' + ' m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(3) + ' A'+'\u207b'+supsub.sup(2), 'V/A', '\u03A9')

    @staticmethod    
    def siemens():
        """
        Description: 
        ==========
        The electric conductance
        
        base units: S = kg⁻¹ m⁻² s³ A²
        derived units: A/V
        symbol: S
        """
        return ('kg'+'\u207b'+supsub.sup(1) + ' m'+'\u207b'+supsub.sup(2) + ' s'+supsub.sup(3) + ' A'+supsub.sup(2), 'A/V', 'S')

    @staticmethod    
    def weber():
        """
        Description: 
        ==========
        The magnetic flux
        
        base units: Wb = kg m² s⁻² A⁻¹
        derived units: V s
        symbol: Wb
        """
        return ('kg' + ' m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(2) + ' A'+'\u207b'+supsub.sup(1), 'V s', 'Wb')

    @staticmethod    
    def tesla():
        """
        Description: 
        ==========
        The magnetic flux density
        
        base units: T = kg s⁻² A⁻¹
        derived units: Wb/m²
        symbol: T
        """
        return ('kg' + ' s'+'\u207b'+supsub.sup(2) + ' A'+'\u207b'+supsub.sup(1), 'Wb/'+'m'+supsub.sup(2), 'T')

    @staticmethod    
    def henry():
        """
        Description: 
        ==========
        The electrical inductance
        
        base units: H = kg m² s⁻² A⁻²
        derived units: Wb/A
        symbol: H
        """
        return ('kg' + ' m'+supsub.sup(2) + ' s'+'\u207b'+supsub.sup(2) + ' A'+'\u207b'+supsub.sup(2), 'Wb/A', 'H')

    @staticmethod    
    def lumen():
        """
        Description: 
        ==========
        The luminous flux
        
        base units: lm = cd sr
        derived units:  ---
        symbol: lm
        """
        return ('cd sr', '---', 'lm')

    @staticmethod    
    def lux():
        """
        Description: 
        ==========
        The luminous flux per unit area or the illuminance
        
        base units: lx = cd sr m⁻²
        derived units:  ---
        symbol: lx
        """
        return ('cd' + ' sr' + ' m'+'\u207b'+supsub.sup(2), 'lm/' +' m'+ supsub.sup(2), 'lx')

    @staticmethod    
    def becquerel():
        """
        Description: 
        ==========
        The radioactivity
        
        base units: Bq = s⁻¹
        derived units:  ---
        symbol: Bq
        """
        return ('s'+'\u207b'+supsub.sup(1), '---', 'Bq')

    @staticmethod    
    def gray():
        """
        Description: 
        ==========
        The ionizing radiation dose
        
        base units: Gy = m² s⁻²
        derived units:  J/kg
        symbol: Gy
        """
        return ('m'+supsub.sup(2)+' s'+'\u207b'+supsub.sup(2), 'J/kg', 'Gy')

    @staticmethod    
    def sievert():
        """
        Description: 
        ==========
        The stochastic health risk of ionizing radiation dose
        
        base units: Sv = 
        derived units:  J/kg
        symbol: Sv
        """
        return ('m'+supsub.sup(2)+' s'+'\u207b'+supsub.sup(2), 'J/kg', 'Sv')

    @staticmethod    
    def katal():
        """
        Description: 
        ==========
        The unit of catalytic activity
        
        base units: kat = mol s⁻¹
        derived units:  ---
        symbol: kat
        """
        return ('mol'+' s'+'\u207b'+supsub.sup(1), '---', 'kat')

    def au():
        """
        Description: 
        ==========
        The astronomical unit.

        """
        return (149597870700,'m')

    def ev():
        """
        Description: 
        ==========
        The electronvolt unit.

        """
        return (1.602176634*10**(-19),'J')


"""
==========================================================================================
"""
class math():
    def __init__(self):
        """Mathematical values."""
        pass

    @staticmethod    
    def Pi():
        return '3.1415926535897932384626433832795028' 

    @staticmethod    
    def Euler():
        return '2.71828182845904523536028747135266249'

    @staticmethod    
    def Gamma():
        return '0.577215664901532860606512090082402431042'

"""
==========================================================================================
"""
quetta = 10**30
ronna = 10**27
yotta = 10**24
zetta = 10**21
exa = 10**18
peta = 10**15
tera = 10**12
giga = 10**9
mega = 10**6
kilo = 10**3
hecto = 10**2
deca = 10**1
deci = 10**(-1)
centi = 10**(-2)
milli = 10**(-3)
micro = 10**(-6)
nano = 10**(-9)
pico = 10**(-12)
femto = 10**(-15)
atto = 10**(-18)
zepto = 10**(-21)
yocto = 10**(-24)
ronto = 10**(-27)
quecto = 10**(-30)

"""
==========================================================================================
"""

if __name__ == "__main__":
    pass
else:
    print("The {} module is initialized.".format(__name__))
