from manim import *
from BMClass import Votes
import random

config.background_color = "#15131c"


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
		step_1 = Text("\n1. Initialise candidate = votes[0], count = 1", font_size=20)     	
		step_2 = Text("\n2. For each element i:", font_size=20).next_to(step_1, DOWN)       
		step_2a = Text("\na. If votes[i] == candidate: count = count+1", font_size=20).shift(UP*2).next_to(step_2, DOWN)             
		step_2b = Text("\nb. If votes[i] != candidate: count = count-1", font_size=20).shift(UP*2).next_to(step_2a, DOWN)         
		step_2c = Text("\nc. If count == 0: candidate = votes[i], count = 1", font_size=20).next_to(step_2b, DOWN)            
		step_3 = Text("\n3. Check the number of votes of the reported candidate is a majority.\nIf so, return that candidate.", font_size=20).next_to(step_2c, DOWN)

		self.play(Write(step_1), run_time=2)
		self.play(Transform(count_num, Text(str(1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25)))
		self.play(Write(step_2), run_time=2)
		self.play(Write(step_2a), run_time=2)
		self.play(
			Transform(count_num, Text(str(2), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)
		self.play(Write(step_2b), run_time=2)
		self.play(
			Transform(count_num, Text(str(1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)
		self.play(Write(step_2c), run_time=2)
		self.play(
			cand_dot.animate.set_color(GREEN),
			Transform(count_num, Text(str(1), font_size=30).move_to(count_rect.get_center()).shift(DOWN*0.25))
		)
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
		step_1 = Text("\n1. Initialise candidate = votes[0], count = 1", font_size=20)     	
		step_2 = Text("\n2. For each element i:", font_size=20).next_to(step_1, DOWN)       
		step_2a = Text("\na. If votes[i] == candidate: count = count+1", font_size=20).shift(UP*2).next_to(step_2, DOWN)             
		step_2b = Text("\nb. If votes[i] != candidate: count = count-1", font_size=20).shift(UP*2).next_to(step_2a, DOWN)         
		step_2c = Text("\nc. If count == 0: candidate = votes[i], count = 1", font_size=20).next_to(step_2b, DOWN)            
		step_3 = Text("\n3. Check the number of votes of the reported candidate is a majority.\nIf so, return that candidate.", font_size=20).next_to(step_2c, DOWN)

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

		new_order = [MAROON, GREEN, GREEN, MAROON, MAROON]
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
            code="""// Boyer Moore Majority Vote algorithm written in C++
// Returns the majority element if there is one
int boyerMoore(vector<int>& nums) {
    int n = nums.size(), target = n/2+1;
    int count = 1, candidate = nums[0];

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
            font_size=16,
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
