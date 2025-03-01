from manim import *
from Leaderboard import Board
from FlowNetwork import FlowNetwork, BaseballNetwork


config.background_color = "#15131c"



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



class HarderExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [22, 20, 19, 19]
		l = None
		r = [6, 7, 9, 4]
		g = [[0, 3, 2, 1], [3, 0, 4, 0], [2, 4, 0, 3], [1, 0, 3, 0]]
		t = [[MAROON, RED, GOLD, YELLOW], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.8)), run_time=2)
		self.wait(2)


		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Can you show ", font_size=24)
		eliminated_text_2 = Text(" has no chance of winning?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*3).scale(0.8)
		self.play(
			Write(eliminated_text),
			Write(eliminated_text_2),
			Create(eliminated_team)
		)
		self.wait(2)



class BaseballIntro(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title_text = Text("Baseball Elimination Problem").shift(UP*3)
		self.play(Write(title_text))

		max_flow_text = Text("max flow application", font_size=24).shift(UP*2)       
		self.play(Write(max_flow_text))

		# [N1 -> N2, weight]
		edge_list = [[0, 1, 10], [0, 2, 12], [0, 3, 4], [1, 4, 3], [1, 2, 6], [3, 5, 7], [2, 6, 9], [4, 6, 10], [5, 6, 5]]
		positions = [[-5, 0], [-1, -0.5], [1, 2], [-2, -2], [1.5, -0.5], [3, -2], [5, 0]]
		fn = FlowNetwork(edge_list, positions)
		fn.create_network(0.9, DOWN*1)
		self.wait(2)

		src_node = Dot(color=TEAL, radius=0.2)
		src_text = Text("source (s)", font_size=24)
		src_group = VGroup(src_node, src_text).arrange()

		sink_node = Dot(color=ORANGE, radius=0.2)
		sink_text = Text("sink (t)", font_size=24)
		sink_group = VGroup(sink_node, sink_text).arrange()

		src_sink = VGroup(src_group, sink_group).arrange(buff=0.5).shift(UP*2)

		max_flow_title = Text("Max Flow").shift(UP*3)
		self.play(Transform(max_flow_text, src_sink), Transform(title_text, max_flow_title))

		fn.bfs_animation(self)
		self.wait(2)

		question_text = Text("What is the maximum flow that can reach", font_size=24)
		question_mark = Text("?", font_size=24)
		question_group = VGroup(question_text, sink_node, question_mark).arrange(buff=0.5).shift(UP*2)
		
		self.play(Transform(max_flow_text, question_group))
		self.wait(2)

		self.play(FadeOut(fn.network))
		self.wait(2)

		edge_list = [[0, 1, 5], [1, 3, 3], [0, 2, 2], [2, 3, 4]]
		positions = [[-3, 0], [0, 2], [0, -2], [3, 0]]
		fn2 = FlowNetwork(edge_list, positions)
		fn2.create_network(1, DOWN*1)
		fn2.bfs_animation(self)
		self.wait(2)

		fn2.flow_animation(self)
		self.wait(2)

		max_flow_calc = Text("max flow = 3 + 2 = 5", font_size=24).shift(UP*2)
		self.play(Transform(max_flow_text, max_flow_calc))
		self.wait(2)



class MaxFlowMinCut(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		max_flow_title = Text("Max Flow").shift(UP*3)
		self.add(max_flow_title)

		mfmc_text = Text("max flow = min cut", color=WHITE, font_size=36)
		mfmc_text[8:11].set_color(LIGHT_PINK)
		mfmc_text[11:14].set_color(PURPLE)
		self.play(Write(mfmc_text))
		self.wait(2)
		
		cut_text = Text("set of edges whose removal\ndisconnects source from sink", color=PURPLE, font_size=24).move_to(mfmc_text.get_center() + UP*1.1 + RIGHT*3.5)
		self.play(Write(cut_text))
		self.wait(2)

		min_text = Text("smallest total\nof edge weights", color=LIGHT_PINK, font_size=24).move_to(mfmc_text.get_center() + DOWN*1.1)
		self.play(Write(min_text))
		self.wait(2)

		self.play(FadeOut(cut_text), FadeOut(min_text), mfmc_text.animate.scale(0.8).move_to(UP*2))
		self.wait(2)


		edge_list = [[0, 1, 5], [1, 3, 3], [0, 2, 2], [2, 3, 4]]
		positions = [[-3, 0], [0, 2], [0, -2], [3, 0]]
		fn2 = FlowNetwork(edge_list, positions)
		fn2.create_network(0.9, DOWN*1.5)
		fn2.bfs_animation(self)
		self.wait(2)


		fn2.remove_edges_put_back(self, [[0, 1], [2, 3]])
		fn2.remove_edges_put_back(self, [[0, 1], [0, 2]])
		fn2.remove_edges_put_back(self, [[0, 2], [1, 3]])
		fn2.remove_edges_put_back(self, [[1, 3], [2, 3]])


		fn2.min_cut_animation(self, [[0, 2], [1, 3]])
		self.wait(2)

		self.remove(fn2.network)
		self.wait(2)		



class MaxFlowMinCut2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		max_flow_title = Text("Max Flow").shift(UP*3)
		self.add(max_flow_title)

		mfmc_text = Text("max flow = min cut", color=WHITE, font_size=36).scale(0.8).move_to(UP*2)
		mfmc_text[8:11].set_color(LIGHT_PINK)
		mfmc_text[11:14].set_color(PURPLE)
		self.add(mfmc_text)
		self.wait(2)

		edge_list = [[0, 1, 10], [0, 2, 12], [0, 3, 4], [1, 4, 3], [1, 2, 6], [3, 5, 7], [2, 6, 9], [4, 6, 10], [5, 6, 5]]
		positions = [[-5, 0], [-1, -0.5], [1, 2], [-2, -2], [1.5, -0.5], [3, -2], [5, 0]]
		fn = FlowNetwork(edge_list, positions)
		fn.create_network(0.9, DOWN*1.5)
		fn.bfs_animation(self)
		self.wait(2)

		fn.min_cut_animation(self, [[0, 3], [1, 4], [2, 6]])
		self.wait(2)



class BaseballWalkthrough(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [22, 20, 19, 19]
		l = None
		r = [6, 7, 9, 4]
		g = [[0, 3, 2, 1], [3, 0, 4, 0], [2, 4, 0, 3], [1, 0, 3, 0]]
		t = [[MAROON, RED, GOLD, YELLOW], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.8)), run_time=2)
		self.wait(2)

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Is ", font_size=24)
		eliminated_text_2 = Text(" eliminated?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*3).scale(0.8)
		self.play(
			Write(eliminated_text),
			Write(eliminated_text_2),
			Create(eliminated_team)
		)
		self.wait(2)

		rect = lb.put_rectangle_around(self, 4)
		board = VGroup(lb.grid, rect)
		self.play(
			board.animate.scale(0.4).move_to(UP*2 + LEFT*5),
			eliminated_group.animate.move_to(UP*3.5 + LEFT*5)
		)

		line = Line(UP*3 + LEFT*2.5, DOWN*3 + LEFT*2.5)
		self.play(Create(line))

		fn = BaseballNetwork(w, r, g, lb.teams, 3)
		fn.create_network(0.7, RIGHT*2.25)		
		fn.draw_source_sink(self)

		game_vertices_text = Text("Create game vertices representing\ngames.", font_size=24).scale(0.5).next_to(board, DOWN)
		self.play(Write(game_vertices_text))
		self.wait(2)
		fn.draw_vertices(self, "game")
		self.wait(2)

		game_capacity_text = Text("Set capacity to number of remaining\ngames between those teams.", font_size=24).scale(0.5).next_to(game_vertices_text, DOWN)
		self.play(Write(game_capacity_text))
		self.wait(2)
		fn.draw_edges(self, "game")
		self.wait(2)

		team_vertices_text = Text("Create team vertices representing\nthe winners of the game vertices.", font_size=24).scale(0.5).next_to(game_capacity_text, DOWN)
		self.play(Write(team_vertices_text))
		self.wait(2)
		fn.draw_vertices(self, "team")
		self.wait(2)

		team_capacity_text = Text("Don't restrict flow from game to\nteam vertices.", font_size=24).scale(0.5).next_to(team_vertices_text, DOWN)
		self.play(Write(team_capacity_text))
		self.wait(2)
		fn.draw_edges(self, "team")
		self.wait(2)

		sink_capacity_text = Text("Set capacity of team vertices to\nsink:\n- Maximum number of wins so that\nthis team doesn't overtake the\nteam we are checking (k).\n- capacity = w[k]+r[k]-w[i]", font_size=24).scale(0.5).next_to(team_capacity_text, DOWN)
		self.play(Write(sink_capacity_text))
		self.wait(2)
		fn.draw_edges(self, "sink")
		self.wait(2)

		win_text = Text("Team is eliminated if:\nmax flow < num remaining games", font_size=24).scale(0.5).next_to(sink_capacity_text, DOWN)
		self.play(Write(win_text))
		self.wait(2)
		fn.highlight_edges(self, "game")
		self.wait(2)
		self.play(fn.network.animate.shift(DOWN*0.5))
		fn.num_remaining_animation(self)
		self.wait(2)
		fn.min_cut_animation(self, "team")
		self.wait(2)

		max_flow_text = Text("max flow < num remaining games", color=BLACK, font_size=24)
		max_flow_team = lb.teams[3].copy().scale(1.5)
		max_flow_text_2 = Text("is eliminated", color=BLACK, font_size=24)
		max_flow_group_2 = VGroup(max_flow_team, max_flow_text_2).arrange()
		max_flow_group = VGroup(max_flow_text, max_flow_group_2).arrange(DOWN)

		surround = BackgroundRectangle(max_flow_group, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2).move_to(ORIGIN)
		self.play(
			Create(surround),
			Write(max_flow_text)
		)
		self.play(
			Write(max_flow_text_2),
			Create(max_flow_team)
		)
		self.wait(2)

		self.play(
			FadeOut(surround, max_flow_group)
		)



class BaseballFlow(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [22, 20, 19, 19]
		l = None
		r = [6, 7, 9, 4]
		g = [[0, 3, 2, 1], [3, 0, 4, 0], [2, 4, 0, 3], [1, 0, 3, 0]]
		t = [[MAROON, RED, GOLD, YELLOW], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()
		lb.grid.scale(0.8)

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Is ", font_size=24)
		eliminated_text_2 = Text(" eliminated?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*3).scale(0.8)
		self.add(
			eliminated_text,
			eliminated_text_2,
			eliminated_team
		)

		rect = lb.add_rectangle_around(self, 4)
		board = VGroup(lb.grid, rect)
		self.add(
			board.scale(0.4).move_to(UP*2 + LEFT*5),
			eliminated_group.move_to(UP*3.5 + LEFT*5)
		)

		line = Line(UP*3 + LEFT*2.5, DOWN*3 + LEFT*2.5)
		self.add(line)

		fn = BaseballNetwork(w, r, g, lb.teams, 3)
		fn.create_network(0.7, RIGHT*2.25+DOWN*0.5)		
		self.add(fn.network)

		game_vertices_text = Text("Create game vertices representing\ngames.", font_size=24).scale(0.5).next_to(board, DOWN)
		self.add(game_vertices_text)

		game_capacity_text = Text("Set capacity to number of remaining\ngames between those teams.", font_size=24).scale(0.5).next_to(game_vertices_text, DOWN)
		self.add(game_capacity_text)

		team_vertices_text = Text("Create team vertices representing\nthe winners of the game vertices.", font_size=24).scale(0.5).next_to(game_capacity_text, DOWN)
		self.add(team_vertices_text)
		
		team_capacity_text = Text("Don't restrict flow from game to\nteam vertices.", font_size=24).scale(0.5).next_to(team_vertices_text, DOWN)
		self.add(team_capacity_text)

		sink_capacity_text = Text("Set capacity of team vertices to\nsink:\n- Maximum number of wins so that\nthis team doesn't overtake the\nteam we are checking (k).\n- capacity = w[k]+r[k]-w[i]", font_size=24).scale(0.5).next_to(team_capacity_text, DOWN)
		self.add(sink_capacity_text)

		win_text = Text("Team is eliminated if:\nmax flow < num remaining games", font_size=24).scale(0.5).next_to(sink_capacity_text, DOWN)
		self.add(win_text)

		fn.num_remaining_animation(self)
		fn.min_cut_animation(self, "team")
		fn.turn_white("team")
		self.wait(2)

		fn.highlight_edges(self, "team")
		self.wait(2)
		fn.highlight_edges(self, "game")
		self.wait(2)

		lb.win_games(self, [3, 0], [1, 0])
		lb.win_games(self, [3, 2], [3, 0])
		self.wait(2)

		edge_list = [[[fn.game_edges[0], 3]], [[fn.game_to_team[0], 1], [fn.team_edges[0], 1]], [[fn.game_to_team[1], 2], [fn.team_edges[1], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 1], [1, 2])
		self.wait(2)

		edge_list = [[[fn.game_edges[1], 2]], [[fn.game_to_team[3], 2]], [[fn.team_edges[2], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 2], [0, 2])
		self.wait(2)

		edge_list = [[[fn.game_edges[2], 4]], [[fn.game_to_team[4], 1], [fn.team_edges[1], 1]], [[fn.game_to_team[5], 3], [fn.team_edges[2], 3]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [1, 2], [1, 3])
		self.wait(2)

		fn.make_edges_colour([fn.team_edges[2]], RED)
		self.wait(2)

		win_team = lb.teams[3].copy()
		win_text = Text(" cannot win", font_size=24)
		win_group = VGroup(win_team, win_text).arrange().move_to(LEFT*5 + UP*3.5).scale(0.8)
		self.play(
			Transform(eliminated_group, win_group),
			Uncreate(rect)
		)
		self.wait(2)

		lb.swap_rows(self, 3, 1)
		self.wait(2)



class BaseballExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [7, 5, 3, 2, 2]
		l = None
		r = [5, 6, 6, 5, 6]
		g = [[0, 2, 1, 1, 1], [2, 0, 2, 1, 1], [1, 2, 0, 1, 2], [1, 1, 1, 0, 2], [1, 1, 2, 2, 0]]
		t = [[MAROON, LIGHT_PINK, PURPLE, BLUE, TEAL], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4), RegularPolygon(n=6)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()

		self.play(Create(lb.grid.scale(0.8)), run_time=2)
		self.wait(2)

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Is ", font_size=24)
		eliminated_text_2 = Text(" eliminated?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*3.5).scale(0.8)
		self.play(
			Write(eliminated_text),
			Write(eliminated_text_2),
			Create(eliminated_team)
		)
		self.wait(2)

		rect = lb.put_rectangle_around(self, 4)
		board = VGroup(lb.grid, rect)
		self.play(
			board.animate.scale(0.4).move_to(LEFT*5),
			eliminated_group.animate.move_to(LEFT*5 + UP*2)
		)

		line = Line(UP*3 + LEFT*2.5, DOWN*3 + LEFT*2.5)
		self.play(Create(line))

		fn = BaseballNetwork(w, r, g, lb.teams, 3)
		fn.create_network(0.7, RIGHT*2.25)		
		fn.draw_source_sink(self)
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

		fn.highlight_edges(self, "game")
		self.wait(2)

		self.play(fn.network.animate.shift(DOWN*0.5))
		fn.num_remaining_animation(self)
		self.wait(2)
		fn.min_cut_animation(self, "game")
		self.wait(2)

		max_flow_text = Text("max flow = num remaining games", color=BLACK, font_size=24)
		max_flow_team = lb.teams[3].copy().scale(1.5)
		max_flow_text_2 = Text("has a chance of winning", color=BLACK, font_size=24)
		max_flow_group_2 = VGroup(max_flow_team, max_flow_text_2).arrange()
		max_flow_group = VGroup(max_flow_text, max_flow_group_2).arrange(DOWN)

		surround = BackgroundRectangle(max_flow_group, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2).move_to(ORIGIN)
		self.play(
			Create(surround),
			Write(max_flow_text)
		)
		self.play(
			Write(max_flow_text_2),
			Create(max_flow_team)
		)
		self.wait(2)

		self.play(
			FadeOut(surround, max_flow_group)
		)

		fn.make_edges_colour(fn.game_edges, WHITE)
		self.wait(2)

		lb.win_games(self, [3, 0], [1, 0])
		lb.win_games(self, [3, 1], [1, 0])
		lb.win_games(self, [3, 2], [1, 0])
		lb.win_games(self, [3, 4], [2, 0])
		self.wait(2)

		edge_list = [[[fn.game_edges[0], 2]], [[fn.game_to_team[1], 2], [fn.team_edges[1], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 1], [0, 2])
		self.wait(2)

		edge_list = [[[fn.game_edges[1], 1]], [[fn.game_to_team[3], 1], [fn.team_edges[2], 1]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 2], [0, 1])
		self.wait(2)

		edge_list = [[[fn.game_edges[2], 1]], [[fn.game_to_team[5], 1], [fn.team_edges[3], 1]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [0, 4], [0, 1])
		self.wait(2)

		edge_list = [[[fn.game_edges[3], 2]], [[fn.game_to_team[7], 2], [fn.team_edges[2], 2]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [1, 2], [0, 2])
		self.wait(2)

		edge_list = [[[fn.game_edges[4], 1]], [[fn.game_to_team[9], 1], [fn.team_edges[3], 1]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [1, 4], [0, 1])
		self.wait(2)

		edge_list = [[[fn.game_edges[5], 2]], [[fn.game_to_team[10], 1], [fn.team_edges[2], 1]], [[fn.game_to_team[11], 1], [fn.team_edges[3], 1]]]
		fn.flow_animate(self, edge_list)
		self.wait(2)

		lb.win_games(self, [2, 4], [1, 1])
		self.wait(2)

		win_team = lb.teams[3].copy()
		win_text = Text(" can win", font_size=24)
		win_group = VGroup(win_team, win_text).arrange().move_to(LEFT*5 + UP*2).scale(0.8)
		self.play(
			Transform(eliminated_group, win_group),
			Uncreate(rect)
		)
		self.wait(2)

		lb.swap_rows(self, 4, 1)
		self.wait(2)



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

		title_text = Text("Baseball Elimination Problem").shift(UP*3)
		self.add(title_text)

		w = [7, 5, 3, 2, 2]
		l = None
		r = [5, 6, 6, 5, 6]
		g = [[0, 2, 1, 1, 1], [2, 0, 2, 1, 1], [1, 2, 0, 1, 2], [1, 1, 1, 0, 2], [1, 1, 2, 2, 0]]
		t = [[MAROON, LIGHT_PINK, PURPLE, BLUE, TEAL], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4), RegularPolygon(n=6)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()
		self.add(lb.grid.scale(0.8).scale(0.4).move_to(LEFT*5).shift(DOWN*0.5))

		eliminated_team = lb.teams[3].copy()
		eliminated_text = Text("Is ", font_size=24)
		eliminated_text_2 = Text(" eliminated?", font_size=24)
		eliminated_group = VGroup(eliminated_text, eliminated_team, eliminated_text_2).arrange().move_to(UP*3.5).scale(0.8).move_to(LEFT*5 + UP*2)
		self.add(eliminated_group.shift(DOWN*0.5))

		line = Line(UP*3 + LEFT*2.5, DOWN*3 + LEFT*2.5)
		self.add(line.shift(DOWN*0.5))

		fn = BaseballNetwork(w, r, g, lb.teams, 3)
		fn.create_network(0.7, RIGHT*2.25)	
		self.add(fn.network.shift(DOWN*0.5))	



class CodeBackground(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		w = [7, 5, 3, 2, 2]
		l = None
		r = [5, 6, 6, 5, 6]
		g = [[0, 2, 1, 1, 1], [2, 0, 2, 1, 1], [1, 2, 0, 1, 2], [1, 1, 1, 0, 2], [1, 1, 2, 2, 0]]
		t = [[MAROON, LIGHT_PINK, PURPLE, BLUE, TEAL], [Square(), RegularPolygon(n=5), Triangle(), RegularPolygon(n=4), RegularPolygon(n=6)]]

		
		lb = Board(w, l, r, g, t)
		lb.create_grid()
		self.add(lb.grid.scale(0.8).scale(0.4).move_to(LEFT*4.5).shift(UP*2))

		fn = BaseballNetwork(w, r, g, lb.teams, 3)
		fn.create_network(0.7, RIGHT*2.25)	
		self.add(fn.network.move_to(LEFT*4.5).shift(DOWN*2).scale(0.5))	
