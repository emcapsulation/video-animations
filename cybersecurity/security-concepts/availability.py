from manim import *
from entities import *
from introduction import move_to_seat


config.background_color = "#1f001a"


class AvailabilityConversation(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		y_pos = DOWN*0.37
		positions = [RIGHT*5+y_pos, *[LEFT*x+y_pos for x in range(5, -5, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family.set_labels(["You", "Grandpa", "Uncle", "Dad", "Mum", "Brother"])
		family.set_colours([PURPLE, ORANGE, GOLD, GREEN, TEAL, BLUE])

		family_list = family.get_family_list()


		move_to_seat(self, family_list, 2.5, DOWN*0.5, animate=False)
		self.play(FadeIn(family.get_family_group().shift(UP*0.5)))


		mum_line_1 = Text("Don't we have\na backup copy?", font_size=16).move_to(family.get_family_group_member("Mum").get_center() + LEFT*2)
		self.play(Write(mum_line_1))
		self.wait(2)

		self.play(Wiggle(family.get_family_group_member("Uncle")))
		self.wait(2)

		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		text = Text("Data not available!", font_size=14, color=PURE_GREEN)
		computer = VGroup(screen, close)

		self.add(computer)
		self.play(AddTextLetterByLetter(text))

		exclamation = Text("!").move_to(mum_line_1.get_center())
		self.play(Transform(mum_line_1, exclamation))
		self.wait(2)



class AvailabilityMeaning(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Availability", color=PINK).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))
		self.wait(2)


		subtitle = Text("Data can be quickly and reliably accessed whenever it's needed.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		# Failover
		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		computer = VGroup(screen, close).move_to(LEFT*3 + DOWN)
		secret_sauce = SecretSauce("shapes").get_secret_sauce().move_to(computer.get_center()).scale(0.3)
		
		self.play(Create(computer), Create(secret_sauce))


		computer_2 = computer.copy().move_to(RIGHT*3 + DOWN)
		secret_sauce_2 = secret_sauce.copy().move_to(computer_2.get_center())

		self.play(Create(computer_2), Create(secret_sauce_2))


		load = Arc(radius=0.2, start_angle=0,
			angle=9*PI/5, stroke_width=4,
			color=WHITE
		).move_to(computer.get_center() + UP*1.5)

		load_2 = load.copy().move_to(computer_2.get_center() + UP*1.5)

		self.add(load)
		self.play(Rotate(load, angle=2*PI, run_time=2, rate_func=linear))


		x = Text("X", color=RED).move_to(computer.get_center() + UP*1.5)
		text = Text("Data not available!", font_size=14, color=PURE_GREEN).move_to(computer.get_center())
		self.play(Transform(load, x), Transform(secret_sauce, text))


		self.add(load_2)
		self.play(Rotate(load_2, angle=2*PI, run_time=2, rate_func=linear))

		self.play(FadeOut(load), FadeOut(load_2))		


		# Replication
		computer_3 = computer.copy().move_to(RIGHT*2 + DOWN*2.5)
		computer_4 = computer.copy().move_to(RIGHT*5)


		self.play(Transform(secret_sauce, secret_sauce_2.copy().move_to(computer.get_center())))
		self.play(
			computer.animate.shift(LEFT+DOWN), 
			secret_sauce.animate.shift(LEFT+DOWN),
			computer_2.animate.shift(LEFT*4+UP*1.5),
			secret_sauce_2.animate.shift(LEFT*4+UP*1.5)
		)
		self.play(FadeIn(computer_3))
		self.play(FadeIn(computer_4))
		self.wait(2)


		secret_sauce_3 = secret_sauce.copy()
		secret_sauce_4 = secret_sauce.copy()


		self.play(secret_sauce_3.animate.move_to(computer_3.get_center()))
		self.play(secret_sauce_4.animate.move_to(computer_4.get_center()))
		self.wait(5)



class DoS(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		# DoS
		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		computer = VGroup(screen, close).move_to(LEFT*4 + DOWN)
		secret_sauce = SecretSauce("shapes").get_secret_sauce().move_to(computer.get_center()).scale(0.3)
		
		self.play(Create(computer), Create(secret_sauce))


		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(RIGHT*5 + DOWN)
		self.play(FadeIn(evil_guy, direction=DOWN*4))


		request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())
		for i in range(0, 7):
			self.play(request.animate.move_to(computer.get_right()), run_time=1/(i+0.3))
			self.play(FadeOut(request), run_time=1/(i+0.3))

			request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())


		x = Text("X", color=RED).move_to(computer.get_center() + UP*1.5)

		self.play(Indicate(x))


		title = Text("Denial of Service", color=PINK).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))
		self.wait(2)


		subtitle = Text("An attack on availability by overwhelming a system with traffic.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		self.play(FadeOut(x), computer.animate.scale(0.8), secret_sauce.animate.scale(0.8))


		# Load balancer
		computer_2 = computer.copy().shift(UP*2)
		secret_sauce_2 = secret_sauce.copy().move_to(computer_2.get_center())
		computer_3 = computer.copy().shift(DOWN*2)
		secret_sauce_3 = secret_sauce.copy().move_to(computer_3.get_center())


		self.play(FadeIn(computer_2), FadeIn(computer_3), FadeIn(secret_sauce_2), FadeIn(secret_sauce_3))

		load_balancer = Rectangle(
			height=1, width=3, fill_opacity=0.9, color=GRAY
		).move_to(DOWN+RIGHT)
		lb_text = Text("Load Balancer", color=BLACK, font_size=20).move_to(load_balancer.get_center())

		self.play(Create(load_balancer), Create(lb_text))


		request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())
		for i in range(0, 7):
			self.play(request.animate.move_to(load_balancer.get_center()))

			pc = computer
			if i%3 == 1:
				pc = computer_2
			elif i%3 == 2:
				pc = computer_3

			self.play(request.animate.move_to(pc.get_right()))
			self.play(FadeOut(request))

			request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())


		# Rate limiter
		lb_text_2 = Text("Rate Limiter", color=BLACK, font_size=20).move_to(load_balancer.get_center())
		self.play(Transform(lb_text, lb_text_2))


		request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())
		for i in range(0, 7):
			self.play(request.animate.move_to(load_balancer.get_center()), run_time=1/(i+0.3))

			if i == 6:
				self.play(Indicate(load_balancer, color=RED), FadeOut(request))
				x = Text("X", color=RED).move_to(evil_guy.get_center() + UP*1.5)
				self.play(SpinInFromNothing(x))
			else:
				self.play(request.animate.move_to(computer.get_right()), run_time=1/(i+0.3))
				self.play(FadeOut(request), run_time=1/(i+0.3))

			request = Text("GET /secret_sauce", font_size=16, color=WHITE).move_to(evil_guy.get_left())

		
		self.wait(1)
		self.play(FadeOut(evil_guy), FadeOut(x))

		self.wait(5)




class AvailabilityConversation2(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		y_pos = DOWN*0.37
		positions = [RIGHT*5+y_pos, *[LEFT*x+y_pos for x in range(5, -5, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family.set_labels(["You", "Grandpa", "Uncle", "Dad", "Mum", "Brother"])
		family.set_colours([PURPLE, ORANGE, GOLD, GREEN, TEAL, BLUE])

		family_list = family.get_family_list()


		move_to_seat(self, family_list, 2.5, DOWN*0.5, animate=False)
		self.play(FadeIn(family.get_family_group().shift(UP*0.5)))


		def make_pen():
			pen_body = Rectangle(
				width=1.5, height=0.25,
				color=BLUE,
				fill_opacity=0.5
			)
			nib = Triangle(
				color=WHITE,
				fill_opacity=0.5
			).scale(0.15)
			nib.rotate(5*PI/6, about_point=nib.get_center()).move_to(pen_body.get_right() + RIGHT*0.15)
			pen = VGroup(pen_body, nib)

			return pen

		pen = make_pen().scale(0.4).next_to(family.get_family_group_member("Grandpa").get_center() + RIGHT*0.5)

		self.play(Wiggle(family.get_family_group_member("Grandpa")))
		self.play(FadeIn(pen))
		self.wait(2)

		self.play(Wiggle(family.get_family_group_member("Brother")))
		self.wait(2)



class MaintenanceMonitoring(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Availability", color=PINK).move_to(UP*3)
		self.add(title)


		subtitle = Text("Data can be quickly and reliably accessed whenever it's needed.", font_size=20).next_to(title, DOWN)
		self.add(subtitle)
		self.wait(1)


		maintenance = Text("Maintenance", font_size=24)
		self.add(maintenance)
		self.wait(1)

		monitoring = Text("Monitoring", font_size=24).next_to(maintenance, DOWN)
		self.add(monitoring)
		self.wait(1)

		dr = Text("Disaster Recovery", font_size=24).next_to(monitoring, DOWN)
		self.add(dr)
		self.wait(1)