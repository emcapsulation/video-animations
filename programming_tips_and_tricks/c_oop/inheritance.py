from manim import *
from uml import *

from constants import *


config.background_color = "#0b0012"


def make_bundle(class_text, file_name, buff=0.2, stf=-1):
	file_name = Text(file_name, font_size=20, color=PURPLE, weight=BOLD)
	class_code = Text(class_text, font_size=16, t2c={
		"// Protected": GRAY,
		"// Public": GRAY,
		"Role": BLUE,
		"typedef": TEAL,
		"struct": TEAL
	})
	code_and_file = VGroup(file_name, class_code).arrange(DOWN)

	class_bg = BackgroundRectangle(
		code_and_file,
		corner_radius=0.2,
		fill_color=PURPLE,
		stroke_color=PURPLE,
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



class Inheritance(Scene):
	def make_class(self, text):		
		text = Text(text, font_size=24)
		class_bg = BackgroundRectangle(
			text,
			fill_color=WHITE,
			fill_opacity=0.3,
			stroke_color=PURPLE,
			stroke_width=4,
			stroke_opacity=1,
			buff=0.25
		)
		return VGroup(class_bg, text)


	def connect(self, a, b):
		arrow = Arrow(
			start=b.get_center(), 
			end=a.get_center(), 
			buff=1.0, 
			tip_length=0.2, 
			stroke_width=3
		)
		return arrow


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Inheritance", gradient=(TEAL, BLUE, PURPLE, PINK))
		self.play(AddTextLetterByLetter(title))
		self.wait(2)

		self.play(title.animate.shift(UP*3))


		definition = Text("Subclasses building upon each other and inheriting from parent classes.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


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

		inh = VGroup(parent, VGroup(child, arrow, child_2, arrow_2))
		self.play(Create(inh))
		self.wait(3)


		self.play(FadeOut(inh))
		shape = self.make_class("Shape").move_to(UP*1.5)
		self.play(Create(shape))


		polygon = self.make_class("Polygon").move_to(LEFT*3)
		arrow = self.connect(shape, polygon)

		ellipse = self.make_class("Ellipse").move_to(RIGHT*3)
		arrow_2 = self.connect(shape, ellipse)

		self.play(GrowFromCenter(arrow), Create(polygon), 
			GrowFromCenter(arrow_2), Create(ellipse))


		quadrilateral = self.make_class("Quadrilateral").move_to(DOWN*2 + LEFT*5)
		arrow_3 = self.connect(polygon, quadrilateral)

		triangle = self.make_class("Triangle").move_to(DOWN*2 + LEFT)
		arrow_4 = self.connect(polygon, triangle)

		circle = self.make_class("Circle").move_to(DOWN*2 + RIGHT*5)
		arrow_5 = self.connect(ellipse, circle)

		self.play(GrowFromCenter(arrow_3), Create(quadrilateral), 
			GrowFromCenter(arrow_4), Create(triangle),
			GrowFromCenter(arrow_5), Create(circle))


		rectangle = self.make_class("Rectangle").move_to(DOWN*3.5 + LEFT*2)
		arrow_6 = self.connect(quadrilateral, rectangle)
		self.play(GrowFromCenter(arrow_6), Create(rectangle))
		self.wait(3)


		num_sides = Text("int numSides;", font_size=24, color=PURPLE).next_to(polygon, RIGHT)
		self.play(Write(num_sides))
		self.wait(2)


		dot = Dot().set_color(GOLD)
		dot_2 = dot.copy()
		dot_3 = dot.copy()

		self.play(MoveAlongPath(dot, arrow_3.copy().reverse_points()), MoveAlongPath(dot_2, arrow_4.copy().reverse_points()))
		self.play(FadeOut(dot), FadeOut(dot_2))
		self.play(MoveAlongPath(dot_3, arrow_6.copy().reverse_points()))
		self.play(FadeOut(dot_3))

		self.wait(3)



class InheritanceGoal1(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("1. Inheritance").shift(UP*3)
		self.play(Write(title))

		definition = Text("Player member variables and methods are passed on to subtypes.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		player_text = """
typedef struct Player_protected 
	Player_protected;

typedef struct Player {
	int player_id;
	Role role;
	Player_protected* protected;
} Player;
		"""
		player_bundle = make_bundle(player_text, "player.h", stf=6).move_to(LEFT*4 + UP*0.5)

		self.play(Create(player_bundle))
		self.wait(3)


		player_protected_text = """
struct Player_protected {
	int is_alive;
	int is_bitten;
	int can_vote;
};
		"""
		player_protected_bundle = make_bundle(player_protected_text, "player_protected.h", stf=6).move_to(LEFT*4 + DOWN*2)

		self.play(Create(player_protected_bundle))
		self.wait(3)



		healer_text = """
typedef struct Healer {

} Healer;


.
		"""
		healer_bundle = make_bundle(healer_text, "healer.h", stf=6).move_to(RIGHT*4 + DOWN)

		self.play(Create(healer_bundle))
		self.wait(3)


		def transform_healer(new_text):
			healer_bundle_2 = make_bundle(new_text, "healer.h", stf=6).move_to(RIGHT*4 + DOWN)

			self.play(Transform(healer_bundle, healer_bundle_2))
			self.wait(1)


		help_text = make_help_text("Subtypes should have member variables inherited from the Player type.")
		self.play(FadeIn(help_text, shift=UP))


		healer_text_2 = """
typedef struct Healer {

} Healer;

Healer *healer = Healer_ctor(id);
printf("%d", healer->player_id);
		"""
		transform_healer(healer_text_2)
		self.wait(2)


		help_text_2 = make_help_text("We shouldn't have to reimplement any inherited member variables and methods.")
		self.play(Transform(help_text, help_text_2))


		healer_text_2 = """
typedef struct Healer {
	int player_id;
} Healer;

Healer *healer = Healer_ctor(id);
printf("%d", healer->player_id);
		"""
		transform_healer(healer_text_2)
		self.play(healer_bundle[0].animate.set_fill_color(RED).set_stroke_color(RED))
		self.wait(2)


		healer_text_2 = """
typedef struct Healer {

} Healer;

Healer *healer = Healer_ctor(id);
printf("%d", healer->player_id);
		"""
		transform_healer(healer_text_2)
		self.wait(2)


		arrow = Arrow(player_bundle.get_right(), healer_bundle.get_left())
		arrow_2 = Arrow(player_protected_bundle.get_right(), healer_bundle.get_left())
		self.play(GrowFromCenter(arrow), GrowFromCenter(arrow_2))
		self.wait(2)



class InheritanceGoal2(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("2. Upcasting").shift(UP*3)
		self.play(Write(title))

		definition = Text("Ability to cast subtypes back to the parent type.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		player_text = """
typedef struct Player_protected 
	Player_protected;

typedef struct Player {
	int player_id;
	Role role;
	Player_protected* protected;
} Player;

// Public
void Player_reset(Player* self);
int Player_can_vote(const Player* self);
...
		"""
		player_bundle = make_bundle(player_text, "player.h", stf=7).move_to(LEFT*3.5)

		self.play(Create(player_bundle))
		self.wait(3)


		help_text = make_help_text("Game interacts with Players via public methods.")
		self.play(FadeIn(help_text, shift=UP))


		game_text = """
Healer *healer = Healer_ctor(id);

if (Player_can_vote(healer))
{
	printf("Player %d: ", player->player_id);
	printf("Cast your vote!\\n);
}
		"""
		game_bundle = make_bundle(game_text, "game.h", stf=7).move_to(RIGHT*3.5)

		self.play(Create(game_bundle))
		self.wait(3)
		self.play(game_bundle[0].animate.set_fill_color(RED).set_stroke_color(RED))


		def transform_game(new_text):
			game_bundle_2 = make_bundle(new_text, "game.h", stf=7).move_to(RIGHT*3.5)

			self.play(Transform(game_bundle, game_bundle_2))
			self.wait(1)


		help_text_2 = make_help_text("Requires a pointer to a Player type; need to upcast.")
		self.play(Transform(help_text, help_text_2))


		game_text_2 = """
Healer *healer = Healer_ctor(id);

if (Player_can_vote((Player *)healer))
{
	printf("Player %d: ", player->player_id);
	printf("Cast your vote!\\n);
}
		"""

		transform_game(game_text_2)
		self.wait(2)



class InheritanceGoal3(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("3. Extendability").shift(UP*3)
		self.play(Write(title))

		definition = Text("Subtypes should be able to extend the parent type.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		healer_text = """
typedef struct Healer {

} Healer;

.
		"""
		healer_bundle = make_bundle(healer_text, "healer.h", buff=1)

		self.play(Create(healer_bundle))
		self.wait(3)


		def transform_healer(new_text):
			healer_bundle_2 = make_bundle(new_text, "healer.h", buff=1)

			self.play(Transform(healer_bundle, healer_bundle_2))
			self.wait(1)


		help_text = make_help_text("Subtypes can add their own private and public member variables.")
		self.play(FadeIn(help_text, shift=UP))


		healer_text_2 = """
typedef struct Healer {
	int last_healed;
} Healer;

.
		"""
		transform_healer(healer_text_2)
		self.wait(2)


		healer_text_2 = """
typedef struct Healer {
	int last_healed;
} Healer;

int Healer_attempt_self_heal(Healer* self);
		"""
		transform_healer(healer_text_2)
		self.wait(2)


		help_text_2 = make_help_text("Should be able to downcast a Player (with HEALER Role) to a Healer.")
		self.play(Transform(help_text, help_text_2))
		self.wait(2)



class StructEmbedding(Scene):
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
			rect_text = Text(member['type'] + '\n' + member['name'] + '\n' + str(member['size']) + " bytes", font_size=24).move_to(rect.get_center()).align_to(rect, LEFT).shift(RIGHT*0.1)
			rectangle = VGroup(rect, rect_text)
			struct.add(rectangle)

		return VGroup(title, struct.arrange(DOWN, buff=0)).arrange(DOWN)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Struct Embedding").shift(UP*3)
		self.play(Write(title))

		definition = Text("Making one struct a member of another struct.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		help_text = make_help_text("Nest the parent type as a member of the child type.")
		self.play(FadeIn(help_text, shift=UP))
		self.wait(2)


		bear_text = """
struct Bear {
	Player super;
}
		"""
		bear_bundle = make_bundle(bear_text, "bear.h")

		self.play(Create(bear_bundle))
		self.wait(3)


		help_text_2 = make_help_text("Embeds the contents of the inner struct into the memory allocated for the outer.")
		self.play(Transform(help_text, help_text_2))
		self.wait(2)


		def transform_bear(new_text):
			bear_bundle_2 = make_bundle(new_text, "bear.h")

			self.play(Transform(bear_bundle, bear_bundle_2))
			self.wait(1)


		bear_text_2 = """
struct Player {
	int player_id;
	Role role;
	Player_protected* protected;
};
		"""
		bear_bundle_2 = make_bundle(bear_text_2, "player.h")
		self.play(Transform(bear_bundle, bear_bundle_2.shift(LEFT*3)))
		self.wait(2)

		struct_dict = [
			{
				"size": 4,
				"colour": BLUE,
				"name": "player_id",
				"type": "int"
			},
			{
				"size": 4,
				"colour": TEAL,
				"name": "role",
				"type": "Role"
			},
			{
				"size": 8,
				"colour": PINK,
				"name": "protected",
				"type": "Player_protected*"
			}
		]

		struct = self.create_struct_memory("Player", struct_dict)
		self.play(Create(struct.scale(0.5).shift(RIGHT*3 + DOWN*0.5)))
		self.wait(2)


		bear_text_2 = """
struct Bear {
	Player super;
	int last_bitten;
};
		"""
		bear_bundle_2 = make_bundle(bear_text_2, "bear.h")
		self.play(Transform(bear_bundle, bear_bundle_2.shift(LEFT*3)))
		self.wait(2)


		struct_dict.append({
			"size": 4,
			"colour": BLUE,
			"name": "last_bitten",
			"type": "int"
		})
		struct_dict.append({
			"size": 4,
			"colour": GRAY_C,
			"name": "padding",
			"type": ""
		})

		struct_2 = self.create_struct_memory("Bear", struct_dict).scale(0.4).shift(RIGHT*3 + DOWN*0.5)
		self.play(Transform(struct, struct_2))
		self.wait(2)


		brace = BraceBetweenPoints(
			point_1=struct[1][0].get_top(),
			point_2=struct[1][2].get_bottom(),
			direction=LEFT
		).shift(LEFT*0.6)
		player = Text("Player\nsuper", font_size=24).next_to(brace, LEFT, buff=0.2)
		self.play(GrowFromCenter(brace), Write(player))
		self.wait(2)



class StructEmbedding2(Scene):
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
			rect_text = Text(member['type'] + '\n' + member['name'] + '\n' + str(member['size']) + " bytes", font_size=24).move_to(rect.get_center()).align_to(rect, LEFT).shift(RIGHT*0.1)
			rectangle = VGroup(rect, rect_text)
			struct.add(rectangle)

		return VGroup(title, struct.arrange(DOWN, buff=0)).arrange(DOWN)


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Upcasting").shift(UP*3)
		self.play(Write(title))

		definition = Text("Casting/treating the subtype as the parent type.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		help_text = make_help_text("Embed the parent type as the FIRST member of the child type.")
		self.play(FadeIn(help_text, shift=UP))
		self.wait(2)


		bear_text = """
struct Bear {
	Player super;
	int last_bitten;
};
		"""
		bear_bundle = make_bundle(bear_text, "bear.h").shift(LEFT*3)

		self.play(Create(bear_bundle))
		self.wait(3)


		help_text_2 = make_help_text("Player data starts at the same address as the Bear struct.")
		self.play(Transform(help_text, help_text_2))
		self.wait(2)


		struct_dict = [
			{
				"size": 4,
				"colour": BLUE,
				"name": "player_id",
				"type": "int"
			},
			{
				"size": 4,
				"colour": TEAL,
				"name": "role",
				"type": "Role"
			},
			{
				"size": 8,
				"colour": PINK,
				"name": "protected",
				"type": "Player_protected*"
			},
			{
				"size": 4,
				"colour": BLUE,
				"name": "last_bitten",
				"type": "int"
			},
			{
				"size": 4,
				"colour": GRAY_C,
				"name": "padding",
				"type": ""
			}
		]

		struct = self.create_struct_memory("Bear", struct_dict).scale(0.4).shift(RIGHT*3 + DOWN*0.5)
		self.play(Create(struct))
		self.wait(2)


		brace = BraceBetweenPoints(
			point_1=struct[1][0].get_top(),
			point_2=struct[1][2].get_bottom(),
			direction=LEFT
		).shift(LEFT*0.6)
		player = Text("Player\nsuper", font_size=24).next_to(brace, LEFT, buff=0.2)
		self.play(GrowFromCenter(brace), Write(player))
		self.wait(2)


		bear_text_2 = """
struct Bear {
	Player super;
	int last_bitten;
};

Bear *bear = malloc(sizeof(Bear));
Player *player = (Player *)bear;
"""

		def transform_bear(new_text):
			bear_bundle_2 = make_bundle(new_text, "bear.h").shift(LEFT*3)

			self.play(Transform(bear_bundle, bear_bundle_2))
			self.wait(1)

		transform_bear(bear_text_2)
		
		help_text_2 = make_help_text("The start of the memory layout for Bear is identical to a Player.")
		self.play(Transform(help_text, help_text_2))
		self.wait(2)



class FisherYates(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Fisher-Yates Shuffle").shift(UP*3)
		self.play(Write(title))

		definition = Text("Generates a random permutation of an array.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(10)



class FactoryPattern(Scene):
	def make_ctor_text(self, text, colour):
		ctor_rect = Rectangle(
			width=3, height=1.5,
			fill_color=colour,
			stroke_color=colour,
			fill_opacity=0.1
		)
		ctor_text = Text(text, font_size=20).move_to(ctor_rect.get_center())
		return VGroup(ctor_rect, ctor_text)

	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)


		title = Text("Factory Pattern").shift(UP*3)
		self.play(Write(title))

		definition = Text("Delegating subtype creation to another function.", font_size=20).next_to(title, DOWN)
		self.play(Write(definition))
		self.wait(3)


		game_rect = Rectangle(
			width=2, height=1.5,
			fill_color=GRAY_C,
			stroke_color=GRAY_C,
			fill_opacity=0.1
		)
		game_text = Text("Game", font_size=24).move_to(game_rect.get_center())
		game = VGroup(game_rect, game_text).shift(LEFT*4 + DOWN)
		self.play(Create(game))
		self.wait(2)


		factory_rect = Rectangle(
			width=3, height=1.5,
			fill_color=GRAY_C,
			stroke_color=GRAY_C,
			fill_opacity=0.1
		)
		factory_text = Text("Factory Method", font_size=24).move_to(factory_rect.get_center())
		factory = VGroup(factory_rect, factory_text).shift(DOWN)
		self.play(Create(factory))
		self.wait(2)


		ctors = VGroup()
		ctor_params = [("Bear_ctor", ORANGE), ("Activist_ctor", GREEN), ("Clairvoyant_ctor", PURPLE), ("Healer_ctor", BLUE), ("Townsperson_ctor", YELLOW)]
		for param in ctor_params:
			ctors.add(self.make_ctor_text(*param))
		ctors.arrange(DOWN).scale(0.6).shift(RIGHT*4 + DOWN)
		self.play(Create(ctors))
		self.wait(2)


		def animate_factory(pid, role, role_id):	
			pass_in = Text("(%d, %s)" % (pid, role.upper()), font_size=24).move_to(game.get_bottom()+DOWN*0.5)
			self.play(pass_in.animate.move_to(factory.get_bottom()+DOWN*0.5))
			self.wait(1)

			pass_in_2 = Text(str(pid), font_size=24).move_to(factory.get_bottom()+DOWN*0.5)
			self.play(Transform(pass_in, pass_in_2))
			self.play(pass_in.animate.move_to(ctors[role_id].get_left()+LEFT*0.5))
			self.wait(1)

			pass_in_2 = Text("%s*" % (role), font_size=24).move_to(ctors[role_id].get_left()+LEFT*0.5)
			self.play(Transform(pass_in, pass_in_2))
			self.play(pass_in.animate.move_to(factory.get_bottom()+DOWN*0.5))
			self.wait(1)

			pass_in_2 = Text("Player*", font_size=24).move_to(factory.get_bottom()+DOWN*0.5)
			self.play(Transform(pass_in, pass_in_2))
			self.play(pass_in.animate.move_to(game.get_bottom()+DOWN*0.5))
			self.wait(1)

			self.play(FadeOut(pass_in))
			self.wait(1)


		animate_factory(1, "Healer", 3)
		animate_factory(2, "Townsperson", 4)
		animate_factory(3, "Bear", 0)
