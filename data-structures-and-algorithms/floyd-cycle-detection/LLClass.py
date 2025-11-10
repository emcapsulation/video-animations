from manim import *
import math


P_RAD = 0.125
P1_COL = PINK
P2_COL = GREEN
NODE_COL = BLUE


class ListNode:
    def __init__(self, dot):
        self.dot = dot
        self.label = None
        self.arrow = None
        self.next = None


    def get_next(self):
        return self.next

    def get_dot(self):
        return self.dot

    def get_label(self):
        return self.label

    def get_arrow(self):
        return self.arrow

    def is_tail(self):
        return self.next == None

    def set_next(self, forward):
        self.next = forward

    def set_label(self, label):
        self.label = label

    def set_arrow(self, arrow):
        self.arrow = arrow

    def get_top_left(self):
        return self.dot.get_center() + UP*self.dot.radius + LEFT*self.dot.radius

    def get_top_right(self):
        return self.dot.get_center() + UP*self.dot.radius + RIGHT*self.dot.radius

    def get_bottom_left(self):
        return self.dot.get_center() + DOWN*self.dot.radius + LEFT*self.dot.radius
        
    def get_bottom_right(self):
        return self.dot.get_center() + DOWN*self.dot.radius + RIGHT*self.dot.radius

    def add_to_vgroup(self, group):
        group.add(self.get_dot())

        if (self.label != None):
            group.add(self.get_label())

        if (self.arrow != None):
            group.add(self.get_arrow())

        return group



