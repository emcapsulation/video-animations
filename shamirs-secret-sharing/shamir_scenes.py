from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#120410"


class Shamir(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in Shamir and speech bubble
		shamir = Human(LIGHT_PINK, 0.8).add_label("Shamir", WHITE).get_human().scale(0.4).move_to(LEFT*5+UP*2.5)
		self.play(Create(shamir))

		speech_bubble = SpeechBubble([PINK, LIGHT_PINK], 9, 1.5).get_speech_bubble().move_to(RIGHT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("This is Shamir's Secret Sharing.", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))
		self.wait(2)


		# Descriptions
		text_1 = Text("Splits any secret into n parts called shares.", font_size=20).move_to(UP)
		self.play(Write(text_1))
		self.wait(2)

		text_2 = Text("You select a threshold, k.", font_size=20).move_to(UP*0.5)
		self.play(Write(text_2))
		self.wait(2)


		# k shares description
		top_rect = SpeechBubble(GREEN, 10, 1.5).get_speech_bubble().move_to(DOWN)
		top_text = Text("≥ k shares reconstructs the secret.", font_size=20).move_to(top_rect.get_center())
		top = VGroup(top_rect, top_text)
		self.play(Create(top_rect), Write(top_text))
		self.wait(2)

		bot_rect = SpeechBubble(RED, 10, 1.5).get_speech_bubble().move_to(DOWN*3)
		bot_text = Text("< k shares are completely useless.", font_size=20).move_to(bot_rect.get_center())
		bot = VGroup(bot_rect, bot_text)
		self.play(Create(bot_rect), Write(bot_text))
		self.wait(2)


		# Slide both rectangles to the side
		self.play(
			top_rect.animate.set_width(7),
			bot_rect.animate.set_width(7)
		)
		self.play(
			top.animate.shift(LEFT*3),
			bot.animate.shift(LEFT*3)
		)
		self.wait(2)

		
		positions = [RIGHT*2+DOWN, RIGHT*4+DOWN, RIGHT*6+DOWN, RIGHT*2+DOWN*2, RIGHT*4+DOWN*2, RIGHT*6+DOWN*2]
		family = Family(0.8, 0.2, 1, positions)
		family_group = family.get_family_group()
		self.play(Create(family_group))

		n_is_6 = Text("n = 6", font_size=28).move_to(RIGHT*3 + DOWN*3)
		self.play(Write(n_is_6))
		self.wait(2)


		self.play(
			family.get_family_group_member("Uncle").animate.set_color(GRAY),
			family.get_family_group_member("Mum").animate.set_color(GRAY)
		)
		self.play(
			family.get_family_group_member("Uncle").animate.set_color(GOLD),
			family.get_family_group_member("Mum").animate.set_color(TEAL)
		)
		self.play(
			family.get_family_group_member("Grandpa").animate.set_color(GRAY),
			family.get_family_group_member("You").animate.set_color(GRAY)
		)
		self.play(
			family.get_family_group_member("Grandpa").animate.set_color(ORANGE),
			family.get_family_group_member("You").animate.set_color(PURPLE)
		)
		self.play(
			family.get_family_group_member("Dad").animate.set_color(GRAY),
			family.get_family_group_member("Mum").animate.set_color(GRAY)
		)


		k_is_4 = Text("k = 4", font_size=28).move_to(RIGHT*5 + DOWN*3)
		self.play(Write(k_is_4))
		self.wait(2)



# This scene took forever lol
class LagrangeInterpolation(Scene):
	
	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Lagrange Interpolation Formula").move_to(UP*3)
		self.play(Write(title))


		points = [(1, 4), (2, 0), (4, 1), (6, 5)]
		colours = [ORANGE, GOLD, TEAL, PURPLE]

		subtitle = VGroup()
		subtitle_1 = Text("Find the polynomial that interpolates ", font_size=20)
		subtitle.add(subtitle_1)

		for i in range(0, len(points)):
			if i == len(points)-1:
				subtitle_2 = Text(f"{points[i]}", font_size=20, color=colours[i])
			else:
				subtitle_2 = Text(f"{points[i]}, ", font_size=20, color=colours[i])
			subtitle.add(subtitle_2)

		subtitle.arrange(RIGHT).move_to(UP*2)
		self.play(Write(subtitle))
		self.wait(2)


		# Show plugging in all the points
		polynomial = MathTex("P(x)", " = ", "a", "x^{3}", " + ", "b", "x^{2}", " + ", "cx", " + ", "d").move_to(UP)
		self.play(Write(polynomial))
		self.wait(2)

		prev_polynomial = polynomial
		i = 0

		for point in points:
			new_polynomial = MathTex(f"P({point[0]})", " = ", "a \\cdot", f"{point[0]}^{3}", " + ", "b \\cdot", f"{point[0]}^{2}", " + ", "c \\cdot", f"{point[0]}", " + ", "d", " = ", f"{point[1]}").move_to(UP)
			new_polynomial.set_color_by_tex(str(point[1]), colours[i])			
			self.play(TransformMatchingTex(prev_polynomial, new_polynomial))
			self.wait(2)

			i += 1
			prev_polynomial = new_polynomial

		self.play(FadeOut(prev_polynomial))


		# Show boxes
		polynomial_boxes = VGroup()

		px = MathTex("P(x) = ")
		polynomial_boxes.add(px)

		colours = [ORANGE, GOLD, TEAL, PURPLE]
		for i in range(len(colours)):
			rect = Rectangle(
				width=2.4, height=2,
				fill_color=colours[i],
				fill_opacity=1,
				stroke_width=0
			)
			polynomial_boxes.add(rect)

			if i != len(colours)-1:
				polynomial_boxes.add(MathTex("+"))

		polynomial_boxes.arrange(RIGHT)
		self.play(Create(polynomial_boxes))
		self.wait(2)


		# Examples - plug in an x value and light up the corresponding box
		def light_up_box(num):
			reset_animation = []
			box_values = VGroup()

			p_num = MathTex(f"P({points[num][0]}) = ").move_to(polynomial_boxes[0].get_center())
			self.play(Transform(polynomial_boxes[0], p_num))
			self.wait(2)

			reset_animation.append(Transform(polynomial_boxes[0], MathTex(f"P(x) = ").move_to(polynomial_boxes[0].get_center())))			

			for i in range(0, 4):				
				box_num = 2*i + 1

				if i == num:					
					self.play(Indicate(polynomial_boxes[box_num]))					
					value = Text(f" = {points[num][1]}", font_size=24, color=colours[i]).next_to(polynomial_boxes[box_num], DOWN)
					self.play(Write(value))

					box_values.add(value)
					self.wait(2)

				else:
					self.play(polynomial_boxes[box_num].animate.set_color(GRAY))
					value = Text(" = 0", font_size=24, color=GRAY).next_to(polynomial_boxes[box_num], DOWN)
					self.play(Write(value))

					box_values.add(value)

				reset_animation.append(polynomial_boxes[box_num].animate.set_color(colours[i]))

			reset_animation.append(FadeOut(box_values))
			self.play(*reset_animation)

		light_up_box(0)
		light_up_box(2)


		# Make the boxes see through
		for i in range(0, 4):
			box_num = 2*i + 1
			self.play(polynomial_boxes[box_num].animate.set_fill(opacity=0).set_stroke(width=1, color=colours[i]))
		self.wait(2)		


		# Start with the deactivating terms
		polynomial_terms = VGroup()

		def create_deactivate_terms(end, ignore_boxes=[]):
			if ignore_boxes == []:
				self.play(Circumscribe(subtitle[end], color=colours[end-1]))
				self.play(Flash(polynomial_boxes[2*(end-1) + 1], color=colours[end-1]))
				self.wait(2)

			for i in range(0, len(points)):
				if i in ignore_boxes:
					continue

				box_num = 2*i + 1

				text = ""			
				for j in range(0, end):
					if j != i:
						text += f"(x-{points[j][0]})"
				
				font_size = 36-4*end
				this_term = MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())
				
				if len(polynomial_terms) <= i:
					polynomial_terms.add(this_term)
					self.play(Write(this_term))
				else:					
					self.play(Transform(polynomial_terms[i], this_term))

			self.wait(2)


		# Use 1 as an example
		create_deactivate_terms(1)


		# Sub in the x values to show the deactivated ones disappearing
		def sub_in_x(x, activate, end, reset=True, ignore_boxes=[]):
			reset_animation = []

			p1 = MathTex(f"P({x}) = ").move_to(polynomial_boxes[0].get_center())
			self.play(Transform(polynomial_boxes[0], p1))
			reset_animation.append(Transform(polynomial_boxes[0], MathTex("P(x) = ").move_to(polynomial_boxes[0].get_center())))
			self.wait(2)

			font_size = 36-4*end
			for i in range(0, len(polynomial_terms)):
				if i in ignore_boxes:
					continue

				box_num = 2*i + 1

				text = ""
				for j in range(0, end):
					if j != i:
						text += f"({x}-{points[j][0]})"

				switch_off = MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())
				self.play(Transform(polynomial_terms[i], switch_off))

			# Replace with the answer
			for i in range(0, len(polynomial_terms)):
				if i in ignore_boxes:
					continue

				box_num = 2*i + 1

				text = ""
				ans, count = 1, 1
				for j in range(0, end):
					if j != i:
						text += f"({x-points[j][0]})"
						if count < end-1:
							text += "\\cdot"
						ans *= (x-points[j][0])
						count += 1

				mult_text = MathTex(text, font_size=32).move_to(polynomial_boxes[box_num].get_center())
				self.play(Transform(polynomial_terms[i], mult_text))
				self.wait(1)

				if ans != 1:
					ans_text = MathTex(str(ans), font_size=32).move_to(polynomial_boxes[box_num].get_center())
					self.play(Transform(polynomial_terms[i], ans_text))
					if ans == 0:
						self.play(polynomial_terms[i].animate.set_color(GRAY))

				text = ""			
				for j in range(0, end):
					if j != i:
						text += f"(x-{points[j][0]})"

				reset_animation.append(Transform(polynomial_terms[i], 
					MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())))

			self.wait(2)
			if reset:						
				self.play(*reset_animation)
				self.wait(2)

		sub_in_x(1, 0, 1)

		for end in range(2, len(points)+1):
			create_deactivate_terms(end)

		sub_in_x(6, 3, 4, reset=False)


		# Turn the final one back to demo normalisation
		i, end = 3, 4
		box_num = 2*i + 1

		text = ""			
		for j in range(0, end):
			if j != i:
				text += f"(x-{points[j][0]})"
		
		font_size = 36-4*end
		this_term = MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())
		self.play(Transform(polynomial_terms[i], this_term))
		self.wait(2)


		# Divide :D
		def divide_term(i, plug_in=False, animate=True):
			box_num = 2*i + 1

			text = "\\frac{"
			for j in range(0, end):
				if j != i:
					if plug_in == False:
						text += f"(x-{points[j][0]})"
					else:
						text += f"({plug_in}-{points[j][0]})"
			text += "}{"
			for j in range(0, end):
				if j != i:
					text += f"({points[i][0]}-{points[j][0]})"
			text += "}"
		
			if animate:
				this_term = MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())
				self.play(Transform(polynomial_terms[i], this_term))
				self.wait(2)

			return text


		divide_term(3)


		# Plug in 6 and convert to 1
		divide_term(3, plug_in=points[3][0])


		text = "1"
		this_term = MathTex(text, font_size=32).move_to(polynomial_boxes[box_num].get_center())
		self.play(Transform(polynomial_terms[i], this_term))
		self.wait(2)


		# Multiply by desired y value
		def create_full_term(i, plug_in=False, animate=True):
			box_num = 2*i + 1
			text = divide_term(i, plug_in, animate)

			text += f"\\cdot {points[i][1]}"
			this_term = MathTex(text, font_size=font_size).move_to(polynomial_boxes[box_num].get_center())
			self.play(Transform(polynomial_terms[i], this_term))
			self.wait(2)

		create_full_term(3)


		# Show the big picture
		px = MathTex("P(x) = ").move_to(polynomial_boxes[0].get_center())
		self.play(Transform(polynomial_boxes[0], px))

		create_deactivate_terms(4, ignore_boxes=[3])
		sub_in_x(6, 3, 4, reset=False, ignore_boxes=[3])
		

		def plug_into_full_term(i, point_i):
			create_full_term(i, plug_in=points[point_i][0], animate=False)

			if i == point_i:
				text = f"1 \\cdot {points[i][1]}"
			else:
				text = f"0 \\cdot {points[i][1]}"

			this_term = MathTex(text, font_size=32).move_to(polynomial_boxes[box_num].get_center())
			self.play(Transform(polynomial_terms[point_i], this_term))
			self.wait(2)

			if i == point_i:
				text = f"{points[i][1]}"
			else:
				text = f"0"

			this_term = MathTex(text, font_size=32).move_to(polynomial_boxes[box_num].get_center())
			self.play(Transform(polynomial_terms[point_i], this_term))
			self.wait(2)

		plug_into_full_term(3, 3)


		# Apply the division and multiplication to each other share
		px = MathTex("P(x) = ").move_to(polynomial_boxes[0].get_center())
		self.play(Transform(polynomial_boxes[0], px))

		create_deactivate_terms(4, ignore_boxes=[3])
		create_full_term(3, animate=False)

		for i in range(0, 3):
			create_full_term(i, animate=True)

		self.wait(2)