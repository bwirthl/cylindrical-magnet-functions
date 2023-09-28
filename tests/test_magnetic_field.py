import pytest
from magnetism.magnetic_field import evaluate_magnetic_field

# base units are: mm, s, g, A
# 1 N = 1 kg m/s^2 = 1e6 g mm/s^2


def test_magnetic_field_1(magnetic_parameters_base):
    # Test the force outside the magnet
    X = 3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_field(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(100.72163529362592, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(63.49616909294483, 1e-14)


def test_magnetic_field_2(magnetic_parameters_base):
    # Test symmetry (swap X and Y)
    X = 0.0
    Y = 3.0
    Z = 4.0
    result = evaluate_magnetic_field(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(0, 1e-14)
    assert result[1] == pytest.approx(100.72163529362592, 1e-14)
    assert result[2] == pytest.approx(63.49616909294483, 1e-14)


def test_magnetic_field_3(magnetic_parameters_base):
    # Test symmetry (negative X)
    X = -3.0
    Y = 0.0
    Z = 4.0
    result = evaluate_magnetic_field(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(-100.72163529362592, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(63.49616909294483, 1e-14)


def test_magnetic_field_4(magnetic_parameters_base):
    # Test symmetry (negative X and Z)
    X = -3.0
    Y = 0.0
    Z = -4.0
    result = evaluate_magnetic_field(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(100.72163529362592, 1e-14)
    assert result[1] == pytest.approx(0, 1e-14)
    assert result[2] == pytest.approx(63.49616909294483, 1e-14)


def test_magnetic_field_5(magnetic_parameters_base):
    # Test another point closer to the axis of the magnet
    X = 0.5
    Y = 0.4
    Z = 2.9
    result = evaluate_magnetic_field(X, Y, Z, magnetic_parameters_base)

    assert result[0] == pytest.approx(45.5237803563867, 1e-14)
    assert result[1] == pytest.approx(36.419024285109366, 1e-14)
    assert result[2] == pytest.approx(371.5106772862314, 1e-14)
