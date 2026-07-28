from manim import *

from shorts.algorithm_mini_challenges import *
from constants import *
from utils import generate_colours

config.background_color = DEFAULT_BACKGROUND

config.pixel_width = MOBILE_WIDTH
config.pixel_height = MOBILE_HEIGHT
config.frame_width = MOBILE_FRAME_WIDTH
config.frame_height = MOBILE_FRAME_HEIGHT


colour_scheme = [PASTEL_RED, PASTEL_ORANGE, PASTEL_GOLD, PASTEL_YELLOW, PASTEL_GREEN, PASTEL_TEAL, PASTEL_BLUE, PASTEL_PURPLE, PASTEL_VIOLET, PASTEL_PINK]


skills = ["Agility", "Climb", "Dodge", "Endurance", "Flee", "Lift", "Parkour", "Run", "Strength"]
skill_colours = generate_colours(skills, in_order=True, colour_scheme=colour_scheme)

n = 9
skill_prerequisites = {
	0: 	[],
	1: 	[5],
	2: 	[0],
	3: 	[0, 8],
	4: 	[1, 2],
	5: 	[8],
	6: 	[2, 7, 8],
	7: 	[0, 3],
	8: 	[]
}


def make_adj_list():
	d_adj = {}
	for skill, prereqs in skill_prerequisites.items():
		for pr in prereqs:
			if pr not in d_adj.keys():
				d_adj[pr] = [skill]
			else:
				d_adj[pr].append(skill)
	return d_adj

d_adj = make_adj_list()



def get_skill_prerequisites_map():
	v_skill_prerequisites = VGroup()
	for i_skill, l_prerequisites in skill_prerequisites.items():
		v_this_sp = VGroup()
		
		skill_text = Text(skills[i_skill], font_size=24, color=skill_colours[i_skill])
		v_this_sp.add(skill_text)

		v_prerequisites = VGroup()
		for i_prerequisite in l_prerequisites:
			prerequisite_text = Text(skills[i_prerequisite], font_size=20, color=skill_colours[i_prerequisite])
			v_prerequisites.add(prerequisite_text)
		v_prerequisites.arrange(RIGHT, buff=0.2)

		bg_rect = SurroundingRectangle(v_prerequisites, stroke_width=0, fill_color=WHITE, fill_opacity=0.1, corner_radius=0.1)
		v_this_sp.add(VGroup(bg_rect, v_prerequisites))

		v_skill_prerequisites.add(v_this_sp.arrange(RIGHT, buff=0.25))

	v_skill_prerequisites.arrange(DOWN, aligned_edge=LEFT)

	right_edge = max(row[0].get_right()[0] for row in v_skill_prerequisites) + 0.5
	for row in v_skill_prerequisites:
		row[1].next_to([right_edge, row[1].get_center()[1], 0], RIGHT, buff=0.5)

	return v_skill_prerequisites


