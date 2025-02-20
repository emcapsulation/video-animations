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
	def __init__(self, n1, n2, capacity, baseball=False):
		self.capacity = capacity
		if capacity == "infinity":
			self.capacity = 100000

		self.n1 = n1
		self.n2 = n2

		a = Arrow(
			start=self.n1.dot.get_center(), 
			end=self.n2.dot.get_center(),
		)

		if baseball:
			a = Arrow(
				start=self.n1.dot.get_center(), 
				end=self.n2.dot.get_center(),
				buff=0.75
			)			

		pos_array = [UP*0.35, DOWN*0.35]
		pos = pos_array[random.randint(0, 1)]

		c = Text(str(self.capacity), font='Monospace', font_size=20).move_to(a.get_center() + pos)
		if capacity == "infinity":
			c = MathTex("\\infty", font_size=20).move_to(a.get_center() + pos)

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




class TeamNode:
	def __init__(self, i, t1, pos):
		self.i = i
		self.t1 = t1

		self.neighbours = []
		self.edges = []

		dot_pos = RIGHT*pos[0] + UP*pos[1]

		self.dot = t1.scale(1.5).move_to(dot_pos)


class GameNode:
	def __init__(self, teams, t1, t2, pos):
		# [i, j]
		self.teams = teams

		self.t1 = t1
		self.t2 = t2

		self.neighbours = []
		self.edges = []

		dot_pos = RIGHT*pos[0] + UP*pos[1]

		t_group = VGroup(teams[0], teams[1]).arrange(buff=0.1)
		t_rect = SurroundingRectangle(t_group, corner_radius=0.2, color=WHITE)
		dot = VGroup(t_group, t_rect)
		self.dot = dot.move_to(dot_pos)



class BaseballNetwork:
	def __init__(self, w, r, g, t, check):
		self.w = w
		self.r = r
		self.g = g

		self.num_teams = len(t)
		self.teams = t
		self.no_check = self.teams.copy()
		self.no_check.pop(check)

		# The team to check is eliminated
		self.check = check


		# Source and sink
		self.source = FlowNode(0, True, False, [-6, 0])
		self.sink = FlowNode(0, False, True, [6, 0])


		# Create the team nodes
		self.team_nodes = []
		self.team_edges = []
		pos = [2, 4]
		pos_increment = 2*pos[1]/((self.num_teams-1)-1)

		self.team_to_index = {}

		for i in range(0, len(self.no_check)):
			team_node = TeamNode(i, self.no_check[i].copy(), pos)
			self.team_nodes.append(team_node)
			pos[1] -= pos_increment

			# Capacity is w[check] + r[check] - w[i]
			e = FlowEdge(self.team_nodes[-1], self.sink, self.w[check]+self.r[check]-self.w[i], baseball=True)
			self.team_edges.append(e)


		# Create the game nodes
		self.game_nodes = []
		self.game_edges = []
		self.game_to_team = []
		pos = [-2, 4]
		pos_increment = 2*pos[1]/(((self.num_teams-1)*(self.num_teams-2)/2)-1) # Don't even ask

		for i in range(0, len(self.no_check)):
			for j in range(i+1, len(self.no_check)):
				game_node = GameNode([self.no_check[i].copy(), self.no_check[j].copy()], i, j, pos)
				self.game_nodes.append(game_node)
				pos[1] -= pos_increment

				# Capacity is number of games left between i and j
				e = FlowEdge(self.source, self.game_nodes[-1], self.g[i][j], baseball=True)
				self.game_edges.append(e)

				# Add edges from games to teams
				f = FlowEdge(self.game_nodes[-1], self.team_nodes[i], "infinity", baseball=True)
				self.game_to_team.append(f)

				g = FlowEdge(self.game_nodes[-1], self.team_nodes[j], "infinity", baseball=True)
				self.game_to_team.append(g)		


	# Makes the network itself
	def create_network(self, scale, position):
		network = VGroup(self.source.dot, self.sink.dot)

		for n in self.team_nodes:
			network.add(n.dot)

		for n in self.game_nodes:
			network.add(n.dot)

		for e in self.team_edges:
			network.add(e.arrow)

		for e in self.game_edges:
			network.add(e.arrow)

		for e in self.game_to_team:
			network.add(e.arrow)

		self.network = network.scale(scale).move_to(position)








