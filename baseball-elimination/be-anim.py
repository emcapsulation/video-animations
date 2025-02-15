from manim import *
from Leaderboard import Board


config.background_color = "#15131c"


class Leaderboard(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [5, 4, 4, 2]
		l = [1, 4, 2, 6]
		r = [4, 2, 4, 2]
		g = [[0, 1, 3, 0], [1, 0, 0, 1], [3, 0, 0, 1], [0, 1, 1, 0]]

		
		lb = Board(w, l, r, g)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.8)), run_time=2)
		self.wait(5)


		# Question posed
		q_text = "Which teams have no chance of winning the season?"
		question = Text(q_text, color=BLACK, font_size=24)
		index = q_text.find("no")-3
		question[index:index+2].set_color(RED)

		surround = BackgroundRectangle(question, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		question_group = VGroup(surround, question)
		self.play(FadeIn(question_group))
		self.wait(2)
		self.play(
			question_group.animate.move_to(UP*3).scale(0.8),
			lb.grid.animate.shift(DOWN*0.5)
		)
		self.play(
			question.animate.set_color(WHITE),
			FadeOut(surround)
		)
		self.wait(2)


		# Show the last place team cannot win
		lb.increment_wins(self, 4, 4)
		self.wait(2)

		lb.swap_rows(self, 4, 2)