def create_graph(scene, animate_info=(False, None), graph_origin=UP*2):
	animate = animate_info[0]
	v_prerequisites_map = animate_info[1]

	node_positions = {
		0: graph_origin + RIGHT*2 + UP*2,
		1: graph_origin + LEFT*2.5 + DOWN*3,
		2: graph_origin + RIGHT*3.5,
		3: graph_origin,
		4: graph_origin + RIGHT + DOWN*5.5,
		5: graph_origin + LEFT*3 + DOWN,
		6: graph_origin + DOWN*3.5,
		7: graph_origin + RIGHT + DOWN*1.5,
		8: graph_origin + LEFT*2 + UP*2.5,
	}


	def make_node(i_skill):
		label = Text(skills[i_skill], font_size=20, color=skill_colours[i_skill])
		bg_rect = SurroundingRectangle(label, stroke_width=0, fill_color=WHITE, fill_opacity=0.1, corner_radius=0.1)
		node = VGroup(bg_rect, label)
		node.move_to(node_positions[i_skill])

		return node


	v_nodes = VGroup(*[ Dot(radius=0) for _ in range(n) ])
	v_edges = VGroup(*[ VGroup(*[Dot(radius=0) for _ in range(n)]) for _ in range(n) ])

	for i_skill, prerequisites in skill_prerequisites.items():
		if isinstance(v_nodes[i_skill], Dot):
			node = make_node(i_skill)

			if animate:
				scene.play(ReplacementTransform(v_prerequisites_map[i_skill][0].copy(), node))
			v_nodes[i_skill] = node


		for i_prereq in range(0, len(prerequisites)):
			prereq = prerequisites[i_prereq]

			if isinstance(v_nodes[prereq], Dot):
				node = make_node(prereq)

				if animate:
					scene.play(ReplacementTransform(v_prerequisites_map[i_skill][1][1][i_prereq].copy(), node))
				
				v_nodes[prereq] = node

			arrow = Arrow(
				v_nodes[prereq].get_center(),
				v_nodes[i_skill].get_center(),
				buff=0.5,
				stroke_width=3,
				max_tip_length_to_length_ratio=0.15,
			)
			v_edges[prereq][i_skill] = arrow

			if animate:
				scene.play(Indicate(v_prerequisites_map[i_skill][1][1][i_prereq], color=PASTEL_YELLOW))
				scene.play(Create(arrow), run_time=0.35)

		if animate:
			scene.wait(1)
			scene.remove(v_prerequisites_map[i_skill])

	if animate:
		scene.wait(2)
	
	return VGroup(v_nodes, v_edges)


def create_indegrees(scene, v_graph, animate=False):
	l_indegs = [0] * n
	in_degs_text = Text("in-degree", font_size=20, color=GRAY)
	
	v_skill_letters = VGroup()
	for i_skill in range(0, len(skills)):
		v_skill_letters.add(Text(skills[i_skill][0], color=skill_colours[i_skill], font_size=24))
	v_skill_letters.arrange(RIGHT, buff=0.5)

	v_indeg_counts = VGroup(*[Text(str(l_indegs[i]), font_size=24).next_to(v_skill_letters[i]) for i in range(0, n)])

	v_indegs = VGroup(in_degs_text, v_skill_letters, v_indeg_counts).arrange(DOWN).move_to(ORIGIN)
	if animate:
		scene.play(FadeIn(v_indegs))

	v_nodes = v_graph[0]
	v_edges = v_graph[1]

	def make_cur_rect(i, stroke_width=0.5):
		if i == -1:
			return Dot(radius=0, color=WHITE)
		return SurroundingRectangle(
			v_nodes[i], buff=0.25, fill_opacity=0, 
			stroke_color=WHITE, stroke_width=stroke_width
		)

	big_rect = make_cur_rect(-1)
	cur_rect = make_cur_rect(-1)

	for i_skill, l_neighbours in d_adj.items():
		new_big_rect = make_cur_rect(i_skill, stroke_width=2)

		for i_neighbour in l_neighbours:
			new_rect = make_cur_rect(i_neighbour)
			if animate:
				scene.play(Transform(big_rect, new_big_rect), Transform(cur_rect, new_rect))

			if animate:
				scene.play(Indicate(v_edges[i_skill][i_neighbour], color=PASTEL_YELLOW))
			l_indegs[i_neighbour] += 1

			new_indeg = Text(str(l_indegs[i_neighbour]), font_size=24).move_to(v_indegs[2][i_neighbour].get_center())
			if animate:
				scene.play(
					Flash(v_indegs[2][i_neighbour], color=skill_colours[i_neighbour]),
					Transform(v_indegs[2][i_neighbour], new_indeg)
				)
			v_indegs[2][i_neighbour] = new_indeg

	if animate:
		scene.play(FadeOut(big_rect), FadeOut(cur_rect))
	return l_indegs, v_indegs



