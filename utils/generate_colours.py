from manim import *


rainbow = [MAROON, RED, ORANGE, GOLD, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK, LIGHT_PINK]


def generate_colours(array, in_order=False):
	if in_order:
		array = list(range(len(array)))

	min_elem, max_elem = min(array), max(array)
	val_range, gradient_steps = max_elem-min_elem, 100

	colours = [None]*len(array)
	for i in range(0, len(array)):
		this_colour = int((array[i]-min_elem)/val_range * (gradient_steps-1))
		colours[i] = color_gradient(rainbow, gradient_steps)[this_colour]
	
	return colours