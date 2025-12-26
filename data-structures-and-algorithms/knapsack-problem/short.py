from manim import *
from items import *

config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


VALUE_COLOUR = GOLD
ITEM_WEIGHT_COLOUR = ORANGE
WEIGHT_LIMIT_COLOUR = PINK
MAX_VALUE_COLOUR = GOLD


class KnapsackMobile(Scene):
    def construct(self):
        Text.set_default(font="Monospace")


        # Create the suitcase
        suitcase = Item("suitcase", None, None).item.scale(0.8)
        suitcase_text = Text("Suitcase", font_size=24).next_to(suitcase, DOWN)

        self.play(Create(suitcase))
        self.play(Write(suitcase_text))
        self.wait(2)

        suitcase_weight = Text("W = 5kg", font_size=24, color=WEIGHT_LIMIT_COLOUR).next_to(suitcase_text, DOWN)
        self.play(Write(suitcase_weight))
        self.wait(2)
        suitcase_group = VGroup(suitcase, suitcase_text, suitcase_weight)


        # Create the items
        items, item_texts, value_texts = VGroup(), VGroup(), VGroup()
        item_list = [
            Item("camera", 25, 2),
            Item("pen", 10, 1),
            Item("sneakers", 40, 3),
            Item("toothbrush", 20, 1),
            Item("headphones", 45, 4)
        ]
        item_positions = [DOWN*3.5+LEFT*2, DOWN*5.5+LEFT, DOWN*5.5+RIGHT, DOWN*3.5, DOWN*3.5+RIGHT*2]


        for i in range(0, len(item_list)):
            item_list[i].item.move_to(item_positions[i]).scale(0.5)
            items.add(item_list[i].item)


        # Add a weight and value to each item
        for i in range(0, len(item_list)):
            item_text = Text(f"w = {item_list[i].weight}kg", font_size=18, color=ITEM_WEIGHT_COLOUR).next_to(items[i], DOWN)
            item_texts.add(item_text)
            self.play(Create(items[i]), Write(item_texts[i]))

            value_text = Text(f"v = {item_list[i].value}", font_size=18, color=VALUE_COLOUR).next_to(item_texts[i], DOWN)
            value_texts.add(value_text)
        self.wait(2)

        for i in range(0, len(item_list)):
            self.play(Write(value_texts[i]))
        self.wait(2)


        problem_1 = Text("Which items should you pack so that the final\nsuitcase contains the maximum value possible,\nwithout exceeding the weight limit of 5kg?", 
            font_size=18, t2c={"value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).move_to(UP*3)
        
        self.play(Write(problem_1))
        self.wait(5)


        title_text = Text("0/1 Knapsack").move_to(UP*3)
        title_text2 = Text("Problem").shift(UP*2.5) 
        title_group = VGroup(title_text, title_text2)
        self.play(ReplacementTransform(problem_1, title_group))
        self.play(
            title_group.animate.shift(UP*2.5), 
            FadeOut(suitcase_group), 
            FadeOut(items),
            FadeOut(item_texts),
            FadeOut(value_texts))
        self.wait(2)

        description = Text("Find the maximum total value you can pack\nwithout exceeding the weight limit.", 
            font_size=18, t2c={"value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).next_to(title_group, DOWN)
        time_complexity = Text("Time complexity: O(nW)", font_size=24)
        time_complexity2 = Text("Space complexity: O(nW)", font_size=24)
        complexity_group = VGroup(time_complexity, time_complexity2).arrange(DOWN).next_to(description, DOWN)

        self.play(Write(description), run_time=2)
        self.play(Write(time_complexity), Write(time_complexity2), run_time=2)
        self.play(time_complexity[15:20].animate.set_color(GREEN),
            time_complexity2[16:21].animate.set_color(GREEN))
        self.wait(2)


        # Add all the items
        item_list = [
            Item("dot", 0, 0),
            Item("pen", 10, 1),
            Item("camera", 25, 2),          
            Item("sneakers", 40, 3),
            Item("toothbrush", 20, 1),
            Item("headphones", 45, 4)
        ]

        item_numbers = ["#"]
        weights = ["w"]
        values = ["v"]
        objects = [Dot(radius=0.8)] 

        for i in range(0, len(item_list)):
            item_numbers.append(i)
            weights.append(item_list[i].weight)
            values.append(item_list[i].value)
            objects.append(item_list[i].item)


        table_ul = LEFT*3
        table = VGroup()

        for i in range(0, len(objects)):
            RT = 0.1

            item_number = Text(str(item_numbers[i]), font_size=24).move_to(table_ul + DOWN*i + RIGHT*0)
            self.play(Write(item_number), run_time=RT)

            obj = objects[i].move_to(table_ul + DOWN*i + RIGHT*0.5).scale(0.2)
            self.play(Create(obj), run_time=RT)

            if i == 0:
                colour = WHITE
            else:
                colour = ITEM_WEIGHT_COLOUR         
            weight = Text(str(weights[i]), font_size=24, color=colour).move_to(table_ul + DOWN*i + RIGHT*1)
            self.play(Write(weight), run_time=RT)           

            if i == 0:
                colour = WHITE
            else:
                colour = VALUE_COLOUR   
            value = Text(str(values[i]), font_size=24, color=colour).move_to(table_ul + DOWN*i + RIGHT*1.5)
            self.play(Write(value), run_time=RT)

            table.add(
                VGroup(
                    item_number,
                    obj,
                    weight,
                    value
                )
            )

        self.add(table)
        

        for weight in range(0, 6):
            weight_text = Text(f"{weight}", font_size=24).move_to(table_ul + RIGHT*(weight+3)*0.75)
            self.play(Write(weight_text), run_time=RT)
            table[0].add(weight_text)

        # Add the weight heading
        w = Text("W", color=PINK, font_size=24).move_to(table_ul + UP*0.75 + RIGHT*3*0.75)
        self.play(Write(w))
        self.wait(2)


        cell_desc = Text("dp[i][j] = The best value we can pack into a bag\nof capacity j, considering the first i items.", 
            font_size=18, t2c={"value": VALUE_COLOUR, "weight": WEIGHT_LIMIT_COLOUR}).move_to(complexity_group.get_center()+DOWN*2)
        self.play(Write(cell_desc))
        self.wait(2)


        # Highlight the zero item
        item_rect = Rectangle(
            width=2.25, height=0.75
        ).move_to(table.get_center()+UP*2+LEFT*2.25)
        self.play(Create(item_rect))
        self.wait(2)


        # Value of zero item is 0
        for cur_weight in range(0, 6):
            zero_val = Text("0", font_size=24).move_to(
                table[1][cur_weight+3].get_center()+RIGHT*0.75
            )
            table[1].add(zero_val)
            self.play(Write(zero_val))
        self.wait(2)


        # Border around current weight
        weight_rect = Rectangle(
            width=0.75, height=0.75
        ).move_to(table_ul + RIGHT*3*0.75)
        self.play(Create(weight_rect))
        self.wait(2)


        # Algorithm
        n, W = len(item_list), 5
        FZ = 24

        for cur_item in range(1, n):
            self.play(weight_rect.animate.move_to(table_ul + RIGHT*3*0.75))
            self.play(item_rect.animate.shift(DOWN))

            i = cur_item+1  
            wi, vi = 2, 3


            for cur_weight in range(0, W+1):
                j = cur_weight+4

                new_val = None
                fade_out_anim = []


                # This item's value and weight
                cur_item_val = int(table[i][vi].text)
                cur_item_weight = int(table[i][wi].text)
                

                # Emphasise the weight of the current item
                weight_rect_2 = Rectangle(
                    width=0.5, height=0.75,
                    color=ORANGE, 
                    stroke_width=0,
                    fill_opacity=0.2
                ).move_to(table[i][wi])

                too_heavy = True
                if cur_item_weight <= cur_weight:
                    too_heavy = False

                self.play(FadeIn(weight_rect_2))
                self.play(Indicate(weight_rect_2, color=(RED if too_heavy else GREEN)))
                self.play(FadeOut(weight_rect_2))


                # Find the value
                # Previous best value
                prev_val = int(table[i-1][j].text)
                prev_val_rect = Rectangle(
                    width=0.75, height=0.75,
                    color=PINK, 
                    stroke_width=0,
                    fill_opacity=0.2
                ).move_to(table[i-1][j].get_center())
                
                self.play(FadeIn(prev_val_rect))
                fade_out_anim.append(FadeOut(prev_val_rect))
                self.wait(1)


                if not too_heavy:

                    # Value of the current item
                    cur_val_rect = Rectangle(
                        width=0.75, height=0.75,
                        color=GOLD, 
                        stroke_width=0,
                        fill_opacity=0.2
                    ).move_to(table[i][vi])

                    self.play(FadeIn(cur_val_rect))
                    fade_out_anim.append(FadeOut(cur_val_rect))


                    # Value of the optimal previous bag
                    best_bag_rect = None
                    best_bag_val = 0
                    if cur_item_weight <= cur_weight:
                        best_bag_rect = Rectangle(
                            width=0.75, height=0.75,
                            color=GOLD, 
                            stroke_width=0,
                            fill_opacity=0.2
                        ).move_to(table[i-1][j-cur_item_weight])
                        
                        self.play(FadeIn(best_bag_rect))
                        fade_out_anim.append(FadeOut(best_bag_rect))

                        best_bag_val = int(table[i-1][j-cur_item_weight].text)


                    # Shift the correct values
                    self.wait(1)
                    flash_green_anim, shift_val_anim, transform_val_anim = [], [], []

                    new_val, new_val_3 = None, None
                    new_pos = table[i][j-1].get_center() + RIGHT*0.75

                    if cur_item_val + best_bag_val > prev_val:
                        flash_green_anim.append(Indicate(cur_val_rect, color=GREEN))
                        new_val = table[i][vi].copy().set_color(WHITE)                  

                        flash_green_anim.append(Indicate(best_bag_rect, color=GREEN))
                        new_val_2 = table[i-1][j-cur_item_weight].copy()
                        shift_val_anim.append(new_val_2.set_color(WHITE).animate.move_to(new_pos))

                        transform_val_anim.append(FadeOut(new_val_2))
                        new_val_3 = Text(str(cur_item_val + best_bag_val), font_size=FZ)
                        transform_val_anim.append(Transform(new_val, new_val_3.move_to(new_pos)))                           

                    else:
                        flash_green_anim.append(Indicate(prev_val_rect, color=GREEN))
                        new_val = table[i-1][j].copy().set_color(WHITE)
                    
                    shift_val_anim.append(new_val.animate.move_to(new_pos))
                    self.play(*flash_green_anim)

                    self.play(*shift_val_anim)
                    if len(transform_val_anim) > 0:
                        self.play(*transform_val_anim)

                    if new_val_3 != None:
                        new_val = new_val_3


                else:
                    # Too heavy, keep the previous item
                    new_val = table[i-1][j].copy()
                    self.play(new_val.animate.shift(DOWN))


                if len(fade_out_anim) > 0:
                    self.play(*fade_out_anim)

                table[i].add(new_val)


                if cur_weight < W:
                    self.play(weight_rect.animate.shift(RIGHT*0.75))


        # Highlight the answer
        ans_rect = Rectangle(
            width=0.75, height=0.75,
            color=GREEN, 
            stroke_width=0,
            fill_opacity=0.2
        ).move_to(table[n][W+4])

        self.play(FadeIn(ans_rect))
        self.wait(2)
        self.play(FadeOut(ans_rect))