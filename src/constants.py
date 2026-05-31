import numpy as np

#PLANET PROPERTIES (SET FOR EARTH)
G = 6.674 * (10**-11) # Gravitational Constant --> units = (Nm^2)/kg^2
m = 5.972 * (10**24) # Planet Mass (earth) --> units = kg
mu = (G * m) * (10 ** - 9) # Gravitational Parameter of Central Body (earth) --> units = (km^3)/s^2
R_p = 6778.0 #6378.137 # Planet Radius (earth equatorial) --> units = km
j2 = 1.08262 * (10 ** -3) # J2 perturbation (earth)

#KEPLERIAN ELEMENTS
sma = 26560.0 # Semi-Major Axis
ecc = 0.74 #0.0006189 # Eccentricity
inc = np.radians(63.4) # Inclination
raan = np.radians(270) # RAAN
aop = np.radians(0) # Argument of Periapsis/Perigee
true_anomaly = np.radians(0)# True Anomaly

#PERIOD CALCULATION (USING SEMI-MAJOR AXIS)
T = (2 * np.pi * np.sqrt((sma ** 3) / mu)) # Units = seconds
print("Period:", str(np.round(T, 3)), "seconds")
orbits = 1

#RK4 FUNCTION SPECIFICATIONS
total_time = T * orbits # Units = seconds
time_step = 10
number_of_time_steps = int(total_time / time_step)  # Number of steps that the RK4 runs
time_at_step = np.zeros((number_of_time_steps, 1)) # The time at each step
propagated_states = np.zeros((number_of_time_steps, 6)) # Array of all 3 positions and 3 velocities, updated at each time step
