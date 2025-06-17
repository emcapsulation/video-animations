from manim import *


config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class SnakeMove(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		segments = [[4, 0], [4, 1], [4, 2], [3, 2], [2, 2], [1, 2], [0, 2], [0, 3], [0, 4]]
		squares = VGroup()
		
		colours = [GREEN, LIGHT_BROWN]
		count = 0
		for piece in segments:
			i, j = piece[0], piece[1]

			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[count%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*i + RIGHT*j)
			snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
			scale = VGroup(snake_piece, snake_coords)

			squares.add(scale)
			count += 1

		self.add(squares.move_to(ORIGIN+DOWN))

		dir_text = Text("Direction: ", font_size=24)
		dir_arrow = Arrow(start=UP*0.5, end=DOWN*0.5)
		dir_stuff = VGroup(dir_text, dir_arrow).arrange(RIGHT).move_to(UP*3)
		self.add(dir_stuff)

		self.wait(2)

		self.play(FadeOut(squares[0]))

		i = len(squares)-1
		i, j = segments[-1][0]+1, segments[-1][1]
		snake_piece = Rectangle(
			width=1, height=1, 
			color=LIGHT_BROWN, 
			fill_opacity=1,
			stroke_width=0
		).move_to(squares[len(squares)-1].get_center()).shift(DOWN)
		snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
		scale = VGroup(snake_piece, snake_coords)

		self.play(FadeIn(snake_piece))
		self.play(Write(snake_coords))
		self.wait(2)