import numpy as np
from src.constants import mu

def cartesian_to_keplerian(projected_states):
    x = projected_states[:,0]
    y = projected_states[:,1]
    z = projected_states[:,2]
    v_x = projected_states[:,3]
    v_y = projected_states[:,4]
    v_z = projected_states[:,5]

    position = projected_states[:, :3]
    velocity = projected_states[:, 3:]
    position_magnitudes = np.linalg.norm(position, axis = 1)
    velocity_magnitudes = np.linalg.norm(velocity, axis = 1)

    r_vecs = projected_states[:, 0:3]
    v_vecs = projected_states[:, 3:6]
    h_vecs = np.cross(r_vecs, v_vecs)  # Full 3D angular momentum matrix
    h_x = h_vecs[:, 0]
    h_y = h_vecs[:, 1]

    ecc_x = (1 / mu) * (((velocity_magnitudes ** 2 - mu / position_magnitudes) * x) - (np.sum(position * velocity, axis = 1) * v_x))
    ecc_y = (1 / mu) * (((velocity_magnitudes ** 2 - mu / position_magnitudes) * y) - (np.sum(position * velocity, axis = 1) * v_y))
    ecc_z = (1 / mu) * (((velocity_magnitudes ** 2 - mu / position_magnitudes) * z) - (np.sum(position * velocity, axis = 1) * v_z))

    # ECCENTRICITY
    ecc = np.sqrt((ecc_x ** 2) + (ecc_y ** 2) + (ecc_z ** 2))

    # NODE VECTOR (WHEN ORBIT CROSSES EQUATOR)
    n_x = -h_y
    n_y = h_x
    n_mag = np.sqrt(n_x**2 + n_y**2)

    # RAAN & AOP KEPLERIAN ELEMENTS
    raan_angles = np.arctan2(n_y, n_x)
    raan_angles = np.where(raan_angles < 0, raan_angles + 2 * np.pi, raan_angles) # Bounded between 0 and 2pi

    n_dot_e = (n_x * ecc_x) + (n_y * ecc_y) # Dot product between node and eccentricity vectors

    aop_angles = np.arccos(np.clip(n_dot_e / (n_mag * ecc + 1e-15), -1.0, 1.0)) # arccos bounds = [-1, 1]
    aop_angles = np.where(ecc_z < 0, 2 * np.pi - aop_angles, aop_angles) # flips orientation for south-pointing perigee

    raan_degrees = np.degrees(raan_angles)
    aop_degrees = np.degrees(aop_angles)

    return raan_degrees, aop_degrees # Degrees of RAAN & AOP at each RK4 time step