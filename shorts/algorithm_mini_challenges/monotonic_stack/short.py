from manim import *

from shorts.algorithm_mini_challenges import *
from constants import *
from utils import generate_colours

config.background_color = DEFAULT_BACKGROUND

config.pixel_width = MOBILE_WIDTH
config.pixel_height = MOBILE_HEIGHT
config.frame_width = MOBILE_FRAME_WIDTH
config.frame_height = MOBILE_FRAME_HEIGHT



class HeightsArray:
    def __init__(self, scene, array):
        self.scene = scene
        self.array = array
        self.colours = generate_colours(self.array, in_order=True)
        self.v_height_array = self.init_array()
        self.v_ans_array = self.init_ans_array()

    def init_array(self):
        self.v_height_rects = self.init_height_rects()
        self.v_height_values = self.init_height_values()
        self.v_indexes = self.init_height_indexes()

        values_only = self.v_height_values[1:-1]

        for r in range(0, len(self.v_height_rects)):
            self.v_height_rects[r].next_to(values_only[r], UP, buff=0.25)
            self.v_indexes[r].next_to(values_only[r], DOWN, buff=0.25)

        baseline = self.v_height_rects[0].get_bottom()[1]
        for rect in self.v_height_rects:
            rect.align_to(self.v_height_rects[0], DOWN)

        return VGroup(self.v_height_rects, self.v_height_values, self.v_indexes)

    def init_ans_array(self):
        ans_vals = VGroup()

        open_bracket = Text("[", font_size=24)
        ans_vals.add(open_bracket)

        for i in range(0, len(self.array)):
            v_val = Text(str(0), font_size=24, color=DEFAULT_BACKGROUND)
            ans_vals.add(v_val)

        close_bracket = Text("]", font_size=24)
        ans_vals.add(close_bracket)

        for i in range(0, len(ans_vals)):
            ans_vals[i].next_to(self.v_height_values[i], DOWN, buff=1)

        return ans_vals

    def reset_ans_array(self):
        anims = []
        for i in range(1, len(self.v_ans_array)-1):
            anims.append(Transform(self.v_ans_array[i], 
                Text("0", color=DEFAULT_BACKGROUND).move_to(self.v_ans_array[i].get_center())))
        self.scene.play(*anims)

    def init_height_rects(self):
        min_height, max_height = min(self.array), max(self.array)

        height_rects = VGroup()

        for i in range(0, len(self.array)):
            v_rect = Rectangle(
                width=0.25, height=((self.array[i]-min_height)/(max_height-min_height))+1,
                fill_color=self.colours[i], fill_opacity=0.25
            )
            height_rects.add(v_rect)

        return height_rects.arrange(RIGHT)

    def init_height_values(self):
        height_vals = VGroup()

        open_bracket = Text("[", font_size=24)
        height_vals.add(open_bracket)

        for i in range(0, len(self.array)):
            v_val = Text(str(self.array[i]), font_size=24, color=self.colours[i])
            height_vals.add(v_val)

        close_bracket = Text("]", font_size=24)
        height_vals.add(close_bracket)

        return height_vals.arrange(RIGHT)

    def init_height_indexes(self):
        index_vals = VGroup()

        for i in range(0, len(self.array)):
            v_val = Text(str(i), font_size=16)
            index_vals.add(v_val)

        return index_vals.arrange(RIGHT)




