import numpy as np


def transform_coordinates_forward(X, Y, Z, params):
    # convert rotation angles to radians
    gamma = params["rotation_x"] * np.pi / 180
    beta = params["rotation_y"] * np.pi / 180

    # translate coordinates
    x_translated = X - params["x_position"]
    y_translated = Y - params["y_position"]
    z_translated = Z - params["z_position"]

    # rotate coordinates
    xi = (
        x_translated * np.cos(beta)
        + y_translated * np.sin(beta) * np.sin(gamma)
        + z_translated * np.sin(beta) * np.cos(gamma)
    )
    eta = y_translated * np.cos(gamma) - z_translated * np.sin(gamma)
    zeta = (
        -x_translated * np.sin(beta)
        + y_translated * np.cos(beta) * np.sin(gamma)
        + z_translated * np.cos(beta) * np.cos(gamma)
    )

    # transform to cylindrical coordinates
    rho = np.sqrt(xi**2 + eta**2)
    phi = np.arctan2(eta, xi)
    z = zeta

    if np.abs(rho) < 1e-6:
        rho = 1e-6

    return rho, phi, z


def transform_vector_backward(rho_component, z_component, phi, params):
    # convert rotation angles to radians
    gamma = params["rotation_x"] * np.pi / 180
    beta = params["rotation_y"] * np.pi / 180

    # transform to cartesian coordinates
    xi = rho_component * np.cos(phi)
    eta = rho_component * np.sin(phi)
    zeta = z_component

    # rotate coordinates
    X_component = xi * np.cos(beta) - zeta * np.sin(beta)
    Y_component = (
        xi * np.sin(beta) * np.sin(gamma)
        + eta * np.cos(gamma)
        + zeta * np.sin(gamma) * np.cos(beta)
    )
    Z_component = (
        xi * np.sin(beta) * np.cos(gamma)
        - eta * np.sin(gamma)
        + zeta * np.cos(beta) * np.cos(gamma)
    )

    return X_component, Y_component, Z_component


def transform_coordinates_backward_magnet_y(xi, eta, zeta, params):
    # convert rotation angles to radians
    gamma = params["rotation_x"] * np.pi / 180
    beta = params["rotation_y"] * np.pi / 180

    # rotate coordinates
    X = xi * np.cos(beta) - zeta * np.sin(beta)
    Z = (
        xi * np.sin(beta) * np.cos(gamma)
        - eta * np.sin(gamma)
        + zeta * np.cos(beta) * np.cos(gamma)
    )

    # translate coordinates
    x = X + params["x_position"]
    z = Z + params["z_position"]

    return x, z


def transform_coordinates_backward_magnet_x(xi, eta, zeta, params):
    # convert rotation angles to radians
    gamma = params["rotation_x"] * np.pi / 180
    beta = params["rotation_y"] * np.pi / 180

    # rotate coordinates
    Y = (
        xi * np.sin(beta) * np.sin(gamma)
        + eta * np.cos(gamma)
        + zeta * np.sin(gamma) * np.cos(beta)
    )
    Z = (
        xi * np.sin(beta) * np.cos(gamma)
        - eta * np.sin(gamma)
        + zeta * np.cos(beta) * np.cos(gamma)
    )

    # translate coordinates
    y = Y + params["y_position"]
    z = Z + params["z_position"]

    return y, z
