from manim import *
from entities import *


config.background_color = "#00141a"


def move_to_seat(scene, family_list, table_radius, table_centre, animate=True):
	move_to_seat_animations = []
	i = 0
	while i < len(family_list):
		up = table_radius*math.sin(i*2*PI/len(family_list))
		right = table_radius*math.cos(i*2*PI/len(family_list))
		seat_position = UP*up + RIGHT*right

		if animate:
			move_to_seat_animations.append(family_list[i].get_human().animate.move_to(seat_position+table_centre))
		else:
			family_list[i].get_human().move_to(seat_position+table_centre)
			scene.add(family_list[i].get_human())
		i += 1

	if animate:
		scene.play(*move_to_seat_animations)



class ConfidentialityConversation(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		y_pos = DOWN*0.37
		positions = [RIGHT*5+y_pos, *[LEFT*x+y_pos for x in range(5, -5, -2)]]

		family = Family(0.8, 0.4, 1, positions)
		family.set_labels(["You", "Grandpa", "Uncle", "Dad", "Mum", "Brother"])
		family.set_colours([PURPLE, ORANGE, GOLD, GREEN, TEAL, BLUE])

		family_list = family.get_family_list()


		move_to_seat(self, family_list, 2.5, DOWN*0.5, animate=False)
		self.play(family.get_family_group().animate.shift(UP*0.5))


		brother_line_1 = Text("PLEASE tell me you\nencrypted it.", font_size=16).move_to(family.get_family_group_member("Brother").get_center() + RIGHT*3.5)
		self.play(Write(brother_line_1))
		self.wait(2)

		uncle_line_1 = Text("not_the_secret_sauce.pdf", font_size=20).move_to(family.get_family_group_member("Uncle").get_center() + LEFT*3)
		self.play(
			AddTextLetterByLetter(uncle_line_1),
			FadeOut(brother_line_1)
		)
		self.wait(2)


		usb = Usb().usb.scale(0.8).move_to(family.get_family_group_member("Brother").get_center() + RIGHT*2)
		self.play(FadeOut(uncle_line_1), FadeIn(usb))

		competitor = Human(MAROON_D, 1).get_human().move_to(usb.get_center() + RIGHT).scale(0.3)
		self.play(FadeIn(competitor))
		self.play(
			competitor.animate.shift(RIGHT*10), 
			usb.animate.shift(RIGHT*10)
		)
		self.wait(2)


		lock = Lock(GOLD).lock.move_to(family.get_family_group_member("Grandpa").get_center() + RIGHT*2)
		self.play(SpinInFromNothing(lock))
		self.wait(2)




class ConfidentialityMeaning(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Confidentiality", color=BLUE).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))


		subtitle = Text("Protection of data from those who are not authorised to access it.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		# Draw the plaintext secret sauce, key, and encryption scheme
		sauce_scale = 0.6
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(LEFT*4 + DOWN*0.5).scale(sauce_scale)
		self.play(Create(secret_sauce_plaintext))

		key = Key(YELLOW).get_key().scale(0.25).move_to(LEFT*4 + DOWN*3)
		self.play(Create(key))

		encryption_background = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		encryption_text = Text("Encryption Scheme", font_size=24).move_to(encryption_background.get_center())
		encryption_scheme = VGroup(encryption_background, encryption_text).shift(DOWN + RIGHT*0.5)
		self.play(Create(encryption_scheme))
		self.wait(2)

		self.play(
			secret_sauce_plaintext.animate.move_to(encryption_scheme.get_left()),
			key.animate.move_to(encryption_scheme.get_left())
		)


		# Encrypted recipe comes out the other side
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(encryption_scheme.get_right()).scale(sauce_scale)

		self.play(
			FadeOut(secret_sauce_plaintext),
			FadeOut(key),
			secret_sauce_encrypted.animate.move_to(RIGHT*5 + DOWN)
		)
		self.wait(2)


		# Correct key can decrypt it
		you = Human(PURPLE, 0.8).human.scale(0.25).move_to(RIGHT*8 + UP*3)
		decrypt = Key(YELLOW).get_key().scale(0.25).move_to(you.get_center() + DOWN*0.3)
		you_and_key = VGroup(you, decrypt)

		self.play(you_and_key.animate.move_to(secret_sauce_encrypted.get_center() + UP*2))
		self.play(
			secret_sauce_encrypted.animate.move_to(encryption_scheme.get_right()),
			decrypt.animate.move_to(encryption_scheme.get_right())
		)

		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(encryption_scheme.get_left()).scale(sauce_scale)
		self.play(
			FadeOut(secret_sauce_encrypted),
			FadeOut(decrypt),
			secret_sauce_plaintext.animate.move_to(LEFT*5 + DOWN)
		)
		self.wait(2)


		# Bring back the encrypted one
		self.play(FadeOut(secret_sauce_plaintext), FadeOut(you))

		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(RIGHT*5 + DOWN).scale(sauce_scale)
		self.play(FadeIn(secret_sauce_encrypted))


		# Other guy tries to guess key
		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(RIGHT*8 + UP*3)
		keys = [PINK, TEAL, PURPLE, GREEN, MAROON]


		decrypt = Key(keys[0]).get_key().scale(0.25).move_to(evil_guy.get_center() + DOWN*0.3)
		evil_and_key = VGroup(evil_guy, decrypt)
		self.play(evil_and_key.animate.move_to(secret_sauce_encrypted.get_center() + UP*2))

		for i in range(1, len(keys)):			
			self.play(
				secret_sauce_encrypted.animate.move_to(encryption_scheme.get_right()),
				decrypt.animate.move_to(encryption_scheme.get_right())
			)
			self.play(
				Wiggle(secret_sauce_encrypted),
				Wiggle(decrypt)
			)
			self.play(
				secret_sauce_encrypted.animate.move_to(RIGHT*5 + DOWN),
				decrypt.animate.move_to(evil_guy.get_center() + DOWN*0.3)
			)
			self.play(
				Transform(decrypt, Key(keys[i]).get_key().scale(0.25).move_to(evil_guy.get_center() + DOWN*0.3))
			)



class Symmetric(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Symmetric Encryption", color=BLUE).move_to(UP*3)
		self.play(AddTextLetterByLetter(title))


		subtitle = Text("Uses the same key to encrypt and decrypt the data.", font_size=20).next_to(title, DOWN)
		self.play(Write(subtitle))
		self.wait(5)


		# Draw the plaintext secret sauce, key, and encryption scheme
		sauce_scale = 0.3
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(LEFT*4.5 + UP*1.25).scale(sauce_scale)

		brother = Human(BLUE, 0.8).add_label("Brother", WHITE).human.scale(0.25).move_to(LEFT*3.5 + UP*1.25)
		key_words = Text("my_256_bit_incredibly_secret_key", font_size=14).next_to(brother, RIGHT)
		decrypt = Key(YELLOW).get_key().scale(0.2).move_to(brother.get_center() + DOWN*0.3)
		bro_key = VGroup(brother, decrypt)

		self.play(Create(brother), AddTextLetterByLetter(key_words))
		self.play(Create(secret_sauce_plaintext), ReplacementTransform(key_words, decrypt))
		self.play(
			secret_sauce_plaintext.animate.move_to(LEFT*4 + UP*1),
			decrypt.animate.move_to(LEFT*4 + UP*1)
		)


		# Encrypted recipe comes out the other side
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(LEFT*4 + DOWN*2.5).scale(sauce_scale)
		self.play(
			FadeOut(secret_sauce_plaintext),
			secret_sauce_encrypted.animate.move_to(LEFT*4 + DOWN*3)
		)
		self.wait(2)


		# Same key can decrypt it
		self.play(
			bro_key.animate.move_to(RIGHT*3.5 + DOWN*3), 
			secret_sauce_encrypted.animate.move_to(RIGHT*4.5 + DOWN*3)
		)
		self.play(
			secret_sauce_encrypted.animate.move_to(RIGHT*4 + DOWN*2.5),
			decrypt.animate.move_to(RIGHT*4 + DOWN*2.5)
		)

		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(RIGHT*4 + UP*1).scale(sauce_scale)
		self.play(
			FadeOut(secret_sauce_encrypted),
			FadeOut(decrypt),
			secret_sauce_plaintext.animate.move_to(RIGHT*4 + UP*1.25)
		)
		self.wait(2)



class SymmetricProblem(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Symmetric Encryption", color=BLUE).move_to(UP*3)
		self.add(title)

		subtitle = Text("Uses the same key to encrypt and decrypt the data.", font_size=20).next_to(title, DOWN)
		self.add(subtitle)


		# Mum and dad are going to email each other
		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		self.play(Create(mum))
		self.wait(2)


		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(RIGHT*5.5 + DOWN)
		self.play(Create(dad))
		self.wait(2)


		# 1. Dad can't decrypt
		sauce_scale = 0.3		
		path = ArcBetweenPoints(LEFT*4.5, RIGHT*4.5, angle=-PI/4, color=GRAY)
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(LEFT*4.5).scale(sauce_scale)
		self.play(FadeIn(path), FadeIn(secret_sauce_encrypted))
		self.play(MoveAlongPath(secret_sauce_encrypted, path))
		self.wait(1)

		exclamation = Text("!").next_to(dad, UP)
		self.play(Indicate(exclamation))
		self.wait(2)

		self.play(FadeOut(secret_sauce_encrypted), FadeOut(exclamation))
		self.wait(1)


		# 2. Someone steals halfway
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().scale(sauce_scale)
		key_words = Text("secret_key", font_size=14)
		sauce_key = VGroup(secret_sauce_encrypted, key_words).arrange(DOWN).move_to(LEFT*4.5)
		path_2 = ArcBetweenPoints(LEFT*4.5, UP*0.5, angle=-PI/8, color=GRAY)

		self.play(FadeIn(sauce_key))
		self.wait(2)

		evil_guy = Human(RED, 0.8).human.scale(0.25).move_to(DOWN*7)
		self.play(MoveAlongPath(sauce_key, path_2), evil_guy.animate.shift(UP*6))
		self.wait(2)

		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(secret_sauce_encrypted.get_center()).scale(sauce_scale)
		self.play(key_words.animate.shift(UP*0.5))
		self.play(key_words.animate.shift(DOWN*0.5), ReplacementTransform(secret_sauce_encrypted, secret_sauce_plaintext))
		self.wait(1)
		self.play(FadeOut(key_words), evil_guy.animate.shift(DOWN*6), secret_sauce_plaintext.animate.shift(DOWN*6))
		
		x = Text("X", color=RED)
		self.play(SpinInFromNothing(x))

		self.wait(2)
		self.play(FadeOut(x))	

		

class Asymmetric(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		mum = Human(TEAL, 0.8).add_label("Mum", WHITE).human.scale(0.25).move_to(LEFT*5.5 + DOWN)
		self.add(mum)

		dad = Human(GREEN, 0.8).add_label("Dad", WHITE).human.scale(0.25).move_to(RIGHT*5.5 + DOWN)
		self.add(dad)


		title = Text("Asymmetric Encryption", color=BLUE).move_to(UP*3)
		self.add(title)

		subtitle = Text("Uses a public and private key pair - one encrypts and the other decrypts.", font_size=20).next_to(title, DOWN)
		self.add(subtitle)
		self.wait(5)


		# Show the public and private keys
		pub = Key(GOLD).get_key().scale(0.5)
		pub_text = Text("public key", font_size=24)
		pub_group = VGroup(pub, pub_text).arrange(DOWN).move_to(LEFT*2)
		self.play(Create(pub_group))

		priv = Key(LIGHT_BROWN).get_key().scale(0.5)
		priv_text = Text("private key", font_size=24)
		priv_group = VGroup(priv, priv_text).arrange(DOWN).move_to(RIGHT*2)
		self.play(Create(priv_group))
		self.wait(2)

		self.play(
			pub_group.animate.scale(0.5).move_to(dad.get_center()+DOWN+LEFT*0.7),
			priv_group.animate.scale(0.5).move_to(dad.get_center()+DOWN+RIGHT*0.7)
		)
		self.wait(2)


		# Encrypt with the public key
		sauce_scale = 0.3		
		path = ArcBetweenPoints(LEFT*4.5, RIGHT*4.5, angle=-PI/4, color=GRAY)
		secret_sauce = SecretSauce("encrypted").get_secret_sauce().move_to(LEFT*4.5).scale(sauce_scale)
		key_words = Text("secret_key", font_size=14)
		sauce_key = VGroup(secret_sauce, key_words).arrange(DOWN).move_to(LEFT*4.5)
		self.play(FadeIn(path), FadeIn(secret_sauce))
		self.wait(1)

		key_words_encrypted = Text("x?v%Oa2hF!", font_size=14).move_to(key_words.get_center())
		pub_copy = pub.copy()
		self.play(pub.animate.move_to(key_words_encrypted.get_right()))
		self.play(
			Transform(key_words, key_words_encrypted), 
			pub.animate.move_to(pub_copy.get_center())
		)
		self.wait(1)

		self.play(MoveAlongPath(sauce_key, path))
		self.wait(1)

		key_words_plain = Text("secret_key", font_size=14).move_to(key_words.get_center())
		priv_copy = priv.copy()
		self.play(priv.animate.move_to(key_words_plain.get_right()))
		self.play(
			Transform(key_words, key_words_plain), 
			priv.animate.move_to(priv_copy.get_center())
		)
		self.wait(2)


		secret_sauce_plain = SecretSauce("text").get_secret_sauce().move_to(secret_sauce.get_center()).scale(sauce_scale)
		key_copy = key_words.copy()
		self.play(key_words.animate.move_to(secret_sauce_plain.get_bottom()))
		self.play(
			Transform(secret_sauce, secret_sauce_plain), 
			key_words.animate.move_to(key_copy.get_center())
		)
		self.wait(2)


		self.play(FadeOut(mum), FadeOut(dad), FadeOut(path), FadeOut(pub_group), FadeOut(priv_group), FadeOut(sauce_key))
		self.wait(5)



class AccessControls(Scene):

	def construct(self):
		Text.set_default(font="Monospace")


		title = Text("Confidentiality", color=BLUE).move_to(UP*3)
		self.add(title)


		subtitle = Text("Protection of data from those who are not authorised to access it.", font_size=20).next_to(title, DOWN)
		self.add(subtitle)


		strong_auth = Text("Authentication and Authorisation", font_size=24, color=GOLD).move_to(UP*1.5)
		auth_def = Text("")
		self.play(Write(strong_auth))

		auth_def = Text("Authentication: Verifying the requestor is who they claim to be.", font_size=20).next_to(strong_auth, DOWN)
		self.add(auth_def)


		secret_sauce = SecretSauce("shapes").get_secret_sauce().move_to(LEFT*4 + DOWN).scale(0.5)
		uncle = Human(GOLD, 0.8).add_label("Uncle", WHITE).human.scale(0.25).move_to(RIGHT*10 + DOWN)
		password_screen = Text("Enter Password:", font_size=20)

		self.play(Create(secret_sauce), uncle.animate.shift(LEFT*6), Create(password_screen))
		self.wait(2)

		password = Text("****************", font_size=24).next_to(password_screen, DOWN)
		self.play(AddTextLetterByLetter(password))
		self.play(password_screen.animate.set_color(GREEN), password.animate.set_color(GREEN))
		self.wait(1)


		# Authorisation
		auth_def_2 = Text("Authorisation: Determining what actions the requestor is allowed to perform.", font_size=20).next_to(strong_auth, DOWN)
		self.play(Transform(auth_def, auth_def_2))


		role_table = VGroup(VGroup(Text("Person", weight=BOLD), Text("Role", weight=BOLD)).arrange(RIGHT, buff=1))
		brother_row = VGroup(Text("Brother").next_to(role_table[-1][0], DOWN), Text("Viewer").next_to(role_table[-1][1], DOWN))
		role_table.add(brother_row)
		uncle_row = VGroup(Text("Dad").next_to(role_table[-1][0], DOWN), Text("Editor").next_to(role_table[-1][1], DOWN))
		role_table.add(uncle_row)
		uncle_row = VGroup(Text("Uncle").next_to(role_table[-1][0], DOWN), Text("Editor").next_to(role_table[-1][1], DOWN))
		role_table.add(uncle_row)		
		uncle_row = VGroup(Text("Grandpa").next_to(role_table[-1][0], DOWN), Text("Owner").next_to(role_table[-1][1], DOWN))
		role_table.add(uncle_row)
		self.play(FadeIn(role_table.scale(0.35).move_to(DOWN*2)))
		self.wait(1)

		self.play(role_table[3][0].animate.set_color(GOLD), role_table[3][1].animate.set_color(GOLD))
		self.wait(1)


		self.play(secret_sauce.animate.move_to(uncle.get_center() + DOWN))
		self.play(uncle.animate.shift(RIGHT*6), secret_sauce.animate.shift(RIGHT*6))
		self.wait(2)