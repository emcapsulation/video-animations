from manim import *
from entities import *
import random


config.background_color = "#15131c"


class Introduction(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		# Store contains (wall, poster, counter)
		burger_store = BurgerStore()
		self.add(burger_store.get_burger_store())


		# Draw in each member of the family
		y_pos = DOWN*0.37
		positions = [RIGHT*5+y_pos, *[LEFT*x+y_pos for x in range(5, -5, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family.set_labels(["You", "Grandpa", "Uncle", "Dad", "Mum", "Brother"])
		family.set_colours([PURPLE, ORANGE, GOLD, GREEN, TEAL, BLUE])

		family_list = family.get_family_list()
		for family_member in family_list:
			self.play(Create(family_member.get_body()), Write(family_member.get_label()))
		self.wait(2)


		self.play(Wiggle(family_list[5].get_body()))


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)

		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Blog", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		website = VGroup(website_screen, website_text).move_to(screen.get_center())
		
		computer = VGroup(screen, website, close).scale(1.75)
		self.play(Create(computer))


		self.play(Wiggle(family_list[2].get_body()))
		hack_text = Text("/posts?filter=<script>alert(':D');</script>", font_size=14, color=GRAY_D).move_to(website.get_top()+LEFT*0.2+DOWN*0.25)
		self.play(AddTextLetterByLetter(hack_text))
		self.wait(2)



class WhatIsXss(Scene):

	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Cross-Site Scripting").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)

		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Website", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		website = VGroup(website_screen, website_text).move_to(screen.get_center())

		hack_text = Text("<script>alert(':D');</script>", font_size=14, color=PURE_RED)
		computer = VGroup(screen, website, close).scale(1.5)
		self.play(Create(computer))

		definition = Text("Cross-Site Scripting: Vulnerability which allows attackers to inject scripts into websites.", font_size=16, t2c={'Cross-Site Scripting:': RED}).move_to(DOWN*3)
		self.play(Write(definition))

		evil_guy = Human(RED, 0.8).human.scale(0.35).move_to(RIGHT*8)
		self.play(evil_guy.animate.move_to(computer.get_center() + RIGHT*3))
		self.play(Wiggle(evil_guy), AddTextLetterByLetter(hack_text))
		self.play(evil_guy.animate.move_to(RIGHT*8))
		self.wait(2)

		definition_2 = Text("Cross-Site Scripting: Victim's browser then executes the script.", font_size=16, t2c={'Cross-Site Scripting:': RED}).move_to(DOWN*3)
		self.play(Transform(definition, definition_2))

		you = Human(PURPLE, 0.8).add_label("You", WHITE).human.scale(0.35).move_to(LEFT*8)
		self.play(you.animate.move_to(computer.get_center() + LEFT*3))

		# TODO: Alert image pops up
		self.wait(2)
		exclamation = Text("!").next_to(you, UP)
		self.play(Wiggle(you), Indicate(exclamation))
		self.wait(2)


		hack_text_2 = Text("Redirecting...", font_size=14, color=PURE_RED)
		self.play(Transform(hack_text, hack_text_2))
		self.play(Indicate(exclamation))
		self.wait(1)

		hack_text_2 = Text("localStorage.getItem('sensitive_info');", font_size=14, color=PURE_RED)
		self.play(Transform(hack_text, hack_text_2))
		self.play(Indicate(exclamation))
		self.wait(1)

		hack_text_2 = Text("document.body.innerHTML = '<p>:D</p>';", font_size=14, color=PURE_RED)
		self.play(Transform(hack_text, hack_text_2))
		self.play(Indicate(exclamation))
		self.wait(1)


		self.play(FadeOut(hack_text), FadeOut(exclamation))

		frontend = Text("Frontend", font_size=24).move_to(LEFT*2.5 + UP*1.5)
		self.play(FadeOut(definition), you.animate.scale(0.9).shift(LEFT*2.5 + DOWN), computer.animate.scale(0.9).shift(LEFT*2.5 + DOWN), FadeIn(frontend))

		backend = Text("Backend", font_size=24).move_to(RIGHT*3.5 + UP*1.5)
		screen_2 = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close_2 = Dot(radius=0.075, color=RED).move_to(screen_2.get_center() + UP*0.75 + RIGHT*1.25)
		server_text = Text("Server", color=PURE_GREEN, font_size=16).move_to(screen_2.get_center() + UP*0.5)
		server = VGroup(screen_2, close_2, server_text).scale(1.1).shift(RIGHT*3.5 + DOWN)
		
		self.play(Create(server), FadeIn(backend))
		self.wait(2)

		not_your_machine = Text("not your machine", font_size=14, color=PURE_GREEN).move_to(server.get_center())
		self.play(AddTextLetterByLetter(not_your_machine))
		self.wait(2)

		browser = Text("your browser loads", font_size=14, color=BLACK).move_to(computer.get_center())
		self.play(AddTextLetterByLetter(browser))
		self.wait(2)



class ReflectedXss(Scene):

	def construct(self):
		Text.set_default(font="Monospace")	


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Website", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		website = VGroup(website_screen, website_text).move_to(screen.get_center())

		computer = VGroup(screen, website, close).scale(1.5).scale(0.9).shift(LEFT*2.5 + DOWN)
		frontend = Text("Frontend", font_size=24).move_to(LEFT*2.5 + UP*1.5)

		screen_2 = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close_2 = Dot(radius=0.075, color=RED).move_to(screen_2.get_center() + UP*0.75 + RIGHT*1.25)
		server_text = Text("Server", color=PURE_GREEN, font_size=16).move_to(screen_2.get_center() + UP*0.5)

		server = VGroup(screen_2, close_2, server_text).scale(1.1).shift(RIGHT*3.5 + DOWN)
		backend = Text("Backend", font_size=24).move_to(RIGHT*3.5 + UP*1.5)

		you = Human(PURPLE, 0.8).add_label("You", WHITE).human.scale(0.35).move_to(LEFT*8).move_to(computer.get_center() + LEFT*3)
		
		self.add(you, computer, frontend, server, backend)
		self.wait(2)


		title = Text("Reflected Cross-Site Scripting").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)

		definition = Text("Reflected XSS: Malicious script is sent in request and immediately reflected in response.", font_size=16, t2c={'Reflected XSS:': ORANGE}).move_to(DOWN*3)
		self.play(Write(definition))
		self.wait(2)

		request = Text("GET /posts?author=<script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": ORANGE}).move_to(LEFT*2.5 + UP)
		path = ArcBetweenPoints(LEFT*2.5 + UP, RIGHT*3.5 + UP, angle=-PI/4, color=GRAY)
		self.play(MoveAlongPath(request, path))
		self.wait(1)
		self.play(FadeOut(request, shift=DOWN*0.5))

		response = Text("Retrieved posts by:\n<script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": ORANGE}).move_to(server.get_center())
		self.play(AddTextLetterByLetter(response))
		self.wait(1)

		response_2 = Text("Retrieved posts by:\n<script>alert(':D');</script>", color=BLACK, font_size=14).move_to(computer.get_center())
		self.play(Transform(response, response_2))
		self.wait(1)

		exclamation = Text("!").next_to(you, UP)
		self.play(Wiggle(you), Indicate(exclamation))



