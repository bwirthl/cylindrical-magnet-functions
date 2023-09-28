import numpy as np


def evaluate_magnetic_force_inf(x, y, z, magnetic_parameters):
    """Evaluate the magnetic force for an infinite magnet.

    Taken from:
    E. P. Furlani and K. C. Ng. “Analytical Model of Magnetic Nanoparticle
    Transport and Capture in the Microvasculature”. Physical Review E 73.6
    (2006), 061919. https://doi.org/10.1103/PhysRevE.73.061919.
    """
    R = magnetic_parameters["radius_magnet"]
    x = x - magnetic_parameters["x_position"]

    volume_particle = (
        (4 / 3) * np.pi * np.power(magnetic_parameters["radius_particle"], 3)
    )
    d = -magnetic_parameters["z_position"]

    F_x = (
        -magnetic_parameters["magnetization"] ** 2
        * magnetic_parameters["magnetic_permeability"]
        * volume_particle
        * R**4
        * x
        / (2 * ((z + d) ** 2 + x**2) ** 3)
    )

    F_z = (
        -magnetic_parameters["magnetization"] ** 2
        * magnetic_parameters["magnetic_permeability"]
        * volume_particle
        * R**4
        * (z + d)
        / (2 * ((z + d) ** 2 + x**2) ** 3)
    )

    return F_x, 0, F_z
