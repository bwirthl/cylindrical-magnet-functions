import matplotlib.pyplot as plt

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
    "font.stretch": "normal",
    "mathtext.fontset": "custom",
    # Default figure size (in)
    "figure.figsize": (pagewidth, 3.5),
    # DPI of display figures (adapt to screen as needed)
    "figure.dpi": 200,
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
