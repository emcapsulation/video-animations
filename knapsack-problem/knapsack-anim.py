from manim import *

config.background_color = "#15131c"


VALUE_COLOUR = GOLD
WEIGHT_LIMIT_COLOUR = PINK


def fade_out_scene(scene):
	scene.play(
		*[FadeOut(mob)for mob in scene.mobjects]
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




class Introduction(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		# Create the suitcase
		suitcase = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		).move_to(RIGHT*4)
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
			item_text = Text(f"w = {weights[i]}kg", font_size=20).next_to(items[i], DOWN)
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

		weight_texts, value_texts = VGroup(Text("w", font_size=24)), VGroup(Text("v", font_size=24, color=VALUE_COLOUR))
		for i in range(0, n):
			weight_texts.add(Text(f"{weights[i]}", font_size=24))
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
		
		max_value_text = Text("max = 0", font_size=24, color=GREEN).move_to(capacity.get_center() + DOWN*0.5)
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
		take_weight = Text(f"current weight = {weights[i-1]}", font_size=16).next_to(take_item, DOWN)
		take_value = Text(f"current value = {values[i-1]}", color=VALUE_COLOUR, font_size=16).next_to(take_weight, DOWN)

		leave_item = Text(f"[]", font_size=24).move_to(RIGHT*3.2 + UP)
		leave_weight = Text(f"current weight = 0", font_size=16).next_to(leave_item, DOWN)
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
		self.play(Transform(max_value_text, Text(f"max = {max_value}", font_size=24, color=GREEN).move_to(capacity.get_center() + DOWN*0.5)))
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
				take_weight = Text(f"current weight = {int(cur_weight) + weights[i-1]}", font_size=16).next_to(take_item, DOWN)

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
						self.play(Transform(max_value_text, Text(f"max = {max_value}", font_size=24, color=GREEN).move_to(capacity.get_center() + DOWN*0.5)))
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
		suitcase = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		).move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.play(Create(suitcase), Write(suitcase_text), Write(suitcase_weight))
		self.wait(2)


		# Create the items
		item_numbers, weights, values = ["#", 1, 2, 3], ["w", 10, 5, 5], ["v", 100, 80, 70]
		objects = [
			Dot(radius=0.1), 
			Dot(radius=0.02*weights[1], color=ORANGE),
			Dot(radius=0.02*weights[2], color=YELLOW),
			Dot(radius=0.02*weights[3], color=GOLD)
		]

		table = VGroup()
		for i in range(0, len(objects)):
			row = VGroup()

			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			row.add(item_number)

			row.add(objects[i].move_to(DOWN*(i-1) + LEFT*4))

			weight = Text(str(weights[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*3)
			row.add(weight)

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
		max_value = Text(f"V = {values[1]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		
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
		max_value = Text(f"V = {values[2]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)

		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
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
			Dot(radius=0.02*weights[1], color=ORANGE),
			Dot(radius=0.02*weights[2], color=YELLOW),
			Dot(radius=0.02*weights[3], color=GOLD)
		]

		table = VGroup()
		for i in range(0, len(objects)):
			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			self.add(item_number)			

			weight = Text(str(weights[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*3)
			value = Text(str(values[i]), font_size=24, color=VALUE_COLOUR).move_to(DOWN*(i-1) + LEFT*2)

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
		suitcase = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		).move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.add(suitcase, suitcase_text, suitcase_weight)
		self.wait(2)


		# Write the idea
		idea_2 = Text("Idea #2: Pack the items in descending order of their value:weight ratio.", 
			font_size=20, t2c={"Idea #2:": RED, "value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).move_to(UP*3)
		
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
		max_value = Text(f"V = {values[2]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)


		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
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


		# Create the suitcase
		suitcase = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.5
		).move_to(RIGHT*4)
		suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)
		suitcase_weight = Text("W = 0/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		self.add(suitcase, suitcase_text, suitcase_weight)
		self.wait(2)



		# Show the counterexample
		item_numbers = ["#", 1, 2, 3]
		weights, values = ["w", 7, 5, 5], ["v", 70, 40, 40]
		objects = [
			Dot(radius=0.1), 
			Dot(radius=0.02*weights[1], color=GREEN),
			Dot(radius=0.02*weights[2], color=TEAL),
			Dot(radius=0.02*weights[3], color=TEAL)
		]
		ratio = ["v/w"] + [values[i]/weights[i] for i in range(1, len(values))]


		# Table headings
		table = VGroup()
		for i in range(0, len(objects)):
			item_number = Text(str(item_numbers[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*5)
			self.add(item_number)

			if i == 0:
				self.add(
					Text(str(weights[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*4),
					objects[i].move_to(DOWN*(i-1) + LEFT*3),
					Text(str(values[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*2),
					Text(str(ratio[i]), font_size=24).move_to(DOWN*(i-1) + LEFT)
				)


		for i in range(1, len(objects)):
			self.play(Create(objects[i].move_to(DOWN*(i-1) + LEFT*4)))

			weight = Text(str(weights[i]), font_size=24).move_to(DOWN*(i-1) + LEFT*3)
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
		max_value = Text(f"V = {values[1]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		
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
		max_value = Text(f"V = {values[2]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Write(max_value),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		

		item_3_copy = objects[3].copy()
		self.play(objects[3].animate.scale(5).move_to(suitcase.get_center() + UP + RIGHT*0.5))
		
		suitcase_weight_2 = Text(f"W = {weights[2]+weights[3]}/10 kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
		max_value_2 = Text(f"V = {values[2]+values[3]}", font_size=24, color=GREEN).move_to(suitcase_weight.get_center() + DOWN*0.5)
		self.play(
			Transform(max_value, max_value_2),
			Transform(suitcase_weight, suitcase_weight_2)
		)
		self.wait(5)