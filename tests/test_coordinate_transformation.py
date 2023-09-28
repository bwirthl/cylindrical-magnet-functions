import numpy as np
import pytest
from magnetism.coordinate_transformation import (
    transform_coordinates_forward,
    transform_vector_backward,
)


def test_coordinate_transformation_1():
    params = {
        "x_position": 0,
        "y_position": 0,
        "z_position": 0,
        "rotation_x": 0,
        "rotation_y": 0,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    # avoid the singularity at rho = 0
    assert rho == pytest.approx(1e-9, 1e-14)
    assert phi == pytest.approx(0, 1e-14)
    assert z == pytest.approx(0, 1e-14)


def test_coordinate_transformation_2():
    params = {
        "x_position": -3.0,
        "y_position": 0,
        "z_position": -4.0,
        "rotation_x": 0,
        "rotation_y": 0,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    assert rho == pytest.approx(3.0, 1e-14)
    assert phi == pytest.approx(0, 1e-14)
    assert z == pytest.approx(4.0, 1e-14)


def test_coordinate_transformation_3():
    params = {
        "x_position": 3.0,
        "y_position": 4.0,
        "z_position": -4.0,
        "rotation_x": 0,
        "rotation_y": 0,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    assert rho == pytest.approx(5.0, 1e-14)
    assert phi == pytest.approx(np.arctan2(-4, -3), 1e-14)
    assert z == pytest.approx(4.0, 1e-14)


def test_coordinate_transformation_rotation_1():
    params = {
        "x_position": 0.0,
        "y_position": -4.0,
        "z_position": -3.0,
        "rotation_x": 20,
        "rotation_y": 0,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    test_rho = 4.0 * np.cos(np.pi * 20 / 180) - 3.0 * np.sin(np.pi * 20 / 180)
    test_z = 4.0 * np.sin(np.pi * 20 / 180) + 3.0 * np.cos(np.pi * 20 / 180)
    assert rho == pytest.approx(test_rho, 1e-14)
    assert phi == pytest.approx(np.pi / 2, 1e-14)
    assert z == pytest.approx(test_z, 1e-14)


def test_coordinate_transformation_rotation_2():
    params = {
        "x_position": 4.0,
        "y_position": 0.0,
        "z_position": -3.0,
        "rotation_x": 0,
        "rotation_y": 40,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    test_rho = 4.0 * np.cos(np.pi * 40 / 180) - 3.0 * np.sin(np.pi * 40 / 180)
    test_z = 4.0 * np.sin(np.pi * 40 / 180) + 3.0 * np.cos(np.pi * 40 / 180)
    assert rho == pytest.approx(test_rho, 1e-14)
    assert phi == pytest.approx(np.pi, 1e-14)
    assert z == pytest.approx(test_z, 1e-14)


def test_coordinate_transformation_rotation_3():
    params = {
        "x_position": 4.0,
        "y_position": 5.0,
        "z_position": -3.0,
        "rotation_x": -30,
        "rotation_y": 40,
    }

    X = 0
    Y = 0
    Z = 0
    rho, phi, z = transform_coordinates_forward(X, Y, Z, params)

    assert rho == pytest.approx(2.8381162459829663, 1e-14)
    assert phi == pytest.approx(-1.4957457178897988, 1e-14)
    assert z == pytest.approx(6.476503391050418, 1e-14)
