import pytest

# base units are: mm, s, g, A
# 1 N = 1 kg m/s^2 = 1e6 g mm/s^2

@pytest.fixture
def magnetic_parameters_base():
    magnetic_parameters = {
        "radius_magnet": 2.5, # mm
        "length": 5.0, # mm
        "x_position": 0.0, # mm
        "y_position": 0.0, # mm
        "z_position": 0.0, # mm
        "magnetic_permeability": 1.25663706212, #  1e-6 N/A^2 = 1 g mm / (A^2 s^2)
        "magnetization": 1e3, # A/mm
        "dynamic_viscosity_fluid": 0.001, # Pa s
        "radius_particle": 100e-6, # 100e-6 mm = 100 nm
        "rotation_x": 0, # degrees
        "rotation_y": 0, # degrees
    }
    return magnetic_parameters