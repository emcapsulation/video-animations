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


	def __init__(self, scene, pattern, text, spaced=False, mobile=False):
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

		self.mobile = True
		if mobile:			
			self.text_group.scale(0.6)
			self.pattern_group.scale(0.6).align_to(self.text_group[0], LEFT)
			KnuthMorrisPratt.HINT_POSITION = DOWN*4


	def create_string_group(self, s):
		string = VGroup(*[Text(str(c), font_size=KnuthMorrisPratt.STRING_GROUP_FS) for c in s]).arrange(RIGHT, buff=KnuthMorrisPratt.STRING_BUFF)
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



	def show_text_pattern(self, scene):
		self.scene.play(Create(self.pattern_group))
		self.scene.wait(2)

		self.scene.play(Create(self.text_group))
		self.scene.wait(2)



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
		fs = 24 if self.mobile else 16

		if show_hints:
			hint_text = "Find longest overlap between the prefix of the pattern, and the suffix of the matched part."
			if self.mobile:
				hint_text = "Find longest overlap between the\nprefix of the pattern, and the\nsuffix of the matched part."

			hint = Text(hint_text, font_size=fs).move_to(KnuthMorrisPratt.HINT_POSITION)
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

			hint_text = f"Move p2 to index {self.lps[p2-1]} - the {prefix} prefix of the pattern equals the {prefix} suffix in the matched part."
			if self.mobile:
				hint_text = f"Move p2 to index {self.lps[p2-1]} \n- the {prefix} prefix of the pattern\nequals the {prefix} suffix in the\nmatched part."

			hint_2 = Text(hint_text, font_size=fs, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)
			
			if self.lps[p2-1] == 0:
				hint_text = f"Move p2 to index {self.lps[p2-1]} - there is no equal prefix in the pattern and suffix in the matched part."
				if self.mobile:
					hint_text = f"Move p2 to index {self.lps[p2-1]}\n- there is no equal prefix in the\npattern and suffix in the\nmatched part."

				hint_2 = Text(hint_text, font_size=fs, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)

			if show_lps:
				hint_text = "If T[p1] != P[p2] and p2 > 0, set p2 = lps[p2-1]."
				if self.mobile:
					hint_text = "If T[p1] != P[p2] and p2 > 0,\nset p2 = lps[p2-1]."

				hint_2 = Text(hint_text, font_size=fs, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)

			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(2)

		if show_lps:
			self.scene.play(Indicate(self.lps_group[p2-1][1]))
			self.scene.play(Flash(self.lps_group[p2-1][1]))

		if show_hints:
			self.scene.play(FadeOut(hint))



	def show_naive_approach(self, speed, pause_at=-1, move=True):
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

			if move:
				anim_list = [self.pattern_group.animate.align_to(self.text_group[start], LEFT)]
				if speed == "slow":
					anim_list.append(self.start_group.animate.move_to(self.text_group[start].get_center()+UP))
				self.scene.play(*anim_list)

			if speed == "slow":
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
				if not move:
					self.scene.play(self.pattern_group.animate.align_to(self.text_group[start], LEFT))
				self.scene.play(
					*[Indicate(self.text_group[j], color=GREEN) for j in range(start, start+m)], 
					*[Indicate(self.pattern_group[j], color=GREEN) for j in range(0, m)]
				)

				self.match_animation(start)

				
			else:
				if speed == "fast" and move == True:
					self.scene.play(
						*[Indicate(self.text_group[j], color=RED) for j in range(start, start+m)], 
						*[Indicate(self.pattern_group[j], color=RED) for j in range(0, m)]
					)
				elif speed == "slow":
					self.scene.play(
						self.text_group[p1].animate.set_color(RED),
						self.pattern_group[p2].animate.set_color(RED)
					)

			if speed == "slow":
				self.scene.wait(2)
			self.scene.play(self.text_group.animate.set_color(WHITE), self.pattern_group.animate.set_color(WHITE))



	def show_naive_with_pause(self):
		self.show_naive_approach("slow", pause_at=1)
		self.scene.play(
			self.p1_group.animate.move_to(self.text_group[1].get_center()+DOWN),
			self.p2_group.animate.move_to(self.pattern_group[0].get_center()+DOWN)
		)
		self.scene.wait(1)

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
			self.start_group.animate.align_to(self.text_group[0].get_center()+UP),
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
		fs = 24 if self.mobile else 16

		n, m = self.n, self.m
		hint = None

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

				if show_hints:				
					hint_text = "If T[p1] == P[p2], increment both p1 and p2."
					if self.mobile:
						hint_text = "If T[p1] == P[p2],\nincrement both p1 and p2."

					hint_2 = Text(hint_text, font_size=fs, t2c={'p1': KnuthMorrisPratt.P1_COLOUR, 'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)

					if hint != None:
						self.scene.play(Transform(hint, hint_2))
					else:
						hint = hint_2
						self.scene.play(Write(hint))
						self.scene.wait(2)

				p1 += 1
				p2 += 1

				anim_list = self.get_arrow_shift(p1, p2, UP)
				self.scene.play(*anim_list)


			prev_p2 = p2
			if p2 == self.m:
				# There is a match at index p1-p2
				if show_hints and hint != None:
					self.scene.play(FadeOut(hint))
					hint = None
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
					if show_hints:
						hint_text = "If T[p1] != P[p2] and p2 == 0, just increment p1 to try from the next substring."
						if self.mobile:
							hint_text = "If T[p1] != P[p2] and p2 == 0,\njust increment p1 to try from\nthe next substring."

						hint_2 = Text(hint_text, font_size=fs, t2c={'p1': KnuthMorrisPratt.P1_COLOUR, 'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(KnuthMorrisPratt.HINT_POSITION)
						
						if hint != None:
							self.scene.play(Transform(hint, hint_2))
						else:
							hint = hint_2
							self.scene.play(Write(hint))
						self.scene.wait(2)

					self.scene.play(
						self.pattern_group.animate.set_color(WHITE),
						self.text_group.animate.set_color(WHITE)
					)
					p1 += 1
				else:
					if show_hints and hint != None:
						self.scene.play(FadeOut(hint))
						hint = None
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

	

	def show_lps_creation(self, show_hints):
		fs = 24 if self.mobile else 20
		if self.mobile:
			self.pattern_group.scale(1.7)

		self.scene.play(Create(self.pattern_group))
		self.scene.wait(2)

		t2c={'prefix': KnuthMorrisPratt.PREFIX_COLOUR, 'suffix': KnuthMorrisPratt.SUFFIX_COLOUR, 'p1': KnuthMorrisPratt.P1_COLOUR, 'p2': KnuthMorrisPratt.P2_COLOUR}
		hint = None


		self.lps_group = self.create_string_group("_"*self.m).move_to(KnuthMorrisPratt.LPS_POSITION)
		if self.mobile:
			self.lps_group.shift(UP*0.5)
		self.scene.play(Create(self.lps_group))


		if show_hints:
			hint_text = "Let p1 keep track of the boundary of the previous longest prefix which is also a suffix."
			if self.mobile:
				hint_text = "Let p1 keep track of the boundary\nof the previous longest prefix\nwhich is also a suffix."
			
			hint = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Write(hint))
			self.scene.wait(2)

			p1 = 0
			self.p1_group = self.create_arrow_group("p1", KnuthMorrisPratt.P1_COLOUR, "down").move_to(self.pattern_group[p1].get_center()+UP)
			self.scene.play(Create(self.p1_group))
			self.scene.wait(2)


		if show_hints:
			hint_text = "Let p2 keep track of our current position in the pattern."
			if self.mobile:
				hint_text = "Let p2 keep track of our current\nposition in the pattern."
			
			hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(2)
		
		label = "p2" if show_hints else ""
		p2 = 0
		self.p2_group = self.create_arrow_group(label, KnuthMorrisPratt.P2_COLOUR, "up").move_to(self.pattern_group[p2].get_center()+DOWN)
		self.scene.play(Create(self.p2_group))
		self.scene.wait(2)


		if show_hints:
			hint_text = "lps[0] = 0 because a single character doesn't have a proper prefix or suffix."
			if self.mobile:
				hint_text = "lps[0] = 0 because a single\ncharacter doesn't have a proper\nprefix or suffix."

			hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
			self.scene.play(Transform(hint, hint_2))
			self.scene.wait(2)


		self.scene.play(
			Transform(
				self.lps_group[p2][1], 
				Text(f"0", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
			)
		)
		self.scene.play(self.p2_group.animate.move_to(self.pattern_group[1].get_center()+DOWN))


		lps = [0]*self.m
		p1, p2 = 0, 1
		while p2 < self.m:
			if self.pattern[p1] == self.pattern[p2]:
				if show_hints:
					hint_text = "If P[p1] == P[p2], we can grow the length of the prefix which is also a suffix."
					if self.mobile:
						hint_text = "If P[p1] == P[p2], we can grow\nthe length of the prefix which\nis also a suffix."

					hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(2)

				self.scene.play(
					*[self.pattern_group[i].animate.set_color(KnuthMorrisPratt.PREFIX_COLOUR) for i in range(0, p1+1)], 
					*[self.pattern_group[i].animate.set_color(WHITE) for i in range(p1+1, p2-p1)],
					*[self.pattern_group[i].animate.set_color(KnuthMorrisPratt.SUFFIX_COLOUR) for i in range(p2-p1, p2+1)]
				)

				p1 += 1

				if show_hints:
					hint_text = "Increment p1 to extend the length of the prefix."
					if self.mobile:
						hint_text = "Increment p1 to extend the length\nof the prefix."

					hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(2)

					self.scene.play(self.p1_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))

				if show_hints:
					hint_2 = Text("Set lps[p2] = p1.", font_size=fs, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(2)

				lps[p2] = p1;

				self.scene.play(
					Transform(
						self.lps_group[p2][1], 
						Text(f"{lps[p2]}", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
					)
				)			
				
				p2 += 1

				if show_hints:
					hint_2 = Text("Increment p2.", font_size=fs, t2c=t2c).move_to(DOWN*3)
					self.scene.play(Transform(hint, hint_2))
					self.scene.wait(2)

				self.scene.play(self.p2_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))

			else:
				if p1 > 0:
					if show_hints:
						hint_text = "If P[p1] != P[p2] and p1 > 0, set p1 to lps[p1-1]."
						if self.mobile:
							hint_text = "If P[p1] != P[p2] and p1 > 0,\nset p1 to lps[p1-1]."

						hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(2)

						if lps[p1-1] == 0:
							self.scene.play(self.pattern_group.animate.set_color(WHITE))

						self.scene.play(Indicate(self.lps_group[p1-1][1]))
						self.scene.play(Flash(self.lps_group[p1-1][1]))

						self.scene.play(
							*[self.pattern_group[i].animate.set_color(WHITE) for i in range(lps[p1-1], p1+1)],
							*[self.pattern_group[i].animate.set_color(WHITE) for i in range(p2-p1, p2-(p1-lps[p1-1]))],
							self.p1_group.animate.move_to(self.pattern_group[lps[p1-1]].get_center()+UP)
						)

					p1 = lps[p1-1]

				else:
					lps[p2] = 0

					self.scene.play(self.pattern_group.animate.set_color(WHITE))

					if show_hints:
						hint_text = "If P[p1] != P[p2] and p1 == 0, set lps[p2] = 0."
						if self.mobile:
							hint_text = "If P[p1] != P[p2] and p1 == 0,\nset lps[p2] = 0."

						hint_2 = Text(hint_text, font_size=fs, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(2)

					self.scene.play(
						Transform(
							self.lps_group[p2][1], 
							Text(f"{lps[p2]}", font_size=KnuthMorrisPratt.STRING_GROUP_FS).move_to(self.lps_group[p2][1].get_center())
						)
					)

					if show_hints:
						hint_2 = Text("Increment p2.", font_size=fs, t2c=t2c).move_to(DOWN*3)
						self.scene.play(Transform(hint, hint_2))
						self.scene.wait(2)
					
					p2 += 1
					self.scene.play(self.p2_group.animate.shift(RIGHT*KnuthMorrisPratt.ARROW_SHIFT))



	def create_thumbnail(self):
		title = Text("Knuth-Morris-Pratt Algorithm").move_to(UP*3)
		self.scene.add(title)

		subtitle = Text("Find all occurrences of the pattern in the longer text.", font_size=20, t2c={"pattern": TEAL, "text": PURPLE}).next_to(title, DOWN)
		self.scene.add(subtitle)


		self.pattern_group.shift(DOWN*1.5)
		self.text_group.shift(DOWN*1.5)


		self.p1_group = self.create_arrow_group("p1", KnuthMorrisPratt.P1_COLOUR, "down").move_to(self.text_group[0].get_center()+DOWN)
		self.p2_group = self.create_arrow_group("p2", KnuthMorrisPratt.P2_COLOUR, "up").move_to(self.pattern_group[0].get_center()+DOWN)


		self.lps_group = self.create_string_group(self.lps).scale(1.075).align_to(self.p2_group[0], LEFT).shift(DOWN*3)


		p1 = 0
		p2 = 0
		while self.text[p1] == self.pattern[p2]:
			if p2 < 2:
				self.pattern_group[p2].set_color(KnuthMorrisPratt.PREFIX_COLOUR)

			if p1 >= 4: 
				self.text_group[p1].set_color(KnuthMorrisPratt.SUFFIX_COLOUR)

			p1 += 1
			p2 += 1


		for c in self.lps_group:
			c.set_color(GRAY_B)


		self.text_group[p1].set_color(RED)
		self.pattern_group[p2].set_color(RED)

		self.p1_group.move_to(self.text_group[p1].get_center()+UP)
		self.p2_group.move_to(self.pattern_group[p2].get_center()+DOWN)


		subtitle_2 = Text("Where does p2 move to next?", font_size=20, t2c={"p2": KnuthMorrisPratt.P2_COLOUR}).move_to(self.lps_group.get_right() + RIGHT*4 + UP*1.5)
		self.scene.add(subtitle_2)


		rect = Rectangle(
			width=0.5, height=1,
			stroke_color=GREEN
		).move_to(self.lps_group[5].get_center())


		self.scene.add(self.pattern_group, self.text_group, self.p1_group, self.p2_group, self.lps_group, subtitle_2, rect)
