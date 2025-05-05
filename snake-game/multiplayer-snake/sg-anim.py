from manim import *


config.background_color = "#15131c"


class MultiplayerIntro(Scene):
	def construct(self):
		Text.set_default(font="Monospace")


		server_box = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_width=10,
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN)
		server_text = Text("Server", font_size=24).move_to(server_box.get_center())
		server_group = VGroup(server_box, server_text)

		self.play(Create(server_group))


		client_box_1 = RoundedRectangle(
			width=3, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+UP*2.5+LEFT*4)
		client_text_1 = Text("Client 1", font_size=24, color=PURPLE).move_to(client_box_1.get_center())
		client_group_1 = VGroup(client_box_1, client_text_1).scale(0.75)

		self.play(Create(client_group_1))

		client_arrow_1 = CurvedArrow(start_point=client_box_1.get_bottom(), end_point=server_box.get_left(), color=PURPLE)
		self.add(client_arrow_1)

		keypress_text = Text("{'keypress': 'w'}", font_size=20)
		keypress_box = SurroundingRectangle(keypress_text, corner_radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=0.75)
		keypress = VGroup(keypress_box, keypress_text)

		self.play(Create(client_arrow_1), MoveAlongPath(keypress, client_arrow_1))
		self.wait(2)


		client_box_2 = RoundedRectangle(
			width=3, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+DOWN*2.5+RIGHT*4)
		client_text_2 = Text("Client 2", font_size=24, color=BLUE).move_to(client_box_2.get_center())
		client_group_2 = VGroup(client_box_2, client_text_2).scale(0.75)		

		self.play(Create(client_group_2))

		client_arrow_2 = CurvedArrow(start_point=client_box_2.get_top(), end_point=server_box.get_right(), color=BLUE)
		self.add(client_arrow_2)

		username_text = Text("{'username': 'ep1cg4m3r'}", font_size=20)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.75)
		username = VGroup(username_box, username_text)		

		self.play(Create(client_arrow_2), MoveAlongPath(username, client_arrow_2))
		self.wait(2)


		updates = VGroup(keypress, username)
		game_state = Text("{game_state}", font_size=20).move_to(server_text.get_center()+DOWN*0.5)

		self.play(ReplacementTransform(updates, game_state))
		self.wait(2)


		server_arrow_1 = CurvedArrow(start_point=server_box.get_top(), end_point=client_box_1.get_right(), color=MAROON, angle=PI/2)
		server_arrow_2 = CurvedArrow(start_point=server_box.get_bottom(), end_point=client_box_2.get_left(), color=MAROON, angle=PI/2)
		self.add(server_arrow_1)
		self.add(server_arrow_2)

		game_state_1_text = game_state.copy()
		game_state_1_box = SurroundingRectangle(game_state_1_text, corner_radius=0.2, stroke_width=0, fill_color=MAROON, fill_opacity=0.75)
		game_state_1 = VGroup(game_state_1_box, game_state_1_text)

		game_state_2_text = game_state.copy()
		game_state_2_box = SurroundingRectangle(game_state_2_text, corner_radius=0.2, stroke_width=0, fill_color=MAROON, fill_opacity=0.75)
		game_state_2 = VGroup(game_state_2_box, game_state_2_text)

		self.play(
			Create(server_arrow_1), 
			MoveAlongPath(game_state_1, server_arrow_1),
			Create(server_arrow_2), 
			MoveAlongPath(game_state_2, server_arrow_2)
		)
		self.wait(2)
		
		snek = RoundedRectangle(
			width=1.2, height=0.3,
			corner_radius=[0.1, 0.1, 0.1, 0.1],
			stroke_width=0,
			fill_color="GREEN",
			fill_opacity=1
		).shift(LEFT*0.7)
		food = Dot(radius=0.1, color=RED).shift(RIGHT*0.3)
		screen = VGroup(snek, food)

		self.play(
			Transform(client_text_1, screen.copy().move_to(client_box_1.get_center())),
			Transform(client_text_2, screen.copy().move_to(client_box_2.get_center())),
			FadeOut(game_state_1), FadeOut(game_state_2)
		)
		self.wait(2)


