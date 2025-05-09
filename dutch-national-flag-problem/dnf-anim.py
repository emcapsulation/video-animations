from manim import *
from DNFClass import Sorter

config.background_color = "#15131c"

VERM_RED = "#AE1C28"
COB_BLUE = "#21468B"


def create_psuedocode(scene):
	code_rect = RoundedRectangle(width=7, height=4.5, fill_color=BLACK, fill_opacity=1, stroke_width=0, corner_radius=0.3)
	code = MarkupText(f"""<span fgcolor="{RED}">low</span> = 0
<span fgcolor="{GREEN}">mid</span> = 0
<span fgcolor="{BLUE}">high</span> = length of nums - 1

while <span fgcolor="{GREEN}">mid</span> &lt;= <span fgcolor="{BLUE}">high</span>:
	if nums[<span fgcolor="{GREEN}">mid</span>] == middle element:
		increment <span fgcolor="{GREEN}">mid</span>

	else if nums[<span fgcolor="{GREEN}">mid</span>] &gt; middle element:
		swap values at <span fgcolor="{GREEN}">mid</span> and <span fgcolor="{BLUE}">high</span>
		decrement <span fgcolor="{BLUE}">high</span>

	else if nums[<span fgcolor="{GREEN}">mid</span>] &lt; middle element:
		swap values at <span fgcolor="{RED}">low</span> and <span fgcolor="{GREEN}">mid</span>
		increment <span fgcolor="{RED}">low</span>, increment <span fgcolor="{GREEN}">mid</span>""", font_size=16, font="Monospace").move_to(code_rect.get_center())	

	pseudocode = VGroup(code_rect, code).scale(0.8).move_to(LEFT*4 + DOWN)
	scene.play(Create(pseudocode), run_time=2)
	scene.wait(3)	

	return pseudocode	



class Introduction(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

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

		dnf = VGroup()
		red = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=VERM_RED, fill_opacity=1)
		white = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=WHITE, fill_opacity=1).next_to(red.get_center(), DOWN*4/3)
		blue = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=COB_BLUE, fill_opacity=1).next_to(white.get_center(), DOWN*4/3)

		dnf.add(red, white, blue)
		dnf.move_to(DOWN*2)
		self.play(FadeIn(dnf))
		self.wait(3)

		s = Sorter([3, 1, 2, 2, 1, 3, 2, 1, 1, 3, 3, 2], UP*0.5, 3, colours=[VERM_RED, WHITE, COB_BLUE], type="balls")
		s.get_scene_elements().scale(0.9)
		s.create_list(self)
		self.wait(3)

		s.perform_algorithm(self, show_arrow=False, run_time=0.5)		

		self.wait(3)
		s.fade_out(self)


class Walkthrough(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		# Pointer rectangles
		low_rect = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=RED
		)

		mid_rect = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=GREEN
		).next_to(low_rect, RIGHT, buff=1)

		high_rect = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=BLUE
		).next_to(mid_rect, RIGHT, buff=1)

		low_text = Text("low", font_size=24).move_to(low_rect.get_center()).shift(LEFT*0.25)
		mid_text = Text("mid", font_size=24).move_to(mid_rect.get_center()).shift(LEFT*0.25)
		high_text = Text("high", font_size=24).move_to(high_rect.get_center()).shift(LEFT*0.25)

		low_arrow = Arrow(start=DOWN, end=ORIGIN, color=RED, stroke_width=8).move_to(low_rect.get_center()).shift(RIGHT*0.5)
		mid_arrow = Arrow(start=DOWN, end=ORIGIN, color=GREEN, stroke_width=8).move_to(mid_rect.get_center()).shift(RIGHT*0.5)
		high_arrow = Arrow(start=DOWN, end=ORIGIN, color=BLUE, stroke_width=8).move_to(high_rect.get_center()).shift(RIGHT*0.5)

		rects = VGroup(low_rect, low_text, low_arrow, mid_rect, mid_text, mid_arrow, high_rect, high_text, high_arrow).move_to(UP*2)
		self.play(Create(rects), run_time=3)


		pseudocode = create_psuedocode(self)

		s = Sorter([2, 3, 1, 2, 3, 3, 2, 1, 1, 3, 2, 1], RIGHT*3 + DOWN, 3, colours=[VERM_RED, WHITE, COB_BLUE])
		s.get_scene_elements().scale(0.7)
		s.create_list(self)

		middle_text = Text("Middle element: 2", font_size=20).move_to(RIGHT*3)
		self.play(Write(middle_text))
		self.wait(3)

		s.perform_algorithm(self, show_arrow=True, run_time=2)		

		self.wait(3)
		s.fade_out(self)


class LargerExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		

		students = [1, 3, 1, 2, 1, 3, 1, 1, 2, 3, 2, 2, 1, 2]
		PURPLE = LIGHT_PINK

		s = Sorter(students, ORIGIN, 3, colours=[ORANGE, TEAL, PURPLE], type="students")
		s.get_scene_elements().scale(0.7)
		s.create_list(self)

		fail_text = Text("Fail", color=ORANGE, font_size=24).move_to(UP*3 + LEFT*5.5)
		pass_text = Text("Pass", color=TEAL, font_size=24).move_to(UP*3 + LEFT*1.25)
		honours_text = Text("Honours", color=PURPLE, font_size=24).move_to(UP*3 + RIGHT*3.5)
		grades = VGroup(fail_text, pass_text, honours_text)

		self.play(Write(fail_text))
		self.play(Write(pass_text))
		self.play(Write(honours_text))


		fail_group = VGroup(fail_text)
		pass_group = VGroup(pass_text)
		honours_group = VGroup(honours_text)

		# Animate moving the elements to the groups
		for i in range(0, len(students)):
			st = students[i]

			if st == 1:
				self.play(s.get_scene_element(i+1).animate.next_to(fail_group[-1], RIGHT))
				fail_group.add(s.get_scene_element(i+1))
			elif st == 2:				
				self.play(s.get_scene_element(i+1).animate.next_to(pass_group[-1], RIGHT))
				pass_group.add(s.get_scene_element(i+1))
			else:				
				self.play(s.get_scene_element(i+1).animate.next_to(honours_group[-1], RIGHT))
				honours_group.add(s.get_scene_element(i+1))


		self.wait(3)
		s.fade_out(self)

		self.play(
			fail_text.animate.move_to(UP*3 + LEFT*3), 
			pass_text.animate.move_to(UP*3), 
			honours_text.animate.move_to(UP*3 + RIGHT*3)
		)

		pseudocode = create_psuedocode(self)

		s = Sorter(students, DOWN+RIGHT*3, 3, colours=[ORANGE, TEAL, PURPLE], type="students")
		s.get_scene_elements().scale(0.5)
		s.create_list(self)

		s.perform_algorithm(self, show_arrow=True, run_time=2)		

		self.wait(3)
		s.fade_out(self)



class Explanation(Scene):
	def construct(self):
		Text.set_default(font="Monospace")	

		low_arrow = Arrow(start=DOWN, end=ORIGIN, color=RED, stroke_width=8).shift(UP*3 + LEFT*5)
		low_text = Text("- End of the low group", font_size=24).next_to(low_arrow, RIGHT, buff=1)
		mid_arrow = Arrow(start=DOWN, end=ORIGIN, color=GREEN, stroke_width=8).shift(UP*2 + LEFT*5)
		mid_text = Text("- End of the middle group", font_size=24).next_to(mid_arrow, RIGHT, buff=1)
		high_arrow = Arrow(start=DOWN, end=ORIGIN, color=BLUE, stroke_width=8).shift(UP + LEFT*5)
		high_text = Text("- Start of the high group", font_size=24).next_to(high_arrow, RIGHT, buff=1)

		arrow_text = VGroup(low_arrow, low_text, mid_arrow, mid_text, high_arrow, high_text).scale(0.8).move_to(ORIGIN + UP*2)

		self.play(Create(low_arrow), Write(low_text))
		self.wait(1)
		self.play(Create(mid_arrow), Write(mid_text))
		self.wait(1)
		self.play(Create(high_arrow), Write(high_text))

		balls = [1, 2, 3, 3, 1, 2, 3, 1, 3, 1, 3, 2, 2, 1, 2]
		s = Sorter(balls, DOWN, 3, colours=[VERM_RED, WHITE, COB_BLUE])
		s.get_scene_elements()
		s.create_list(self)

		s.perform_algorithm(self, show_arrow=True, run_time=2)		

		self.wait(3)
		s.fade_out(self)



class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font="Monospace")	

		title_text = Text("Dutch National Flag Problem").shift(UP*3)
		self.add(title_text)

		time_complexity_3 = Text("Time complexity: O(n), Space complexity: O(1)", font_size=24).shift(UP*2)    
		time_complexity_3[15:19].set_color(GREEN)   
		time_complexity_3[36:40].set_color(GREEN)
		self.add(time_complexity_3)

		dnf = VGroup()
		red = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=VERM_RED, fill_opacity=1)
		white = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=WHITE, fill_opacity=1).next_to(red.get_center(), DOWN*4/3)
		blue = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=COB_BLUE, fill_opacity=1).next_to(white.get_center(), DOWN*4/3)

		dnf.add(red, white, blue)
		dnf.move_to(DOWN*2)
		self.add(dnf)

		s = Sorter([3, 1, 2, 2, 1, 3, 2, 1, 1, 3, 3, 2], UP*0.5, 3, colours=[VERM_RED, WHITE, COB_BLUE], type="balls")
		self.add(s.scene_elems.scale(0.9))
