from manim import *
import math


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


class LinkedList:
    def __init__(self, has_cycle):
        self.has_cycle = has_cycle

        self.num_nodes = 0
        self.straight_size = 0
        self.cycle_size = 0

        self.head = None            


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
        cur_node = ListNode(Dot(color=BLUE).shift(LEFT*(left_shift) + DOWN*1))
        cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

        self.set_head(cur_node)

        for i in range(1, self.straight_size):
            next_node = ListNode(Dot(color=BLUE).shift(LEFT*(left_shift-2*i) + DOWN*1))
            next_node.set_label(Text(str(i+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left(), buff=0.2))
            cur_node.set_next(next_node)
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

            next_node = ListNode(Dot(color=BLUE).shift(LEFT*cur_left_shift + DOWN*down_shift))
            next_node.set_label(Text(str(i+self.straight_size+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            # Set arrows
            # Super ugly but I just need to make a hexagon
            if i%self.cycle_size == 0:
                cur_node.set_arrow(Arrow(cur_node.get_top_right(), next_node.get_bottom_left(), buff=0.2))
            elif i%1 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left(), buff=0.2))
            elif i%2 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_right(), next_node.get_top_left(), buff=0.2))
            elif i%3 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_left(), next_node.get_top_right(), buff=0.2))
            elif i%4 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_left(), next_node.get_dot().get_right(), buff=0.2))
            else:
                cur_node.set_arrow(Arrow(cur_node.get_top_left(), next_node.get_bottom_right(), buff=0.2))

            cur_node.set_next(next_node)
            cur_node = next_node

        cur_node.set_next(cycle_head)
        cur_node.set_arrow(Arrow(cur_node.get_top_left(), cycle_head.get_bottom_right(), buff=0.2))


    def set_nodes(self, num_nodes):
        self.num_nodes = num_nodes

        if not self.has_cycle:
            '''
            Linked list with no cycle
            '''
            left_shift = 6
            shift_multiplier = 12/self.get_num_nodes()

            # Set up nodes
            cur_node = ListNode(Dot(color=BLUE).shift(LEFT*(left_shift) + DOWN*1))
            cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

            # Set up the head
            self.set_head(cur_node)

            for i in range(1, self.num_nodes):
                next_node = None

                if i == self.num_nodes-1:
                    # Final node should say "NULL"
                    next_node = ListNode(Text("NULL", font_size=24).shift(LEFT*(left_shift-shift_multiplier*i) + DOWN*1))

                else:
                    next_node = ListNode(Dot(color=BLUE).shift(LEFT*(left_shift-shift_multiplier*i) + DOWN*1))
                    next_node.set_label(Text(str(i+1), font_size=24).next_to(next_node.get_dot(), DOWN))

                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left(), buff=1.2/self.get_num_nodes()))
                cur_node.set_next(next_node)
                cur_node = next_node

        else:
            self.set_cycle_nodes()



    def create_big_loop(self, scene):
        '''
        Cycle only
        '''
        self.num_nodes = 6
        left_shift = 6
        down_shift = 1

        self.straight_size = 0
        self.cycle_size = 5

        cur_left_shift = 0

        # Set up nodes
        cur_node = ListNode(Dot(color=BLUE).shift(DOWN*1))
        cur_node.set_label(Text(str(1), font_size=24).next_to(cur_node.get_dot(), DOWN))

        self.set_head(cur_node)
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

            next_node = ListNode(Dot(color=BLUE).shift(LEFT*cur_left_shift + DOWN*down_shift))
            next_node.set_label(Text(str(i+self.straight_size+1), font_size=24).next_to(next_node.get_dot(), DOWN))

            # Set arrows
            # Super ugly but I just need to make a hexagon
            if i%self.cycle_size == 0:
                cur_node.set_arrow(Arrow(cur_node.get_top_right(), next_node.get_bottom_left(), buff=0.2))
            elif i%1 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_right(), next_node.get_dot().get_left(), buff=0.2))
            elif i%2 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_right(), next_node.get_top_left(), buff=0.2))
            elif i%3 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_bottom_left(), next_node.get_top_right(), buff=0.2))
            elif i%4 == 0:
                cur_node.set_arrow(Arrow(cur_node.get_dot().get_left(), next_node.get_dot().get_right(), buff=0.2))
            else:
                cur_node.set_arrow(Arrow(cur_node.get_top_left(), next_node.get_bottom_right(), buff=0.2))

            cur_node.set_next(next_node)
            cur_node = next_node

        cur_node.set_next(cycle_head)
        cur_node.set_arrow(Arrow(cur_node.get_top_left(), cycle_head.get_bottom_right(), buff=0.2))


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
    def traversal_animation(self, scene):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=PURPLE).move_to(self.get_head().get_dot().get_center())
        scene.play(pointer.animate.move_to(self.get_head().get_dot().get_center()))

        if not self.has_cycle:   
            cur_node = self.get_head()
            while cur_node.get_next() != None:
                scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=1)
                cur_node = cur_node.get_next()
            
            # Animate the dot changing color from yellow to red
            scene.play(FadeOut(pointer), cur_node.get_dot().animate.set_color(RED), run_time=2)

        else:           
            # It shows it going around the cycle a few times
            count = 0
            cur_node = self.get_head()
            while count < self.get_num_nodes()+4:
                scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=1)
                cur_node = cur_node.get_next()
                count += 1


    def set_animation(self, scene, brackets, node, visited_nodes, run_time=1, font_size=72):
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
        pointer = Dot(color=PURPLE).move_to(self.get_head().get_dot().get_center())

        # Animation: move the pointer along the linked list
        visited_nodes = []
        brackets = Text("[]", font_size=72).shift(UP * 2)
        scene.play(Write(brackets))

        cur_node = self.get_head()
        while cur_node.get_label().get_text() not in visited_nodes:
            visited_nodes = self.set_animation(scene, brackets, cur_node, visited_nodes)
            scene.play(pointer.animate.move_to(cur_node.get_next().get_dot().get_center()), run_time=1)            
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
    def step_backwards(self, scene, hare, tortoise):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=PURPLE).move_to(tortoise.get_dot().get_center())
        pointer2 = Dot(color=GREEN).move_to(hare.get_dot().get_center())

        scene.add(pointer, pointer2)

        # Move the tortoise to head
        scene.play(pointer.animate.move_to(self.get_head().get_dot().get_center()))
        tortoise = self.get_head()

        while tortoise.get_dot() != hare.get_dot():
            scene.play(
                pointer.animate.move_to(tortoise.get_next().get_dot().get_center()).set_run_time(1),
                pointer2.animate.move_to(hare.get_next().get_dot().get_center()).set_run_time(1)
            )

            tortoise = tortoise.get_next()
            hare = hare.get_next()

        scene.play(
            pointer.animate.set_color(RED),
            pointer2.animate.set_color(RED)
        )


    # The Floyd cycle finding animation
    def floyd_animation(self, scene, show_step=True):
        # Create a pointer (represented by a larger dot)
        pointer = Dot(color=PURPLE).move_to(self.get_head().get_dot().get_center())
        pointer2 = Dot(color=GREEN).move_to(self.get_head().get_dot().get_center())

        # Animation: move the pointer along the linked list
        scene.play(
            pointer.animate.move_to(self.get_head().get_dot().get_center()),
            pointer2.animate.move_to(self.get_head().get_dot().get_center()),
        )

        tortoise = self.get_head()
        hare = self.get_head()
        started = False
        while hare.get_next() != None and (started == False or tortoise.get_dot() != hare.get_dot()):
            scene.play(   
                pointer.animate.move_to(tortoise.get_next().get_dot().get_center()).set_run_time(2),        
                pointer2.animate.move_to(hare.get_next().get_dot().get_center()).set_run_time(1)
            )
            tortoise = tortoise.get_next()
            hare = hare.get_next()

            if hare.get_next() != None:
                scene.play(
                    pointer2.animate.move_to(hare.get_next().get_dot().get_center()).set_run_time(1)
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
            scene.wait(4)
            scene.remove(pointer, pointer2)
            self.step_backwards(scene, hare, tortoise)

        else:
            # Animate the dot changing color from yellow to red
            scene.play(FadeOut(pointer), 
                pointer2.animate.set_color(RED), 
                hare.get_dot().animate.set_color(RED), run_time=2)


    # The proof
    def proof_animation(self, scene):
        pass



def get_code_animation(self):
    # Create a Code object with a simple Python code snippet
    code = Code(
        code="""ListNode *ptr = head;
while (ptr != nullptr) {
    ptr = ptr->next;
}""",
        language="C++",
        font_size=16,
        background="window",
    ).shift(UP*2 + LEFT*2)
    
    # Add the code to the scene
    self.add(code)
    return code    



class LLNoCycle(Scene):
    def construct(self):
        LL = LinkedList(False)
        LL.set_nodes(6)

        LL.draw_linked_list(self, 1)

        code = get_code_animation(self)
        self.play(Write(code), run_time=2)

        LL.traversal_animation(self)



class LLCycle(Scene):   
    def construct(self):
        code = get_code_animation(self)

        LL = LinkedList(True)
        LL.set_nodes(9)

        LL.draw_linked_list(self, 0.2)

        LL.traversal_animation(self)



class LLCycleSet(Scene):
    def construct(self):
        LL = LinkedList(True)
        LL.set_nodes(9)
        LL.add_linked_list(self)
        LL.traversal_animation_set(self)



class SetComplexity(Scene):
    def construct(self):
        time_complexity = Text("Time complexity: O(n)", font_size=24).shift(UP*0.5)       
        self.play(Write(time_complexity), run_time=2)
        self.play(time_complexity[15:].animate.set_color(GREEN))

        self.wait(2)

        space_complexity = Text("Space complexity: O(n)", font_size=24)
        self.play(Write(space_complexity), run_time=2)
        self.play(space_complexity[16:].animate.set_color(RED))

        LL = LinkedList(False)
        LL.set_nodes(20)

        LL.draw_with_set(self)



class FloydNoCycle(Scene):
    def construct(self):
        pointer = Dot(color=PURPLE).shift(UP*2 + LEFT*3)
        slow_text = Text("slow pointer (tortoise)", font_size=24).shift(UP*2)
        self.play(FadeIn(pointer), Write(slow_text))

        pointer2 = Dot(color=GREEN).shift(UP*1 + LEFT*3)
        fast_text = Text("fast pointer (hare)", font_size=24).shift(UP*1)
        self.play(FadeIn(pointer2), Write(fast_text))

        LL = LinkedList(False)
        LL.set_nodes(7)
        LL.draw_linked_list(self, 0.05)
        LL.floyd_animation(self)



class FloydCycle(Scene):  
    def construct(self):
        LL = LinkedList(True)
        LL.set_nodes(9)
        LL.add_linked_list(self)
        LL.floyd_animation(self)

        start_cycle = Text("Start of the cycle: 4", font_size=24).shift(UP*2)
        self.play(Write(start_cycle))
        self.wait(4)



class CycleChase(Scene):
    def construct(self):
        LL = LinkedList(True)
        LL.create_big_loop(self)
        LL.add_linked_list(self)
        LL.floyd_animation(self, show_step=False)



class FloydCycleProof(Scene):  
    def construct(self):
        LL = LinkedList(True)
        LL.set_nodes(9)
        LL.add_linked_list(self)
        LL.proof_animation(self)
