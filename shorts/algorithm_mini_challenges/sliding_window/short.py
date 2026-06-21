from manim import *

from shorts.algorithm_mini_challenges import *
from constants import *

config.background_color = DEFAULT_BACKGROUND

config.pixel_width = MOBILE_WIDTH
config.pixel_height = MOBILE_HEIGHT
config.frame_width = MOBILE_FRAME_WIDTH
config.frame_height = MOBILE_FRAME_HEIGHT

PASTEL_RED = "#ff8c90"
PASTEL_ORANGE = "#f5a442"
PASTEL_YELLOW = "#fff56e"
PASTEL_GREEN = "#96ffb2"



class SeatsArray:
    def __init__(self, scene, array):
        self.scene = scene
        self.array = array
        self.v_seats_array = self.init_array()

    def init_array(self):
        self.v_seat_values = self.init_seat_values()
        self.v_indexes = self.init_seat_indexes()

        values_only = self.v_seat_values[1:-1]
        for r in range(0, len(self.v_indexes)):
            self.v_indexes[r].next_to(values_only[r], UP, buff=0.25)

        return VGroup(self.v_seat_values, self.v_indexes)

    def init_seat_values(self):
        seat_vals = VGroup()

        open_bracket = Text("[", font_size=24)
        seat_vals.add(open_bracket)

        for i in range(0, len(self.array)):
            v_val = Text(str(self.array[i]), font_size=30, color=PASTEL_RED if self.array[i] == 1 else WHITE)
            seat_vals.add(v_val)

        close_bracket = Text("]", font_size=24)
        seat_vals.add(close_bracket)

        return seat_vals.arrange(RIGHT, buff=0.1)

    def init_seat_indexes(self):
        index_vals = VGroup()

        for i in range(0, len(self.array)):
            v_val = Text(str(i), font_size=12, color=GRAY)
            index_vals.add(v_val)

        return index_vals.arrange(RIGHT)

    def run_algorithm(self, k):
        # Index and size of minimum block
        index, minSize = -1, 100

        # Window start and num vacant seats
        wStart, wVacant = 0, 0;

        for wEnd in range(0, len(self.array)):
            wVacant += (self.array[wEnd] == 0);

            # Close window while condition is met
            while wVacant >= k and wStart <= wEnd:
                wSize = wEnd-wStart+1
                if wSize < minSize:
                    minSize, index = wSize, wStart
                wVacant -= (self.array[wStart] == 0)
                wStart += 1

        return index, minSize

    def get_i(self, i):
        return self.v_seats_array[0][i+1]



class DividerBox:
    def __init__(self, scene, sections):
        self.scene = scene
        self.node = self.create_box(sections)

    def create_box(self, sections):
        n = len(sections)

        box = RoundedRectangle(
            width=2.2*n, height=1.5,
            corner_radius=0.15
        )

        content_groups = VGroup()
        for section in sections:
            group = VGroup(
                Text(section["title"], font_size=24, color=section["colour"]), 
                Text(section["value"])
            ).arrange(DOWN, buff=0.15)

            content_groups.add(group)


        cell_width = box.width / n

        for i, group in enumerate(content_groups):
            x = box.get_left()[0] + cell_width*(i + 0.5)
            group.move_to([x, box.get_center()[1], 0])

        dividers = VGroup()
        for i in range(1, n):
            x = box.get_left()[0] + cell_width * i

            divider = Line(
                [x, box.get_top()[1], 0],
                [x, box.get_bottom()[1], 0]
            )

            dividers.add(divider)

        return VGroup(box, dividers, content_groups)

    def get_content_group(self, i):
        return self.node[2][i]

    def change_val(self, i, new_val):
        old_val = self.get_content_group(i)[1]
        return Transform(old_val, Text(str(new_val)).move_to(old_val.get_center()))




