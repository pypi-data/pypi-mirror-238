import numpy as np
from scipy.misc import derivative


def calc_intens_with_runge_kuttta(start_T, end_T, cov, mu, calc_theta, k_B, V0, E_a0, B, d_mu, dT, diff_order, edge_theta):
	"""
	Parameters:
		start_T: The initial value of the temperature, K.
		end_T: The finite value of the temperature, K.
		cov: The initial value of coverage.
		mu: The initial value of chemical potential of the environment, kB*K.
		k_B: The gas constant.
		V0: The pre-exponential factor, c^(-1).
		E_a0: The desorption activation energy, kB*K.
		B: The rate of heating, K/c.
		d_mu: The increment of mu.
		dT: The increment of T.
		diff_order: The order of the derivative.
		edge_theta: The accuracy of the calculation of the rate of desorption.
		calc_theta: The function for calculation the initial value of coverage.
	Returns:
		intensities: The array of rate of desorption (d_theta/d_t), where t is time.
	"""

	def rhs_calc(T_n, mu_n, theta_n):
		Kd0 = V0 * np.exp(-E_a0 / (k_B * T_n))
		try:
			Kd_theta = Kd0 * np.exp(mu_n / (k_B * T_n)) * (1.0 - theta_n) * (theta_n ** (-1.0))
		except OverflowError:
			Kd_theta = float('inf')

		d_theta_d_mu = derivative(lambda x: calc_theta(x, T_n), x0=mu_n, dx=d_mu, n=1, order=diff_order)
		d_theta_d_T = derivative(lambda x: calc_theta(mu_n, x), x0=T_n, dx=dT, n=1, order=diff_order)

		if abs(d_theta_d_mu) < 1E-10:
			return 0

		return (-(1 / B) * (Kd_theta * theta_n + B * d_theta_d_T)) / d_theta_d_mu

	intensities = []

	mu_n = mu
	theta_n = cov
	theta_n_1 = 0

	for T in np.arange(start_T, end_T, dT):
		k1 = rhs_calc(T, mu_n, theta_n)

		k2_shiftT = T + dT / 2.0
		k2_shiftMu = mu_n + dT * k1 / 2.0
		k2 = rhs_calc(k2_shiftT, k2_shiftMu, calc_theta(mu_n, T))

		k3_shiftT = T + dT / 2.0
		k3_shiftMu = mu_n + dT * k2 / 2.0
		k3 = rhs_calc(k3_shiftT, k3_shiftMu, calc_theta(k2_shiftMu, k2_shiftT))

		k4_shiftT = T + dT
		k4_shiftMu = mu_n + dT * k3
		k4 = rhs_calc(k4_shiftT, k4_shiftMu, calc_theta(k3_shiftMu, k3_shiftT))

		mu_n_1 = mu_n + (dT / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

		if theta_n_1 != 0:
			theta_n = theta_n_1
		theta_n_1 = calc_theta(mu_n_1, T + dT)

		if theta_n_1 < edge_theta:
			break

		intensity = (theta_n_1 - theta_n) / dT
		if intensity < 0:
			intensity = -intensity
		intensities.append(intensity)

		mu_n = mu_n_1
		T += dT

	return intensities
