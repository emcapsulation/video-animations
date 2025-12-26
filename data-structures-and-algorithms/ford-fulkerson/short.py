from manim import *
from FlowNetwork import FlowNetwork

config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class FFMobile(Scene):

	def set_steps(self):
		Text.set_default(font="Monospace")

		self.steps = [
			[Text("Find an augmenting path (p) from source to sink", font_size=18, color=MAROON).move_to(UP*2)],
			[Text("Find the bottleneck capacity of the path (fb)", font_size=18, color=ORANGE).move_to(UP*2),
			Text("bottleneck = edge which can have the least", font_size=16, color=WHITE),
			Text("amount of flow pushed through it", font_size=16, color=WHITE)],
			[Text("Push fb flow units through each edge (e) in p", font_size=18, color=GOLD).move_to(UP*2),
			Text("if e is a forward edge:\n\tadd fb to the flow in e", font_size=16, color=WHITE),
			Text("if e is a backward edge:\n\tminus fb from the flow in\n\tthe corresponding forward edge", font_size=16, color=WHITE)],
			[Text("Build the residual graph (update back edges)", font_size=18, color=GREEN).move_to(UP*2),
			Text("for each edge (e) in p, insert a back edge", font_size=16, color=WHITE),
			Text("capacity of back edge = flow in forward edge", font_size=16, color=WHITE)],
			[Text("Return max flow when there are no more paths", font_size=18, color=BLUE).move_to(UP*2),
			Text("flow = sum of flows on edges leaving the source", font_size=16, color=WHITE),
			Text("= sum of flows on edges entering the sink", font_size=16, color=WHITE)]
		]


	def animate_steps(self, fn, path, fb_edge):	
		write_speed = 1

		step_text = Text("Find an augmenting path (p) from source to sink", font_size=18, color=MAROON).move_to(UP*2)
		self.play(Write(step_text), run_time=write_speed)

		fn.make_edges_colour(self, path, GREEN)

		next_step = self.steps[1][0]
		self.play(Transform(step_text, next_step), run_time=write_speed)

		step_text_1 = self.steps[1][1]
		step_text_2 = self.steps[1][2]
		step_desc = VGroup(step_text_1, step_text_2).arrange(DOWN).next_to(next_step, DOWN)		
		self.play(FadeIn(step_desc), run_time=write_speed)

		fb = fb_edge[0].capacity-fb_edge[0].flow_num
		b_neck_sum = str(fb_edge[0].capacity)
		if fb_edge[0].flow_num != 0:
			b_neck_sum += ' - ' + str(fb_edge[0].flow_num) + ' = ' + str(fb)

		b_neck = Text("bottleneck = " + b_neck_sum, font_size=14, color=MAROON).next_to(fb_edge[0].arrow, fb_edge[1]).shift(fb_edge[2])
		self.play(Write(b_neck))

		next_step = self.steps[2][0]
		self.play(Transform(step_text, next_step), FadeOut(step_desc), run_time=write_speed)

		step_text_1 = self.steps[2][1]
		step_text_2 = self.steps[2][2]
		step_desc = VGroup(step_text_1, step_text_2).arrange(DOWN).next_to(next_step, DOWN)
		self.play(FadeIn(step_desc), run_time=write_speed)

		fn.flow_animate(self, [[[e, fb]] for e in path], wait_time=0)
		self.play(FadeOut(b_neck))

		next_step = self.steps[3][0]
		self.play(Transform(step_text, next_step), FadeOut(step_desc), run_time=write_speed)

		step_text_1 = self.steps[3][1]
		step_text_2 = self.steps[3][2]
		step_desc = VGroup(step_text_1, step_text_2).arrange(DOWN).next_to(next_step, DOWN)
		self.play(FadeIn(step_desc), run_time=write_speed)

		fn.create_back_edges(self, reversed(path))

		self.play(FadeOut(step_text), FadeOut(step_desc), run_time=write_speed)
		fn.make_edges_colour(self, path, WHITE, reset_edge=True)


	def construct(self):
		self.set_steps()

		# Title animation
		title_text = Text("Ford-Fulkerson")

		desc_1 = Text("Find the max flow which can reach", font_size=24)
		desc_2 = Dot(color=ORANGE, radius=0.2)
		desc_group = VGroup(desc_1, desc_2).arrange(buff=0.5).move_to(UP*3.5)

		title_desc = VGroup(title_text, desc_group)
		title_desc.scale(0.9)

		self.play(Write(title_text))
		self.play(title_text.animate.shift(UP*4))
		self.wait(1)


		# Animate network creation
		node_list = [
			{"neighbours": [[1, 3], [2, 5], [3, 4]], "pos": [-4, 0], "type": "source"},
			{"neighbours": [[2, 7], [4, 9]], "pos": [-2, 3], "type": ""},
			{"neighbours": [[5, 8]], "pos": [1, 0], "type": ""},
			{"neighbours": [[2, 2]], "pos": [-2, -3], "type": ""},
			{"neighbours": [[5, 7]], "pos": [2, 3], "type": ""},
			{"neighbours": [], "pos": [4, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)	
		fn.create_network(0.8, DOWN*1.25)	
		fn.bfs_animation(self)
		self.play(fn.network.animate.shift(DOWN*2))

		self.play(Write(desc_1))
		self.play(Create(desc_2))

		# Animate FF
		self.animate_steps(fn, [fn.edges[1], fn.edges[5]], (fn.edges[1], DOWN, UP*0.2))
		self.animate_steps(fn, [fn.edges[0], fn.edges[3], fn.edges[5]], (fn.edges[5], DOWN, DOWN*0.5))
		self.animate_steps(fn, [fn.edges[2], fn.edges[6], fn.edges[3].back_edge, fn.edges[4], fn.edges[7]], (fn.edges[6], RIGHT, LEFT))

		self.play(Write(self.steps[4][0]), run_time=1)
		step_text_1 = self.steps[4][1]
		step_text_2 = self.steps[4][2]
		step_desc = VGroup(step_text_1, step_text_2).arrange(DOWN).next_to(self.steps[4][0], DOWN)		
		self.play(FadeIn(step_desc))

		fn.min_cut_animation(self, [fn.edges[5], fn.edges[7]], max_flow=True)
		self.wait(2)
