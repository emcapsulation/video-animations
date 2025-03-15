from manim import *
from FlowNetwork import FlowNetwork


config.background_color = "#15131c"


class FlowNetworkIntro(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		# [N1 -> N2, weight]
		node_list = [
			{"neighbours": [[1, 10], [2, 12], [3, 4]], "pos": [-5, 0], "type": "source"},
			{"neighbours": [[4, 3], [2, 6]], "pos": [-1, -0.5], "type": ""},
			{"neighbours": [[6, 9]], "pos": [1, 2], "type": ""},
			{"neighbours": [[5, 7]], "pos": [-2, -2], "type": ""},
			{"neighbours": [[6, 10]], "pos": [1.5, -0.5], "type": ""},
			{"neighbours": [[6, 5]], "pos": [3, -2], "type": ""},
			{"neighbours": [], "pos": [5, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.9, DOWN*1)

		src_node = Dot(color=TEAL, radius=0.2)
		src_text = Text("source (s)", font_size=24)
		src_group = VGroup(src_node, src_text).arrange()

		sink_node = Dot(color=ORANGE, radius=0.2)
		sink_text = Text("sink (t)", font_size=24)
		sink_group = VGroup(sink_node, sink_text).arrange()

		src_sink = VGroup(src_group, sink_group).arrange(buff=0.5).shift(UP*2)

		max_flow_title = Text("Flow Network").shift(UP*3)
		self.play(Write(max_flow_title), Create(src_node), Write(src_text), Create(sink_node), Write(sink_text))

		fn.bfs_animation(self)
		self.wait(2)

		question_text = Text("What is the maximum flow that can reach", font_size=24)
		sink_node_2 = Dot(color=ORANGE, radius=0.2)
		question_mark = Text("?", font_size=24)
		question_group = VGroup(question_text, sink_node_2, question_mark).arrange(buff=0.5).shift(UP*2)
		
		self.play(ReplacementTransform(src_sink, question_group))
		self.wait(2)

		self.play(FadeOut(fn.network))
		self.wait(2)



class SceneDescription(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		max_flow_title = Text("Flow Networks and Ford-Fulkerson").shift(UP*3)	
		self.play(Write(max_flow_title))

		line = Line(UP*2, DOWN*3)
		self.play(Create(line))

		scene_1 = Text("1. Useful flow network properties", font_size=20)
		scene_2 = Text("2. Ford-Fulkerson walkthrough", font_size=20)
		scene_3 = Text("3. Edmonds-Karp implementation in C++", font_size=20)
		scene_4 = Text("4. Ford-Fulkerson and max-flow min-cut proof", font_size=20)

		scene_desc = VGroup(scene_1, scene_2, scene_3, scene_4).arrange(DOWN, buff=1).next_to(line, LEFT)

		self.play(Write(scene_1), Write(scene_2), Write(scene_3), Write(scene_4))

		self.play(scene_1.animate.set_color(RED))
		# TODO: Animation
		self.wait(2)
		self.play(scene_1.animate.set_color(WHITE))

		self.play(scene_2.animate.set_color(ORANGE))
		# TODO: Animation
		self.wait(2)
		self.play(scene_2.animate.set_color(WHITE))

		self.play(scene_3.animate.set_color(YELLOW))
		# TODO: Animation
		self.wait(2)
		self.play(scene_3.animate.set_color(WHITE))

		self.play(scene_4.animate.set_color(GREEN))
		# TODO: Animation
		self.wait(2)
		self.play(scene_4.animate.set_color(WHITE))



class FlowNetworks(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		src_node = Dot(color=TEAL, radius=0.2)
		src_text = Text("source (s)", font_size=24)
		src_group = VGroup(src_node, src_text).arrange()

		sink_node = Dot(color=ORANGE, radius=0.2)
		sink_text = Text("sink (t)", font_size=24)
		sink_group = VGroup(sink_node, sink_text).arrange()

		src_sink = VGroup(src_group, sink_group).arrange(buff=0.5).shift(UP*2)

		max_flow_title = Text("Properties of Flow Networks").shift(UP*3)
		self.play(Write(max_flow_title))
		self.wait(2)
		self.play(Create(src_node), Write(src_text), Create(sink_node), Write(sink_text))
		self.wait(2)

		node_list = [
			{"neighbours": [[1, 5], [2, 2]], "pos": [-3, 0], "type": "source"},
			{"neighbours": [[3, 3]], "pos": [0, 2], "type": ""},
			{"neighbours": [[3, 4]], "pos": [0, -2], "type": ""},
			{"neighbours": [], "pos": [3, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(1, DOWN*1)
		fn.bfs_animation(self)
		self.wait(2)

		self.play(fn.network.animate.shift(LEFT*3 + DOWN*0.25))
		self.wait(2)


		# Capacity constraint
		capacity_rect = RoundedRectangle(
			width=5, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=PURPLE
		).move_to(RIGHT*4)
		capacity_limit = Text("Capacity Limit", font_size=24).set_color(PURPLE);
		capacity_desc = Text("Flow through an edge is at most", font_size=20)
		capacity_desc_2 = Text("the capacity of that edge", font_size=20)
		capacity_tex = MathTex("\\forall e \\in E, 0 \\leq f(e) \\leq c(e)", font_size=30)
		capacity_group = VGroup(capacity_limit, capacity_desc, capacity_desc_2, capacity_tex).arrange(DOWN).scale(0.8).move_to(capacity_rect.get_center())

		self.play(Create(capacity_rect))
		self.play(Write(capacity_limit))
		self.play(Write(capacity_desc))
		self.play(Write(capacity_desc_2))
		self.play(Write(capacity_tex))
		self.wait(2)
		
		# Animate the top path
		top_path = [[[fn.edges[0], 5]], [[fn.edges[2], 3]]]
		fn.flow_animate(self, top_path)
		self.wait(2)

		# Label the bottleneck
		fn.make_edges_colour(self, [fn.edges[2].flow_arrow], MAROON, include_text=False)
		self.play(Write(Text("bottleneck", font_size=20, color=MAROON).next_to(fn.edges[2].arrow, UP*0.1)))
		self.wait(2)

		# Adjust flow
		top_path = [[[fn.edges[0], 3]]]
		fn.flow_animate(self, top_path, replace_flow=True)


		# Conservation of flow
		conservation_rect = RoundedRectangle(
			width=5, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=LIGHT_PINK
		).next_to(capacity_rect, DOWN*2)
		conservation_limit = Text("Flow Conservation", font_size=24).set_color(LIGHT_PINK);
		conservation_desc = Text("Flow leaving a node equals the", font_size=20)
		conservation_desc_2 = Text("flow entering it", font_size=20)
		conservation_tex = MathTex("\\forall v \\in V \\setminus \\{s, t\\} \\sum_{e_1 = (u, v) \\in E} f(e_1) = \\sum_{e_2 = (v, w) \\in E} f(e_2)", font_size=24)
		conservation_group = VGroup(conservation_limit, conservation_desc, conservation_desc_2, conservation_tex).arrange(DOWN).scale(0.8).move_to(conservation_rect.get_center())

		self.play(Create(conservation_rect))
		self.play(Write(conservation_limit))
		self.play(Write(conservation_desc))
		self.play(Write(conservation_desc_2))
		self.play(Write(conservation_tex))

		# Animate the bottom path
		bottom_path = [[[fn.edges[1], 2]], [[fn.edges[3], 2]]]
		fn.flow_animate(self, bottom_path)
		self.wait(2)


		# Label the bottleneck
		fn.make_edges_colour(self, [fn.edges[1].flow_arrow], MAROON, include_text=False)
		self.play(Write(Text("bottleneck", font_size=20, color=MAROON).next_to(fn.edges[1].arrow, UP*0.1)))
		self.wait(2)

		src_node_2 = Dot(color=TEAL, radius=0.2)
		src_text_2 = Text("flow = sum of flow leaving ", font_size=24)
		src_group_2 = VGroup(src_text_2, src_node_2).arrange()

		sink_node_2 = Dot(color=ORANGE, radius=0.2)
		sink_text_2 = Text("= sum of flow entering ", font_size=24)
		sink_group_2 = VGroup(sink_text_2, sink_node_2).arrange()

		src_sink_2 = VGroup(src_group_2, sink_group_2).arrange().shift(UP*2)
		self.play(ReplacementTransform(src_sink, src_sink_2))
		self.wait(2)

		fn.min_cut_animation(self, [fn.edges[2].flow_arrow, fn.edges[3].flow_arrow], None)
		self.wait(2)

		# Greedy algorithm scene
		question_text = Text("How do we find the maximum flow that can reach", font_size=24)
		sink_node_2 = Dot(color=ORANGE, radius=0.2)
		question_mark = Text("?", font_size=24)
		question_group = VGroup(question_text, sink_node_2, question_mark).arrange(buff=0.5).shift(UP*2)
		
		self.play(ReplacementTransform(src_sink_2, question_group))
		self.wait(2)



class Greedy(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		question_text = Text("How do we find the maximum flow that can reach", font_size=24)
		sink_node_2 = Dot(color=ORANGE, radius=0.2)
		question_mark = Text("?", font_size=24)
		question_group = VGroup(question_text, sink_node_2, question_mark).arrange(buff=0.5).shift(UP*2)
		self.add(question_group)

		self.play(question_group.animate.shift(UP))


		node_list = [
			{"neighbours": [[1, 5], [2, 2]], "pos": [-3, 0], "type": "source"},
			{"neighbours": [[3, 3]], "pos": [0, 2], "type": ""},
			{"neighbours": [[3, 4]], "pos": [0, -2], "type": ""},
			{"neighbours": [], "pos": [3, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.8, DOWN*1.5)
		fn.bfs_animation(self)
		self.wait(2)


		greedy_alg = Code(code="""while there is a path p from s to t:
	find the bottleneck capacity fb of p
	push fb units of flow through that path
return flow""", 
			font_size=16,
            language="C++",
            background="rectangle").next_to(question_group, DOWN)
		self.play(Write(greedy_alg))
		self.wait(2)


		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[2].arrow], MAROON, include_text=False)
		b1 = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[1].arrow, UP*0.1)
		b2 = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[2].arrow, UP*0.1)
		self.play(Write(b1), Write(b2))
		self.wait(2)

		# Animate the greedy flow
		top_path = [[[fn.edges[0], 3], [fn.edges[1], 2]], [[fn.edges[2], 3], [fn.edges[3], 2]]]
		fn.flow_animate(self, top_path)
		self.wait(2)

		# Animate flow value
		fn.min_cut_animation(self, [fn.edges[2].flow_arrow, fn.edges[3].flow_arrow], None, max_flow=True)
		self.wait(2)

		self.play(FadeOut(fn.network), FadeOut(b1), FadeOut(b2))
		self.wait(2)


		# Fail example
		node_list = [
			{"neighbours": [[1, 1], [2, 2]], "pos": [-4, -0.5], "type": "source"},
			{"neighbours": [[2, 3], [3, 1]], "pos": [-1.5, 2], "type": ""},
			{"neighbours": [[3, 2]], "pos": [1.5, -2], "type": ""},
			{"neighbours": [], "pos": [4, 0.5], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.8, DOWN*1.5)
		fn.bfs_animation(self)
		self.wait(2)


		# Zig zag path
		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[2].arrow, fn.edges[4].arrow], GREEN, include_text=False)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[0].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[2].arrow, fn.edges[4].arrow], WHITE, include_text=False)
		self.wait(2)

		# Animate the flow
		bottom_path = [[[fn.edges[0], 1]], [[fn.edges[2], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)


		# Label the path
		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[4].arrow], GREEN, include_text=False)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[4].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[4].arrow], WHITE, include_text=False)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		# Animate flow value
		fn.min_cut_animation(self, [fn.edges[4].flow_arrow], None, max_flow=True)
		self.wait(2)

		fn.remove_flow(self)


		# Label the correct max flow path
		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[1].arrow, fn.edges[3].arrow, fn.edges[4].arrow], GREEN, include_text=False)
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[1].arrow, fn.edges[3].arrow, fn.edges[4].arrow], WHITE, include_text=False)
		self.wait(2)

		paths = [[[fn.edges[0], 1], [fn.edges[1], 2]], [[fn.edges[3], 1], [fn.edges[4], 2]]]
		fn.flow_animate(self, paths)
		self.wait(2)

		fn.min_cut_animation(self, [fn.edges[3].flow_arrow, fn.edges[4].flow_arrow], None, max_flow=True)
		self.wait(2)



		ff_title = Text("Ford-Fulkerson").shift(UP*3)

		ff_alg = Code(code="""while there is a path p from s to t:
	find the bottleneck capacity fb of p
	push fb units of flow through that path
	create back edges with capacity fe
return flow""", 
			font_size=16,
            language="C++",
            background="rectangle").next_to(question_group, DOWN)
		self.play(ReplacementTransform(greedy_alg, ff_alg), ReplacementTransform(question_group, ff_title))
		self.wait(2)


		fn.remove_flow(self)


		# Zig zag path
		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[2].arrow, fn.edges[4].arrow], GREEN, include_text=False)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[0].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0].arrow, fn.edges[2].arrow, fn.edges[4].arrow], WHITE, include_text=False)
		self.wait(2)

		# Animate the flow
		bottom_path = [[[fn.edges[0], 1]], [[fn.edges[2], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		# Create back edges
		fn.create_back_edges(self, [fn.edges[4], fn.edges[2], fn.edges[0]])


		# Label the path
		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[4].arrow], GREEN, include_text=False)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[4].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[4].arrow], WHITE, include_text=False)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[4], fn.edges[1]])
		self.wait(2)


		# Label the path
		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[2].back_edge.arrow, fn.edges[3].arrow], GREEN, include_text=False)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[1].arrow, UP*0.1 + LEFT*0.2)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1].arrow, fn.edges[2].back_edge.arrow, fn.edges[3].arrow], WHITE, include_text=False)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[2].back_edge, 1]], [[fn.edges[3], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[4], fn.edges[1]])
		self.wait(2)


		fn.min_cut_animation(self, [fn.edges[3].flow_arrow, fn.edges[4].flow_arrow], None, max_flow=True)
		self.wait(2)

