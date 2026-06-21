from manim import *

from shorts.algorithm_mini_challenges import *
from constants import *
from props.furniture import Plant, Chair, Table

config.background_color = DEFAULT_BACKGROUND

config.pixel_width = MOBILE_WIDTH
config.pixel_height = MOBILE_HEIGHT
config.frame_width = MOBILE_FRAME_WIDTH
config.frame_height = MOBILE_FRAME_HEIGHT


FILL_OPACITY = 0.8


def make_human(colour):
	head = Circle(color=colour, fill_opacity=FILL_OPACITY, radius=1)
	body = Arc(color=colour, fill_opacity=FILL_OPACITY, radius=1.5, angle=PI)
	human = VGroup(head, body).arrange(DOWN)

	return VGroup(human)


def make_window():
	WINDOW_WIDTH, WINDOW_HEIGHT = 4.5, 2.5
	window = Rectangle(
		width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
		stroke_color=DARK_BROWN,
		stroke_width=20,
		fill_color=BLUE,
		fill_opacity=FILL_OPACITY
	)

	sun = Circle(
		radius=0.3,
		stroke_color=YELLOW,
		fill_color=YELLOW,
		fill_opacity=FILL_OPACITY
	).move_to(window.get_center() + UP*(0.4*WINDOW_HEIGHT/2) + RIGHT*(0.6*WINDOW_WIDTH/2))

	return VGroup(window, sun)


