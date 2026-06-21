from manim import *
import random

from constants import *


config.background_color = "#0d000b"


def make_bundle(class_text, file_name="", buff=0.2, stf=-1):
	file_name = Text(file_name, font_size=20, color=PINK, weight=BOLD)
	class_code = Text(class_text, font_size=16, t2c={
		"// Protected": GRAY,
		"Role": BLUE,
		"typedef": TEAL,
		"struct": TEAL
	})
	code_and_file = VGroup(file_name, class_code).arrange(DOWN)

	class_bg = BackgroundRectangle(
		code_and_file,
		corner_radius=0.2,
		fill_color=PINK,
		stroke_color=PINK,
		stroke_width=2,
		stroke_opacity=1,
		fill_opacity=0.05,
		buff=buff
	)
	if stf != -1:
		class_bg = class_bg.stretch_to_fit_width(stf)

	return VGroup(class_bg, code_and_file)


def make_help_text(text, t2c={}):		
	help_bg = Rectangle(
		width=20, height=0.5,
		fill_color=WHITE,
		fill_opacity=0.2,
		stroke_width=0
	).move_to(DOWN*3.75)
	help_text = Text(text, font_size=18, t2c=t2c).move_to(help_bg.get_center())
	return VGroup(help_bg, help_text)


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


class Polymorphism(Scene):
	def make_bundle(self, class_text):
		class_code = Text(class_text, font_size=16, t2c=T2C)

		class_bg = BackgroundRectangle(
			class_code,
			corner_radius=0.2,
			fill_color=PINK,
			stroke_color=PINK,
			stroke_width=2,
			stroke_opacity=1,
			fill_opacity=0.1,
			buff=0.2
		)

		return VGroup(class_bg, class_code)

	def make_box(self, text, colour, fs=24):
		text = Text(text, font_size=fs)
		rect = BackgroundRectangle(
			text,
			fill_color=colour,
			fill_opacity=0.1,
			stroke_color=colour,
			stroke_width=2,
			stroke_opacity=1,
			buff=0.25
		)
		return VGroup(rect, text)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Polymorphism", gradient=(TEAL, BLUE, PURPLE, PINK))
		self.play(AddTextLetterByLetter(title))
		self.wait(2)

		self.play(title.animate.shift(UP*3))


		definition = Text("Different subtypes under a single interface expressing different behaviour.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		subtypes = VGroup()
		params = [("Subtype 1", ORANGE), ("Subtype 2", PURPLE), ("Subtype 3", GREEN), ("Subtype 4", RED)]
		for param in params:
			subtypes.add(self.make_box(*param))
		subtypes.arrange(DOWN)

		line = Line(start=UP*3, end=DOWN*3)
		interface = self.make_box("Shared Interface\nMany Forms", PINK).scale(1.5)

		poly = VGroup(subtypes, line, interface).arrange(RIGHT).shift(DOWN)
		self.play(Create(poly))
		self.wait(3)
		self.play(FadeOut(poly))


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
		self.wait(10)



class VTables(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("vTables").shift(UP*3)
		self.play(Write(title))


		definition = Text("A struct of function pointers used for dynamic dispatch.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		player_text = """
struct Player {
	Player_vTable *vTable;
	int player_id;
	Role role;
};
"""
		player = make_bundle(player_text, "").move_to(LEFT*5 + UP)
		self.play(Create(player))
		self.wait(2)

		vt_text = """
struct Player_vTable {
	void (*show_summary)(const Player* self);
	Event(*special_ability)(Player* self, Player* target);
};
"""
		vt = make_bundle(vt_text, "").next_to(player, RIGHT, buff=1)		
		self.play(Create(vt))
		self.wait(2)


		activist_text = """
struct Activist {
	Player super;
};
"""
		activist = make_bundle(activist_text, "").next_to(player, DOWN, buff=1)
		arrow_2 = Arrow(start=activist.get_top(), end=player.get_bottom(), tip_length=0.2)
		self.play(Create(arrow_2), Create(activist))
		self.wait(2)


		activist_vt_text = """
static const Player_vTable activist_vTable = {    
    .show_summary = Activist_show_summary,
    .special_ability = Activist_special_ability
};
"""
		activist_vt = make_bundle(activist_vt_text, "").next_to(vt, DOWN, buff=1)
		arrow = Arrow(start=player.get_right(), end=activist_vt.get_left(), tip_length=0.2)
		self.play(Create(arrow), Create(activist_vt))
		self.wait(2)


		call_text = Text("player->vTable->show_summary", color=BLACK, font_size=24)
		white_rect = BackgroundRectangle(
			call_text, buff=0.5, fill_color=WHITE
		)
		call_group = VGroup(white_rect, call_text).move_to(DOWN*3)
		self.play(Create(call_group))
		self.wait(2)


		dot = Dot(radius=0.2, color=GOLD).move_to(player.get_center()+UP*0.2+RIGHT)
		self.play(FadeIn(dot))
		self.play(dot.animate.move_to(activist_vt.get_center()+UP*0.15+RIGHT*0.8))
		self.play(dot.animate.shift(RIGHT*5))
		self.wait(2)



class Static(Scene):
	def make_box(self, text, colour, fs=24):
		text = Text(text, font_size=fs)
		rect = BackgroundRectangle(
			text,
			fill_color=colour,
			fill_opacity=0.1,
			stroke_color=colour,
			stroke_width=2,
			stroke_opacity=1,
			buff=0.25
		)
		return VGroup(rect, text)


	def make_bear(self, number):
		bear = self.make_box("bear_%d" % (number), PURPLE).move_to(DOWN)
		is_alive = self.make_box("is_alive = %d;" % (random.randint(0, 1)), TEAL, fs=18).move_to(LEFT*1.5 + DOWN*3)
		arrow_1 = Arrow(start=bear.get_bottom(), end=is_alive.get_top())
		can_vote = self.make_box("can_vote = %d;" % (random.randint(0, 1)), TEAL, fs=18).move_to(RIGHT*1.5 + DOWN*3)
		arrow_2 = Arrow(start=bear.get_bottom(), end=can_vote.get_top())

		return VGroup(bear, is_alive, can_vote, arrow_1, arrow_2)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Static Storage Duration").shift(UP*3)
		self.play(Write(title))


		definition = Text("Lifetime of the subtype's vTable is the duration of the entire program.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		bear_1 = self.make_bear(1).shift(LEFT*3)
		self.play(Create(bear_1))

		bear_2 = self.make_bear(2).shift(RIGHT*3)
		self.play(Create(bear_2))

		self.wait(2)


		vt = self.make_box("bear_vTable", PINK).move_to(UP)
		arrow_1 = Arrow(start=bear_1.get_top(), end=vt.get_bottom())
		arrow_2 = Arrow(start=bear_2.get_top(), end=vt.get_bottom())
		self.play(Create(arrow_1), Create(arrow_2))
		self.play(Create(vt))

		self.wait(2)


		self.play(FadeOut(bear_1), FadeOut(arrow_1))
		self.wait(2)


		
