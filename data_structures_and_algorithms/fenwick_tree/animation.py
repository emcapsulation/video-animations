from manim import *
from constants import *
from props import HintBox

from ArrayGroup import ArrayGroup
from BinaryByte import BinaryByte
from CodeBlock import CodeBlock
from FenwickTree import FenwickTree
from SkewedBellCurve import SkewedBellCurve

import math
import random

config.background_color = DEFAULT_BACKGROUND


def lsb(i):
	return i & -i


class Introduction(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		sbc = SkewedBellCurve([0, 8, 1], [0, 0.5, 0.1], 8, 4, "Marathon Times", "time", "freq")
		self.play(Create(sbc.axes), Create(sbc.labels))
		self.play(Create(sbc.curve), run_time=2)
		self.wait(2)

		hb = HintBox(
			Text("Scenario: You work on a sports statistics platform.", font_size=24, t2c={"Scenario:": PASTEL_BLUE}),
			PASTEL_BLUE
		)
		self.play(*hb.init_lbl())

		self.play(Write(sbc.title))
		self.wait(2)

		self.play(sbc.chart.animate.shift(LEFT*2))


		def make_time_box(pos, time):
			time_box = RoundedRectangle(
				width=2, height=1,
				fill_color=WHITE,
				fill_opacity=1,
				corner_radius=0.2
			).move_to(pos)		
			time_text = Text(time, font_size=28, color=BLACK).move_to(time_box.get_center())
			return VGroup(time_box, time_text)

		time_1 = make_time_box(RIGHT*4, "4:45:00")
		self.play(Create(time_1[0]))	
		self.play(AddTextLetterByLetter(time_1[1]))

		line_1 = sbc.get_line_at_x(4.75)		
		area_1 = sbc.get_area_before_x(4.75)
		self.play(Create(line_1))
		self.play(FadeIn(area_1))


		def make_bottom_text(t1, t2):
			n_runners_1 = Text(t1, font_size=20).move_to(DOWN*3)
			n_runners_2 = Text(t2, font_size=20, color=PASTEL_BLUE)
			box = SurroundingRectangle(
				n_runners_2, 
				color=PASTEL_TEAL, 
				fill_opacity=0,
				corner_radius=0.1
			)
			boxed_element = VGroup(box, n_runners_2)
			return VGroup(n_runners_1, boxed_element).arrange(RIGHT).move_to(DOWN*3)


		n_runners = make_bottom_text("# runners with time <= 4:45:00", "800,000")
		self.play(FadeIn(n_runners))
		self.wait(2)

		self.play(time_1.animate.shift(DOWN))

		time_2 = make_time_box(RIGHT*4 + UP, "3:15:30")
		self.play(Create(time_2[0]))	
		self.play(AddTextLetterByLetter(time_2[1]))

		line_2 = sbc.get_line_at_x(3.255)		
		area_2 = sbc.get_area_in_x_range(3.255, 4.75)
		self.play(Create(line_2))

		n_runners_2 = make_bottom_text("# runners with 3:15:30 <= time <= 4:45:00", "625,000")
		
		self.play(Transform(area_1, area_2), Transform(n_runners, n_runners_2))
		self.wait(2)



class MarathonCounts(Scene):
	def construct(self):

		Text.set_default(font=MONOSPACE_FONT)

		np.random.seed(1)

		MAX_INDEX = 28800
		WINDOW_SIZE = 7

		times = np.arange(MAX_INDEX + 1)
		counts = np.zeros_like(times)

		mu, sigma_left, sigma_right = 15000, 2500, 4500
		left = times <= mu
		right = times > mu

		counts[left] = 2500 * np.exp(-((times[left] - mu) ** 2) / (2 * sigma_left**2))
		counts[right] = 2500 * np.exp(-((times[right] - mu) ** 2) / (2 * sigma_right**2))

		counts = counts.astype(int)
		counts[16200] = 2507

		subtitle_1 = Text("data stores the frequency of each potential time, i seconds.", font_size=24, t2c={"data": PASTEL_TEAL}).move_to(UP*3)
		subtitle_2 = Text("i.e. data[i] = number of runners with a PB of i seconds.", font_size=20, t2c={"data[i]": PASTEL_TEAL}).next_to(subtitle_1, DOWN, buff=0.5)
		subtitle = VGroup(subtitle_1, subtitle_2)
		
		hb = HintBox(
			subtitle,
			PASTEL_BLUE
		)
		self.play(FadeIn(hb.box))
		self.wait(2)

		title = Text("data =", font_size=30)
		title.to_edge(LEFT)

		self.play(Write(title))


		def make_window(tracker_index):

			entries = []

			# start index of the window
			start = max(0, min(tracker_index - WINDOW_SIZE//2, MAX_INDEX - WINDOW_SIZE + 1))

			for i in range(WINDOW_SIZE):
				idx = start + i

				# idk if it's the best way but I pad it with invisible 0s to hold its position
				def invisible_zeros(pad_width, text_mob, text, fs):
					return VGroup(Text(f"{'0'*(pad_width-len(text))}", font_size=fs, color=DEFAULT_BACKGROUND), text_mob).arrange(RIGHT, buff=0)


				index_text = Text(f"{idx}", font_size=18, color=GREY_B)
				index_text = invisible_zeros(5, index_text, str(idx), 18)

				value_text = Text(f"{int(counts[idx])}", font_size=30)
				value_text = invisible_zeros(4, value_text, str(int(counts[idx])), 30)


				cell = VGroup(index_text, value_text)
				cell.arrange(DOWN, buff=0.08)
				cell.set_width(1.25)

				entries.append(cell)

			row = VGroup(*entries)
			row.arrange(RIGHT, buff=0.35)

			return row


		visible = make_window(3)
		visible.next_to(title, RIGHT, buff=0.6)
		self.add(visible)


		left_bracket = Text("[", font_size=72)
		right_bracket = Text("]", font_size=72)

		left_bracket.next_to(visible, LEFT, buff=0.15)
		right_bracket.next_to(visible, RIGHT, buff=0.15)

		self.play(
			FadeIn(left_bracket),
			FadeIn(right_bracket),
		)


		slidey_line = Line(LEFT*4, RIGHT*4, color=GREY, stroke_width=6)
		slidey_line.next_to(visible, DOWN, buff=0.8)

		left_label = Text("0", font_size=22).next_to(slidey_line, LEFT, buff=0.25)
		right_label = Text("28800", font_size=22).next_to(slidey_line, RIGHT, buff=0.25)

		slidey_thing = RoundedRectangle(
			width=0.45,
			height=0.25,
			corner_radius=0.05,
			fill_color=PASTEL_BLUE,
			fill_opacity=1,
			stroke_width=0
		)
		slidey_thing.move_to(slidey_line.get_start())

		self.play(Create(slidey_line), FadeIn(left_label), FadeIn(right_label))
		self.add(slidey_thing)


		tracker = ValueTracker(3)

		def update_window(mob):
			new = make_window(int(tracker.get_value()))
			new.move_to(mob)
			mob.become(new)

		visible.add_updater(update_window)


		def update_slidey_thing(mob):
			alpha = tracker.get_value() / MAX_INDEX
			mob.move_to(interpolate(slidey_line.get_start(), slidey_line.get_end(), alpha))

		slidey_thing.add_updater(update_slidey_thing)


		position_label = always_redraw(lambda: Text(f"index = {int(tracker.get_value()):,}", font_size=24).next_to(slidey_line, DOWN, buff=0.35))
		self.add(position_label)


		self.play(tracker.animate.set_value(28800), run_time=5, rate_func=linear)
		self.wait(0.5)


		self.play(tracker.animate.set_value(16200), run_time=2.5, rate_func=smooth)
		self.play(Indicate(slidey_thing, color=PASTEL_TEAL, scale_factor=1.4))


		visible.remove_updater(update_window)
		slidey_thing.remove_updater(update_slidey_thing)

		final_window = make_window(16200)
		final_window.move_to(visible)

		self.play(Transform(visible, final_window))


		center = visible[WINDOW_SIZE // 2]

		highlight = SurroundingRectangle(center, color=PASTEL_BLUE, fill_color=PASTEL_BLUE, fill_opacity=0.1, buff=0.15).shift(RIGHT*0.1)
		self.play(Create(highlight))


		explanation = Text("data[16200] = 2507", font_size=24, t2c={"2507": PASTEL_TEAL}).move_to(DOWN*3)
		time_text = Text("16200 seconds = 04:30:00", font_size=18, color=GRAY).next_to(explanation, UP).shift(LEFT*0.95)

		self.play(Write(explanation))
		self.play(FadeIn(time_text))
		self.wait(2)



class NaiveRangeQuery(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Naive Range Sum").move_to(UP*3)
		self.play(Write(title))


		counts = [random.randint(0, 20) for _ in range(14)]

		ag = ArrayGroup(counts)
		for e in ag.array_group:
			self.play(Create(e), run_time=0.07)


		query = Text("sumBetween(2, 7)", font_size=24, color=PASTEL_BLUE).move_to(UP*2)
		hb = HintBox(query, PASTEL_BLUE, 1.75)
		self.play(FadeIn(hb.box))


		total_label = Text("total = ", font_size=24)
		total_ans = Text("0", font_size=24)
		total_group = VGroup(total_label, total_ans).arrange(RIGHT).move_to(DOWN*2)
		self.play(Write(total_group))


		arrow = Arrow(DOWN, UP, color=PASTEL_TEAL).scale(0.3)
		arrow.next_to(ag.get_i(2), DOWN)
		self.play(FadeIn(arrow))


		total = 0

		for i in range(2, 8):
			total += counts[i]

			new_total = Text(f"{total}", font_size=24).move_to(total_group[1].get_center())

			self.play(
				arrow.animate.next_to(ag.get_i(i), DOWN),
				ag.get_i(i).animate.set_color(PASTEL_TEAL),
				Transform(total_group[1], new_total),
				run_time=0.7
			)

		answer = Text(f"= {str(total)}", font_size=24)
		answer.next_to(query, RIGHT)

		self.play(FadeIn(answer))
		self.wait(2)


		complexity = Text("Query the Range Sum: O(n)", font_size=24, t2c={"O(n)": PASTEL_RED}).move_to(query.get_center())
		self.play(FadeOut(answer), hb.change_text(complexity))
		self.wait(2)


		timeline = NumberLine(
			x_range=[0, 100, 10],
			length=11,
			include_numbers=False,
			include_ticks=True,
		).move_to(DOWN)

		left_label = Text("0", font_size=24, color=GRAY)
		left_label.next_to(timeline.n2p(0), DOWN)

		right_label = Text("28800", font_size=24, color=GRAY)
		right_label.next_to(timeline.n2p(100), DOWN)

		labels = VGroup(left_label, right_label)

		self.play(FadeOut(ag.array_group), FadeOut(arrow), FadeOut(total_group), FadeIn(timeline), FadeIn(labels))
		self.wait(2)


		queries = [tuple(sorted((random.randint(0, 100), random.randint(0, 100)))) for _ in range(10)]

		intervals = VGroup()
		colors = [PASTEL_TEAL, PASTEL_BLUE, PASTEL_INDIGO, PASTEL_PURPLE, PASTEL_PINK]

		for row, (l, r) in enumerate(queries):
			left = timeline.n2p(l)
			right = timeline.n2p(r)

			interval = Line(
				left,
				right,
				color=colors[row % len(colors)],
				stroke_width=12,
				stroke_opacity=0.25,
			)

			interval.shift(UP*(0.1 + row*0.1))
			intervals.add(interval)

			self.play(Create(interval))
		self.wait(2)


		repeated_text = Text("Repeated work from re-scanning ranges.", font_size=20, color=GRAY_B).move_to(DOWN*3)
		self.play(Write(repeated_text))

		for interval in intervals:
			dot = Dot(interval.get_start(), color=PASTEL_BLUE, radius=0.06)
			self.add(dot)

			self.play(MoveAlongPath(dot, interval), run_time=0.8, rate_func=linear)
			self.remove(dot)

		self.wait(2)


		question = Text("Could we save time using precomputation?", font_size=24, t2c={"precomputation": PASTEL_BLUE}).move_to(query.get_center())
		self.play(hb.change_text(question))
		self.wait(2)



class PrefixSumRangeQuery(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Prefix Sum Approach").move_to(UP*3)
		self.play(Write(title))


		complexity = Text("Precomputation: O(n)", font_size=24, t2c={"O(n)": PASTEL_RED}).move_to(UP*2)
		hb = HintBox(complexity, PASTEL_INDIGO, 1.75)
		self.play(FadeIn(hb.box))


		counts = [random.randint(0, 20) for _ in range(11)]

		ag = ArrayGroup(counts)

		counts_title = Text("data", font_size=20, color=GRAY).move_to(LEFT*6)
		self.play(Write(counts_title))
		for e in ag.array_group:
			self.play(Create(e), run_time=0.07)
		self.wait(2)

		prefix = [counts[0]]
		for i in range(1, len(counts)):
			prefix.append(prefix[i-1]+counts[i])

		ps_title = Text("prefixSum", font_size=20, color=GRAY).move_to(LEFT*6 + DOWN)
		
		ag_p = ArrayGroup(prefix)
		ag_p.array_group.shift(DOWN)
		self.play(Write(ps_title))
		self.play(FadeIn(ag_p.get_brackets()))
		self.wait(2)


		ps_desc = Text("prefixSum[i] = total sum of runners with PB <= i seconds.", font_size=20, t2c={"prefixSum[i]": PASTEL_INDIGO}).move_to(DOWN*3)
		self.play(Write(ps_desc))
		self.wait(2)


		def get_underline_between(i, j, colour=PASTEL_PURPLE):
			l, r = ag.get_i(i).get_left()+LEFT*0.1, ag.get_i(j).get_right()+RIGHT*0.1
			return Rectangle(width=r[0]-l[0], height=1, fill_color=colour, fill_opacity=0.1, stroke_width=0).move_to((l+r)/2)

		underline = get_underline_between(0, 0)
		self.add(underline)

		self.play(Transform(ag.get_i(0).copy(), ag_p.get_i(0)))
		self.wait(0.5)       

		for i in range(1, len(ag_p.get_array_group())):
			self.play(Transform(underline, get_underline_between(0, i)))

			prev = ag_p.get_i(i-1).copy()
			cur = ag.get_i(i).copy()
			zum = VGroup(prev, cur)

			self.play(prev.animate.move_to(ag_p.get_i(i).get_center()))            
			self.play(cur.animate.move_to(ag_p.get_i(i).get_center()))
			self.play(Transform(zum, ag_p.get_i(i)))

		self.wait(2)
		self.play(FadeOut(underline))

		complexity_2 = Text("Query the Range Sum: O(1)", font_size=24, t2c={"O(1)": GREEN}).move_to(UP*1.75)
		self.play(Transform(complexity, complexity_2))
		self.wait(2)


		query = Text("sumBetween(left, right)", font_size=20, color=PASTEL_INDIGO).move_to(UP)
		query_2 = Text("= prefixSum[right] - prefixSum[left-1]", font_size=20).move_to(UP)
		query_group = VGroup(query, query_2).arrange(RIGHT).move_to(UP*1.25)

		self.play(Write(query_group[0]))
		self.wait(2)
		self.play(FadeIn(query_group[1]))
		self.wait(2)


		def highlight(i, colour):
			self.play(ag_p.get_i(i).animate.set_color(colour))

			l, r = ag.get_i(0).get_left()+LEFT*0.1, ag.get_i(i).get_right()+RIGHT*0.1
			rect = Rectangle(width=r[0]-l[0], height=1, fill_color=colour, fill_opacity=0.1, stroke_width=0).move_to((l+r)/2)
			self.play(GrowFromEdge(rect, LEFT))

			return rect


		def quick_example(i=None, j=None, show_rects=False):
			boundaries = (tuple(sorted((random.randint(1, 10), random.randint(1, 10)))))
			if i != None:
				boundaries = (i, j)

			query_ex = Text(f"sumBetween({str(boundaries[0])}, {str(boundaries[1])})", font_size=20, color=PASTEL_INDIGO)
			query_2_ex = Text(f"= prefixSum[{str(boundaries[1])}] - prefixSum[{str(boundaries[0])}-1]", font_size=20)
			if i == 0:
				query_2_ex = Text(f"= prefixSum[{str(boundaries[1])}]", font_size=20)

			query_group = VGroup(query_ex, query_2_ex).arrange(RIGHT).move_to(UP*1.25)

			self.play(FadeIn(query_group))
			self.wait(2)

			ans_text = VGroup(
				Text(str(ag_p.array[boundaries[1]]), font_size=20, color=PASTEL_PURPLE),
				Text("-", font_size=20),
				Text(str(ag_p.array[boundaries[0]-1]), font_size=20, color=PASTEL_RED),
				Text(f"= {str(ag_p.array[boundaries[1]]-(0 if boundaries[0] == 0 else ag_p.array[boundaries[0]-1]))}", font_size=20)
			).arrange(RIGHT).move_to(DOWN*2)

			long_rect = None
			if show_rects:
				long_rect = highlight(boundaries[1], PASTEL_PURPLE)
			self.play(ag_p.get_i(boundaries[1]).animate.set_color(PASTEL_PURPLE))
			self.play(ReplacementTransform(ag_p.get_i(boundaries[1])[1][1].copy(), ans_text[0]))
			self.wait(2)

			if i > 0:
				short_rect = None
				if show_rects:
					short_rect = highlight(boundaries[0]-1, PASTEL_RED)
				self.play(ag_p.get_i(boundaries[0]-1).animate.set_color(PASTEL_RED))
				self.play(FadeIn(ans_text[1]), ReplacementTransform(ag_p.get_i(boundaries[0]-1)[1][1].copy(), ans_text[2]))
				self.wait(2)

			remaining = get_underline_between(boundaries[0], boundaries[1], colour=PASTEL_PURPLE)
			if show_rects:
				self.play(FadeOut(short_rect), FadeOut(long_rect), FadeIn(remaining))
			else:
				self.play(FadeIn(remaining))

			if i > 0:
				self.play(FadeIn(ans_text[3]))
			self.wait(2)

			self.play(FadeOut(ans_text), FadeOut(query_group), ag_p.array_group.animate.set_color(WHITE), FadeOut(remaining))

		self.play(FadeOut(query_group))
		quick_example(i=2, j=7, show_rects=True)
		quick_example(i=4, j=9, show_rects=False)
		quick_example(i=0, j=6, show_rects=False)



class PrefixSumUpdate(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Prefix Sum Approach").move_to(UP*3)
		self.play(Write(title))


		counts = [random.randint(0, 20) for _ in range(11)]

		counts_title = Text("data", font_size=20, color=GRAY).move_to(LEFT*6)
		self.play(Write(counts_title))

		ag = ArrayGroup(counts)
		for e in ag.array_group:
			self.play(Create(e), run_time=0.07)
		self.wait(2)


		prefix = [counts[0]]
		for i in range(1, len(counts)):
			prefix.append(prefix[i-1]+counts[i])

		prefix_title = Text("prefixSum", font_size=20, color=GRAY).move_to(LEFT*6 + DOWN)
		self.play(Write(prefix_title))
		
		ag_p = ArrayGroup(prefix)
		ag_p.array_group.move_to(DOWN)
		for e in ag_p.array_group:
			self.play(Create(e), run_time=0.07)
		self.wait(2) 


		complexity = Text("Update: O(n)", font_size=24, t2c={"O(n)": PASTEL_RED})
		hb = HintBox(complexity, PASTEL_INDIGO, 1.75)
		self.play(FadeIn(hb.box))
		self.wait(2)


		i, new_val = 3, 7

		query = Text(f"update({str(i)}, {str(new_val)})", font_size=20, color=PASTEL_INDIGO)
		query_group = VGroup(query).arrange(RIGHT).move_to(UP*1.25)
		self.play(complexity.animate.move_to(UP*1.75), Write(query))


		def highlight(i, j, colour):
			l, r = ag.get_i(i).get_left()+LEFT*0.1, ag.get_i(j).get_right()+RIGHT*0.1
			rect = Rectangle(width=r[0]-l[0], height=1, fill_color=colour, fill_opacity=0.1, stroke_width=0).move_to((l+r)/2)
			self.play(GrowFromEdge(rect, LEFT))

			return rect

		rect = highlight(i, i, PASTEL_PURPLE)
		plus_one = Text(f"+{new_val}", font_size=16, color=GREEN).move_to(ag.get_i(i).get_right())
		self.play(ag.change_i(i, new_val), FadeIn(plus_one), plus_one.animate.shift(UP*0.25))
		self.remove(plus_one)
		self.wait(2)


		self.play(*[ag_p.get_i_num(i).animate.set_color(PASTEL_RED) for i in range(3, len(ag_p.array))])
		self.wait(1)
		self.play(
			FadeOut(rect), 
			*[ag_p.get_i_num(i).animate.set_color(WHITE) for i in range(3, len(ag_p.array))]
		)

		self.play(*[FadeOut(ag_p.get_i_num(i)) for i in range(3, len(ag_p.array))])
		self.wait(1)


		for j in range(i, len(ag_p.get_array_group())):
			prev = ag_p.get_i(j-1).copy()
			cur = ag.get_i(j).copy()
			zum = VGroup(prev, cur)

			self.play(prev.animate.move_to(ag_p.get_i(j).get_center()))            
			self.play(cur.animate.move_to(ag_p.get_i(j).get_center()))
			
			self.play(FadeOut(cur), FadeOut(prev), ag_p.change_i(j, new_val))

		self.wait(2)



def index_to_v_part(index, v_parts):
	# This happens every lsb*2 elements
	i = int((index-lsb(index))/(lsb(index)*2))
	return v_parts[int(math.log2(lsb(index)))][i]

def get_range_line(index, v_parts):
	box_width = 0.6
	buff = 0.1

	v_part = index_to_v_part(index, v_parts)
	target_v_part = index_to_v_part(index-lsb(index)+1, v_parts)

	start_x = (v_part.get_center() + RIGHT*(box_width/2))[0]
	end_x = (target_v_part.get_center() + LEFT*(box_width/2))[0]
	y = v_part.get_top()[1] + UP[1]*0.2

	line = Line(
		start=[start_x, y, 0],
		end=[end_x, y, 0], 
		color=v_part[1][0].color,
		stroke_width=8
	)
	return line



class FenwickTreeExample(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		helper = Text("Fenwick Tree Example")
		hb = HintBox(helper, PASTEL_PINK)
		self.play(Create(hb.box))
		self.wait(2)

		array = [9, 7, -6, 1, -5, -2, 17, 4, -14, 16, -3, -10, -3, 12]
		ft = FenwickTree(array)
		ft.v_array.shift(UP*1.5)
		self.play(Create(ft.v_array))
		self.wait(2)

		colours = [PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO]

		def change_helper(k):
			text_one = Text("Fenwick Tree Example", font_size=24)
			suffix = '1' + '0'*k
			colour = colours[k]
			text_two = Text(
				f"bin(i) ends in {suffix} -> highest power of 2 dividing i is 2^{k} = {2**k}", 
				font_size=20, t2c={f"{suffix}": colour, f"2^{k}": colour}
			)
			text_group = VGroup(text_one, text_two).arrange(DOWN)
			self.play(hb.change_text(text_group))

		def flash_lsb(k, colour):
			anims = []
			for i in ft.get_l_k_bit(k):
				anims.append(Indicate(ft.get_i(ft.v_array, i-1)[1][1], color=colour))
			self.play(*anims)


		v_parts = VGroup()
		rule = Text("bit[i] stores the single element at data[i]", font_size=20).move_to(DOWN*3)

		for k in range(0, 4):
			change_helper(k)
			self.wait(1)

			if k == 0:
				self.play(AddTextLetterByLetter(rule), run_time=0.5)
			else:
				new_rule = Text(f"bit[i] stores the range sum of data from index i-{2**k}+1 to i inclusive", font_size=20, t2c={str(2**k): colours[k]}).move_to(DOWN*3)
				self.play(Transform(rule, new_rule))


			flash_lsb(k, colour=colours[k])
			rectangles = ft.make_rect_ranges(colours[k], k)
			self.play(*[GrowFromEdge(r, RIGHT) for r in rectangles])
			self.wait(2)

			source = ft.make_v_ranges(colours[k], k)
			target = ft.make_part(colours[k], k)
			v_parts.add(target)

			for i in range(0, len(source)):
				self.play(ReplacementTransform(source[i], target[i]))

			self.play(FadeOut(rectangles))
			self.wait(2)

		self.play(
			FadeOut(rule),
			hb.change_text(Text("Ranges widen by a factor of 2", font_size=24))
		)


		lines = VGroup()
		for k in range(0, 4):
			anims = []
			for index in ft.get_l_k_bit(k):
				range_line = get_range_line(index, v_parts)
				anims.append(GrowFromEdge(range_line, RIGHT))
				lines.add(range_line)
			self.play(*anims)



		self.play(
			*[v_parts[i].animate.shift(UP*(2-(i+1)*0.5)) for i in range(0, len(v_parts))], 
			FadeIn(ft.v_bit[0]), FadeIn(ft.v_bit[2]), FadeOut(lines)
		)
		self.wait(2)



class FenwickTreePointQuery(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		helper = Text("Fenwick Tree Query")
		hb = HintBox(helper, PASTEL_PINK)
		self.play(Create(hb.box))
		self.wait(2)

		array = [9, 7, -6, 1, -5, -2, 17, 4, -14, 16, -3, -10, -3, 12]
		ft = FenwickTree(array)
		ft.v_array.shift(UP*1.5)
		self.play(Create(ft.v_array))
		self.wait(2)

		colours = [PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO]

		v_parts = VGroup()
		for k in range(0, 4):
			rectangles = ft.make_rect_ranges(colours[k], k)
			self.play(*[GrowFromEdge(r, RIGHT) for r in rectangles])

			source = ft.make_v_ranges(colours[k], k)
			target = ft.make_part(colours[k], k)
			v_parts.add(target)

			self.play(
				*[ReplacementTransform(source[i], target[i]) for i in range(0, len(source))],
				FadeOut(rectangles)
			)


		text_one = Text("Find the Range Sum from Index 1 to 11 (Inclusive)", font_size=24)
		text_two = Text("sumUpTo(11)", font_size=20, color=PASTEL_PINK)
		text_group = VGroup(text_one, text_two).arrange(DOWN)

		self.play(hb.change_text(text_group))
		self.wait(2)

		def create_equation(index):
			start = index - lsb(index) + 1
			end = index

			return MathTex(f"lsb({index}) = {lsb(index)} \\rightarrow bit[{index}] = \\sum\\limits_{{k={start}}}^{{{end}}} data[k]", font_size=24)

		def create_equation_2(index):
			return MathTex(f"i = {index} - lsb({index}) = {index} - {lsb(index)} = {index - lsb(index)}", font_size=24)


		cb = CodeBlock(
			["sum = 0", "while i > 0:", "* Add bit[i] to sum", "* Set i = i - lsb(i)"],
			font_size=16, 
			pos=DOWN*3 + LEFT*4, 
			stroke_colour=PASTEL_RED,
			fill_colour=BLACK,
			arrow_colour=PASTEL_RED
		)
		self.play(FadeIn(cb.code_block))
		cb.arrow.next_to(cb.line_group[2], LEFT)


		bottom_right = Text("i = 1", font_size=24, color=PASTEL_RED).move_to(DOWN*2.75 + RIGHT*4)


		sum_text = Text("sum =", font_size=20)
		term_1 = Text("-3", font_size=20, color=PASTEL_PINK)
		term_2 = Text(" + 2", font_size=20, color=PASTEL_PURPLE)
		term_3 = Text(" + 25", font_size=20, color=PASTEL_INDIGO)
		v_sum = VGroup(sum_text, term_1, term_2, term_3).arrange(RIGHT).move_to(DOWN*3)
		self.play(FadeIn(v_sum[0], shift=UP))
		self.wait(2)


		index = 11
		count = 0

		v_cur = index_to_v_part(index, v_parts)
		cur_rect = Rectangle(
			width=0.75, height=1.5, 
			fill_color=colours[int(math.log2(lsb(index)))], 
			fill_opacity=0.1,
			stroke_width=0
		).move_to(v_cur.get_center())

		eq_2 = None
		while index > 0:
			v_cur = index_to_v_part(index, v_parts)

			if eq_2 != None:
				self.play(FadeOut(eq_2))

			cur_rect_2 = Rectangle(
				width=0.75, height=1.5, 
				fill_color=colours[int(math.log2(lsb(index)))], 
				fill_opacity=0.1,
				stroke_width=0
			).move_to(v_cur.get_center())
			self.play(
				Transform(bottom_right, Text(f"i = {index}", font_size=24).move_to(DOWN*2.75 + RIGHT*4)), 
				Transform(cur_rect, cur_rect_2)
			)						
			self.wait(2)

			self.play(cb.move_arrow_to_line(2))
			eq_2 = create_equation(index).move_to(DOWN*3.5 + RIGHT*4)
			self.play(FadeIn(eq_2))
			self.wait(1)

			range_line = get_range_line(index, v_parts)
			self.play(GrowFromEdge(range_line, RIGHT))
			self.wait(1)

			self.play(ReplacementTransform(v_cur[1][2].copy(), v_sum[count+1]))
			self.wait(2)


			self.play(cb.move_arrow_to_line(3))
			self.play(Transform(eq_2, create_equation_2(index).move_to(DOWN*3.5 + RIGHT*4)))
			self.wait(1)

			index -= lsb(index)
			count += 1


		total = Text(f"sum = {-3 + 2 + 25}", font_size=20).move_to(DOWN*3)
		self.play(Transform(v_sum, total))
		self.wait(2)



class FenwickTreeUpdate(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		text_one = Text("Update Index 9 by Adding +5", font_size=24)
		text_two = Text("update(9, 5)", font_size=20, color=PASTEL_PINK)
		text_group = VGroup(text_one, text_two).arrange(DOWN)
		hb = HintBox(text_group, PASTEL_PINK)
		self.play(FadeIn(hb.box))
		self.wait(2)


		array = [9, 7, -6, 1, -5, -2, 17, 4, -14, 16, -3, -10, -3, 12]
		ft = FenwickTree(array)
		ft.v_array.shift(UP*1.5)
		self.play(Create(ft.v_array))
		self.wait(2)

		colours = [PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO]	

		v_parts = VGroup()
		for k in range(0, 4):
			target = ft.make_part(colours[k], k)
			v_parts.add(target)
		self.add(v_parts)

		self.play(GrowFromEdge(v_parts, DOWN))
		self.wait(2)


		def add_animation(a, v_a, index, delta):
			plus_one = Text(f"+{DELTA}", font_size=16, color=GREEN).move_to(ft.get_i(v_a, index).get_right())
			self.play(
				ft.update_i(a, v_a, index, delta),
				Transform(old_box, new_box),
				plus_one.animate.shift(UP*0.25)
			)
			self.remove(plus_one)
			self.wait(2)


		DELTA = 5
		INDEX = 9

		# Add the delta to index 9
		old_box = ft.get_i(ft.v_array, INDEX-1)[0]
		new_box = old_box.copy()
		new_box.stroke_color = PASTEL_BLUE
		new_box.stroke_width = 2
		new_box.height = 1.2

		add_animation(ft.array, ft.v_array, INDEX-1, DELTA)


		bottom_text = Text("Which values in bit include index 9 in their range sum?", font_size=20, t2c={"bit": PASTEL_PINK}).move_to(DOWN*3)
		self.play(AddTextLetterByLetter(bottom_text))
		self.wait(2)


		lines = VGroup()
		cur = INDEX
		while cur <= len(ft.array):
			range_line = get_range_line(cur, v_parts)
			lines.add(range_line)
			self.play(GrowFromEdge(range_line, RIGHT))
			cur += lsb(cur)
		self.wait(2)


		def create_equation_2(index):
			return MathTex(f"i = {index} + lsb({index}) = {index} + {lsb(index)} = {index + lsb(index)}", font_size=24)


		cb = CodeBlock(
			["while i < bit.size:", "* Add delta to bit[i]", "* Set i = i + lsb(i)"],
			font_size=16, 
			pos=DOWN*3 + LEFT*3, 
			stroke_colour=PASTEL_RED,
			fill_colour=BLACK,
			arrow_colour=PASTEL_RED
		)
		self.play(FadeOut(bottom_text), FadeIn(cb.code_block))
		cb.arrow.next_to(cb.line_group[1], LEFT)


		index = INDEX
		bottom_right = Text(f"i = {index}", font_size=24).move_to(DOWN*2.75 + RIGHT*3)

		v_cur = index_to_v_part(index, v_parts)
		cur_rect = Rectangle(
			width=0.75, height=1.5, 
			fill_color=colours[int(math.log2(lsb(index)))], 
			fill_opacity=0.1,
			stroke_width=0
		).move_to(v_cur.get_center())

		eq_2 = None
		while index <= len(ft.array):
			v_cur = index_to_v_part(index, v_parts)

			if eq_2 != None:
				self.play(FadeOut(eq_2))

			cur_rect_2 = Rectangle(
				width=0.75, height=1.5, 
				fill_color=colours[int(math.log2(lsb(index)))], 
				fill_opacity=0.1,
				stroke_width=0
			).move_to(v_cur.get_center())
			self.play(
				Transform(bottom_right, Text(f"i = {index}", font_size=24).move_to(DOWN*2.75 + RIGHT*3)), 
				Transform(cur_rect, cur_rect_2)
			)						
			self.wait(2)

			self.play(cb.move_arrow_to_line(1))
			
			v_old_val = v_cur[1][2]
			v_new_val = Text(str(ft.bit[index]+DELTA), font_size=24).move_to(v_old_val.get_center())

			plus_one = Text(f"+{DELTA}", font_size=16, color=GREEN).move_to(v_old_val.get_right())

			self.play(
				Transform(v_old_val, v_new_val),
				plus_one.animate.shift(UP*0.25)
			)
			self.remove(plus_one)
			self.wait(2)

			self.play(cb.move_arrow_to_line(2))	
			eq_2 = create_equation_2(index).move_to(DOWN*3.5 + RIGHT*3)
			self.play(FadeIn(eq_2))
			self.wait(1)

			index += lsb(index)

		self.wait(2)



class FenwickTreeConstruction(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		text_one = Text("Fenwick Tree Construction")
		hb = HintBox(text_one, PASTEL_PINK)
		self.play(FadeIn(hb.box))
		self.wait(2)


		array = [9, 7, -6, 1, -5, -2, 17, 4, -14, 16, -3, -10, -3, 12]
		ft = FenwickTree(array)
		ft.v_array.shift(UP*1.5)
		self.play(Create(ft.v_array))
		self.wait(2)

		ft.bit = [0]*(len(ft.array)+1)
		ft.v_bit = ft.make_v_bit()


		colours = [PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO]	

		v_parts = VGroup()
		for k in range(0, 4):
			target = ft.make_part(colours[k], k)
			v_parts.add(target)


		cb = CodeBlock(
			["for i in range [1, bit.size):", "* Add element in data to bit[i]", "* Add bit[i] to bit[parent(i)]"],
			font_size=16, 
			pos=DOWN*3 + LEFT*3, 
			stroke_colour=PASTEL_RED,
			fill_colour=BLACK,
			arrow_colour=PASTEL_RED
		)
		self.play(FadeIn(cb.code_block))
		cb.arrow.next_to(cb.line_group[1], LEFT)

		index = 1
		bottom_right = Text(f"i = {index}", font_size=24).move_to(DOWN*2.75 + RIGHT*3)


		def create_equation_2(index):
			return MathTex(f"parent(i) = {index} + lsb({index}) = {index} + {lsb(index)} = {index + lsb(index)}", font_size=24)

		def change_helper(added_text):
			text_one = Text("Construct the Fenwick Tree", font_size=24)
			text_two = Text("fenwickTree(data)", font_size=20, color=PASTEL_PINK)
			text_group = VGroup(text_one, text_two).arrange(DOWN)
			text_group.move_to(hb.box.get_center() + LEFT*4)

			added_text.move_to(hb.box.get_center() + RIGHT*3)
			new_helper = VGroup(text_group, added_text)

			return Transform(hb.box[1], new_helper)


		shown = [False for _ in range(len(ft.array)+1)]
		line_index = [VGroup() for _ in range(len(ft.array) + 1)]

		eq_2 = None
		while index <= len(ft.array):
			v_cur = index_to_v_part(index, v_parts)

			if eq_2 != None:
				self.play(FadeOut(eq_2))

			self.play(
				Transform(bottom_right, 
					Text(f"i = {index}", font_size=24).move_to(DOWN*2.75 + RIGHT*3)
				)
			) 

			if not shown[index]:
				self.play(FadeIn(v_cur))
				shown[index] = True


			self.play(cb.move_arrow_to_line(1))

			# Update bit[i]
			new_value = ft.bit[index]+ft.array[index-1]
			ft.bit[index] = new_value

			v_old_val = v_cur[1][2]
			v_new_val = Text(str(new_value), font_size=24).move_to(v_old_val.get_center())

			data_element = ft.get_i(ft.v_array, index-1)[1][2].copy()
			plus_one = Text(f"+{ft.array[index-1]}", font_size=16, color=GREEN).move_to(v_old_val.get_right()+RIGHT*0.25)

			self.play(
				Transform(data_element, plus_one)
			)
			self.play(
				Transform(v_old_val, v_new_val),
				data_element.animate.shift(UP*0.25)
			)
			self.remove(data_element)


			cur_line = get_range_line(index, v_parts)
			if len(line_index[index]) == 0:
				line_index[index].add(cur_line)
				self.play(GrowFromEdge(cur_line, LEFT))
			else:
				self.play(Transform(line_index[index], cur_line))
				line_index[index] = VGroup(cur_line)


			# Update parent
			self.play(cb.move_arrow_to_line(2))

			eq_2 = create_equation_2(index).move_to(DOWN*3.5 + RIGHT*3)
			self.play(FadeIn(eq_2))

			parent = index + lsb(index)
			if parent <= len(ft.array):
				v_parent = index_to_v_part(parent, v_parts)

				if not shown[parent]:
					self.play(FadeIn(v_parent))
					shown[parent] = True

				parent_rect = Rectangle(
					width=0.75, height=1.5, 
					fill_color=colours[int(math.log2(lsb(parent)))], 
					fill_opacity=0.1,
					stroke_width=0
				).move_to(v_cur.get_center())
				self.play(parent_rect.animate.move_to(v_parent.get_center()))	


				new_value = ft.bit[parent]+ft.bit[index]
				ft.bit[parent] = new_value

				v_old_val = v_parent[1][2]
				v_new_val = Text(str(new_value), font_size=24).move_to(v_old_val.get_center())

				data_element = v_cur[1][2].copy()
				plus_one = Text(f"+{ft.bit[index]}", font_size=16, color=GREEN).move_to(v_parent.get_right()+RIGHT*0.25)

				self.play(
					Transform(data_element, plus_one)				
				)

				cur_line_2 = cur_line.copy()			

				cur_y = cur_line_2.get_center()[1]
				new_y = v_parent.get_top()[1] + UP[1]*0.2

				self.play(
					Transform(v_old_val, v_new_val),
					data_element.animate.shift(UP*0.25),
					cur_line_2.animate.shift(UP*(new_y-cur_y))
				)
				self.remove(data_element)

				line_index[parent].add(cur_line_2)
				self.play(FadeOut(parent_rect))

			index += 1

		self.wait(2)

		self.play(
			*[v_parts[i].animate.shift(UP*(2-(i+1)*0.5)) for i in range(0, len(v_parts))], 
			FadeIn(ft.v_bit[0]), FadeIn(ft.v_bit[2])
		)
		self.wait(2)



class BinaryTheory(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		rule_1 = Text("For each index, i, consider the highest power of 2 which divides i.", font_size=16, t2c={' i': PASTEL_TEAL})
		rule_2 = Text("Suppose that is 2^k.", font_size=16, t2c={'2^k': PASTEL_PURPLE})
		rule_3 = Text("Then bit[i] stores the range sum of the of the subarray of size 2^k\nending at index i (one-indexed).", font_size=16, t2c={'2^k': PASTEL_PURPLE, 'bit[i]': PASTEL_BLUE})
		rule = VGroup(rule_1, rule_2, rule_3).arrange(DOWN, buff=0.2)

		hb = HintBox(rule, PASTEL_TEAL)
		self.play(FadeIn(hb.box))
		self.wait(2)


		question = Text("How do we find the highest power of 2 which divides i?", font_size=24, t2c={' i': PASTEL_TEAL})
		self.play(AddTextLetterByLetter(question))
		self.wait(2)

		answer_1 = Text("The least-significant set bit!", font_size=20)
		answer_2 = Text("(The 1-bit closest to the right)", font_size=16, color=PASTEL_TEAL)
		answer = VGroup(answer_1, answer_2).arrange(DOWN, buff=0.1).next_to(question, DOWN)
		self.play(FadeIn(answer))
		self.wait(10)

		bb = BinaryByte(204)
		self.play(FadeOut(question), FadeOut(answer))
		self.play(FadeIn(bb.v_binary))


		ascending_arrow = Arrow(start=bb.v_binary[7].get_top(), end=bb.v_binary[0].get_top(), stroke_width=1)
		ascending_text = Text("ascending powers of 2", font_size=16)
		ascending_group = VGroup(ascending_text, ascending_arrow).arrange(DOWN, buff=0.1).next_to(bb.v_binary, UP)
		self.play(GrowFromEdge(ascending_group, RIGHT))
		self.wait(2)


		question = Text("Is 204 divisible by 4 (2^2)?", font_size=24, t2c={'2^3': bb.get_bit(3)[0].color}).move_to(DOWN*1.5)
		self.play(Write(question))
		self.wait(2)


		equation = VGroup(
			MathTex("204 = "),
			bb.get_bit(7)[0].copy(),
			MathTex("+"),
			bb.get_bit(6)[0].copy(),
			MathTex("+"),
			bb.get_bit(3)[0].copy(),
			MathTex("+"),
			bb.get_bit(2)[0].copy()
		).arrange(RIGHT).move_to(DOWN*2)
		self.play(LaggedStart(*[FadeIn(item) for item in equation], lag_ratio=0.2))
		self.wait(2)

		equation_2 = VGroup(
			MathTex("= "),
			bb.get_bit(2)[0].copy(),
			MathTex("("),
			bb.get_bit(5)[0].copy(),
			MathTex("+"),
			bb.get_bit(4)[0].copy(),
			MathTex("+"),
			bb.get_bit(1)[0].copy(),
			MathTex("+"),
			bb.get_bit(0)[0].copy(),
			MathTex(")")
		).arrange(RIGHT).move_to(DOWN*2.5)
		self.play(LaggedStart(*[FadeIn(item) for item in equation_2], lag_ratio=0.2))
		self.wait(2)


		green_check = Text("✓", color=GREEN).move_to(question.get_center())
		self.play(SpinInFromNothing(green_check))
		self.wait(1)
		self.play(FadeOut(green_check), FadeOut(equation_2))
		self.wait(2)


		question_2 = Text("Is 204 divisible by 8 (2^3)?", font_size=24, t2c={'2^3': bb.get_bit(3)[0].color}).move_to(DOWN*1.5)
		self.play(Transform(question, question_2))
		self.wait(2)

		equation_2 = VGroup(
			MathTex("= "),
			bb.get_bit(3)[0].copy(),
			MathTex("("),
			bb.get_bit(4)[0].copy(),
			MathTex("+"),
			bb.get_bit(3)[0].copy(),
			MathTex("+"),
			bb.get_bit(0)[0].copy(),
			MathTex(")"),
			MathTex("+"),
			bb.get_bit(2)[0].copy()
			
		).arrange(RIGHT).move_to(DOWN*2.5)
		self.play(LaggedStart(*[FadeIn(item) for item in equation_2], lag_ratio=0.2))
		self.wait(2)


		red_x = Text("X", color=RED).move_to(question.get_center())
		self.play(SpinInFromNothing(red_x))
		self.wait(1)
		self.play(FadeOut(red_x), FadeOut(equation_2))
		self.wait(2)


		self.play(Circumscribe(bb.get_bit(2), color=bb.get_bit(2)[0].color), run_time=2)
		self.wait(2)



class TwosComplement(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title = Text("Two's Complement")

		hb = HintBox(title, PASTEL_TEAL)
		self.play(FadeIn(hb.box))
		self.wait(2)


		number_line = NumberLine(
			x_range=[-8, 7, 1],
			length=12,
			include_numbers=True,
			include_tip=False,
			stroke_width=2,
		).shift(DOWN)
		self.play(Create(number_line))
		self.wait(2)


		bins, instructions = VGroup(), VGroup()
		right = 6
		for i in range(7, -9, -1):
			cur = i
			if i < 0:
				cur = -1*i

			num_bin = bin(cur)[2:]
			num_bin = '0'*(4-len(num_bin)) + num_bin

			if i == -1:
				instructions_1 = Text("1. Take the positive equivalent.", font_size=24).move_to(UP*2)
				self.play(Write(instructions_1))
				instructions.add(instructions_1)

			binary = Text(num_bin, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN*0.5)
			self.play(Write(binary))

			# Show two's complement
			if i < 0:
				if i == -1:
					instructions_2 = Text("2. Flip all the bits.", font_size=24).next_to(instructions_1, DOWN)
					self.play(Write(instructions_2))
					instructions.add(instructions_2)

				flip_bits = ""
				for c in num_bin:
					flip_bits += ('1' if c == '0' else '0')

				binary_2 = Text(flip_bits, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN*0.5)
				self.play(Transform(binary, binary_2))

				if i == -1:
					instructions_3 = Text("3. Add 1.", font_size=24).next_to(instructions_2, DOWN)
					self.play(Write(instructions_3))
					instructions.add(instructions_3)

				num_bin = bin(i & 0b1111)[2:]
				binary_3 = Text(num_bin, color=GRAY, font_size=16).move_to(RIGHT*right + DOWN*0.5)
				self.play(Transform(binary, binary_3))

			right -= 0.8
			bins.add(binary)

		self.wait(2)



class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font=MONOSPACE_FONT)

		title_text = Text("Fenwick Trees").shift(UP*3)
		self.add(title_text)

		question_text = Text("O(log n) Range Sum Queries and Point Updates", 
			font_size=24,
			t2c={"O(log n)": PINK, "Queries": PURPLE, "Updates": BLUE}
		).shift(UP*2)
		self.add(question_text)


		array = [9, 7, -6, 1, -5, -2, 17, 4, -14, 16, -3, -10, -3, 12]
		ft = FenwickTree(array)
		ft.v_array.shift(UP*0.5)
		self.add(ft.v_array)

		colours = [PASTEL_RED, PASTEL_PINK, PASTEL_PURPLE, PASTEL_INDIGO]	

		v_parts = VGroup()
		for k in range(0, 4):
			target = ft.make_part(colours[k], k)
			v_parts.add(target)
		self.add(v_parts.shift(DOWN))


		lines = VGroup()
		for k in range(0, 4):
			for index in ft.get_l_k_bit(k):
				range_line = get_range_line(index, v_parts)
				lines.add(range_line)
		self.add(lines)