import numpy as np

'''
Inputs
------
* mu: The mean of the gaussian fit
* sigma: The covariance of the gaussian fit

Outputs
-------
* mu: The center of the ellipse
* a: The semi-major axis length
* b: The semi-minor axis length
* theta: The ellipse orientation
'''
def cov2ell(mu, sigma):
	xy = mu

	vals, vecs = np.linalg.eigh(sigma)

	x, y = vecs[:, 0]
	angle = np.degrees(np.arctan2(y, x))

	width, height = 2 * np.sqrt(vals)

	return xy, width, height, angle  
