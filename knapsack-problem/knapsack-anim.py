from manim import *

import math

config.background_color = "#15131c"


VALUE_COLOUR = GOLD
ITEM_WEIGHT_COLOUR = ORANGE
WEIGHT_LIMIT_COLOUR = PINK
MAX_VALUE_COLOUR = GOLD


def fade_out_scene(scene):
	scene.play(
		*[FadeOut(mob)for mob in scene.mobjects]
	)


def make_suitcase():
	return RoundedRectangle(
		width=3, height=4,
		corner_radius=0.2,
		color=GRAY,
		fill_opacity=0.5
	)


def make_camera():
	camera_body = RoundedRectangle(
		width=1.2, height=0.8,
		corner_radius=0.2,
		color=GRAY,
		fill_opacity=0.5
	)
	lens = Circle(
		radius=0.2,
		color=BLACK,
		fill_opacity=0.5
	).move_to(camera_body.get_center() + RIGHT*0.25)
	camera = VGroup(camera_body, lens)

	return camera


def make_pen():
	pen_body = Rectangle(
		width=1.5, height=0.25,
		color=BLUE,
		fill_opacity=0.5
	)
	nib = Triangle(
		color=WHITE,
		fill_opacity=0.5
	).scale(0.15)
	nib.rotate(5*PI/6, about_point=nib.get_center()).move_to(pen_body.get_right() + RIGHT*0.15)
	pen = VGroup(pen_body, nib)

	return pen


def make_sneakers():
	shoe = RoundedRectangle(
		width=0.5, height=0.8,
		corner_radius=0.2,
		color=WHITE,
		fill_opacity=0.5
	)
	sneakers = VGroup(shoe, shoe.copy()).arrange(RIGHT)

	return sneakers


def make_toothbrush():
	toothbrush_body = Rectangle(
		width=1.9, height=0.2,
		color=WHITE,
		fill_opacity=0.5
	)
	brushes = RoundedRectangle(
		width=0.4, height=0.25,
		corner_radius=0.1,
		color=RED,
		fill_opacity=0.5
	).move_to(toothbrush_body.get_top() + UP*0.125 + RIGHT*0.71)
	toothbrush = VGroup(toothbrush_body, brushes)

	return toothbrush


def make_headphones():
	headphone = RoundedRectangle(
		width=0.4, height=0.7,
		corner_radius=0.2,
		color=GRAY_D,
		fill_opacity=0.5
	)
	band = Arc(
		radius=0.7, angle=PI,
		color=GRAY_D
	)
	headphones = VGroup(headphone.shift(LEFT*0.4 + DOWN*0.15), band, headphone.copy().shift(RIGHT*0.8))

	return headphones


def get_value_colour(min_val, max_val, val):
	val_range, gradient_steps = max_val-min_val, 100

	return color_gradient(
		[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK], 
		gradient_steps
	)[int((val - min_val)/val_range * (gradient_steps-1))]



