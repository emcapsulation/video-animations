from manim import *
from entities import *
from polynomials import *

import random
import math


config.background_color = "#120a01"


class UncleCounterArgument(Scene):
	
	def construct(self):
		Text.set_default(font="Monospace")

		# Draw in the encrypted recipe, uncle and speech bubble
		secret_sauce_encrypted = SecretSauce("encrypted").get_secret_sauce().move_to(ORIGIN + DOWN).scale(0.6*1.5)
		self.add(secret_sauce_encrypted)

		uncle = Human(GOLD, 0.8).add_label("Uncle", WHITE).get_human().scale(0.4).move_to(RIGHT*5+UP*2.5)
		self.play(Create(uncle))

		speech_bubble = SpeechBubble([GOLD, GOLD_B], 9, 1.5).get_speech_bubble().move_to(LEFT*1.75+UP*2.5)
		self.play(Create(speech_bubble))

		speech1 = Text("Then how are WE supposed to read it?", font_size=20).move_to(speech_bubble.get_center())
		self.play(Write(speech1))		
		self.wait(2)


		# He is confused about how to make the burger
		burger = BurgerStore.make_burger().move_to(RIGHT*3 + DOWN)
		q_mark = Text("?", color=GOLD).move_to(burger.get_center())

		self.play(secret_sauce_encrypted.animate.shift(LEFT*3), Create(burger))
		self.play(Transform(burger, q_mark))
		self.wait(2)

		self.play(
			FadeOut(uncle), 
			FadeOut(speech_bubble), 
			FadeOut(q_mark), 
			FadeOut(speech1), 
			FadeOut(burger), 
			secret_sauce_encrypted.animate.move_to(ORIGIN).scale(0.6)
		)