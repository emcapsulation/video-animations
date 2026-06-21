from manim import *

class SpeechBubble:
	def __init__(self, colour, width, height):
		self.speech_bubble = RoundedRectangle(
			width=width, height=height, 
			fill_color=colour, stroke_color=colour,
			corner_radius=0.2, fill_opacity=0.1
		)

	def get_speech_bubble(self):
		return self.speech_bubble