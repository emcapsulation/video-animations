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

			c = Text("0/" + str(self.capacity), font='Monospace', font_size=font_size, color="#15131c").move_to(a.get_center() + UP*0.45)
			r = BackgroundRectangle(c, buff=0.1, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
			self.arrow = VGroup(a, r, c)

		else:
			self.is_back_edge = True

			a = CurvedArrow(
				self.n1.dot.get_center(), 
				self.n2.dot.get_center(),
				angle=-PI/12,
				stroke_width=2,
				tip_length=0.2,
				color=GRAY_B
			).shift(DOWN*0.1)

			c = Text("0/" + str(self.capacity), font='Monospace', font_size=(font_size-4), color="#15131c").move_to(a.get_center() + DOWN*0.45)
			r = BackgroundRectangle(c, buff=0.1, stroke_width=0, color=GRAY_B, fill_opacity=1, corner_radius=0.2)
			self.arrow = VGroup(a, r, c)


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
			scene.play(Create(e.arrow[1]))
			scene.play(Write(e.arrow[2]))


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
	def min_cut_animation(self, scene, edge_list, max_flow=False):
		min_cut_set = VGroup()
		if max_flow:
			min_cut_set.add(Text("max flow", font_size=20))
		else:
			min_cut_set.add(Text("flow", font_size=20))

		min_cut_set.add(Text("=", font_size=20))

		s = 0
		for e2 in edge_list:
			if len(edge_list) > 1:
				min_cut_set.add(Text(str(e2.flow_num), color=BLUE_D, font_size=20))

			s += e2.flow_num

		if len(edge_list) > 1:
			i = 2
			while i < len(min_cut_set):
				i += 1
				if i < len(min_cut_set):					
					min_cut_set.insert(i, Text("+", color=WHITE, font_size=20))
				i += 1

		if len(edge_list) > 1:
			min_cut_set.add(Text("=", color=WHITE, font_size=20))
		min_cut_set.add(Text(str(s), color=WHITE, font_size=20))

		scene.play(min_cut_set.animate.set_font_size(30).arrange(buff=0.25).next_to(self.network, UP))
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

				new_flow = ""
				if e[0].flow_arrow != None:
					# Some flow has already passed through this edge
					e[0].flow_num += e[1]
					if replace_flow:
						e[0].flow_num = e[1]

				else:
					e[0].flow_num = e[1]

				new_flow = str(e[0].flow_num)

				fz = self.font_size
				if e[0].is_back_edge:
					fz -= 4

				f = Text(new_flow + "/" + str(e[0].capacity), font_size=fz, color="#15131c").move_to(e[0].arrow[2].get_center()).scale(self.scale)
				text_anim.append(ReplacementTransform(e[0].arrow[2], f))

				if e[0].flow_arrow != None:
					e[0].flow_arrow = None		
				e[0].flow_arrow = a

			scene.play(*edge_anim)
			scene.play(*text_anim)

		scene.wait(2)
		single_list = []
		for edge_set in edge_list:
			for e in edge_set:
				single_list.append(FadeOut(e[0].flow_arrow))
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
				f = Text("0/" + str(e.capacity), font_size=self.font_size, color="#15131c").move_to(e.arrow[2].get_center()).scale(self.scale)
				fade_out.append(ReplacementTransform(e.arrow[2], f))

			e.flow_arrow = None	

		if self.min_cut_set != None:
			for t in self.min_cut_set:
				fade_out.append(FadeOut(t))
			self.network.remove(self.min_cut_set)

		scene.play(*fade_out)


	# Creates the back edges on a path
	def create_back_edges(self, scene, edge_list):
		for e in edge_list:		
			if e.back_edge != None:
				f = Text(str(e.back_edge.flow_num) + "/" + str(e.flow_num), font_size=self.font_size-4, color="#15131c").move_to(e.back_edge.arrow[2].get_center()).scale(self.scale)
				scene.play(ReplacementTransform(e.back_edge.arrow[2], f))

			else:	
				back_edge = FlowEdge(e.n2, e.n1, e.flow_num, back_edge=True)
				back_edge.arrow.scale(self.scale)	

				scene.play(Create(back_edge.arrow))
				self.network.add(back_edge.arrow)

				e.back_edge = back_edge
				e.back_edge.forward_edge = e


			
			
			

			

