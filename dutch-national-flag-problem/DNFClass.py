from manim import *
import colorsys

class Sorter:
	def __init__(self, elements, position, num_colors, colours=[], type="nums"):
		self.elements = elements
		self.sorted_elements = sorted(self.elements)
		self.position = position

		self.scene_elems = VGroup()
		self.scene_sorted_elems = VGroup()
		self.num_colors = num_colors

		if len(colours) == 0:
			self.colours = self.generate_colors(self.num_colors)
		else:
			self.colours = colours

		self.init_elems(type=type)
		

	def get_elements(self):
		return self.elements


	def get_scene_elements(self):
		return self.scene_elems


	def get_scene_sorted_elements(self):
		return self.scene_elems


	def get_element(self, i):
		return self.elements[i]


	def get_scene_element(self, i):
		return self.scene_elems[i]


	def get_sorted_element(self, i):
		return self.sorted_elements[i]


	def get_num_elements(self):
		return len(self.get_elements())


	def add_element(self, e):
		self.scene_elems.add(e)		


	def add_sorted_element(self, e):
		self.scene_sorted_elems.add(e)


	def get_grade(self, i): 
		if i == 1:
			return "F"
		elif i == 2:
			return "P"
		else:
			return "H"


	def init_elems(self, type=type):
		self.scene_elems = VGroup()
		self.scene_sorted_elems = VGroup()

		self.add_element(Text("["))		
		self.add_sorted_element(Text("["))

		for i in range(0, self.get_num_elements()):
			if type == "balls":
				new_elem = Dot(radius=0.3)
				s_elem = Dot(radius=0.3)

			elif type == "students":
				sid = Text(str(i+1))
				grade = Text(self.get_grade(self.get_element(i))).next_to(sid, DOWN)
				new_elem = VGroup(sid, grade)

				sid2 = Text(str(i+1))
				grade2 = Text(self.get_grade(self.get_sorted_element(i))).next_to(sid, DOWN)
				s_elem = VGroup(sid2, grade2)

			else:
				new_elem = Text(str(self.get_element(i)))
				s_elem = Text(str(self.get_sorted_element(i)))

			new_elem = new_elem.set_color(self.colours[self.get_element(i)-1]).next_to(self.scene_elems[i], buff=0.5)
			self.add_element(new_elem)

			s_elem = s_elem.set_color(self.colours[self.get_sorted_element(i)-1]).next_to(self.scene_sorted_elems[i], buff=0.5)
			self.add_sorted_element(s_elem)

		self.add_element(Text("]").next_to(self.scene_elems[-1]))
		self.add_sorted_element(Text("]").next_to(self.scene_sorted_elems[-1]))

		self.scene_elems.move_to(self.position)
		self.scene_sorted_elems.move_to(self.position)


	def create_list(self, scene):
		scene.play(Create(self.scene_elems))


	def create_sorted_list(self, scene):
		scene.play(Create(self.scene_sorted_elems))


	def add_list_to_screen(self, scene, array, position):
		elems = VGroup()

		elems.add(Text("["))

		for i in range(0, len(array)):			
			new_elem = Text(str(array[i])).set_color(self.colours[array[i]-1]).next_to(elems[i])
			elems.add(new_elem)

		elems.add(Text("]").next_to(elems[-1]))

		elems.move_to(position)
		scene.play(Create(elems))


	def generate_colors(self, n):
		colors = []
		for i in range(n):
			hue = (i / n)

			# Convert HSL to RGB, then format as a hex string
			# Full saturation, medium lightness
			rgb = colorsys.hls_to_rgb(hue, 0.5, 0.5)  
			hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
			colors.append(hex_color)

		return colors 


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

		tmp = self.scene_elems[i+1]
		self.scene_elems[i+1] = self.scene_elems[j+1]
		self.scene_elems[j+1] = tmp


	def perform_algorithm(self, scene, show_arrow=True, run_time=1):	

		l = 0
		m = 0
		h = len(self.get_elements())-1

		low = Arrow(start=DOWN, end=ORIGIN, color=RED, stroke_width=8).next_to(self.get_scene_elements()[l+1], DOWN+LEFT*0.05, buff=0.2)
		mid = Arrow(start=DOWN, end=ORIGIN, color=GREEN, stroke_width=8).next_to(self.get_scene_elements()[m+1], DOWN, buff=0.2)
		high = Arrow(start=DOWN, end=ORIGIN, color=BLUE, stroke_width=8).next_to(self.get_scene_elements()[h+1], DOWN, buff=0.2)

		if show_arrow:
			scene.play(FadeIn(low))
			scene.play(FadeIn(mid))
			scene.play(FadeIn(high))
			scene.wait(2)

		middle = 2

		while m <= h:
			if self.get_element(m) == middle:
				m += 1

			elif self.get_element(m) > middle:
				tmp = self.elements[m]
				self.elements[m] = self.elements[h]
				self.elements[h] = tmp

				self.animate_swap(scene, m, h, run_time=run_time)

				h -= 1;

			elif self.get_element(m) < middle:
				tmp = self.elements[l]
				self.elements[l] = self.elements[m]
				self.elements[m] = tmp

				self.animate_swap(scene, l, m, run_time=run_time)

				l += 1
				m += 1

			if show_arrow and m <= h:
				if l == m:
					scene.play(
						mid.animate.next_to(self.get_scene_element(m+1), DOWN, buff=0.2),
						run_time=run_time
					)
					scene.play(
						low.animate.next_to(mid.get_center(), LEFT*0.4, buff=0.2),
						high.animate.next_to(self.get_scene_element(h+1), DOWN, buff=0.2),
						run_time=run_time
					)
				else:
					scene.play(
						low.animate.next_to(self.get_scene_element(l+1), DOWN, buff=0.2),
						mid.animate.next_to(self.get_scene_element(m+1), DOWN, buff=0.2),
						high.animate.next_to(self.get_scene_element(h+1), DOWN, buff=0.2),
						run_time=run_time
					)

				scene.wait(2)


	def fade_out(self, scene):
		scene.play(FadeOut(self.get_scene_elements()), FadeOut(self.get_scene_sorted_elements()))