class LinkedList:
    def __init__(self, has_cycle):
        self.has_cycle = has_cycle

        self.num_nodes = 0
        self.straight_size = 0
        self.cycle_size = 0

        self.head = None
        self.meeting_point = None
        self.entry_point = None

        self.ll_group = VGroup()       


    def get_num_nodes(self):
        return self.num_nodes

    def get_straight_size(self):
        return self.straight_size

    def get_cycle_size(self):
        return self.cycle_size

    def get_head(self):
        return self.head

    def set_head(self, head):
        self.head = head


    def set_cycle_nodes(self):
        '''
        Linked list with cycle
        '''
        self.num_nodes = 9
        left_shift = 6
        down_shift = 1

        self.straight_size = 4
        self.cycle_size = 5

        cur_left_shift = 0

        # Set up nodes
        cur_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift) + DOWN*1))
        cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

        self.set_head(cur_node)        

        for i in range(1, self.straight_size):
            next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift-2*i) + DOWN*1))
            next_node.set_label(Text(str(i+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
            cur_node.set_next(next_node)
            self.ll_group = cur_node.add_to_vgroup(self.ll_group)

            cur_node = next_node

            cur_left_shift = left_shift-2*i

        cycle_head = cur_node

        # 0 means we are moving leftwards
        direction = 0
        for i in range(0, self.cycle_size):
            # Put the cycle in a circle
            if cur_left_shift <= -1*left_shift:
                direction = 1

            if direction == 1:
                cur_left_shift = cur_left_shift+2
            else:
                cur_left_shift = cur_left_shift-2

            if i == math.floor(self.cycle_size/2):
                down_shift = 1
            elif i < self.cycle_size/2:
                down_shift = -1
            else:
                down_shift = 3

            next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*cur_left_shift + DOWN*down_shift))
            next_node.set_label(Text(str(i+self.straight_size+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            # Set arrows
            # Super ugly but I just need to make a hexagon
            if i == 0:
                cur_node.set_arrow(Arrow(cur_node.get_top_right(), next_node.get_bottom_left()))
            elif i == 1:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
            elif i == 2:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_right(), next_node.get_top_left()))
            elif i == 3:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_left(), next_node.get_top_right()))
            elif i == 4:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_left(), next_node.get_dot().get_right()))
            else:
                cur_node.set_arrow(Arrow(cur_node.get_top_left(), next_node.get_bottom_right()))

            cur_node.set_next(next_node)
            self.ll_group = cur_node.add_to_vgroup(self.ll_group)

            cur_node = next_node

        cur_node.set_next(cycle_head)
        cur_node.set_arrow(Arrow(cur_node.get_top_left(), cycle_head.get_bottom_right()))
        self.ll_group = cur_node.add_to_vgroup(self.ll_group)

        self.ll_group.move_to(ORIGIN).shift(DOWN*1)


    def set_nodes(self, num_nodes):
        self.num_nodes = num_nodes

        if not self.has_cycle:
            '''
            Linked list with no cycle
            '''
            left_shift = 6
            shift_multiplier = 12/self.get_num_nodes()

            # Set up nodes
            cur_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift) + DOWN*1))
            cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

            # Set up the head
            self.set_head(cur_node)

            for i in range(1, self.num_nodes):
                next_node = None

                if i == self.num_nodes-1:
                    # Final node should say "NULL"
                    next_node = ListNode(Text("NULL", font_size=24).shift(LEFT*(left_shift-shift_multiplier*i) + DOWN*1))

                else:
                    next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift-shift_multiplier*i) + DOWN*1))
                    next_node.set_label(Text(str(i+1), font_size=24).next_to(next_node.get_dot(), DOWN))

                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
                cur_node.set_next(next_node)
                self.ll_group = cur_node.add_to_vgroup(self.ll_group)

                cur_node = next_node   
            self.ll_group = next_node.add_to_vgroup(self.ll_group)         

        else:
            self.set_cycle_nodes()
        
        self.ll_group.move_to(ORIGIN).shift(DOWN*1)



    def create_big_loop(self, scene):
        '''
        Cycle only
        '''
        self.num_nodes = 8
        left_shift = 6
        down_shift = 1

        self.straight_size = 0
        self.cycle_size = 7

        cur_left_shift = 0

        # Set up nodes
        cur_node = ListNode(Dot(color=NODE_COL).shift(DOWN*1))
        cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

        self.set_head(cur_node)
        cycle_head = cur_node

        # 0 means we are moving leftwards
        direction = 0
        for i in range(0, self.cycle_size):
            # Put the cycle in a circle
            if cur_left_shift <= -7:
                direction = 1

            if direction == 1:
                cur_left_shift = cur_left_shift+2
            else:
                cur_left_shift = cur_left_shift-2

            if i == math.floor(self.cycle_size/2):
                down_shift = 1
            elif i < self.cycle_size/2:
                down_shift = -1
            else:
                down_shift = 3

            next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*cur_left_shift + DOWN*down_shift))
            next_node.set_label(Text(str(i+self.straight_size+2), font_size=24).next_to(next_node.get_dot(), DOWN))

            # Set arrows
            if i == 0:
                cur_node.set_arrow(Arrow(cur_node.get_top_right(), next_node.get_bottom_left()))
            elif i == 1 or i == 2:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
            elif i == 3:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_right(), next_node.get_top_left()))
            elif i == 4:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_left(), next_node.get_top_right()))
            elif i == 5 or i == 6:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_left(), next_node.get_dot().get_right()))
            else:
                cur_node.set_arrow(Arrow(cur_node.get_top_left(), next_node.get_bottom_right()))

            cur_node.set_next(next_node)
            self.ll_group = cur_node.add_to_vgroup(self.ll_group)
            cur_node = next_node

        cur_node.set_next(cycle_head)
        cur_node.set_arrow(Arrow(cur_node.get_top_left(), cycle_head.get_bottom_right()))
        self.ll_group = cur_node.add_to_vgroup(self.ll_group)

        self.ll_group.move_to(ORIGIN)


    def create_large_list(self):
        '''
        Linked list with cycle
        '''
        self.num_nodes = 16
        left_shift = 5
        down_shift = 1

        self.straight_size = 10
        self.cycle_size = 6

        cur_left_shift = 0

        # Set up nodes
        cur_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift) + DOWN*1))
        cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

        self.set_head(cur_node)

        for i in range(1, self.straight_size):
            next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*(left_shift-1*i) + DOWN*1))
            next_node.set_label(Text(str(i+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
            cur_node.set_next(next_node)
            self.ll_group = cur_node.add_to_vgroup(self.ll_group)
            cur_node = next_node

            cur_left_shift = left_shift-1*i

        cycle_head = cur_node

        # 0 means we are moving leftwards
        direction = 0
        down_count = 0
        for i in range(0, self.cycle_size):
            # Put the cycle in a circle
            if cur_left_shift <= -7 and down_count == 0:
                direction = 2
                down_count = 1
            elif down_count == 1:
                direction = 1

            if direction == 1:
                cur_left_shift = cur_left_shift+1
            elif direction == 0:
                cur_left_shift = cur_left_shift-1

            if down_count == 0:
                down_shift = 0
            else:
                down_shift = 2

            next_node = ListNode(Dot(color=NODE_COL).shift(LEFT*cur_left_shift + DOWN*down_shift))
            next_node.set_label(Text(str(i+self.straight_size+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            # Set arrows
            if i == 0:
                cur_node.set_arrow(Arrow(cur_node.get_top_right(), next_node.get_bottom_left()))
            elif i == 1 or i == 2:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left()))
            elif i == 3:
                cur_node.set_arrow(CurvedArrow(cur_node.get_dot().get_right(), next_node.get_dot().get_right(), angle=-PI/2).shift(RIGHT*0.2))
            elif i == 4 or i == 5:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_left(), next_node.get_dot().get_right()))
            else:
                cur_node.set_arrow(Arrow(cur_node.get_top_left(), next_node.get_bottom_right()))

            cur_node.set_next(next_node)
            self.ll_group = cur_node.add_to_vgroup(self.ll_group)
            cur_node = next_node

        cur_node.set_next(cycle_head)
        cur_node.set_arrow(Arrow(cur_node.get_top_left(), cycle_head.get_bottom_right()))
        self.ll_group = cur_node.add_to_vgroup(self.ll_group)

        self.ll_group.move_to(ORIGIN).shift(DOWN*2)


    # Add all nodes, labels and arrows to the scene
    def add_linked_list(self, scene):
        cur_node = self.head
        for i in range(0, self.num_nodes):
            if cur_node.get_dot() != None:
                scene.add(cur_node.get_dot())

            if cur_node.get_label() != None:
                scene.add(cur_node.get_label())

            if cur_node.get_arrow() != None:
                scene.add(cur_node.get_arrow())

            cur_node = cur_node.get_next()


    # Draws the linked list onto the screen
    def draw_linked_list(self, scene, run_time):
        cur_node = self.head
        for i in range(0, self.num_nodes):
            if cur_node.get_dot() != None:
                scene.add(cur_node.get_dot())

                if cur_node.get_label() != None:
                    scene.play(FadeIn(cur_node.get_dot(), cur_node.get_label()), run_time=run_time)
                else:
                    scene.play(FadeIn(cur_node.get_dot()), run_time=run_time)

            if cur_node.get_arrow() != None:
                scene.add(cur_node.get_arrow())
                scene.play(FadeIn(cur_node.get_arrow()), run_time=run_time)

            cur_node = cur_node.get_next()


    # The traversal of a linked list with one pointer
    def traversal_animation(self, scene, run_time_mult=1):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=P1_COL, radius=P_RAD).move_to(self.get_head().get_dot().get_center())
        scene.play(pointer.animate.move_to(self.get_head().get_dot().get_center()))

        if not self.has_cycle:   
            cur_node = self.get_head()
            while cur_node.get_next() != None:
                scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=1*run_time_mult)
                cur_node = cur_node.get_next()
            
            # Animate the dot changing color from yellow to red
            scene.play(FadeOut(pointer), cur_node.get_dot().animate.set_color(RED), run_time=2)

        else:           
            # It shows it going around the cycle a few times
            count = 0
            cur_node = self.get_head()
            while count < self.get_num_nodes()+8:
                scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=1*run_time_mult)
                cur_node = cur_node.get_next()
                count += 1


    def set_animation(self, scene, brackets, node, visited_nodes, run_time=1, font_size=48):
        if node.get_label() != None:
            # Add the label of the first node to the visited nodes list
            visited_nodes.append(node.get_label().get_text())

            # Update the brackets with the new content (visited nodes)
            new_brackets = Text(f"[{', '.join(visited_nodes)}]", font_size=font_size).shift(UP * 2)

            # Animate the transformation, fading out the old brackets
            scene.play(Transform(brackets, new_brackets), run_time=run_time)

        return visited_nodes


    # The traversal of a linked list by marking nodes as visted
    def traversal_animation_set(self, scene):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=P1_COL, radius=P_RAD).move_to(self.get_head().get_dot().get_center())

        # Animation: move the pointer along the linked list
        visited_nodes = []
        brackets = Text("[]", font_size=48).shift(UP * 2)
        scene.play(Write(brackets))

        cur_node = self.get_head()
        while cur_node.get_label().get_text() not in visited_nodes:
            visited_nodes = self.set_animation(scene, brackets, cur_node, visited_nodes, run_time=0.75)
            scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=0.75)            
            cur_node = cur_node.get_next()            

        scene.play(
            brackets[7].animate.set_color(RED),
            pointer.animate.set_color(RED)
        )
        scene.wait(4)


    # Draws the linked list with a set
    def draw_with_set(self, scene):
        # Animation: move the pointer along the linked list
        visited_nodes = []
        brackets = Text("[]", font_size=48).shift(UP * 2)
        scene.play(Write(brackets))            

        cur_node = self.head
        for i in range(0, self.num_nodes):
            if cur_node.get_dot() != None:
                scene.add(cur_node.get_dot())

                if cur_node.get_label() != None:
                    scene.play(FadeIn(cur_node.get_dot(), cur_node.get_label()), run_time=0.05)
                else:
                    scene.play(FadeIn(cur_node.get_dot()), run_time=0.05)

            if cur_node.get_arrow() != None:
                scene.add(cur_node.get_arrow())
                scene.play(FadeIn(cur_node.get_arrow()), run_time=0.05)

            visited_nodes = self.set_animation(scene, brackets, cur_node, visited_nodes, run_time=0.05, font_size=48)
            cur_node = cur_node.get_next()


    # Stepping to the meeting point
    def step_backwards(self, scene, hare, tortoise, run_time_mult=1, show_pointer_only=0):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=P1_COL, radius=P_RAD).move_to(tortoise.get_dot().get_center())
        pointer2 = Dot(color=P2_COL, radius=P_RAD).move_to(hare.get_dot().get_center())

        if show_pointer_only == 2:
            pointer.set_opacity(0)
        elif show_pointer_only == 1:
            pointer2.set_opacity(0)

        scene.add(pointer, pointer2)

        # Move the tortoise to head
        scene.play(pointer.animate.move_to(self.get_head().get_dot().get_center()))
        tortoise = self.get_head()

        while tortoise.get_dot() != hare.get_dot():
            scene.play(
                pointer.animate.move_to(tortoise.get_next().get_dot().get_center()),
                pointer2.animate.move_to(hare.get_next().get_dot().get_center()),
                run_time=1*run_time_mult
            )

            tortoise = tortoise.get_next()
            hare = hare.get_next()

        scene.play(
            pointer.animate.set_color(RED),
            pointer2.animate.set_color(RED)
        )

        scene.wait(2)

        scene.play(
            FadeOut(pointer), FadeOut(pointer2)
        )

        self.entry_point = tortoise


    # The Floyd cycle finding animation
    def floyd_animation(self, scene, show_step=True, run_time_mult=1, show_pointer_only=0):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=P1_COL, radius=P_RAD).move_to(self.get_head().get_dot().get_center())
        pointer2 = Dot(color=P2_COL, radius=P_RAD).move_to(self.get_head().get_dot().get_center())

        if show_pointer_only == 2:
            pointer.set_opacity(0)
        elif show_pointer_only == 1:
            pointer2.set_opacity(0)

        # Animation: move the pointer along the linked list
        scene.play(
            pointer.animate.move_to(self.get_head().get_dot().get_center()),
            pointer2.animate.move_to(self.get_head().get_dot().get_center()),
        )

        tortoise = self.get_head()
        hare = self.get_head()
        started = False
        while hare.get_next() != None and (started == False or tortoise.get_dot() != hare.get_dot()):
            if show_pointer_only != 2:
                scene.play(   
                    pointer.animate.move_to(tortoise.get_next().get_dot().get_center()),        
                    pointer2.animate.move_to(hare.get_next().get_dot().get_center()),
                    run_time=1*run_time_mult
                )

            tortoise = tortoise.get_next()
            hare = hare.get_next()

            if hare.get_next() != None:
                if show_pointer_only != 2:
                    scene.play(
                        pointer2.animate.move_to(hare.get_next().get_dot().get_center()),
                        run_time=1*run_time_mult
                    )
                else:
                    scene.play(   
                        pointer.animate.move_to(tortoise.get_next().get_dot().get_center()),        
                        pointer2.animate.move_to(hare.get_next().get_dot().get_center()),
                        run_time=1*run_time_mult
                    )

                hare = hare.get_next()

            else:
                break

            started = True

        if show_step == True:
            scene.play(
                pointer.animate.set_color(RED),
                pointer2.animate.set_color(RED)
            )
            scene.wait(6)
            scene.remove(pointer, pointer2)
            self.step_backwards(scene, hare, tortoise, run_time_mult, show_pointer_only)

        else:
            # Animate the dot changing color to red
            scene.play( 
                # pointer.animate.set_color(RED), 
                pointer2.animate.set_color(RED), 
                run_time=2)

            scene.play( 
                FadeOut(pointer), 
                FadeOut(pointer2), 
                run_time=2)


    def get_meeting_point(self):
        tortoise = self.head
        hare = self.head

        started = False
        while started == False or tortoise != hare:
            tortoise = tortoise.get_next()
            hare = hare.get_next().get_next()
            started = True

        self.meeting_point = tortoise


    def colour_xyz(self, scene):
        # Pointer 1 distance
        cur_node = self.head

        count = 0
        while count < self.straight_size-1:
            scene.play(cur_node.get_dot().animate.set_color(PURPLE), run_time=0.3)

            count += 1
            cur_node = cur_node.get_next()

        x_label = Text("x").set_color(PURPLE)
        x_label.next_to(self.head.get_dot(), UP)
        x_text = Text("x = Distance from head to start of cycle", font_size=18).shift(UP*3)
        x_text[0:1].set_color(PURPLE)
        scene.play(Write(x_label), Write(x_text))


        # Pointer 2 distance
        while cur_node != self.meeting_point:
            scene.play(cur_node.get_dot().animate.set_color(YELLOW), run_time=0.3)
            cur_node = cur_node.get_next()

        y_label = Text("y").set_color(YELLOW)
        y_label.next_to(self.meeting_point.get_dot(), RIGHT*8 + UP*1)
        y_text = Text("y = Distance from start of cycle to meeting point", font_size=18).shift(UP*2.5)
        y_text[0:1].set_color(YELLOW)
        scene.play(Write(y_label), Write(y_text))

        while cur_node != self.entry_point:
            scene.play(cur_node.get_dot().animate.set_color(RED), run_time=0.3)
            cur_node = cur_node.get_next()

        z_label = Text("z").set_color(RED)
        z_label.next_to(self.meeting_point.get_dot(), DOWN*3 + LEFT*4)
        z_text = Text("z = Distance from meeting point to start of cycle", font_size=18).shift(UP*2)
        z_text[0:1].set_color(RED)
        scene.play(Write(z_label), Write(z_text))        

        return x_text, y_text, z_text


    # The proof
    def proof_animation(self, scene, run_time_mult=1):
        self.get_meeting_point()
        self.step_backwards(scene, self.meeting_point, self.meeting_point, run_time_mult)  
        
        scene.wait(2)        
        meet_pt_text = Text("Meeting point: 15", font_size=24).shift(UP*3.5)

        scene.play(Write(meet_pt_text), self.meeting_point.get_dot().animate.set_color(RED))

        x_text, y_text, z_text = self.colour_xyz(scene) 

        text = Text("We want to show: ", font_size=24).shift(UP*1)
        scene.play(Write(text))
        show_text = Tex("$x = cL + z$").shift(UP*0.5)
        scene.play(Write(show_text))        

        self.step_backwards(scene, self.meeting_point, self.meeting_point, run_time_mult=0.3, show_pointer_only=1)
        self.step_backwards(scene, self.meeting_point, self.meeting_point, run_time_mult=0.5, show_pointer_only=2)

        scene.wait(3)
        scene.remove(meet_pt_text, x_text, y_text, z_text, text, show_text)


    def proof_algebra(self, scene):
        down_shift = 0.5
        num_shifts = 0

        line_1 = MathTex("d_f = 2 \\cdot d_s", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Write(line_1))
        scene.wait(2)

        line_2 = MathTex("d_f = 2 \\cdot d_s", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_2.animate.shift(DOWN*down_shift))
        num_shifts += 1

        self.floyd_animation(scene, show_step=False, run_time_mult=0.5, show_pointer_only=2)

        line_21 = MathTex("x + n_f L + y = 2 \\cdot d_s", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_2, line_21))
        scene.wait(2)

        self.floyd_animation(scene, show_step=False, run_time_mult=0.3, show_pointer_only=1)

        line_22 = MathTex("x + n_f L + y = 2 \\cdot (x + n_s L + y)", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_2, line_22))
        scene.wait(2)

        line_3 = MathTex("x + n_f L + y = 2 \\cdot (x + n_s L + y)", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_3.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_31 = MathTex("x + n_f L + y = 2x + 2 n_s L + 2y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_3, line_31))
        scene.wait(2)

        line_32 = MathTex("x + n_f L + y = 2x + n L + 2y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_3, line_32))
        scene.wait(2)

        line_4 = MathTex("x + n_f L + y = 2x + n L + 2y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_4.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_41 = MathTex("-x = nL - n_fL + y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_4, line_41))
        scene.wait(2)

        line_42 = MathTex("x = n_fL - nL - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_4, line_42))
        scene.wait(2)

        line_421 = MathTex("x = n_fL - nL - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_421.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_4211 = MathTex("x = (n_f-n)L - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_421, line_4211))
        scene.wait(2)

        line_422 = MathTex("x = mL - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_421, line_422))
        scene.wait(2)

        line_5 = MathTex("x = mL - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_5.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_51 = MathTex("x = (m-1)L + L - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_5, line_51))
        scene.wait(2)

        line_6 = MathTex("x = (m-1)L + L - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_6.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_61 = MathTex("x = (m-1)L + y+z - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_6, line_61))
        scene.wait(2)

        line_7 = MathTex("x = (m-1)L + y+z - y", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_7.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_71 = MathTex("x = (m-1)L + z", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_7, line_71))
        scene.wait(2)

        line_8 = MathTex("x = (m-1)L + z", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(line_8.animate.shift(DOWN*down_shift))
        num_shifts += 1

        line_81 = MathTex("x = cL + z", font_size=28).shift(UP*(3-down_shift*num_shifts))
        scene.play(Transform(line_8, line_81))
        scene.wait(2)