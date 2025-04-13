from manim import *


config.background_color = "#15131c"


class PythonIntro(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		

		blue_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(LEFT)

		yellow_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(RIGHT)

		blue_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(UP)

		yellow_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(DOWN)	

		eye_1 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(blue_vertical.get_center()).shift(UP*0.4 + LEFT*0.4)

		eye_2 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(yellow_vertical.get_center()).shift(DOWN*0.4 + RIGHT*0.4)
		
		python_logo = VGroup(blue_horizontal, yellow_horizontal, blue_vertical, yellow_vertical, eye_1, eye_2)
		self.play(Create(python_logo))
		self.wait(10)


class TenCounter(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		colours = [MAROON, RED, ORANGE, GOLD, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]

		count_rect = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.3,
			stroke_width=6,
			stroke_color=WHITE
		).shift(RIGHT*2)
		count_text = Text("Line Count", font_size=24).move_to(count_rect.get_center()).shift(UP*0.25)
		count_num = Text("1", font_size=30, color=MAROON).move_to(count_rect.get_center()).shift(DOWN*0.25)

		self.play(Create(count_rect), Write(count_text))
		self.play(FadeIn(count_num), run_time=0.2)

		for i in range(1, 51):
			self.play(Transform(count_num, Text(str(i), font_size=30, color=colours[(i-1)%10]).move_to(count_rect.get_center()).shift(DOWN*0.25)), run_time=0.2)
		self.wait(5)


class MakeSnake(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		

		blue_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(LEFT)

		yellow_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(RIGHT)

		blue_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(UP)

		yellow_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(DOWN)	

		eye_1 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(blue_vertical.get_center()).shift(UP*0.4 + LEFT*0.4)

		eye_2 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(yellow_vertical.get_center()).shift(DOWN*0.4 + RIGHT*0.4)
		
		python_logo = VGroup(blue_horizontal, yellow_horizontal, blue_vertical, yellow_vertical, eye_1, eye_2)
		self.play(Create(python_logo))


		snake_body = RoundedRectangle(
			width=5, height=1, 
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			color="#306998", 
			fill_opacity=1
		)

		snake_head = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).move_to(snake_body.get_center()).shift(RIGHT*3)

		eye_3 = Circle(
			radius=0.1,
			color=WHITE,
			fill_opacity=1
		).move_to(snake_head.get_center()).shift(UP*0.2 + RIGHT*0.5)

		eye_4 = Circle(
			radius=0.1,
			color=WHITE,
			fill_opacity=1
		).move_to(snake_head.get_center()).shift(DOWN*0.2 + RIGHT*0.5)

		snake_boi = VGroup(snake_body, snake_head, eye_3, eye_4).move_to(ORIGIN)
		self.play(ReplacementTransform(python_logo, snake_boi))
		self.wait(10)


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

		squares.move_to(ORIGIN)
		self.play(Create(squares))

		dir_text = Text("Direction: ", font_size=24)
		dir_arrow = Arrow(start=UP*0.5, end=DOWN*0.5)
		dir_stuff = VGroup(dir_text, dir_arrow).arrange(RIGHT).move_to(UP*3)
		self.play(Write(dir_text), GrowArrow(dir_arrow))

		self.play(squares.animate.move_to(LEFT*3))

		snek = squares.copy()
		self.play(snek.animate.move_to(RIGHT*3))
		self.wait(2)

		for i in range(0, len(snek)):
			if i < len(snek)-1:
				next_coord = snek[i+1][1].copy().move_to(snek[i][1].get_center())
				self.play(ReplacementTransform(snek[i][1], next_coord))
				self.play(snek[i].animate.move_to(snek[i+1].get_center()))

			else:
				next_coord = Text('('+str(segments[-1][0]+1)+','+str(segments[-1][1])+')', font_size=16).move_to(snek[i][1].get_center())
				self.play(ReplacementTransform(snek[i][1], next_coord))
				self.play(snek[i].animate.shift(DOWN))
		self.wait(2)

		for i in range(0, len(snek)-1):
			self.play(
				snek[i].animate.set_color(LIGHT_GRAY),
				squares[i+1].animate.set_color(LIGHT_GRAY)
			)
		self.wait(2)


class SnakeMove2(Scene):
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

		squares.move_to(LEFT*3)
		self.add(squares)

		dir_text = Text("Direction: ", font_size=24)
		dir_arrow = Arrow(start=UP*0.5, end=DOWN*0.5)
		dir_stuff = VGroup(dir_text, dir_arrow).arrange(RIGHT).move_to(UP*3)
		self.add(dir_stuff)

		snek = squares.copy().move_to(RIGHT*3)
		self.add(snek)

		self.wait(2)

		self.play(FadeOut(snek[0]))

		i = len(snek)-1
		i, j = segments[-1][0]+1, segments[-1][1]
		snake_piece = Rectangle(
			width=1, height=1, 
			color=LIGHT_BROWN, 
			fill_opacity=1,
			stroke_width=0
		).move_to(snek[len(snek)-1].get_center()).shift(DOWN)
		snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
		scale = VGroup(snake_piece, snake_coords)

		self.play(FadeIn(snake_piece))
		self.play(Write(snake_coords))
		self.wait(2)


class WASD(Scene):
	def create_key(self, letter, position):
		key = Rectangle(
			width=1, height=1,
			color=GRAY_A,
			fill_opacity=1,
			stroke_width=0
		).move_to(position)
		text = Text(letter, color=BLACK).move_to(key.get_center())
		group = VGroup(key, text)
		self.add(group)

		return group;

	def press_key(self, key, pos, asc):
		ascii_text = Text(asc).next_to(key, pos)

		self.play(
			key[0].animate.set_color(GRAY),
			FadeIn(ascii_text),
			run_time=0.5
		)

		self.play(
			key[0].animate.set_color(GRAY_A),
			FadeOut(ascii_text),
			run_time=0.5
		)

	def construct(self):
		Text.set_default(font="Monospace")

		s_key = self.create_key("S", ORIGIN)
		w_key = self.create_key("W", ORIGIN+UP)
		a_key = self.create_key("A", ORIGIN+LEFT)
		d_key = self.create_key("D", ORIGIN+RIGHT)

		self.press_key(w_key, UP, "119")
		self.press_key(a_key, LEFT, "97")
		self.press_key(s_key, DOWN, "115")
		self.press_key(d_key, RIGHT, "100")

		self.press_key(w_key, UP, "119")
		self.press_key(a_key, LEFT, "97")
		self.press_key(s_key, DOWN, "115")
		self.press_key(d_key, RIGHT, "100")


class UnitVectors(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-2, 2, 1],
			y_range=[-2, 2, 1],
			x_length=6, y_length=6,
			tips=False,
		)

		axes.y_axis.scale(-1)
		axes.add_coordinates()
		self.add(axes)

		vectors_info = [
			{"coord": [0, -1], "label": "W", "label_shift": UP*2 + LEFT*0.5},
			{"coord": [-1, 0], "label": "A", "label_shift": LEFT*2 + DOWN*0.5},
			{"coord": [0, 1], "label": "S", "label_shift": DOWN*2 + RIGHT*0.5},
			{"coord": [1, 0], "label": "D", "label_shift": RIGHT*2 + UP*0.5},
		]
		origin = axes.c2p(0, 0)

		colors = [RED, PURPLE, GREEN, GOLD]

		for i in range(0, 4):
			info = vectors_info[i]

			end = axes.c2p(*info["coord"])
			vector = Arrow(start=origin, end=end, color=colors[i], buff=0)
			label = Text(info["label"], color=colors[i]).next_to(end, info["label_shift"])
			self.play(GrowArrow(vector), FadeIn(label))

			self.wait(0.5)

		self.wait(2)