class StoredXss(Scene):

	def construct(self):
		Text.set_default(font="Monospace")	


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Website", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		website = VGroup(website_screen, website_text).move_to(screen.get_center())

		computer = VGroup(screen, website, close).scale(1.5).scale(0.9).shift(LEFT*2.5 + DOWN)
		frontend = Text("Frontend", font_size=24).move_to(LEFT*2.5 + UP*1.5)

		screen_2 = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close_2 = Dot(radius=0.075, color=RED).move_to(screen_2.get_center() + UP*0.75 + RIGHT*1.25)
		server_text = Text("Server", color=PURE_GREEN, font_size=16).move_to(screen_2.get_center() + UP*0.5)

		server = VGroup(screen_2, close_2, server_text).scale(1.1).shift(RIGHT*3.5)
		backend = Text("Backend", font_size=24).move_to(RIGHT*3.5 + UP*1.5)		
		
		self.add(computer, frontend, server, backend)
		self.wait(2)


		title = Text("Stored Cross-Site Scripting").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)

		definition = Text("Stored XSS: Malicious script gets stored, then injected when the affected content is loaded.", font_size=16, t2c={'Stored XSS:': GOLD}).move_to(DOWN*3)
		self.play(Write(definition))
		self.wait(2)

		evil_guy = Human(RED, 0.8).human.scale(0.35).move_to(LEFT*8).move_to(computer.get_center() + LEFT*3)
		self.play(FadeIn(evil_guy, shift=RIGHT))

		browser_text = Text("title: New Post\nbody: <script>alert(':D');</script>", color=BLACK, font_size=14).move_to(computer.get_center())
		self.play(AddTextLetterByLetter(browser_text), Wiggle(evil_guy))
		self.wait(1)

		server_text = Text("Save post to DB", font_size=14).move_to(server.get_center())
		self.play(Transform(browser_text, server_text), evil_guy.animate.shift(LEFT*8))
		self.wait(1)

		db_text = VGroup(
			VGroup(Text("Title", font_size=14, weight=BOLD), Text("Body", font_size=14, weight=BOLD)).arrange(RIGHT, buff=1.5),
			VGroup(Text("New Post", font_size=14), Text("<script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": GOLD})).arrange(RIGHT)
		).arrange(DOWN).move_to(RIGHT*3.5 + DOWN*2)
		db_text[0].shift(LEFT*0.5)
		self.play(Transform(browser_text, db_text))
		self.wait(2)

		you = Human(PURPLE, 0.8).add_label("You", WHITE).human.scale(0.35).move_to(LEFT*8).move_to(computer.get_center() + LEFT*3)
		self.play(FadeIn(you, shift=RIGHT*1))

		request = Text("GET /posts", font_size=14, t2c={"<script>alert(':D');</script>": GOLD}).move_to(LEFT*2.5 + UP)
		path = ArcBetweenPoints(LEFT*2.5 + UP, RIGHT*3.5, angle=-PI/4, color=GRAY)
		self.play(MoveAlongPath(request, path))
		self.wait(1)		

		response = Text("title: New Post\nbody: <script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": GOLD}).scale(0.8).move_to(server.get_center())
		self.play(FadeOut(request))

		db_text_copy = db_text.copy()
		self.play(Transform(db_text_copy, response))
		self.wait(1)

		response_2 = Text("title: New Post\nbody: <script>alert(':D');</script>", color=BLACK, font_size=14).move_to(computer.get_center())
		self.play(Transform(db_text_copy, response_2))
		self.wait(1)

		exclamation = Text("!").next_to(you, UP)
		self.play(Wiggle(you), Indicate(exclamation))



