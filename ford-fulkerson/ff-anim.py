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
