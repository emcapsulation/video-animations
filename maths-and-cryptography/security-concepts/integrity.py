from manim import *
from entities import *
from introduction import move_to_seat
import hashlib


config.background_color = "#17001f"


class IntegrityConversation(Scene):

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
		self.wait(2)


		floppy = FloppyDisk().floppy_disk.scale(0.8).move_to(family.get_family_group_member("Dad").get_center() + LEFT*2)
		self.play(FadeIn(floppy))
		self.wait(2)

		self.play(Wiggle(floppy))
		secret_sauce = SecretSauce("tampered").get_secret_sauce().move_to(floppy.get_center()).scale(0.5)
		self.play(Transform(floppy, secret_sauce))
		self.wait(2)


		self.play(Wiggle(family.get_family_group_member("Uncle")))
		self.wait(2)


		self.play(Wiggle(family.get_family_group_member("Brother")))
		exclamation = Text("!").move_to(family.get_family_group_member("Brother").get_center() + RIGHT)
		self.play(Indicate(exclamation, color=RED))
		self.wait(2)




class IntegrityMeaning(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Integrity", color=PURPLE).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))


		subtitle = Text("Data has not been altered in any way - it is complete and accurate.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		secret_sauce = SecretSauce("text").get_secret_sauce().scale(0.8).move_to(DOWN)
		self.play(Create(secret_sauce))
		self.wait(1)

		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().scale(0.8).move_to(DOWN)
		self.play(Transform(secret_sauce, secret_sauce_encrypted))
		self.wait(2)


		secret_sauce_plain = SecretSauce("text").get_secret_sauce().scale(0.8).move_to(DOWN)
		self.play(Transform(secret_sauce, secret_sauce_plain))
		self.wait(1)

		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(RIGHT*8 + DOWN*3)
		secret_sauce_tamper = SecretSauce("tampered").get_secret_sauce().scale(0.8).move_to(DOWN)
		
		self.play(evil_guy.animate.move_to(secret_sauce.get_right() + RIGHT + DOWN))
		self.play(Transform(secret_sauce, secret_sauce_tamper), evil_guy.animate.move_to(RIGHT*8 + DOWN*3))
		self.wait(2)



class HashFunctions(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Hash Functions", color=PURPLE).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))


		subtitle = Text("A one-way process that converts an input into a fixed-size hash.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		# Draw the plaintext secret sauce and hash function
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(LEFT*5 + DOWN).scale(0.6)
		secret_sauce_copy = secret_sauce_plaintext.copy()
		self.play(Create(secret_sauce_plaintext))

		hash_background = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		hash_text = Text("Hash Function", font_size=24).move_to(hash_background.get_center())
		hash_scheme = VGroup(hash_background, hash_text).shift(DOWN + LEFT*1.5)
		self.play(Create(hash_scheme))
		self.wait(2)

		self.play(secret_sauce_plaintext.animate.move_to(hash_scheme.get_left()))


		# Hash comes out the other side
		sha256_hash = hashlib.sha256()
		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash.update(data_to_hash.encode('utf-8'))
		hash_output = Text(sha256_hash.hexdigest(), font_size=20).move_to(hash_scheme.get_right()).scale(0.7)

		self.play(
			secret_sauce_plaintext.animate.move_to(secret_sauce_copy.get_center()),
			hash_output.animate.move_to(RIGHT*3.5 + DOWN)
		)
		self.wait(5)


		# Tamper with the recipe
		tampered_secret_sauce = SecretSauce("tampered_2").get_secret_sauce().move_to(LEFT*5 + DOWN).scale(0.6)
		self.play(Transform(secret_sauce_plaintext, tampered_secret_sauce))
		self.wait(2)

		self.play(
			secret_sauce_plaintext.animate.move_to(hash_scheme.get_left()),
			hash_output.animate.shift(UP),
		)

		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n0 clove garlic"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		hash_output_2 = Text(sha256_hash.hexdigest(), font_size=20).move_to(hash_scheme.get_right()).scale(0.7)

		self.play(
			secret_sauce_plaintext.animate.move_to(secret_sauce_copy.get_center()),			
			hash_output_2.animate.move_to(RIGHT*3.5 + DOWN)
		)
		self.wait(5)


		# One way
		self.play(hash_output_2.animate.shift(LEFT*0.5))
		self.play(hash_output_2.animate.shift(RIGHT*0.5))
		self.play(Wiggle(hash_output_2))
		self.wait(3)



class HashFunctions2(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Hash Functions", color=PURPLE).move_to(UP*3)
		subtitle = Text("A one-way process that converts an input into a fixed-size hash.", font_size=20).next_to(title, DOWN)
		self.add(title, subtitle)
		self.wait(2)


		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		self.play(Create(dad))

		secret_sauce = SecretSauce("text").get_secret_sauce().move_to(LEFT*4 + DOWN).scale(0.6)
		self.play(Create(secret_sauce))
		self.wait(2)


		# Store hash of original
		sha256_hash = hashlib.sha256()
		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash = Text(sha256_hash.hexdigest(), font_size=20).move_to(DOWN)
		self.play(ReplacementTransform(secret_sauce, sauce_hash))
		self.wait(1)

		self.play(sauce_hash.animate.move_to(RIGHT*2 + UP).scale(0.7))

		lock = Lock(GOLD).lock.scale(0.7).move_to(sauce_hash.get_center() + DOWN*0.5)
		self.play(SpinInFromNothing(lock))
		self.wait(2)


		# Recompute hash (correct)
		secret_sauce = SecretSauce("text").get_secret_sauce().move_to(LEFT*4 + DOWN).scale(0.6)
		self.play(FadeIn(secret_sauce, shift=RIGHT*0.5))
		self.wait(2)

		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash_2 = Text(sha256_hash.hexdigest(), font_size=20).move_to(DOWN)
		self.play(ReplacementTransform(secret_sauce, sauce_hash_2))
		self.wait(1)

		self.play(sauce_hash_2.animate.move_to(RIGHT*2 + DOWN).scale(0.7))
		self.wait(2)


		green_check = Text("☑", color=GREEN, font_size=108).move_to(sauce_hash_2.get_center())
		self.play(SpinInFromNothing(green_check))
		self.wait(2)


		self.play(FadeOut(sauce_hash_2), FadeOut(green_check))


		# Recompute hash (not correct)
		secret_sauce = SecretSauce("tampered").get_secret_sauce().move_to(LEFT*4 + DOWN).scale(0.6)
		self.play(FadeIn(secret_sauce, shift=RIGHT*0.5))
		self.wait(2)

		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n10 chillis"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash_2 = Text(sha256_hash.hexdigest(), font_size=20).move_to(DOWN)
		self.play(ReplacementTransform(secret_sauce, sauce_hash_2))
		self.wait(1)

		self.play(sauce_hash_2.animate.move_to(RIGHT*2 + DOWN).scale(0.7))
		self.wait(2)


		x = Text("X", color=RED).move_to(sauce_hash_2.get_center())
		self.play(SpinInFromNothing(x))
		self.wait(2)


		self.play(FadeOut(sauce_hash_2), FadeOut(x))



class ModifyTransit(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		# Mum and dad are going to email each other
		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(RIGHT*5.5 + DOWN)
		self.play(Create(dad), Create(mum))
		self.wait(2)


		# Sauce goes halfway
		sauce_scale = 0.3		
		path = ArcBetweenPoints(RIGHT*4.5, LEFT*4.5, angle=PI/4, color=GRAY)
		path_2 = ArcBetweenPoints(RIGHT*4.5, UP*0.5, angle=PI/8, color=GRAY)

		secret_sauce = SecretSauce("text").get_secret_sauce().scale(sauce_scale)
		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash = Text(sha256_hash.hexdigest()[0:9], font_size=20)
		sauce_and_hash = VGroup(secret_sauce, sauce_hash).arrange(DOWN).move_to(RIGHT*4.5)

		self.play(FadeIn(path), FadeIn(sauce_and_hash))


		# Guy changes it
		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(DOWN*7)
		self.play(MoveAlongPath(sauce_and_hash, path_2), evil_guy.animate.shift(UP*6))
		self.wait(1)

		secret_sauce_tampered = SecretSauce("tampered").get_secret_sauce().scale(sauce_scale).move_to(secret_sauce.get_center())
		self.play(evil_guy.animate.shift(UP))
		self.play(evil_guy.animate.shift(DOWN), Transform(secret_sauce, secret_sauce_tampered))

		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n10 chillis"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		new_sauce_hash = Text(sha256_hash.hexdigest()[0:9], font_size=20, color=RED).move_to(sauce_hash.get_center())

		self.play(evil_guy.animate.shift(UP*0.5))
		self.play(evil_guy.animate.shift(DOWN*6), Transform(sauce_hash, new_sauce_hash))
		self.wait(2)


		path_3 = ArcBetweenPoints(UP*0.5, LEFT*4.5, angle=PI/8, color=GRAY)
		self.play(MoveAlongPath(sauce_and_hash, path_3))


		x = Text("X", color=RED)
		self.play(SpinInFromNothing(x))

		self.wait(2)
		self.play(FadeOut(x))




class MAC(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Message Authentication Code", color=PURPLE).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))


		subtitle = Text("A tag computed on the message and a shared secret key.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(RIGHT*5.5 + DOWN)
		self.play(Create(dad), Create(mum))
		self.wait(2)


		start = RIGHT*4
		end = LEFT*4
		sauce_scale = 0.3
		FS = 14


		# Append a MAC
		rect_bg = RoundedRectangle(
			width=2, height=2.5,
			stroke_color=WHITE
		)
		
		secret_sauce = SecretSauce("text").get_secret_sauce().scale(sauce_scale)
		key_words = Text("secret_key", font_size=FS, color=GOLD)		
		sauce_key = VGroup(key_words, secret_sauce).arrange(DOWN).move_to(rect_bg.get_center())
		sauce_key_bg = VGroup(rect_bg, secret_sauce, key_words)		

		data_to_hash = "secret_keySecret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		mac = Text(sha256_hash.hexdigest()[0:9], font_size=FS)

		sauce_key_mac = VGroup(sauce_key_bg, mac).arrange(DOWN).move_to(start)
		sauce_key_bg_copy = sauce_key_mac.copy().shift(LEFT*8)
		sauce_mac = VGroup(secret_sauce, mac)
		key_words_copy = sauce_key_bg_copy[0][2]


		self.play(Create(secret_sauce))
		self.wait(1)
		self.play(FadeIn(key_words), FadeIn(key_words_copy))
		self.wait(2)
		self.play(Create(rect_bg))
		self.play(FadeIn(mac, shift=DOWN*0.5))
		self.wait(2)


		self.play(sauce_mac.animate.shift(LEFT*8), FadeOut(rect_bg))
		self.wait(1)


		# Receiver recomputes the MAC
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		mac_2 = Text(sha256_hash.hexdigest()[0:9], font_size=FS).move_to(sauce_key_bg_copy[1].get_center())

		self.play(mac.animate.shift(DOWN*0.5), Create(sauce_key_bg_copy[0][0]))
		self.play(FadeIn(mac_2, shift=DOWN*0.5))
		self.wait(2)

		self.play(mac.animate.set_color(GREEN), mac_2.animate.set_color(GREEN))
		self.wait(1)

		green_check = Text("☑", color=GREEN_D, font_size=108).move_to(secret_sauce.get_center())
		self.play(SpinInFromNothing(green_check))
		self.wait(2)




class MAC2(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Message Authentication Code", color=PURPLE).move_to(UP*3)
		self.add(title)


		subtitle = Text("A tag computed on the message and a shared secret key.", font_size=20).next_to(title, DOWN)
		self.add(subtitle)


		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(RIGHT*5.5 + DOWN)
		self.add(dad, mum)
		self.wait(2)


		start = RIGHT*4
		end = LEFT*4
		sauce_scale = 0.3
		FS = 14


		# Append a MAC
		rect_bg = RoundedRectangle(
			width=2, height=2.5,
			stroke_color=WHITE
		)
		
		secret_sauce = SecretSauce("text").get_secret_sauce().scale(sauce_scale)
		key_words = Text("secret_key", font_size=FS, color=GOLD)		
		sauce_key = VGroup(key_words, secret_sauce).arrange(DOWN).move_to(rect_bg.get_center())
		sauce_key_bg = VGroup(rect_bg, secret_sauce, key_words)		

		data_to_hash = "secret_keySecret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		mac = Text(sha256_hash.hexdigest()[0:9], font_size=FS)

		sauce_key_mac = VGroup(sauce_key_bg, mac).arrange(DOWN).move_to(start)
		sauce_key_bg_copy = sauce_key_mac.copy().shift(LEFT*8)
		sauce_mac = VGroup(secret_sauce, mac)
		key_words_copy = sauce_key_bg_copy[0][2]


		self.play(Create(secret_sauce))
		self.wait(1)
		self.play(FadeIn(key_words), FadeIn(key_words_copy))
		self.wait(2)
		self.play(Create(rect_bg))
		self.play(FadeIn(mac, shift=DOWN*0.5))
		self.wait(2)


		# Guy changes it
		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(DOWN*7)
		self.play(sauce_mac.animate.shift(LEFT*4), FadeOut(rect_bg), evil_guy.animate.shift(UP*5.5))
		self.wait(1)

		secret_sauce_tampered = SecretSauce("tampered").get_secret_sauce().scale(sauce_scale).move_to(secret_sauce.get_center())
		self.play(evil_guy.animate.shift(UP*0.5))
		self.play(evil_guy.animate.shift(DOWN*0.5), Transform(secret_sauce, secret_sauce_tampered))
		self.wait(2)


		q_mark = Text("?", color=RED).move_to(evil_guy.get_center())
		self.play(Transform(evil_guy, q_mark))
		self.wait(2)
		self.play(evil_guy.animate.shift(DOWN*5.5))
		self.play(sauce_mac.animate.shift(LEFT*4))


		# Receiver recomputes the MAC
		sha256_hash = hashlib.sha256()
		data_to_hash = "secret_keySecret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n10 chillis"
		sha256_hash.update(data_to_hash.encode('utf-8'))
		mac_2 = Text(sha256_hash.hexdigest()[0:9], font_size=FS).move_to(sauce_key_bg_copy[1].get_center())

		self.play(mac.animate.shift(DOWN*0.5), Create(sauce_key_bg_copy[0][0]))
		self.play(FadeIn(mac_2, shift=DOWN*0.5))
		self.wait(2)

		self.play(mac.animate.set_color(RED), mac_2.animate.set_color(RED))
		self.wait(1)

		x = Text("X", color=RED_D, font_size=108).move_to(secret_sauce.get_center())
		self.play(SpinInFromNothing(x))
		self.wait(2)


		digital_signatures = Text("Digital Signatures: Uses private key to sign, public key to verify.", font_size=24, t2c={"Digital Signatures:": PURPLE}).move_to(DOWN*3)
		self.play(FadeOut(x), Write(digital_signatures))
		self.wait(5)




class VersionControl(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Version Control and Logging", color=PURPLE).move_to(UP*3)
		self.add(title)
		self.wait(5)


		accountability = Text("Accountability: Tracing an action back to the entity which performed it.", font_size=20, t2c={"Accountability:": PURPLE}).move_to(DOWN*3)
		self.play(Write(accountability))
		self.wait(5)




class IntegrityConversation2(Scene):

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
		

		self.play(Wiggle(family.get_family_group_member("Brother")))
		self.wait(2)

		self.play(Wiggle(family.get_family_group_member("Uncle")))
		self.wait(2)

		self.play(Wiggle(family.get_family_group_member("Grandpa")))
		self.wait(2)