import numpy as np
from src.constants import mu

def elements_to_state_vectors(a, E, i, o, w, v):
    r = (a * (1 - E ** 2) / (1 + E * np.cos(v)))  # Earth center to satellite in km

    r_pqw = np.round(np.array([r * np.cos(v), r * np.sin(v), 0]), 7)  # Perifocal position vectors

    h = np.sqrt(mu * a * (1 - (E ** 2)))  # Specific Angular Momentum
    sf = mu / h  # Scaling Factor

    v_pqw = np.round(np.array([-sf * np.sin(v), sf * (E + np.cos(v)), 0]), 3)  # Perifocal velocity vectors

    # ROTATION MATRIX
    # Row 1
    R_11 = (np.cos(o) * np.cos(w)) - (np.sin(o) * np.sin(w) * np.cos(i))
    R_12 = (-np.cos(o) * np.sin(w)) - (np.sin(o) * np.cos(w) * np.cos(i))
    R_13 = (np.sin(o) * np.sin(i))

    # Row 2
    R_21 = (np.sin(o) * np.cos(w)) + (np.cos(o) * np.sin(w) * np.cos(i))
    R_22 = (-np.sin(o) * np.sin(w)) + (np.cos(o) * np.cos(w) * np.cos(i))
    R_23 = (-np.cos(o) * np.sin(i))

    # Row 3
    R_31 = np.sin(w) * np.sin(i)
    R_32 = np.cos(w) * np.sin(i)
    R_33 = np.cos(i)

    R = np.array([
        [R_11, R_12, R_13],
        [R_21, R_22, R_23],
        [R_31, R_32, R_33]
    ])

    r_xyz = R @ r_pqw
    v_xyz = R @ v_pqw

    return np.concatenate([r_xyz, v_xyz])