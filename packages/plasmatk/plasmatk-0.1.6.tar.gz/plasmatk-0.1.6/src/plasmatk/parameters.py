import numpy as np
import pandas as pd
import scipy.constants as c

e = c.e
m_e = c.m_e
epsilon_0 = c.epsilon_0

def Gamma_e(T, n_e):
    """Return the coupling constant.

    Args:
        T (float): The temperature in eV.
        n_e (float): The electron number density in cm^-3.
    Returns:
        The electron coupling parameter.
    """
    # Convert to meters
    n = n_e * 100**3
    a_e = (3/(4*np.pi*n))**(1/3)
    return c.e**2/(
        a_e*4*np.pi*c.epsilon_0*c.e*T)

def Beta_e(B, n_e):
    r"""Return the magnetization parameter
    :math:`B \equiv \frac{\omega_{ce}}{\omega_{pe}}`.

    Args:
        B (float): The magnetic field in Tesla.
        n_e (float): The electron number density in cm^-3.
    """
    n = n_e * 100**3
    return B*np.sqrt(c.epsilon_0 / (c.m_e * n))

def v_the(n, T, B):
    r"""Return the thermal speed. Defined as
    :math:`v_\mathrm{th} = \sqrt{\frac{k_\mathrm{B}T}{m_\mathrm{e}}}`.

    Args:
        1
    """
    # Convert from keV to Joules
    E = T * 1000 * e
    return np.sqrt(E/m_e)

def l_De(n, T, B):
    # Convert from keV to Joules
    E = T * 1000 * e
    return np.sqrt(epsilon_0 * E / (n*e**2))

def N_De(n, T, B):
    return n*l_De(n, T, B)**3

def wpe(n, T, B):
    return np.sqrt(c.e**2 * n / (epsilon_0 * m_e) )

def wce(n, T, B):
    """The electron cyclofrequency."""
    return e*B/m_e
