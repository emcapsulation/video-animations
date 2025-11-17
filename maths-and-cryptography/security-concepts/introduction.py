from manim import *
from entities import *


config.background_color = "#000000"


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


		self.play(FadeOut(secret_sauce.get_secret_sauce_with_background()))


		usb = Usb().usb.move_to(family_list[2].get_body().get_center() + UP*1.5)
		self.play(FadeIn(usb))
		self.play(Indicate(usb), color=RED)
		self.wait(2)


		smol_key = Key(GOLD).key.move_to(family_list[5].get_body().get_center() + UP*1.5).scale(0.2)
		self.play(
			SpinInFromNothing(smol_key),
			Wiggle(family_list[5].get_body())
		)
		self.wait(2)

		self.play(Wiggle(family_list[2].get_body()))
		self.play(
			FadeOut(smol_key), 
			FadeOut(usb)
		)
		self.wait(1)


		exclamation = Text("!", color=ORANGE, font_size=40).move_to(family_list[1].get_body().get_center() + UP*1.5)
		self.play(FadeIn(exclamation))
		for i in range(0, 3):
			self.play(Indicate(exclamation))
		self.play(FadeOut(exclamation))


		# Burger store exits the scene
		self.play(FadeOut(burger_store.get_counter()))
		self.play(
			burger_store.get_poster().animate.shift(UP*8), 
			FadeOut(burger_store.get_wall())
		)
		self.wait(2)


		table_radius = 2.5
		table_centre = DOWN*0.5
		move_to_seat(self, family_list, table_radius, table_centre)


		# They rotate around the table while the question comes up
		text = Text("The CIA Triad: Confidentiality, Integrity, Availability", 
			font_size=20,
			t2c={"Confidentiality": TEAL, "Integrity": PURPLE, "Availability": PINK}
		).shift(UP*3)

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



class Conclusion(Scene):

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


		self.play(Wiggle(family_list[2].get_body()))
		self.play(Wiggle(family_list[4].get_body()))


		usb = Usb().usb.move_to(family_list[2].get_body().get_center() + UP*1.5)
		self.play(FadeIn(usb))
		self.play(Indicate(usb), color=GREEN)
		self.wait(2)

