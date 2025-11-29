from manim import *
from entities import *
import hashlib

config.background_color = "#15131c"


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

		title_text = Text("Fundamental Cybersecurity Concepts").shift(UP*3)
		self.add(title_text)

		question_text = Text("The CIA Triad: Confidentiality, Integrity, Availability", 
			font_size=24,
			t2c={"Confidentiality": BLUE, "Integrity": PURPLE, "Availability": PINK}
		).shift(UP*2)
		self.add(question_text)


		confidentiality_bg = RoundedRectangle(
			width=6, height=2.5,
			fill_color="#00141a",
			fill_opacity=1,
			corner_radius=0.05
		).move_to(UP*0.25)
		self.add(confidentiality_bg)


		# Draw the plaintext secret sauce, key, and encryption scheme
		encryption = VGroup()

		sauce_scale = 0.6
		secret_sauce_plaintext = SecretSauce("text").get_secret_sauce().move_to(LEFT*4 + DOWN*0.5).scale(sauce_scale)
		encryption.add(secret_sauce_plaintext)

		key = Key(YELLOW).get_key().scale(0.35).move_to(LEFT*4 + DOWN*2.5)
		encryption.add(key)

		encryption_background = RoundedRectangle(
			width=4, height=2,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		encryption_text = Text("Encryption Scheme", font_size=24).move_to(encryption_background.get_center())
		encryption_scheme = VGroup(encryption_background, encryption_text).shift(DOWN + RIGHT*0.5)
		encryption.add(encryption_scheme)

		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(encryption_scheme.get_right()).scale(0.85).move_to(RIGHT*5 + DOWN)
		encryption.add(secret_sauce_encrypted)


		encryption.scale(0.45).move_to(confidentiality_bg.get_center())
		self.add(encryption)


		integrity_bg = RoundedRectangle(
			width=6, height=2.5,
			fill_color="#17001f",
			fill_opacity=1,
			corner_radius=0.05
		).move_to(DOWN*2.5 + RIGHT*3.125)
		self.add(integrity_bg)


		hashing = VGroup()

		secret_sauce = SecretSauce("tampered").get_secret_sauce().move_to(LEFT*5 + DOWN).scale(0.6)
		hashing.add(secret_sauce)


		hash_background = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=0.2,
			color=GRAY,
			fill_opacity=0.85
		)
		hash_text = Text("Hash Function", font_size=24).move_to(hash_background.get_center())
		hash_scheme = VGroup(hash_background, hash_text).shift(DOWN + LEFT*1.5)
		hashing.add(hash_scheme)


		# Store hash of original
		sha256_hash = hashlib.sha256()
		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n1 clove garlic"
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash = Text(sha256_hash.hexdigest()[0:9]).move_to(RIGHT*2).scale(0.7)
		hashing.add(sauce_hash)

		lock = Lock(GOLD).lock.scale(0.7).move_to(sauce_hash.get_center() + DOWN*0.5)
		hashing.add(lock)


		data_to_hash = "Secret Sauce\n2 tbsp mayonnaise\n2 tbsp ketchup\n1 tbsp mustard\n1 tsp paprika\n10 chillis"
		sha256_hash = hashlib.sha256()
		sha256_hash.update(data_to_hash.encode('utf-8'))
		sauce_hash_2 = Text(sha256_hash.hexdigest()[0:9], color=RED).move_to(RIGHT*2 + DOWN*2).scale(0.7)
		hashing.add(sauce_hash_2)


		hashing.scale(0.6).move_to(integrity_bg.get_center())
		self.add(hashing)

		


		availability_bg = RoundedRectangle(
			width=6, height=2.5,
			fill_color="#1f001a",
			fill_opacity=1,
			corner_radius=0.05
		).move_to(DOWN*2.5 + LEFT*3.125)
		self.add(availability_bg)


		availability = VGroup()


		screen = RoundedRectangle(height=2, width=3, fill_color=BLACK, stroke_color=GRAY, stroke_width=5, fill_opacity=0.8, corner_radius=0.1)
		close = Dot(radius=0.075, color=RED).move_to(screen.get_center() + UP*0.75 + RIGHT*1.25)
		computer = VGroup(screen, close).move_to(LEFT*2 + DOWN)
		secret_sauce = SecretSauce("shapes").get_secret_sauce().move_to(computer.get_center()).scale(0.3)
		
		availability.add(computer)


		computer_2 = computer.copy().move_to(RIGHT*2 + DOWN)
		secret_sauce_2 = secret_sauce.copy().move_to(computer_2.get_center())

		availability.add(computer_2, secret_sauce_2)


		load = Arc(radius=0.2, start_angle=0,
			angle=9*PI/5, stroke_width=4,
			color=WHITE
		).move_to(computer.get_center() + UP*1.5)
		load_2 = load.copy().move_to(computer_2.get_center() + UP*1.5)


		x = Text("X", color=RED).move_to(computer.get_center() + UP*1.5)
		text = Text("Data not available!", font_size=14, color=PURE_GREEN).move_to(computer.get_center())
		availability.add(x, text)


		availability.add(load_2)


		availability.scale(0.7).move_to(availability_bg.get_center())
		self.add(availability)	