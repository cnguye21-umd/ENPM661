import matplotlib.pyplot as plt
import numpy as np

# Simulated ball trajectory data with small x deviations
np.random.seed(42)
x = np.linspace(0, 1, 20) + np.random.normal(0, 0.02, 20)  # small x deviation
y = -4.9 * (x*2)**2 + 5*(x*2) + np.random.normal(0, 0.1, 20)  # simplified parabolic trajectory

# Ordinary Least Squares (OLS) fit (y vs x)
A_ols = np.vstack([x, np.ones_like(x)]).T
m_ols, c_ols = np.linalg.lstsq(A_ols, y, rcond=None)[0]
y_ols = m_ols*x + c_ols

# Total Least Squares (TLS) fit using SVD
points = np.vstack((x, y)).T
points_mean = points.mean(axis=0)
U, S, Vt = np.linalg.svd(points - points_mean)
direction = Vt[0]  # first singular vector
# TLS line points
t = np.linspace(-0.1, 1.1, 100)
x_tls = points_mean[0] + direction[0]*t
y_tls = points_mean[1] + direction[1]*t

# Plotting
plt.figure(figsize=(8,6))
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x, y_ols, color='red', label='OLS fit (vertical error minimized)')
plt.plot(x_tls, y_tls, color='green', linestyle='--', label='TLS fit (perpendicular error minimized)')
plt.xlabel('x (horizontal displacement)')
plt.ylabel('y (height)')
plt.title('Comparison: OLS vs TLS for Ball Trajectory')
plt.legend()
plt.grid(True)
plt.show()