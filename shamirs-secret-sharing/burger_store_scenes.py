from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#000000"


class Introduction(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Store contains (wall, poster, counter)
		burger_store = BurgerStore()
		self.add(burger_store.get_burger_store())


		# Draw in each member of the family
		y_pos = DOWN*0.37
		positions = [RIGHT*5+y_pos, *[LEFT*x+y_pos for x in range(5, -5, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family.set_labels(["You", "Grandpa", "Uncle", "Dad", "Mum", "Brother"])
		family.set_colours([PURPLE, ORANGE, GOLD, GREEN, TEAL, BLUE])

		family_list = family.get_family_list()
		for family_member in family_list:
			self.play(Create(family_member.get_body()), Write(family_member.get_label()))
		self.wait(2)


		# Draw in the secret sauce
		secret_sauce = SecretSauce("shapes")
		self.play(Create(secret_sauce.get_background()))
		self.play(Create(secret_sauce.get_paper()))
		self.play(Write(secret_sauce.get_title()), Create(secret_sauce.get_lines()))
		self.wait(2)


		# The competitors rotate around the sauce
		competitor_scale = 0.6
		competitor_1 = Human(MAROON_D, 1).get_human().move_to(LEFT*3).scale(competitor_scale)
		competitor_2 = Human(RED_D, 1).get_human().move_to(RIGHT*3).scale(competitor_scale)
		self.play(Create(competitor_1), Create(competitor_2))

		arc_1 = Arc(radius=3, start_angle=PI, angle=PI)
		arc_2 = Arc(radius=3, start_angle=0, angle=PI)
		
		self.play(
			MoveAlongPath(competitor_1, arc_1), 
			MoveAlongPath(competitor_2, arc_2),
			run_time=10,
			rate_func=linear
		)


		# Competitor steals the sauce
		self.play(
			competitor_1.animate.shift(RIGHT*10), 
			secret_sauce.get_secret_sauce().animate.shift(RIGHT*10)
		)
		self.play(
			FadeOut(secret_sauce.get_background()),
			competitor_2.animate.shift(LEFT*8)
		)
		self.wait(2)		


		# Burger store exits the scene
		self.play(FadeOut(burger_store.get_counter()))
		self.play(
			burger_store.get_poster().animate.shift(UP*8), 
			FadeOut(burger_store.get_wall())
		)
		self.wait(2)


		# Move each family member to sit around the table
		table_radius = 2.5
		table_centre = DOWN*0.5

		move_to_seat_animations = []
		i = 0
		while i < len(family_list):
			up = table_radius*math.sin(i*2*PI/len(family_list))
			right = table_radius*math.cos(i*2*PI/len(family_list))
			seat_position = UP*up + RIGHT*right

			move_to_seat_animations.append(family_list[i].get_human().animate.move_to(seat_position+table_centre))
			i += 1

		self.play(*move_to_seat_animations)


		# They rotate around the table while the question comes up
		text = Text("How can we protect the recipe from falling into the wrong hands?", font_size=20).shift(UP*3)

		move_around_table_animations = [Write(text)]
		i = 0
		while i < len(family_list):
			arc = Arc(radius=table_radius, start_angle=i*2*PI/len(family_list), angle=PI/2).shift(table_centre)
			move_around_table_animations.append(MoveAlongPath(family_list[i].get_human(), arc))
			i += 1

		self.play(
			*move_around_table_animations, 
			run_time=5,
			rate_func=linear
		)

		self.wait(2)



class KeySplitCounterArgument(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Store contains (wall, poster, counter)
		burger_store = BurgerStore()
		self.add(burger_store.get_burger_store())


		# Draw in each member of the family
		y_pos = DOWN*0.37
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family_list = family.get_family_list()

		# Give a key piece to each person
		key_text = Text("super_secret_key_1").scale(0.5)
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(key_text.get_text()), 3):
			key_text[i:i+3].set_color(colours[i//3])
			key_text[i:i+3].move_to(family_list[i//3].get_human().get_center()+DOWN*1.1)


		# Animate each family member
		mum_index = 3
		mum = family_list[mum_index]
		self.play(Create(mum.get_body()), Write(mum.get_label()), Write(key_text[mum_index*3:mum_index*3+3]))
		self.wait(2)


		for i in range(0, len(family_list)):
			if i != mum_index:
				self.play(
					Create(family_list[i].get_body()), 
					Write(family_list[i].get_label()), 
					Write(key_text[i*3:(i*3)+3]), run_time=0.5)


		# Combine the key parts
		combine_parts_anim = []
		for i in range(0, len(key_text.get_text()), 3):
			combine_parts_anim.append(key_text[i:i+3].animate.move_to(UP + LEFT*1.2 + RIGHT*i/5))
		self.play(*combine_parts_anim)

		key = Key(YELLOW).get_key().move_to(UP).scale(0.3)
		self.play(Transform(key_text, key))
		self.wait(2)



class KeySplitCounterArgument2(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Store contains (wall, poster, counter)
		burger_store = BurgerStore()
		self.add(burger_store.get_burger_store())


		# Draw in each member of the family
		y_pos = DOWN*0.37
		positions = [*[LEFT*x+y_pos for x in range(5, -7, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family_group = family.get_family_group()


		# Draw in key
		key_text = Text("super_secret_key_1").scale(0.5)
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		for i in range(0, len(key_text.get_text()), 3):
			key_text[i:i+3].set_color(colours[i//3])
			key_text[i:i+3].move_to(family_group[i//3].get_center()+DOWN*1.1)

		self.add(family_group, key_text)
		self.wait(2)


		# Key spins out, key moves down, and one key disappears
		start_pos, end_pos = key_text[0:0+3].get_center(), LEFT*5 + UP*5
		def key_spin(mob, alpha):
			new_pos = interpolate(start_pos, end_pos, alpha)
			mob.move_to(new_pos)
			mob.rotate(2*PI*alpha)
		
		self.play(UpdateFromAlphaFunc(key_text[0:0+3], key_spin))

		dad_index = 2
		self.play(
			family_group[dad_index].animate.shift(DOWN*5), 
			key_text[dad_index*3:(dad_index*3)+3].animate.shift(DOWN*5)
		)

		brother_index = 4
		self.play(
			FadeOut(family_group[brother_index]), 
			FadeOut(key_text[brother_index*3:(brother_index*3)+3])
		)
		self.wait(2)


		self.play(FadeOut(burger_store.get_burger_store()))
