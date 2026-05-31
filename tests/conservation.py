import numpy as np
from src.constants import R_p
from src.rk4 import j2

def energy_conservation(projected_states, n_steps, mu, radius_magnitudes, position_states):
    velocity_states = projected_states[:, 3:]
    velocity_magnitudes = np.linalg.norm(velocity_states, axis=1)
    z = projected_states[:, 2]

    # ENERGIES (GRAVITATIONAL & J2 POTENTIAL)
    gravitational_potential = (0.5 * (velocity_magnitudes ** 2)) - (mu / radius_magnitudes)
    j2_potential = (mu / radius_magnitudes) * (j2 / 2) * ((R_p / radius_magnitudes) ** 2) * (3 * ((z / radius_magnitudes) ** 2) -1)

    # SUM OF ALL ENERGIES
    orbital_energy = gravitational_potential + j2_potential

    #ANGULAR MOMENTUM
    angular_momentum = [np.linalg.norm(np.cross(position_states, velocity_states)) for JJ in
                        range(n_steps)]  # Cross product (r x v)

    if np.abs(np.std(orbital_energy)) and np.abs(np.std(angular_momentum)) <= 1:
        results = "Orbital Energy and Angular Momentum Conserved"
    elif np.abs(np.std(orbital_energy)) <= 1 < np.abs(np.std(angular_momentum)):
        results = "Orbital Energy NOT Conserved, Angular Momentum Conserved"
    elif np.abs(np.std(angular_momentum))<= 1 < np.abs(np.std(orbital_energy)):
        results = "Angular Momentum NOT Conserved, Orbital Energy Conserved"
    else:
        results = "Orbital Energy and Angular Momentum NOT Conserved"

    cv_orbital_energy = "Orbital Energy Coefficient of Variation " + str(np.round(np.abs(np.std(orbital_energy) / np.mean(orbital_energy)),3) * 100) + "%"
    cv_angular_momentum = "Angular Momentum Coefficient of Variation " + str(np.round(np.abs(np.std(angular_momentum) / np.mean(angular_momentum)), 3) * 100) + "%"

    return print(results, "\n" + cv_orbital_energy, "\n" + cv_angular_momentum), gravitational_potential, angular_momentum