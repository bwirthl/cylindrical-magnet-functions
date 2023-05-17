import matplotlib
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import plot_settings as plts
from coordinate_transformation import (transform_coordinates_backward_magnet_x,
                                       transform_coordinates_backward_magnet_y)
from evaluate_magnetic_field import evaluate_magnetic_field
from evaluate_magnetic_force import evaluate_magnetic_force

plts.set_params()

matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
plt.rcParams["font.sans-serif"] = "Myriad Pro"

resolution = 251
x, y, z = np.meshgrid(
    np.linspace(-7, 7, resolution),
    np.linspace(-7, 7, resolution),
    np.linspace(-7, 7, resolution),
    indexing="ij",
)  # mm

magnetic_parameters = {
    "radius_magnet": 2.0,
    "length": 7.0,
    "x_position": 0.0,
    "y_position": 0.0,
    "z_position": 0.0,
    "magnetic_permeability": 1.25663706212,
    "magnetization": 1e3,
    "dynamic_viscosity_fluid": 0.001,
    "radius_particle": 100e-6,
    "rotation_x": 0,
    "rotation_y": 0,
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

force_magnitude = np.sqrt(F_x**2 + F_y**2 + F_z**2)
field_magnitude = np.sqrt(H_x**2 + H_y**2 + H_z**2)

# Plotting
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

force_levels = np.linspace(0, 1.0, 40)
force_levels[-1] = 15

y_idx = int(resolution / 2)
cp = ax1.contourf(
    x[:, y_idx, :],
    z[:, y_idx, :],
    force_magnitude[:, y_idx, :],
    vmin=0,
    vmax=1.0,
    levels=force_levels,
    extend="max",
)
cp2 = ax2.contourf(
    x[:, y_idx, :],
    z[:, y_idx, :],
    field_magnitude[:, y_idx, :],
    levels=np.linspace(0, np.nanmax(field_magnitude), 40),
)
for c in cp.collections:
    c.set_edgecolor("face")
for c in cp2.collections:
    c.set_edgecolor("face")

cbar = fig1.colorbar(cp, ax=ax1)
cbar.set_label("Magnetic force (μN)")
cbar.set_ticks([0, 0.5, 1])
cbar.minorticks_on()
cbar.solids.set_edgecolor("face")

cbar2 = fig2.colorbar(cp2, ax=ax2)
cbar2.set_label("Magnetic field H (A/mm)")
cbar2.solids.set_edgecolor("face")

ax1.streamplot(
    x[:, y_idx, :].transpose(),
    z[:, y_idx, :].transpose(),
    F_x[:, y_idx, :].transpose(),
    F_z[:, y_idx, :].transpose(),
    density=[1.5, 1.5],
    color=force_magnitude[:, y_idx, :].transpose(),
    cmap="YlGnBu",
    linewidth=0.7,
    # broken_streamlines=False,
)
ax2.streamplot(
    x[:, y_idx, :].transpose(),
    z[:, y_idx, :].transpose(),
    H_x[:, y_idx, :].transpose(),
    H_z[:, y_idx, :].transpose(),
    density=[1, 2],
    color=field_magnitude[:, y_idx, :].transpose(),
    cmap="YlGnBu",
    linewidth=1.0,
    # broken_streamlines=False,
)


radius = magnetic_parameters["radius_magnet"]
length = magnetic_parameters["length"]
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
ax1.add_patch(mpatches.PathPatch(path, facecolor="none", edgecolor="tab:orange"))
ax2.add_patch(mpatches.PathPatch(path, facecolor="none", edgecolor="tab:orange"))

ax1.set_xlabel("x (mm)")
ax1.set_ylabel("z (mm)")
ax2.set_xlabel("x (mm)")
ax2.set_ylabel("z (mm)")

ax1.set_xlim((-7, 7))
ax2.set_xlim((-7, 7))
ax1.set_ylim((-7, 7))
ax2.set_ylim((-7, 7))

ax1.set_title("XZ slice")
ax2.set_title("XZ slice")

ax1.set_aspect("equal", adjustable="box")
ax2.set_aspect("equal", adjustable="box")

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
fig4 = plt.figure()
ax4 = fig4.add_subplot(111)

x_idx = int(resolution / 2)
cp3 = ax3.contourf(
    y[x_idx, :, :],
    z[x_idx, :, :],
    force_magnitude[x_idx, :, :],
    vmin=0,
    vmax=1.0,
    levels=force_levels,
    extend="max",
)
cp4 = ax4.contourf(
    y[x_idx, :, :],
    z[x_idx, :, :],
    field_magnitude[x_idx, :, :],
    levels=np.linspace(0, np.nanmax(field_magnitude), 40),
)
for c in cp3.collections:
    c.set_edgecolor("face")
for c in cp4.collections:
    c.set_edgecolor("face")

cbar3 = fig3.colorbar(cp3, ax=ax3)
cbar3.set_label("Magnetic force (μN)")
cbar3.set_ticks([0, 0.5, 1])
cbar3.minorticks_on()
cbar3.solids.set_edgecolor("face")

cbar4 = fig4.colorbar(cp4, ax=ax4)
cbar4.set_label("Magnetic field H (A/mm)")
cbar4.solids.set_edgecolor("face")

ax3.streamplot(
    y[x_idx, :, :].transpose(),
    z[x_idx, :, :].transpose(),
    F_y[x_idx, :, :].transpose(),
    F_z[x_idx, :, :].transpose(),
    density=[1.5, 1.5],
    color=force_magnitude[x_idx, :, :].transpose(),
    cmap="YlGnBu",
    linewidth=0.7,
    # broken_streamlines=False,
)
ax4.streamplot(
    y[x_idx, :, :].transpose(),
    z[x_idx, :, :].transpose(),
    H_y[x_idx, :, :].transpose(),
    H_z[x_idx, :, :].transpose(),
    density=[1, 2],
    color=field_magnitude[x_idx, :, :].transpose(),
    cmap="YlGnBu",
    linewidth=1.0,
    # broken_streamlines=False,
)

radius = magnetic_parameters["radius_magnet"]
length = magnetic_parameters["length"]
verts = [
    transform_coordinates_backward_magnet_x(
        0, -radius, -0.5 * length, magnetic_parameters
    ),  # left, bottom
    transform_coordinates_backward_magnet_x(
        0, -radius, 0.5 * length, magnetic_parameters
    ),  # left, top
    transform_coordinates_backward_magnet_x(
        0, radius, 0.5 * length, magnetic_parameters
    ),  # right, top
    transform_coordinates_backward_magnet_x(
        0, radius, -0.5 * length, magnetic_parameters
    ),  # right, bottom
    transform_coordinates_backward_magnet_x(
        0, -radius, -0.5 * length, magnetic_parameters
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
ax3.add_patch(mpatches.PathPatch(path, facecolor="none", edgecolor="tab:orange"))
ax4.add_patch(mpatches.PathPatch(path, facecolor="none", edgecolor="tab:orange"))

ax3.set_xlabel("y (mm)")
ax3.set_ylabel("z (mm)")
ax4.set_xlabel("y (mm)")
ax4.set_ylabel("z (mm)")

ax3.set_xlim((-7, 7))
ax4.set_xlim((-7, 7))
ax3.set_ylim((-7, 7))
ax4.set_ylim((-7, 7))

ax3.set_title("YZ slice")
ax4.set_title("YZ slice")

ax3.set_aspect("equal", adjustable="box")
ax4.set_aspect("equal", adjustable="box")

fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig4.tight_layout()

plt.tight_layout()
plt.show()

output_name = f"Magnet_centered"
fig1.savefig(output_name + "_force_XZ.pdf", dpi=600)
fig2.savefig(output_name + "_field_XZ.pdf", dpi=600)
fig3.savefig(output_name + "_force_YZ.pdf", dpi=600)
fig4.savefig(output_name + "_field_YZ.pdf", dpi=600)
