from manim import *
import random


class FlowNode:
	def __init__(self, i, source, sink, pos):
		self.i = i
		self.neighbours = []
		self.edges = []

		# Booleans
		self.source = source
		self.sink = sink

		dot_colour = WHITE
		if self.source:
			dot_colour = TEAL

		elif self.sink:
			dot_colour = ORANGE

		dot_pos = RIGHT*pos[0] + UP*pos[1]
		self.dot = Dot(color=dot_colour, radius=0.2).move_to(dot_pos)



class FlowEdge:
	def __init__(self, n1, n2, capacity):
		self.capacity = capacity
		self.n1 = n1
		self.n2 = n2
		
		a = Arrow(
			start=self.n1.dot.get_center(), 
			end=self.n2.dot.get_center()
		)

		pos_array = [UP*0.35, DOWN*0.35]
		pos = pos_array[random.randint(0, 1)]

		c = Text(str(self.capacity), font='Monospace', font_size=20).move_to(a.get_center() + pos)
		self.arrow = VGroup(a, c)

		self.n1.neighbours.append(self.n2)
		self.n1.edges.append(self)



class FlowNetwork:
	def __init__(self, edge_list, positions):
		source = 0
		sink = 0

		# Get the sink value
		for edge in edge_list:
			sink = max(sink, edge[1])

		# Create the list of nodes
		self.nodes = []
		self.positions = positions
		self.num_nodes = len(positions)

		for i in range(source, sink+1):
			n = FlowNode(i, i==0, i==sink, self.positions[i])
			self.nodes.append(n)

		self.source = self.nodes[0]
		self.sink = self.nodes[-1]

		# Create the list of edges
		self.edges = []
		for edge in edge_list:
			e = FlowEdge(self.nodes[edge[0]], self.nodes[edge[1]], edge[2])
			self.edges.append(e)


	# Makes the network itself
	def create_network(self, scale, position):
		network = VGroup()

		for n in self.nodes:
			network.add(n.dot)

		for e in self.edges:
			network.add(e.arrow)

		self.network = network.scale(scale).move_to(position)


	# Create network animation BFS
	def bfs_animation(self, scene):		
		cur = self.source
		visited = [cur]
		queue = [cur]
		scene.play(Create(cur.dot))

		while len(queue) > 0:
			cur = queue[0]

			for e in cur.edges:
				scene.play(Create(e.arrow))

				if e.n2 not in visited:					
					scene.play(Create(e.n2.dot))
					queue.append(e.n2)
					visited.append(e.n2)

			queue.pop(0)


	# Flow animation
	def flow_animation(self, scene):
		visited = [e for e in self.source.edges]
		stack = [[e, 1000] for e in self.source.edges]

		while len(stack) > 0:
			cur = stack[0][0]
			flow = min(stack[0][1], cur.capacity)
			a = Arrow(cur.n1.dot.get_center(), cur.n2.dot.get_center(), color=BLUE)
			f = Text(str(flow), font_size=20, color=BLUE).move_to(a.get_center() + RIGHT*0.4)

			scene.play(GrowArrow(a))
			scene.wait(2)
			scene.play(Write(f))
			scene.wait(2)

			stack.pop(0)

			for e in cur.n2.edges:
				if e not in visited:
					stack.insert(0, [e, flow])
					visited.append(e)


	# Removes edges and puts them back
	def remove_edges_put_back(self, scene, edge_list):
		edge_set = []
		edge_set_2 = []

		for e in edge_list:
			for e2 in self.edges:
				if e2.n1.i == e[0] and e2.n2.i == e[1]:
					edge_set.append(FadeOut(e2.arrow))
					edge_set_2.append(FadeIn(e2.arrow))

		scene.play(*edge_set)
		scene.wait(1)
		scene.play(*edge_set_2)


	# Removes edges of the min cut
	def min_cut_animation(self, scene, edge_list):
		edge_set = []
		edge_set_2 = []
		min_cut_set = VGroup()

		for e in edge_list:
			for e2 in self.edges:
				if e2.n1.i == e[0] and e2.n2.i == e[1]:
					edge_set.append(e2.arrow.animate.set_color(RED))
					edge_set_2.append(FadeOut(e2.arrow[0]))
					min_cut_set.add(e2.arrow[1])

		scene.play(*edge_set)
		scene.wait(2)
		scene.play(*edge_set_2, min_cut_set.animate.set_color(BLUE).scale(1.5).arrange(buff=0.5).move_to(UP))







