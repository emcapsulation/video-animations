from manim import *
from uml import *

from constants import *
from props import Human


config.background_color = "#000e12"


T2C = {
	"// Abstract - concrete impls. must implement": GRAY,
	"// Use parent constructor": GRAY,
	"// Concrete implementation": GRAY,
	"getArea": GREEN,
	"setWidth": GREEN,
	"this": GOLD,
	"int": PURPLE,
	"void": PURPLE,
	"class": TEAL,
	"Quadrilateral": TEAL,
	"Rectangle": TEAL,
	"Square": TEAL,
	"private": MAROON,
	"public": MAROON,
	"protected": MAROON,
	"@Override": YELLOW
}


class Abstraction(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Abstraction", gradient=(TEAL, BLUE, PURPLE, PINK))
		self.play(AddTextLetterByLetter(title))
		self.wait(2)

		self.play(title.animate.shift(UP*3))


		definition = Text("Hiding implementation complexity; exposing only what's necessary for use.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		player = Human(BLUE).add_label("Player").get_human().scale(0.5).move_to(LEFT*4 + DOWN)
		self.play(Create(player))
		self.wait(1)

		x = Text("X", color=RED, font_size=70).move_to(player.get_center())
		self.play(SpinInFromNothing(x))
		self.wait(1)

		list_1 = Text("is_alive = 0;", font_size=20)
		healer_text = """
if (player->role == HEALER)
  Healer_attempt_self_heal(player);
		"""
		list_2 = Text(healer_text, font_size=20)
		list_tasks = VGroup(list_1, list_2).arrange(DOWN).move_to(DOWN)
		self.play(FadeIn(list_1, shift=UP))
		self.wait(1)
		self.play(FadeIn(list_2, shift=UP))
		self.wait(3)


		real = Text("Player_eliminate(player);", font_size=20).move_to(list_tasks.get_center())
		self.play(Transform(list_tasks, real))
		self.wait(2)


		simple = Text("Simple Interface", font_size=20)
		box = BackgroundRectangle(simple, fill_color=BLUE, buff=0.5, fill_opacity=0.1, corner_radius=0.2)
		interface = VGroup(box, simple).move_to(list_tasks.get_center())
		self.play(Transform(list_tasks, interface), FadeOut(x))


		game = Text("Game").move_to(RIGHT*4 + DOWN)
		arrow = Arrow(start=game.get_left(), end=interface.get_right())
		arrow_2 = Arrow(start=interface.get_left(), end=player.get_right())
		self.play(Write(game))
		self.play(Create(arrow))
		self.play(Create(arrow_2))
		self.wait(2)



class AbstractClass(Scene):
	def make_bundle(self, class_text):
		class_code = Text(class_text, font_size=16, t2c=T2C)

		class_bg = BackgroundRectangle(
			class_code,
			corner_radius=0.2,
			fill_color=BLUE,
			stroke_color=BLUE,
			stroke_width=2,
			stroke_opacity=1,
			fill_opacity=0.1,
			buff=0.2
		)

		return VGroup(class_bg, class_code)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Abstract Classes").shift(UP*3)
		self.play(Write(title))
		self.wait(2)

		definition = Text("Reveal the interface but cannot be instantiated directly.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		code_text = """
public abstract class Quadrilateral {
	protected int width;
	protected int height;

	protected Quadrilateral(int width, int height) {
		this.width = width;
		this.height = height;
	}

	// Abstract - concrete impls. must implement
	public abstract int getArea();

	public void setWidth(int width) {
		if (width > 0) {
			this.width = width;
		}
	}
}
		"""
		class_bundle = self.make_bundle(code_text).move_to(DOWN)

		self.play(Create(class_bundle))
		self.wait(3)
		self.play(class_bundle.animate.scale(0.6).shift(LEFT*4))


		rectangle_text = """
public class Rectangle extends Quadrilateral {
	public Rectangle(int width, int height) {
		// Use parent constructor
		super(width, height);
	}

	// Concrete implementation
	public int getArea() {
		return this.width*this.height;
	}
}
		"""
		rectangle_bundle = self.make_bundle(rectangle_text).move_to(RIGHT*3)

		self.play(Create(rectangle_bundle))
		self.wait(3)
		self.play(rectangle_bundle.animate.scale(0.6).shift(UP))


		square_text = """
public class Square extends Quadrilateral {
	public Square(int width) {
		super(width, width);
	}

	public int getArea() {
		return this.width*this.width;
	}

	@Override
	public void setWidth(int width) {
		super.setWidth(width);
		this.height = width;
	}
}
		"""
		square_bundle = self.make_bundle(square_text).move_to(RIGHT*3 + DOWN*2)

		self.play(Create(square_bundle))
		self.wait(3)
		self.play(square_bundle.animate.scale(0.6).shift(DOWN*0.5))
		self.wait(2)



class PlayerClass(Scene):

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		attributes = [
			"+ player_id : int",
			"+ role : Role",
			"# is_alive : int",
			"# is_bitten : int",
			"# can_vote : int"
		]

		methods = [
			"+ Player_reset() : void",
			"+ Player_is_alive() : int",
			"...",
			"# Player_init(player_id : int, ...) : void"
		]

		uml = Uml("Player", attributes, methods)

		self.play(Create(uml.get_box()), Create(uml.get_class_name()))
		self.wait(2)

		attributes = uml.get_attributes()[0]
		for i in range(0, len(attributes)):
			self.play(FadeIn(attributes[i]))
		self.play(Create(uml.get_attributes()[1]))
		self.wait(2)

		methods = uml.get_methods()
		for i in range(0, len(methods)):
			self.play(FadeIn(methods[i]))
			self.wait(2)
		self.wait(2)



class PImplIdiom(Scene):
	def make_bundle(self, class_text, file_name):
		file_name = Text(file_name, font_size=20, color=BLUE)
		class_code = Text(class_text, font_size=16, t2c={
			"// Protected": GRAY,
			"int": PURPLE,
			"Role": PURPLE,
			"Player": TEAL,
			"_protected": TEAL
		})
		code_and_file = VGroup(file_name, class_code).arrange(DOWN)

		class_bg = BackgroundRectangle(
			code_and_file,
			corner_radius=0.2,
			fill_color=BLUE,
			stroke_color=BLUE,
			stroke_width=2,
			stroke_opacity=1,
			fill_opacity=0.1,
			buff=0.2
		)

		return VGroup(class_bg, code_and_file)


	def make_help_text(self, text, t2c):		
		help_bg = Rectangle(
			width=20, height=1,
			fill_color=WHITE,
			fill_opacity=0.2,
			stroke_width=0
		).move_to(DOWN*3.5)
		help_text = Text(text, font_size=20, t2c=t2c).move_to(help_bg.get_center())
		return VGroup(help_bg, help_text)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("PImpl Idiom").shift(UP*3)
		self.play(Write(title))
		self.wait(2)

		definition = Text("Pointer to an implementation.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		struct_text = """
typedef struct Player {
	int player_id;
	Role role;

	// Protected
	int is_alive;
	int is_bitten;
	int can_vote;
} Player;
		"""
		struct_bundle = self.make_bundle(struct_text, "player.h")

		self.play(Create(struct_bundle))
		self.wait(3)


		struct_text_2 = """
typedef struct Player_protected Player_protected;

typedef struct Player {
	int player_id;
	Role role;
	Player_protected *protected;
} Player;
		"""

		struct_bundle_2 = self.make_bundle(struct_text_2, "player.h")

		self.play(Transform(struct_bundle, struct_bundle_2))
		self.wait(3)


		text = "Opaque Pointer: A pointer to an opaque type / forward-declared\nstruct whose internal structure is hidden."
		help_text = self.make_help_text(text, {"Opaque Pointer:": BLUE})
		self.play(FadeIn(help_text))
		self.wait(3)


		struct_text_2 = """
struct Player_protected {
	int is_alive;
	int is_bitten;
	int can_vote;
};
		"""

		struct_bundle_3 = self.make_bundle(struct_text_2, "another file").scale(0.8).move_to(DOWN*1.5)

		self.play(struct_bundle.animate.scale(0.8).shift(UP*0.5))
		self.play(Create(struct_bundle_3))
		self.wait(3)


		text = "In which file do we put the Player_protected struct?"
		help_text_2 = self.make_help_text(text, {"Player_protected": BLUE})
		self.play(Transform(help_text, help_text_2))
		self.wait(3)


		struct_bundle_4 = self.make_bundle(struct_text_2, "player.c").scale(0.8).move_to(DOWN*1.5)
		self.play(Transform(struct_bundle_3, struct_bundle_4))
		self.wait(2)


		text = "Child subtypes in other files cannot access Player_protected members."
		help_text_2 = self.make_help_text(text, {"Player_protected": BLUE})
		self.play(Transform(help_text, help_text_2))
		self.wait(2)


		x = Text("X", color=RED, font_size=100)
		self.play(SpinInFromNothing(x))
		self.wait(2)


		text = "Add to a new header file to be included by child subtype .c files."
		help_text_2 = self.make_help_text(text, {})
		self.play(FadeOut(x))
		self.play(Transform(help_text, help_text_2))
		self.wait(2)


		struct_bundle_4 = self.make_bundle(struct_text_2, "player_protected.h").scale(0.8).move_to(DOWN*1.5)
		self.play(Transform(struct_bundle_3, struct_bundle_4))
		self.wait(2)
