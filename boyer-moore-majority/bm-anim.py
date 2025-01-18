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

	def show_votes(self, scene, order):
		for i in range(0, len(order)):
			cur_dot = Dot(color=order[i], radius=0.2)				
			self.votes.insert(i+1, cur_dot)		

			cur_dot.move_to(self.votes[i].get_right() + RIGHT*cur_dot.get_width())	
			self.votes[-1].shift(RIGHT*1.5*cur_dot.get_width())
			self.votes.move_to(ORIGIN + DOWN*2)

		scene.add(self.votes)

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


	def animate_map(self, scene, order):
		self.show_votes(scene, order)
		self.get_votes().scale(1.4).shift(UP)

		hashmap = VGroup(Text("Candidates\n     Votes"))
		hashmap.scale(0.7).shift(UP*2)

		scene.play(Create(hashmap))
		scene.wait(1)


		# Maps colour to position in VGroup and number of votes
		vote_map = {}
		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)

		winner = None
		seen = 1
		for i in range(0, self.get_population()):
			# Move the arrow along
			scene.play(arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2))
			cand_key = str(self.get_votes()[i+1].get_color())

			this_dot = Dot(color=self.get_votes()[i+1].get_color(), radius=0.2).scale(1.4)
			this_dot.move_to(self.get_votes()[i+1].get_center())

			if cand_key not in vote_map:
				vote_map[cand_key] = [seen, 1]
				seen += 1

				candidate_dot = Dot(color=self.get_votes()[i+1].get_color(), radius=0.2)

				# New column data
				new_column = VGroup(					
				    candidate_dot,
				    Text("1")
				)
				new_column.scale(0.7).arrange(DOWN).next_to(hashmap, RIGHT, buff=1)
				hashmap.add(new_column)

				scene.play(
					FadeIn(new_column), 
					this_dot.animate.move_to(hashmap[-1][0].get_center()).scale(0.5)					
				)
				scene.remove(this_dot)
				scene.play(
					hashmap.animate.move_to(ORIGIN + UP*2)
				)

			else:
				index = vote_map[cand_key][0]
				vote_map[cand_key][1] += 1

				scene.play(
					this_dot.animate.scale(0.5).move_to(hashmap[index][0].get_center()),
					Transform(hashmap[index][1], 
					Text(str(vote_map[cand_key][1])).scale(0.7).move_to(hashmap[index][1]))
				)
				scene.remove(this_dot)


			if vote_map[cand_key][1] > self.get_population()/2:
				scene.play(
					hashmap[index][1].animate.set_color(RED)
				)

				winner = Dot(color=hashmap[index][0].get_color(), radius=0.2)
				break

		outcome = VGroup()
		if winner != None:
			win_text = Text("Winner: ", font_size=24)
			winner.next_to(win_text, RIGHT, buff=1)
			outcome.add(win_text, winner)
		else:
			win_text = Text("No one received a majority", font_size=24)
			outcome.add(win_text)

		outcome.move_to(ORIGIN).shift(DOWN*3)
		scene.play(Write(outcome))
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

		order = [PINK, GREEN, PINK, PINK, PINK, BLUE, GREEN, PINK, PINK, BLUE]
		v.animate_votes(self, order)


		self.play(
			FadeOut(candidates), FadeOut(majority_text)
		)



class HashmapExample(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(10)
		order = [PINK, GREEN, PINK, PINK, PINK, BLUE, GREEN, PINK, PINK, BLUE]	
		v.animate_map(self, order)



class HashmapNoMaj(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(10)
		order = [BLUE, GREEN, PINK, PINK, BLUE, BLUE, GREEN, PINK, GREEN, BLUE]	
		v.animate_map(self, order)
