import numpy as np
from numpy import arctan, sqrt, pi, exp, log
from scipy.special import dawsn
from RSFlib.Constants import PhysConst

def get_MSE(e_psi, e_delta, f_psi, f_delta, M=3):
    '''
    Calculates mean-square-error
    :param e_psi: experimental psi
    :param e_delta: esperimental delta
    :param f_psi: model generated psi
    :param f_delta: model generated delta
    :param M: number of fiting parameterrs
    :return: MSE as reliability of fit
    '''

    N = len(e_psi)
    mse = 0
    sigma_psi = np.std(e_psi)
    sigma_delta = np.std(e_delta)
    for n in range(N):
        mse += ( ( (f_psi[n]-e_psi[n])/sigma_psi )**2 + ( (f_delta[n]-e_delta[n])/sigma_delta )**2 )
    return sqrt(1/(2*N-M) * mse)

def cauchy(wvl, A=0, B=0, C=0):
    '''
    Cauchy function for fitting real part of dielectric function
    :param wvl: wavelength in nm
    :param A: amplitude
    :param B:
    :param C:
    :return: real part of dielectric function
    '''

    wvl = wvl / 1000
    return A + B / wvl ** 2 + C / wvl ** 4

def tauc_lorentz(E, An, En, Cn, Eg, eps1_inf=0):
    '''
    tauc-lorentz function for fiting complex dielectric function
    :param E: energy in Ev
    :param An: amplitude in Ev
    :param En:
    :param Cn:
    :param Eg: band gab energy in Ev
    :param eps1_inf: offset in Ev
    :return:
    '''

    eps2 = (An*En*Cn*(E-Eg)**2) / ((E**2 - En**2)**2+Cn**2*E**2) * 1/E
    eps2 = np.array( [0 if E <= Eg else eps for eps, E in zip(eps2, E)] )

    # E_0 = En
    alp = sqrt(4*En**2 - Cn**2)
    gam = sqrt(En**2 - Cn**2/2)

    a_ln = (Eg**2-En**2)*E**2 + Eg**2*Cn**2 - En**2*(En**2 + 3*Eg**2)
    a_atan = (E**2 - En**2)*(En**2 + Eg**2) + Eg**2*Cn**2
    zeta4 = (E**2 - gam**2)**2 + alp**2*Cn**2/4

    eps1 = (
        eps1_inf + An*Cn/pi/zeta4 * a_ln/2/alp/En * log( (En**2 + Eg**2 + alp*Eg) / (En**2 + Eg**2 - alp*Eg) )
        - An/pi/zeta4 * a_atan/En * ( pi - arctan( (2*Eg + alp)/Cn ) + arctan( (-2*Eg + alp)/Cn ) )
        + 2*An*En/pi/zeta4/alp * Eg * (E**2 - gam**2) * ( pi + 2*arctan( 2 * (gam**2-Eg**2)/alp/Cn ) )
        - An*En*Cn/pi/zeta4 * (E**2 + Eg**2)/E * log( abs(E-Eg) / (E+Eg) )
        + 2*An*En*Cn/pi/zeta4 * Eg * log( (abs(E-Eg)*(E+Eg)) / sqrt( (En**2 - Eg**2)**2 + Eg**2*Cn**2 ) )
    )

    return (eps1, eps2)

def gauss(E, An, Br, En, eps_inf=0):
    '''
    gauss function for complex dielectric function
    :param E: energy in Ev
    :param An: Amplitude in Ev
    :param Br: half of Width till konvergention to 0 in Ev
    :param En:
    :param eps_inf:
    :return:
    '''


    sigma = Br/2/sqrt(log(2))
    eps2 = An * exp(-( (E-En)/sigma )**2) - An * exp(-( (E+En)/sigma )**2)

    eps1 = eps_inf + 2*An/sqrt(pi) * ( dawsn(2 * sqrt(log(2)) * (E + En)/Br) - dawsn(2 * sqrt(log(2)) * (E - En)/Br) )

    return (eps1, eps2)

def calculate_perm(n, k):
    ''' function that makes permitivity from refractive index and absor '''

    epsilon1 = n**2 - k**2
    epsilon2 = 2 * n * k
    return epsilon1, epsilon2

def calculate_nk(epsilon1, epsilon2):
    ''' function that makes nk from permitivity '''

    n = np.sqrt((epsilon1 + np.sqrt(epsilon1**2 + epsilon2**2)) / 2)
    k = np.sqrt((np.sqrt(epsilon1**2 + epsilon2**2) - epsilon1) / 2)
    return n, k

def Ev2m(data):
    ''' calculates Ev to m '''
    pc = PhysConst()
    h, e, c = pc.planck, pc.elem_charge, pc.light_speed
    return h*c/data/e

def elips_eps(psi, delta, theta):
    ''' calculates complex dielectric function from psi, delta and theta, must be in radians '''
    rho = np.tan(psi) * np.exp(1j * delta)
    eps = np.sin(theta) ** 2 * (1 + ((1 - rho) / (1 + rho)) ** 2 * np.tan(theta) ** 2)
    return eps.real, eps.imag

