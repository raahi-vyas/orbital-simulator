import numpy as np
import pandas as pd
from src.constants import R_p

def lat_lon(projected_states):
    position_states = projected_states[:, :3]  # xyz position vector for all steps from RK4
    radius_magnitudes = np.linalg.norm(position_states, axis=1)  # computes 3D magnitude of all 3 position vectors in xyz

    x_path = projected_states[:, 0]  # Satellite orbital paths for each dimension (xyz)
    y_path = projected_states[:, 1]
    z_path = projected_states[:, 2]

    longitude = np.degrees(np.arctan2(y_path, x_path))  # longitude = azimuth
    latitude = 90 - np.degrees(np.arccos(z_path / radius_magnitudes))  # 90 - inclination = latitude

    return longitude, latitude, radius_magnitudes, position_states

def telemetry(projected_states, time_step, n_steps):
    df = pd.DataFrame({
        'time (s)': [step * time_step for step in range(n_steps)],
        'altitude (km)': [np.linalg.norm(projected_states[i][:3]) - R_p for i in range(n_steps)],
        'velocity (km / s)': [np.linalg.norm(projected_states[i][3:]) for i in range(n_steps)]})

    df.to_csv('data/telemetry.csv', index=False)
    return df