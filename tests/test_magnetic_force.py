import pytest
from magnetism.magnetic_force import evaluate_magnetic_force


def test_magnetic_force_1(magnetic_parameters_base):
    # Test the force outside the magnet
    X = 3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(-3.4546442147049736e-08, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(-3.714467765981674e-08, 1e-14)


def test_magnetic_force_2(magnetic_parameters_base):
    # Test symmetry (swap X and Y)
    X = 0.0
    Y = 3.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0, 1e-14)
    assert result[1] == pytest.approx(-3.4546442147049736e-08, 1e-14)
    assert result[2] == pytest.approx(-3.714467765981674e-08, 1e-14)


def test_magnetic_force_3(magnetic_parameters_base):
    # Test symmetry (negative X)
    X = -3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(3.4546442147049736e-08, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(-3.714467765981674e-08, 1e-14)


def test_magnetic_force_4(magnetic_parameters_base):
    # Test symmetry (negative X and Z)
    X = -3.0
    Y = 0.0
    Z = -4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(3.4546442147049736e-08, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(3.714467765981674e-08, 1e-14)


def test_magnetic_force_5(magnetic_parameters_base):
    # Test another point closer to the axis of the magnet
    X = 0.5
    Y = 0.4
    Z = 2.9
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(6.350220130923992e-09, 1e-14)
    assert result[1] == pytest.approx(5.080176104739194e-09, 1e-14)
    assert result[2] == pytest.approx(-3.682112343191538e-07, 1e-14)