def create_queue(scene, indegs, animate=True):
	l_indegs, v_indegs = indegs[0], indegs[1]

	l_queue = []
	queue_text = Text("queue", font_size=20, color=GRAY).move_to(LEFT*1.5 + UP*1.5)
	if animate:
		scene.play(FadeIn(queue_text))


	def make_cur_rect_id(i):
		return SurroundingRectangle(
			VGroup(v_indegs[1][i], v_indegs[2][i]), buff=0.25, fill_opacity=0, 
			stroke_color=WHITE, stroke_width=0.5
		)

	cur_rect_id = make_cur_rect_id(0)

	v_queue = VGroup(queue_text)
	for i_skill in range(len(l_indegs)):
		new_rect_id = make_cur_rect_id(i_skill)
		if animate:
			scene.play(Transform(cur_rect_id, new_rect_id))

		if l_indegs[i_skill] == 0:
			l_queue.append(i_skill)
			skill_letter = v_indegs[1][i_skill].copy().next_to(v_queue[-1], RIGHT, buff=0.5)
			v_queue.add(skill_letter)

			if animate:
				scene.play(Indicate(v_indegs[2][i_skill], color=PASTEL_RED))
				scene.play(ReplacementTransform(v_indegs[1][i_skill].copy(), skill_letter))

	if animate:
		scene.play(FadeOut(cur_rect_id))
	return l_queue, v_queue



def perform_kahn(scene, v_graph, indegs, queue):
	l_indegs, v_indegs = indegs[0], indegs[1]
	l_queue, v_queue = queue[0], queue[1]
	v_nodes, v_edges = v_graph[0], v_graph[1]

	l_order = []
	order_text = Text("order", font_size=20, color=GRAY).move_to(LEFT*3.5 + UP*2.5)
	scene.play(FadeIn(order_text))


	def make_cur_rect(i):
		return SurroundingRectangle(
			v_queue[i+1], buff=0.25, fill_opacity=0, 
			stroke_color=WHITE, stroke_width=0.5
		)

	v_order = VGroup(order_text)
	while len(l_queue) != 0:
		i_skill = l_queue[0]
		l_queue.pop(0)

		cur_rect = make_cur_rect(0)
		scene.play(FadeIn(cur_rect))

		l_order.append(i_skill)
		skill_letter = v_queue[1].copy().next_to(v_order[-1], RIGHT, buff=0.5)
		v_order.add(skill_letter)

		# Unlock node and add to order
		scene.play(
			Flash(v_nodes[i_skill][0], color=skill_colours[i_skill]), 
			v_nodes[i_skill][0].animate.set_opacity(0.2).set_stroke_width(4).set_stroke_color(skill_colours[i_skill])
		)
		scene.play(
			ReplacementTransform(v_queue[1].copy(), skill_letter),
			cur_rect.animate.move_to(skill_letter.get_center()),
			FadeOut(v_queue[1])
		)

		# Remove from queue
		v_queue.remove(v_queue[1])
		if len(v_queue) != 1:	
			scene.play(*[v_queue[i].animate.shift(LEFT*0.6) for i in range(1, len(v_queue))])

		if i_skill in d_adj:
			deg_rect = VMobject()
			nei_rect = VMobject()
			for i_neighbour in d_adj[i_skill]:
				new_deg_rect = SurroundingRectangle(VGroup(v_indegs[1][i_neighbour], v_indegs[2][i_neighbour]), stroke_width=0.5, stroke_color=WHITE)
				new_nei_rect = SurroundingRectangle(v_nodes[i_neighbour], stroke_width=0.5, stroke_color=WHITE)
				scene.play(Transform(deg_rect, new_deg_rect), Transform(nei_rect, new_nei_rect))

				l_indegs[i_neighbour] -= 1

				new_indeg = Text(str(l_indegs[i_neighbour]), font_size=24).move_to(v_indegs[2][i_neighbour].get_center())
				scene.play(v_edges[i_skill][i_neighbour].animate.set_opacity(0.1))
				scene.play(Transform(v_indegs[2][i_neighbour], new_indeg))

				if l_indegs[i_neighbour] == 0:
					l_queue.append(i_neighbour)
					skill_letter = v_indegs[1][i_neighbour].copy().next_to(v_queue[-1], RIGHT, buff=0.5)

					scene.play(Indicate(v_indegs[2][i_neighbour], color=PASTEL_RED))
					scene.play(ReplacementTransform(v_indegs[1][i_neighbour].copy(), skill_letter))
					v_queue.add(skill_letter)

			scene.play(FadeOut(deg_rect), FadeOut(nei_rect))
		scene.play(FadeOut(cur_rect))

	return l_order, v_order