class SlidingWindowNaive(Scene):

    def construct(self):
        Text.set_default(font=MONOSPACE_FONT)


        # Premise

        sh = ShortHint(self, "You have a seat-booking system.")
        sh.create_hint()

        sa = SeatsArray(self, [1,1,0,1,1,1,0,0,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1])
        self.play(Create(sa.v_seats_array))

        sh.change_hint("The array shows the seats which are\nvacant (0) and taken (1).")
        self.wait(2)

        sh.change_hint("Find the smallest contiguous block\nwhich includes at least k empty seats.")
        self.wait(2)


        # Examples

        def make_example(k):
            example_text = Text(f"E.g. k = {k}", font_size=30, color=PASTEL_ORANGE).move_to(UP*3)
            self.play(AddTextLetterByLetter(example_text))
            self.wait(1)

            (index, minSize) = sa.run_algorithm(k)
            self.play(*[Indicate(sa.get_i(i), color=PASTEL_GREEN) for i in range(index, index+minSize)])

            brace = BraceBetweenPoints(sa.get_i(index).get_bottom(), sa.get_i(index+minSize-1).get_bottom(), direction=DOWN)
            brace_text = Text(str(minSize) + " seats", font_size=24).next_to(brace, DOWN)
            brace_group = VGroup(brace, brace_text)
            self.play(Create(brace_group))

            self.wait(2)

            self.play(FadeOut(brace_group), FadeOut(example_text))

        make_example(3)
        make_example(4)


        # Naive

        title = Text("Algorithm Mini Challenges #3", font_size=30, t2c={"#3": LIGHT_PINK}).move_to(UP*4.5)
        self.play(Write(title))
        self.wait(2)


        self.play(sa.v_seats_array.animate.shift(UP*2))


        def perform_naive(k):
            db = DividerBox(self, [{
                'title': "retIndex",
                'value': "-1",
                'colour': PASTEL_ORANGE
            }, {
                'title': "minSize",
                'value': "INF",
                'colour': GOLD_A
            }])
            db.node.shift(DOWN*2)
            self.play(Create(db.node))


            example_text = Text(f"E.g. k = {k}", font_size=30, color=PASTEL_ORANGE).next_to(title, DOWN)
            self.play(AddTextLetterByLetter(example_text))
            self.wait(1)

            arrow_i = Arrow(start=sa.v_seat_values.get_bottom()+DOWN*2, end=sa.v_seat_values.get_bottom()+DOWN, stroke_color=PASTEL_ORANGE)
            arrow_j = Arrow(start=sa.v_seat_values.get_bottom()+DOWN*2, end=sa.v_seat_values.get_bottom()+DOWN, stroke_color=PASTEL_YELLOW)

            min_size = 1000
            ret_index = -1

            seats_only = sa.v_seat_values[1:-1]
            for i in range(0, len(seats_only)):
                if i == 0:
                    self.play(FadeIn(arrow_i.move_to(seats_only[i].get_center()+DOWN)))
                else:
                    self.play(arrow_i.animate.move_to(seats_only[i].get_center()+DOWN))

                if sa.array[i] == 0:
                    db_cur = DividerBox(self, [{
                        'title': "curIndex",
                        'value': str(i),
                        'colour': PASTEL_ORANGE
                    }, {
                        'title': "curSize",
                        'value': str(0),
                        'colour': GOLD_A
                    }, {
                        'title': "numVacant",
                        'value': str(0),
                        'colour': PASTEL_YELLOW
                    }])
                    db_cur.node.next_to(db.node, DOWN)


                    j = i
                    arrow_j.move_to(seats_only[j].get_center()+DOWN)
                    self.play(FadeIn(arrow_j), FadeIn(db_cur.node))

                    empty_count = 0

                    while j < len(seats_only) and empty_count < k:
                        self.play(arrow_j.animate.move_to(seats_only[j].get_center()+DOWN))

                        anims = []
                        if sa.array[j] == 0:
                            empty_count += 1
                            anims.append(db_cur.change_val(2, empty_count))

                        anims.append(db_cur.change_val(1, j-i+1))
                        self.play(*anims)
                        j += 1

                    # Update min values
                    if empty_count == k and j-i < min_size:
                        min_size=j-i
                        self.play(
                            *[Indicate(sa.get_i(l), color=PASTEL_GREEN) for l in range(i, i+j-i)], 
                            Circumscribe(db_cur.get_content_group(1))
                        )
                        self.play(
                            db.change_val(0, i),
                            db.change_val(1, min_size)
                        )
                    elif empty_count == k and not (j-1 < min_size):
                        self.play(
                            *[Indicate(sa.get_i(l), color=PASTEL_RED) for l in range(i, i+j-i)], 
                        )


                    self.play(FadeOut(arrow_j), FadeOut(db_cur.node))

            self.wait(2)

            self.play(Transform(title, Text("O(n^2)", color=PASTEL_RED).move_to(title.get_center())))
            self.wait(2)

            self.play(FadeOut(arrow_i), FadeOut(example_text), FadeOut(db.node))


        perform_naive(4)       


