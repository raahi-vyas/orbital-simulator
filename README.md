# Satellite Orbit Simulator

A Python-based orbital mechanics simulator implementing RK4 numerical integration, 
J2 perturbation modeling, and ground track visualization. Validated against real-world 
ISS, GEO, and Molniya orbital parameters.

## Features
- Perifocal to ECI frame transformation from Keplerian elements
- RK4 numerical propagator with J2 perturbation modeling
- Orbital energy (with J2 potential correction) and angular momentum conservation: 0.0% coefficient of variation (CV) across all test cases
- RAAN and AOP secular drift computation via linear regression (np.polyfit)
- 3D orbital trajectory visualization and 2D ground track mapping
- Telemetry pipeline (altitude, velocity, time) exported to CSV
- Latitude/longitude conversion for all propagated states

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Configure orbital parameters in `src/constants.py`
4. Run: `python main.py`

## Orbital Period Validation
| Orbit     | Expected Period | Simulated Period | Error             | Energy CV | Momentum CV |
|-----------|----------------|------------------|-------------------|-----------|-------------|
| LEO (ISS) | 92.68 min      | 92.561 min       | 0.119 min (0.13%) | 0.0%      | 0.0%        |
| GEO       | 1436.07 min    | 1436.112 min     | 0.042 min (0.00%) | 0.0%      | 0.0%        |
| Molniya   | 717.80 min     | 717.989 min      | 0.189 min (0.03%) | 0.0%      | 0.0%        |

## J2 Perturbation Validation
Validated against the Soviet Molniya orbit (a = 26,560 km, e = 0.74, i = 63.4°).
At the critical inclination of 63.4°, J2 theory predicts AOP drift freezes to 0.000°/day —
confirming the physical property exploited in real Molniya satellite design.

| Parameter | Expected (°/day) | Simulated (°/day) | Error   |
|-----------|-----------------|-------------------|---------|
| RAAN Drift | -0.1470        | -0.1478           | 0.0008° |
| AOP Drift  |  0.0000        |  0.0002           | 0.0002° |

All drift rates validated within < 0.3% error across multiple test cases.

## Project Structure
```plaintext
satellite-orbit-simulator/
├── src/
│   ├── constants.py
│   ├── perifocal_to_eci.py
│   ├── rk4.py
│   ├── navigation.py
│   └── plotting.py
├── tests/
│   ├── conservation.py
│   └── j2.py
├── data/
│   └── telemetry.csv
├── main.py
└── requirements.txt
```

## Skills Demonstrated
- **Astrodynamics:** Two-body problem, Keplerian elements, perifocal to ECI 
  transformation, J2 perturbation modeling, RAAN/AOP secular drift validation, 
  critical inclination verification, LEO/GEO/Molniya orbit support
- **Numerical Methods:** RK4 integration, J2 potential energy correction, 
  step size sensitivity analysis
- **Data Analytics:** Linear regression for secular drift rates, telemetry 
  pipeline, CSV export, coefficient of variation validation
- **Visualization:** 3D orbital plots, 2D ground track mapping (Cartopy), 
  RAAN/AOP drift plots with linear regression overlay
- **Software Engineering:** Modular architecture, requirements management
- **Python:** NumPy, Matplotlib, Cartopy, Pandas
