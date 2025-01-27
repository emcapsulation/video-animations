from manim import *
from DNFClass import Sorter

config.background_color = "#15131c"


class Introduction(Scene):
	def construct(self):
		Text.set_default(font="Consolas")


		l = [5, 2, 12, 7, 11, 4, 1, 3, 9, 6, 10, 8]
		s = Sorter(l, ORIGIN, len(l))
		s.create_list(self)
		self.wait(3)

		self.play(Transform(s.scene_elems, s.scene_sorted_elems))
		time_complexity = Text("Time complexity: O(nlog(n))", font_size=24).shift(UP)       
		self.play(Write(time_complexity), run_time=2)

		self.wait(3)
		s.fade_out(self)

		l = [3, 1, 1, 2, 2, 1, 3, 2, 3, 1, 3, 2]
		s = Sorter(l, ORIGIN, 3, colours=[GOLD, GREEN, TEAL])
		s.create_list(self)
		self.wait(3)		

		time_complexity_2 = Text("Time complexity: O(n)", font_size=24).shift(UP) 
		self.play(Transform(s.scene_elems, s.scene_sorted_elems), Transform(time_complexity, time_complexity_2))
		self.play(time_complexity[20:].animate.set_color(GREEN))
		self.wait(3)

		title_text = Text("Dutch National Flag Problem").shift(UP*3)
		self.play(Write(title_text))

		time_complexity_3 = Text("Time complexity: O(n), Space complexity: O(1)", font_size=24).shift(UP*2)       
		self.play(Transform(time_complexity, time_complexity_3), run_time=2)
		self.play(time_complexity[15:19].animate.set_color(GREEN),
		    time_complexity[36:40].animate.set_color(GREEN))
		self.wait(3)

		dot1 = Dot(color=s.colours[0], radius=0.5).move_to(DOWN*2+LEFT*2)
		dot2 = Dot(color=s.colours[1], radius=0.5).move_to(DOWN*2)
		dot3 = Dot(color=s.colours[2], radius=0.5).move_to(DOWN*2+RIGHT*2)
		dots = VGroup(dot1, dot2, dot3)

		self.play(Create(dots))
		self.wait(3)

		s.fade_out(self)
		self.play(FadeOut(dots))

		s = Sorter([3, 1, 2, 2, 1, 3, 2, 1, 1, 3, 3, 2], ORIGIN, 3, colours=["#AD1D25", WHITE, "#1E4785"], balls=True)
		s.create_list(self)
		self.wait(3)

		s.perform_algorithm(self, show_arrow=False, run_time=0.5)

		dnf = VGroup()
		red = Rectangle(width=3, height=2/3, stroke_width=0, fill_color="#AD1D25", fill_opacity=1)
		white = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=WHITE, fill_opacity=1).next_to(red.get_center(), DOWN*4/3)
		blue = Rectangle(width=3, height=2/3, stroke_width=0, fill_color="#1E4785", fill_opacity=1).next_to(white.get_center(), DOWN*4/3)

		dnf.add(red, white, blue)
		dnf.move_to(DOWN*2)
		self.play(FadeIn(dnf))

		self.wait(3)
		s.fade_out(self)