class SlidingWindow(Scene):

    def construct(self):
        Text.set_default(font=MONOSPACE_FONT)

        # Sliding window
        sh = ShortHint(self, "Sliding Window", font_size=40)
        sh.create_hint()

        t1 = Text("Window: Subarray which we track the state of.", font_size=20, t2c={'Window:': PASTEL_ORANGE})
        t2 = Text("* Open the window (wEnd++) while wVacant < k", font_size=20, t2c={'wVacant < k': PASTEL_RED})
        t3 = Text("* Close the window (wStart++) while wVacant >= k", font_size=20, t2c={'wVacant >= k': PASTEL_GREEN})
        window_definition = VGroup(t1, t2, t3).arrange(DOWN).move_to(UP*4.5)
        self.play(Create(window_definition))
        self.wait(2)


        retIndex = -1
        minSize = 1000

        db = DividerBox(self, [{
            'title': "retIndex",
            'value': str(retIndex),
            'colour': PASTEL_ORANGE
        }, {
            'title': "minSize",
            'value': "INF",
            'colour': GOLD_A
        }])
        db.node.shift(DOWN*3.5)

        wStart = 0
        wEnd = 0
        wVacant = 0

        db_cur = DividerBox(self, [{
            'title': "wStart",
            'value': str(wStart),
            'colour': PASTEL_ORANGE
        }, {
            'title': "wEnd",
            'value': str(wEnd),
            'colour': GOLD_A
        }, {
            'title': "wVacant",
            'value': str(wVacant),
            'colour': PASTEL_YELLOW
        }])
        db_cur.node.next_to(db.node, DOWN)

        self.play(Create(db_cur.node))
        self.wait(2)

        self.play(Create(db.node))
        self.wait(2)


        sa = SeatsArray(self, [1,1,0,1,1,1,0,0,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1])
        self.play(Create(sa.v_seats_array.shift(DOWN)))

        k = 4
        example_text = Text(f"k = {k}", font_size=30, color=PASTEL_ORANGE).next_to(window_definition, DOWN)


        def make_window_box(i, j, colour=PASTEL_YELLOW):
            return Rectangle(
                height=1, 
                width=(sa.get_i(j).get_right()[0] - sa.get_i(i).get_left()[0]),
                fill_color=colour,
                fill_opacity=0.1,
                stroke_width=0.2
            ).move_to(sa.v_seats_array.get_center()).align_to(sa.get_i(i), LEFT)


        window = make_window_box(wStart, wEnd)
        self.play(Create(window))        
        self.wait(2)


        def make_algo_text(wVacant):
            if wVacant >= k:
                return Text(f"wVacant >= k: Close window (wStart++)", font_size=22, t2c={"wVacant >= k": PASTEL_GREEN, "wStart++": PASTEL_ORANGE}).next_to(sa.v_seats_array, DOWN)
            else:
                return Text(f"wVacant < k: Open window (wEnd++)", font_size=22, t2c={"wVacant < k": PASTEL_RED, "wEnd++": GOLD_A}).next_to(sa.v_seats_array, DOWN)
        algo_text = make_algo_text(wVacant)


        def make_wsize_text(wStart, wEnd):
            return Text(f"wSize = wEnd-wStart+1 = {wEnd-wStart+1}", font_size=22, t2c={"wEnd": GOLD_A, "wStart": PASTEL_ORANGE}).next_to(algo_text, DOWN)
        w_size_text = make_wsize_text(wStart, wEnd)
        w_size_visible = False


        delta_pos = db_cur.get_content_group(2).get_right() + DOWN*0.25
        plus_one = Text("+1", font_size=16, color=PASTEL_GREEN).move_to(delta_pos)
        minus_one = Text("-1", font_size=16, color=PASTEL_RED).move_to(delta_pos)


        for wEnd in range(0, len(sa.array)):
            if w_size_visible:
                self.play(FadeOut(w_size_text))
                w_size_visible = False

            self.play(Transform(algo_text, make_algo_text(wVacant)))
            self.play(
                Transform(window, make_window_box(wStart, wEnd)),
                db_cur.change_val(1, wEnd)
            ) 

            if sa.array[wEnd] == 0:
                wVacant += 1
                self.play(
                    FadeIn(plus_one.move_to(delta_pos)),
                    plus_one.animate.shift(UP*0.25),
                    db_cur.change_val(2, wVacant)
                )        
                self.remove(plus_one)

            # Close window while condition is met
            while wVacant >= k and wStart <= wEnd:                
                self.play(Transform(algo_text, make_algo_text(wVacant)))

                wSize = wEnd-wStart+1
                if w_size_visible:
                    self.play(Transform(w_size_text, make_wsize_text(wStart, wEnd)))
                else:
                    w_size_text = make_wsize_text(wStart, wEnd)
                    self.play(FadeIn(w_size_text))
                    w_size_visible = True

                if wSize < minSize:
                    minSize = wSize
                    retIndex = wStart

                    self.play(Indicate(window, color=PASTEL_GREEN))
                    self.play(
                        db.change_val(0, retIndex),
                        db.change_val(1, minSize)
                    )         
                
                self.play(Transform(algo_text, make_algo_text(wVacant)))

                wStart += 1
                self.play(
                    Transform(window, make_window_box(wStart, wEnd)),
                    db_cur.change_val(0, wStart)
                )

                if sa.array[wStart-1] == 0:
                    wVacant -= 1;
                    self.play(
                        FadeIn(minus_one.move_to(delta_pos)),
                        minus_one.animate.shift(UP*0.25),
                        db_cur.change_val(2, wVacant)
                    )        
                    self.remove(minus_one)


        self.play(FadeOut(algo_text))
        self.wait(2)

        ans_box = make_window_box(retIndex, retIndex+minSize-1, colour=PASTEL_GREEN)
        self.play(Transform(window, ans_box), Indicate(db.node, color=PASTEL_GREEN))
        self.wait(2)

        self.play(Transform(window_definition, Text("O(n)", color=PASTEL_GREEN).move_to(window_definition.get_center())))
        self.wait(2)