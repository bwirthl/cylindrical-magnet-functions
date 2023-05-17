import pytest

from magnetism.evaluate_magnetic_force import evaluate_magnetic_force

# base units are: mm, s, g, A
# 1 N = 1 kg m/s^2 = 1e6 g mm/s^2


def test_magnetic_force_1(magnetic_parameters_base):
    # Test the force outside the magnet
    X = 3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(-0.04581864194950962, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(-0.019705863530383092, 1e-14)


def test_magnetic_force_2(magnetic_parameters_base):
    # Test symmetry (swap X and Y)
    X = 0.0
    Y = 3.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0, 1e-14)
    assert result[1] == pytest.approx(-0.04581864194950962, 1e-14)
    assert result[2] == pytest.approx(-0.019705863530383092, 1e-14)


def test_magnetic_force_3(magnetic_parameters_base):
    # Test symmetry (negative X)
    X = -3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0.04581864194950962, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(-0.019705863530383092, 1e-14)


def test_magnetic_force_4(magnetic_parameters_base):
    # Test symmetry (negative X and Z)
    X = -3.0
    Y = 0.0
    Z = -4.0
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0.04581864194950962, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(0.019705863530383092, 1e-14)


def test_magnetic_force_5(magnetic_parameters_base):
    # Test another point closer to the axis of the magnet
    X = 0.5
    Y = 0.4
    Z = 2.9
    result = evaluate_magnetic_force(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0.008422241029651797, 1e-14)
    assert result[1] == pytest.approx(0.0067377928237214385, 1e-14)
    assert result[2] == pytest.approx(-0.19534212681287147, 1e-14)
