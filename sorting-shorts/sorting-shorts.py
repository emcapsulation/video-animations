from manim import *
import random
from Sorter import Sorter
from MidiGenerator import MidiGenerator

config.background_color = "#15131c"

config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class SelectionSort(Scene):
    def construct(self):
        Text.set_default(font="Consolas")

        # Default settings
        filename = "selection-sort"
        track = 0
        channel = 0
        volume = 100
        tempo = 60
        default_duration = 1

        # Create MIDI
        mf = MidiGenerator(filename, track, channel, volume, tempo, default_duration)    

        title_text = Text("Selection Sort", font_size=48).shift(UP*2) 
        title_group = VGroup(title_text)

        time_complexity1 = Text("Time complexity: ", font_size=24)
        time_complexity2 = Tex("$O(n^2)$", font_size=30).next_to(time_complexity1, RIGHT) 
        time_complexity3 = Text("Space complexity: ", font_size=24).next_to(time_complexity1, DOWN)
        time_complexity4 = Tex("$O(1)$", font_size=30).next_to(time_complexity3, RIGHT) 
        complexity_group = VGroup(time_complexity1, time_complexity2, time_complexity3, time_complexity4)
        complexity_group.move_to(ORIGIN + DOWN*3)

        title_complexity = VGroup(title_group, complexity_group)    
        title_complexity.scale(0.9)  
        
        l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(l);
        s = Sorter(l, ORIGIN, mf)
        s.create_list(self, scale=0.7)

        self.play(Write(title_text), run_time=0.75)

        self.play(Write(time_complexity1), Write(time_complexity3), run_time=0.5)
        self.play(Write(time_complexity2), Write(time_complexity4), run_time=0.5)
        
        self.play(
            title_complexity.animate.shift(UP*2.5),
            complexity_group.animate.shift(UP*6),
            s.get_scene_elements().animate.shift(DOWN*3),
            run_time=0.75
        )        

        mf.write_pause(0.75+0.5+0.5+0.75)

        s.selection_sort(self, run_time=0.8)

        self.wait(1)
        mf.write_pause(1)

        # Write it to disk
        with open("out/" + filename + ".mid", 'wb') as outf:
            mf.write_file(outf)
