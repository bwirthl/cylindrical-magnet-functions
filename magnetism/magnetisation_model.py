import numpy as np


def evaluate_magnetisation_model(magnetic_parameters, H_magnitude, magnetic_volume):
    """Choose the magnetisation model."""
    if magnetic_parameters["magnetisation_model"] == "linear_saturation":
        return evaluate_mag_model_linear_sat(
            magnetic_parameters, H_magnitude, magnetic_volume
        )
    if magnetic_parameters["magnetisation_model"] == "constant":
        return evaluate_mag_model_constant(
            magnetic_parameters, H_magnitude, magnetic_volume
        )
    else:
        raise ValueError("Invalid magnetisation model.")


def evaluate_mag_model_constant(magnetic_parameters, H_magnitude, magnetic_volume):
    """Linear magnetisation model with saturation."""
    if magnetic_volume is None:
        magnetic_volume = (
            (4 / 3) * np.pi * np.power(magnetic_parameters["radius_particle"], 3)
        )
    f_H_volumetric = 1.0
    return f_H_volumetric * magnetic_volume


def evaluate_mag_model_linear_sat(magnetic_parameters, H_magnitude, magnetic_volume):
    """Linear magnetisation model with saturation."""
    if magnetic_volume is None:
        magnetic_volume = (
            (4 / 3) * np.pi * np.power(magnetic_parameters["radius_particle"], 3)
        )

    if (
        H_magnitude
        < (1.0 / 3.0) * magnetic_parameters["particle_saturation_magnetization"]
    ):
        f_H_volumetric = 3.0
    else:
        f_H_volumetric = (
            magnetic_parameters["particle_saturation_magnetization"] / H_magnitude
        )

    return f_H_volumetric * magnetic_volume
