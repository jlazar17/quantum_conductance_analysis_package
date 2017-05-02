#! /usr/bin/python

import numpy as np
import pylab
from scipy.optimize import leastsq
from scipy.interpolate import UnivariateSpline

################################################################################
######################### DEFINING FUNCTIONS ###################################

def lorentzian(x,p):
	numerator = (p[0]**2)
	denominator = ( x -(p[1]) )**2 + p[0]**2
	y = p[2]*(numerator/denominator)
	return y

def residuals(p,y,x):
	err = y - lorentzian(x,p)
	return err

################################################################################
######################## BACKGROUND SUBTRACTION ################################

# defining the background part of the spectrum
def make_background_arrays(x,y,lb,ub):
	ind_bg_low = (x > min(x)) & (x < lb)
	ind_bg_high = (x > ub) & (x < max(x))
	x_bg = np.concatenate((x[ind_bg_low],x[ind_bg_high]))
	y_bg = np.concatenate((y[ind_bg_low],y[ind_bg_high]))
	return x_bg,y_bg

# fits background to a line then returns input y-array with this background
# subtracted out. lb and ub are the lower bound and upper bound of the actual
# signal
def remove_background(x,y,lb,ub):
	# fitting the background to a line
	x_bg,y_bg=make_background_arrays(x,y,lb,ub)
	m, c = np.polyfit(x_bg, y_bg, 1)
	# removing background
	background = m*x + c
	y_wo_background = y-background
	return y_wo_background,background

################################################################################
########################### FITING DATA ########################################

# p is a tuple with initial guess at parameters of the Lorentzian, the values
# being gamma, peak center, and peak intensity. x is the input x array, and
# y_wo_bg and bg are the y array with background subtracted out and the
# background as output by the remove_background function
def fit(p0, x, y_wo_bg, bg):
	# optimization
	pbest = leastsq(residuals,p0,args=(y_wo_bg,x),full_output=1)
	best_parameters=pbest[0]
	# fit the data
	fit=lorentzian(x,best_parameters)
	FWHM = find_FWHM(fit,x)
	fit_w_bg = fit + bg
	return fit_w_bg,best_parameters,FWHM

def find_FWHM(lz,x):
	spline = UnivariateSpline(x, lz-np.max(lz)/2, s=0)
	r1, r2 = spline.roots()
	FWHM = abs(r1 - r2)
	return FWHM

def main(p,x,y,lb,ub):
	y_wo_bg, bg = remove_background(x,y,lb,ub)
	fitted_data, parameters, FWHM = fit(p,x,y_wo_bg,bg)
	return fitted_data, parameters, FWHM

if __name__ == '__main__':
    main(args['f'],args['d'])
