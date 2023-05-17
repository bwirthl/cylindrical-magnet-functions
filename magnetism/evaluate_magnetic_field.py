import numpy as np

from magnetism.coordinate_transformation import (transform_coordinates_forward,
                                                 transform_vector_backward)
from magnetism.elliptic_integrals import EllipticE, EllipticK, EllipticPi


def P_1(k):
    """
    Evaluate auxiliary function P_1.

    For Reference see Eq. (4) in Caciagli et al. (2018)
    """
    k_squared = k**2
    K = EllipticK(1 - k_squared)
    E = EllipticE(1 - k_squared)
    return K - (2 / (1 - k_squared)) * (K - E)


def P_2(k, gamma):
    """
    Evaluate auxiliary function P_2.

    For Reference see Eq. (4) in Caciagli et al. (2018)
    """
    k_squared = k**2
    gamma_squared = gamma**2
    K = EllipticK(1 - k_squared)
    P = EllipticPi(1 - gamma_squared, 1 - k_squared)
    return -(gamma / (1 - gamma_squared)) * (P - K) - (1 / (1 - gamma_squared)) * (
        gamma_squared * P - K
    )


def evaluate_magnetic_field(x, y, z, magnetic_parameters):
    """
    Calculate magnetic field H of a cylindrical magnet.

    The magnetic field is calculated according to the following reference:
    Caciagli, A., Baars, R. J., Philipse, A. P., & Kuipers, B. W. M. (2018). Exact expression for the magnetic field of a finite cylinder with arbitrary uniform magnetization. Journal of Magnetism and Magnetic Materials, 456, 423-432. https://doi.org/10.1016/j.jmmm.2018.02.003
    """

    # transform coordinates to cylindrical coordinates
    rho, phi, z = transform_coordinates_forward(x, y, z, magnetic_parameters)

    R = magnetic_parameters["radius_magnet"]
    half_length = 0.5 * magnetic_parameters["length"]

    # calculate auxiliary variables
    rho_p = R + rho
    if np.abs(rho_p) < 1e-2:
        rho_p = 1e-2
    rho_m = R - rho
    zeta_p = half_length + z
    zeta_m = half_length - z
    alpha_p = 1 / (np.sqrt(zeta_p**2 + rho_p**2))
    alpha_m = 1 / (np.sqrt(zeta_m**2 + rho_p**2))
    beta_p = zeta_p * alpha_p
    beta_m = -zeta_m * alpha_m
    gamma = (rho - R) / (rho + R)
    k_p = np.sqrt((zeta_p**2 + rho_m**2) / (zeta_p**2 + rho_p**2))
    k_m = np.sqrt((zeta_m**2 + rho_m**2) / (zeta_m**2 + rho_p**2))

    # calculate magnetic field components
    # see Eq. (3) in Caciagli et al. (2018)
    H_rho = (
        R
        * (magnetic_parameters["magnetization"] / np.pi)
        * (alpha_p * P_1(k_p) - alpha_m * P_1(k_m))
    )
    H_z = (
        R
        * (magnetic_parameters["magnetization"] / (np.pi * rho_p))
        * (beta_p * P_2(k_p, gamma) - beta_m * P_2(k_m, gamma))
    )

    # transform magnetic field components back to cartesian coordinates
    H_x, H_y, H_z = transform_vector_backward(H_rho, H_z, phi, magnetic_parameters)

    if rho < R and np.abs(z) < half_length:
        H_z = H_z - magnetic_parameters["magnetization"]

    return H_x, H_y, H_z
