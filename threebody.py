import numpy as np
from scipy.integrate import solve_ivp

def three_body_equations(t, y, m1, m2, m3, G):
    # y = [x1, y1, z1, x2, y2, z2, x3, y3, z3, vx1, vy1, vz1, vx2, vy2, vz2, vx3, vy3, vz3]
    r1 = y[0:3]
    r2 = y[3:6]
    r3 = y[6:9]
    v1 = y[9:12]
    v2 = y[12:15]
    v3 = y[15:18]
    
    # Calculate pairwise forces
    def accel(ri, rj, mj):
        diff = rj - ri
        dist3 = np.linalg.norm(diff)**3 + 1e-12  # avoid division by zero
        return G * mj * diff / dist3

    a1 = accel(r1, r2, m2) + accel(r1, r3, m3)
    a2 = accel(r2, r1, m1) + accel(r2, r3, m3)
    a3 = accel(r3, r1, m1) + accel(r3, r2, m2)
    
    dydt = np.zeros(18)
    dydt[0:3] = v1
    dydt[3:6] = v2
    dydt[6:9] = v3
    dydt[9:12] = a1
    dydt[12:15] = a2
    dydt[15:18] = a3
    return dydt


def simulate_three_body(masses, positions, velocities, G=6.67430e-11, t_span=(0, 1e6), t_eval=None):
    m1, m2, m3 = masses
    y0 = np.concatenate([positions[0], positions[1], positions[2], velocities[0], velocities[1], velocities[2]])
    if t_eval is None:
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
    sol = solve_ivp(three_body_equations, t_span, y0, args=(m1, m2, m3, G), t_eval=t_eval, rtol=1e-9, atol=1e-9)
    # Return positions as arrays: shape (3, len(t_eval), 3)
    body1 = sol.y[0:3].T
    body2 = sol.y[3:6].T
    body3 = sol.y[6:9].T
    return sol.t, [body1, body2, body3]
