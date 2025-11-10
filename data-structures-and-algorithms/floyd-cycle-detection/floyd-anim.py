from manim import *
from LLClass import ListNode, LinkedList
import math


config.background_color = "#15131c"

P_RAD = 0.125
P1_COL = PINK
P2_COL = GREEN
NODE_COL = BLUE


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
    ).shift(UP*2 + LEFT*3.5)
    
    # Add the code to the scene
    self.add(code)
    return code    



class LLNoCycle(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(False)
        LL.set_nodes(6)

        LL.draw_linked_list(self, 1)
        self.wait(5)

        code = get_code_animation(self)
        self.play(Write(code), run_time=2)

        LL.traversal_animation(self, run_time_mult=0.5)
        self.wait(3)



class LLCycle(Scene):   
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.set_nodes(9)

        LL.draw_linked_list(self, 0.2)
        self.wait(3)

        code = get_code_animation(self)
        self.play(Write(code), run_time=2)

        LL.traversal_animation(self, run_time_mult=0.3)
        self.wait(3)



class LLCycleSet(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.set_nodes(9)
        LL.add_linked_list(self)
        LL.traversal_animation_set(self)
        self.wait(2)

        self.play(Write(Text("Start of cycle: 4", font_size=24).shift(UP*3)))
        self.wait(2)



class SetComplexity(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        time_complexity = Text("Time complexity: O(n)", font_size=24).shift(UP*0.5)       
        self.play(Write(time_complexity), run_time=2)
        self.play(time_complexity[15:].animate.set_color(GREEN))

        self.wait(4)

        space_complexity = Text("Space complexity: O(n)", font_size=24)
        self.play(Write(space_complexity), run_time=2)       
        self.play(space_complexity[16:].animate.set_color(RED))

        self.wait(4)

        LL = LinkedList(False)
        LL.set_nodes(20)

        LL.draw_with_set(self)
        self.wait(3)



class FloydNoCycle(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        title_text = Text("Floyd's Cycle Finding Algorithm").shift(UP*3)
        self.play(Write(title_text))

        time_complexity = Text("Time complexity: O(n), Space complexity: O(1)", font_size=24).shift(UP*2)       
        self.play(Write(time_complexity), run_time=2)
        self.play(time_complexity[15:19].animate.set_color(GREEN),
            time_complexity[36:40].animate.set_color(GREEN))

        pointer = Dot(color=P1_COL, radius=P_RAD).shift(UP*1 + LEFT*3.5)
        slow_text = Text("Slow pointer (tortoise) \n - Moves one node at a time", font_size=24).shift(UP*1)
        self.play(FadeIn(pointer), Write(slow_text))

        self.wait(3)

        pointer2 = Dot(color=P2_COL, radius=P_RAD).shift(LEFT*3.5)
        fast_text = Text("Fast pointer (hare) \n - Moves two nodes at a time", font_size=24)
        self.play(FadeIn(pointer2), Write(fast_text))

        self.wait(3)

        p_group = VGroup(pointer, slow_text, pointer2, fast_text)
        self.play(FadeOut(title_text, time_complexity),
            p_group.animate.shift(UP*1))

        LL = LinkedList(False)
        LL.set_nodes(7)
        LL.draw_linked_list(self, 0.05)
        LL.floyd_animation(self, show_step=False)
        self.wait(3)



class FloydCycle(Scene):  
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.set_nodes(9)
        LL.draw_linked_list(self, run_time=0.1)
        LL.floyd_animation(self)

        start_cycle = Text("Start of the cycle: 4", font_size=24).shift(UP*2)
        self.play(Write(start_cycle))
        self.wait(3)



class LargerExample(Scene):  
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.create_large_list()
        LL.ll_group.move_to(ORIGIN)
        LL.draw_linked_list(self, run_time=0.05)
        LL.floyd_animation(self, run_time_mult=0.4)
        
        start_cycle = Text("Start of the cycle: 10", font_size=24).shift(UP*2)
        self.play(Write(start_cycle))
        self.wait(3)



class CycleChase(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.create_big_loop(self)
        LL.add_linked_list(self)
        LL.floyd_animation(self, show_step=False, run_time_mult=0.5)
        self.wait(3)



class FloydCycleProof(Scene):  
    def construct(self):
        Text.set_default(font="Monospace")

        LL = LinkedList(True)
        LL.create_large_list()
        LL.draw_linked_list(self, run_time=0.05)
        LL.proof_animation(self, run_time_mult=0.4)
        LL.proof_algebra(self)
        self.wait(3)



class SourceCode(Scene):  
    def construct(self):
        Text.set_default(font="Monospace")

        code = Code(
            code="""// Floyd's cycle finding algorithm written in C++
// Returns NULL if there is no cycle, otherwise returns a pointer to the start of the cycle
Node *floydCycleFinder(Node *head) {
    // Check the head
    if (head == NULL || head->next == NULL) {
        return NULL;
    }

    Node *tortoise = head->next;
    Node *hare = head->next->next;

    // Part 1: Move the tortoise and hare until they meet again
    while (tortoise != hare) {
        // Hare has reached the end, indicating there is no cycle
        if (hare == NULL || hare->next == NULL) {
            return NULL;
        }

        // Move the tortoise one node
        tortoise = tortoise->next;

        // Move the hare two nodes
        hare = hare->next->next;
    }

    // Part 2: Move the tortoise back to the head of the LL
    tortoise = head;

    while (tortoise != hare) {
        // Step the tortoise and hare one node at a time until they meet at the entry point
        tortoise = tortoise->next;
        hare = hare->next;
    }

    // Return the entry point of the cycle
    return tortoise;
}""",
            language="C++",
            font_size=12,
            background="window"
        )
        
        # Add the code to the scene
        self.play(Write(code), run_time=5)
        self.wait(10)
        self.play(FadeOut(code))



class DrawAndGlowLetter(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        self.play(Write(Text("Thank you for watching!").shift(UP*2)))

        letter_e = Text("e", font_size=200, color=TEAL)
        self.play(Write(letter_e))

        letter_e_stroke = letter_e.copy().set_color(TEAL).set_opacity(1).set_stroke(width=3)        
        glow_effect = letter_e_stroke.copy().set_stroke(width=3, color=WHITE).set_opacity(0.6)
        self.play(FadeIn(letter_e_stroke), Transform(letter_e_stroke, glow_effect))
        self.play(FadeOut(letter_e_stroke, glow_effect))

        self.wait(3)



class Thumbnail(Scene):
    def construct(self):
        Text.set_default(font="Monospace")

        title_text = Text("Floyd's Cycle Finding Algorithm").shift(UP*3)
        self.add(title_text)

        time_complexity = Text("Time complexity: O(n), Space complexity: O(1)", font_size=24).shift(UP*2)    
        time_complexity[15:19].set_color(GREEN)   
        time_complexity[36:40].set_color(GREEN)
        self.add(time_complexity)

        pointer = Dot(color=P1_COL, radius=P_RAD).shift(UP*1 + LEFT*3.5)
        slow_text = Text("Slow pointer (tortoise) \n - Moves one node at a time", font_size=24).shift(UP*1)

        pointer2 = Dot(color=P2_COL, radius=P_RAD).shift(LEFT*3.5)
        fast_text = Text("Fast pointer (hare) \n - Moves two nodes at a time", font_size=24)

        p_group = VGroup(pointer, slow_text, pointer2, fast_text)
        self.add(p_group)

        LL = LinkedList(True)
        LL.create_large_list()
        self.add(LL.ll_group)

