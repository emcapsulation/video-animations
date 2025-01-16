from manim import *
from LLClass import ListNode, LinkedList
import math


config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8

P_RAD = 0.1
P1_COL = PINK
P2_COL = GREEN
NODE_COL = BLUE



class FloydMobile(Scene):
    def construct(self):
        Text.set_default(font="Consolas")

        title_text = Text("Floyd's Cycle\nFinding Algorithm").shift(UP*3)    
        description = Text("Detects a cycle in a linked list", font_size=24).shift(UP*2) 
        time_complexity = Text("Time complexity: O(n)\nSpace complexity: O(1)", font_size=24).shift(UP*2) 
        
        title_complexity = VGroup(title_text, time_complexity)
        title_complexity.scale(0.75)

        self.play(Write(title_text))
        self.play(Write(time_complexity), run_time=2)
        self.play(time_complexity[15:19].animate.set_color(GREEN),
            time_complexity[35:40].animate.set_color(GREEN))

        pointer = Dot(color=P1_COL, radius=P_RAD).shift(UP*1 + LEFT*3.5)
        slow_text = Text("Slow pointer (tortoise) \n - Moves one node at a time", font_size=24).shift(UP*1)        

        pointer2 = Dot(color=P2_COL, radius=P_RAD).shift(LEFT*3.5)
        fast_text = Text("Fast pointer (hare) \n - Moves two nodes at a time", font_size=24)        

        p_group = VGroup(pointer, slow_text, pointer2, fast_text)
        p_group.scale(0.75)

        self.play(FadeIn(pointer), Write(slow_text))
        self.wait(3)
        self.play(FadeIn(pointer2), Write(fast_text))
        # self.wait(3)
        # self.play(FadeOut(title_text, time_complexity),
        #     p_group.animate.shift(UP*3))
        self.wait(3)

        LL = LinkedList(True)
        LL.create_large_list()
        LL.ll_group.shift(DOWN*1).scale(0.5)
        LL.draw_linked_list(self, run_time=0.05)
        LL.floyd_animation(self, run_time_mult=0.4)
        
        start_cycle = Text("Start of the cycle: 10", font_size=24).shift(DOWN*2)
        self.play(Write(start_cycle))
        self.wait(3)