class SweepLine(Scene):
	def make_room(self):
		chair_1 = Chair(fill_opacity=FILL_OPACITY).chair.move_to(LEFT*1)
		table = Table(fill_opacity=FILL_OPACITY).table.move_to(RIGHT + DOWN)
		plant = Plant(fill_opacity=FILL_OPACITY).plant.move_to(LEFT*3).scale(0.8)

		return VGroup(plant, chair_1, table)


	def time_as_float(self, time_str):
		hours, minutes = map(int, time_str.split(':'))
		time_as_float = hours + (minutes / 60.0)
		return time_as_float


	def float_as_time(self, hours_float):
		hours, minutes = divmod(hours_float * 60, 60)
		formatted_time = f"{int(hours):02d}:{int(minutes):02d}"
		return formatted_time


	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		sh = ShortHint(self, "You own an office space.")
		sh.create_hint()

		room = self.make_room().move_to(DOWN*4)
		self.play(Create(room))
		self.wait(2)

		l_schedule = [
			{"key": "A", "colour": RED, "start": "06:15", "end": "14:15"},
			{"key": "B", "colour": ORANGE, "start": "11:45", "end": "15:15"},
			{"key": "C", "colour": YELLOW, "start": "08:30", "end": "17:45"},
			{"key": "D", "colour": GREEN, "start": "14:15", "end": "20:00"},
			{"key": "E", "colour": TEAL, "start": "05:45", "end": "09:00"},
			{"key": "F", "colour": BLUE, "start": "06:15", "end": "08:30"},
			{"key": "G", "colour": PURPLE, "start": "10:00", "end": "14:15"}
		]

		sh.change_hint("Given a schedule of all the shifts...")
		
		v_schedule = VGroup()
		for shift in l_schedule:
			t_shift = Text(shift["key"] + ": " + shift["start"] + " - " + shift["end"], font_size=30, t2c={str(shift["key"] + ":"): shift["colour"]})
			v_schedule.add(t_shift)
		v_schedule.arrange(DOWN).shift(UP)
		self.play(Create(v_schedule))

		sh.change_hint("What is the maximum number of people\nin the room at any give time?")
		self.wait(2)


		title = Text("Algorithm Mini Challenges #1", font_size=30, t2c={"#1": LIGHT_PINK}).move_to(UP*4.5)
		self.play(Write(title))
		self.wait(2)


		self.play(v_schedule.animate.shift(LEFT*2))
		v_rects = VGroup()
		for i in range(0, len(l_schedule)):
			shift = l_schedule[i]
			start, end = self.time_as_float(shift['start']), self.time_as_float(shift['end'])
			rect = Rectangle(
				width=(end-start)/4, height=0.5, 
				fill_color=shift['colour'], 
				fill_opacity=0.25
			).next_to(v_schedule[i], RIGHT).shift(LEFT*((12-start)/4)).shift(RIGHT*1.5)
			v_rects.add(rect)
			self.play(GrowFromEdge(rect, UP))
		
		for i in range(1, len(v_rects)):
			anim = []
			for j in range(0, i):
				anim.append(v_rects[j].animate.align_to(v_rects[i], UP))
			self.play(*anim)
		self.wait(2)


		sh.change_hint("Sweep Line Algorithm", font_size=40)
		self.play(FadeOut(v_rects), v_schedule.animate.shift(RIGHT*2), FadeOut(title))
		self.wait(1)

		l_events = []
		v_events, v_events_2 = VGroup(), VGroup()
		for i in range(0, len(l_schedule)):
			enter = Text("(" + l_schedule[i]['start'] + " +1)", font_size=30).move_to(v_schedule[i].get_center()+LEFT*1.5)
			leave = Text("(" + l_schedule[i]['end'] + " -1)", color=GRAY, font_size=30).move_to(v_schedule[i].get_center()+RIGHT*1.5)
			
			v_events_2.add(VGroup(enter, leave))

			l_events.append({'time': self.time_as_float(l_schedule[i]['start']), 'add': 1, 'colour': l_schedule[i]['colour']})
			l_events.append({'time': self.time_as_float(l_schedule[i]['end']), 'add': -1, 'colour': l_schedule[i]['colour']})

			self.play(Transform(v_schedule[i], v_events_2[i]))
			if i == 0:
				self.wait(2)

		sh.change_hint("Sort events in chronological order.\nProcess departures before arrivals.")
		sorted_l_events = sorted(l_events, key=lambda x: (x['time'], x['add']))
		for event in sorted_l_events:
			if event['add'] == 1:
				v_events.add(Text("(" + self.float_as_time(event['time']) + " +1)", font_size=30))
			else:
				v_events.add(Text("(" + self.float_as_time(event['time']) + " -1)", font_size=30, color=GRAY))
		v_events.arrange(DOWN)
		self.play(FadeOut(room), Transform(v_schedule, v_events))
		self.wait(2)
		self.play(v_schedule.animate.shift(LEFT*2))


		sh.change_hint("Sweep a line through the events.\nTrack the current number of people,\nand max amount seen.")
		
		t2c = {"Current:": LIGHT_PINK, "Max:": PINK}
		current = 0
		t_current = Text("Current: %d" % (current), font_size=30, t2c=t2c).move_to(DOWN*5.5 + LEFT*1.5)

		maximum = 0
		t_max = Text("Max: %d" % (maximum), font_size=30, t2c=t2c).move_to(DOWN*5.5 + RIGHT*1.5)

		arrow = Arrow(start=RIGHT, end=ORIGIN).move_to(v_schedule[0].get_right()+RIGHT*0.5)
		self.play(Create(arrow))
		self.play(AddTextLetterByLetter(t_current))
		self.play(AddTextLetterByLetter(t_max))
		self.wait(2)

		guys = []		
		for i in range(0, len(sorted_l_events)):
			change_max = False
			self.play(arrow.animate.move_to(v_schedule[i].get_right()+RIGHT*0.5))
			
			shift = sorted_l_events[i]
			if shift['add'] == 1:
				pos = (
					(UP*4+RIGHT*2) if len(guys) == 0 
					else (guys[len(guys)-1]['human'].get_center() + DOWN*1.5)
				)
				human = make_human(shift['colour']).move_to(pos).scale(0.25)
				guys.append({'human': human, 'colour': shift['colour']})
				self.play(FadeIn(guys[len(guys)-1]['human'], shift=LEFT*2))

				current += 1
				if current > maximum:
					maximum = current
					change_max = True

			else:
				guy_dict = next((it for it in guys if it['colour'] == shift['colour']), None)
				guys[:] = [it for it in guys if it.get('colour') != shift['colour']]
				self.play(FadeOut(guy_dict['human'], shift=RIGHT*2))

				current -= 1

			t_current_2 = Text("Current: %d" % (current), font_size=30, t2c=t2c).move_to(DOWN*5.5 + LEFT*1.5)
			t_max_2 = Text("Max: %d" % (maximum), font_size=30, t2c=t2c).move_to(DOWN*5.5 + RIGHT*1.5)

			self.play(Transform(t_current, t_current_2))
			if change_max:
				self.play(Transform(t_max, t_max_2))

		self.play(FadeOut(arrow))
		self.wait(2)

		self.play(Indicate(t_max))
		self.wait(2)

		brace = BraceBetweenPoints(point_1=v_schedule[0].get_top(), point_2=v_schedule[len(v_schedule)-1].get_bottom(), direction=RIGHT).shift(RIGHT)
		sorting = Text("Sorting: O(nlog(n))", font_size=24).next_to(brace, RIGHT)
		self.play(GrowFromCenter(brace), Write(sorting))
		self.wait(2)

		line = Line(start=v_schedule[0].get_left(), end=v_schedule[0].get_right())
		l_sweep = Text("Line Sweep: O(n)", font_size=24).next_to(v_schedule[len(v_schedule)-1].get_center(), RIGHT, buff=2)
		self.play(line.animate.move_to(v_schedule[len(v_schedule)-1].get_center()))
		self.play(FadeOut(line), Write(l_sweep))
		self.wait(2)
