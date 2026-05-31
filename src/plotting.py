import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec
from src.constants import R_p

def dashboard(projected_states, longitude, latitude, times, nodal_regression, perigee_rotation):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.25)

    # 3D ORBIT (TOP LEFT)
    ax = fig.add_subplot(gs[0, 0], projection='3d')

    length = 6000
    ax.quiver(0, 0, 0, length, 0, 0, color='r', label='X')
    ax.quiver(0, 0, 0, 0, length, 0, color='g', label='Y')
    ax.quiver(0, 0, 0, 0, 0, length, color='b', label='Z')

    x_path = projected_states[:, 0]
    y_path = projected_states[:, 1]
    z_path = projected_states[:, 2]
    ax.plot3D(x_path, y_path, z_path, color='purple', label='Satellite Orbit', linewidth=4)

    ax.plot([x_path[0]], [y_path[0]], [z_path[0]], 'o',
            color='green', markersize=7, label='Initial Position')
    ax.plot([x_path[-1]], y_path[-1], z_path[-1], 'o',
            color='blue', markersize=7, label='Final Position')

    U, V = np.mgrid[0:2 * np.pi:30j, 0:np.pi:30j]
    x_planet = R_p * np.cos(U) * np.sin(V)
    y_planet = R_p * np.sin(U) * np.sin(V)
    z_planet = R_p * np.cos(V)
    ax.plot_surface(x_planet, y_planet, z_planet, color='blue', alpha=0.1)
    ax.plot_wireframe(x_planet, y_planet, z_planet, color='black', alpha=0.1)

    ax.set_xlabel('X (km)', fontsize=7, labelpad=1)
    ax.set_ylabel('Y (km)', fontsize=7, labelpad=1)
    ax.set_zlabel('Z (km)', fontsize=7, labelpad=1)
    ax.set_title('3D Orbit Trajectory', fontsize=10, fontweight='bold')

    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)
    ax.tick_params(axis='z', labelsize=7)

    max_range = np.array([
        x_path.max() - x_path.min(),
        y_path.max() - y_path.min(),
        z_path.max() - z_path.min()
    ]).max() / 2.0
    mid_x = (x_path.max() + x_path.min()) * 0.5
    mid_y = (y_path.max() + y_path.min()) * 0.5
    mid_z = (z_path.max() + z_path.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.scatter(x_path, y_path, z_path,
               c=np.linspace(0, 1, len(x_path)),
               cmap='plasma', s=1)

    ax.set_box_aspect([1, 1, 1])
    ax.legend(
        loc='upper right',
        fontsize=6,
        edgecolor='black',
        handlelength=1.2,
        markerscale=0.7,
        borderpad=0.4
    )
    ax.view_init(elev=35.16, azim=45)

    # GROUND MAPPING (TOP RIGHT)
    ax_map = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree())
    ax_map.set_global()

    ax_map.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    ax_map.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax_map.add_feature(cfeature.COASTLINE, linewidth=1.0)
    ax_map.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')

    gl = ax_map.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False

    ax_map.plot(longitude, latitude, color='purple', linewidth=2.0,
                transform=ccrs.Geodetic(), label='Trajectory')
    ax_map.scatter(longitude[0], latitude[0], color='green', s=25,
                   zorder=5, transform=ccrs.Geodetic(), label='Start')
    ax_map.scatter(longitude[-1], latitude[-1], color='blue', s=25,
                   zorder=5, transform=ccrs.Geodetic(), label='End')
    ax_map.set_title('Ground Map Trajectory', fontsize=10, fontweight='bold')
    ax_map.legend(loc='lower left', fontsize = 6)

    # DRIFT (BOTTOM ROW)
    times_raw = np.squeeze(times)
    raan_raw  = np.squeeze(nodal_regression)
    aop_raw   = np.squeeze(perigee_rotation)

    raan_unwrapped = np.degrees(np.unwrap(np.radians(raan_raw)))
    aop_unwrapped  = np.degrees(np.unwrap(np.radians(aop_raw)))

    valid_mask = (
        np.isfinite(times_raw) &
        np.isfinite(raan_unwrapped) &
        np.isfinite(aop_unwrapped)
    )

    time_clean    = times_raw[valid_mask]
    raan_clean    = raan_unwrapped[valid_mask]
    perigee_clean = aop_unwrapped[valid_mask]

    if len(time_clean) < 2:
        print("Empty time array")
        return

    slope_raan, intercept_raan = np.polyfit(time_clean, raan_clean, 1)
    slope_aop,  intercept_w    = np.polyfit(time_clean, perigee_clean, 1)

    trend_raan = (slope_raan * time_clean) + intercept_raan
    trend_aop  = (slope_aop  * time_clean) + intercept_w

    drift_raan_day = slope_raan * 86400.0
    drift_aop_day  = slope_aop  * 86400.0

    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1], sharex=ax1)

    # LEFT GRAPH (RAAN)
    if slope_raan != 0.0:
        ax1.plot(time_clean / 3600.0, trend_raan,
                 label=f'Trend: {drift_raan_day:.4f}°/day', color='darkred')
    ax1.plot(time_clean / 3600.0, raan_clean, label='Simulated Data', color='darkgreen', alpha=0.8)
    ax1.set_xlabel('Time elapsed (Hours)')
    ax1.set_ylabel(r'RAAN, $\Omega$ (Degrees)')
    ax1.set_title('RAAN Drift vs. Time', fontsize=10, fontweight='bold', loc = 'center')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')

    # RIGHT GRAPH (AOP)
    ax2.plot(time_clean / 3600.0, perigee_clean, label='Simulated Data', color='mediumseagreen', alpha=0.8)
    if slope_aop != 0.0:
        ax2.plot(time_clean / 3600.0, trend_aop,
                 label=f'Trend: {drift_aop_day:.4f}°/day', color='darkred')
    ax2.set_xlabel('Time elapsed (Hours)')
    ax2.set_ylabel(r'Argument of Perigee, $\omega$ (Degrees)')
    ax2.set_title('AOP Drift vs. Time', fontsize=10, fontweight='bold', loc='center')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left')

    fig.suptitle('Orbital Simulation Dashboard', fontsize=14, fontweight='bold')
    plt.subplots_adjust(top=0.93)
    plt.show()