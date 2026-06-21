from manim import *

from constants import *

config.background_color = DEFAULT_BACKGROUND

config.pixel_width = MOBILE_WIDTH
config.pixel_height = MOBILE_HEIGHT
config.frame_width = MOBILE_FRAME_WIDTH
config.frame_height = MOBILE_FRAME_HEIGHT


class Rules(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		FZ = 20

		title = Text("Rules", gradient=(TEAL, BLUE, PURPLE, PINK)).move_to(UP*5)

		main_rule = Text("Bears win by biting the other players (NIGHT)", font_size=20)
		main_rule_2 = Text("Players win by voting out the bears (DAY)", font_size=20)
		main_rules = VGroup(main_rule, main_rule_2).arrange(DOWN)
		mr_rect = BackgroundRectangle(main_rules, stroke_color=TEAL, stroke_width=2, stroke_opacity=1, corner_radius=0.2, buff=0.25)

		night_round = Text("Night Round", font_size=FZ, weight=BOLD)
		rule_1 = Text("1. Each player takes their turn to see\ntheir role.", font_size=FZ)
		rule_2 = Text("2. Some players have special abilities\nto perform on a target player.", font_size=FZ)
		rule_3 = Text("3. Bears have a different output - they\ncan see who the other Bears are\nand which player has been bitten.", font_size=FZ)
		rule_4 = Text("4. The player bitten by the bears is\neliminated, unless healed by the\nHealer.", font_size=FZ)
		night_rules = VGroup(night_round, rule_1, rule_2, rule_3, rule_4).arrange(DOWN, aligned_edge=LEFT)
		nr_rect = BackgroundRectangle(night_rules, stroke_color=BLUE, stroke_width=2, stroke_opacity=1, corner_radius=0.2, buff=0.25)

		day_round = Text("Day Round", font_size=FZ, weight=BOLD)
		rule_1 = Text("1. Each player takes their turn to vote\nout who they think the Bears are.", font_size=FZ)
		rule_2 = Text("2. The Activist gets a 1/2 chance to\nvote twice.", font_size=FZ)
		rule_3 = Text("3. One player is banned from voting by\nthe Activist.", font_size=FZ)
		rule_4 = Text("4. The player with the most votes is\neliminated.", font_size=FZ)
		day_rules = VGroup(day_round, rule_1, rule_2, rule_3, rule_4).arrange(DOWN, aligned_edge=LEFT)
		dr_rect = BackgroundRectangle(day_rules, stroke_color=PINK, stroke_width=2, stroke_opacity=1, corner_radius=0.2, buff=0.25)

		all_rules = VGroup(title, VGroup(mr_rect, main_rules), VGroup(nr_rect, night_rules), VGroup(dr_rect, day_rules)).arrange(DOWN)
		for rule in all_rules:
			self.play(FadeIn(rule))
			self.wait(5)