from manim import *
import random


class Board:
	def __init__(self, w, l, r, g):
		self.w = w
		self.l = l
		self.r = r
		self.g = g

		self.num_teams = len(self.w)
		self.teams = self.get_teams()

		self.grid = VGroup()



	# Randomly generate team logos
	def get_teams(self):
		colour_list = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED, MAROON, PURPLE, PINK]
		colors = random.sample(colour_list, self.num_teams)
		shape_list = [Circle(), Square(), Triangle(), RegularPolygon(n=4), RegularPolygon(n=5), RegularPolygon(n=6)]
		shapes = random.sample(shape_list, self.num_teams)

		teams = []
		for i in range(0, self.num_teams):
			teams.append(shapes[i].scale(0.3).set_color(colors[i]).set_fill(colors[i], 1))
		return teams


	# Creates the grid
	def create_grid(self):
		heading_text = ["t", "w", "l", "r"]

		headings = VGroup()
		for h in heading_text:
			headings.add(Text(h))		

		for t in self.teams:
			headings.add(t.copy())

		headings.arrange(buff=0.95)
		headings[0].set_opacity(0)
		self.grid.add(headings)

		vectors = [self.teams, self.w, self.l, self.r, self.g]

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



	# Increments number of wins for team
	def increment_wins(self, scene, team, num_wins):
		row = self.grid[team]

		row[1].set_color(GREEN)
		row[3].set_color(GREEN)

		for i in range(1, num_wins-int(row[1].get_text())+1):
			scene.play(
				Transform(row[1], Text(str(int(row[1].get_text())+i), font_size=36, color=GREEN).move_to(row[1].get_center()).scale(0.8)),
				Transform(row[3], Text(str(int(row[3].get_text())-i), font_size=36, color=GREEN).move_to(row[3].get_center()).scale(0.8))
			)

		print("HI")