from manim import *
from KnuthMorrisPratt import KnuthMorrisPratt

config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8



class KMPShortDescriptions(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		question = Text("Can you find all occurrences of\nthe pattern in the longer text,\nin just O(m+n) time?", font_size=24, t2c={"pattern": TEAL, "text": PURPLE, "O(m+n)": GREEN}).move_to(UP*4)
		self.play(Write(question))
		self.wait(2)


		title = Text("Knuth-Morris-Pratt").move_to(UP*4)
		self.play(Transform(question, title))
		self.wait(5)


		title = Text("LPS Array").move_to(UP*5.5)
		self.play(Transform(question, title))
		self.wait(20)


		title = Text("KMP Algorithm").move_to(UP*5.5)
		self.play(Transform(question, title))
		self.wait(20)



class KMPShort(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "AABCAABCBAABCAAABCAAAB"		
		pattern = "AABCAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text, spaced=False, mobile=True)
		KMP.show_naive_approach(speed="fast", move=False)



class KMPLpsOnly(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		text = "AABCAABCBAABCAAABCAAAB"		
		pattern = "AABCAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text, mobile=True)
		KMP.pattern_group.move_to(ORIGIN+UP)
		KMP.show_lps_creation(True)

		self.play(KMP.pattern_group.animate.set_color(WHITE))
		self.play(
			*[FadeOut(mob)for mob in self.mobjects]
		)
		self.wait(5)



class KMPAlgorithmOnly(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		text = "AABCAABCBAABCAAABCAAAB"		
		pattern = "AABCAAAB"

		KMP = KnuthMorrisPratt(self, pattern, text, mobile=True)
		KMP.show_full_kmp(True, True)

		self.wait(5)