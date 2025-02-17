from manim import *
from Leaderboard import Board
from FlowNetwork import FlowNetwork


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
		mfmc_text[8:11].set_color(YELLOW)
		mfmc_text[11:14].set_color(PINK)
		self.play(Write(mfmc_text))
		self.wait(2)
		
		cut_text = Text("set of edges whose removal\ndisconnects source from sink", color=PINK, font_size=24).move_to(mfmc_text.get_center() + UP*1.1 + RIGHT*2)
		self.play(Write(cut_text))
		self.wait(2)

		min_text = Text("smallest total of\nedge weights", color=YELLOW, font_size=24).move_to(mfmc_text.get_center() + DOWN*1.1 + LEFT*0.5)
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


		edge_list = [[0, 1, 10], [0, 2, 12], [0, 3, 4], [1, 4, 3], [1, 2, 6], [3, 5, 7], [2, 6, 9], [4, 6, 10], [5, 6, 5]]
		positions = [[-5, 0], [-1, -0.5], [1, 2], [-2, -2], [1.5, -0.5], [3, -2], [5, 0]]
		fn = FlowNetwork(edge_list, positions)
		fn.create_network(0.9, DOWN*1.5)
		fn.bfs_animation(self)
		self.wait(2)

		fn.min_cut_animation(self, [[0, 3], [1, 4], [2, 6]])
		self.wait(2)