class MonotonicStack(Scene):

    def construct(self):
        Text.set_default(font=MONOSPACE_FONT)


        # Premise

        sh = ShortHint(self, "You are organising seats for a cinema.")
        sh.create_hint()

        ha = HeightsArray(self, [182, 167, 152, 176, 182, 160, 172])
        self.play(Create(ha.v_height_array))

        sh.change_hint("The array shows the heights of people in\neach row.\ni=0 is the row furthest from the screen.")
        self.wait(2)

        sh.change_hint("How many rows ahead can each person see\nbefore their view is blocked by someone\nof equal height or taller?")
        self.wait(2)



        # Examples

        def get_compare_line(rect_short, rect_tall):
            start = rect_short.get_top()
            end = [rect_tall.get_left()[0], start[1], 0]
            height_line = Line(start=start, end=end)
            return height_line


        example_1 = get_compare_line(ha.v_height_rects[0], ha.v_height_rects[4])
        self.play(Create(example_1))
        self.wait(1)
        self.play(FadeOut(example_1))

        example_1 = get_compare_line(ha.v_height_rects[1], ha.v_height_rects[3])
        self.play(Create(example_1))
        self.wait(1)
        self.play(FadeOut(example_1))



        # Naive

        title = Text("Algorithm Mini Challenges #2", font_size=30, t2c={"#2": LIGHT_PINK}).move_to(UP*4.5)
        self.play(Write(title))
        self.wait(2)

        self.play(FadeIn(ha.v_ans_array.shift(DOWN)))

        arrow_i = Arrow(start=ha.v_height_values.get_bottom()+DOWN*2, end=ha.v_height_values.get_bottom()+DOWN, stroke_color=ORANGE)
        arrow_j = Arrow(start=ha.v_height_values.get_bottom()+DOWN*2, end=ha.v_height_values.get_bottom()+DOWN, stroke_color=PINK)

        heights_only = ha.v_height_values[1:-1]
        for i in range(0, len(heights_only)):
            if i == 0:
                self.play(FadeIn(arrow_i.move_to(heights_only[i].get_center()+DOWN)))
            else:
                self.play(arrow_i.animate.move_to(heights_only[i].get_center()+DOWN))

            j = i+1
            arrow_j.move_to(ha.v_height_values[j+1].get_center()+DOWN)
            self.play(FadeIn(arrow_j))
            while j < len(heights_only) and ha.array[j] < ha.array[i]:                
                j += 1
                self.play(arrow_j.animate.move_to(ha.v_height_values[j+1].get_center()+DOWN))

            self.play(Transform(ha.v_ans_array[i+1], Text(str(j-i), font_size=24).move_to(ha.v_ans_array[i+1].get_center())))
            self.play(FadeOut(arrow_j))

        self.wait(2)

        self.play(Transform(title, Text("O(n^2)", color=RED).move_to(title.get_center())))
        self.wait(2)


        # Monotonic stack

        sh.change_hint("Monotonic Stack", font_size=40)
        t1 = Text("Stack data structure (last-in first-out)", font_size=20)
        t2 = Text("Values are increasing or decreasing", font_size=20)
        monotonic_stack_definition = VGroup(t1, t2).arrange(DOWN).move_to(title.get_center())
        self.play(Transform(title, monotonic_stack_definition))
        self.wait(2)

        self.play(FadeOut(arrow_i))
        ha.reset_ans_array()
        self.wait(2)

        sh.change_hint("Store indexes of people in the stack\nwhose heights strictly decrease\nfrom bottom of the stack to top.")
        self.play(FadeOut(title))
        self.wait(2)


        top_text = Text("Bottom", font_size=24)
        top_arrow = Arrow(start=LEFT*2, end=LEFT)
        top = VGroup(top_text, top_arrow).arrange(DOWN).move_to(LEFT*3 + DOWN*5)
        self.play(Create(top))
        self.wait(2)


        # Monotonic stack implementation

        st = []
        v_st = VGroup(top)

        arrow_i = Arrow(start=ha.v_height_values.get_bottom()+DOWN*2, end=ha.v_height_values.get_bottom()+DOWN, stroke_color=ORANGE)

        for i in range(1, len(ha.v_height_values)-1):
            if i == 1:
                self.play(FadeIn(arrow_i.move_to(ha.v_height_values[i].get_center()+DOWN)))
            else:
                self.play(arrow_i.animate.move_to(ha.v_height_values[i].get_center()+DOWN))

            height_bundle = VGroup(ha.v_height_rects[i-1].copy(), ha.v_indexes[i-1].copy()).arrange(DOWN).next_to(
                v_st[-1], RIGHT, buff=2).align_to(v_st[-1], DOWN)
            self.play(ReplacementTransform(ha.v_height_rects[i-1].copy(), height_bundle))
            self.wait(0.5)

            while len(st) != 0 and ha.array[i-1] >= ha.array[st[-1]]:
                height_line = get_compare_line(v_st[-1], height_bundle)

                self.play(Create(height_line))
                self.wait(0.5)

                subtraction = Text(str(i-1) + "-" + str(st[-1]), font_size=20).move_to(DOWN*6)
                self.play(Write(subtraction))

                self.play(Transform(ha.v_ans_array[st[-1]+1], Text(str(i-1-st[-1]), font_size=24).move_to(ha.v_ans_array[st[-1]+1].get_center())))
                self.wait(0.5)

                st.pop()
                self.play(FadeOut(v_st[-1]), FadeOut(height_line), FadeOut(subtraction))
                v_st.remove(v_st[-1])
                self.wait(0.5)

            st.append(i-1)

            self.play(height_bundle.animate.next_to(v_st[-1], RIGHT, buff=0.5).align_to(v_st[-1], DOWN))
            v_st.add(height_bundle)
            self.wait(1)


        # Clean up last ones

        self.play(arrow_i.animate.shift(RIGHT))
        self.wait(1)

        i = len(ha.array)
        while len(st) != 0:
            subtraction = Text(str(i) + "-" + str(st[-1]), font_size=20).move_to(DOWN*6)
            self.play(Write(subtraction))

            self.play(Transform(ha.v_ans_array[st[-1]+1], Text(str(i-st[-1]), font_size=24).move_to(ha.v_ans_array[st[-1]+1].get_center())))
            self.wait(0.5)

            st.pop()
            self.play(FadeOut(v_st[-1]), FadeOut(subtraction))
            v_st.remove(v_st[-1])
            self.wait(0.5)

        self.wait(2)

