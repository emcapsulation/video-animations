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
	def __init__(self, n1, n2, capacity, font_size=20):
		self.capacity = capacity

		self.n1 = n1
		self.n2 = n2

		a = Arrow(
			start=self.n1.dot.get_center(), 
			end=self.n2.dot.get_center(),
		)

		c = Text(str(self.capacity), font='Monospace', font_size=font_size).move_to(a.get_center() + UP*0.35)
		self.arrow = VGroup(a, c)

		self.n1.neighbours.append(self.n2)
		self.n1.edges.append(self)

		# This is for flow animations
		self.flow = None


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


	# Removes edges of the min cut
	def min_cut_animation(self, scene, edge_list):
		edge_set_2 = []
		min_cut_set = VGroup(Text("max flow = ", font_size=20))

		for e2 in edge_list:
			edge_set_2.append(e2.arrow.animate.set_color(RED))
			min_cut_set.add(e2.arrow[1].copy())
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


	# Animates flow
	def flow_animate(self, scene, edge_list):
		# Edge list is: [[[edge, flow], [edge, flow]], [[edge, flow], [edge, flow]]]
		for edge_set in edge_list:
			edge_anim = []

			for e in edge_set:
				a = e[0].arrow[0].copy().set_color(BLUE)				
				edge_anim.append(GrowArrow(a))

				flow_pos = e[0].arrow[0].get_start() + (e[0].arrow[0].get_end() - e[0].arrow[0].get_start())*0.65 + UP*0.25

				if e[0].flow != None:
					f = Text(str(int(e[0].flow[1].get_text())+e[1]), font_size=14, color=BLUE).move_to(flow_pos)
					edge_anim.append(ReplacementTransform(e[0].flow[1], f))
				else:
					f = Text(str(e[1]), font_size=14, color=BLUE).move_to(flow_pos)
					edge_anim.append(Write(f))
				e[0].flow = VGroup(a, f)

			scene.play(*edge_anim)


	# Make the edges red
	def make_edges_colour(self, edge_list, colour):
		for e in edge_list:
			e.arrow.set_color(colour)
			if e.flow != None:
				e.flow[0].set_color(colour)


