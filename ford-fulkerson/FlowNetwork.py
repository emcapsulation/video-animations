from manim import *


class FlowNode:
	def __init__(self, i, pos, type):
		self.i = i
		self.type = type
		self.neighbours = []
		self.edges = []

		dot_pos = RIGHT*pos[0] + UP*pos[1]

		color = WHITE
		if self.type == "source":
			color = TEAL
		elif self.type == "sink":
			color = ORANGE

		self.dot = Dot(color=color).scale(1.5).move_to(dot_pos)


class FlowEdge:
	def __init__(self, n1, n2, capacity, font_size=20, back_edge=False):
		self.capacity = capacity

		self.n1 = n1
		self.n2 = n2


		if not back_edge:
			self.is_back_edge = False

			a = Arrow(
				start=self.n1.dot.get_center(), 
				end=self.n2.dot.get_center(),
				tip_length=0.2
			)

			c = Text(str(self.capacity), font='Monospace', font_size=font_size).move_to(a.get_center() + UP*0.35)
			self.arrow = VGroup(a, c)

		else:
			self.is_back_edge = True

			a = CurvedArrow(
				self.n1.dot.get_center(), 
				self.n2.dot.get_center(),
				angle=-PI/4,
				stroke_width=2,
				tip_length=0.2
			).shift(DOWN*0.1)

			c = Text(str(self.capacity), font='Monospace', font_size=font_size).move_to((self.n2.dot.get_center() + a.get_center())/2 + DOWN*0.6 + RIGHT*0.2)
			self.arrow = VGroup(a, c)


		self.n1.neighbours.append(self.n2)
		self.n1.edges.append(self)

		# This is for flow animations
		self.flow_arrow = None
		self.flow_num = 0

		# This is for the back edge
		self.back_edge = None
		self.forward_edge = None


