from manim import *
from QuickSort import QuickSort
import random


config.background_color = "#15131c"


class QuickSortDemo(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title_text = Text("Algorithm Walkthrough").shift(UP*3)
		self.play(Write(title_text))
		self.wait(2)

		elements = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		random.shuffle(elements)

		quick_sort = QuickSort(elements)
		scene_elements = quick_sort.create_scene_elements()
		self.play(Create(scene_elements))
		self.wait(2)

		# Get the pivot index in the middle
		pivot_index = (len(elements)-1)//2
		pivot_arrow = quick_sort.set_pivot(pivot_index)
		self.play(Create(pivot_arrow))

		pivot_text = VGroup(Text("pivot = ", font_size=20), 
			quick_sort.scene_elements[quick_sort.pivot_index].copy().scale(0.5)).arrange(RIGHT).next_to(pivot_arrow, DOWN)
		self.play(Write(pivot_text))
		self.wait(2)


		low_brace = BraceBetweenPoints(quick_sort.scene_elements[0].get_center(),
			quick_sort.scene_elements[pivot_index-1].get_center()).shift(DOWN*0.5)
		low_brace_text = Text("<= pivot value", font_size=20).next_to(low_brace, DOWN)
		self.play(Create(low_brace))
		self.play(Write(low_brace_text))
		self.wait(2)

		high_brace = BraceBetweenPoints(quick_sort.scene_elements[pivot_index+1].get_center(),
			quick_sort.scene_elements[len(quick_sort.scene_elements)-1].get_center()).shift(DOWN*0.5)
		high_brace_text = Text(">= pivot value", font_size=20).next_to(high_brace, DOWN)
		self.play(Create(high_brace))
		self.play(Write(high_brace_text))
		self.wait(2)


		# Swap the pivot to the end
		quick_sort.animate_swap(self, pivot_index, len(quick_sort.scene_elements)-1)

		self.play(
			pivot_text.animate.move_to(RIGHT*6),
			FadeOut(pivot_arrow),
			FadeOut(low_brace), FadeOut(low_brace_text),
			FadeOut(high_brace), FadeOut(high_brace_text)
		)

		self.play(quick_sort.scene_elements.animate.shift(UP*2))
		self.wait(2)


		# Create the arrows
		low_arrow = quick_sort.create_low_arrow(self, 0)
		high_arrow = quick_sort.create_high_arrow(self, len(quick_sort.scene_elements)-2)


		
