from manim import *
import random


class Board:
	def __init__(self, w, l, r, g, t=None):
		self.w = w
		self.l = l
		self.r = r
		self.g = g
		self.t = t

		self.num_teams = len(self.w)

		if t == None:
			self.teams = self.get_teams()
		else:
			self.teams = self.get_teams(t[0], t[1])

		self.grid = VGroup()



	# Randomly generate team logos
	def get_teams(self, colour_list=None, shape_list=None):
		colors = colour_list
		shapes = shape_list

		if colour_list == None:
			colour_list = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED, MAROON, PURPLE, PINK]
			colors = random.sample(colour_list, self.num_teams)
		if shape_list == None:
			shape_list = [Circle(), Square(), Triangle(), RegularPolygon(n=4), RegularPolygon(n=5), RegularPolygon(n=6)]
			shapes = random.sample(shape_list, self.num_teams)	

		teams = []
		for i in range(0, self.num_teams):
			teams.append(shapes[i].scale(0.3).set_color(colors[i]).set_fill(colors[i], 1))
		return teams


	# Creates the grid
	def create_grid(self):
		heading_text = ["t", "w", "l", "r"]
		if self.l == None:
			heading_text = ["t", "w", "r"]

		headings = VGroup()
		for h in heading_text:
			headings.add(Text(h))		

		for t in self.teams:
			headings.add(t.copy())

		headings.arrange(buff=0.95)
		headings[0].set_opacity(0)
		self.grid.add(headings)

		vectors = [self.teams, self.w, self.l, self.r, self.g]
		if self.l == None:
			vectors = [self.teams, self.w, self.r, self.g]

		for i in range(0, len(vectors[0])):
			row = VGroup(self.teams[i])

			for v in range(1, len(vectors)-1):
				row.add(Text(str(vectors[v][i]), font_size=36))

			for c in range(0, len(vectors[len(vectors)-1][i])):
				rem = Text(str(vectors[len(vectors)-1][i][c]), font_size=36)
				if c == i:
					rem.set_opacity(0)
				row.add(rem)

			row.arrange(buff=1)
			self.grid.add(row)

		self.grid.arrange(DOWN, buff=0.8)	

		# Fix up the heading alignment
		self.grid[0].shift(RIGHT*0.7)
		for i in range(4, len(self.grid[0])):
			self.grid[0][i].shift(LEFT*0.15 + LEFT*(i-4)*0.3)


	# Moves row i to row j
	def swap_rows(self, scene, i, j):
		background_rect = Rectangle(
			width=self.grid[i].get_width()+0.5, 
			height=self.grid[i].get_height()+0.5, 
			fill_color="#2c2336",
			stroke_width=0.5).move_to(
				self.grid[i].get_center()
			).set_opacity(0.3)

		scene.play(FadeIn(background_rect))

		shuffle = [self.grid[k].animate.move_to(self.grid[k+1].get_center()) for k in range(i-1, j-1, -1)]
		scene.play(
			LaggedStart(*shuffle, lag_ratio=1/(i-j)),
			self.grid[i].animate.move_to(self.grid[j].get_center()),
			background_rect.animate.move_to(self.grid[j].get_center()),
			run_time=1
		)
		scene.play(FadeOut(background_rect))

		# Swap the rows in the grid
		tmp = self.grid[i]
		for k in range(i, j, -1):
			self.grid[k] = self.grid[k-1]	
		self.grid[j] = tmp	


	# Gets the row number of the team in this column
	def get_team_row(self, j):
		team_color = self.grid[0][j].get_color()

		for i in range(1, len(self.grid)):
			if self.grid[i][0].get_color() == team_color:
				return i

		return -1


	# Increments number of wins for team
	def increment_wins(self, scene, team, num_wins, scale=0.8):
		row = self.grid[team]

		for i in range(1, num_wins-int(row[1].get_text())+1):
			scene.play(
				Transform(row[1], Text(str(int(row[1].get_text())+i), font_size=36, color=GREEN).move_to(row[1].get_center()).scale(scale)),
				Transform(row[3], Text(str(int(row[3].get_text())-i), font_size=36).move_to(row[3].get_center()).scale(scale))
			)

		scene.play(
			row[1].animate.set_color(WHITE)
		)


	# Increments number of wins for a team and decrements remaining games too
	def increment_wins_2(self, scene, team, num_wins, scale=0.8):
		row = self.grid[team]

		for i in range(1, num_wins-int(row[1].get_text())+1):
			dec_cells = []
			inc_cells = []

			for j in range(4, len(row)):
				if row[j].get_text() != "0":
					dec_cells.append(row[j])
					row_num = self.get_team_row(j)

					if row_num != -1:
						# Team remain column
						dec_cells.append(self.grid[row_num][4+team-1])

						# Remain column
						dec_cells.append(self.grid[row_num][3])

						# Loss column
						inc_cells.append(self.grid[row_num][2])
					break


			incs = [ReplacementTransform(ic, Text(str(int(ic.get_text())+1), font_size=36).move_to(ic.get_center()).scale(scale)) for ic in inc_cells]
			decs = [ReplacementTransform(dc, Text(str(int(dc.get_text())-1), font_size=36).move_to(dc.get_center()).scale(scale)) for dc in dec_cells]

			incs.append(ReplacementTransform(row[1], Text(str(int(row[1].get_text())+1), font_size=36, color=GREEN).move_to(row[1].get_center()).scale(scale)))
			decs.append(ReplacementTransform(row[3], Text(str(int(row[3].get_text())-1), font_size=36).move_to(row[3].get_center()).scale(scale)))

			scene.play(
				*incs, *decs
			)

		scene.play(
			row[1].animate.set_color(WHITE),
			row[3].animate.set_color(WHITE)
		)


	# Increments number of losses for a team and decrements remaining games too
	def increment_losses_2(self, scene, team, num_losses, scale=0.8):
		row = self.grid[team]
		row_num = 0

		for i in range(1, num_losses-int(row[2].get_text())+1):
			dec_cells = []
			inc_cells = []

			for j in range(4, len(row)):
				if row[j].get_text() != "0":
					dec_cells.append(row[j])
					row_num = self.get_team_row(j)

					if row_num != -1:
						# Team remain column
						dec_cells.append(self.grid[row_num][4+team-2])

						# Remain column
						dec_cells.append(self.grid[row_num][3])

						# Win column
						inc_cells.append(self.grid[row_num][1])
					break

			incs = [ReplacementTransform(ic, Text(str(int(ic.get_text())+1), font_size=36, color=GREEN).move_to(ic.get_center()).scale(scale)) for ic in inc_cells]
			decs = [ReplacementTransform(dc, Text(str(int(dc.get_text())-1), font_size=36).move_to(dc.get_center()).scale(scale)) for dc in dec_cells]

			incs.append(ReplacementTransform(row[2], Text(str(int(row[2].get_text())+1), font_size=36, color=RED).move_to(row[2].get_center()).scale(scale)))
			decs.append(ReplacementTransform(row[3], Text(str(int(row[3].get_text())-1), font_size=36).move_to(row[3].get_center()).scale(scale)))

			scene.play(
				*incs, *decs
			)


		scene.play(
			row[2].animate.set_color(WHITE),
			row[3].animate.set_color(WHITE),
			self.grid[row_num][1].animate.set_color(WHITE)
		)


	# Sets the row colour except the shape
	def set_row_color(self, scene, i, color):
		set_colours = [self.grid[i][k].animate.set_color(color) for k in range(1, len(self.grid[i]))]
		scene.play(*set_colours)


	# Fades out row i and shifts everyone else up
	def fade_out_row(self, scene, i):
		# Shuffle everyone else after it up
		shuffle = [self.grid[k].animate.move_to(self.grid[k-1].get_center()) for k in range(i+1, len(self.grid))]

		scene.play(FadeOut(self.grid[i]))
		scene.play(
			LaggedStart(*shuffle, lag_ratio=1/(len(self.grid)-i)),
			run_time=1
		)
		self.grid -= self.grid[i]


	# Put a rectangle around a row
	def put_rectangle_around(self, scene, i):
		surround = SurroundingRectangle(
			self.grid[i],
			buff=0.4,
			color=WHITE
		)

		scene.play(Create(surround))
		return surround


	# Put a rectangle around a row
	def add_rectangle_around(self, scene, i):
		surround = SurroundingRectangle(
			self.grid[i],
			buff=0.4,
			color=WHITE
		)

		scene.add(surround)
		return surround


	# Put a rectangle around multiple rows
	def put_rectangle_around_2(self, scene, a):
		rect_group = VGroup()
		for k in a:
			rect_group.add(self.grid[k])

		surround = SurroundingRectangle(
			rect_group,
			buff=0.4,
			color=WHITE
		)

		return surround


	# Animates winning games
	def win_games(self, scene, vs, wins, scale=0.4):
		t1, t2 = vs[0], vs[1]
		w1, w2 = wins[0], wins[1]

		for i in range(0, 2):
			win_team = vs[i]

			for j in range(0, wins[i]):
				inc_cells = [self.grid[win_team+1][1]]
				dec_cells = [self.grid[t1+1][t2+1+2], self.grid[t2+1][t1+1+2], self.grid[t1+1][2], self.grid[t2+1][2]]

				incs = [ReplacementTransform(ic, Text(str(int(ic.get_text())+1), font_size=30, color=GREEN).move_to(ic.get_center()).scale(scale)) for ic in inc_cells]
				decs = [ReplacementTransform(dc, Text(str(int(dc.get_text())-1), font_size=30).move_to(dc.get_center()).scale(scale)) for dc in dec_cells]

				scene.play(
					*incs, *decs
				)

			scene.play(
				self.grid[win_team+1][1].animate.set_color(WHITE)
			)