class DomXss(Scene):

	def construct(self):
		Text.set_default(font="Monospace")	


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Website", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		website = VGroup(website_screen, website_text).move_to(screen.get_center())

		computer = VGroup(screen, website, close).scale(1.5).scale(0.9).shift(LEFT*2.5 + DOWN)
		frontend = Text("Frontend", font_size=24).move_to(LEFT*2.5 + UP*1.5)

		screen_2 = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close_2 = Dot(radius=0.075, color=RED).move_to(screen_2.get_center() + UP*0.75 + RIGHT*1.25)
		server_text = Text("Server", color=PURE_GREEN, font_size=16).move_to(screen_2.get_center() + UP*0.5)

		server = VGroup(screen_2, close_2, server_text).scale(1.1).shift(RIGHT*3.5 + DOWN)
		backend = Text("Backend", font_size=24).move_to(RIGHT*3.5 + UP*1.5)

		you = Human(PURPLE, 0.8).add_label("You", WHITE).human.scale(0.35).move_to(LEFT*8).move_to(computer.get_center() + LEFT*3)
		
		self.add(you, computer, frontend, server, backend)
		self.wait(2)


		title = Text("DOM-Based Cross-Site Scripting").move_to(UP*3)
		self.play(Write(title))
		self.wait(2)

		definition = Text("DOM-Based XSS: Malicious script is injected and executed entirely in the browser.", font_size=16, t2c={'DOM-Based XSS:': YELLOW}).move_to(DOWN*3)
		self.play(Write(definition))
		self.wait(2)

		request = Text("GET /posts?filter=<script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": YELLOW}).move_to(LEFT*2.5 + UP)
		self.play(request.animate.shift(DOWN*2))
		self.wait(1)

		response = Text("Filter:\n<script>alert(':D');</script>", color=BLACK, font_size=14).move_to(computer.get_center())
		self.play(Transform(request, response))
		self.wait(1)

		exclamation = Text("!").next_to(you, UP)
		self.play(Wiggle(you), Indicate(exclamation))



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



class Thumbnail(Scene):
	def construct(self):

		Text.set_default(font="Monospace")

		title_text = Text("Cross-Site Scripting").shift(UP*3)
		self.add(title_text)

		question_text = Text("Breaking My Own Website to Show You How to Defend Yours", 
			font_size=24,
			t2c={"Breaking": RED, "Defend": GREEN}
		).shift(UP*2)
		self.add(question_text)


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		website_screen = RoundedRectangle(height=1.75, width=2.75, fill_color="#faf5e8", stroke_width=0, fill_opacity=0.8, corner_radius=0.1)
		website_text = Text("Website", font_size=16, color=BLACK).move_to(website_screen.get_center() + UP*0.5)
		lock = Lock(LIGHT_BROWN).get_lock().scale(0.8).move_to(website_screen.get_center() + DOWN*0.15)
		website = VGroup(website_screen, website_text, lock).move_to(screen.get_center())

		computer = VGroup(screen, website, close).scale(1.5).scale(0.9).shift(LEFT*2.5 + DOWN*1.5)

		screen_2 = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close_2 = Dot(radius=0.075, color=RED).move_to(screen_2.get_center() + UP*0.75 + RIGHT*1.25)
		server_text = Text("Script", color=PURE_GREEN, font_size=16).move_to(screen_2.get_center() + UP*0.5)

		server = VGroup(screen_2, close_2, server_text).scale(1.1).shift(RIGHT*3 + DOWN*0.5)
		self.add(computer, server)


		evil_guy = Human(RED, 0.8).human.scale(0.35).move_to(server.get_center() + RIGHT*3)
		self.add(evil_guy)

		you = Human(PURPLE, 0.8).human.scale(0.35).move_to(LEFT*8).move_to(computer.get_center() + LEFT*3)
		self.add(you)

		request = Text("GET /posts?filter=...", font_size=24).move_to(LEFT*2.5 + UP*0.5)
		self.add(request)

		response = Text("title: New Post\nbody: <script>alert(':D');</script>", font_size=14, t2c={"<script>alert(':D');</script>": GOLD}).scale(0.8).move_to(server.get_center())
		self.add(response)

		arrow = Arrow(start=server.get_left(), end=computer.get_right())
		self.add(arrow)

		x = Text("X", font_size=60, color=RED, weight=BOLD).move_to(arrow.get_center()+UP)
		self.add(x)