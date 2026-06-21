import math

from manim import *

def move_to_seat(scene, family_list, table_radius, table_centre, animate=True):
	move_to_seat_animations = []
	i = 0
	while i < len(family_list):
		up = table_radius*math.sin(i*2*PI/len(family_list))
		right = table_radius*math.cos(i*2*PI/len(family_list))
		seat_position = UP*up + RIGHT*right

		if animate:
			move_to_seat_animations.append(family_list[i].get_human().animate.move_to(seat_position+table_centre))
		else:
			family_list[i].get_human().move_to(seat_position+table_centre)
			scene.add(family_list[i].get_human())
		i += 1

	if animate:
		scene.play(*move_to_seat_animations)