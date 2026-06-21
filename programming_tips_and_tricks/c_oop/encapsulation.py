from manim import *
from uml import *

from constants import *


config.background_color = "#000f0e"


T2C = {
	"// Member variables": GRAY,
	"// Constructor - initialises a new instance": GRAY,
	"// Methods": GRAY,
	"getArea": GREEN,
	"setWidth": GREEN,
	"this": GOLD,
	"int": PURPLE,
	"void": PURPLE,
	"class": TEAL,
	"Rectangle": TEAL,
	"private": MAROON,
	"public": MAROON
}


class Encapsulation(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Encapsulation", gradient=(TEAL, BLUE, PURPLE, PINK))
		self.play(AddTextLetterByLetter(title))
		self.wait(2)

		self.play(title.animate.shift(UP*3))


		definition = Text("Enclosing data together with functions which operate on it in a single bundle.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		smol_bundle = RoundedRectangle(
			corner_radius=0.2,
			height=3, width=5,
			fill_color=TEAL,
			stroke_color=TEAL,
			fill_opacity=0.1
		).shift(DOWN)

		line = Line(start=LEFT*2.5, end=RIGHT*2.5, stroke_color=TEAL).move_to(smol_bundle.get_center()+UP*0.5)
		object_text = Text("Object", font_size=28, weight=BOLD).move_to(smol_bundle.get_center() + UP)
		title_bundle = VGroup(object_text, line)
		
		data_circle = RoundedRectangle(
			corner_radius=0.2,
			height=1, width=3,
			fill_color=ORANGE,
			stroke_color=ORANGE,
			fill_opacity=0.2
		).move_to(smol_bundle.get_center() + LEFT)
		data_text = Text("Data", font_size=26).move_to(data_circle.get_center())
		data_bundle = VGroup(data_circle, data_text)

		method_circle = RoundedRectangle(
			corner_radius=0.2,
			height=1, width=3,
			fill_color=GREEN,
			stroke_color=GREEN,
			fill_opacity=0.2
		).move_to(smol_bundle.get_center() + DOWN + RIGHT)
		method_text = Text("Functions", font_size=26).move_to(method_circle.get_center())
		method_bundle = VGroup(method_circle, method_text)

		object_bundle = VGroup(smol_bundle, title_bundle, data_bundle, method_bundle)
		self.play(GrowFromEdge(object_bundle, UP))
		self.wait(3)



		bundle = RoundedRectangle(
			corner_radius=0.2,
			height=5, width=8,
			fill_color=TEAL,
			stroke_color=TEAL,
			fill_opacity=0.1
		).shift(DOWN)


		code_text = """
class Rectangle {
	// Member variables
	int width;
	int height;

	// Constructor - initialises a new instance
	Rectangle(int width, int height) {
		this.width = width;
		this.height = height;
	}

	// Methods
	int getArea() {
		return this.width*this.height;
	}

	void setWidth(int width) {
		if (width > 0) {
			this.width = width;
		}
	}
}
		"""

		code = Text(code_text, font_size=16, t2c=T2C).move_to(bundle.get_center())
		class_bundle = VGroup(bundle, code)

		self.play(ReplacementTransform(object_bundle, class_bundle))
		self.wait(3)


		state_brace = BraceBetweenPoints(
			point_1=UP*1.2,
			point_2=UP*0.5,
			direction=LEFT
		).shift(LEFT*4)
		state_text = Text("State", font_size=24, color=ORANGE).next_to(state_brace, LEFT, buff=1)
		state = VGroup(state_brace, state_text)
		self.play(Create(state))
		self.wait(2)


		method_brace = BraceBetweenPoints(
			point_1=DOWN*1,
			point_2=DOWN*3.2,
			direction=LEFT
		).shift(LEFT*4)
		method_text = Text("Methods", font_size=24, color=GREEN).next_to(method_brace, LEFT, buff=1)
		methods = VGroup(method_brace, method_text)
		self.play(Create(methods))
		self.wait(2)


		code_text_2 = """
public class Rectangle {
	// Member variables
	private int width;
	private int height;

	// Constructor - initialises a new instance
	public Rectangle(int width, int height) {
		this.width = width;
		this.height = height;
	}

	// Methods
	public int getArea() {
		return this.width*this.height;
	}

	public void setWidth(int width) {
		if (width > 0) {
			this.width = width;
		}
	}
}
		"""

		code_2 = Text(code_text_2, font_size=16, t2c=T2C).move_to(class_bundle[1].get_center())
		self.play(ReplacementTransform(class_bundle[1], code_2))
		self.wait(3)




class GameClass(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		attributes = [
			"- num_players : int",
			"- num_bears_left : int",
			"- num_townspeople_left : int",
			"- is_night : int",
			"- player_bitten_ids : int[2]",
			"- bites_this_round : int",
			"- player_healed_id : int",
			"- players : Player**"
		]

		methods = [
			"+ Game_ctor(num_players : int) : Game*",
			"+ Game_loop(self : Game*) : void",
			"+ Game_dtor(self : Game*) : void"
		]

		uml = Uml("Game", attributes, methods)

		self.play(Create(uml.get_box()), Create(uml.get_class_name()))
		self.wait(2)

		attributes = uml.get_attributes()[0]
		for i in range(0, len(attributes)):
			if i == 4 or i == 7:
				self.wait(2)
			self.play(FadeIn(attributes[i]))
		self.play(Create(uml.get_attributes()[1]))
		self.wait(2)


		question = Text("Does main really need to access this internal state?", color=BLACK, font_size=20, t2c={'main': TEAL})
		surround = BackgroundRectangle(question, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		question_group = VGroup(surround, question)
		self.play(FadeIn(question_group))
		self.wait(2)


		x = Text("X", color=RED, font_size=50)
		self.play(SpinInFromNothing(x))
		self.wait(2)
		self.play(FadeOut(question_group), FadeOut(x))


		methods = uml.get_methods()
		for i in range(0, len(methods)):
			self.play(FadeIn(methods[i]))
			self.wait(2)
		self.wait(2)




class DataHiding(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Data Hiding").move_to(UP*3)
		self.play(AddTextLetterByLetter(title))

		definition = Text("Restricting outside access to object internals.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


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
		object_text = Text("Game", font_size=32, weight=BOLD).move_to(smol_bundle.get_center() + UP*(HEIGHT/3))
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


		self.play(GrowFromEdge(object_bundle, UP))
		self.wait(2)

		main_text = Text("Main", color=BLACK).move_to(LEFT*5)
		mr = BackgroundRectangle(main_text, fill_color=WHITE, fill_opacity=1, buff=0.2, corner_radius=0.2)
		main = VGroup(mr, main_text)

		self.play(main.animate.move_to(object_bundle[2].get_left()))
		self.play(object_bundle[0].animate.set_stroke_color(RED))
		self.play(main.animate.move_to(LEFT*5))
		self.wait(2)

		self.play(object_bundle[0].animate.set_stroke_color(TEAL))
		self.play(Create(pp))
		self.play(main.animate.move_to(object_bundle[3].get_left()))
		self.play(main.animate.move_to(LEFT*5))
		self.wait(2)




class Structs(Scene):
	def create_struct_memory(self, title, struct_members):
		title = Text(title, font_size=24, weight=BOLD)
		struct = VGroup()
		for member in struct_members:
			rect = Rectangle(
				width=4, height=member['size']//2,
				fill_color=member['colour'],
				stroke_color=member['colour'],
				fill_opacity=0.2
			)
			rect_text = Text(member['type'] + '\n' + member['name'], font_size=24).move_to(rect.get_center()).align_to(rect, LEFT).shift(RIGHT*0.1)
			rectangle = VGroup(rect, rect_text)
			struct.add(rectangle)

		return VGroup(title, struct.arrange(DOWN, buff=0)).arrange(DOWN)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Structs").move_to(UP*3)
		self.play(AddTextLetterByLetter(title))

		definition = Text("Grouping a set of variables into a single type.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		struct_text = """
struct Game {
	int num_players;
	int is_night;
	int bitten_ids[2];
	Player** players;
};
"""
		st = Text(struct_text, font_size=20).move_to(LEFT*3 + DOWN)
		self.play(Write(st))
		self.wait(2)


		struct_dict = [
			{
				"size": 4,
				"colour": BLUE,
				"name": "num_players",
				"type": "int"
			},
			{
				"size": 4,
				"colour": BLUE,
				"name": "is_night",
				"type": "int"
			},
			{
				"size": 8,
				"colour": TEAL,
				"name": "bitten_ids",
				"type": "int[2]"
			},
			{
				"size": 8,
				"colour": PINK,
				"name": "players",
				"type": "Player**"
			}
		]

		struct = self.create_struct_memory("Game", struct_dict).scale(0.4).shift(RIGHT*3 + DOWN)
		self.play(Create(struct))
		self.wait(2)


		brace = BraceBetweenPoints(struct[1].get_top(), struct[1].get_bottom(), direction=LEFT).shift(LEFT*0.75)
		self.play(GrowFromCenter(brace))

		cont = Text("Contiguous\nMemory", color=TEAL, font_size=24).next_to(brace, LEFT)
		self.play(Write(cont))
		self.wait(2)



class ClassFiles(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		header_box = Rectangle(
			height=6.5, width=6,
			fill_opacity=0.1
		)
		header_text = Text("game.h", color=TEAL).move_to(header_box.get_top()+DOWN*0.5)
		header_inner = Text("Public functions / member variables", font_size=20, t2c={"Public": GREEN}).next_to(header_text, DOWN)

		header_method_text = """
Game *Game_ctor(int num_players);
void Game_loop(Game* self);
void Game_dtor(Game* self);
		"""
		header_methods = Text(header_method_text, font_size=16).next_to(header_inner, DOWN)
		header_file = VGroup(header_box, header_text, header_inner, header_methods)

		self.play(Create(header_file[0]), Write(header_file[1]))
		self.wait(2)		

		self.play(FadeIn(header_file[2], shift=UP))
		self.wait(2)


		c_box = Rectangle(
			height=6.5, width=6,
			fill_opacity=0.1
		)
		c_text = Text("game.c", color=TEAL).move_to(c_box.get_top()+DOWN*0.5)
		c_inner = Text("Private definitions + implementations", font_size=20, t2c={"Private": RED}).next_to(c_text, DOWN)

		c_method_text = """
Game *Game_ctor(int num_players) {
	// TODO
}
void Game_loop(Game* self) {
	// TODO
}
void Game_dtor(Game* self) {
	// TODO
}
		"""
		c_methods = Text(c_method_text, font_size=16, t2c={"// TODO": GRAY}).next_to(c_inner, DOWN)
		c_file = VGroup(c_box, c_text, c_inner, c_methods).shift(RIGHT*3.5)


		NEW_POS = LEFT*3.5
		self.play(
			header_file[0].animate.shift(NEW_POS), 
			header_file[1].animate.shift(NEW_POS), 
			header_file[2].animate.shift(NEW_POS)
		)
		self.play(Create(c_file[0]), Write(c_file[1]))
		self.wait(2)

		self.play(FadeIn(c_file[2], shift=UP))
		self.wait(2)


		# Public methods
		self.play(Write(header_file[3].shift(NEW_POS)))
		self.play(Write(c_file[3]))
		self.wait(2)


		question = Text("Private data (data hiding) can be emulated using opaque types.", color=BLACK, font_size=20, t2c={'Private': RED, 'opaque types': PURPLE})
		surround = BackgroundRectangle(question, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		question_group = VGroup(surround, question)
		self.play(FadeIn(question_group))
		self.wait(2)
		self.play(FadeOut(question_group))
		self.wait(2)


		opaque = Text("typedef struct Game Game;", color=TEAL, weight=BOLD, font_size=16).next_to(header_inner, DOWN, buff=0.5)
		self.play(header_methods.animate.shift(DOWN*1))
		self.play(Write(opaque))
		self.wait(2)


		struct_text = """
struct Game {
	int num_players;
	int num_bears_left;
	...
	Player** players;	
};
		"""
		struct_def = Text(struct_text, font_size=16, weight=BOLD, t2c={"Game": TEAL, "typedef struct": TEAL}).next_to(c_inner, DOWN, buff=0.5)
		self.play(c_methods.animate.shift(DOWN*2.5))
		self.play(Write(struct_def))
		self.wait(2)



class StaticTip(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		hint = Text("Tip: Mark private methods static to give them internal linkage.", color=BLACK, font_size=20, t2c={'Tip:': TEAL, 'private': RED, 'static': PURPLE})
		surround = BackgroundRectangle(hint, buff=0.5, stroke_width=0, color=WHITE, fill_opacity=1, corner_radius=0.2)
		hint_group = VGroup(surround, hint)
		self.play(FadeIn(hint_group))
		self.wait(5)
		self.play(FadeOut(hint_group))
		self.wait(2)