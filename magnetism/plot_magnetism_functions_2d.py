import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import magnetism.plot_settings as plts
from magnetism.coordinate_transformation import get_rectangle_path_xz
from magnetism.magnetic_field import evaluate_magnetic_field
from magnetism.magnetic_force import evaluate_magnetic_force

plts.set_params()

matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
plt.rcParams["font.sans-serif"] = "Noto Sans"

resolution = 51
x, z = np.meshgrid(
    np.linspace(-7e-3, 7e-3, resolution),
    np.linspace(-7e-3, 7e-3, resolution),
    indexing="ij",
)  # m

magnetic_parameters = {
    "radius_magnet": 2.0e-3,  # m
    "length": 7.0e-3,  # m
    "x_position": 0.0,  # m
    "y_position": 0.0,  # m
    "z_position": 0.0,  # m
    "magnetic_permeability": 1.25663706212e-6,  # N/A^2
    "magnetization": 1.05e6,  # A/m
    "dynamic_viscosity_fluid": 0.001,  # Pa s
    "radius_particle": 100e-9,  # m
    "rotation_x": 0,
    "rotation_y": 0,
    "magnetisation_model": "constant",
}

F_x = np.empty((resolution, resolution))
F_z = np.empty(F_x.shape)
H_x = np.empty(F_x.shape)
H_z = np.empty(F_x.shape)

for i in range(resolution):
    for k in range(resolution):
        H_x[i, k], _, H_z[i, k] = evaluate_magnetic_field(
            x[i, k], 0, z[i, k], magnetic_parameters
        )
        F_x[i, k], _, F_z[i, k] = evaluate_magnetic_force(
            x[i, k], 0, z[i, k], magnetic_parameters
        )

# Force: N -> pN
F_x = F_x * 1e12
F_z = F_z * 1e12

# H field: A/m -> kA/m = A/mm
H_x = H_x * 1e-3
H_z = H_z * 1e-3

# Position: m -> mm
x = x * 1e3
z = z * 1e3

force_magnitude = np.sqrt(F_x**2 + F_z**2)
field_magnitude = np.sqrt(H_x**2 + H_z**2)

# Plotting
half_width = 80 / 25.4
fig1, ax1 = plt.subplots(1, 1, figsize=(half_width, 3.0))
fig2, ax2 = plt.subplots(1, 1, figsize=(half_width, 3.0))

force_levels = np.linspace(0, 1.0, 200)
field_levels = np.linspace(0, 500, 200)

contour_force = ax1.contourf(
    x,
    z,
    force_magnitude,
    vmin=0,
    vmax=1.0,
    cmap="cividis",
    levels=force_levels,
    extend="max",
)
contour_field = ax2.contourf(
    x,
    z,
    field_magnitude,
    vmin=0,
    vmax=500,
    cmap="plasma",
    levels=field_levels,
    extend="max",
)

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="5%", pad=0.08)
cbar_force = fig1.colorbar(contour_force, ax=ax1, cax=cax1)
cbar_force.set_label("Magnetic force (pN)")
cbar_force.set_ticks([0, 1])

divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="5%", pad=0.08)
cbar_field = fig2.colorbar(contour_field, ax=ax2, cax=cax2)
cbar_field.set_label("Magnetic field H (kA/m)")
cbar_field.set_ticks([0, 500])

ax1.streamplot(
    x[:, :].transpose(),
    z[:, :].transpose(),
    F_x[:, :].transpose(),
    F_z[:, :].transpose(),
    density=[1.5, 1.5],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)
ax2.streamplot(
    x[:, :].transpose(),
    z[:, :].transpose(),
    H_x[:, :].transpose(),
    H_z[:, :].transpose(),
    density=[1, 2],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)

radius = magnetic_parameters["radius_magnet"] * 1e3
length = magnetic_parameters["length"] * 1e3
path = get_rectangle_path_xz(magnetic_parameters, radius, length)

for ax in [ax1, ax2]:
    ax.add_patch(mpatches.PathPatch(path, facecolor="none", edgecolor="k"))
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_xticks([-5, 0, 5])
    ax.set_yticks([-5, 0, 5])
    ax.set_xlim((-7, 7))
    ax.set_ylim((-7, 7))
    ax.set_aspect("equal", adjustable="box")

for contour in [contour_force, contour_field]:
    for c in contour.collections:
        c.set_edgecolor("face")

for cbar in [cbar_force, cbar_field]:
    cbar.minorticks_on()
    cbar.solids.set_edgecolor("face")

for fig in [fig1, fig2]:
    fig.tight_layout()

plt.show()

output_name = f"Magnet_{radius}mm_{length}mm"
# fig1.savefig(output_name + "_force_XZ.pdf", dpi=600)
# fig2.savefig(output_name + "_field_XZ.pdf", dpi=600)
