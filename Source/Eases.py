from math import cos, sin, pi, sqrt
from numba import njit


@njit
def linear(t: float):
	return t

# In

@njit
def power1_in(t: float):
	return t * t

@njit
def power2_in(t: float):
	return t ** 3

@njit
def power3_in(t: float):
	return t ** 4

@njit
def power4_in(t: float):
	return t ** 5

@njit
def sine_in(t: float):
	return 1. - cos((t * pi) * 0.5)

@njit
def expo_in(t: float):
	return 2. ** (10. * t - 10.)

@njit
def circ_in(t: float):
	return 1. - sqrt(1. - t * t)

@njit
def back_in(t: float):
	return 2.70158 * (t ** 3) - 1.70158 * t * t

# Out

@njit
def power1_out(t: float):
	return 1. - (1. - t) ** 2

@njit
def power2_out(t: float):
	return 1. - (1. - t) ** 3

@njit
def power3_out(t: float):
	return 1. - (1. - t) ** 4

@njit
def power4_inOut(t: float):
	return 1. - (1. - t) ** 5

@njit
def sine_out(t: float):
	return sin((t * pi) * 0.5)

@njit
def expo_out(t: float):
	return 1. - 2. ** (-10. * t)

@njit
def circ_out(t: float):
	return sqrt(1. - (t - 1.) ** 2)

@njit
def back_out(t: float):
	return 1. + 2.70158 * (t - 1.) ** 3 + 1.70158 * (t - 1.) ** 2

# InOut

@njit
def power1_inout(t: float):
	return 2. * power1_in(t) if t < 0.5 else 1. - (-2. * t + 2.) ** 2 * 0.5

@njit
def power2_inout(t: float):
	return 4. * power2_in(t) if t < 0.5 else 1. - (-2. * t + 2.) ** 3 * 0.5

@njit
def power3_inout(t: float):
	return 8. * power3_in(t) if t < 0.5 else 1. - (-2. * t + 2.) ** 4 * 0.5

@njit
def power4_inout(t: float):
	return 16. * power4_in(t) if t < 0.5 else 1. - (-2. * t + 2.) ** 5 * 0.5

@njit
def sine_inout(t: float):
	return -(cos(t * pi) - 1.) * 0.5

@njit
def expo_inout(t: float):
	return 2.**(20. * t - 10.) * 0.5 if t < 0.5 else 2. - 2.**(-20. * t + 10.) * 0.5

@njit
def circ_inout(t: float):
	return (1. - sqrt(1. - (2. * t) ** 2)) * 0.5 if t < 0.5 else (sqrt(1. - (-2. * t + 2.) ** 2) + 1.) * 0.5

@njit
def back_inout(t: float):	
	return ((2. * t) ** 2 * (7.189819 * t - 2.5949095)) * 0.5 if t < 0.5 else ((2. * t - 2.) ** 2 * (3.5949095 * (t * 2. - 2.) + 2.5949095) + 2.) * 0.5

# Extra
def steps(s: int):
	@njit
	def aux(t: float):
		...
	return aux

@njit
def bounce_out(t: float):
	n1 = 7.5625
	d1 = 2.75

	if (t < 1 / d1):
		return n1 * t * t
	if (t < 2 / d1):
		t -= 1.5 / d1
		return n1 * t * t + 0.75
	if (t < 2.5 / d1):
		t -= 2.25 / d1
		return n1 * t * t + 0.9375
	t -= 2.625 / d1
	return n1 * t * t + 0.984375

@njit
def bounce_in(t: float):
	return 1. - bounce_out(t)

__all__ = [
	'linear',

	'power1_in',
	'power2_in',
	'power3_in',
	'power4_in',
	'sine_in',
	'expo_in',
	'circ_in',
	'back_in',

	'power1_out',
	'power2_out',
	'power3_out',
	'power4_inOut',
	'sine_out',
	'expo_out',
	'circ_out',
	'back_out',

	'power1_inout',
	'power2_inout',
	'power3_inout',
	'power4_inout',
	'sine_inout',
	'expo_inout',
	'circ_inout',
	'back_inout',

	'bounce_in',
	'bounce_out',
]
