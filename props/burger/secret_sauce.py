from manim import *

class SecretSauce:
	def __init__(self, type):
		self.type = type
		self.secret_sauce = self.make_secret_sauce()
		self.secret_sauce_with_background = self.make_secret_sauce_with_background()


	def get_secret_sauce(self):
		return self.secret_sauce

	def get_secret_sauce_with_background(self):
		return self.secret_sauce_with_background

	def get_paper(self):
		return self.secret_sauce[0]

	def get_title(self):
		return self.secret_sauce[1]

	def get_lines(self):
		return self.secret_sauce[2]

	def get_background(self):
		return self.secret_sauce_with_background[0]


	def make_secret_sauce(self):
		secret_sauce = VGroup()		

		paper = RoundedRectangle(
			width=3, height=4,
			corner_radius=0.2,
			color=LOGO_WHITE,
			fill_opacity=0.85
		)


		title = None
		if self.type == "shapes" or self.type == "text" or self.type == "tampered" or self.type == "tampered_2":
			title = Text(
				"Secret Sauce",
				color=BLACK,
				font_size=22
			).shift(UP*1.1)

		elif self.type == "encrypted":
			title = Text(
				"qL7#xP$v@Kf2!W",
				color=BLACK,
				font_size=22
			).shift(UP*1.1)


		lines = None
		if self.type == "shapes":
			writing = RoundedRectangle(
				width=3.6, height=0.15,
				corner_radius=[0.05, 0.05, 0.05, 0.05],
				stroke_color=BLACK,
				fill_color=BLACK,
				fill_opacity=1
			)
			lines = VGroup(
				writing, 
				writing.copy(), 
				writing.copy(), 
				writing.copy(), 
				writing.copy(), 
				writing.copy()
			).arrange(DOWN, buff=0.5).scale(0.5).shift(DOWN*0.5)

		elif self.type == "text" or self.type == "tampered" or self.type == "tampered_2":
			text_1 = Text("2 tbsp mayonnaise", font_size=16, color=BLACK)
			text_2 = Text("2 tbsp ketchup", font_size=16, color=BLACK)
			text_3 = Text("1 tbsp mustard", font_size=16, color=BLACK)
			text_4 = Text("1 tsp paprika", font_size=16, color=BLACK)
			text_5 = Text("1 clove garlic", font_size=16, color=BLACK)
			if self.type == "tampered":
				text_5 = Text("10 chillis", font_size=16, color=RED)
			elif self.type == "tampered_2":
				text_5 = Text("0 clove garlic", font_size=16, color=RED)
			lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

		elif self.type == "encrypted":
			text_1 = Text("f9@Lz#Wq8v!2Xp$N", font_size=16, color=BLACK)
			text_2 = Text("B#v5$eYp!tn8Wz@J", font_size=16, color=BLACK)
			text_3 = Text("xM7&rA^Fz3@b!gPL", font_size=16, color=BLACK)
			text_4 = Text("Z!uT@p#qE9*WsLd^", font_size=16, color=BLACK)
			text_5 = Text("r%NyB!q2$GKz*vM@", font_size=16, color=BLACK)
			lines = VGroup(text_1, text_2, text_3, text_4, text_5).arrange(DOWN, buff=0.2).shift(DOWN*0.5)

		secret_sauce.add(paper, title, lines)
		return secret_sauce


	def make_secret_sauce_with_background(self):
		circle = Circle(
			radius=3,
			color=GOLD_A,
			fill_opacity=0.85
		)

		secret_sauce_with_background = VGroup(circle, self.secret_sauce)
		return secret_sauce_with_background