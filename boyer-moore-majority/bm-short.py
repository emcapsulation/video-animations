from manim import *
from BMClass import Votes

config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class BMMobile(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        title_text = Text("Boyer Moore").shift(UP*2) 
        title_text2 = Text("Majority Vote").shift(UP*1.5) 
        title_text3 = Text("Algorithm").shift(UP*1) 
        title_group = VGroup(title_text, title_text2, title_text3)

        description = Text("\nDetect the majority element", font_size=24).shift(UP*0) 
        time_complexity = Text("\nTime complexity: O(n)", font_size=24).shift(DOWN*3) 
        time_complexity2 = Text("Space complexity: O(1)", font_size=24).shift(DOWN*3.5) 
        complexity_group = VGroup(time_complexity, time_complexity2)
        
        title_complexity = VGroup(title_group, description, complexity_group)
        title_complexity.scale(0.9)        
        
        self.play(Write(description), run_time=2)
        self.wait(1)

        v = Votes(11)
        order = [TEAL, TEAL, GOLD, MAROON, MAROON, TEAL, TEAL, TEAL, GOLD, TEAL, MAROON]
        v.create_votes(self, order, scale=0.9)
        self.wait(1)

        self.play(Write(time_complexity), Write(time_complexity2), run_time=2)
        self.wait(1)

        self.play(Write(title_text), Write(title_text2), Write(title_text3), run_time=2)
        self.wait(1)
        self.play(time_complexity[15:19].animate.set_color(GREEN),
            time_complexity2[16:20].animate.set_color(GREEN))
        self.play(
        	title_complexity.animate.shift(UP*2.5), 
        	description.animate.shift(UP*2.5),
        	complexity_group.animate.shift(UP*4.5),
        	v.get_votes().animate.shift(DOWN*2)
        )        

        v.animate_bm_mobile(self, order, 1)
