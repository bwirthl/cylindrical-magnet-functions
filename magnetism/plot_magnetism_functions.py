import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

import magnetism.plot_settings as plts
from magnetism.coordinate_transformation import (
    get_rectangle_path_xz,
    get_rectangle_path_yz,
)
from magnetism.magnetic_field import evaluate_magnetic_field
from magnetism.magnetic_force import evaluate_magnetic_force

plts.set_params()

matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")

resolution = 51
x, y, z = np.meshgrid(
    np.linspace(-7e-3, 7e-3, resolution),
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
    "rotation_x": 40,
    "rotation_y": 0,
    "magnetisation_model": "constant",
}

F_x = np.empty((resolution, resolution, resolution))
F_y = np.empty((resolution, resolution, resolution))
F_z = np.empty((resolution, resolution, resolution))

H_x = np.empty((resolution, resolution, resolution))
H_y = np.empty((resolution, resolution, resolution))
H_z = np.empty((resolution, resolution, resolution))

for i in range(resolution):
    for j in range(resolution):
        for k in range(resolution):
            H_x[i, j, k], H_y[i, j, k], H_z[i, j, k] = evaluate_magnetic_field(
                x[i, j, k], y[i, j, k], z[i, j, k], magnetic_parameters
            )
            F_x[i, j, k], F_y[i, j, k], F_z[i, j, k] = evaluate_magnetic_force(
                x[i, j, k], y[i, j, k], z[i, j, k], magnetic_parameters
            )

# Force: N -> pN
F_x = F_x * 1e12
F_y = F_y * 1e12
F_z = F_z * 1e12

# H field: A/m -> kA/m = A/mm
H_x = H_x * 1e-3
H_y = H_y * 1e-3
H_z = H_z * 1e-3

# Position: m -> mm
x = x * 1e3
y = y * 1e3
z = z * 1e3

force_magnitude = np.sqrt(F_x**2 + F_y**2 + F_z**2)
field_magnitude = np.sqrt(H_x**2 + H_y**2 + H_z**2)

# Plotting
half_width = 80 / 25.4
fig1, ax1 = plt.subplots(1, 1, figsize=(half_width, 3.0))
fig2, ax2 = plt.subplots(1, 1, figsize=(half_width, 3.0))
fig3, ax3 = plt.subplots(1, 1, figsize=(half_width, 3.0))
fig4, ax4 = plt.subplots(1, 1, figsize=(half_width, 3.0))

force_levels = np.linspace(0, 1.0, 40)
field_levels = np.linspace(0, np.nanmax(field_magnitude), 40)

# choose which slice to plot
y_idx = int(resolution / 2)
contour_force_xz = ax1.contourf(
    x[:, y_idx, :],
    z[:, y_idx, :],
    force_magnitude[:, y_idx, :],
    vmin=0,
    vmax=1.0,
    cmap="cividis",
    levels=force_levels,
    extend="max",
)
contour_field_xz = ax2.contourf(
    x[:, y_idx, :],
    z[:, y_idx, :],
    field_magnitude[:, y_idx, :],
    cmap="plasma",
    levels=field_levels,
    extend="max",
)

ax1.streamplot(
    x[:, y_idx, :].transpose(),
    z[:, y_idx, :].transpose(),
    F_x[:, y_idx, :].transpose(),
    F_z[:, y_idx, :].transpose(),
    density=[1.5, 1.5],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)
ax2.streamplot(
    x[:, y_idx, :].transpose(),
    z[:, y_idx, :].transpose(),
    H_x[:, y_idx, :].transpose(),
    H_z[:, y_idx, :].transpose(),
    density=[1, 2],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)

# choose which slice to plot
x_idx = int(resolution / 2)
contour_force_yz = ax3.contourf(
    y[x_idx, :, :],
    z[x_idx, :, :],
    force_magnitude[x_idx, :, :],
    vmin=0,
    vmax=1.0,
    levels=force_levels,
    extend="max",
)
contour_field_yz = ax4.contourf(
    y[x_idx, :, :],
    z[x_idx, :, :],
    field_magnitude[x_idx, :, :],
    cmap="plasma",
    levels=field_levels,
    extend="max",
)

ax3.streamplot(
    y[x_idx, :, :].transpose(),
    z[x_idx, :, :].transpose(),
    F_y[x_idx, :, :].transpose(),
    F_z[x_idx, :, :].transpose(),
    density=[1.5, 1.5],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)
ax4.streamplot(
    y[x_idx, :, :].transpose(),
    z[x_idx, :, :].transpose(),
    H_y[x_idx, :, :].transpose(),
    H_z[x_idx, :, :].transpose(),
    density=[1, 2],
    color="xkcd:ivory",
    linewidth=0.5,
    arrowsize=0.5,
)

# axis settings
for ax in [ax1, ax2, ax3, ax4]:
    ax.set_xticks([-5, 0, 5])
    ax.set_yticks([-5, 0, 5])
    ax.set_xlim((-7, 7))
    ax.set_ylim((-7, 7))
    ax.set_aspect("equal", adjustable="box")

# add magnet outline
radius = magnetic_parameters["radius_magnet"] * 1e3
length = magnetic_parameters["length"] * 1e3
rectangle_xz = get_rectangle_path_xz(magnetic_parameters, radius, length)
rectangle_yz = get_rectangle_path_yz(magnetic_parameters, radius, length)

# XZ slices
for ax in [ax1, ax2]:
    ax.add_patch(mpatches.PathPatch(rectangle_xz, facecolor="none", edgecolor="k"))
    ax.set_title("XZ slice")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("z (mm)")

# YZ slices
for ax in [ax3, ax4]:
    ax.add_patch(mpatches.PathPatch(rectangle_yz, facecolor="none", edgecolor="k"))
    ax.set_title("YZ slice")
    ax.set_xlabel("y (mm)")
    ax.set_ylabel("z (mm)")

# colorbars for force plots
for ax, fig, contour in zip(
    [ax1, ax3], [fig1, fig3], [contour_force_xz, contour_force_yz]
):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.08)
    cbar_force = fig.colorbar(contour, ax=ax, cax=cax)
    cbar_force.set_label("Magnetic force (pN)")
    cbar_force.set_ticks([0, 1])
    cbar_force.minorticks_on()
    cbar_force.solids.set_edgecolor("face")

# colorbars for field plots
for ax, fig, contour in zip(
    [ax2, ax4], [fig1, fig3], [contour_field_xz, contour_field_yz]
):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.08)
    cbar_field = fig.colorbar(contour, ax=ax, cax=cax)
    cbar_field.set_label("Magnetic field H (kA/m)")
    cbar_field.minorticks_on()
    cbar_field.solids.set_edgecolor("face")

# set tight layout
for fig in [fig1, fig2, fig3, fig4]:
    fig.tight_layout()

# remove white lines in contour plots for pdf output
for contour in [contour_force_xz, contour_field_xz, contour_force_yz, contour_field_yz]:
    for c in contour.collections:
        c.set_edgecolor("face")


plt.show()

output_name = f"My_magnet"
fig1.savefig(output_name + "_force_XZ.pdf", dpi=600)
fig2.savefig(output_name + "_field_XZ.pdf", dpi=600)
fig3.savefig(output_name + "_force_YZ.pdf", dpi=600)
fig4.savefig(output_name + "_field_YZ.pdf", dpi=600)
