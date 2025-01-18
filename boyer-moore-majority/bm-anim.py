from manim import *

config.background_color = "#15131c"


class Votes:
	def __init__(self, population):
		self.population = population
		self.votes = VGroup()
		self.voters = VGroup()

		self.set_voters()
		self.init_votes()


	def get_population(self):
		return self.population

	def get_voters(self):
		return self.voters

	def set_voters(self):
		for i in range(0, self.population):
			self.voters.add(Dot(color=WHITE, radius=0.2))
		self.voters.arrange(RIGHT)

	def get_votes(self):
		return self.votes

	def init_votes(self):
		open_bracket = Text("[");
		close_bracket = Text("]").move_to(open_bracket.get_right() + RIGHT*0.2);
		self.votes.add(open_bracket, close_bracket)

	# Order is the order of votes
	def animate_votes(self, scene, order):
		for i in range(0, len(order)):
			cur_dot = Dot(color=order[i], radius=0.2).move_to(self.voters[0].get_center())
			self.votes.insert(i+1, cur_dot)

			# Moving the vote into the array
			scene.play(
				cur_dot.animate.move_to(self.votes[i].get_right() + RIGHT*cur_dot.get_width()),
				self.votes[-1].animate.shift(RIGHT*1.5*cur_dot.get_width()),
				FadeOut(self.voters[0]),
				run_time=0.5
			)
			self.voters.remove(self.voters[0])

			# Shifting everyone over
			scene.play(
				self.voters.animate.shift(LEFT*1.5*cur_dot.get_width()),
				self.votes.animate.move_to(ORIGIN + DOWN*2),
				run_time=0.5
			)
		scene.wait(1)

		scene.play(
			self.votes.animate.scale(1.4).shift(UP)
		)
		scene.wait(3)



def getZigZag():
    lightning = Line(start=LEFT+UP*2, end=RIGHT+UP*1, stroke_width=4, color=WHITE)
    for i in range(0, 4):
    	if i%2 == 0:
    		lightning.add_line_to(LEFT+DOWN*i);
    	else:
    		lightning.add_line_to(RIGHT+DOWN*i);
    return lightning.shift(UP*0.5)


class VotingScenario(Scene):
	def construct(self):
		Text.set_default(font="Consolas")


		# Population sign
		rounded_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE,
			fill_color=GREEN,
			fill_opacity=1
		)

		vertical_rect = Rectangle(
			width=0.5, height=1,
			stroke_width=4,
			stroke_color=WHITE,
			fill_color=GOLD_E,
			fill_opacity=1,
		)

		vertical_rect.next_to(rounded_rect, DOWN, buff=0)

		pop_text = Text("Population", font_size=24, color=BLACK).move_to(rounded_rect.get_center()).shift(UP*0.25)
		pop_text2 = Text("10", font_size=30, color=BLACK).move_to(rounded_rect.get_center()).shift(DOWN*0.25)

		population_sign = VGroup(vertical_rect, rounded_rect, pop_text, pop_text2)

		self.play(Create(rounded_rect), Create(vertical_rect), Write(pop_text), Write(pop_text2))
		self.play(population_sign.animate.scale(0.7).shift(UP*3 + RIGHT*5))
		self.wait(1)


		# Circular candidates
		candidates = VGroup()

		candidates_text = Text("Candidates: ")
		candidates.add(candidates_text)

		# Create the dots with different colors
		dot1 = Dot(color=GREEN, radius=0.5)
		lightning1 = getZigZag().scale((0.3, 0.5, 1))
		dot2 = Dot(color=PINK, radius=0.5)
		lightning2 = getZigZag().scale((0.3, 0.5, 1))
		dot3 = Dot(color=BLUE, radius=0.5)

		candidates.add(dot1, lightning1, dot2, lightning2, dot3)
		candidates.arrange(RIGHT)        

		self.play(Write(candidates_text), run_time=1)
		for i in range(1, len(candidates)):
			self.play(Create(candidates[i]), run_time=0.2)
		self.play(candidates.animate.scale(0.6).shift(UP*2.5 + LEFT*3))
		self.wait(1)


		# Majority text
		majority_text = VGroup()

		part1 = Text("Majority:")
		part2 = Text(" > 1/2 * total")

		majority_text.add(part1, part2).shift(ORIGIN)
		majority_text.arrange(RIGHT)

		self.play(Write(part1))
		self.wait(1)
		self.play(Write(part2))
		self.wait(1)

		transformed_part = Text(" > 1/2 * 10")
		transformed_part.move_to(part2.get_center())

		self.play(Transform(part2, transformed_part))
		self.wait(1)

		transformed_part = Text(" > 5")
		transformed_part.move_to(part2.get_center() + LEFT)

		self.play(Transform(part2, transformed_part))
		self.wait(1)


		# Move the majority to upper right
		self.play(FadeOut(population_sign), majority_text.animate.scale(0.6).shift(UP*2.5 + RIGHT*5.5))
		self.wait(3)


		v = Votes(10)

		# The voters represented as white dots
		voters = v.get_voters()
		voters.move_to(ORIGIN-voters.get_left())
		self.play(Create(voters))
		self.wait(2)

		# The votes represented as colourful dots
		votes = v.get_votes()
		votes.shift(DOWN*2)
		self.play(Create(votes))

		order = [PINK, GREEN, PINK, PINK, PINK, GREEN, BLUE, PINK, PINK, BLUE]
		v.animate_votes(self, order)