class FlowNetwork:
	'''
	node_list = [
		{
			"neighbours": [[neighbour1, capacity], [neighbour2, capacity], ...],
			"pos": [x, y],
			"type": "source" | "sink" | ""
		},
		{
			"neighbours": [[neighbour1, capacity], [neighbour2, capacity], ...],
			"pos": [x, y],
			"type": "source" | "sink" | ""
		},
	]
	'''
	def __init__(self, node_list, font_size=20):
		self.nodes = []
		self.edges = []
		self.font_size = font_size


		i = 0
		for n in node_list:
			node = FlowNode(i, n["pos"], n["type"])

			if n["type"] == "source":
				self.source = node
			elif n["type"] == "sink":
				self.sink = node

			self.nodes.append(node)
			i += 1


		i = 0
		for n in node_list:
			for neighbour in n["neighbours"]:				
				self.edges.append(FlowEdge(self.nodes[i], self.nodes[neighbour[0]], neighbour[1]))
			i += 1	


	# Makes the network itself
	def create_network(self, scale, position):
		network = VGroup()

		for n in self.nodes:
			network.add(n.dot)

		for e in self.edges:
			network.add(e.arrow)

		self.network = network.scale(scale).move_to(position)
		self.scale = scale


	# Creates the source and sink
	def draw_source_sink(self, scene):
		scene.play(Create(self.source.dot))
		scene.play(Create(self.sink.dot))


	# Creates the game vertices
	def draw_vertices(self, scene):
		for n in self.nodes:
			scene.play(Create(n.dot))


	# Creates the game edges
	def draw_edges(self, scene):
		for e in self.edges:
			scene.play(GrowArrow(e.arrow[0]))
			scene.play(Write(e.arrow[1]))


	# Creates the network with BFS
	def bfs_animation(self, scene):
		cur = self.source
		visited = [cur]
		queue = [cur]
		scene.play(Create(cur.dot))
		scene.play(Create(self.sink.dot))

		while len(queue) > 0:
			cur = queue[0]

			for e in cur.edges:
				scene.play(Create(e.arrow))

				if e.n2 not in visited:	
					if e.n2 != self.sink:				
						scene.play(Create(e.n2.dot))
					queue.append(e.n2)
					visited.append(e.n2)

			queue.pop(0)


	# Highlights edges of the min cut
	def min_cut_animation(self, scene, edge_list, colour, max_flow=False):
		edge_set_2 = []
		min_cut_set = VGroup()
		if max_flow:
			min_cut_set.add(Text("max flow = ", font_size=20))
		else:
			min_cut_set.add(Text("flow = ", font_size=20))

		for e2 in edge_list:
			if hasattr(e2, "arrow"):
				if colour != None:
					edge_set_2.append(e2.arrow.animate.set_color(colour))
				min_cut_set.add(e2.arrow[1].copy())
			else:
				# Flow arrow passed in
				if colour != None:
					edge_set_2.append(e2.animate.set_color(colour))
				min_cut_set.add(e2[1].copy())
		scene.wait(2)

		s = 0
		i = 1
		while i < len(min_cut_set):
			s += int(min_cut_set[i].get_text())
			i += 1
			if i < len(min_cut_set):
				min_cut_set.insert(i, Text("+", color=WHITE, font_size=20))
			i += 1

		min_cut_set.add(Text("=", color=WHITE, font_size=20))
		min_cut_set.add(Text(str(s), color=WHITE, font_size=20))

		scene.play(*edge_set_2, min_cut_set.animate.set_font_size(30).arrange(buff=0.25).next_to(self.network, UP))
		self.min_cut_set = min_cut_set
		self.network.add(min_cut_set)


	# Animates flow
	def flow_animate(self, scene, edge_list, replace_flow=False):
		# Edge list is: [[[edge, flow], [edge, flow]], [[edge, flow], [edge, flow]]]
		for edge_set in edge_list:
			edge_anim = []
			text_anim = []

			for e in edge_set:
				a = e[0].arrow[0].copy().set_color(BLUE_D)		
				edge_anim.append(Create(a))	

				# Position where to write the flow
				if not e[0].is_back_edge:
					flow_pos = e[0].arrow[0].get_start() + (e[0].arrow[0].get_end() - e[0].arrow[0].get_start())*0.65 + UP*0.3
				else:
					flow_pos = e[0].arrow[1].get_center() + RIGHT*0.2 + DOWN*0.3

				if e[0].flow_arrow != None:
					e[0].flow_num += e[1]
					if replace_flow:
						e[0].flow_num = e[1]

					new_flow = str(e[0].flow_num)

					f = Text(new_flow, font_size=self.font_size, color=BLUE_D).move_to(flow_pos).scale(self.scale)
					text_anim.append(ReplacementTransform(e[0].flow_arrow[1], f))

				else:
					e[0].flow_num = e[1]
					f = Text(str(e[1]), font_size=self.font_size, color=BLUE_D).move_to(flow_pos).scale(self.scale)
					text_anim.append(Write(f))


				# Decrease the flow of the forward edge (if back edge)
				if e[0].is_back_edge:
					e[0].forward_edge.flow_num -= e[1]
					f = Text(str(e[0].forward_edge.flow_num), font_size=self.font_size, color=BLUE_D).move_to(e[0].forward_edge.flow_arrow[1].get_center()).scale(self.scale)

					text_anim.append(ReplacementTransform(e[0].forward_edge.flow_arrow[1], f))


				if e[0].flow_arrow != None:
					e[0].flow_arrow = None		
				e[0].flow_arrow = VGroup(a, f)
				self.network.add(e[0].flow_arrow[1])

			scene.play(*edge_anim)
			scene.play(*text_anim)

		scene.wait(2)
		single_list = []
		for edge_set in edge_list:
			for e in edge_set:
				single_list.append(FadeOut(e[0].flow_arrow[0]))
		scene.play(*single_list)


	# Make the edges red
	def make_edges_colour(self, scene, edge_list, colour, include_text=True):
		anim_list = []
		for e in edge_list:
			if include_text:
				anim_list.append(e.animate.set_color(colour))
			else:
				anim_list.append(e[0].animate.set_color(colour))
		scene.play(*anim_list)


	# Removes the flow from the network
	def remove_flow(self, scene):
		fade_out = []
		for e in self.edges:
			e.flow_num = 0

			if e.flow_arrow != None:
				fade_out.append(FadeOut(e.flow_arrow[1]))	

			e.flow_arrow = None	

		if self.min_cut_set != None:
			for t in self.min_cut_set:
				fade_out.append(FadeOut(t))
			self.network.remove(self.min_cut_set)

		scene.play(*fade_out)


	# Creates the back edges on a path
	def create_back_edges(self, scene, edge_list):
		for e in edge_list:
			back_edge = FlowEdge(e.n2, e.n1, e.flow_num, back_edge=True)
			back_edge.arrow.scale(self.scale)

			# Add it to the network
			if e.back_edge != None:
				scene.play(ReplacementTransform(e.back_edge.arrow, back_edge.arrow))

			else:				
				scene.play(Create(back_edge.arrow))
				self.network.add(back_edge.arrow)

			e.back_edge = back_edge
			e.back_edge.forward_edge = e


			
			
			

			

