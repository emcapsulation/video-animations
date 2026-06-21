from manim import *

from constants import *
from props import *

from room import Room


config.background_color = DEFAULT_BACKGROUND


class Interview(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		# Create the room
		room = Room()
		interview_room = Room().get_room()
		self.play(Create(interview_room))

		interviewer = Human(TEAL).add_label("Interviewer").get_human().scale(0.5).move_to(RIGHT*5.5+DOWN*2)
		candidate = Human(BLUE).add_label("Candidate").get_human().scale(0.5).move_to(LEFT*1.5+DOWN*2)
		self.play(Create(interviewer), Create(candidate))

		self.wait(2)


		def write_speech_bubble(text, colour, speaker):
			t = Text(text, font_size=24, weight=BOLD).move_to(room.get_roof().get_center())
			self.play(room.get_roof().animate.set_stroke_color(colour), room.get_roof().animate.set_fill_color(colour), FadeIn(t), Wiggle(speaker))
			return t

		t = write_speech_bubble(
			"Welcome to your C interview!",
			TEAL,
			interviewer
		)
		self.wait(1)
		self.play(FadeOut(t))

		t = write_speech_bubble(
			"Your first question is...",
			TEAL,
			interviewer
		)
		self.wait(1)
		self.play(FadeOut(t))

		t = write_speech_bubble(
			"What is the difference between C and C++?",
			TEAL,
			interviewer
		)
		self.wait(2)
		self.play(FadeOut(t))


		t = write_speech_bubble(
			"Uhh... You can do OOP in C++ but not in C?",
			BLUE,
			candidate
		)
		self.wait(2)
		self.play(FadeOut(t))


		t = write_speech_bubble(
			"You have failed the interview!! >:(",
			TEAL,
			interviewer
		)
		self.wait(10)

		self.play(*[FadeOut(mob) for mob in self.mobjects])



class FourPillars(Scene):
	WIDTH, HEIGHT = 16, 9
	OPACITY = 0.9

	def make_encapsulation(self):
		background = Rectangle(
			width=FourPillars.WIDTH, height=FourPillars.HEIGHT, 
			fill_color="#000f0e", stroke_color="#000f0e",
			fill_opacity=FourPillars.OPACITY)
		title = Text("Encapsulation", color=TEAL).move_to(UP*3)


		# Class
		HEIGHT, WIDTH = 4, 6.5
		smol_bundle = RoundedRectangle(
			corner_radius=0.2,
			height=HEIGHT, width=WIDTH,
			fill_color=TEAL,
			stroke_color=TEAL,
			fill_opacity=0.1
		).shift(DOWN)

		line = Line(start=LEFT*(WIDTH/2), end=RIGHT*(WIDTH/2), stroke_color=TEAL).move_to(smol_bundle.get_center()+UP*(HEIGHT/6))
		object_text = Text("Object", font_size=32, weight=BOLD).move_to(smol_bundle.get_center() + UP*(HEIGHT/3))
		title_bundle = VGroup(object_text, line)
		
		data_circle = RoundedRectangle(
			corner_radius=0.2,
			height=(HEIGHT/3), width=(0.6*WIDTH),
			fill_color=ORANGE,
			stroke_color=ORANGE,
			fill_opacity=0.2
		).move_to(smol_bundle.get_center() + LEFT)
		data_text = Text("Data", font_size=28).move_to(data_circle.get_center())
		data_bundle = VGroup(data_circle, data_text)

		method_circle = RoundedRectangle(
			corner_radius=0.2,
			height=(HEIGHT/3), width=(0.6*WIDTH),
			fill_color=GREEN,
			stroke_color=GREEN,
			fill_opacity=0.2
		).move_to(smol_bundle.get_center() + DOWN*(HEIGHT/3) + RIGHT)
		method_text = Text("Functions", font_size=28).move_to(method_circle.get_center())
		method_bundle = VGroup(method_circle, method_text)

		object_bundle = VGroup(smol_bundle, title_bundle, data_bundle, method_bundle)


		# Visibility
		public = Text("Public", font_size=24, weight=BOLD, color=GREEN).next_to(object_bundle[3], RIGHT).shift(RIGHT*0.5)
		private = Text("Private", font_size=24, weight=BOLD, color=RED).next_to(object_bundle[2], LEFT).shift(LEFT*0.5)
		pp = VGroup(public, private)


		return VGroup(background, title, object_bundle, pp)



	def make_abstraction(self):
		background = Rectangle(
			width=FourPillars.WIDTH, height=FourPillars.HEIGHT, 
			fill_color="#000e12", stroke_color="#000e12",
			fill_opacity=FourPillars.OPACITY)
		title = Text("Abstraction", color=BLUE).move_to(UP*3)


		player = Human(BLUE).add_label("").get_human().scale(0.5)

		simple = Text("Simple\nInterface", font_size=20)
		box = BackgroundRectangle(simple, fill_color=BLUE, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
		interface = VGroup(box, simple).scale(1.5)

		game = Text("Object")

		complexity = Text("Complex\nInternals", font_size=20)
		box_2 = BackgroundRectangle(complexity, fill_color=MAROON, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
		complex_internals = VGroup(box_2, complexity).scale(1.5)
		object_ = VGroup(game, complex_internals).arrange(DOWN)

		line = Line(start=UP*2, end=DOWN*2)
		arrow = Arrow(start=interface.get_left(), end=player.get_right())

		api = VGroup(object_, line, interface, arrow, player).arrange(RIGHT).shift(DOWN)

		return VGroup(background, title, api)



	def make_inheritance(self):
		background = Rectangle(
			width=FourPillars.WIDTH, height=FourPillars.HEIGHT, 
			fill_color="#0b0012", stroke_color="#0b0012",
			fill_opacity=FourPillars.OPACITY)
		title = Text("Inheritance", color=PURPLE).move_to(UP*3)


		def make_box(title, text):
			title = Text(title, font_size=20, weight=BOLD)
			text = Text(text, font_size=18)
			middle = VGroup(title, text).arrange(DOWN)
			box = BackgroundRectangle(middle, fill_color=PURPLE, stroke_color=PURPLE, stroke_opacity=1, stroke_width=4, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
			return VGroup(box, middle).scale(1.1)

		parent = make_box("Parent Type", "Common Properties\nShared Interface").shift(UP*0.5)
		child = make_box("Child Subtype", "Overrides\nExtensions").move_to(DOWN*2.5 + LEFT*3)
		child_2 = make_box("Child Subtype 2", "Overrides\nExtensions").move_to(DOWN*2.5 + RIGHT*3)

		arrow = Arrow(start=parent.get_bottom(), end=child.get_top())
		arrow_2 = Arrow(start=parent.get_bottom(), end=child_2.get_top())

		return VGroup(background, title, parent, VGroup(child, arrow, child_2, arrow_2))



	def make_polymorphism(self):
		background = Rectangle(
			width=FourPillars.WIDTH, height=FourPillars.HEIGHT, 
			fill_color="#0d000b", stroke_color="#0d000b",
			fill_opacity=FourPillars.OPACITY)
		title = Text("Polymorphism", color=PINK).move_to(UP*3)

		def make_box(title, colour):
			title = Text(title, font_size=20)
			box = BackgroundRectangle(title, fill_color=colour, stroke_color=colour, stroke_opacity=1, stroke_width=2, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
			return VGroup(box, title).scale(1.1)

		subtypes = VGroup()
		params = [("Subtype 1", ORANGE), ("Subtype 2", PURPLE), ("Subtype 3", GREEN), ("Subtype 4", RED)]
		for param in params:
			subtypes.add(make_box(*param))
		subtypes.arrange(DOWN)

		line = Line(start=UP*3, end=DOWN*3)
		interface = make_box("Shared Interface\nMany Forms", PINK).scale(1.5)

		return VGroup(background, title, VGroup(subtypes, line, interface).arrange(RIGHT).shift(DOWN))




	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text('"You can\'t do object-oriented programming in C"', font_size=24).move_to(UP*3)
		self.play(Write(title))
		self.wait(5)


		encapsulation = self.make_encapsulation().scale(0.8)
		self.play(GrowFromCenter(encapsulation[0]))
		self.play(AddTextLetterByLetter(encapsulation[1]))
		self.play(GrowFromEdge(encapsulation[2], UP))
		self.play(Create(encapsulation[3]))

		self.play(encapsulation.animate.scale(0.4).move_to(LEFT*3 + UP))
		self.wait(2)


		abstraction = self.make_abstraction().scale(0.8)

		self.play(GrowFromCenter(abstraction[0]))
		self.play(AddTextLetterByLetter(abstraction[1]))
		self.play(Create(abstraction[2]))

		self.play(abstraction.animate.scale(0.4).move_to(RIGHT*3 + UP))
		self.wait(2)


		inheritance = self.make_inheritance().scale(0.8)

		self.play(GrowFromCenter(inheritance[0]))
		self.play(AddTextLetterByLetter(inheritance[1]))
		self.play(Create(inheritance[2]))
		self.play(GrowFromEdge(inheritance[3], UP))

		self.play(inheritance.animate.scale(0.4).move_to(LEFT*3 + DOWN*2.5))
		self.wait(2)


		polymorphism = self.make_polymorphism().scale(0.8)

		self.play(GrowFromCenter(polymorphism[0]))
		self.play(AddTextLetterByLetter(polymorphism[1]))
		self.play(Create(polymorphism[2]))

		self.play(polymorphism.animate.scale(0.4).move_to(RIGHT*3 + DOWN*2.5))
		self.wait(2)



class Limitations(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Evaluation", gradient=(TEAL, BLUE, PURPLE, PINK))
		self.play(AddTextLetterByLetter(title))
		self.wait(5)



class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Object-Oriented Programming in C").move_to(UP*3)
		self.add(title)
		subtitle = Text("Encapsulation, Abstraction, Inheritance, Polymorphism", font_size=24, t2c={"Encapsulation": TEAL, "Abstraction": BLUE, "Inheritance": PURPLE, "Polymorphism": PINK})
		self.add(subtitle.next_to(title, DOWN))

		player = Human(BLUE).add_label("").get_human().scale(0.5)

		def make_box(title, colour):
			title = Text(title, font_size=20)
			box = BackgroundRectangle(title, fill_color=colour, stroke_color=colour, stroke_opacity=1, stroke_width=2, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
			return VGroup(box, title).scale(1.1)

		subtypes = VGroup()
		params = [("Subtype 1", LIGHT_PINK), ("Subtype 2", PURPLE), ("Subtype 3", BLUE), ("Subtype 4", PINK)]
		for param in params:
			subtypes.add(make_box(*param))
		subtypes.scale(0.8).arrange(DOWN)

		simple = Text("Simple\nInterface", font_size=20)
		box = BackgroundRectangle(simple, fill_color=BLUE, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
		interface = VGroup(box, simple).scale(1.5)

		line = Line(start=UP*2, end=DOWN*2)
		arrow = Arrow(start=interface.get_right(), end=player.get_left())

		api = VGroup(subtypes, line, interface, arrow, player).arrange(RIGHT).shift(DOWN)
		self.add(api)