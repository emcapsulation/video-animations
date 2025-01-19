from manim import *
import random

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
			self.votes.move_to(ORIGIN + DOWN*1.5)	
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


	def animate_map(self, scene, order, run_time):
		self.show_votes(scene, order)
		self.get_votes().scale(1.4).shift(UP)

		hashmap = VGroup(Text("Candidates\n     Votes"))
		hashmap.scale(0.7).shift(UP*2)

		scene.play(FadeIn(self.get_votes()))
		scene.wait(1)

		scene.play(Create(hashmap))
		scene.wait(1)


		# Maps colour to position in VGroup and number of votes
		vote_map = {}
		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)
		scene.add(arrow)

		winner = None
		seen = 1
		for i in range(0, self.get_population()):
			# Move the arrow along
			cand_key = str(self.get_votes()[i+1].get_color())

			this_dot = Dot(color=self.get_votes()[i+1].get_color(), radius=0.2).scale(1.4)
			this_dot.move_to(self.get_votes()[i+1].get_center())

			# Arrow animation
			arrow_animate = None
			if i < self.get_population()-1:
				arrow_animate = arrow.animate.next_to(self.get_votes()[i+2], DOWN, buff=0.2)
			else:
				arrow_animate = arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2)


			if cand_key not in vote_map:
				vote_map[cand_key] = [seen, 1]
				seen += 1

				candidate_dot = Dot(color=self.get_votes()[i+1].get_color(), radius=0.2)

				# New column data
				new_column = VGroup(					
				    candidate_dot,
				    Text("1")
				)
				new_column.scale(0.7).arrange(DOWN).next_to(hashmap, RIGHT, buff=0.7)
				hashmap.add(new_column)

				scene.play(
					FadeIn(new_column), 
					this_dot.animate.move_to(hashmap[-1][0].get_center()).scale(0.5),
					run_time=run_time					
				)
				scene.remove(this_dot)
				scene.play(
					hashmap.animate.move_to(ORIGIN + UP*2),
					arrow_animate,
					run_time=run_time
				)

			else:
				index = vote_map[cand_key][0]
				vote_map[cand_key][1] += 1

				scene.play(
					this_dot.animate.scale(0.5).move_to(hashmap[index][0].get_center()),
					Transform(hashmap[index][1], 
					Text(str(vote_map[cand_key][1])).scale(0.7).move_to(hashmap[index][1])),
					run_time=run_time
				)
				scene.remove(this_dot)

				if vote_map[cand_key][1] <= self.get_population()/2:
					scene.play(
						arrow_animate,
						run_time=run_time
					)


			if vote_map[cand_key][1] > self.get_population()/2:
				scene.play(
					hashmap[index][1].animate.set_color(GREEN)
				)

				winner = Dot(color=hashmap[index][0].get_color(), radius=0.2)
				break

		outcome = VGroup()
		if winner != None:
			win_text = Text("Winner: ", font_size=24)
			winner.next_to(win_text, RIGHT, buff=1)
			outcome.add(win_text, winner)
		else:
			win_text = Text("There is no majority element", font_size=24)
			outcome.add(win_text)

		outcome.move_to(ORIGIN).shift(DOWN*3)
		scene.play(Write(outcome))
		scene.wait(3)


	def pass_through(self, scene, outcome, run_time):
		winner = outcome[1]

		count_text = Text("Count: ")
		count_num = Text("0").next_to(count_text, RIGHT, buff=1)
		top_text = VGroup(count_text, count_num)
		top_text.move_to(ORIGIN + UP*2)

		scene.play(FadeIn(top_text))

		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)
		scene.add(arrow)

		cur_count = 0
		for i in range(1, self.get_population()+1):
			if winner.get_color() == self.get_votes()[i].get_color():
				scene.play(
					Transform(count_num, Text(str(cur_count+1)).next_to(count_text, RIGHT, buff=1)),
					run_time=run_time
				)
				cur_count += 1

			scene.play(arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2), run_time=run_time)

		if cur_count > self.get_population()/2:
			scene.play(
				count_num.animate.set_color(GREEN)
			)
			scene.play(
				Transform(outcome[0], Text("Actual winner: ", font_size=24).move_to(ORIGIN).shift(DOWN*3.5))
			)
			scene.play(
				outcome.animate.move_to(ORIGIN)
			)
		else:
			scene.play(
				count_num.animate.set_color(RED)
			)
			scene.play(
				FadeOut(winner),
				Transform(outcome[0], Text("There is no majority element", font_size=24))
			)
		scene.wait(2)


	def create_rects(self, scene):
		# Candidate and count rectangles
		candidate_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)
		count_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)

		count_rect.next_to(candidate_rect, RIGHT, buff=2)

		cand_text = Text("Candidate", font_size=24).move_to(candidate_rect.get_center()).shift(UP*0.25)
		cand_dot = Dot(color=WHITE, radius=0.2).move_to(candidate_rect.get_center()).shift(DOWN*0.25).set_opacity(0)
		count_text = Text("Count", font_size=24).move_to(count_rect.get_center()).shift(UP*0.25)
		count_num = Text("0", font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)

		rects = VGroup(candidate_rect, count_rect, cand_text, cand_dot, count_text, count_num).move_to(ORIGIN + UP)

		scene.play(Create(candidate_rect), Create(count_rect), Write(cand_text), Write(count_text), Write(count_num))
		scene.wait(1)

		return rects, candidate_rect, count_rect, cand_text, cand_dot, count_text, count_num


	def animate_bm(self, scene, order, run_time):
		self.create_votes(scene, order)

		rects, candidate_rect, count_rect, cand_text, cand_dot, count_text, count_num = self.create_rects(scene)

		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)
		scene.add(arrow)

		cur_count = 0
		for i in range(1, self.get_population()+1):
			
			if i > 1:
				if cand_dot.get_color() != self.get_votes()[i].get_color():
					scene.play(
						Transform(count_num, Text(str(cur_count-1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
						run_time=run_time
					)
					cur_count -= 1
				else:
					scene.play(
						Transform(count_num, Text(str(cur_count+1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
						run_time=run_time
					)
					cur_count += 1

			if cur_count == 0:
				scene.play(
					cand_dot.animate.set_color(self.get_votes()[i].get_color()).set_opacity(1),
					Transform(count_num, Text("1", font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
					run_time=run_time
				)
				cur_count = 1

			if i < self.get_population(): 
				scene.play(arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2), run_time=run_time)


		outcome = VGroup()
		winner = Dot(color=cand_dot.get_color(), radius=0.2)		
		win_text = Text("Potential winner: ", font_size=24)
		winner.next_to(win_text, RIGHT, buff=1)
		outcome.add(win_text, winner)
	
		outcome.move_to(ORIGIN).shift(DOWN*3.5)
		scene.play(Write(outcome))
		scene.wait(3)

		scene.play(FadeOut(rects), FadeOut(arrow))
		self.pass_through(scene, outcome, run_time)


	def animate_pass(self, scene, order, run_time):
		self.create_votes(scene, order)

		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)
		scene.add(arrow)

		for i in range(1, self.get_population()+1):
			scene.play(arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2), run_time=run_time)

		scene.wait(2)
		scene.play(FadeOut(self.get_votes(), arrow))


	def create_votes(self, scene, order, scale=1.4):
		self.show_votes(scene, order)

		if self.get_population() < 20:
			self.get_votes().scale(scale)

		scene.play(Create(self.get_votes()))
		scene.wait(1)


	def animate_bm_proof(self, scene, order, run_time, draw_votes=True):
		if draw_votes:
			self.create_votes(scene, order, scale=1.8)

		rects, candidate_rect, count_rect, cand_text, cand_dot, count_text, count_num = self.create_rects(scene)

		arrow = Arrow(start=DOWN, end=ORIGIN, color=WHITE, stroke_width=8).next_to(self.get_votes()[1], DOWN, buff=0.2)
		scene.add(arrow)

		cur_count = 0
		removed = []
		lines = VGroup()
		for i in range(1, self.get_population()+1):
			
			if i > 1:
				if cand_dot.get_color() != self.get_votes()[i].get_color():
					scene.play(
						Transform(count_num, Text(str(cur_count-1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
						run_time=run_time
					)

					j = i-1
					while j in removed:
						j -= 1

					if j != 0:
						line1 = Line(start=self.get_votes()[i].get_center()+LEFT*0.5+DOWN*0.5, end=self.get_votes()[i].get_center()+RIGHT*0.5+UP*0.5, color=RED, stroke_width=8)
						line2 = Line(start=self.get_votes()[j].get_center()+LEFT*0.5+DOWN*0.5, end=self.get_votes()[j].get_center()+RIGHT*0.5+UP*0.5, color=RED, stroke_width=8)
						lines.add(line1, line2)

						scene.play(
							FadeIn(line1),
							FadeIn(line2)
						)
						scene.wait(3)

						removed.append(i)
						removed.append(j)

					cur_count -= 1
				else:
					scene.play(
						Transform(count_num, Text(str(cur_count+1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
						run_time=run_time
					)
					cur_count += 1		


			if cur_count == 0:
				scene.play(
					cand_dot.animate.set_color(self.get_votes()[i].get_color()).set_opacity(1),
					Transform(count_num, Text("1", font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)),
					run_time=run_time
				)
				cur_count = 1

			if i < self.get_population(): 
				scene.play(arrow.animate.next_to(self.get_votes()[i+1], DOWN, buff=0.2), run_time=run_time)

		scene.play(FadeOut(rects), FadeOut(arrow), FadeOut(lines))


	def shuffle(self, scene, new_order):
		new_votes = VGroup()

		open_bracket = Text("[");
		close_bracket = Text("]").move_to(open_bracket.get_right() + RIGHT*0.2);
		new_votes.add(open_bracket, close_bracket)

		for i in range(0, len(new_order)):
			cur_dot = Dot(color=new_order[i], radius=0.2)				
			new_votes.insert(i+1, cur_dot)		

			cur_dot.move_to(new_votes[i].get_right() + RIGHT*cur_dot.get_width())	
			new_votes[-1].shift(RIGHT*1.5*cur_dot.get_width())
			new_votes.move_to(ORIGIN + DOWN*1.5)

		new_votes.scale(1.8)	
		scene.play(Transform(self.votes, new_votes))
		self.votes = new_votes
		scene.wait(1)


	def animate_majority(self, scene, order):
		self.create_votes(scene, order)

		line = Line(start=UP*3, end=DOWN*0.5, stroke_width=4, color=WHITE)
		scene.play(Create(line))

		for i in range(0, self.get_population()):
			side = random.uniform(0.5, 4)
			up = random.uniform(-0.5, 3)

			if order[i] == TEAL:
				scene.play(self.get_votes()[i+1].animate.move_to(LEFT*side + UP*up), run_time=0.3)

			else:
				scene.play(self.get_votes()[i+1].animate.move_to(RIGHT*side + UP*up), run_time=0.3)

		scene.play(FadeOut(self.get_votes()[0]), FadeOut(self.get_votes()[-1]))

		greater = MathTex("> \\frac{n}{2}").shift(DOWN*2 + LEFT*2)
		less = MathTex("< \\frac{n}{2}").shift(DOWN*2 + RIGHT*2)
		scene.play(Write(greater))
		scene.wait(2)
		scene.play(Write(less))

		p1, p2 = 0, 1
		removed = []
		while p1 < self.get_population() and p2 < self.get_population():
			if p1 not in removed:
				while p2 < self.get_population() and (order[p1] == order[p2] or p2 in removed):
					p2 += 1

				if p2 < self.get_population():
					removed.append(p1)
					removed.append(p2)
					scene.play(FadeOut(self.get_votes()[p1+1]), FadeOut(self.get_votes()[p2+1]))

			p1 += 1
			p2 = p1+1

		scene.wait(2)
		scene.play(Write(Text("Majority Element", font_size=24).shift(UP*3 + LEFT*3)))



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
		self.wait(1)
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
		v.animate_map(self, order, 1)



class HashmapNoMaj(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(10)
		order = [BLUE, GREEN, PINK, PINK, BLUE, BLUE, GREEN, PINK, GREEN, BLUE]	
		v.animate_map(self, order, 0.3)



class TimeComplexity(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		time_complexity = Text("Time complexity: O(n)", font_size=24).shift(UP)       
		self.play(Write(time_complexity), run_time=2)
		self.play(time_complexity[15:].animate.set_color(GREEN))

		self.wait(4)

		space_complexity = Text("Space complexity: O(n)", font_size=24).shift(UP*0.5)
		self.play(Write(space_complexity), run_time=2)       
		self.play(space_complexity[16:].animate.set_color(RED))

		self.wait(4)

		v = Votes(10)
		order = [BLUE, YELLOW, GREEN, PINK, RED, PURPLE, ORANGE, TEAL, GOLD, MAROON]	
		v.animate_map(self, order, 0.5)



class BoyerMoore(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		title_text = Text("Boyer Moore Majority Vote Algorithm").shift(UP*3)
		self.play(Write(title_text))

		time_complexity = Text("Time complexity: O(n), Space complexity: O(1)", font_size=24).shift(UP*2)       
		self.play(Write(time_complexity), run_time=2)
		self.play(time_complexity[15:19].animate.set_color(GREEN),
		    time_complexity[36:40].animate.set_color(GREEN))

		# Candidate and count rectangles
		candidate_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)
		count_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)

		count_rect.next_to(candidate_rect, RIGHT, buff=2)

		cand_text = Text("Candidate", font_size=24).move_to(candidate_rect.get_center()).shift(UP*0.25)
		count_text = Text("Count", font_size=24).move_to(count_rect.get_center()).shift(UP*0.25)

		rects = VGroup(candidate_rect, count_rect, cand_text, count_text).move_to(ORIGIN)


		# Candidate
		self.play(Create(candidate_rect), Write(cand_text))

		cand_dot = Dot(color=PINK, radius=0.2).move_to(candidate_rect.get_center()).shift(DOWN*0.25)
		self.play(FadeIn(cand_dot))
		self.play(cand_dot.animate.set_color(GREEN))
		self.play(cand_dot.animate.set_color(BLUE))
		rects.add(cand_dot)


		# Count
		self.play(Create(count_rect), Write(count_text))
		count_num = Text("1", font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)
		self.play(FadeIn(count_num))

		for i in range(0, 10):
			self.play(Transform(count_num, Text(str(i), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)), run_time=0.2)
		rects.add(count_num)

		self.wait(1)


		self.play(
			FadeOut(title_text), 
			FadeOut(time_complexity),
			rects.animate.shift(UP*2)
		)


		# Algorithm
		step_1 = Text("\n1. Start the count at 0.", font_size=20)     
		self.play(Write(step_1), run_time=2)
		self.play(Transform(count_num, Text(str(0), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)))

		step_2 = Text("\n2. For each element:", font_size=20).next_to(step_1, DOWN)       
		self.play(Write(step_2), run_time=2)		

		step_2a = Text("\na. If the current element is equal to the candidate,\nincrement the count.", font_size=20).shift(UP*2).next_to(step_2, DOWN)             
		self.play(Write(step_2a), run_time=2)
		self.play(
			Transform(count_num, Text(str(2), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)

		step_2b = Text("\nb. If the current element is not equal to the candidate,\ndecrement the count.", font_size=20).shift(UP*2).next_to(step_2a, DOWN)         
		self.play(Write(step_2b), run_time=2)
		self.play(
			Transform(count_num, Text(str(1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)

		step_2c = Text("\nc. If the count is 0, the current element becomes the\ncandidate and set the count to 1.", font_size=20).next_to(step_2b, DOWN)            
		self.play(Write(step_2c), run_time=2)
		self.play(
			cand_dot.animate.set_color(GREEN),
			Transform(count_num, Text(str(1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)

		step_3 = Text("\n3. Check the number of votes of the reported candidate is\na majority. If so, return that candidate.", font_size=20).next_to(step_2c, DOWN)            
		self.play(Write(step_3), run_time=2)
		self.wait(3)



class BMAnim(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(10)
		order = [PINK, GREEN, PINK, PINK, PINK, BLUE, GREEN, PINK, PINK, BLUE]	
		v.animate_bm(self, order, 1)



class BMNoMaj(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		# Algorithm
		step_1 = Text("\n1. Start the count at 0.", font_size=20)     	
		step_2 = Text("\n2. For each element:", font_size=20).next_to(step_1, DOWN)       
		step_2a = Text("\na. If the current element is equal to the candidate,\nincrement the count.", font_size=20).shift(UP*2).next_to(step_2, DOWN)             
		step_2b = Text("\nb. If the current element is not equal to the candidate,\ndecrement the count.", font_size=20).shift(UP*2).next_to(step_2a, DOWN)         
		step_2c = Text("\nc. If the count is 0, the current element becomes the\ncandidate and set the count to 1.", font_size=20).next_to(step_2b, DOWN)            
		step_3 = Text("\n3. Check the number of votes of the reported candidate is\na majority. If so, return that candidate.", font_size=20).next_to(step_2c, DOWN)

		algorithm = VGroup(step_1, step_2, step_2a, step_2b, step_2c, step_3).move_to(ORIGIN)
		self.play(FadeIn(algorithm))     
		self.wait(2)
		self.play(step_3.animate.set_color(TEAL))       
		self.wait(5)
		self.play(FadeOut(algorithm))

		v = Votes(10)
		order = [BLUE, GREEN, PINK, PINK, BLUE, BLUE, GREEN, PINK, GREEN, BLUE]
		v.animate_bm(self, order, 0.5)



class BMLargerExample(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(20)
		order = [TEAL, TEAL, GOLD, MAROON, GOLD, TEAL, TEAL, PURPLE, MAROON, GOLD, GOLD, TEAL, TEAL, TEAL, TEAL, TEAL, GOLD, TEAL, TEAL, PURPLE]	
		v.animate_bm(self, order, 0.8)



class BMComplexity(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		time_complexity = Text("Space complexity: O(1)", font_size=24).shift(UP*2)       
		self.play(Write(time_complexity), run_time=2)

		# Candidate and count rectangles
		candidate_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)
		count_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		)

		count_rect.next_to(candidate_rect, RIGHT, buff=2)

		cand_text = Text("Candidate", font_size=24).move_to(candidate_rect.get_center()).shift(UP*0.25)
		count_text = Text("Count", font_size=24).move_to(count_rect.get_center()).shift(UP*0.25)

		rects = VGroup(candidate_rect, count_rect, cand_text, count_text).move_to(ORIGIN)
		self.play(Create(candidate_rect), Write(cand_text), Create(count_rect), Write(count_text))

		cand_dot = Dot(color=PINK, radius=0.2).move_to(candidate_rect.get_center()).shift(DOWN*0.25)
		count_num = Text("1", font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)

		self.play(FadeIn(cand_dot), run_time=0.2)
		self.play(cand_dot.animate.set_color(GREEN), run_time=0.2)
		self.play(cand_dot.animate.set_color(BLUE), run_time=0.2)
		rects.add(cand_dot)

		self.play(FadeIn(count_num), run_time=0.2)
		for i in range(0, 10):
			self.play(Transform(count_num, Text(str(i), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)), run_time=0.1)
		rects.add(count_num)

		self.wait(1)
		self.play(
			FadeOut(rects)
		)
		

		# Counter
		count_text = Text("Count: ")
		count_num = Text("0").next_to(count_text, RIGHT, buff=1)
		top_text = VGroup(count_text, count_num)
		top_text.move_to(ORIGIN)

		self.play(FadeIn(top_text))
		for i in range(0, 10):
			self.play(
				Transform(count_num, Text(str(i+1)).next_to(count_text, RIGHT, buff=1)),
				run_time=0.1
			)

		self.wait(1)
		self.play(
			FadeOut(top_text)
		)


		# Time complexity
		self.play(Transform(time_complexity, Text("Time complexity: O(n)", font_size=24).shift(UP*3)))

		v = Votes(20)
		order = [MAROON, ORANGE, LIGHT_PINK, TEAL, ORANGE, GREEN, ORANGE, ORANGE, MAROON, ORANGE, ORANGE, TEAL, ORANGE, ORANGE, MAROON, ORANGE, ORANGE, GREEN, ORANGE, LIGHT_PINK]	
		v.animate_bm(self, order, 0.05)



class BMProof(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(2)
		order = [TEAL, ORANGE]
		v.animate_bm_proof(self, order, 1)



class BMProof2(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(3)
		order = [TEAL, ORANGE, TEAL]
		v.animate_bm_proof(self, order, 1)

		self.wait(3)



class BMProof3(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(5)
		order = [MAROON, MAROON, GREEN, MAROON, GREEN]
		v.animate_bm_proof(self, order, 1)

		self.wait(3)

		new_order = [GREEN, GREEN, MAROON, MAROON, MAROON]
		v.shuffle(self, new_order)

		v.animate_bm_proof(self, new_order, 1, draw_votes=False)		



class BMProof4(Scene):
	def construct(self):
		Text.set_default(font="Consolas")

		v = Votes(11)
		order = [TEAL, TEAL, LIGHT_PINK, TEAL, LIGHT_PINK, TEAL, TEAL, LIGHT_PINK, TEAL, LIGHT_PINK, LIGHT_PINK]
		v.animate_majority(self, order)

		self.wait(3)



class SourceCode(Scene):  
    def construct(self):
        Text.set_default(font="Consolas")

        code = Code(
            code="""// Boyer Moore's Majority Vote algorithm written in C++
// Returns the majority element if there is one, or -1
int boyerMoore(vector<int>& nums) {
    int n = nums.size(), target = nums.size()/2+1, count = 1, candidate = nums[0];

    for (int i = 1; i < n; i++) {           
        if (nums[i] == candidate) {
            count += 1;
        } else {
            count -= 1;
        }
        if (count == 0) {
            candidate = nums[i];
            count = 1;
        }
    }

    int cur = 0;
    for (int i = 0; i < n; i++) {
    	if (nums[i] == candidate) {
    		cur += 1;
    	}
    	if (cur == target) {
    		return candidate;
    	}
    }

    return -1;
}""",
            language="C++",
            font_size=14,
            background="window"
        )
        
        # Add the code to the scene
        self.play(Write(code), run_time=5)
        self.wait(10)
        self.play(FadeOut(code))



class DrawAndGlowLetter(Scene):
    def construct(self):
        Text.set_default(font="Consolas")

        self.play(Write(Text("Thank you for watching!").shift(UP*2)))

        letter_e = Text("e", font_size=200, color=TEAL)
        self.play(Write(letter_e))

        letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
        glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
        self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
        self.play(FadeOut(letter_e_stroke, glow_effect))

        self.wait(3)
