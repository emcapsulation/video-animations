from manim import *
from KnuthMorrisPratt import KnuthMorrisPratt

config.background_color = "#15131c"



class NaiveApproachDemo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "ABABABCAABABCAABABCABABCAAB"		
		pattern = "ABABCAAB"

		KMP = KnuthMorrisPratt(self, pattern, text, spaced=True)
		KMP.show_naive_approach("fast")



class NaiveApproachDescriptions(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		problem = Text("Find all occurrences of the pattern in the longer text.", font_size=20, t2c={"pattern": TEAL, "text": PURPLE}).move_to(UP*3)
		self.play(Write(problem))
		self.wait(5)



class NaiveApproachCode(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		text = "ABABABCAABABCAABABCABABCAAB"		
		pattern = "ABABCAAB"

		KMP = KnuthMorrisPratt(self, pattern, text, spaced=True)
		KMP.show_naive_approach("slow")



class NaiveApproachTimeComplexity(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "AAAAAAAAAAAA"		
		pattern = "AAAB"
		
		KMP = KnuthMorrisPratt(self, pattern, text, spaced=True)
		KMP.show_naive_approach("slow")



class NaiveApproachTimeComplexityDescriptions(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Time Complexity (Naive Approach)").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)

		text = Text("(n-m+1) start positions in the text x m characters in the pattern", font_size=24).move_to(DOWN*3)
		self.play(Write(text))
		self.wait(2)

		text_2 = Text("(n-m+1) * m comparisons", font_size=24).move_to(DOWN*3)
		self.play(Transform(text, text_2))
		self.wait(2)

		text_3 = Text("Given n >> m, then n-m+1 is upper-bounded by n", font_size=24).move_to(DOWN*3)
		self.play(Transform(text, text_3))
		self.wait(2)

		text_4 = Text("O(nm)", font_size=30).move_to(DOWN*3)
		self.play(Transform(text, text_4))
		self.wait(2)

		self.play(text.animate.set_color(RED))
		self.wait(2)



class KMPInitialDemoWithHints(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "ABABABCAABABCAABABCABABCAAB"		
		pattern = "ABABCAAB"
		
		KMP = KnuthMorrisPratt(self, pattern, text, spaced=True)
		KMP.show_naive_with_pause()



class KMPInitialDemoWithHintsDescriptions(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Knuth-Morris-Pratt").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)

		problem = Text("Do we really need to take p2 back to index 0?", font_size=20, t2c={'p2': KnuthMorrisPratt.P2_COLOUR}).move_to(UP*3)
		self.play(Transform(title, problem))
		self.wait(2)

		hint_1 = Text("Hint #1: The first four characters, ABAB, do match in the pattern and text.", color=BLACK, font_size=20, t2c={'Hint #1:': PINK})
		surround = BackgroundRectangle(hint_1, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		hint_group = VGroup(surround, hint_1).move_to(DOWN*3)
		self.play(FadeIn(hint_group))
		self.wait(1)

		hint_2 = Text("Hint #2: The pattern starts with AB, and the matched part ends with AB.", color=BLACK, font_size=20, t2c={'Hint #2:': PINK})
		surround_2 = BackgroundRectangle(hint_2, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		hint_group_2 = VGroup(surround_2, hint_2).move_to(DOWN*3)
		self.play(Transform(hint_group, hint_group_2))
		self.wait(1)

		self.play(FadeOut(hint_group))
		self.wait(2)



class KMPInitialDemoWithHints2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "ABABABCAABABCAABABCABABCAAB"		
		pattern = "ABABCAAB"

		KMP = KnuthMorrisPratt(self, pattern, text)
		KMP.show_full_kmp(False, True)

		self.wait(5)



class KMPDemoWithCode(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "AAABAAABCAAABAAAABAAAABC"		
		pattern = "AAABAAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text)
		KMP.show_full_kmp(False, True)

		self.wait(5)




class PrefixSuffixExplanation(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		PREFIX_COLOUR = TEAL
		SUFFIX_COLOUR = PURPLE
		P1_COLOUR = ORANGE
		P1_POS = UP


		title = Text("LPS Array").move_to(UP*3)
		self.play(Write(title))
		self.wait(1)


		subtitle = Text("Longest (proper) Prefix (which is also equal to a proper) Suffix", font_size=20, t2c={'Prefix': TEAL, 'Suffix': PURPLE}).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(1)


		pattern = "ABABCAAB"
		m = len(pattern)
		fs = 30

		pattern_group = VGroup(*[Text(c, font_size=fs) for c in pattern]).arrange(RIGHT, buff=0.3)
		index_group = VGroup(*[Text(str(i), font_size=10).next_to(pattern_group[i], UP) for i in range(m)])

		self.play(AddTextLetterByLetter(pattern_group), AddTextLetterByLetter(index_group))
		self.wait(2)


		proper_prefix = Text("Proper Prefix: A substring at the start of a string, not including the entire string.", font_size=16, t2c={'Proper Prefix:': TEAL}).move_to(DOWN*3)
		self.play(Write(proper_prefix))

		brace = BraceBetweenPoints(pattern_group[0].get_left()+DOWN, pattern_group[0].get_left()+DOWN, direction=DOWN)
		self.play(Create(brace))

		for i in range(0, m-1):
			brace_2 = BraceBetweenPoints(pattern_group[0].get_left()+DOWN, pattern_group[i].get_right()+DOWN, direction=DOWN)
			self.play(
				Transform(brace, brace_2),
				*[pattern_group[i].animate.set_color(TEAL) for i in range(0, i+1)]
			)
		self.play(FadeOut(brace), pattern_group.animate.set_color(WHITE))


		proper_suffix = Text("Proper Suffix: A substring at the end of a string, not including the entire string.", font_size=16, t2c={'Proper Suffix:': PURPLE}).move_to(DOWN*3)
		self.play(ReplacementTransform(proper_prefix, proper_suffix))

		brace = BraceBetweenPoints(pattern_group[m-1].get_right()+DOWN, pattern_group[m-1].get_right()+DOWN, direction=DOWN)
		self.play(Create(brace))

		for i in range(m-1, 0, -1):
			brace_2 = BraceBetweenPoints(pattern_group[i].get_left()+DOWN, pattern_group[m-1].get_right()+DOWN, direction=DOWN)
			self.play(
				Transform(brace, brace_2),
				*[pattern_group[i].animate.set_color(PURPLE) for i in range(i, m)]
			)
		self.play(FadeOut(brace), pattern_group.animate.set_color(WHITE))
		self.wait(2)



class LPSArrayWalkthrough(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		pattern = "ABABCAAB"

		KMP = KnuthMorrisPratt(self, pattern, "AAAAAAAA")
		KMP.show_lps_creation(False)



class LPSAlgorithm(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		pattern = "AAABAAAAB"

		KMP = KnuthMorrisPratt(self, pattern, "AAABAAAAB")
		KMP.show_lps_creation(True)



class LPSAlgorithm(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		pattern = "ABABCABABAB"

		KMP = KnuthMorrisPratt(self, pattern, "ABABCABABAB")
		KMP.show_lps_creation(True)



class KMPFullAlgorithm(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		text = "ABABABCAABABCAABABCABABCAAB"		
		pattern = "ABABCAAB"

		KMP = KnuthMorrisPratt(self, pattern, text)
		KMP.show_full_kmp(True, True)

		self.wait(5)



class KMPAlgorithmExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		text = "AABCAACAABCAAABCAAAB"		
		pattern = "AABCAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text)
		KMP.show_lps_creation(True)

		self.play(KMP.pattern_group.animate.set_color(WHITE))
		self.play(
			*[FadeOut(mob)for mob in self.mobjects]
		)

		KMP.show_full_kmp(True, True)

		self.wait(5)



class DrawAndGlowLetter(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        self.play(Write(Text("Thank you for watching!").shift(UP*2)))

        letter_e = Text("e", font_size=200, color=TEAL)
        self.play(Write(letter_e))

        letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
        glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
        self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
        self.play(FadeOut(letter_e_stroke, glow_effect))

        self.wait(3)




class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		text = "AABCAACAABCAAABCAAAB"		
		pattern = "AABCAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text)
		KMP.create_thumbnail()
