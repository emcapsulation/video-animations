from manim import *

config.background_color = "#15131c"

class NaiveApproachDemo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "ABABABCAABABCAABABABABCAAB"		
		pattern = "ABABCAAB"
		fs = 30

		colour_map = {
			'A': TEAL,
			'B': BLUE,
			'C': PURPLE
		}

		problem = Text("Find all occurrences of the pattern in the longer text.", font_size=20, t2c={"pattern": TEAL, "text": PURPLE}).move_to(UP*3)

		text_group = VGroup(*[Text(c, font_size=fs, color=colour_map[c]) for c in text]).arrange(RIGHT, buff=0.3).move_to(UP*0.5)
		pattern_group = VGroup(*[Text(c, font_size=fs, color=colour_map[c]) for c in pattern]).arrange(RIGHT, buff=0.3)
		pattern_group.next_to(text_group, DOWN, buff=0.5).align_to(text_group[0], LEFT)

		self.play(Write(pattern_group))
		self.wait(2)

		self.play(Write(text_group), Write(problem))
		self.wait(2)


		match_text = Text("Match Indexes: ", font_size=fs).move_to(DOWN*3)
		match_group = VGroup(match_text)
		matches = []

		n, m = len(text), len(pattern)

		index_group = VGroup(*[Text(str(i), font_size=20).next_to(text_group[i], UP) for i in range(n)])
		self.play(AddTextLetterByLetter(index_group))
		self.wait(2)

		self.play(Write(match_text))
		for start in range(0, n-m+1):
			self.play(pattern_group.animate.align_to(text_group[start], LEFT))
			self.wait(0.5)

			match = (text[start:start+m] == pattern)
			colour = GREEN if match else RED

			self.play(
				*[Indicate(text_group[j], color=colour) for j in range(start, start+m)], 
				*[Indicate(pattern_group[j], color=colour) for j in range(0, m)]
			)

			if match:
				this_match = Text(str(start), font_size=fs).next_to(match_group[len(match_group)-1], RIGHT, buff=0.5)
				index_copy = index_group[start].copy()

				self.play(ReplacementTransform(index_copy, this_match))
				match_group.add(this_match)
				matches.append(start)
				self.play(match_group.animate.arrange(RIGHT, buff=0.5).move_to(DOWN*3))

		self.wait(2)


		self.play(
			text_group.animate.set_color(WHITE),
			pattern_group.animate.set_color(WHITE)
		)
		self.wait(2)


		for match in matches:
			self.play(pattern_group.animate.align_to(text_group[match], LEFT))

			self.play(
				*[Indicate(text_group[j], color=colour) for j in range(match, match+m)], 
				*[Indicate(pattern_group[j], color=colour) for j in range(0, m)]
			)
		self.wait(2)



