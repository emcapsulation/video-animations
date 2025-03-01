from manim import *
from Leaderboard import Board
from FlowNetwork import FlowNetwork, BaseballNetwork


config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class Leaderboard(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [6, 4, 4, 2]
		l = [0, 2, 4, 6]
		r = [4, 4, 2, 2]
		g = [[0, 3, 1, 0], [3, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]
		t = [[LIGHT_PINK, PURPLE, BLUE, TEAL], [Circle(), Square(), Triangle(), RegularPolygon(n=4)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.65)), run_time=2)
		self.wait(5)


		# Question posed
		q_text = "Which teams have no chance of winning the season?"
		question = Text(q_text, color=BLACK, font_size=24)
		index = q_text.find("no")-3
		question[index:index+2].set_color(RED)

		surround = BackgroundRectangle(question, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		question_group = VGroup(surround, question).scale(0.65)
		self.play(FadeIn(question_group))
		self.wait(2)
		self.play(
			question_group.animate.move_to(UP*3),
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
		lb.increment_wins(self, 4, 4, scale=0.65)
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
		lb.increment_wins_2(self, 3, 6, scale=0.65)
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

		lb.increment_losses_2(self, 2, 4, scale=0.65)
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



class Walkthrough(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [22, 20, 19, 19]
		l = None
		r = [6, 7, 9, 4]
		g = [[0, 3, 2, 1], [3, 0, 4, 0], [2, 4, 0, 3], [1, 0, 3, 0]]
		t = [[MAROON, RED, GOLD, YELLOW], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.65)), run_time=2)
		self.wait(2)

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Can you show ", font_size=24)
		eliminated_text_2 = Text(" has no chance of winning?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*2.5).scale(0.75)
		self.play(
			Write(eliminated_text),
			Write(eliminated_text_2),
			Create(eliminated_team)
		)
		rect = lb.put_rectangle_around(self, 4)
		self.wait(2)


		title_text = Text("Baseball Elimination").shift(UP*5)
		title_text_2 = Text("Problem").shift(UP*4.5)
		title_group = VGroup(title_text, title_text_2)
		title_group.scale(0.8)
		self.play(Write(title_group))

		max_flow_text = Text("max flow application", font_size=24).shift(UP*4).scale(0.8)      
		self.play(Write(max_flow_text))
		self.wait(2)

		self.play(
			FadeOut(max_flow_text),
			title_group.animate.shift(UP),
			eliminated_group.animate.shift(UP*2),
			rect.animate.shift(UP*2.85).scale(0.75),
			lb.grid.animate.shift(UP*2.5).scale(0.8)
		)


		fn = BaseballNetwork(w, r, g, lb.teams, 3, font_size=24)
		fn.create_network(0.5, DOWN*3.5)		
		fn.draw_source_sink(self)
		self.wait(2)

		fn.draw_vertices(self, "game")
		self.wait(2)

		fn.draw_edges(self, "game")
		self.wait(2)

		fn.draw_vertices(self, "team")
		self.wait(2)

		fn.draw_edges(self, "team")
		self.wait(2)

		fn.draw_edges(self, "sink")
		self.wait(2)

		win_text = Text("Team is eliminated if max flow < num remaining games", font_size=24).scale(0.65).next_to(lb.grid, DOWN*2)
		win_text[18:].set_color(ORANGE)
		self.play(Write(win_text))
		self.wait(2)

		fn.highlight_edges(self, "game")
		self.wait(2)

		fn.num_remaining_animation(self)
		self.wait(2)

		fn.min_cut_animation(self, "team")
		self.wait(2)

		fn.make_edges_colour(fn.team_edges, WHITE)
		self.wait(2)


		lb.win_games(self, [3, 0], [1, 0], 0.65)
		lb.win_games(self, [3, 2], [3, 0], 0.65)
		self.wait(2)

		edge_list = [[[fn.game_edges[0], 3]], [[fn.game_to_team[0], 1], [fn.team_edges[0], 1]], [[fn.game_to_team[1], 2], [fn.team_edges[1], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 1], [1, 2], 0.65)
		self.wait(2)

		edge_list = [[[fn.game_edges[1], 2]], [[fn.game_to_team[3], 2]], [[fn.team_edges[2], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 2], [0, 2], 0.65)
		self.wait(2)

		edge_list = [[[fn.game_edges[2], 4]], [[fn.game_to_team[4], 1], [fn.team_edges[1], 1]], [[fn.game_to_team[5], 3], [fn.team_edges[2], 3]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [1, 2], [1, 3], 0.65)
		self.wait(2)

		fn.make_edges_colour([fn.team_edges[2]], RED)
		self.wait(2)

		win_team = lb.teams[3].copy()
		win_text = Text(" cannot win", font_size=24)
		win_group = VGroup(win_team, win_text).arrange().move_to(UP*2.5).scale(0.75).shift(UP*2)
		self.play(
			Transform(eliminated_group, win_group),
			Uncreate(rect)
		)
		self.wait(2)

		lb.swap_rows(self, 3, 1)
		self.wait(2)		