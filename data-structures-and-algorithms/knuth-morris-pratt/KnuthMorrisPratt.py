from manim import *


class KnuthMorrisPratt:
	STRING_BUFF = 0.3
	ARROW_SHIFT = 0.52

	STRING_GROUP_FS = 30
	MATCH_GROUP_FS = 24
	INDEX_GROUP_FS = 10
	ARROW_FS = 16

	TEXT_POSITION = UP*2
	PATTERN_POSITION = UP*1
	MATCH_POSITION = DOWN*1
	LPS_POSITION = DOWN*2
	HINT_POSITION = DOWN*3

	P1_COLOUR = ORANGE
	P2_COLOUR = LIGHT_PINK
	START_COLOUR = YELLOW
	PREFIX_COLOUR = TEAL
	SUFFIX_COLOUR = PURPLE


	def __init__(self, scene, pattern, text, spaced=False):
		self.scene = scene

		if spaced == True:
			KnuthMorrisPratt.PATTERN_POSITION = UP*0
			KnuthMorrisPratt.MATCH_POSITION = DOWN*2

		self.pattern = pattern
		self.text = text

		self.m = len(pattern)
		self.n = len(text)
		
		self.text_group = self.create_string_group(text).move_to(KnuthMorrisPratt.TEXT_POSITION)
		self.pattern_group = self.create_string_group(pattern).move_to(KnuthMorrisPratt.PATTERN_POSITION).align_to(self.text_group[0], LEFT)
		
		self.match_group = VGroup(
			Text("Match Indexes: ", font_size=KnuthMorrisPratt.MATCH_GROUP_FS).move_to(KnuthMorrisPratt.MATCH_POSITION)
		)

		self.lps = self.create_lps()


	def create_string_group(self, s):
		string = VGroup(*[Text(c, font_size=KnuthMorrisPratt.STRING_GROUP_FS) for c in s]).arrange(RIGHT, buff=KnuthMorrisPratt.STRING_BUFF)
		indexes = VGroup(*[Text(str(i), font_size=KnuthMorrisPratt.INDEX_GROUP_FS).next_to(string[i], UP) for i in range(len(s))])
		return VGroup(*[VGroup(indexes[i], string[i]) for i in range(0, len(string))])


	def create_arrow_group(self, label, colour, direction):
		arrow = Arrow(
			start=UP if direction == "down" else ORIGIN,
			end=ORIGIN if direction == "down" else UP
		).scale(0.5)
		label = Text(label, font_size=KnuthMorrisPratt.ARROW_FS, color=colour)
		return VGroup(label, arrow).arrange(DOWN if direction == "down" else UP)


	def create_lps(self):
		lps = [0]*self.m

		p1, p2 = 0, 1
		while p2 < self.m:
			if self.pattern[p1] == self.pattern[p2]:
				lps[p2] = p1+1
				p1 += 1
				p2 += 1
			else:
				if p1 > 0:
					p1 = lps[p1-1]
				else:
					lps[p2] = 0
					p2 += 1

		return lps



	def get_arrow_shift(self, p1, p2, p1_pos):
		anim_list = []

		if p1 == self.n:
			anim_list.append(self.p1_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))
		else:
			anim_list.append(self.p1_group.animate.move_to(self.text_group[p1].get_center()+p1_pos))

		if p2 == self.m:
			anim_list.append(self.p2_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))
		else:
			anim_list.append(self.p2_group.animate.move_to(self.pattern_group[p2].get_center()+DOWN))

		return anim_list



	def match_animation(self, match_index):
		this_match = (
			Text(
				str(match_index), font_size=KnuthMorrisPratt.MATCH_GROUP_FS
			).next_to(
				self.match_group[len(self.match_group)-1], RIGHT, buff=KnuthMorrisPratt.STRING_BUFF
			)
		)
		self.scene.play(
			ReplacementTransform(
				self.text_group[match_index][0].copy(), 
				this_match
			)
		)
		self.match_group.add(this_match)
		self.scene.play(self.match_group.animate.arrange(RIGHT, buff=0.5).move_to(KnuthMorrisPratt.MATCH_POSITION))



	def prefix_animation(self, p1, p2, show_lps, show_hints):
		if show_hints:
			hint = Text("Find longest overlap between the prefix of the pattern, and the suffix of the matched part.", 
				font_size=16).move_to(KnuthMorrisPratt.HINT_POSITION)
			self.scene.play(Write(hint))
			self.scene.wait(2)

		self.scene.play(
			*[self.pattern_group[i].animate.set_color(WHITE) for i in range(0, p2)], 
			*[self.text_group[i].animate.set_color(WHITE) for i in range(p1-p2, p1)]
		)

		if self.lps[p2-1] > 0:
			self.scene.play(
				*[self.pattern_group[i].animate.set_color(GREEN) for i in range(0, self.lps[p2-1])]
			)
			self.scene.play(			
				*[self.text_group[i].animate.set_color(GREEN) for i in range(p1-self.lps[p2-1], p1)]
			)
		self.scene.wait(2)

		if show_hints:
			prefix = ''.join([self.pattern_group[i][1].text for i in range(0, self.lps[p2-1])])
			hint_2 = Text(f"Move p2 to index {self.lps[p2-1]} - the {prefix} prefix of the pattern equals the {prefix} suffix in the matched part.", 
					font_size=16, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)
			
			if self.lps[p2-1] == 0:
				hint_2 = Text(f"Move p2 to index {self.lps[p2-1]} - there is no equal prefix in the pattern and suffix in the matched part.", 
					font_size=16, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)

			if show_lps:
				hint_2 = Text("Set p2 = lps[p2-1].", 
					font_size=16).move_to(KnuthMorrisPratt.HINT_POSITION)

			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(2)

		if show_lps:
			self.scene.play(Flash(self.lps_group[p2-1][1]))

		if show_hints:
			self.scene.play(FadeOut(hint))



	def show_naive_approach(self, speed, pause_at=-1):
		n, m = self.n, self.m


		self.scene.play(Create(self.pattern_group))
		self.scene.wait(2)

		self.scene.play(Create(self.text_group))
		self.scene.wait(2)

		self.scene.play(Create(self.match_group))
		self.scene.wait(2)


		# 'fast' mode doesn't include the pointers
		self.start_group, self.p1_group, self.p2_group = None, None, None
		if speed == "slow":
			self.start_group = self.create_arrow_group("start", KnuthMorrisPratt.START_COLOUR, "down").move_to(self.text_group[0].get_center()+UP)
			self.p1_group = self.create_arrow_group("p1", KnuthMorrisPratt.P1_COLOUR, "up").move_to(self.text_group[0].get_center()+DOWN)
			self.p2_group = self.create_arrow_group("p2", KnuthMorrisPratt.P2_COLOUR, "up").move_to(self.pattern_group[0].get_center()+DOWN)

			self.scene.play(Create(self.start_group))
			self.scene.wait(2)

			self.scene.play(Create(self.p1_group))
			self.scene.wait(2)

			self.scene.play(Create(self.p2_group))
			self.scene.wait(2)


		for start in range(0, n-m+1):
			p1, p2 = start, 0

			anim_list = [self.pattern_group.animate.align_to(self.text_group[start], LEFT)]
			if speed == "slow":
				anim_list.append(self.start_group.animate.move_to(self.text_group[start].get_center()+UP))
			self.scene.play(*anim_list)
			self.scene.wait(1)

			if pause_at == start:
				self.scene.wait(2)
				break

			while p2 < m and self.text[p1] == self.pattern[p2]:
				if speed == "slow":
					self.scene.play(
						self.p1_group.animate.move_to(self.text_group[p1].get_center()+DOWN),
						self.p2_group.animate.move_to(self.pattern_group[p2].get_center()+DOWN)
					)			
					self.scene.play(
						self.text_group[p1].animate.set_color(GREEN),
						self.pattern_group[p2].animate.set_color(GREEN)
					)

				p1 += 1
				p2 += 1


			if speed == "slow":
				anim_list = self.get_arrow_shift(p1, p2, DOWN)
				self.scene.play(*anim_list)


			if p2 == m:
				# There is a match at start
				self.scene.play(
					*[Indicate(self.text_group[j], color=GREEN) for j in range(start, start+m)], 
					*[Indicate(self.pattern_group[j], color=GREEN) for j in range(0, m)]
				)

				self.match_animation(start)

				
			else:
				if speed == "fast":
					self.scene.play(
						*[Indicate(self.text_group[j], color=RED) for j in range(start, start+m)], 
						*[Indicate(self.pattern_group[j], color=RED) for j in range(0, m)]
					)
				elif speed == "slow":
					self.scene.play(
						self.text_group[p1].animate.set_color(RED),
						self.pattern_group[p2].animate.set_color(RED)
					)

			self.scene.wait(2)
			self.scene.play(self.text_group.animate.set_color(WHITE), self.pattern_group.animate.set_color(WHITE))



	def show_naive_with_pause(self):
		self.show_naive_approach("slow", pause_at=1)

		x = Text("X", font_size=50, color=MAROON)
		self.scene.play(SpinInFromNothing(x))
		self.scene.wait(1)
		self.scene.play(FadeOut(x))

		# Redo up to where it failed
		p1, p2 = 4, 4
		self.scene.play(
			self.pattern_group.animate.align_to(self.text_group[0], LEFT)
		)
		self.scene.play(
			self.p1_group.animate.move_to(self.text_group[p1].get_center()+DOWN),
			self.p2_group.animate.move_to(self.pattern_group[p2].get_center()+DOWN),
			*[self.text_group[i].animate.set_color(GREEN) for i in range(0, 4)],
			*[self.pattern_group[i].animate.set_color(GREEN) for i in range(0, 4)],
			self.text_group[4].animate.set_color(RED),
			self.pattern_group[4].animate.set_color(RED)
		)
		self.scene.wait(2)

		self.scene.play(
			self.text_group.animate.set_color(WHITE),
			self.pattern_group.animate.set_color(WHITE)
		)
		self.scene.wait(2)

		self.scene.play(
			*[Indicate(self.text_group[i], color=GREEN) for i in range(0, 4)],
			*[Indicate(self.pattern_group[i], color=GREEN) for i in range(0, 4)]			
		)
		self.scene.wait(2)		

		self.scene.play(
			*[Indicate(self.pattern_group[i], color=GREEN) for i in range(0, 2)]
		)
		self.scene.play(
			*[Indicate(self.text_group[i], color=GREEN) for i in range(2, 4)]
		)
		self.scene.wait(2)



	def show_full_kmp(self, show_lps, show_hints):
		n, m = self.n, self.m


		self.scene.play(Create(self.pattern_group))
		self.scene.wait(2)

		self.scene.play(Create(self.text_group))
		self.scene.wait(2)

		self.scene.play(Create(self.match_group))
		self.scene.wait(2)

		if show_lps:
			self.lps_group = self.create_string_group(''.join([str(self.lps[i]) for i in range(0, m)])).move_to(KnuthMorrisPratt.LPS_POSITION)
			self.scene.play(Create(self.lps_group))
			self.scene.wait(2)

		p1, p2 = 0, 0
		self.p1_group = self.create_arrow_group("p1", KnuthMorrisPratt.P1_COLOUR, "down").move_to(self.text_group[p1].get_center()+UP)
		self.p2_group = self.create_arrow_group("p2", KnuthMorrisPratt.P2_COLOUR, "up").move_to(self.pattern_group[p2].get_center()+DOWN)

		self.scene.play(Create(self.p1_group))
		self.scene.wait(2)

		self.scene.play(Create(self.p2_group))
		self.scene.wait(2)


		while p1 < self.n:
			anim_list = self.get_arrow_shift(p1, p2, UP)
			self.scene.play(*anim_list)

			while p1 < self.n and p2 < self.m and self.text[p1] == self.pattern[p2]:
				self.scene.play(
					self.text_group[p1].animate.set_color(GREEN),
					self.pattern_group[p2].animate.set_color(GREEN)
				)

				p1 += 1
				p2 += 1

				anim_list = self.get_arrow_shift(p1, p2, UP)
				self.scene.play(*anim_list)


			prev_p2 = p2
			if p2 == self.m:
				# There is a match at index p1-p2
				self.match_animation(p1-self.m)
				self.prefix_animation(p1, p2, show_lps, show_hints)
				p2 = self.lps[p2-1]

			elif p1 < self.n:
				self.scene.play(
					self.text_group[p1].animate.set_color(RED),
					self.pattern_group[p2].animate.set_color(RED)
				)
				self.scene.wait(2)

				if p2 == 0:
					self.scene.play(
						self.pattern_group.animate.set_color(WHITE),
						self.text_group.animate.set_color(WHITE)
					)
					p1 += 1
				else:
					self.prefix_animation(p1, p2, show_lps, show_hints)
					p2 = self.lps[p2-1]

			self.scene.play(
				*[self.pattern_group[i].animate.set_color(WHITE) for i in range(p2, self.m)], 
				*[self.text_group[i].animate.set_color(WHITE) for i in range(p1, self.n)]
			)
			if p1-p2 < self.n:
				self.scene.play(
					self.pattern_group.animate.align_to(self.text_group[p1-p2], LEFT)
				)
			self.scene.wait(2)

	

	def show_lps_creation(self, show_hints):
		self.scene.play(Create(self.pattern_group))
		self.scene.wait(2)

		t2c={'prefix': KnuthMorrisPratt.PREFIX_COLOUR, 'suffix': KnuthMorrisPratt.SUFFIX_COLOUR, 'p1': KnuthMorrisPratt.P1_COLOUR, 'p2': KnuthMorrisPratt.P2_COLOUR}
		hint = None


		self.lps_group = self.create_string_group("_"*self.m).move_to(KnuthMorrisPratt.LPS_POSITION)
		self.scene.play(Create(self.lps_group))


		if show_hints:
			hint = Text("Let p1 keep track of the boundary of the previous longest prefix which is also a suffix.", font_size=20, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Write(hint))
			self.scene.wait(1)

			p1 = 0
			self.p1_group = self.create_arrow_group("p1", KnuthMorrisPratt.P1_COLOUR, "down").move_to(self.pattern_group[p1].get_center()+UP)
			self.scene.play(Create(self.p1_group))
			self.scene.wait(2)


		if show_hints:
			hint_2 = Text("Let p2 keep track of our current position in the pattern.", font_size=20, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(1)
		
		label = "p2" if show_hints else ""
		p2 = 0
		self.p2_group = self.create_arrow_group(label, KnuthMorrisPratt.P2_COLOUR, "up").move_to(self.pattern_group[p2].get_center()+DOWN)
		self.scene.play(Create(self.p2_group))
		self.scene.wait(2)


		if show_hints:
			hint_2 = Text("lps[0] = 0 because a single character doesn't have a proper prefix or suffix.", font_size=20, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(2)


		self.scene.play(
			Transform(
				self.lps_group[p2][1], 
				Text(f"0", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
			)
		)
		self.scene.play(self.p2_group.animate.move_to(self.pattern_group[1].get_center()+DOWN))
		self.scene.wait(1)


		lps = [0]*self.m
		p1, p2 = 0, 1
		while p2 < self.m:
			if self.pattern[p1] == self.pattern[p2]:
				if show_hints:
					hint_2 = Text("If P[p1] == P[p2], we can grow the length of the prefix which is also a suffix.", font_size=20, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(1)

				self.scene.play(
					*[self.pattern_group[i].animate.set_color(KnuthMorrisPratt.PREFIX_COLOUR) for i in range(0, p1+1)], 
					*[self.pattern_group[i].animate.set_color(WHITE) for i in range(p1+1, p2-p1+1)],
					*[self.pattern_group[i].animate.set_color(KnuthMorrisPratt.SUFFIX_COLOUR) for i in range(p2-p1, p2+1)]
				)

				p1 += 1

				if show_hints:
					hint_2 = Text("Increment p1 to extend the length of the prefix.", font_size=20, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(1)

					self.scene.play(self.p1_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))
					self.scene.wait(1)

				if show_hints:
					hint_2 = Text("Set lps[p2] = p1.", font_size=20, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(1)

				lps[p2] = p1;

				self.scene.play(
					Transform(
						self.lps_group[p2][1], 
						Text(f"{lps[p2]}", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
					)
				)
				self.scene.wait(1)				
				
				p2 += 1

				if show_hints:
					hint_2 = Text("Increment p2.", font_size=20, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(1)

				self.scene.play(self.p2_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))
				self.scene.wait(1)

			else:
				if p1 > 0:
					if show_hints:
						hint_2 = Text("If P[p1] != P[p2] and p1 > 0, set p1 to lps[p1-1].", font_size=20, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(1)

						self.scene.play(
							*[self.pattern_group[i].animate.set_color(WHITE) for i in range(lps[p1-1], p1+1)],
							*[self.pattern_group[i].animate.set_color(WHITE) for i in range(p2-p1, p2-(p1-lps[p1-1]))],
							self.p1_group.animate.move_to(self.pattern_group[lps[p1-1]].get_center()+UP)
						)
						self.scene.wait(2)

					p1 = lps[p1-1]

				else:
					lps[p2] = 0

					self.scene.play(self.pattern_group.animate.set_color(WHITE))

					if show_hints:
						hint_2 = Text("If P[p1] != P[p2] and p1 == 0, set lps[p2] = 0.", font_size=20, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(1)

					self.scene.play(
						Transform(
							self.lps_group[p2][1], 
							Text(f"{lps[p2]}", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
						)
					)
					self.scene.wait(1)

					if show_hints:
						hint_2 = Text("Increment p2.", font_size=20, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(1)
					
					p2 += 1
					self.scene.play(self.p2_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))
					self.scene.wait(1)					

