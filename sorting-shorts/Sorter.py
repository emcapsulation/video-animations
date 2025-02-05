from manim import *
import colorsys

class Sorter:
	def __init__(self, elements, position, mf, colours=[], type="nums"):
		self.elements = elements
		self.position = position

		# The Midi file
		self.mf = mf

		self.scene_elems = VGroup()

		if len(colours) == 0:
			self.colours = self.generate_colors()
		else:
			self.colours = colours

		self.init_elems(type=type)
		

	def get_elements(self):
		return self.elements


	def get_element(self, i):
		return self.elements[i]


	def get_scene_elements(self):
		return self.scene_elems


	def get_scene_element(self, i):
		return self.scene_elems[i]


	def get_num_elements(self):
		return len(self.get_elements())


	def get_num_scene_elements(self):
		return len(self.get_scene_elements())


	def add_element(self, e):
		self.scene_elems.add(e)		


	def init_elems(self, type=type):
		self.scene_elems = VGroup()
		self.add_element(Text("["))		

		for i in range(0, self.get_num_elements()):
			if type == "balls":
				new_elem = Dot(radius=0.3)
			elif type == "nums":
				new_elem = Text(str(self.get_element(i)))

			new_elem = new_elem.set_color(self.colours[self.get_element(i)-1]).next_to(self.scene_elems[i], buff=0.5)
			self.add_element(new_elem)

		self.add_element(Text("]").next_to(self.scene_elems[-1]))
		self.scene_elems.move_to(self.position)


	def create_list(self, scene, scale=1):
		scene.play(Create(self.scene_elems.scale(scale)), run_time=1)

		for i in self.get_scene_elements():
			if i.get_text() == '[' or i.get_text() == ']':
				self.mf.write_pause(1/self.get_num_scene_elements())
			else:
				self.mf.write_int(int(i.get_text()), 1/self.get_num_scene_elements())


	def generate_colors(self):
		min_elem = min(self.elements)
		max_elem = max(self.elements)
		num_colors = max_elem-min_elem+1

		colors = [None]*self.get_num_elements()
		for e in self.elements:
			hue = ((e-min_elem) / num_colors)

			# Convert HSL to RGB, then format as a hex string
			rgb = colorsys.hls_to_rgb(hue, 0.5, 1)  
			hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
			colors[e-1] = hex_color

		return colors 


	def animate_last_pass(self, scene, p1_arrow, p2_arrow, run_time):
		for p in range(0, self.get_num_elements()):
			scene.play(p1_arrow.animate.next_to(self.get_scene_element(p+1), DOWN, buff=0.2), 
				p2_arrow.animate.next_to(self.get_scene_element(p+1), DOWN, buff=0.2), run_time=run_time*0.1)
			self.mf.write_int(self.get_element(p), run_time*0.1)

			p += 1


	def animate_swap(self, scene, i, j, run_time):
		i_pos = self.get_scene_element(i+1).get_center()
		j_pos = self.get_scene_element(j+1).get_center()

		path = Line(i_pos, j_pos)
		path.points[1:3] += UP*1

		path2 = Line(j_pos, i_pos)
		path2.points[1:3] += DOWN*1

		scene.play(
			MoveAlongPath(self.get_scene_element(i+1), path),
			MoveAlongPath(self.get_scene_element(j+1), path2),
			run_time=run_time
		)
		self.mf.write_chord(
			[int(self.get_scene_element(i+1).get_text()), int(self.get_scene_element(j+1).get_text())], 
			run_time
		)

		tmp = self.scene_elems[i+1]
		self.scene_elems[i+1] = self.scene_elems[j+1]
		self.scene_elems[j+1] = tmp


	def selection_sort(self, scene, run_time=1):
		p1_col = MAROON_B
		p2_col = TEAL_B

		p1 = 0
		p2 = p1

		p1_arrow = Arrow(start=DOWN, end=ORIGIN, color=p1_col, stroke_width=8).next_to(self.get_scene_elements()[p1+1], DOWN, buff=0.2)
		p2_arrow = Arrow(start=DOWN, end=ORIGIN, color=p2_col, stroke_width=8).next_to(self.get_scene_elements()[p2+1], DOWN, buff=0.2)

		tutorial_text = MarkupText(f"""initialise <span fgcolor="{p1_col}">p1</span> = 0""", 
			font_size=24, font="Consolas").shift(UP)
		scene.play(Write(tutorial_text), run_time=run_time)
		self.mf.write_pause(run_time)

		rect_shape = RoundedRectangle(
			width=2.5, height=1.5,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)
		rect_text = Text("min", font_size=24).move_to(rect_shape.get_center()).shift(UP*0.25)
		rect_num = Text("", font_size=30).move_to(rect_shape.get_center()).shift(DOWN*0.25)
		rect = VGroup(rect_shape, rect_text, rect_num).move_to(DOWN*0.5).scale(0.9)

		rect_drawn = False
		

		for p1 in range(0, self.get_num_elements()):
			p2 = p1			

			scene.play(
				p1_arrow.animate.next_to(self.get_scene_element(p1+1), DOWN, buff=0.2),
				run_time=run_time
			)
			self.mf.write_int(self.get_element(p1), run_time)

			scene.play(
				p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
				Transform(tutorial_text, 
					MarkupText(f"""set <span fgcolor="{p2_col}">p2</span> = <span fgcolor="{p1_col}">p1</span>""", 
						font_size=24, font="Consolas").shift(UP)),
				run_time=run_time
			)
			self.mf.write_int(self.get_element(p2), run_time)

			min_elem = self.get_element(p2)
			min_p2 = p2

			new_rect_num = Text(str(self.get_element(p2)), 
				font_size=30).set_color(self.colours[self.get_element(p2)-1]).move_to(rect_shape.get_center()).shift(DOWN*0.25)

			if not rect_drawn:			
				scene.play(Transform(tutorial_text, 
					MarkupText(f"""<span fgcolor="{p2_col}">p2</span> finds min""",
						font_size=24, font="Consolas").shift(UP)),
					Create(rect_shape), Write(rect_text), Transform(rect_num, new_rect_num), run_time=run_time)

				self.mf.write_pause(run_time)	
				rect_drawn = True	

			else:
				scene.play(Transform(tutorial_text, 
					MarkupText(f"""<span fgcolor="{p2_col}">p2</span> finds min""",
						font_size=24, font="Consolas").shift(UP)), 
					Transform(rect_num, new_rect_num), run_time=run_time)

				self.mf.write_pause(run_time)	


			for p2 in range(p1+1, self.get_num_elements()):
				if self.get_element(p2) < min_elem:
					min_elem = self.get_element(p2)
					min_p2 = p2

					new_rect_num = Text(str(self.get_element(p2)), 
						font_size=30).set_color(self.colours[self.get_element(p2)-1]).move_to(rect_shape.get_center()).shift(DOWN*0.25)

					scene.play(
						Transform(rect_num, new_rect_num),
						p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
						run_time=run_time*0.1
					)	
					self.mf.write_int(self.get_element(p2), run_time*0.1)

				else:
					scene.play(
						p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
						run_time=run_time*0.1
					)		
					self.mf.write_int(self.get_element(p2), run_time*0.1)


			scene.play(Transform(tutorial_text, 
				MarkupText(f"""swap min with <span fgcolor="{p1_col}">p1</span>""", 
					font_size=24, font="Consolas").shift(UP)), run_time=run_time)
			self.mf.write_pause(run_time)	

			tmp = self.elements[p1]
			self.elements[p1] = self.elements[min_p2]
			self.elements[min_p2] = tmp

			self.animate_swap(scene, p1, min_p2, run_time=run_time)			

			if p1 < self.get_num_elements()-1:
				scene.play(Transform(tutorial_text, 
					MarkupText(f"""increment <span fgcolor="{p1_col}">p1</span>""", 
						font_size=24, font="Consolas").shift(UP)), run_time=run_time)

				self.mf.write_pause(run_time)

			else:
				scene.play(Transform(tutorial_text, 
					MarkupText(f"""sorted :)""", 
						font_size=24, font="Consolas").shift(UP)), run_time=run_time)

				self.mf.write_pause(run_time)


		self.animate_last_pass(scene, p1_arrow, p2_arrow, run_time)


	def bubble_sort(self, scene, run_time=1):
		self.mf.write_pause(run_time*0.2)

		p1_col = MAROON_B
		p2_col = TEAL_B

		p1 = 0
		p2 = 1

		p1_arrow = Arrow(start=DOWN, end=ORIGIN, color=p1_col, stroke_width=8).next_to(self.get_scene_elements()[p1+1], DOWN, buff=0.2)
		p2_arrow = Arrow(start=DOWN, end=ORIGIN, color=p2_col, stroke_width=8).next_to(self.get_scene_elements()[p2+1], DOWN, buff=0.2)	


		rect_shape = RoundedRectangle(
			width=2.5, height=1.5,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)

		rect_text_p1 = MarkupText(f"""<span fgcolor="{p1_col}">p1</span>: """, font_size=24, font="Consolas")
		rect_p1 = MarkupText(f"""0""", font_size=24, font="Consolas").set_color("#15131c").next_to(rect_text_p1, RIGHT, buff=0.2)
		p1_text = VGroup(rect_text_p1, rect_p1).move_to(rect_shape.get_center()).shift(UP*0.25)

		rect_text_p2 = MarkupText(f"""<span fgcolor="{p2_col}">p2</span>: """, font_size=24, font="Consolas")
		rect_p2 = MarkupText(f"""0""", font_size=24, font="Consolas").set_color("#15131c").next_to(rect_text_p2, RIGHT, buff=0.2)
		p2_text = VGroup(rect_text_p2, rect_p2).move_to(rect_shape.get_center()).shift(DOWN*0.25)

		rect = VGroup(rect_shape, p1_text, p2_text).move_to(DOWN*0.5).scale(0.9)
		rect_drawn = False	


		tutorial_text = MarkupText(f"""""", font_size=24, font="Consolas").shift(UP)


		while True:
			swapped = False	

			for p2 in range(1, self.get_num_elements()):
				p1 = p2-1		

				new_p1 = Text(str(self.get_element(p1)), 
					font_size=24).set_color(self.colours[self.get_element(p1)-1]).next_to(rect_text_p1, RIGHT, buff=0.2)
				new_p2 = Text(str(self.get_element(p2)), 
					font_size=24).set_color(self.colours[self.get_element(p2)-1]).next_to(rect_text_p2, RIGHT, buff=0.2)


				if not rect_drawn:			
					scene.play(Transform(tutorial_text, 
						MarkupText(f"""set <span fgcolor="{p1_col}">p1</span> = 0, <span fgcolor="{p2_col}">p2</span> = 1""",
							font_size=24, font="Consolas").shift(UP)),
						p1_arrow.animate.next_to(self.get_scene_element(p1+1), DOWN, buff=0.2),
						p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
						Create(rect_shape), 
						Write(rect_text_p1), Transform(rect_p1, new_p1), 
						Write(rect_text_p2), Transform(rect_p2, new_p2), 
						run_time=run_time*2)

					self.mf.write_int(self.get_element(p1), run_time*2)
					rect_drawn = True	

				else:
					if p1 == 0:
						scene.play(Transform(tutorial_text, 
							MarkupText(f"""reset <span fgcolor="{p1_col}">p1</span> = 0, <span fgcolor="{p2_col}">p2</span> = 1""",
								font_size=24, font="Consolas").shift(UP)),
							p1_arrow.animate.next_to(self.get_scene_element(p1+1), DOWN, buff=0.2),
							p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
							Transform(rect_p1, new_p1), 
							Transform(rect_p2, new_p2), 						
							run_time=run_time)

						# Delay because the arrow has a long way to go
						self.mf.write_pause(run_time*0.8)
						self.mf.write_int(self.get_element(p1), run_time*0.2)

					else:
						scene.play(Transform(tutorial_text, 
							MarkupText(f"""swap if <span fgcolor="{p1_col}">p1</span> &gt; <span fgcolor="{p2_col}">p2</span>""",
								font_size=24, font="Consolas").shift(UP)),
							p1_arrow.animate.next_to(self.get_scene_element(p1+1), DOWN, buff=0.2),
							p2_arrow.animate.next_to(self.get_scene_element(p2+1), DOWN, buff=0.2),
							Transform(rect_p1, new_p1), 
							Transform(rect_p2, new_p2), 						
							run_time=run_time*0.2)

						self.mf.write_int(self.get_element(p1), run_time*0.2)


				if self.get_element(p1) > self.get_element(p2):
					swapped = True

					tmp = self.elements[p1]
					self.elements[p1] = self.elements[p2]
					self.elements[p2] = tmp

					self.animate_swap(scene, p1, p2, run_time=run_time)


			if not swapped:
				scene.play(Transform(tutorial_text, 
					MarkupText(f"""no more swaps detected""",
						font_size=24, font="Consolas").shift(UP)), run_time=run_time)

				self.mf.write_pause(run_time)	
				break


		self.animate_last_pass(scene, p1_arrow, p2_arrow, run_time)

		scene.play(Transform(tutorial_text, 
			MarkupText(f"""sorted :)""", 
				font_size=24, font="Consolas").shift(UP)), run_time=run_time)
		self.mf.write_pause(run_time)


	def fade_out(self, scene):
		scene.play(FadeOut(self.get_scene_elements()))