class EatFood(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		segments = [[1, 0], [2, 0], [3, 0]]
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
			squares.add(snake_piece)
			count += 1

		self.add(squares)

		food = Dot(color=WHITE, radius=0.2).move_to(ORIGIN + UP)
		self.add(food)

		count = 0
		while count >= -1:
			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[(count+1)%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*count)

			squares.insert(0, snake_piece)
			self.play(FadeOut(squares[-1]), FadeIn(squares[0]))
			squares.remove(squares[-1])

			count -= 1;

		dont_pop = Text("Don't pop tail", font_size=24).move_to(DOWN*2)

		snake_piece = Rectangle(
			width=1, height=1, 
			color=colours[(count+1)%2], 
			fill_opacity=1,
			stroke_width=0
		).move_to(ORIGIN + UP*2)

		self.play(Write(dont_pop))
		self.play(FadeIn(snake_piece))
		squares.insert(0, snake_piece)

		count += 1
		snake_piece = Rectangle(
			width=1, height=1, 
			color=colours[(count+1)%2], 
			fill_opacity=1,
			stroke_width=0
		).move_to(ORIGIN + UP*3)

		squares.insert(0, snake_piece)
		self.play(FadeOut(dont_pop), FadeOut(squares[-1]), FadeIn(squares[0]))
		squares.remove(squares[-1])

		self.wait(3)


class OppositeDirections(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		axes = Axes(
			x_range=[-2, 2, 1],
			y_range=[-2, 2, 1],
			x_length=6, y_length=6,
			tips=False,
		)

		axes.y_axis.scale(-1)
		axes.add_coordinates()
		self.add(axes)

		vectors_info = [
			{"coord": [0, -1], "label": "W", "label_shift": UP*2 + LEFT*0.5},
			{"coord": [-1, 0], "label": "A", "label_shift": LEFT*2 + DOWN*0.5},
			{"coord": [0, 1], "label": "S", "label_shift": DOWN*2 + RIGHT*0.5},
			{"coord": [1, 0], "label": "D", "label_shift": RIGHT*2 + UP*0.5},
		]
		origin = axes.c2p(0, 0)

		colors = [RED, PURPLE, GREEN, GOLD]
		vectors = VGroup()
		labels = VGroup()

		for i in range(0, 4):
			info = vectors_info[i]
			end = axes.c2p(*info["coord"])

			vector = Arrow(start=origin, end=end, color=colors[i], buff=0)
			label = Text(info["label"], color=colors[i]).next_to(end, info["label_shift"])

			vectors.add(vector)
			labels.add(label)

		self.add(vectors)
		self.add(labels)

		vector_adding = Text("W + S\n= [0, -1] + [0, 1]\n= [0, 0]", font_size=24).move_to(RIGHT*3 + UP*2)
		self.play(Write(vector_adding));
		self.play(FadeOut(vectors[0]), FadeOut(labels[0]), FadeOut(vectors[2]), FadeOut(labels[2]), FadeOut(vector_adding))

		vector_adding = Text("A + D\n= [-1, 0] + [1, 0]\n= [0, 0]", font_size=24).move_to(RIGHT*3 + UP*2)
		self.play(Write(vector_adding))
		self.play(FadeOut(vectors[1]), FadeOut(labels[1]), FadeOut(vectors[3]), FadeOut(labels[3]), FadeOut(vector_adding))

		self.wait(2)


class DrawAndGlowLetter(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        self.play(Write(Text("Thank you for watching!").shift(UP*2)))

        letter_e = Text("e", font_size=200, color=TEAL)
        self.play(Write(letter_e))

        letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
        glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
        self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
        self.play(FadeOut(letter_e_stroke, glow_effect))

        self.wait(3)