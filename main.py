from src.constants import mu, sma, ecc, inc, raan, aop, true_anomaly, number_of_time_steps, propagated_states, time_step
from src.perifocal_to_eci import elements_to_state_vectors
from src.rk4 import rk4_loop
from src.plotting import dashboard
from src.navigation import lat_lon, telemetry
from tests.conservation import energy_conservation
from tests.j2 import cartesian_to_keplerian

initial_states = elements_to_state_vectors(sma, ecc, inc, raan, aop, true_anomaly)
times = rk4_loop(initial_states)[1]
longitude, latitude, radius_magnitudes, position_states = lat_lon(propagated_states)
keplerian_energy, angular_momentum = energy_conservation(propagated_states, number_of_time_steps, mu, radius_magnitudes, position_states)[1:]
telemetry(propagated_states, time_step, number_of_time_steps)
nodal_regression, perigee_rotation = cartesian_to_keplerian(propagated_states)
dashboard(propagated_states, longitude, latitude, times, nodal_regression, perigee_rotation)