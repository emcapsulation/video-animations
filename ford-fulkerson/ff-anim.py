from manim import *
from FlowNetwork import FlowNetwork


config.background_color = "#15131c"


class FlowNetworkIntro(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		# [N1 -> N2, weight]
		node_list = [
			{"neighbours": [[1, 5], [2, 12], [3, 4]], "pos": [-6, 0], "type": "source"},
			{"neighbours": [[4, 3], [2, 6]], "pos": [-1.5, 0], "type": ""},
			{"neighbours": [[5, 9]], "pos": [0, 3.5], "type": ""},
			{"neighbours": [[4, 7]], "pos": [-4, -3], "type": ""},
			{"neighbours": [[5, 10]], "pos": [2, -0.5], "type": ""},
			{"neighbours": [], "pos": [6, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.8, DOWN*1)

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
		scene_3 = Text("3. Ford-Fulkerson larger example", font_size=20)
		scene_4 = Text("4. Edmonds-Karp implementation in C++", font_size=20)

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
		fn.make_edges_colour(self, [fn.edges[2]], MAROON)
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
		fn.make_edges_colour(self, [fn.edges[1]], MAROON)
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

		fn.min_cut_animation(self, [fn.edges[2], fn.edges[3]])
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
	push fb units of flow through p
return flow""", 
			font_size=14,
            language="C++",
            background="rectangle").next_to(question_group, DOWN)
		self.play(Write(greedy_alg))
		self.wait(2)


		# Show the bottlenecks
		fn.make_edges_colour(self, [fn.edges[1], fn.edges[2]], MAROON)
		b1 = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[1].arrow, UP*0.1)
		b2 = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[2].arrow, UP*0.1)
		self.play(Write(b1), Write(b2))
		self.wait(2)


		# Animate the greedy flow (success)
		top_path = [[[fn.edges[0], 3], [fn.edges[1], 2]], [[fn.edges[2], 3], [fn.edges[3], 2]]]
		fn.flow_animate(self, top_path)
		self.wait(2)

		fn.min_cut_animation(self, [fn.edges[2], fn.edges[3]], max_flow=True)
		self.wait(2)

		self.play(FadeOut(fn.network), FadeOut(b1), FadeOut(b2))
		self.wait(2)



class GreedyFail(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		question_text = Text("How do we find the maximum flow that can reach", font_size=24)
		sink_node_2 = Dot(color=ORANGE, radius=0.2)
		question_mark = Text("?", font_size=24)
		question_group = VGroup(question_text, sink_node_2, question_mark).arrange(buff=0.5).shift(UP*2)
		self.add(question_group.shift(UP))

		greedy_alg = Code(code="""while there is a path p from s to t:
	find the bottleneck capacity fb of p
	push fb units of flow through p
return flow""", 
			font_size=14,
            language="C++",
            background="rectangle").next_to(question_group, DOWN)
		self.add(greedy_alg)


		# Show the greedy flow failing
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
		fn.make_edges_colour(self, [fn.edges[0], fn.edges[2], fn.edges[4]], GREEN)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[0].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0], fn.edges[2], fn.edges[4]], WHITE, reset_edge=True)
		self.wait(2)

		zig_zag_path = [[[fn.edges[0], 1]], [[fn.edges[2], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, zig_zag_path)
		self.play(FadeOut(b_neck))
		self.wait(2)


		# Bottom path
		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4]], GREEN)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[4].arrow)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4]], WHITE, reset_edge=True)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)


		# Min cut is 2
		fn.min_cut_animation(self, [fn.edges[4]], max_flow=True)
		self.wait(2)

		fn.remove_flow(self)


		# Label the correct max flow paths (3)
		fn.make_edges_colour(self, [fn.edges[0], fn.edges[1], fn.edges[3], fn.edges[4]], GREEN)
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0], fn.edges[1], fn.edges[3], fn.edges[4]], WHITE, reset_edge=True)
		self.wait(2)

		paths = [[[fn.edges[0], 1], [fn.edges[1], 2]], [[fn.edges[3], 1], [fn.edges[4], 2]]]
		fn.flow_animate(self, paths)
		self.wait(2)

		fn.min_cut_animation(self, [fn.edges[3], fn.edges[4]], max_flow=True)
		self.wait(2)


		self.play(FadeOut(fn.network))
		self.wait(2)


		fail_text = Text("Greedy algorithm fails", font_size=24, color=RED).move_to(ORIGIN)
		self.play(Write(fail_text))
		self.wait(2)



class FFExample(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		

		ff_title = Text("Ford-Fulkerson").shift(UP*3)

		ff_alg = Code(code="""while there is a path (p) from s to t:
	find the bottleneck capacity (fb) of p

	for each edge e in p:
		push fb units of flow through e

		if e is a back edge:
			deduct fb units of flow from 
			the corresponding forward edge

	create back edges with capacity equal to 
	the flow in the corresponding forward edge
return flow""", 
			font_size=14,
            language="C++",
            background="rectangle").next_to(ff_title, DOWN).shift(LEFT*3.5 + DOWN*1.5)

		self.play(Write(ff_title))
		self.play(Create(ff_alg))
		self.wait(2)


		# Show the greedy flow failing
		node_list = [
			{"neighbours": [[1, 1], [2, 2]], "pos": [-4, -0.5], "type": "source"},
			{"neighbours": [[2, 3], [3, 1]], "pos": [-1.5, 2], "type": ""},
			{"neighbours": [[3, 2]], "pos": [1.5, -2], "type": ""},
			{"neighbours": [], "pos": [4, 0.5], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.8, RIGHT*3 + DOWN*0.5)
		fn.bfs_animation(self)
		self.wait(2)


		# Zig zag path
		fn.make_edges_colour(self, [fn.edges[0], fn.edges[2], fn.edges[4]], GREEN)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[0].arrow, UP*0.1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0], fn.edges[2], fn.edges[4]], WHITE, reset_edge=True)
		self.wait(2)

		zig_zag_path = [[[fn.edges[0], 1]], [[fn.edges[2], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, zig_zag_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[4], fn.edges[2], fn.edges[0]])


		# Bottom path
		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4]], GREEN)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[4].arrow).shift(LEFT*1 + DOWN*1)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4]], WHITE, reset_edge=True)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[4], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[4], fn.edges[1]])
		self.wait(2)


		# Label the path
		fn.make_edges_colour(self, [fn.edges[1], fn.edges[2].back_edge, fn.edges[3]], GREEN)
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[3].arrow).shift(LEFT)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[2].back_edge, fn.edges[3]], WHITE, reset_edge=True)
		self.wait(2)

		bottom_path = [[[fn.edges[1], 1]], [[fn.edges[2].back_edge, 1]], [[fn.edges[3], 1]]]
		fn.flow_animate(self, bottom_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[3], fn.edges[2], fn.edges[1]])
		self.wait(2)


		fn.min_cut_animation(self, [fn.edges[3], fn.edges[4]], max_flow=True)
		self.wait(2)


class FordFulkerson(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		ff_title = Text("Ford-Fulkerson").shift(UP*3)
		self.add(ff_title)

		line = Line(UP*2, DOWN*3).shift(LEFT*3)
		self.play(Create(line))


		line_1 = Text("1. Find an augmenting\npath from s to t (p).", font_size=16)
		line_2 = Text("2. Find the bottleneck\ncapacity of p (fb).", font_size=16)
		line_3 = Text("3. For each edge e in p:\nflow through e += fb\nIf e is a back edge:\nDeduct fb from the\ncorresponding forward\nedge's flow.", font_size=16)
		line_4 = Text("4. Build the residual\ngraph.\nFor each edge e in p,\ncreate a back edge with\ncapacity = flow in e.", font_size=16)
		line_5 = Text("5. Return the flow when\nthere are no more\naugmenting paths.", font_size=16)

		algo = VGroup(line_1, line_2, line_3, line_4, line_5).arrange(DOWN, buff=0.5).next_to(line, LEFT)
		self.add(algo)


		# [N1 -> N2, weight]
		node_list = [
			{"neighbours": [[1, 5], [2, 12], [3, 4]], "pos": [-6, 0], "type": "source"},
			{"neighbours": [[4, 3], [2, 6]], "pos": [-1.5, 0], "type": ""},
			{"neighbours": [[5, 9]], "pos": [0, 3.5], "type": ""},
			{"neighbours": [[4, 7]], "pos": [-4, -3], "type": ""},
			{"neighbours": [[5, 10]], "pos": [2, -0.5], "type": ""},
			{"neighbours": [], "pos": [6, 0], "type": "sink"}
		]
		fn = FlowNetwork(node_list)
		fn.create_network(0.75, RIGHT*1.9 + DOWN*0.5)

		fn.bfs_animation(self)
		self.wait(2)


		# Middle path
		self.play(line_1.animate.set_color(MAROON))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0], fn.edges[4], fn.edges[5]], GREEN)
		self.wait(2)

		self.play(line_1.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_2.animate.set_color(ORANGE))
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[0].arrow, DOWN).shift(RIGHT*0.2)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[0], fn.edges[4], fn.edges[5]], WHITE, reset_edge=True)
		self.wait(2)

		self.play(line_2.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_3.animate.set_color(GOLD))
		self.wait(2)

		zig_zag_path = [[[fn.edges[0], 5]], [[fn.edges[4], 5]], [[fn.edges[5], 5]]]
		fn.flow_animate(self, zig_zag_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		self.play(line_3.animate.set_color(WHITE))
		self.wait(2)
		

		self.play(line_4.animate.set_color(GREEN))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[5], fn.edges[4], fn.edges[0]])

		self.play(line_4.animate.set_color(WHITE))
		self.wait(2)


		# Top path
		self.play(line_1.animate.set_color(MAROON))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[5]], GREEN)
		self.wait(2)

		self.play(line_1.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_2.animate.set_color(ORANGE))
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[5].arrow).shift(LEFT*1.5)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[5]], WHITE, reset_edge=True)
		self.wait(2)

		self.play(line_2.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_3.animate.set_color(GOLD))
		self.wait(2)

		top_path = [[[fn.edges[1], 4]], [[fn.edges[5], 4]]]
		fn.flow_animate(self, top_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		self.play(line_3.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_4.animate.set_color(GREEN))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[5], fn.edges[1]])

		self.play(line_4.animate.set_color(WHITE))
		self.wait(2)


		# Bottom path
		self.play(line_1.animate.set_color(MAROON))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[2], fn.edges[6], fn.edges[7]], GREEN)
		self.wait(2)

		self.play(line_1.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_2.animate.set_color(ORANGE))
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[2].arrow, RIGHT).shift(LEFT*0.5)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[2], fn.edges[6], fn.edges[7]], WHITE, reset_edge=True)
		self.wait(2)

		self.play(line_2.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_3.animate.set_color(GOLD))
		self.wait(2)

		top_path = [[[fn.edges[2], 4]], [[fn.edges[6], 4]], [[fn.edges[7], 4]]]
		fn.flow_animate(self, top_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		self.play(line_3.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_4.animate.set_color(GREEN))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[7], fn.edges[6], fn.edges[2]])

		self.play(line_4.animate.set_color(WHITE))
		self.wait(2)


		# Back edge path
		self.play(line_1.animate.set_color(MAROON))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4].back_edge, fn.edges[3], fn.edges[7]], GREEN)
		self.wait(2)

		self.play(line_1.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_2.animate.set_color(ORANGE))
		self.wait(2)

		b_neck = Text("bottleneck", font_size=16, color=MAROON).next_to(fn.edges[3].arrow, DOWN).shift(UP*0.3 + LEFT*0.25)
		self.play(Write(b_neck))
		self.wait(2)

		fn.make_edges_colour(self, [fn.edges[1], fn.edges[4].back_edge, fn.edges[3], fn.edges[7]], WHITE, reset_edge=True)
		self.wait(2)

		self.play(line_2.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_3.animate.set_color(GOLD))
		self.wait(2)

		top_path = [[[fn.edges[1], 3]], [[fn.edges[4].back_edge, 3]], [[fn.edges[3], 3]], [[fn.edges[7], 3]]]
		fn.flow_animate(self, top_path)
		self.play(FadeOut(b_neck))
		self.wait(2)

		self.play(line_3.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_4.animate.set_color(GREEN))
		self.wait(2)

		fn.create_back_edges(self, [fn.edges[1], fn.edges[4], fn.edges[3], fn.edges[7]])

		self.play(line_4.animate.set_color(WHITE))
		self.wait(2)


		self.play(line_5.animate.set_color(BLUE))
		self.wait(2)

		fn.min_cut_animation(self, [fn.edges[5], fn.edges[7]], max_flow=True)
		self.wait(2)

		self.play(line_5.animate.set_color(WHITE))
		self.wait(2)