class Introduction(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Create the suitcase
		suitcase = make_suitcase().move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)

		self.play(Create(suitcase))
		self.play(Write(suitcase_text))
		self.wait(2)

		suitcase_weight = Text("W = 5kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.play(Write(suitcase_weight))
		self.wait(2)


		# Create the items
		items, item_texts, value_texts = VGroup(), VGroup(), VGroup()
		weights = [2, 1, 3, 1, 4]
		values = [25, 10, 40, 20, 45]


		camera = make_camera().move_to(LEFT+DOWN*0.5)
		pen = make_pen().move_to(UP*2)
		sneakers = make_sneakers().move_to(UP*2.25 + LEFT*5)
		toothbrush = make_toothbrush().move_to(LEFT*4, UP*1.5)
		headphones = make_headphones().move_to(LEFT*2.5 + UP*2)

		items.add(camera, pen, sneakers, toothbrush, headphones)
		items.shift(DOWN)


		for i in range(0, len(items)):
			item_text = Text(f"w = {weights[i]}kg", font_size=20, color=ITEM_WEIGHT_COLOUR).next_to(items[i], DOWN)
			item_texts.add(item_text)
			self.play(Create(items[i]), Write(item_texts[i]))
		self.wait(2)


		# Add a value to each item
		for i in range(len(items)):
			value_text = Text(f"v = {values[i]}", font_size=20, color=VALUE_COLOUR).next_to(item_texts[i], DOWN)
			value_texts.add(value_text)
			

		order = [2, 1, 0, 3, 4]
		for i in order:
			self.play(Write(value_texts[i]))
			if i == 2 or i == 1:
				self.wait(2)
		self.wait(2)


		# Write the question
		problem_1 = Text("Which items should you pack so that the final suitcase contains the\nmaximum value possible, without exceeding the weight limit of 5kg?", 
			font_size=20, t2c={"value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).move_to(UP*3)
		
		self.play(Write(problem_1))
		self.wait(5)

		fade_out_scene(self)




class BruteForce(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		n = 5

		# Create table of items
		item_numbers = VGroup(Text("#", font_size=24))
		for i in range(1, n+1):
			num = Text(f"{i}", font_size=24)
			item_numbers.add(num)
		item_numbers.arrange(RIGHT, buff=2).move_to(UP*3.5)


		s = 0.5
		items = VGroup(Text("i", color="#15131c", font_size=24),
			make_camera().scale(s), 
			make_pen().scale(s), 
			make_sneakers().scale(s), 
			make_toothbrush().scale(s), 
			make_headphones().scale(s)
		).arrange(RIGHT, buff=1.4).move_to(UP*3).shift(RIGHT*0.3)


		weights = [2, 1, 3, 1, 4]
		values = [25, 10, 40, 20, 45]

		weight_texts, value_texts = VGroup(Text("w", font_size=24)), VGroup(Text("v", font_size=24))
		for i in range(0, n):
			weight_texts.add(Text(f"{weights[i]}", font_size=24, color=ITEM_WEIGHT_COLOUR))
			value_texts.add(Text(f"{values[i]}", font_size=24, color=VALUE_COLOUR))
		weight_texts.arrange(RIGHT, buff=2).move_to(UP*2.5)
		value_texts.arrange(RIGHT, buff=1.8).move_to(UP*2)


		for i in range(0, n+1):
			self.play(
				Write(item_numbers[i]),
				Create(items[i]),
				Write(weight_texts[i]),
				Write(value_texts[i])
			)

		item_table = VGroup(item_numbers, items, weight_texts, value_texts)
		self.play(item_table.animate.scale(0.8).shift(RIGHT*2))

		capacity = Text("W = 5kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).move_to(item_table.get_left() + LEFT*3)
		self.play(Write(capacity))
		
		max_value_text = Text("max = 0", font_size=24, color=MAX_VALUE_COLOUR).move_to(capacity.get_center() + DOWN*0.5)
		max_value = 0
		self.play(Write(max_value_text))
		self.wait(2)


		# Highlight the items
		i = 1
		highlight = Rectangle(
			width=1, height=1.5,
			color=GREEN,
			stroke_width=0,
			fill_opacity=0.15
		).move_to(weight_texts[i].get_top() + UP*0.1 + LEFT*0.1)
		self.play(Create(highlight))
		self.wait(2)


		# First item
		take_item = Text(f"[{i}]", font_size=24).move_to(LEFT*3.2 + UP)
		take_weight = Text(f"current weight = {weights[i-1]}", color=ITEM_WEIGHT_COLOUR, font_size=16).next_to(take_item, DOWN)
		take_value = Text(f"current value = {values[i-1]}", color=VALUE_COLOUR, font_size=16).next_to(take_weight, DOWN)

		leave_item = Text(f"[]", font_size=24).move_to(RIGHT*3.2 + UP)
		leave_weight = Text(f"current weight = 0", color=ITEM_WEIGHT_COLOUR, font_size=16).next_to(leave_item, DOWN)
		leave_value = Text(f"current value = 0", color=VALUE_COLOUR, font_size=16).next_to(leave_weight, DOWN)

		current_row = [
			VGroup(take_item, take_weight, take_value),
			VGroup(leave_item, leave_weight, leave_value)
		]

		self.play(Write(take_item))
		self.play(Write(leave_item))
		self.wait(2)

		self.play(Write(take_weight))
		self.play(Write(take_value))

		max_value = values[i-1]
		self.play(Transform(max_value_text, Text(f"max = {max_value}", font_size=24, color=MAX_VALUE_COLOUR).move_to(capacity.get_center() + DOWN*0.5)))
		self.play(Indicate(max_value_text))
		self.wait(2)

		self.play(Write(leave_weight))
		self.play(Write(leave_value))
		self.wait(2)


		# Next items
		for i in range(2, 5):
			self.play(highlight.animate.move_to(weight_texts[i].get_top() + UP*0.1 + LEFT*0.1))
			self.wait(2)

			take_group, leave_group = VGroup(), VGroup()
			new_row = []

			# Highlight the subset
			highlight_2 = Rectangle(
				width=4, height=2,
				color=TEAL,
				stroke_width=0,
				fill_opacity=0.15
			).scale(0.7**(i-1)).move_to(current_row[0].get_center())
			self.play(FadeIn(highlight_2))


			for item in current_row:			
				self.play(highlight_2.animate.move_to(item.get_center()))

				# Create subset
				take_item_text = item[0].text[0:len(item[0].text)-1] + f",{i}]"
				if len(item[0].text) == 2:
					take_item_text = f"[{i}]"

				take_item = Text(
					f"{take_item_text}", 
					font_size=24).move_to(LEFT*3 + UP)

				cur_weight = item[1].text[len(item[1])-1]
				take_weight = Text(f"current weight = {int(cur_weight) + weights[i-1]}", color=ITEM_WEIGHT_COLOUR, font_size=16).next_to(take_item, DOWN)

				cur_value = item[2].text[len(item[2])-2:len(item[2])]
				if not cur_value.isnumeric():
					cur_value = item[2].text[len(item[2])-1]
				take_value = Text(f"current value = {int(cur_value) + values[i-1]}", color=VALUE_COLOUR, font_size=16).next_to(take_weight, DOWN)


				mult = (3.2/i)
				if i == 3:
					mult = (2.5/i)
				elif i == 4:
					mult = (1.5/i)

				scale = 0.7**(i-1)
				if i == 4:
					scale = 0.5*0.7**(i-2)
				take_group = VGroup(take_item, take_weight, take_value).scale(scale).move_to(item.get_center() + LEFT*mult + DOWN*(4/i))

				self.play(Create(take_item))
				self.play(Write(take_weight))
				self.play(Write(take_value))


				# Fade out if exceeds weight
				if int(cur_weight) + weights[i-1] > 5:
					red_x = Text("X", color=RED).move_to(take_group.get_center())
					self.play(SpinInFromNothing(red_x))
					self.play(FadeOut(take_group), FadeOut(red_x))
				else:
					new_row.append(take_group)

					# Replace max value
					if int(cur_value) + values[i-1] > max_value:
						max_value = int(cur_value) + values[i-1]
						self.play(Transform(max_value_text, Text(f"max = {max_value}", font_size=24, color=MAX_VALUE_COLOUR).move_to(capacity.get_center() + DOWN*0.5)))
						self.play(Indicate(max_value_text))


				# Don't take item
				leave_group = item.copy()
				scale = 0.7
				if i == 4:
					scale = 0.5
				self.play(leave_group.animate.scale(scale).move_to(item.get_center() + RIGHT*mult + DOWN*(4/i)))

				new_row.append(leave_group)

			current_row = new_row
			self.play(FadeOut(highlight_2))


		fade_out_scene(self)




class SortByValue(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Write the idea
		idea_1 = Text("Idea #1: Sort the items by value, and greedily pack the most valuable items first.", 
			font_size=20, t2c={"Idea #1:": RED, "value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).move_to(UP*3)
		
		self.play(Write(idea_1))
		self.wait(2)


		# Create the suitcase
		suitcase = make_suitcase().move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.play(Create(suitcase), Write(suitcase_text), Write(suitcase_weight))
		self.wait(2)


		# Create the items
		item_numbers, weights, values = ["#", 1, 2, 3], ["w", 10, 5, 5], ["v", 100, 80, 70]
		objects = [
			Dot(radius=0.1), 
			Dot(radius=0.02*weights[1], color=get_value_colour(70, 100, values[1])),
			Dot(radius=0.02*weights[2], color=get_value_colour(70, 100, values[2])),
			Dot(radius=0.02*weights[3], color=get_value_colour(70, 100, values[3]))
		]

		table = VGroup()
		for i in range(0, len(objects)):
			row = VGroup()

			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			row.add(item_number)

			row.add(objects[i].move_to(DOWN*(i-1) + LEFT*4))

			if i == 0:
				colour = WHITE
			else:
				colour = ITEM_WEIGHT_COLOUR
			weight = Text(str(weights[i]), font_size=24, color=colour).move_to(DOWN*(i-1) + LEFT*3)
			row.add(weight)

			if i == 0:
				colour = WHITE
			else:
				colour = VALUE_COLOUR
			value = Text(str(values[i]), font_size=24, color=VALUE_COLOUR).move_to(DOWN*(i-1) + LEFT*2)
			row.add(value)

			self.play(Create(row))
			table.add(row)
		self.wait(2)


		# Highlight the first row
		highlight = Rectangle(
			width=4, height=1,
			color=ORANGE,
			stroke_width=0,
			fill_opacity=0.15
		).move_to(table[1].get_center())
		self.play(FadeIn(highlight))
		self.wait(2)

		item_1_copy = objects[1].copy()
		self.play(objects[1].animate.scale(5).move_to(suitcase.get_center()))

		suitcase_weight_2 = Text(f"W = {weights[1]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value = Text(f"V = {values[1]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		self.wait(2)

		red_x = Text("X", color=RED)
		self.play(SpinInFromNothing(red_x))
		self.wait(1)

		suitcase_weight_2 = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.play(
			FadeOut(red_x), 
			FadeOut(objects[1]), 
			FadeOut(max_value), 
			FadeIn(item_1_copy),
			Transform(suitcase_weight, suitcase_weight_2)
		)


		# Show the better two items
		self.play(highlight.animate.stretch_to_fit_height(2).set_color(YELLOW).shift(DOWN*1.5))
		self.wait(2)

		item_2_copy = objects[2].copy()		
		self.play(objects[2].animate.scale(5).move_to(suitcase.get_center() + DOWN + LEFT*0.5))

		suitcase_weight_2 = Text(f"W = {weights[2]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value = Text(f"V = {values[2]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)

		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Transform(max_value, max_value_2),
			Transform(suitcase_weight, suitcase_weight_2)
		)		
		self.wait(5)


		self.play(
			FadeIn(item_2_copy),
			FadeIn(item_3_copy),
			FadeOut(objects[2]),
			FadeOut(objects[3]),
			FadeOut(max_value),
			FadeOut(highlight),
			FadeOut(idea_1)
		)




class SortByValueWeightRatio(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Create the items
		item_numbers, weights, values = ["#", 1, 2, 3], ["w", 10, 5, 5], ["v", 100, 80, 70]
		objects = [
			Dot(radius=0.1), 
			Dot(radius=0.02*weights[1], color=get_value_colour(70, 100, values[1])),
			Dot(radius=0.02*weights[2], color=get_value_colour(70, 100, values[2])),
			Dot(radius=0.02*weights[3], color=get_value_colour(70, 100, values[3]))
		]

		table = VGroup()
		for i in range(0, len(objects)):
			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			self.add(item_number)

			if i == 0:
				colour = WHITE
			else:
				colour = ITEM_WEIGHT_COLOUR			
			weight = Text(str(weights[i]), font_size=24, color=colour).move_to(DOWN*(i-1) + LEFT*3)

			if i == 0:
				colour = WHITE
			else:
				colour = VALUE_COLOUR	
			value = Text(str(values[i]), font_size=24, color=colour).move_to(DOWN*(i-1) + LEFT*2)

			if i > 0:
				table.add(
					VGroup(
						objects[i].move_to(DOWN*(i-1) + LEFT*4),
						weight,
						value
					)
				)

			else:
				self.add(objects[i].move_to(DOWN*(i-1) + LEFT*4))
				self.add(weight)
				self.add(value)

		self.add(table)


		# Create the suitcase
		suitcase = make_suitcase().move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.add(suitcase, suitcase_text, suitcase_weight)
		self.wait(2)


		# Write the idea
		idea_2 = Text("Idea #2: Pack the items in descending order of their value:weight ratio.", 
			font_size=20, t2c={"Idea #2:": RED, "value": VALUE_COLOUR, "weight": ITEM_WEIGHT_COLOUR}).move_to(UP*3)
		
		self.play(Write(idea_2))
		self.wait(2)


		# Moves row i to row j in the table
		def swap_rows(i, j, table):
			background_rect = Rectangle(
				width=table[i].width+0.5, 
				height=table[i].height+0.5, 
				fill_color=table[j][0].fill_color,
				fill_opacity=0.15,
				stroke_width=0
			).move_to(table[i].get_center())

			self.play(FadeIn(background_rect))

			# Move all the rows down one
			shuffle = [table[k].animate.shift(DOWN) for k in range(i-1, j-1, -1)]
			self.play(
				LaggedStart(*shuffle, lag_ratio=1/(i-j)),
				table[i].animate.shift(UP),
				background_rect.animate.shift(UP),
				run_time=1
			)
			self.play(FadeOut(background_rect))

			# Swap the rows in the table
			tmp = table[i]
			for k in range(i, j, -1):
				table[k] = table[k-1]	
			table[j] = tmp


		# Write in the value/weight ratios
		ratio = ["v/w"] + [values[i]/weights[i] for i in range(1, len(values))]

		for i in range(0, len(ratio)):
			vw = None
			if i == 0:
				vw = Text(str(ratio[i]), font_size=24).move_to(DOWN*(i-1) + LEFT)
				self.play(Write(vw))
				self.wait(1)

			else:
				vw = Text(f"{values[i]}/{weights[i]}", font_size=24).move_to(DOWN*(i-1) + LEFT)
				self.play(Write(vw))
				self.wait(1)

				vw_ans = Text(f"{ratio[i]}", font_size=24).move_to(DOWN*(i-1) + LEFT)
				self.play(Transform(vw, vw_ans))
				self.wait(1)

				table[i-1].add(vw)

			if i == 2:
				swap_rows(1, 0, table)
			elif i == 3:
				swap_rows(2, 1, table)
		self.wait(2)


		# Pack the two top items
		item_2_copy = objects[2].copy()
		self.play(objects[2].animate.scale(5).move_to(suitcase.get_center() + DOWN + LEFT*0.5))

		suitcase_weight_2 = Text(f"W = {weights[2]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value = Text(f"V = {values[2]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)


		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Transform(max_value, max_value_2),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		self.wait(2)


		self.play(
			FadeOut(objects[2]),
			FadeOut(objects[3]),
			FadeOut(max_value),
			FadeOut(table)
		)




class SortByValueWeightCounterExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Write the idea
		idea_2 = Text("Idea #2: Pack the items in descending order of their value:weight ratio.", 
			font_size=20, t2c={"Idea #2:": RED, "value": VALUE_COLOUR, "weight": ITEM_WEIGHT_COLOUR}).move_to(UP*3)
		
		self.add(idea_2)


		# Create the suitcase
		suitcase = make_suitcase().move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.add(suitcase, suitcase_text, suitcase_weight)
		self.wait(2)



		# Show the counterexample
		item_numbers = ["#", 1, 2, 3]
		weights, values = ["w", 7, 5, 5], ["v", 70, 40, 40]
		objects = [
			Dot(radius=0.1), 
			Dot(radius=0.02*weights[1], color=get_value_colour(40, 70, values[1])),
			Dot(radius=0.02*weights[2], color=get_value_colour(40, 70, values[2])),
			Dot(radius=0.02*weights[3], color=get_value_colour(40, 70, values[3]))
		]
		ratio = ["v/w"] + [values[i]/weights[i] for i in range(1, len(values))]


		# Table headings
		table = VGroup()
		for i in range(0, len(objects)):
			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			self.add(item_number)

			if i == 0:
				self.add(
					objects[i].move_to(DOWN*(i-1) + LEFT*4),
					Text(str(weights[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*3),					
					Text(str(values[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*2),
					Text(str(ratio[i]), font_size=24).move_to(DOWN*(i-1) + LEFT)
				)


		for i in range(1, len(objects)):
			self.play(Create(objects[i].move_to(DOWN*(i-1) + LEFT*4)))

			weight = Text(str(weights[i]), font_size=24, color=ITEM_WEIGHT_COLOUR).move_to(DOWN*(i-1) + LEFT*3)
			self.play(Write(weight))

			value = Text(str(values[i]), font_size=24, color=VALUE_COLOUR).move_to(DOWN*(i-1) + LEFT*2)
			self.play(Write(value))

			table.add(
				VGroup(
					objects[i].move_to(DOWN*(i-1) + LEFT*4),
					weight,
					value
				)
			)


		# v/w ratio
		for i in range(1, len(objects)):
			vw = Text(str(ratio[i]), font_size=24).move_to(DOWN*(i-1) + LEFT)
			self.play(Write(vw))

			table[i-1].add(vw)


		self.add(table)
		self.wait(2)


		# Counterexample
		item_1_copy = objects[1].copy()
		self.play(objects[1].animate.scale(5).move_to(suitcase.get_center()))

		suitcase_weight_2 = Text(f"W = {weights[1]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value = Text(f"V = {values[1]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		self.wait(2)

		red_x = Text("X", color=RED)
		self.play(SpinInFromNothing(red_x))
		self.wait(1)

		suitcase_weight_2 = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.play(
			FadeIn(item_1_copy),
			FadeOut(red_x), 
			FadeOut(objects[1]), 
			FadeOut(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)


		# Show two correct ones
		item_2_copy = objects[2].copy()
		self.play(objects[2].animate.scale(5).move_to(suitcase.get_center() + DOWN + LEFT*0.5))

		suitcase_weight_2 = Text(f"W = {weights[2]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value = Text(f"V = {values[2]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		

		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Transform(max_value, max_value_2),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		self.wait(5)




class KnapsackIntroduction(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Title
		title = Text("0/1 Knapsack Problem").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		# Given a list of items
		items, weight_texts, value_texts = VGroup(), VGroup(), VGroup()
		weights = [2, 1, 3, 1, 4]
		values = [25, 10, 40, 20, 45]


		camera = make_camera().move_to(RIGHT*3)
		pen = make_pen().move_to(LEFT*5 + UP*2)
		sneakers = make_sneakers().move_to(UP*2 + RIGHT*5)
		toothbrush = make_toothbrush().move_to(LEFT*3)
		headphones = make_headphones().move_to(UP*2)

		items.add(camera, pen, sneakers, toothbrush, headphones)
		items.shift(DOWN)		


		for i in range(0, len(items)):	
			self.play(Create(items[i]))
		self.wait(2)


		# Each item has a weight
		for i in range(0, len(items)):
			weight_text = Text(f"w = {weights[i]}kg", font_size=20, color=ITEM_WEIGHT_COLOUR).next_to(items[i], DOWN)
			weight_texts.add(weight_text)
			self.play(Write(weight_text))
		self.wait(2)


		complete_items = VGroup()


		# And a value
		for i in range(len(items)):
			value_text = Text(f"v = {values[i]}", font_size=20, color=VALUE_COLOUR).next_to(weight_texts[i], DOWN)
			value_texts.add(value_text)
			self.play(Write(value_text))

			complete_items.add(VGroup(items[i], weight_texts[i], value_texts[i]))

		self.wait(2)


		# You are also given a capacity
		suitcase = RoundedRectangle(
			width=2, height=2,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		).scale(0.8).shift(UP*0.2+RIGHT*0.3)


		# Move each object around the suitcase
		bag_radius = 2.5
		bag_centre = DOWN*0.5

		move_around_bag = []
		i = 0
		while i < len(complete_items):
			up = bag_radius*math.sin(i*2*PI/len(complete_items))
			right = bag_radius*math.cos(i*2*PI/len(complete_items))
			position = UP*up + RIGHT*right

			move_around_bag.append(complete_items[i].animate.move_to(position+bag_centre).scale(0.8))
			i += 1


		self.play(
			Create(suitcase),
			*move_around_bag
		)
		self.wait(2)

		suitcase_weight = Text("W = 5kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN)
		self.play(Write(suitcase_weight))
		self.wait(2)


		suitcase_weight_2 = Text("W = 0/5 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN)
		self.play(Transform(suitcase_weight, suitcase_weight_2))
		self.wait(2)


		# Goal 1: Total weight doesn't go over limit
		cur_weight = 0
		for i in [2, 4]:
			self.play(
				items[i].animate.move_to(suitcase.get_center())
			)

			cur_weight += weights[i]
			self.play(
				FadeOut(items[i]),
				Transform(suitcase_weight, Text(f"W = {cur_weight}/5 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN))
			)


		red_x = Text("X", color=RED).shift(UP*0.2+RIGHT*0.3)
		self.play(Indicate(suitcase_weight, color=RED), SpinInFromNothing(red_x))
		self.play(FadeOut(red_x))


		move_back = []
		for i in [2, 4]:
			up = bag_radius*math.sin(i*2*PI/len(items))
			right = bag_radius*math.cos(i*2*PI/len(items))
			position = UP*up + RIGHT*right

			move_back.append(items[i].animate.move_to(position+bag_centre+UP*0.5))
			i += 1

		self.play(
			*move_back,
			Transform(suitcase_weight, Text(f"W = 0/5 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN))
		)
		self.wait(2)


		# Goal 2: Value is as high as possible
		max_value_text = Text("V = 0", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(Write(max_value_text))


		cur_weight, cur_val = 0, 0
		for i in [1,2,3]:
			self.play(
				items[i].animate.move_to(suitcase.get_center())
			)

			cur_weight += weights[i]
			cur_val += values[i]
			self.play(
				FadeOut(items[i]),
				Transform(suitcase_weight, Text(f"W = {cur_weight}/5 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN)),
				Transform(max_value_text, Text(f"V = {cur_val}", font_size=24, color=MAX_VALUE_COLOUR).move_to(suitcase_weight.get_center() + DOWN*0.5))
			)


		self.play(
			Indicate(max_value_text, color=GREEN)
		)
		self.wait(2)

		fade_out_scene(self)




class DynamicProgramming(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Title
		title = Text("Dynamic Programming").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		# Show grid turning into squares
		grid = VGroup()
		left, up = 2.5, 1.5

		for r in range(0, 4):
			row = VGroup()
			left = 2.5			

			for c in range(0, 6):
				square = Square(
					side_length=1,
					fill_color=WHITE,
					stroke_color=WHITE,
					stroke_width=0.5,
					fill_opacity=1
				).move_to(LEFT*left + UP*up)
				row.add(square.scale(1.2))

				left -= 1

			grid.add(row)
			up -= 1

		self.play(FadeIn(grid))
		self.wait(2)


		# Show the "subproblems"
		for row in grid:
			for cell in row:
				self.play(cell.animate.set_fill(opacity=0), run_time=0.1)
		self.wait(2)


		# Merge subproblems
		count = 0
		for i in range(0, len(grid)):
			for j in range(0, len(grid[0])):
				if i == 0:
					self.play(grid[i][j].animate.set_fill(
							get_value_colour(0, len(grid[0])-1, j),
							opacity=0.2
						)						
					)

				elif j == 0:
					self.play(grid[i][j].animate.set_fill(
							get_value_colour(0, len(grid)-1, i),
							opacity=0.2
						)						
					)

				else:
					combo = VGroup()
					combo_anim = []

					left_square = grid[i][j-1].copy()
					combo_anim.append(left_square.animate.shift(RIGHT))

					top_square = grid[i-1][j].copy()
					combo_anim.append(top_square.animate.shift(DOWN))

					self.play(*combo_anim)
					combo = VGroup(left_square, top_square)

					grid[i][j] = combo

		self.wait(2)

		fade_out_scene(self)




class SmallExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Suitcase shrinks to 1kg
		suitcase = make_suitcase()
		suitcase_weight = Text("W = 5kg", font_size=30, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase, DOWN)
		suitcase_group = VGroup(suitcase, suitcase_weight)
		self.play(Create(suitcase_group))
		self.wait(2)
		
		self.play(
			suitcase_group.animate.scale(0.4)			
		)

		suitcase_weight_2 = Text(
			"W = 1kg", font_size=30, color=WEIGHT_LIMIT_COLOUR
		).move_to(suitcase_weight.get_center()).scale(0.4)
		self.play(
			Transform(suitcase_weight, suitcase_weight_2)			
		)

		self.play(suitcase_group.animate.shift(RIGHT*5))
		


		# Add all the items
		item_numbers = ["#", 0, 1, 2, 3, 4, 5]
		weights = ["w", 0, 1, 2, 3, 1, 4]
		values = ["v", 0, 10, 25, 40, 20, 45]
		objects = [
			Dot(radius=0.8),	
			Dot(radius=0.2),
			make_pen(),
			make_camera(),
			make_sneakers(),
			make_toothbrush(),
			make_headphones()
		]


		table_ul = DOWN*-2.5 + LEFT*6.5
		table = VGroup()

		for i in range(0, len(objects)):
			RT = 0.2

			item_number = Text(str(item_numbers[i]), font_size=24).move_to(table_ul + DOWN*i + RIGHT*0)
			self.play(Write(item_number), run_time=RT)

			obj = objects[i].move_to(table_ul + DOWN*i + RIGHT*1).scale(0.2)
			self.play(Create(obj), run_time=RT)

			if i == 0:
				colour = WHITE
			else:
				colour = ITEM_WEIGHT_COLOUR			
			weight = Text(str(weights[i]), font_size=24, color=colour).move_to(table_ul + DOWN*i + RIGHT*2)
			self.play(Write(weight), run_time=RT)			

			if i == 0:
				colour = WHITE
			else:
				colour = VALUE_COLOUR	
			value = Text(str(values[i]), font_size=24, color=colour).move_to(table_ul + DOWN*i + RIGHT*3)
			self.play(Write(value), run_time=RT)

			table.add(
				VGroup(
					item_number,
					obj,
					weight,
					value
				)
			)

		self.add(table)
		self.wait(2)



		# Add the weight heading
		w = Text("W", color=PINK, font_size=24).move_to(table_ul + UP + RIGHT*4)

		for weight in range(0, 6):
			weight_text = Text(f"{weight}", font_size=24).move_to(table_ul + RIGHT*(weight+4))
			self.play(Write(weight_text))
			table[0].add(weight_text)

		self.play(Write(w))
		self.wait(2)



		# Explain the meaning of cell (i, j)
		cell_explain = Text(
			"cell (i, j) = The best value we can pack into\na bag of capacity j, using the first i items.", 
			font_size=18
		).move_to(UP*3.5 + RIGHT*3.5)
		self.play(Write(cell_explain))
		self.wait(2)


		# Explain the meaning of the rows
		i, j = 3+1, 1+4
		arrow = Arrow(
			start=table[i][0].get_right()+RIGHT*(j+1.5), 
			end=table[i][0].get_right()+RIGHT*(j+0.25)
		)
		box = Rectangle(
			width=1, height=0.75, 
			fill_color=WHITE, 
			fill_opacity=0.2,
			stroke_width=0
		).next_to(arrow, LEFT, buff=0)
		arrow_box = VGroup(arrow, box)
		self.play(Create(arrow_box))


		# (3, 1)
		explain_row = Text(
			"Max value we can pack\ninto a 1kg bag using\nthe first 3 items.", 
			font_size=18
		).next_to(arrow_box.get_right())

		item_brace = BraceBetweenPoints(table[1][3].get_top(), table[i][3].get_bottom(), direction=RIGHT)
		self.play(Write(explain_row), Create(item_brace))

		self.play(Flash(table[0][j]))
		self.play(Flash(table[i][0]))

		self.wait(2)


		# (4, 3)
		i, j = 4+1, 3+4
		item_brace_2 = BraceBetweenPoints(table[1][3].get_top(), table[i][3].get_bottom(), direction=RIGHT)
		self.play(
			arrow_box.animate.shift(DOWN + RIGHT*2),
			explain_row.animate.shift(DOWN + RIGHT*2),
			Transform(item_brace, item_brace_2)
		)

		explain_row_2 = Text(
			"Max value we can pack\ninto a 3kg bag using\nthe first 4 items.", 
			font_size=18
		).next_to(arrow_box.get_right())
		self.play(Transform(explain_row, explain_row_2))

		self.play(Flash(table[0][j]))
		self.play(Flash(table[i][0]), Flash(explain_row.get_center()+DOWN*0.25))

		self.wait(2)


		self.play(
			FadeOut(arrow_box),
			FadeOut(item_brace),
			FadeOut(explain_row)
		)


		# Highlight the zero item
		item_rect = Rectangle(
			width=4, height=1
		).move_to(table.get_center()+UP*2+LEFT*3)
		self.play(Create(item_rect))
		self.wait(2)


		# Value of zero item is 0
		for cur_weight in range(0, 6):
			zero_val = Text("0", font_size=24).move_to(table[1][cur_weight+3].get_center()+RIGHT)
			table[1].add(zero_val)
			self.play(Write(zero_val))
		self.wait(2)


		# Highlight the zero column
		item_rect_2 = Rectangle(
			width=1, height=1
		).move_to(table.get_center()+LEFT*0.5+UP*3)
		self.play(Transform(item_rect, item_rect_2))
		self.wait(2)


		# Value of zero capacity is 0		
		for cur_item in range(1, 6):
			zero_val = Text("0", font_size=24).move_to(table[cur_item][4].get_center()+DOWN)
			table[cur_item+1].add(zero_val)
			self.play(Write(zero_val))
		self.play(FadeOut(item_rect))
		self.wait(2)



		# Algorithm time!
		for cur_weight in range(1, 6):
			j = cur_weight+4
			bag_items = VGroup().move_to(suitcase.get_center())


			# Border around current item
			item_rect = Rectangle(
				width=4, height=1
			).move_to(table.get_center()+UP*1+LEFT*3)
			self.play(Create(item_rect))
			self.wait(2)


			for cur_item in range(1, 6):
				i, vi, wi = cur_item+1, 3, 2
				new_val = None
				fade_out_anim = []


				# This item's value and weight
				cur_item_val = int(table[i][vi].text)
				cur_item_weight = int(table[i][wi].text)


				# Border around current item
				if cur_item > 1:
					self.play(item_rect.animate.shift(DOWN))
					self.wait(2)
				

				# Emphasise the weight of the current item
				weight_rect = Rectangle(
					width=1, height=0.75,
					color=ORANGE, 
					stroke_width=0,
					fill_opacity=0.2
				).move_to(table[i][wi])

				too_heavy = True
				if cur_item_weight <= cur_weight:
					too_heavy = False

				self.play(FadeIn(weight_rect))
				self.wait(1)
				self.play(Indicate(weight_rect, color=(RED if too_heavy else GREEN)))
				self.wait(1)
				self.play(FadeOut(weight_rect))


				if not too_heavy:

					# Previous best value
					prev_val = 0
					prev_val_rect = Rectangle(
						width=1, height=0.75,
						color=PINK, 
						stroke_width=0,
						fill_opacity=0.2
					).move_to(table[i-1][j].get_center())
					
					self.play(FadeIn(prev_val_rect))
					fade_out_anim.append(FadeOut(prev_val_rect))
					self.wait(2)

					prev_val = int(table[i-1][j].text)


					# Value of the current item
					cur_val_rect = Rectangle(
						width=1, height=0.75,
						color=GOLD, 
						stroke_width=0,
						fill_opacity=0.2
					).move_to(table[i][vi])

					self.play(FadeIn(cur_val_rect))
					fade_out_anim.append(FadeOut(cur_val_rect))
					self.wait(2)


					# Value of the optimal previous bag
					best_bag_rect = None
					best_bag_val = 0
					if cur_item_weight <= cur_weight:
						best_bag_rect = Rectangle(
							width=1, height=0.75,
							color=GOLD, 
							stroke_width=0,
							fill_opacity=0.2
						).move_to(table[i-1][j-cur_item_weight])
						
						self.play(FadeIn(best_bag_rect))
						fade_out_anim.append(FadeOut(best_bag_rect))
						self.wait(2)

						if cur_weight == 2 and cur_item == 4:
							self.play(Indicate(best_bag_rect, color=GOLD))
							self.wait(2)

						best_bag_val = int(table[i-1][j-cur_item_weight].text)


					# Shift the correct values
					flash_green_anim, shift_val_anim, transform_val_anim = [], [], []

					new_val, new_val_3 = None, None
					new_pos = table[i][j-1].get_center() + RIGHT

					if cur_item_val + best_bag_val > prev_val:
						flash_green_anim.append(Indicate(cur_val_rect, color=GREEN))
						new_val = table[i][vi].copy().set_color(WHITE)					

						flash_green_anim.append(Indicate(best_bag_rect, color=GREEN))
						new_val_2 = table[i-1][j-cur_item_weight].copy()
						shift_val_anim.append(new_val_2.set_color(WHITE).animate.move_to(new_pos))

						transform_val_anim.append(FadeOut(new_val_2))
						new_val_3 = Text(str(cur_item_val + best_bag_val), font_size=24)
						transform_val_anim.append(Transform(new_val, new_val_3.move_to(new_pos)))							

					else:
						flash_green_anim.append(Indicate(prev_val_rect, color=GREEN))
						new_val = table[i-1][j].copy().set_color(WHITE)
					
					shift_val_anim.append(new_val.animate.move_to(new_pos))


					# Quick aside - show the items being added together
					if cur_item == 4 and cur_weight == 2:
						toothbrush_2 = make_toothbrush().scale(0.7)
						toothbrush_weight = Text("w = 1kg", font_size=24, color=ITEM_WEIGHT_COLOUR).next_to(toothbrush_2, DOWN)
						toothbrush_group = VGroup(toothbrush_2, toothbrush_weight).move_to(suitcase_group.get_center() + LEFT*3 + UP*0.5)
						
						self.play(Create(toothbrush_group))
						fade_out_anim.append(FadeOut(toothbrush_group))

						plus = Text("+").move_to(suitcase_group.get_center() + LEFT*3 + DOWN*0.5)
						
						self.play(Write(plus))
						fade_out_anim.append(FadeOut(plus))

						suitcase_2 = make_suitcase()
						suitcase_weight_2 = Text("W = 1kg", font_size=30, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_2, DOWN)
						suitcase_group_2 = VGroup(suitcase_2, suitcase_weight_2).scale(0.4).move_to(suitcase_group.get_center() + LEFT*3 + DOWN*2.5)
						suitcase_group_2.add(table[2][1].copy().move_to(suitcase_2.get_center()))
						
						self.play(Create(suitcase_group_2))
						fade_out_anim.append(FadeOut(suitcase_group_2))
						
						equals = Text("=").move_to(suitcase_group.get_center() + LEFT*1.5)
						self.play(Write(equals))
						fade_out_anim.append(FadeOut(equals))

						toothbrush_copy = table[5][1].copy().move_to(suitcase.get_center() + DOWN*0.25)
						pen_copy = table[2][1].copy().move_to(suitcase.get_center() + UP*0.25)
						bag_contents = VGroup(toothbrush_copy, pen_copy)
						self.play(Transform(bag_items, bag_contents))
						self.wait(2)

						self.play(Indicate(best_bag_rect, color=GOLD))
						self.wait(2)


					self.play(*flash_green_anim)
					self.wait(2)

					self.play(*shift_val_anim)
					if len(transform_val_anim) > 0:
						self.play(*transform_val_anim)
					self.wait(2)

					if new_val_3 != None:
						new_val = new_val_3


				else:
					# Too heavy, keep the previous item
					new_val = table[i-1][j].copy()
					self.play(new_val.animate.shift(DOWN))
					self.wait(2)


				# Fade in the bag items
				# This is dumb but I just found it easier to hard code this
				new_bag_items = None
				if cur_item == 1:
					new_bag_items = VGroup(
						table[2][1].copy()
					)
				elif cur_weight == 1 and cur_item == 4:
					new_bag_items = VGroup(
						table[5][1].copy()
					)
				elif cur_weight == 2 and cur_item == 2:
					new_bag_items = VGroup(
						table[3][1].copy()
					)
				elif cur_weight >= 3 and cur_item == 2:
					new_bag_items = VGroup(
						table[2][1].copy(),
						table[3][1].copy()
					)
				elif cur_weight == 3 and cur_item == 3:
					new_bag_items = VGroup(
						table[4][1].copy()
					)
				elif cur_weight == 4 and cur_item == 3:
					new_bag_items = VGroup(
						table[2][1].copy(),
						table[4][1].copy()
					)
				elif cur_weight == 3 and cur_item == 4:
					new_bag_items = VGroup(
						table[3][1].copy(),
						table[5][1].copy()
					)
				elif cur_weight == 4 and cur_item == 4:
					new_bag_items = VGroup(
						table[4][1].copy(),
						table[5][1].copy()
					)
				elif cur_weight == 5 and cur_item == 3:
					new_bag_items = VGroup(
						table[3][1].copy(),
						table[4][1].copy()
					)
				elif cur_weight == 5 and cur_item == 4:
					new_bag_items = VGroup(
						table[2][1].copy(),
						table[4][1].copy(),
						table[5][1].copy()
					)



				if new_bag_items != None:
					self.play(Transform(bag_items, new_bag_items.arrange(DOWN).move_to(suitcase.get_center())))


				if len(fade_out_anim) > 0:
					self.play(*fade_out_anim)


				table[i].add(new_val)


			# Highlight the answer
			ans_rect = Rectangle(
				width=1, height=0.75,
				color=GREEN, 
				stroke_width=0,
				fill_opacity=0.2
			).move_to(table[6][j])

			self.play(FadeOut(item_rect))
			self.play(FadeIn(ans_rect))
			self.play(Flash(bag_items, color=GREEN))
			self.play(FadeOut(ans_rect))
			self.wait(2)		


			if cur_weight < 5:
				# Resize the bag
				self.play(suitcase_group.animate.scale(1.2), FadeOut(bag_items))

				suitcase_weight_2 = Text(
					f"W = {cur_weight+1}kg", font_size=30, color=WEIGHT_LIMIT_COLOUR
				).move_to(suitcase_weight.get_center()).scale(0.4*(1.2**cur_weight))
				self.play(Transform(suitcase_weight, suitcase_weight_2))


		self.wait(2)
		fade_out_scene(self)




class LargeExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Add all the items
		item_numbers = ["#", 0, 1, 2, 3, 4, 5, 6, 7, 8]
		weights = ["w", 0, 3, 4, 9, 2, 7, 5, 1, 8]
		values = ["v", 0, 15, 20, 40, 10, 20, 35, 10, 25]
		item_desc = [item_numbers, weights, values]
		W, n = 10, len(item_numbers)


		table_ul = UP*2 + LEFT*6.5
		table = VGroup()

		RT, FZ = 0.2, 18

		d = 0
		for i in range(0, n):
			r = 0
			row = VGroup()

			for j in range(0, len(item_desc)):

				if j == 0 or i == 0:
					colour = WHITE
				else:
					if j == 1:
						colour = ITEM_WEIGHT_COLOUR
					elif j == 2:
						colour = VALUE_COLOUR

				item = Text(str(item_desc[j][i]), font_size=FZ, color=colour).move_to(table_ul + DOWN*d + RIGHT*r)
				self.play(Write(item), run_time=RT)

				row.add(item)
				r += 0.5

			table.add(row)
			d += 0.5

		self.add(table)
		self.wait(2)


		# Add the weight heading
		w = Text("W", color=PINK, font_size=24).move_to(table_ul + UP*0.5 + RIGHT*1.5)

		r = 1.5
		for weight in range(0, W+1):
			weight_text = Text(f"{weight}", font_size=FZ).move_to(table_ul + RIGHT*r)
			self.play(Write(weight_text), run_time=RT)

			table[0].add(weight_text)
			r += 0.5

		self.play(Write(w))
		self.wait(2)


		# Base cases
		r, d = 1.5, 0.5
		for i in range(0, W+1):
			zero_text = Text("0", font_size=FZ).move_to(table_ul + RIGHT*r + DOWN*d)
			self.play(Write(zero_text), run_time=RT)

			table[1].add(zero_text)
			r += 0.5
		self.wait(2)

		r, d = 1.5, 1.0
		for i in range(2, n):
			zero_text = Text("0", font_size=FZ).move_to(table_ul + RIGHT*r + DOWN*d)
			self.play(Write(zero_text), run_time=RT)

			table[i].add(zero_text)
			d += 0.5
		self.wait(2)


		
		# Border around current item
		item_rect = Rectangle(
			width=1.5, height=0.5
		).move_to(table_ul + RIGHT*0.5 + DOWN*1)
		self.play(Create(item_rect))
		self.wait(2)


		# Border around current weight
		weight_rect = Rectangle(
			width=0.5, height=0.5
		).move_to(table_ul + RIGHT*2 + DOWN*0)
		self.play(Create(weight_rect))
		self.wait(2)


		for i in range(0, len(table)):
			for j in range(0, len(table[i])):
				print(table[i][j])
			print('\n')


		# Algorithm
		for cur_item in range(1, n-1):		
			self.play(weight_rect.animate.move_to(table_ul + RIGHT*2 + DOWN*0))	
			i = cur_item+1	
			wi, vi = 1, 2


			for cur_weight in range(1, W+1):
				j = cur_weight+3

				new_val = None
				fade_out_anim = []


				# This item's value and weight
				cur_item_val = int(table[i][vi].text)
				cur_item_weight = int(table[i][wi].text)
				

				# Emphasise the weight of the current item
				weight_rect_2 = Rectangle(
					width=0.5, height=0.5,
					color=ORANGE, 
					stroke_width=0,
					fill_opacity=0.2
				).move_to(table[i][wi])

				too_heavy = True
				if cur_item_weight <= cur_weight:
					too_heavy = False

				self.play(FadeIn(weight_rect_2))
				self.play(Indicate(weight_rect_2, color=(RED if too_heavy else GREEN)))
				self.play(FadeOut(weight_rect_2))


				# Find the value
				# Previous best value
				prev_val = int(table[i-1][j].text)
				prev_val_rect = Rectangle(
					width=0.5, height=0.5,
					color=PINK, 
					stroke_width=0,
					fill_opacity=0.2
				).move_to(table[i-1][j].get_center())
				
				self.play(FadeIn(prev_val_rect))
				fade_out_anim.append(FadeOut(prev_val_rect))


				if not too_heavy:

					# Value of the current item
					cur_val_rect = Rectangle(
						width=0.5, height=0.5,
						color=GOLD, 
						stroke_width=0,
						fill_opacity=0.2
					).move_to(table[i][vi])

					self.play(FadeIn(cur_val_rect))
					fade_out_anim.append(FadeOut(cur_val_rect))


					# Value of the optimal previous bag
					best_bag_rect = None
					best_bag_val = 0
					if cur_item_weight <= cur_weight:
						best_bag_rect = Rectangle(
							width=0.5, height=0.5,
							color=GOLD, 
							stroke_width=0,
							fill_opacity=0.2
						).move_to(table[i-1][j-cur_item_weight])
						
						self.play(FadeIn(best_bag_rect))
						fade_out_anim.append(FadeOut(best_bag_rect))

						best_bag_val = int(table[i-1][j-cur_item_weight].text)


					# Shift the correct values
					flash_green_anim, shift_val_anim, transform_val_anim = [], [], []

					new_val, new_val_3 = None, None
					new_pos = table[i][j-1].get_center() + RIGHT*0.5

					if cur_item_val + best_bag_val > prev_val:
						flash_green_anim.append(Indicate(cur_val_rect, color=GREEN))
						new_val = table[i][vi].copy().set_color(WHITE)					

						flash_green_anim.append(Indicate(best_bag_rect, color=GREEN))
						new_val_2 = table[i-1][j-cur_item_weight].copy()
						shift_val_anim.append(new_val_2.set_color(WHITE).animate.move_to(new_pos))

						transform_val_anim.append(FadeOut(new_val_2))
						new_val_3 = Text(str(cur_item_val + best_bag_val), font_size=FZ)
						transform_val_anim.append(Transform(new_val, new_val_3.move_to(new_pos)))							

					else:
						flash_green_anim.append(Indicate(prev_val_rect, color=GREEN))
						new_val = table[i-1][j].copy().set_color(WHITE)
					
					shift_val_anim.append(new_val.animate.move_to(new_pos))

					self.play(*flash_green_anim)

					self.play(*shift_val_anim)
					if len(transform_val_anim) > 0:
						self.play(*transform_val_anim)

					if new_val_3 != None:
						new_val = new_val_3


				else:
					# Too heavy, keep the previous item
					new_val = table[i-1][j].copy()
					self.play(new_val.animate.shift(DOWN*0.5))


				if len(fade_out_anim) > 0:
					self.play(*fade_out_anim)

				table[i].add(new_val)


				if cur_weight < W:
					self.play(weight_rect.animate.shift(RIGHT*0.5))

			if cur_item < n-2:
				self.play(item_rect.animate.shift(DOWN*0.5))


		# Highlight the answer
		ans_rect = Rectangle(
			width=0.5, height=0.5,
			color=GREEN, 
			stroke_width=0,
			fill_opacity=0.2
		).move_to(table[n-1][W+3])

		self.play(FadeIn(ans_rect))
		self.wait(2)
		self.play(FadeOut(ans_rect))
		self.wait(2)


