from manim import *
import random


config.background_color = "#15131c"
config.pixel_width = 450
config.pixel_height = 800
config.frame_width = 8


class Socket(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Network Sockets", font_size=48).shift(UP*2)
		self.play(title.animate.shift(UP*2.5))

		socket_object = RoundedRectangle(
			width=3, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(ORIGIN+LEFT)
		socket_text = Text("Socket", font_size=24).move_to(socket_object.get_center())	

		send_arrow = Arrow(start=socket_object.get_right(), end=socket_object.get_right()+RIGHT*3).shift(UP*0.5)
		send_text = Text("send", font_size=24, color=ORANGE).move_to(send_arrow.get_center()+UP*0.5)
		send_group = VGroup(send_arrow, send_text)

		recv_arrow = Arrow(start=socket_object.get_right()+RIGHT*3, end=socket_object.get_right()).shift(DOWN*0.5)
		recv_text = Text("recv", font_size=24, color=GREEN).move_to(recv_arrow.get_center()+DOWN*0.5)
		recv_group = VGroup(recv_arrow, recv_text)

		socket = VGroup(socket_object, socket_text, send_group, recv_group).move_to(ORIGIN)

		self.play(Create(socket_object))
		self.play(Write(socket_text))
		self.wait(2)

		self.play(GrowArrow(send_arrow), Write(send_text))
		self.play(GrowArrow(recv_arrow), Write(recv_text))
		self.wait(2)

		self.play(socket.animate.shift(UP*2))


		socket_address = RoundedRectangle(
			width=4.5, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(ORIGIN + DOWN)

		ip_text = Text("IP address: x.x.x.x", font_size=24, color=BLUE)
		port_text = Text("Port: 0-65535", font_size=24, color=PURPLE)
		protocol_text = Text("Protocol: TCP/UDP", font_size=24, color=LIGHT_PINK)
		socket_address_text = VGroup(ip_text, port_text, protocol_text).arrange(DOWN).move_to(socket_address.get_center())

		self.play(Create(socket_address))
		self.play(Write(ip_text))
		self.play(Write(port_text))
		self.play(Write(protocol_text))
		self.wait(2)

		socket_address_group = VGroup(socket_address, socket_address_text)
		socket_object_group = VGroup(socket_object, socket_text)

		send_arrow_2 = DoubleArrow(start=LEFT+UP*2, end=RIGHT+UP*2)
		send_text_2 = Text("send/recv", font_size=18, color=GREEN).move_to(send_arrow_2.get_center()+UP)
		send_group_2 = VGroup(send_arrow_2, send_text_2)

		tcp_title = Text("TCP", font_size=48).shift(UP*4.5)

		self.play(
			socket_object_group.animate.scale(0.8).move_to(LEFT*2+UP*2),
			socket_address_group.animate.scale(0.75).move_to(LEFT*2+DOWN),
			ReplacementTransform(VGroup(send_group, recv_group), send_group_2),
			Transform(title, tcp_title)
		)

		socket_object_2 = socket_object_group.copy().move_to(RIGHT*2+UP*2)
		socket_address_2 = socket_address_group.copy().move_to(RIGHT*2+DOWN)

		self.play(
			Create(socket_object_2),
			Create(socket_address_2)
		)
		self.wait(2)

		socket_addresses = VGroup(socket_address_group, socket_address_2)

		five_tuple = RoundedRectangle(
			width=5, height=3,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(ORIGIN + DOWN)

		ip_text = Text("IP address 1: x.x.x.x", font_size=24, color=BLUE)
		port_text = Text("Port 1: 0-65535", font_size=24, color=PURPLE)
		ip_text_2 = Text("IP address 2: x.x.x.x", font_size=24, color=BLUE)
		port_text_2 = Text("Port 2: 0-65535", font_size=24, color=PURPLE)
		protocol_text = Text("Protocol: TCP", font_size=24, color=LIGHT_PINK)
		five_tuple_text = VGroup(ip_text, port_text, ip_text_2, port_text_2, protocol_text).arrange(DOWN).move_to(five_tuple.get_center())

		five_tuple_group = VGroup(five_tuple, five_tuple_text).scale(0.75)
		self.play(ReplacementTransform(socket_addresses, five_tuple_group))
		self.wait(2)


		line = Line(start=RIGHT+UP*2, end=LEFT+UP*2, color=GREEN, stroke_width=20)

		reliable = Text("Reliable", font_size=20).move_to(DOWN*3)
		self.play(ShowPassingFlash(line, time_width=1), Write(reliable))

		ordered = Text("Ordered", font_size=20).move_to(DOWN*3.5)
		self.play(ShowPassingFlash(line, time_width=1), Write(ordered))

		red_line = Line(start=RIGHT+UP*2, end=UP*2, color=RED, stroke_width=20)
		error_checking = Text("Error-Checking", font_size=20).move_to(DOWN*4)
		self.play(ShowPassingFlash(red_line, time_width=1), Write(error_checking))

		retransmitted = Text("Retransmitted", font_size=20).move_to(DOWN*4.5)
		self.play(ShowPassingFlash(line, time_width=1), Write(retransmitted))
		self.wait(2)


		udp_title = Text("UDP", font_size=48).shift(UP*4.5)
		self.play(Transform(title, udp_title), FadeOut(reliable), FadeOut(ordered), FadeOut(error_checking), FadeOut(retransmitted))
		

		self.play(FadeOut(five_tuple_group), FadeOut(send_group_2), FadeOut(socket_object_2))

		connectionless = Text("Connectionless", font_size=20).move_to(DOWN*3)
		self.play(ShowPassingFlash(line, time_width=1), Write(connectionless))

		line_2 = Line(start=RIGHT+UP, end=LEFT+UP*2, color=GREEN, stroke_width=20)
		datagrams = Text("Datagrams", font_size=20).move_to(DOWN*3.5)
		self.play(ShowPassingFlash(line_2, time_width=1), Write(datagrams))

		red_line = Line(start=RIGHT+UP*3, end=LEFT+UP*2, color=RED, stroke_width=20)
		self.play(ShowPassingFlash(red_line, time_width=1))

		less_overhead = Text("Less Overhead", font_size=20).move_to(DOWN*4)
		self.play(ShowPassingFlash(line_2, time_width=1), Write(less_overhead))
		self.wait(2)