class MakeSnake(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		

		blue_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(LEFT)

		yellow_horizontal = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(RIGHT)

		blue_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#306998",
			fill_color="#306998",
			fill_opacity=1
		).shift(UP)

		yellow_vertical = RoundedRectangle(
			width=2, height=2,
			corner_radius=[0.5, 0.5, 0.5, 0],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).shift(DOWN)	

		eye_1 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(blue_vertical.get_center()).shift(UP*0.4 + LEFT*0.4)

		eye_2 = Circle(
			radius=0.2,
			color=WHITE,
			fill_opacity=1
		).move_to(yellow_vertical.get_center()).shift(DOWN*0.4 + RIGHT*0.4)
		
		python_logo = VGroup(blue_horizontal, yellow_horizontal, blue_vertical, yellow_vertical, eye_1, eye_2)
		self.play(Create(python_logo))


		snake_body = RoundedRectangle(
			width=5, height=1, 
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			color="#306998", 
			fill_opacity=1
		)

		snake_head = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color="#FFD43B",
			fill_color="#FFD43B",
			fill_opacity=1
		).move_to(snake_body.get_center()).shift(RIGHT*3)

		eye_3 = Circle(
			radius=0.1,
			color=WHITE,
			fill_opacity=1
		).move_to(snake_head.get_center()).shift(UP*0.2 + RIGHT*0.5)

		eye_4 = Circle(
			radius=0.1,
			color=WHITE,
			fill_opacity=1
		).move_to(snake_head.get_center()).shift(DOWN*0.2 + RIGHT*0.5)

		snake_boi = VGroup(snake_body, snake_head, eye_3, eye_4).move_to(ORIGIN)
		self.play(ReplacementTransform(python_logo, snake_boi))
		self.wait(10)



class Socket1(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

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

		send_arrow_2 = DoubleArrow(start=socket_object.get_right()+LEFT*2, end=socket_object.get_right()+RIGHT*2)
		send_text_2 = Text("send/recv", font_size=24, color=GREEN).move_to(send_arrow_2.get_center()+UP*0.5)
		send_group_2 = VGroup(send_arrow_2, send_text_2)

		self.play(
			socket_object_group.animate.move_to(LEFT*4+UP*2),
			socket_address_group.animate.scale(0.75).move_to(LEFT*4+DOWN),
			Transform(VGroup(send_group, recv_group), send_group_2)
		)

		socket_object_2 = socket_object_group.copy().move_to(RIGHT*4+UP*2)
		socket_address_2 = socket_address_group.copy().move_to(RIGHT*4+DOWN)

		self.play(
			Create(socket_object_2),
			Create(socket_address_2)
		)
		self.wait(2)


class Socket2(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		server_box = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+LEFT*3)
		server_text = Text("Server", font_size=24, color=MAROON).move_to(server_box.get_center())
		server_group = VGroup(server_box, server_text).scale(0.75)

		self.play(Create(server_group))


		client_box = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+RIGHT*3)
		client_text = Text("Client", font_size=24, color=TEAL).move_to(client_box.get_center())
		client_group = VGroup(client_box, client_text).scale(0.75)

		self.play(Create(client_group))

		server_client = VGroup(server_group, client_group)
		self.play(server_client.animate.shift(UP*2.75))
		self.wait(2)


		socket_text = Text("create socket", font_size=24, color=RED).scale(0.75).move_to(server_box.get_center()+DOWN)
		self.play(Write(socket_text))
		self.wait(2)

		bind_text = Text("bind to (host, port)", font_size=24, color=ORANGE).scale(0.75).move_to(socket_text.get_center()+DOWN)
		self.play(Write(bind_text))
		self.wait(2)

		listen_text = Text("socket.listen()", font_size=24, color=GOLD).scale(0.75).move_to(bind_text.get_center()+DOWN)
		self.play(Write(listen_text))
		self.wait(2)

		socket_text_2 = Text("create socket", font_size=24, color=BLUE).scale(0.75).move_to(client_box.get_center()+DOWN)
		self.play(Write(socket_text_2))
		self.wait(2)

		connect_text = Text("connect to server (host, port)", font_size=24, color=PURPLE).scale(0.75).move_to(socket_text_2.get_center()+DOWN*3)
		self.play(Write(connect_text))
		self.wait(2)

		accept_text = Text("accept connection", font_size=24, color=YELLOW).scale(0.75).move_to(listen_text.get_center()+DOWN)
		self.play(Write(accept_text))
		self.wait(2)


		conn_box = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(accept_text.get_center()+DOWN)
		conn_text = Text("conn", font_size=24, color=GREEN).move_to(conn_box.get_center())
		conn = VGroup(conn_box, conn_text).scale(0.75)

		self.play(Create(conn))
		self.wait(2)


		sock_box = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(connect_text.get_center()+DOWN)
		sock_text = Text("socket", font_size=24, color=LIGHT_PINK).move_to(sock_box.get_center())
		sock = VGroup(sock_box, sock_text).scale(0.75)

		self.play(Create(sock))
		self.wait(2)


		send_arrow = Arrow(start=conn_box.get_right(), end=sock_box.get_left()).shift(UP*0.5)
		recv_arrow = Arrow(start=sock_box.get_left(), end=conn_box.get_right()).shift(DOWN*0.5)
		
		self.play(GrowArrow(send_arrow))
		self.play(GrowArrow(recv_arrow))
		self.wait(2)


		close_text_1 = Text("close conn", font_size=24, color=TEAL).scale(0.75).move_to(conn_box.get_center()+DOWN)
		close_text_2 = Text("close socket", font_size=24, color=MAROON).scale(0.75).move_to(sock_box.get_center()+DOWN)
		
		self.play(Write(close_text_1), Write(close_text_2))
		self.wait(2)