from manim import *
from Leaderboard import Board


config.background_color = "#15131c"


class Leaderboard(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [6, 4, 4, 2]
		l = [0, 2, 4, 6]
		r = [4, 4, 2, 2]
		g = [[0, 3, 1, 0], [3, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]

		
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
		question_group -= surround
		self.wait(2)


		# Show the last place team cannot win
		surround = lb.put_rectangle_around(self, 4)
		lb.increment_wins(self, 4, 4)
		self.play(Uncreate(surround))
		self.wait(2)		

		lb.swap_rows(self, 4, 2)
		self.wait(2)

		# Eliminate the team
		lb.set_row_color(self, 2, RED)

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("is trivially eliminated", font_size=24)
		eliminated_group = VGroup(eliminated_team, eliminated_text).arrange().move_to(UP*3).scale(0.8)
		self.play(
			Transform(question_group, eliminated_group)
		)
		self.wait(2)

		lb.fade_out_row(self, 2)
		self.wait(2)


		what_about_team = lb.teams[2].copy()
		what_about_text = Text("What about", font_size=24)
		question_mark = Text("?", font_size=24)
		what_about_group = VGroup(what_about_text, what_about_team, question_mark).arrange().move_to(UP*3).scale(0.8)
		self.play(
			Transform(question_group, what_about_group)
		)
		self.wait(2)


		# Show the third place team cannot win
		surround = lb.put_rectangle_around(self, 3)
		lb.increment_wins_2(self, 3, 6)
		self.play(Uncreate(surround))
		self.wait(2)

		lb.swap_rows(self, 3, 1)
		self.wait(2)

		surround = lb.put_rectangle_around(self, 2)
		self.play(lb.grid[2][5].animate.set_color(lb.teams[1].get_color()))
		self.wait(2)

		rect2 = lb.put_rectangle_around_2(self, [2, 3])
		self.play(Transform(surround, rect2))
		self.wait(2)

		lb.increment_losses_2(self, 2, 4)
		self.play(Uncreate(surround))
		self.wait(2)

		lb.swap_rows(self, 3, 1)
		self.wait(2)


		no_win_team = lb.teams[2].copy()
		no_win_text = Text("cannot win", font_size=24)
		no_win_group = VGroup(no_win_team, no_win_text).arrange().move_to(UP*3).scale(0.8)
		self.play(
			Transform(question_group, no_win_group)
		)
		self.wait(2)