class NaiveApproachCode(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		text = "ABABABCAABABCAABABABABCAAB"		
		pattern = "ABABCAAB"
		n, m = len(text), len(pattern)
		fs = 16


		text_group = VGroup(*[Text(c, font_size=fs) for c in text]).arrange(RIGHT, buff=0.15).to_edge(LEFT).shift(UP*2)
		pattern_group = VGroup(*[Text(c, font_size=fs) for c in pattern]).arrange(RIGHT, buff=0.15)
		pattern_group.next_to(text_group, DOWN, buff=2).align_to(text_group[0], LEFT)
		index_group = VGroup(*[Text(str(i), font_size=10).next_to(text_group[i], UP) for i in range(n)])

		match_text = Text("Match Indexes: ", font_size=fs).move_to(LEFT*3.25 + DOWN*3.5)
		match_group = VGroup(match_text)

		self.play(Write(pattern_group), AddTextLetterByLetter(text_group), AddTextLetterByLetter(index_group))
		self.play(Write(match_group))
		self.wait(2)


		START_COLOUR = ORANGE
		P1_COLOUR = LIGHT_PINK
		P2_COLOUR = TEAL


		start_arrow = Arrow(
			start=index_group[0].get_center() + UP,
			end=index_group[0].get_center()
		)
		start_text = Text("start", font_size=16, color=START_COLOUR)
		start_group = VGroup(start_text, start_arrow).arrange(DOWN).move_to(index_group[0].get_center()+UP)


		start = 0
		start_rect = RoundedRectangle(
			width=2, height=1,
			corner_radius=0.3,
			stroke_width=4,
			stroke_color=WHITE
		).move_to(DOWN*2.5 + LEFT*5.75)

		rect_text_start = MarkupText(f"""<span fgcolor="{START_COLOUR}">start</span>: """, font_size=20, font="Monospace")
		rect_val_start = MarkupText(f"""{start}""", font_size=20, font="Monospace").next_to(rect_text_start, RIGHT, buff=0.2)
		start_text_2 = VGroup(rect_text_start, rect_val_start).move_to(start_rect.get_center())


		p1_arrow = Arrow(
			start=text_group[0].get_center() + DOWN,
			end=text_group[0].get_center()
		)
		p1_text = Text("p1", font_size=16, color=P1_COLOUR)
		p1_group = VGroup(p1_arrow, p1_text).arrange(DOWN).move_to(text_group[0].get_center()+DOWN)


		p1 = start
		p1_rect = RoundedRectangle(
			width=2, height=1,
			corner_radius=0.3,
			stroke_width=4,
			stroke_color=WHITE
		).move_to(DOWN*2.5 + LEFT*3.25)

		rect_text_p1 = MarkupText(f"""T[<span fgcolor="{P1_COLOUR}">p1</span>]: """, font_size=20, font="Monospace")
		rect_val_p1 = MarkupText(f"""{text[p1]}""", font_size=20, font="Monospace").next_to(rect_text_p1, RIGHT, buff=0.2)
		p1_text_2 = VGroup(rect_text_p1, rect_val_p1).move_to(p1_rect.get_center())


		p2_arrow = Arrow(
			start=pattern_group[0].get_center() + DOWN,
			end=pattern_group[0].get_center()
		)
		p2_text = Text("p2", font_size=16, color=P2_COLOUR)
		p2_group = VGroup(p2_arrow, p2_text).arrange(DOWN).move_to(pattern_group[0].get_center()+DOWN)


		p2 = 0
		p2_rect = RoundedRectangle(
			width=2, height=1,
			corner_radius=0.3,
			stroke_width=4,
			stroke_color=WHITE
		).move_to(DOWN*2.5 + LEFT*0.75)

		rect_text_p2 = MarkupText(f"""P[<span fgcolor="{P2_COLOUR}">p2</span>]: """, font_size=20, font="Monospace")
		rect_val_p2 = MarkupText(f"""{pattern[p2]}""", font_size=20, font="Monospace").next_to(rect_text_p2, RIGHT, buff=0.2)
		p2_text_2 = VGroup(rect_text_p2, rect_val_p2).move_to(p2_rect.get_center())


		self.play(Create(start_group), Create(start_rect), Write(start_text_2))
		self.wait(2)

		self.play(Create(p1_group), Create(p1_rect), Write(p1_text_2))
		self.wait(2)

		self.play(Create(p2_group), Create(p2_rect), Write(p2_text_2))
		self.wait(2)


		
		for start in range(0, n-m+1):
			p1, p2 = start, 0

			rect_val_start = MarkupText(f"""{start}""", font_size=20, font="Monospace").move_to(start_text_2[1].get_center())	
			self.play(
				start_group.animate.move_to(index_group[start].get_center()+UP),
				Transform(start_text_2[1], rect_val_start), 
				pattern_group.animate.align_to(text_group[start], LEFT)
			)

			

			while p2 < m and text[p1] == pattern[p2]:
				rect_val_p1 = MarkupText(f"""{text[p1]}""", font_size=20, font="Monospace").move_to(p1_text_2[1].get_center())
				rect_val_p2 = MarkupText(f"""{pattern[p2]}""", font_size=20, font="Monospace").move_to(p2_text_2[1].get_center())

				self.play(
					p1_group.animate.move_to(text_group[p1].get_center()+DOWN),
					p2_group.animate.move_to(pattern_group[p2].get_center()+DOWN)
				)			
				self.play(
					Transform(p1_text_2[1], rect_val_p1),
					Transform(p2_text_2[1], rect_val_p2),
					text_group[p1].animate.set_color(GREEN),
					pattern_group[p2].animate.set_color(GREEN)
				)

				p1 += 1
				p2 += 1

				
			if p2 == m:
				self.play(
					p1_group.animate.shift(RIGHT*0.2),
					p2_group.animate.shift(RIGHT*0.2)
				)

				this_match = Text(str(start), font_size=fs).next_to(match_group[len(match_group)-1], RIGHT, buff=0.5)
				index_copy = index_group[start].copy()

				self.play(ReplacementTransform(index_copy, this_match))
				match_group.add(this_match)
				self.play(match_group.animate.arrange(RIGHT, buff=0.5).move_to(LEFT*3.25 + DOWN*3.5))

			else:
				rect_val_p1 = MarkupText(f"""{text[p1]}""", font_size=20, font="Monospace").move_to(p1_text_2[1].get_center())
				rect_val_p2 = MarkupText(f"""{pattern[p2]}""", font_size=20, font="Monospace").move_to(p2_text_2[1].get_center())

				self.play(
					p1_group.animate.move_to(text_group[p1].get_center()+DOWN),
					p2_group.animate.move_to(pattern_group[p2].get_center()+DOWN)
				)			
				self.play(
					Transform(p1_text_2[1], rect_val_p1),
					Transform(p2_text_2[1], rect_val_p2),
					text_group[p1].animate.set_color(RED),
					pattern_group[p2].animate.set_color(RED)
				)

			self.wait(2)
			self.play(text_group.animate.set_color(WHITE), pattern_group.animate.set_color(WHITE))

				
