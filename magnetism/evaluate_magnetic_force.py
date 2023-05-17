import numpy as np

from magnetism.coordinate_transformation import (transform_coordinates_forward,
                                                 transform_vector_backward)
from magnetism.elliptic_integrals import EllipticE, EllipticK, EllipticPi


def evaluate_magnetic_force(x, y, z, magnetic_parameters):
    """
    Evaluate the magnetic force at a given point in space.
    """
    # transform the coordinates
    rho, phi, z = transform_coordinates_forward(x, y, z, magnetic_parameters)

    # extract the magnetic parameters
    R = magnetic_parameters["radius_magnet"]
    half_length = 0.5 * magnetic_parameters["length"]

    mobility = np.power(
        6
        * np.pi
        * magnetic_parameters["dynamic_viscosity_fluid"]
        * magnetic_parameters["radius_particle"],
        -1.0,
    )
    volume_particle = (
        (4 / 3) * np.pi * np.power(magnetic_parameters["radius_particle"], 3)
    )

    # calculate the auxiliary variables
    rho_p = R + rho
    rho_m = R - rho
    zeta_p = half_length + z
    zeta_m = half_length - z

    a_1 = rho_p**2 + zeta_p**2
    a_2 = rho_p**2 + zeta_m**2
    a_3 = rho_m**2 + zeta_p**2
    a_4 = rho_m**2 + zeta_m**2

    b_1 = zeta_p**2 + R**2
    b_2 = zeta_m**2 + R**2
    b_3 = zeta_p**2 - R**2
    b_4 = zeta_m**2 - R**2

    c_1 = b_1 + rho**2
    c_2 = b_2 + rho**2
    c_3 = b_3 + rho**2
    c_4 = b_4 + rho**2

    alpha_p = 1 / np.sqrt(a_1)
    alpha_m = 1 / np.sqrt(a_2)

    psi_p = (4 * rho * R) / a_1
    psi_m = (4 * rho * R) / a_2

    beta = (4 * rho * R) / (rho_p**2)

    # calculate the auxiliary functions
    Q_1 = (
        a_2 * EllipticE(psi_m) / alpha_p
        - a_1 * EllipticE(psi_p) / alpha_m
        + c_1 * EllipticK(psi_p) / alpha_m
        - c_2 * EllipticK(psi_m) / alpha_p
    )

    Q_2 = (
        rho_p * zeta_p * EllipticK(psi_p) / alpha_m
        + rho_p * zeta_m * EllipticK(psi_m) / alpha_p
        + rho_m * zeta_p * EllipticPi(beta, psi_p) / alpha_m
        + rho_m * zeta_m * EllipticPi(beta, psi_m) / alpha_p
    )

    # calculate the magnetic force in cylindrical coordinates
    F_rho = (
        mobility
        * magnetic_parameters["magnetization"] ** 2
        * magnetic_parameters["magnetic_permeability"]
        * volume_particle
        * R
        * (
            rho**2
            * Q_2
            * (
                a_3 * c_2 * zeta_m * EllipticE(psi_m) / alpha_p
                + a_4 * c_1 * zeta_p * EllipticE(psi_p) / alpha_m
                - a_3 * a_4 * zeta_m * EllipticK(psi_m) / alpha_p
                - a_3 * a_4 * zeta_p * EllipticK(psi_p) / alpha_m
            )
            + rho_p
            * Q_1
            * (
                (b_1**2 + rho**2 * b_3) * a_4 * EllipticE(psi_p) / alpha_m
                - (b_2**2 + rho**2 * b_4) * a_3 * EllipticE(psi_m) / alpha_p
                + a_3 * a_4 * b_2 * EllipticK(psi_m) / alpha_p
                - a_3 * a_4 * b_1 * EllipticK(psi_p) / alpha_m
            )
        )
    ) / (4.0 * np.pi**2 * rho**3 * rho_p * a_4 * a_2 * a_3 * a_1)

    F_z = (
        mobility
        * magnetic_parameters["magnetization"] ** 2
        * magnetic_parameters["magnetic_permeability"]
        * volume_particle
        * (
            (Q_1 / rho**2)
            * (
                a_3 * a_4 * zeta_m * EllipticK(psi_m) / alpha_p
                + a_3 * a_4 * zeta_p * EllipticK(psi_p) / alpha_m
                - c_2 * zeta_m * a_3 * EllipticE(psi_m) / alpha_p
                - c_1 * zeta_p * a_4 * EllipticE(psi_p) / alpha_m
            )
            + (Q_2 / rho_p)
            * (
                c_4 * a_3 * EllipticE(psi_m) / alpha_p
                - c_3 * a_4 * EllipticE(psi_p) / alpha_m
                - a_3 * a_4 * EllipticK(psi_m) / alpha_p
                + a_3 * a_4 * EllipticK(psi_p) / alpha_m
            )
        )
    ) / (4.0 * np.pi**2 * a_4 * a_2 * a_3 * a_1)

    # transform the magnetic force back to cartesian coordinates
    F_x, F_y, F_z = transform_vector_backward(F_rho, F_z, phi, magnetic_parameters)

    return F_x, F_y, F_z
