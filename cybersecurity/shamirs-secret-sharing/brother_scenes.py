from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#090f1a"


class BrotherIdeaOne(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in brother and speech bubble
		brother = Human(BLUE, 0.8).add_label("Brother", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(brother))

		speech_bubble = SpeechBubble([TEAL, BLUE], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("We should encrypt the recipe.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))


		# Draw the plaintext secret sauce, key, and encryption scheme
		sauce_scale = 0.6
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(LEFT*4 + DOWN*0.5).scale(sauce_scale)
		self.play(Create(secret_sauce_plaintext))

		key = Key(YELLOW).get_key().scale(0.25).move_to(LEFT*4 + DOWN*3)
		self.play(Create(key))

		encryption_background = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		encryption_text = Text("Encryption Scheme", font_size=24).move_to(encryption_background.get_center())
		encryption_scheme = VGroup(encryption_background, encryption_text).shift(DOWN + RIGHT*0.5)
		self.play(Create(encryption_scheme))

		self.play(
			secret_sauce_plaintext.animate.move_to(encryption_scheme.get_left()),
			key.animate.move_to(encryption_scheme.get_left())
		)


		# Encrypted recipe comes out the other side
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(encryption_scheme.get_right()).scale(sauce_scale)

		self.play(
			FadeOut(secret_sauce_plaintext),
			FadeOut(key),
			secret_sauce_encrypted.animate.move_to(RIGHT*5 + DOWN)
		)
		self.wait(2)


		# Competitors try to steal it but can't
		self.play(
			FadeOut(encryption_scheme),
			secret_sauce_encrypted.animate.move_to(ORIGIN+DOWN).scale(1.5)
		)

		competitor_scale = 0.6
		competitor_1 = Human(MAROON_D, 0.8).get_human().move_to(RIGHT*4).scale(competitor_scale)
		competitor_2 = Human(RED_D, 0.8).get_human().move_to(LEFT*4 + DOWN*2).scale(competitor_scale)
		self.play(Create(competitor_1), Create(competitor_2))
		self.wait(2)

		q_mark_1 = Text("?", color=MAROON_D).move_to(competitor_1.get_center())
		q_mark_2 = Text("?", color=RED_D).move_to(competitor_2.get_center())

		self.play(Transform(competitor_1, q_mark_1), Transform(competitor_2, q_mark_2))
		self.wait(2)



class EachKeepACopyOfTheKey(Scene):

	def decrypt_encrypt_recipe(self, key, secret_sauce_encrypted):
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(ORIGIN).scale(0.6*1.5*0.6)
		encrypted_copy = secret_sauce_encrypted.copy()
		original_key_position = key.get_center()

		# Key taps the sauce and decrypts it
		self.play(key.animate.move_to(secret_sauce_encrypted.get_center()))
		self.play(
			key.animate.move_to(original_key_position),
			Transform(secret_sauce_encrypted, secret_sauce_plaintext)
		)
		self.wait(2)

		# Key taps the sauce and encrypts it
		self.play(key.animate.move_to(secret_sauce_plaintext.get_center()))
		self.play(
			key.animate.move_to(original_key_position),
			Transform(secret_sauce_encrypted, encrypted_copy)
		)
		self.wait(2)


	def construct(self):
		Text.set_default(font="Monospace")

		sauce_scale = 0.6*1.5*0.6
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(ORIGIN).scale(sauce_scale)
		self.add(secret_sauce_encrypted)


		# Draw in each member of the family
		positions = []
		radius, num_family_members = 3, 6
		for i in range(0, num_family_members):
			up = radius*math.sin(i*2*PI/num_family_members)
			right = radius*math.cos(i*2*PI/num_family_members)
			positions.append(UP*up + RIGHT*right)

		family = Family(0.8, 0.3, 1, positions)
		family_group = family.get_family_group()

		self.play(Create(family_group))
		self.wait(2)


		# Give each family member a key
		key_radius = radius - 0.85
		key_group = VGroup()
		for i in range(0, len(family_group)):
			up = key_radius*math.sin(i*2*PI/len(family_group))
			right = key_radius*math.cos(i*2*PI/len(family_group))
			position = UP*up + RIGHT*right

			key = Key(YELLOW).get_key().scale(0.15).move_to(position)

			self.play(Create(key))
			key_group.add(key)
		self.wait(2)


		# Decrypt and encrypt recipe
		self.decrypt_encrypt_recipe(key_group[1], secret_sauce_encrypted)
		self.decrypt_encrypt_recipe(key_group[3], secret_sauce_encrypted)


		# One key goes spinning off and other key gets stolen
		start_pos, end_pos = key_group[2].get_center(), LEFT*5 + UP*5
		def key_spin(mob, alpha):
			mob.restore()
			new_pos = interpolate(start_pos, end_pos, alpha)
			mob.move_to(new_pos)
			mob.rotate(2*PI*alpha)

		key_group[2].save_state()
		self.play(UpdateFromAlphaFunc(key_group[2], key_spin))

		self.play(key_group[5].animate.shift(DOWN + RIGHT*2))

		competitor = Human(MAROON_D, 0.8).get_human().move_to(RIGHT*8).scale(0.3)
		self.play(competitor.animate.move_to(key_group[5].get_center() + RIGHT))

		self.play(
			competitor.animate.shift(RIGHT*8),
			key_group[5].animate.shift(RIGHT*8)
		)

		self.wait(2)



class LossOfPrecision(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in brother and speech bubble
		brother = Human(BLUE, 0.8).add_label("Brother", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(brother))

		speech_bubble = SpeechBubble([TEAL, BLUE], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Let's randomly create a degree-3 polynomial!", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))


		# Draw in axes and polynomial
		plane = Plane(([-1, 3, 1], [-1, 4, 1]), xy_length=[12, 6])
		plane.get_axes_and_labels().scale(0.75).shift(DOWN*1.5)
		self.play(Create(plane.get_axes()), Write(plane.get_axis_labels()))
		self.wait(2)


		polynomial = Polynomial(plane.get_axes(), lambda x: 1/3 * x*x*x - 5/7 * x*x + 2/9 * x + 2/5)
		
		curve, curve_label = polynomial.draw_polynomial(
			[-1, 3], 
			"P(x) = \\frac{1}{3} x^{3} - \\frac{5}{7} x^{2} + \\frac{2}{9} x + \\frac{2}{5}", 
			UP*1 + RIGHT, WHITE, label_font_size=36
		)
		self.play(Write(curve_label))
		self.play(Create(curve))
		self.wait(2)


		# y-intercept
		yint_and_label = plane.add_point((0, 0.4), RED, plane.get_axes().coords_to_point(0, 0.4) + LEFT+UP*0.5, RED, label_text="(0, \\frac{2}{5})")
		self.play(Create(yint_and_label[0]), Write(yint_and_label[1]))
		self.wait(2)


		speech2 = Text("How can we ensure the computer is precise enough?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Transform(speech1, speech2))
		self.wait(2)

		self.play(FadeOut(brother), FadeOut(speech_bubble), FadeOut(speech1))		


		# Draw in points and fractions
		colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]
		fam_points = [(1/2, 943/2520), (3/4, 2053/6720), (1, 76/315), (7/5, 254/1125), (3/2, 211/840), (11/4, 51239/20160)]
		fam_labels = [
			"(\\frac{1}{2}, \\frac{943}{2520})",
			"(\\frac{3}{4}, \\frac{2053}{6720})",
			"(1, \\frac{76}{315})",
			"(\\frac{7}{5}, \\frac{254}{1125})",
			"(\\frac{3}{2}, \\frac{211}{840})",
			"(\\frac{11}{4}, \\frac{51239}{20160})",
		]		
		point_group, label_group = VGroup(), VGroup()

		i = 0
		for point in fam_points:
			point_and_label = plane.add_point(point, colours[i], UP*3 + LEFT*(2.5 - i)*2, colours[i], label_text=fam_labels[i])

			point_group.add(point_and_label[0])
			label_group.add(point_and_label[1])
			self.play(Create(point_and_label[0]), Write(point_and_label[1]))

			i += 1
		self.wait(2)


		# Transform to floating point equivalent
		i = 0
		for point in fam_points:
			label_2 = MathTex(f"{point}", font_size=24, color=colours[i]).move_to(UP*(2.5+i%2) + LEFT*(2.5 - i)*2)
			self.play(Transform(label_group[i], label_2))
			i += 1

		self.wait(2)


		# Draw the less accurate polynomial
		polynomial = Polynomial(plane.get_axes(), lambda x: Polynomial.lagrange_interpolation(x, fam_points))
		
		rounded_curve, rounded_curve_label = polynomial.draw_polynomial([-1, 3], "", ORIGIN, MAROON)
		self.play(Create(rounded_curve))
		self.wait(2)

		yint_and_label_2 = plane.add_point((0, Polynomial.lagrange_interpolation(0, fam_points)), 
			MAROON, plane.get_axes().coords_to_point(0, Polynomial.lagrange_interpolation(0, fam_points)) + LEFT*2, 
			MAROON, label_text=f"(0, {Polynomial.lagrange_interpolation(0, fam_points)})")
		self.play(Create(yint_and_label_2[0]), Write(yint_and_label_2[1]))
		self.wait(2)