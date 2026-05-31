import numpy as np
from src.constants import number_of_time_steps, propagated_states, time_step, time_at_step, mu, j2, R_p

def two_body_ode(t, state):
    r_states = state[:3]
    r_magnitude = np.linalg.norm(r_states)
    simplified_acceleration = (- mu * r_states) / (r_magnitude ** 3) # Newton's Law of Gravitation in Vector Form

    #J2 PERTURBATION
    j2_factor = (- (3 / 2) * (j2 * mu * (R_p ** 2))) / (r_magnitude ** 5) #R_p = EQUATORIAL planet radius (6371km for earth)
    z_sq_factor = (5 * (state[2] ** 2)) / (r_magnitude ** 2)
    a_j2_x = j2_factor * (1.0 - z_sq_factor) * state[0]
    a_j2_y = j2_factor * (1.0 - z_sq_factor) * state[1]
    a_j2_z = j2_factor * (3.0 - z_sq_factor) * state[2]
    j2_acceleration = np.array([a_j2_x, a_j2_y, a_j2_z])

    total_acceleration = simplified_acceleration + j2_acceleration
    rk4_array = np.array([state[3], state[4], state[5], total_acceleration[0], total_acceleration[1], total_acceleration[2]])
    return rk4_array

#RK4 FUNCTION
def rk4(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h/2, y + k1 * h/2)
    k3 = f(t + h/2, y + k2 * h/2)
    k4 = f(t + h, y + k3 * h)
    weighted_mean = (h/6) * (k1 + (2 * k2) + (2 * k3) + k4)
    next_velocity = y + weighted_mean
    return next_velocity

#RK4 LOOP
def rk4_loop(initial_states):
    times = [0]
    current_time = 0
    propagated_states[0] = initial_states # The initial cartesian positions and velocities
    for step in range(number_of_time_steps - 1):
        propagated_states[step + 1] = rk4(two_body_ode, time_at_step[step], propagated_states[step], time_step)
        current_time += time_step
        times += [current_time]
    return propagated_states, times
