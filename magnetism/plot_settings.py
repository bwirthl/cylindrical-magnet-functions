import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
from coordinate_transformation import (transform_coordinates_backward_magnet_x,
                                       transform_coordinates_backward_magnet_y)

pagewidth_mm = 155.5
# pagewith in inch
pagewidth = pagewidth_mm / 25.4

# Default Matplotlib parameters
params = {
    "FontsizeReg": 9,
    "FontsizeMed": 9,
    "FontsizeSmall": 8,
}

params_rc_default = {
    "text.usetex": False,
    "font.size": params["FontsizeReg"],
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.stretch": "normal",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Helvetica",
    "mathtext.it": "Helvetica:italic",
    "mathtext.bf": "Helvetica:bold",
    "mathtext.sf": "Helvetica",
    # Default figure size (in)
    "figure.figsize": (pagewidth, 3.5),
    # DPI of display figures (adapt to screen as needed)
    "figure.dpi": 200,
    # DPI of saved figures
    "savefig.dpi": 600,
    # Use unicode minus symbol
    "axes.unicode_minus": True,
    # Width of axes
    "axes.linewidth": 0.7,
    # Width of axes x and y ticks
    "xtick.major.width": 0.7,
    "xtick.minor.width": 0.7,
    "ytick.major.width": 0.7,
    "ytick.minor.width": 0.7,
}


# Function definitions
def set_params(params_rc=None):
    """Set Matplotlib parameters"""

    if params_rc is None:
        params_rc = {}
    plt.rcParams.update({**params_rc_default, **params_rc})


# Set default Matplotlib parameters
set_params()


def get_path(magnetic_parameters, radius, length):
    verts = [
        transform_coordinates_backward_magnet_y(
            -radius, 0, -0.5 * length, magnetic_parameters
        ),  # left, bottom
        transform_coordinates_backward_magnet_y(
            -radius, 0, 0.5 * length, magnetic_parameters
        ),  # left, top
        transform_coordinates_backward_magnet_y(
            radius, 0, 0.5 * length, magnetic_parameters
        ),  # right, top
        transform_coordinates_backward_magnet_y(
            radius, 0, -0.5 * length, magnetic_parameters
        ),  # right, bottom
        transform_coordinates_backward_magnet_y(
            -radius, 0, -0.5 * length, magnetic_parameters
        ),  # ignored
    ]

    Path = mpath.Path
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    path = Path(verts, codes)
    return path