class TopoSortIntroduction(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		sh = ShortHint(self, "You are designing the skills for a game.")
		sh.create_hint()	


		
		v_skill_prerequisites = get_skill_prerequisites_map()
		self.play(Create(v_skill_prerequisites.move_to(ORIGIN)))
		self.wait(2)


		sh.change_hint("Each skill comes with a set of\nprerequisites which must be unlocked first.")

		skill_heading = Text("Skill", font_size=24, weight=BOLD).next_to(v_skill_prerequisites[0][0], UP, buff=0.5)
		self.play(FadeIn(skill_heading))

		right_edge = max(row[0].get_right()[0] for row in v_skill_prerequisites) + 0.5
		prerequisite_heading = Text("Prerequisites", font_size=24, weight=BOLD).next_to([right_edge, skill_heading.get_center()[1], 0], RIGHT, buff=0.5)
		self.play(FadeIn(prerequisite_heading))

		self.wait(2)


		sh.change_hint("Can you find a valid order in which the\ncharacter can unlock every skill?")
		self.wait(5)



class TopoSortMakeGraph(Scene):
	def construct(self):

		Text.set_default(font=MONOSPACE_FONT)

		v_prerequisites_map = get_skill_prerequisites_map().move_to(ORIGIN)
		self.add(v_prerequisites_map)

		sh = ShortHint(self, "Topological Sort", font_size=36)
		sh.create_hint()	
		self.wait(2)


		self.play(v_prerequisites_map.animate.shift(DOWN*4))

		title = Text("Algorithm Mini Challenges #4", font_size=30, t2c={"#4": LIGHT_PINK}).move_to(UP*4.5)
		self.play(Write(title))
		self.wait(2)
		self.play(FadeOut(title))


		v_graph = create_graph(self, animate_info=(True, v_prerequisites_map))
		self.play(v_graph.animate.shift(DOWN*3))
		self.wait(5)



class TopoSortInDegrees(Scene):
	def construct(self):

		Text.set_default(font=MONOSPACE_FONT)

		sh = ShortHint(self, "Kahn's Algorithm", font_size=36)
		sh.create_hint()

		v_graph = create_graph(self, graph_origin=DOWN)
		self.add(v_graph)
		self.wait(2)

		self.play(v_graph.animate.scale(0.75).shift(DOWN*2))


		sh.change_hint("in-degree: Number of incoming edges.\nRepresents prerequisites yet to unlock.", t2c={'in-degree': PASTEL_BLUE})
		self.wait(5)

		l_indegs, v_indegs = create_indegrees(self, v_graph, animate=True)
		self.wait(1)


		sh.change_hint("Add all 0 in-degree nodes to a queue.")
		l_queue, v_queue = create_queue(self, (l_indegs, v_indegs), animate=True)
		self.wait(5)



class TopoSortKahn(Scene):
	def construct(self):

		Text.set_default(font=MONOSPACE_FONT)

		v_graph = create_graph(self, graph_origin=DOWN)
		self.add(v_graph.scale(0.75).shift(DOWN*2))

		l_indegs, v_indegs = create_indegrees(self, v_graph, animate=False)
		self.add(v_indegs)

		l_queue, v_queue = create_queue(self, (l_indegs, v_indegs), animate=False)
		self.add(v_queue)

		perform_kahn(self, v_graph, (l_indegs, v_indegs), (l_queue, v_queue))
		self.wait(5)

