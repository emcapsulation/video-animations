from manim import *
from DNFClass import Sorter

config.background_color = "#15131c"
VERM_RED = "#AE1C28"
COB_BLUE = "#21468B"

config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


def create_psuedocode(scene):
    code_rect = RoundedRectangle(width=7, height=4.5, fill_color=BLACK, fill_opacity=1, stroke_width=0, corner_radius=0.3)
    code = MarkupText(f"""<span fgcolor="{RED}">low</span> = 0
<span fgcolor="{GREEN}">mid</span> = 0
<span fgcolor="{BLUE}">high</span> = length of nums - 1

while <span fgcolor="{GREEN}">mid</span> &lt;= <span fgcolor="{BLUE}">high</span>:
    if nums[<span fgcolor="{GREEN}">mid</span>] == middle element:
        increment <span fgcolor="{GREEN}">mid</span>

    else if nums[<span fgcolor="{GREEN}">mid</span>] &gt; middle element:
        swap values at <span fgcolor="{GREEN}">mid</span> and <span fgcolor="{BLUE}">high</span>
        decrement <span fgcolor="{BLUE}">high</span>

    else if nums[<span fgcolor="{GREEN}">mid</span>] &lt; middle element:
        swap values at <span fgcolor="{RED}">low</span> and <span fgcolor="{GREEN}">mid</span>
        increment <span fgcolor="{RED}">low</span>, increment <span fgcolor="{GREEN}">mid</span>""", font_size=16, font="Monospace").move_to(code_rect.get_center()) 

    pseudocode = VGroup(code_rect, code).scale(0.8).move_to(DOWN*4)
    scene.play(Create(pseudocode), run_time=2)
    scene.wait(3)   

    return pseudocode


class DNFMobile(Scene):
    def construct(self):
        Text.set_default(font="Monospace")


        l = [5, 2, 12, 7, 11, 4, 1, 3, 9, 6, 10, 8]
        s = Sorter(l, ORIGIN, len(l))
        s.create_list(self, scale=0.6)
        self.wait(3)

        self.play(Transform(s.scene_elems, s.scene_sorted_elems.scale(0.6)))
        time_complexity = Text("Time complexity: O(nlog(n))", font_size=24).shift(UP)       
        self.play(Write(time_complexity), run_time=2)

        self.wait(3)
        s.fade_out(self)

        s = Sorter([3, 1, 2, 2, 1, 3, 2, 1, 1, 3, 3, 2], ORIGIN, 3, colours=[VERM_RED, WHITE, COB_BLUE], type="nums")
        s.create_list(self, scale=0.6)
        self.wait(3)

        dot1 = Dot(color=s.colours[0], radius=0.5).move_to(DOWN*2+LEFT*2)
        dot2 = Dot(color=s.colours[1], radius=0.5).move_to(DOWN*2)
        dot3 = Dot(color=s.colours[2], radius=0.5).move_to(DOWN*2+RIGHT*2)
        dots = VGroup(dot1, dot2, dot3)

        self.play(Create(dots))
        self.wait(3)        

        time_complexity_2 = Text("Time complexity: O(n)", font_size=24).shift(UP) 
        self.play(Transform(s.scene_elems, s.scene_sorted_elems.scale(0.6)), 
            Transform(time_complexity, time_complexity_2))
        self.play(time_complexity[20:].animate.set_color(GREEN))
        self.wait(3)        

        title_text1 = Text("Dutch National").shift(UP*5)
        title_text2 = Text("Flag Problem").shift(UP*4.25)
        self.play(Write(title_text1), Write(title_text2))

        time_complexity1 = Text("Time complexity: O(n)", font_size=24).shift(UP*3.5)   
        time_complexity2 = Text("Space complexity: O(1)", font_size=24).shift(UP*3)  
        time_comp_group = VGroup(time_complexity1, time_complexity2)         
        self.play(Transform(time_complexity, time_comp_group), run_time=2)
        self.play(time_complexity1[15:19].animate.set_color(GREEN),
            time_complexity2[16:20].animate.set_color(GREEN))
        self.wait(3)

        dnf = VGroup()
        red = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=VERM_RED, fill_opacity=1)
        white = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=WHITE, fill_opacity=1).next_to(red.get_center(), DOWN*4/3)
        blue = Rectangle(width=3, height=2/3, stroke_width=0, fill_color=COB_BLUE, fill_opacity=1).next_to(white.get_center(), DOWN*4/3)

        dnf.add(red, white, blue)
        dnf.move_to(DOWN*2)

        s2 = Sorter([3, 1, 2, 2, 1, 3, 2, 1, 1, 3, 3, 2], ORIGIN, 3, colours=[VERM_RED, WHITE, COB_BLUE], type="balls")
        self.play(Transform(dots, dnf), Transform(s.scene_elems, s2.scene_elems.scale(0.5)))

        s.perform_algorithm(self, show_arrow=False, run_time=0.3)      

        self.wait(3)
        self.play(FadeOut(dots), FadeOut(time_complexity), FadeOut(time_complexity1), FadeOut(time_complexity2), FadeOut(s.scene_elems))

        low_arrow = Arrow(start=DOWN, end=ORIGIN, color=RED, stroke_width=8).shift(UP*3 + LEFT*5)
        low_text = Text("Low - End of the low group", font_size=24).next_to(low_arrow, RIGHT, buff=1)
        mid_arrow = Arrow(start=DOWN, end=ORIGIN, color=GREEN, stroke_width=8).shift(UP*2 + LEFT*5)
        mid_text = Text("Mid - End of the middle group", font_size=24).next_to(mid_arrow, RIGHT, buff=1)
        high_arrow = Arrow(start=DOWN, end=ORIGIN, color=BLUE, stroke_width=8).shift(UP + LEFT*5)
        high_text = Text("High - Start of the high group", font_size=24).next_to(high_arrow, RIGHT, buff=1)

        arrow_text = VGroup(low_arrow, low_text, mid_arrow, mid_text, high_arrow, high_text).scale(0.7).move_to(ORIGIN + UP*2)

        self.play(Create(low_arrow), Write(low_text))
        self.wait(1)
        self.play(Create(mid_arrow), Write(mid_text))
        self.wait(1)
        self.play(Create(high_arrow), Write(high_text))        

        create_psuedocode(self)
        self.wait(3)

        s = Sorter([2, 3, 1, 2, 3, 3, 2, 1, 1, 3, 2, 1], DOWN*0.5, 3, colours=[VERM_RED, WHITE, COB_BLUE], type="nums")
        s.create_list(self, scale=0.6)
        s.perform_algorithm(self)

        self.wait(3)
