from manim import *
import random


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



class ThreeSnakes(Scene):
	def snake_guy(self, body_colour, head_colour):
		snake_body = RoundedRectangle(
			width=5, height=1, 
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			color=body_colour, 
			fill_opacity=1
		)

		snake_head = RoundedRectangle(
			width=2, height=1.5,
			corner_radius=[0.5, 0.5, 0.5, 0.5],
			stroke_width=6,
			stroke_color=head_colour,
			fill_color=head_colour,
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
		return snake_boi


	def construct(self):
		Text.set_default(font="Monospace")

		og_snake = self.snake_guy("#306998", "#FFD43B")
		snake_2 = self.snake_guy(GREEN, PINK)
		snake_3 = self.snake_guy(PURPLE, ORANGE)

		self.play(Create(og_snake))
		self.wait(2)
		self.play(
			snake_2.animate.shift(UP*2),
			snake_3.animate.shift(DOWN*2)
		)
		self.wait(2)



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
		protocol_text = Text("Protocol: TCP/UDP", font_size=24, color=LIGHT_PINK)
		five_tuple_text = VGroup(ip_text, port_text, ip_text_2, port_text_2, protocol_text).arrange(DOWN).move_to(five_tuple.get_center())

		five_tuple_group = VGroup(five_tuple, five_tuple_text).scale(0.75)
		self.play(Transform(socket_addresses, five_tuple_group))
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



class Threads(Scene):
	def add_thread(self, title, color, pos, shared_text_line):
		thread_1_title = Text(title, font_size=20, color=color)
		thread_1_resource = Text("Stack\nRegisters", font_size=20).next_to(thread_1_title, DOWN)
		thread_1_curve = ParametricFunction(lambda t: [t, np.sin(t), 0], t_range=[-PI, PI, 0.01], color=color).scale(0.25).move_to(pos)
		thread_1 = VGroup(thread_1_title, thread_1_resource).next_to(shared_text_line, DOWN).shift(pos)
		self.play(Create(thread_1))
		self.play(Create(thread_1_curve))

		return thread_1_curve


	def add_code(self, code, pos):
		background_rect = Rectangle(
			width=2.5, 
			height=1, 
			fill_color="#2c2336",
			stroke_width=0.5
		).next_to(pos, DOWN*1.3).set_opacity(0.3)	
		code = Text(code, font_size=14).move_to(background_rect.get_center())
		return VGroup(background_rect, code)


	def make_vegetable(self, color, pos, size):
		lettuce = Dot(radius=size, color=color).next_to(pos, RIGHT*0.25)
		self.play(Create(lettuce), run_time=0.2)
		left_rand, down_rand = random.uniform(-1.5, 1.5), random.uniform(2, 2.5)
		self.play(lettuce.animate.move_to(ORIGIN + LEFT*left_rand + DOWN*down_rand), run_time=0.2)


	def construct(self):
		Text.set_default(font="Monospace")

		process_box = RoundedRectangle(
			width=12, height=6,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(ORIGIN+DOWN*0.5)
		self.play(Create(process_box))

		process_title = Text("Multithreaded Process").move_to(process_box.get_top()+UP*0.5)
		self.play(Write(process_title))
		
		shared_text_1 = Text("Heap", font_size=24)
		shared_text_2 = Text("Data", font_size=24)
		shared_text_3 = Text("Code", font_size=24)
		shared_text = VGroup(shared_text_1, shared_text_2, shared_text_3).arrange(RIGHT, buff=2).move_to(process_box.get_top()+DOWN*0.5)
		shared_text_line = Line(LEFT*6, RIGHT*6).next_to(shared_text, DOWN)

		self.play(Write(shared_text), Create(shared_text_line))

		thread_1 = self.add_thread("Thread 1", RED, LEFT*4.5, shared_text_line)
		thread_2 = self.add_thread("Thread 2", ORANGE, LEFT*1.5, shared_text_line)
		thread_3 = self.add_thread("Thread 3", YELLOW, RIGHT*1.5, shared_text_line)
		thread_4 = self.add_thread("Thread 4", GREEN, RIGHT*4.5, shared_text_line)
		
		code_1 = self.add_code("lettuce.chop()\nsalad.push(lettuce)", thread_1.get_center())
		code_2 = self.add_code("tomato.chop()\nsalad.push(tomato)", thread_2.get_center())
		code_3 = self.add_code("onion.chop()\nsalad.push(onion)", thread_3.get_center())
		code_4 = self.add_code("carrot.chop()\nsalad.push(carrot)", thread_4.get_center())
		self.play(Create(code_1), Create(code_2), Create(code_3), Create(code_4))

		bowl = ParametricFunction(lambda t: [t, 0.25*t**2, 0], t_range=[-2, 2, 0.01]).move_to(ORIGIN+DOWN*2.5)
		self.play(Create(bowl))

		self.wait(2)
		cpu = Text("CPU", font_size=24, color=TEAL).next_to(code_1, DOWN)
		self.play(Write(cpu))

		self.make_vegetable(GREEN, code_1, 0.25)		

		for i in range(0, 4):
			self.play(cpu.animate.next_to(code_2, DOWN), run_time=0.2)
			self.make_vegetable(RED, code_2, 0.1)	

			self.play(cpu.animate.next_to(code_3, DOWN), run_time=0.2)
			self.make_vegetable(PURPLE, code_3, 0.15)	

			self.play(cpu.animate.next_to(code_4, DOWN), run_time=0.2)
			self.make_vegetable(ORANGE, code_4, 0.2)	

			self.play(cpu.animate.next_to(code_1, DOWN), run_time=0.2)
			self.make_vegetable(GREEN, code_1, 0.25)		

		self.wait(2)



class MessageQueue(Scene):
	def add_thread(self, title, color, pos):
		thread_1_title = Text(title, font_size=20, color=color).move_to(pos)
		thread_1_curve = ParametricFunction(lambda t: [t, np.sin(t), 0], t_range=[-PI, PI, 0.01], color=color).scale(0.25).next_to(thread_1_title, DOWN)
		self.play(Create(thread_1_title), Create(thread_1_curve))

		return thread_1_title, thread_1_curve


	def add_code(self, code, pos):
		background_rect = Rectangle(
			width=2.5, 
			height=1, 
			fill_color="#2c2336",
			stroke_width=0.5
		).next_to(pos, DOWN*1.3).set_opacity(0.3)	
		code = Text(code, font_size=14).move_to(background_rect.get_center())

		return VGroup(background_rect, code)


	def add_thread_code(self, thread_title, box_title, color, position, code_text):
		server_title, server_thread = self.add_thread(thread_title, color, position)
		server_box = self.create_box(box_title, color, server_thread.get_center() + DOWN*1.5, code_text)
		server = VGroup(server_title, server_thread, server_box)
		return server


	def create_box(self, box_title, color, pos, code_text, scale=1, pos2=0):
		server_box = RoundedRectangle(
			width=4, height=3,
			corner_radius=[0.25, 0.25, 0.25, 0.25]
		).move_to(pos)
		server_text = Text(box_title, font_size=24, color=color).move_to(server_box.get_top()+DOWN*0.5)
		server_group = VGroup(server_box, server_text).scale(0.75).scale(scale)
		self.play(Create(server_group))

		server_code = self.add_code(code_text, server_text.get_bottom()+UP*pos2).scale(scale)
		self.play(Create(server_code))

		box = VGroup(server_group, server_code)
		return box	


	def send_msg(self, message, color, start, end):
		username_text = Text(message, font_size=16)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=color, fill_opacity=0.75)
		username = VGroup(username_box, username_text).move_to(start)
		self.play(username.animate.move_to(end))

		return username


	def construct(self):
		Text.set_default(font="Monospace")

		self.add_thread_code("Main Thread", "Server", LIGHT_PINK, UP*2+LEFT*5, "self.socket.accept()")
		conn_1 = self.add_thread_code("Conn 1 Thread", "Connection 1", BLUE, UP*2+LEFT*1.5, "handle:\n\tself.socket.recv()")
		conn_2 = self.add_thread_code("Conn 2 Thread", "Connection 2", TEAL, UP*2+RIGHT*1.5, "handle:\n\tself.socket.recv()")
		conn_3 = self.add_thread_code("Conn 3 Thread", "Connection 3", GREEN, UP*2+RIGHT*4.5, "handle:\n\tself.socket.recv()")

		client_1 = self.create_box("Client 1", BLUE, LEFT*1.5+DOWN*2.5, "self.socket.send(msg)", scale=0.7, pos2=0.25)
		client_2 = self.create_box("Client 2", TEAL, RIGHT*1.5+DOWN*2.5, "self.socket.send(msg)", scale=0.7, pos2=0.25)
		client_3 = self.create_box("Client 3", GREEN, RIGHT*4.5+DOWN*2.5, "self.socket.send(msg)", scale=0.7, pos2=0.25)

		username = self.send_msg("\"{'username': 'Sn4keK1ng'}\"", BLUE, client_1.get_center(), conn_1.get_center())
		self.play(FadeOut(username))
		direction = self.send_msg("\"{'direction': 'W'}\"", TEAL, client_2.get_center(), conn_2.get_center())
		self.play(FadeOut(direction))
		
		remove_connection = self.send_msg("\"{'remove_connection': 'g4mer'}\"", GREEN, client_3.get_center(), conn_3.get_center())
		self.play(FadeOut(remove_connection))

		message_queue = Text("Message Queue: ", font_size=24).move_to(UP*3+LEFT*5)
		self.play(Write(message_queue))

		username = self.send_msg("\"{'username': 'Sn4keK1ng'}\"", BLUE, client_1.get_center(), conn_1.get_center())
		self.play(Transform(username[1], Text("{'username': 'Sn4keK1ng'}", font_size=16).move_to(username[0].get_center())))
		self.play(username.animate.move_to(message_queue.get_right()+RIGHT*2.5))

		self.play(
			conn_1.animate.shift(RIGHT*3),
			conn_2.animate.shift(RIGHT*3),
			conn_3.animate.shift(RIGHT*3),
			client_1.animate.shift(RIGHT*3),
			client_2.animate.shift(RIGHT*3),
			client_3.animate.shift(RIGHT*3)
		)

		process = self.add_thread_code("Process Thread", "Server", PURPLE, UP*2+LEFT*2, "self.message_queue.get()")

		direction = self.send_msg("\"{'direction': 'W'}\"", TEAL, client_2.get_center(), conn_2.get_center())
		self.play(Transform(direction[1], Text("{'direction': 'W'}", font_size=16).move_to(direction[0].get_center())))
		self.play(direction.animate.move_to(username.get_right()+RIGHT*2))

		self.play(
			username.animate.move_to(process.get_center()),
			direction.animate.shift(LEFT*4.5)
		)
		self.play(FadeOut(username))

		remove_connection = self.send_msg("\"{'remove_connection': 'g4mer'}\"", GREEN, client_3.get_center(), conn_3.get_center())
		self.play(Transform(remove_connection[1], Text("{'remove_connection': 'g4mer'}", font_size=16).move_to(remove_connection[0].get_center())))
		self.play(remove_connection.animate.move_to(direction.get_right()+RIGHT*3))

		self.play(
			direction.animate.move_to(process.get_center()),
			remove_connection.animate.shift(LEFT*4)
		)
		self.play(FadeOut(direction))

		self.play(remove_connection.animate.move_to(process.get_center()))
		self.play(FadeOut(remove_connection))
		self.wait(2)



class Architecture(Scene):
	def create_box(self, box_title, color, pos, code_text, height, code_height=1):
		server_box = RoundedRectangle(
			width=5, height=height,
			corner_radius=[0.25, 0.25, 0.25, 0.25]
		).move_to(pos)
		server_text = Text(box_title, font_size=24, color=color).move_to(server_box.get_top()+DOWN*0.5)
		server_group = VGroup(server_box, server_text).scale(0.5)
		self.play(Create(server_group))

		server_code = self.add_code(code_text, server_text.get_bottom()+UP*0.25, height=code_height).scale(0.7)
		self.play(Create(server_code))

		box = VGroup(server_group, server_code)
		return box	


	def add_code(self, code, pos, height=1):
		background_rect = Rectangle(
			width=3, 
			height=height, 
			fill_color="#2c2336",
			stroke_width=0.5
		).next_to(pos, DOWN*1.3).set_opacity(0.3)	
		code = Text(code, font_size=14).move_to(background_rect.get_center())

		return VGroup(background_rect, code)


	def send_msg(self, message, color, start, end):
		username_text = Text(message, font_size=16)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=color, fill_opacity=0.75)
		username = VGroup(username_box, username_text).scale(0.7).move_to(start)
		self.play(username.animate.move_to(end))

		return username


	def construct(self):
		Text.set_default(font="Monospace")

		server_text = Text("Server", font_size=30).move_to(LEFT*4+UP*3)
		client_text = Text("Client", font_size=30).move_to(RIGHT*4+UP*3)
		self.play(Write(server_text), Write(client_text))

		server_main = self.create_box("Main", MAROON, LEFT*4+UP*1.5, "listen for connections\nwhile True:\n\taccept connections", 3)

		client_main = self.create_box("Main", ORANGE, RIGHT*4+DOWN*2, "connect to server\nsend username", 5, code_height=2)
		connection = self.create_box("Connection", GOLD, LEFT*1.5+DOWN, "receive from client\nadd message to queue", 3)

		username = self.send_msg("\"{'username': 'Sn4keK1ng'}\"", GREEN, client_main, connection)

		username_text = Text("(connection, {'username': 'Sn4keK1ng'})", font_size=16)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=GREEN, fill_opacity=0.75)
		username_2 = VGroup(username_box, username_text).scale(0.7).move_to(username.get_center())
		self.play(Transform(username, username_2))

		message_queue = Text("Message Queue: ", font_size=20).next_to(server_main, DOWN*1.5).shift(LEFT)
		self.play(Write(message_queue))
		self.play(username.animate.move_to(message_queue.get_right() + RIGHT*2.5))

		process = self.create_box("Process Queue", TEAL, LEFT*5+DOWN, "poll the queue\nperform updates", 3)
		self.play(username.animate.move_to(process.get_center()))

		game_state = Text("Game State", font_size=20).next_to(connection, DOWN*3)
		self.play(Write(game_state))
		self.wait(2)

		self.play(username.animate.move_to(game_state.get_center()))
		self.play(FadeOut(username))

		state = self.create_box("Update State", BLUE, LEFT*5+DOWN*3, "update game state\nbroadcast new state", 3)
		gs = self.send_msg("{game_state}", PURPLE, game_state, state)
		self.wait(2)
		self.play(gs.animate.move_to(connection.get_center()))

		new_code = self.add_code("connect to server\nsend username\nwhile True:\n\treceive game state\n\trender world", client_main.get_center()+UP*1.25, height=2).scale(0.7)
		self.play(Transform(client_main[1], new_code))

		self.play(gs.animate.move_to(client_main.get_center()))
		self.play(FadeOut(gs))		

		capture = self.create_box("Capture Keypress", LIGHT_PINK, client_main.get_top()+UP*2, "while True:\n\tcapture keypress\n\tsend to server", 3)
		direction = self.send_msg("\"{'direction': 'W'}\"", PINK, capture, connection)

		direction_text = Text("(connection, {'direction': 'W'})", font_size=16)
		direction_box = SurroundingRectangle(direction_text, corner_radius=0.2, stroke_width=0, fill_color=PINK, fill_opacity=0.75)
		direction_2 = VGroup(direction_box, direction_text).scale(0.7).move_to(direction.get_center())
		self.play(Transform(direction, direction_2))

		self.play(direction.animate.move_to(message_queue.get_right() + RIGHT*2.5))
		self.wait(2)
		self.play(direction.animate.move_to(process.get_center()))
		self.wait(2)
		self.play(direction.animate.move_to(game_state.get_center()))
		self.wait(2)
		self.play(FadeOut(direction))

		self.wait(2)



class RaceCondition(Scene):
	def send_msg(self, message, color, start, end):
		username_text = Text(message, font_size=20)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=color, fill_opacity=1)
		username = VGroup(username_box, username_text).scale(0.7).move_to(start)
		self.play(username.animate.move_to(end))

		return username


	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Race Conditions and Locking", font_size=32).move_to(UP*3)
		self.play(Write(title))

		# Game State box
		game_state = RoundedRectangle(
			width=4, height=2, 
			color=WHITE, 
			corner_radius=[0.25, 0.25, 0.25, 0.25]
		).shift(DOWN*1.5)

		game_state_label = Text("State", font_size=20).move_to(game_state.get_top() + DOWN*0.3)
		players_list = Text("players = []", font_size=18).move_to(game_state.get_center())
		game_group = VGroup(game_state, game_state_label, players_list)
		self.play(Create(game_group))

		thread1 = Text("Thread 1", font_size=16).shift(LEFT*4 + UP*1)
		arrow1 = Arrow(start=thread1.get_right(), end=game_state.get_left(), buff=0.5, color=BLUE)
		self.play(FadeIn(thread1), GrowArrow(arrow1))        

		thread2 = Text("Thread 2", font_size=16).shift(RIGHT*4 + UP*1)
		arrow2 = Arrow(start=thread2.get_left(), end=game_state.get_right(), buff=0.5, color=PURPLE)
		self.play(FadeIn(thread2), GrowArrow(arrow2))

		msg1 = self.send_msg("check 'em' is not in players", BLUE, thread1.get_center(), game_group.get_center())
		msg2 = self.send_msg("check 'em' is not in players", PURPLE, thread2.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg1), FadeOut(msg2))

		msg1 = self.send_msg("add 'em' to players list", BLUE, thread1.get_center(), game_group.get_center())
		msg2 = self.send_msg("add 'em' to players list", PURPLE, thread2.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg1), FadeOut(msg2))

		players_list_2 = Text("players = ['em', 'em']", font_size=18).move_to(game_state.get_center())
		self.play(Transform(players_list, players_list_2))

		ohno = Text("Duplicate names in players list", color=RED, font_size=20).move_to(game_state.get_bottom()+DOWN)
		self.play(Write(ohno))
		self.wait(2)

		players_list_2 = Text("players = []", font_size=18).move_to(game_state.get_center())
		self.play(FadeOut(ohno), Transform(players_list, players_list_2))

		# Add lock
		lock = Dot(radius=0.5, color=GOLD).scale(0.5).move_to(game_state.get_left() + LEFT*1)
		lock_label = Text("Lock", font_size=16).next_to(lock, UP)
		self.play(FadeIn(lock), Write(lock_label))
		lock_group = VGroup(lock, lock_label)

		msg1 = self.send_msg("check 'em' is not in players", BLUE, thread1.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg1))

		msg1 = self.send_msg("add 'em' to players list", BLUE, thread1.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg1))

		players_list_2 = Text("players = ['em']", font_size=18).move_to(game_state.get_center())
		self.play(Transform(players_list, players_list_2))

		self.play(lock_group.animate.move_to(game_state.get_right() + RIGHT*1))

		msg2 = self.send_msg("check 'em' is not in players", PURPLE, thread2.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg2))

		msg2 = self.send_msg("add 'em1' to players list", PURPLE, thread2.get_center(), game_group.get_center())
		self.wait(2)
		self.play(FadeOut(msg2))

		players_list_2 = Text("players = ['em', 'em1']", font_size=18).move_to(game_state.get_center())
		self.play(Transform(players_list, players_list_2))

		self.play(*[FadeOut(mob) for mob in self.mobjects])



class RenderStuff(Scene):
	def create_box(self, box_title, color, pos, code_text, height, code_height=1):
		server_box = RoundedRectangle(
			width=5, height=height,
			corner_radius=[0.25, 0.25, 0.25, 0.25]
		).move_to(pos)
		server_text = Text(box_title, font_size=24, color=color).move_to(server_box.get_top()+DOWN*0.5)
		server_group = VGroup(server_box, server_text).scale(0.5)
		self.play(Create(server_group))

		server_code = self.add_code(code_text, server_text.get_bottom()+UP*0.25, height=code_height).scale(0.7)
		self.play(Create(server_code))

		box = VGroup(server_group, server_code)
		return box	


	def add_code(self, code, pos, height=1):
		background_rect = Rectangle(
			width=3, 
			height=height, 
			fill_color="#2c2336",
			stroke_width=0.5
		).next_to(pos, DOWN*1.3).set_opacity(0.3)	
		code = Text(code, font_size=14).move_to(background_rect.get_center())

		return VGroup(background_rect, code)


	def send_msg(self, message, color, start, end):
		username_text = Text(message, font_size=16)
		username_box = SurroundingRectangle(username_text, corner_radius=0.2, stroke_width=0, fill_color=color, fill_opacity=0.75)
		username = VGroup(username_box, username_text).scale(0.7).move_to(start)
		self.play(username.animate.move_to(end))

		return username


	def construct(self):
		Text.set_default(font="Monospace")

		server_text = Text("Server", font_size=30).move_to(LEFT*4+UP*3)
		client_text = Text("Client", font_size=30).move_to(RIGHT*4+UP*3)
		self.play(Write(server_text), Write(client_text))

		state = self.create_box("Update State", RED, LEFT*4, "while True:\n\tupdate game state\n\tbroadcast new state", 3)

		client_1 = self.create_box("Client 1", ORANGE, RIGHT*0.5+UP*1.5, "while True:\n\treceive game state\n\trender world", 3)
		client_2 = self.create_box("Client 2", GOLD, RIGHT*0.5+DOWN*0.5, "while True:\n\treceive game state\n\trender world", 3)
		client_3 = self.create_box("Client 3", GREEN, RIGHT*0.5+DOWN*2.5, "while True:\n\treceive game state\n\trender world", 3)

		gs_text = Text("{game_state}", font_size=20)
		gs_box = SurroundingRectangle(gs_text, corner_radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
		gs = VGroup(gs_box, gs_text).scale(0.7).move_to(state.get_center())
		gs2 = gs.copy()
		gs3 = gs.copy()

		self.play(
			gs.animate.move_to(client_1.get_center()), 
			gs2.animate.move_to(client_2.get_center()),
			gs3.animate.move_to(client_3.get_center())
		)		


		screen = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(client_1.get_center() + RIGHT*4)

		snek = RoundedRectangle(
			width=1.2, height=0.3,
			corner_radius=[0.1, 0.1, 0.1, 0.1],
			stroke_width=0,
			fill_color="GREEN",
			fill_opacity=1
		).shift(LEFT*1.5)
		food = Dot(radius=0.1, color=RED).shift(RIGHT*1.5)
		game = VGroup(snek, food).move_to(screen.get_center())

		render = VGroup(screen, game)

		render2 = render.copy()
		render2.move_to(client_2.get_center() + RIGHT*4)

		render3 = render.copy()
		render3.move_to(client_3.get_center() + RIGHT*4)

		self.play(
			FadeOut(gs), FadeOut(gs2), FadeOut(gs3),
			FadeIn(render), FadeIn(render2), FadeIn(render3)
		)


		gs_text = Text("{game_state_2}", font_size=20)
		gs_box = SurroundingRectangle(gs_text, corner_radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
		gs = VGroup(gs_box, gs_text).scale(0.7).move_to(state.get_center())
		gs2 = gs.copy()
		gs3 = gs.copy()

		self.play(
			gs.animate.move_to(client_1.get_center()), 
			gs2.animate.move_to(client_2.get_center()),
			gs3.animate.move_to(client_3.get_center())
		)		


		self.play(
			FadeOut(gs), FadeOut(gs2), FadeOut(gs3),
			render[1][0].animate.shift(RIGHT*0.5),
			render2[1][0].animate.shift(RIGHT*0.5),
			render3[1][0].animate.shift(RIGHT*0.5)
		)


		gs_text = Text("{game_state_3}", font_size=20)
		gs_box = SurroundingRectangle(gs_text, corner_radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
		gs = VGroup(gs_box, gs_text).scale(0.7).move_to(state.get_center())
		gs2 = gs.copy()
		gs3 = gs.copy()

		self.play(
			gs.animate.move_to(client_1.get_center()), 
			gs2.animate.move_to(client_2.get_center()),
			gs3.animate.move_to(client_3.get_center())
		)		


		self.play(
			FadeOut(gs), FadeOut(gs2), FadeOut(gs3),
			render[1][0].animate.shift(RIGHT*0.5),
			render2[1][0].animate.shift(RIGHT*0.5),
			render3[1][0].animate.shift(RIGHT*0.5)
		)


		gs_text = Text("{game_state_4}", font_size=20)
		gs_box = SurroundingRectangle(gs_text, corner_radius=0.2, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
		gs = VGroup(gs_box, gs_text).scale(0.7).move_to(state.get_center())
		gs2 = gs.copy()
		gs3 = gs.copy()

		self.play(
			gs.animate.move_to(client_1.get_center()), 
			gs2.animate.move_to(client_2.get_center()),
			gs3.animate.move_to(client_3.get_center())
		)		

		self.play(
			FadeOut(gs), FadeOut(gs2), FadeOut(gs3),
			render[1][0].animate.shift(RIGHT*0.5),
			render2[1][0].animate.shift(RIGHT*0.5),
			render3[1][0].animate.shift(RIGHT*0.5)
		)



class RenderNewStuff(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		current_state_title = Text("self.state", font_size=30).move_to(LEFT*3+UP*3)
		new_state_title = Text("new_state", font_size=30).move_to(RIGHT*3+UP*3)
		self.play(Write(current_state_title), Write(new_state_title))


		current_state = MarkupText(f"""{{
'dimensions': [30, 80],
'food_pos': [12, 69],
'players': {{
	'em': {{
		'segments': [[12, 69], [11, 69], [11, 68]],
		'direction': [1, 0],
		'score': 3,
		'colour': 4
	}},
	'em1': {{
		'segments': [[10, 11], [10, 12], [10, 13],
		'direction': [0, -1],
		'score': 3,
		'colour': 6
	}},
}}""", 
			font_size=10, font="Monospace").next_to(current_state_title, DOWN)


		self.play(Write(current_state))
		self.wait(2)


		new_state = MarkupText(f"""{{
'dimensions': [30, 80],
'food_pos': [5, 24],
'players': {{
	'em': {{
		'segments': [[13, 69], [12, 69], [11, 69], [11, 68]],
		'direction': [1, 0],
		'score': 4,
		'colour': 4
	}},
	'em1': {{
		'segments': [[10, 10], [10, 11], [10, 12],
		'direction': [0, -1],
		'score': 3,
		'colour': 6
	}},
}}""", 
			font_size=10, font="Monospace").next_to(new_state_title, DOWN)

		self.play(Write(new_state))
		self.wait(2)


		help_text = Text("Draw differences only", font_size=24).move_to(DOWN*3)
		self.play(Write(help_text))



		current_state_diff = MarkupText(f"""{{
'dimensions': [30, 80],
'food_pos': <span fgcolor="{ORANGE}">[12, 69]</span>,
'players': {{
	'em': {{
		'segments': [[12, 69], [11, 69], [11, 68]],
		'direction': [1, 0],
		'score': <span fgcolor="{ORANGE}">3</span>,
		'colour': 4
	}},
	'em1': {{
		'segments': [[10, 11], [10, 12], <span fgcolor="{RED}">[10, 13]</span>,
		'direction': [0, -1],
		'score': 3,
		'colour': 6
	}},
}}""", 
			font_size=10, font="Monospace").next_to(current_state_title, DOWN)


		new_state_diff = MarkupText(f"""{{
'dimensions': [30, 80],
'food_pos': <span fgcolor="{ORANGE}">[5, 24]</span>,
'players': {{
	'em': {{
		'segments': [<span fgcolor="{GREEN}">[13, 69]</span>, [12, 69], [11, 69], [11, 68]],
		'direction': [1, 0],
		'score': <span fgcolor="{ORANGE}">4</span>,
		'colour': 4
	}},
	'em1': {{
		'segments': [<span fgcolor="{GREEN}">[10, 10]</span>, [10, 11], [10, 12],
		'direction': [0, -1],
		'score': 3,
		'colour': 6
	}},
}}""", 
			font_size=10, font="Monospace").next_to(new_state_title, DOWN)


		self.play(Transform(current_state, current_state_diff), Transform(new_state, new_state_diff))
		self.wait(2)


		self.play(Transform(help_text, Text("Assign self.state = new_state", font_size=24).move_to(DOWN*3)))
		self.wait(2)


		self.play(new_state.animate.move_to(current_state), FadeOut(current_state))
		self.wait(2)



class NudgeSnake(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		segments = [[0, -1], [0, 0], [0, 1], [0, 2], [0, 3]]
		squares = VGroup()
		
		colours = [MAROON, GRAY_C]
		count = 0
		for piece in segments:
			i, j = piece[0], piece[1]

			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[count%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*i + RIGHT*j)
			snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
			scale = VGroup(snake_piece, snake_coords)

			squares.add(scale)
			count += 1

		squares.move_to(ORIGIN+RIGHT+UP*2)
		self.play(Create(squares))

		dir_text = Text("current_snake['segments']", font_size=24).next_to(squares, UP)
		self.play(Write(dir_text))



		segments2 = [[0, -3], [0, -2], [0, -1], [0, 0], [0, 1]]
		squares2 = VGroup()
		
		count = 0
		for piece in segments2:
			i, j = piece[0], piece[1]

			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[count%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*i + RIGHT*j)
			snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
			scale = VGroup(snake_piece, snake_coords)

			squares2.add(scale)
			count += 1

		squares2.move_to(ORIGIN+LEFT)
		self.play(Create(squares2))

		dir_text2 = Text("new_snake['segments']", font_size=24).next_to(squares2, UP)
		self.play(Write(dir_text2))


		main_text = Text("Loop forwards through the new state", font_size=24).move_to(DOWN*2)
		self.play(Write(main_text))


		arrow = Arrow(start=ORIGIN, end=UP*0.5, buff=0).next_to(squares2[0], DOWN)
		self.add(arrow)
		self.play(squares2[0].copy().animate.shift(UP*2))
		self.play(arrow.animate.shift(RIGHT))
		self.play(squares2[1].copy().animate.shift(UP*2))
		self.play(arrow.animate.shift(RIGHT))


		main_text_2 = Text("Exit loop when this segment is in the current state", font_size=24).move_to(DOWN*2)
		self.play(Transform(main_text, main_text_2), FadeOut(arrow))
		self.wait(2)


		main_text_2 = Text("Loop backwards through the current state", font_size=24).move_to(DOWN*2)
		self.play(Transform(main_text, main_text_2))
		self.wait(2)


		arrow = Arrow(start=ORIGIN, end=UP*0.5, buff=0).next_to(squares[4], DOWN)
		self.add(arrow)
		self.play(FadeOut(squares[4]))
		self.play(arrow.animate.shift(LEFT))
		self.play(FadeOut(squares[3]))
		self.play(arrow.animate.shift(LEFT))


		main_text_2 = Text("Exit loop when this segment is in the new state", font_size=24).move_to(DOWN*2)
		self.play(Transform(main_text, main_text_2), FadeOut(arrow))
		self.wait(2)



class ThreadVsAsync(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Problem #1: Scalability").to_edge(UP)
		self.play(Write(title))


		colours = [RED, ORANGE, YELLOW, GREEN, TEAL]
		threads = VGroup(*[Rectangle(width=2, height=1, color=colours[i]).shift(UP*2 + DOWN*i) for i in range(5)])
		thread_labels = VGroup(*[Text(f"Thread {i+1}", font_size=20).move_to(threads[i].get_center()) for i in range(5)])
		threads_title = Text("One thread per client", font_size=30).next_to(threads, LEFT*2)

		self.play(FadeIn(threads_title), Create(threads), Write(thread_labels))
		self.wait(2)

		overheads = VGroup(*[Text("memory + overhead", font_size=16).next_to(threads[i], RIGHT) for i in range(5)])
		self.play(*[FadeIn(oh) for oh in overheads])
		self.wait(2)

		CPU = Text("CPU", font_size=28, color=BLUE).move_to(threads[0]).shift(RIGHT*5)

		self.play(Write(CPU))
		for i in range(1, 5):
			self.play(CPU.animate.move_to(threads[i]).shift(RIGHT*5), run_time=0.2)
		for i in range(0, 5):
			self.play(CPU.animate.move_to(threads[i]).shift(RIGHT*5), run_time=0.2)

		self.play(*[FadeOut(m) for m in [CPU, overheads, threads, thread_labels, threads_title]])
		self.wait(2)


		async_title = Text("Event Loop", font_size=30).to_edge(LEFT)
		single_thread = Rectangle(width=5, height=1, color=GREEN)
		label = Text("Single Thread", font_size=20).move_to(single_thread.get_center())

		# Coroutines inside the async loop
		coroutines = VGroup(*[Circle(radius=0.25, color=YELLOW).shift(RIGHT*(i - 2) + DOWN*1) for i in range(5)])
		coroutine_labels = VGroup(*[Text(f"C{i+1}", font_size=18).move_to(coroutines[i]) for i in range(5)])

		self.play(Write(async_title))
		self.play(Create(single_thread), Write(label))
		self.play(Create(coroutines), Write(coroutine_labels))


		for i in range(5):
		    self.play(coroutines[i].animate.set_fill(YELLOW, opacity=1), run_time=0.2)
		    self.play(coroutines[i].animate.set_fill(YELLOW, opacity=0.3), run_time=0.2)

		for i in range(5):
		    self.play(coroutines[i].animate.set_fill(YELLOW, opacity=1), run_time=0.2)
		    self.play(coroutines[i].animate.set_fill(YELLOW, opacity=0.3), run_time=0.2)

		self.wait(2)



class ClientPrediction(Scene):
	def construct(self):
		Text.set_default(font="Monospace")

		title = Text("Problem #2: Server Lag").to_edge(UP)
		self.play(Write(title))

		client = Rectangle(width=2.5, height=1.5, color=BLUE).shift(LEFT * 4)
		client_label = Text("Client", font_size=24).next_to(client, DOWN)
		server = Rectangle(width=2.5, height=1.5, color=RED).shift(RIGHT * 4)
		server_label = Text("Server", font_size=24).next_to(server, DOWN)

		self.play(FadeIn(client), Write(client_label), FadeIn(server), Write(server_label))

		key = Text("W", font_size=28).next_to(client, UP)
		arrow_to_server = Arrow(start=client.get_right(), end=server.get_left(), buff=0.2)
		latency_label = Text("50 ms", font_size=24).next_to(arrow_to_server, UP)
		self.play(FadeIn(key), GrowArrow(arrow_to_server), Write(latency_label))
		self.wait(2)

		server_process = Text("player.direction = W", font_size=20).next_to(server, UP)
		self.play(Write(server_process))
		self.wait(2)

		arrow_back = Arrow(start=server.get_left(), end=client.get_right(), buff=0.2)
		latency_return = Text("50 ms", font_size=24).next_to(arrow_back, DOWN)

		self.play(FadeOut(arrow_to_server), GrowArrow(arrow_back), Write(latency_return))
		self.wait(2)

		self.play(FadeOut(arrow_back),
		          FadeOut(latency_label), FadeOut(latency_return),
		          FadeOut(server_process), FadeOut(key))
		self.wait(2)

		self.play(FadeIn(key))
		client_predict = Text("Prediction: Move snake upwards", font_size=20).next_to(client, DOWN*3)
		self.play(Write(client_predict))

		pred_snake = Rectangle(width=0.5, height=1.5, color=GREEN, fill_opacity=0.5).move_to(client.get_center()).scale(0.7)
		self.play(FadeIn(pred_snake))
		self.wait(1)

		server_state = Rectangle(width=0.5, height=1.5, color=RED, fill_opacity=0.5).move_to(server.get_center()).scale(0.7)
		server_state_text = Text("Actual snake movement", font_size=20).next_to(server, DOWN*3)
		self.play(FadeIn(server_state), Write(server_state_text))
		self.play(server_state.animate.move_to(pred_snake))
		self.wait(2)

		note = Text("Prediction gives instant response | Server ensures consistency", font_size=24).to_edge(DOWN)
		self.play(Write(note))
		self.wait(2)



class Thumbnail(Scene):
	def construct(self):
		Text.set_default(font="Monospace")		


		socket_scene = VGroup()

		server_box = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+LEFT*4.75+DOWN*0.25)
		server_text = Text("Server", font_size=24, color=MAROON).move_to(server_box.get_center())
		server_group = VGroup(server_box, server_text).scale(0.75)

		client_box = RoundedRectangle(
			width=4, height=2,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="GRAY_C",
			fill_color="BLACK",
			fill_opacity=1
		).move_to(ORIGIN+RIGHT*4.75+DOWN*0.25)
		client_text = Text("Client", font_size=24, color=TEAL).move_to(client_box.get_center())
		client_group = VGroup(client_box, client_text).scale(0.75)

		server_client = VGroup(server_group, client_group).shift(UP*2.75)
		socket_scene.add(server_client)


		socket_text = Text("create socket", font_size=24, color=RED).scale(0.75).move_to(server_box.get_center()+DOWN)
		socket_scene.add(socket_text)

		bind_text = Text("bind to (host, port)", font_size=24, color=ORANGE).scale(0.75).move_to(socket_text.get_center()+DOWN)
		socket_scene.add(bind_text)

		listen_text = Text("socket.listen()", font_size=24, color=GOLD).scale(0.75).move_to(bind_text.get_center()+DOWN)
		socket_scene.add(listen_text)

		socket_text_2 = Text("create socket", font_size=24, color=BLUE).scale(0.75).move_to(client_box.get_center()+DOWN)
		socket_scene.add(socket_text_2)

		connect_text = Text("connect to server (host, port)", font_size=24, color=PURPLE).scale(0.75).move_to(socket_text_2.get_center()+DOWN*3)
		socket_scene.add(connect_text)

		accept_text = Text("accept connection", font_size=24, color=YELLOW).scale(0.75).move_to(listen_text.get_center()+DOWN)
		socket_scene.add(accept_text)


		conn_box = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(accept_text.get_center()+DOWN)
		conn_text = Text("conn", font_size=24, color=GREEN).move_to(conn_box.get_center())
		conn = VGroup(conn_box, conn_text).scale(0.75)
		socket_scene.add(conn)


		sock_box = RoundedRectangle(
			width=3, height=1.5,
			corner_radius=[0.25, 0.25, 0.25, 0.25],
			stroke_color="WHITE"
		).move_to(connect_text.get_center()+DOWN)
		sock_text = Text("socket", font_size=24, color=LIGHT_PINK).move_to(sock_box.get_center())
		sock = VGroup(sock_box, sock_text).scale(0.75)
		socket_scene.add(sock)


		send_arrow = Arrow(start=conn_box.get_right(), end=sock_box.get_left()).shift(UP*0.5)
		recv_arrow = Arrow(start=sock_box.get_left(), end=conn_box.get_right()).shift(DOWN*0.5)
		
		socket_scene.add(send_arrow)
		socket_scene.add(recv_arrow)


		close_text_1 = Text("close conn", font_size=24, color=TEAL).scale(0.75).move_to(conn_box.get_center()+DOWN)
		close_text_2 = Text("close socket", font_size=24, color=MAROON).scale(0.75).move_to(sock_box.get_center()+DOWN)		
		socket_scene.add(close_text_1, close_text_2)

		self.add(socket_scene)



		title_text = Text("Python Multiplayer Snake").shift(UP*3)
		self.add(title_text)

		question_text = Text("Learn sockets and threads", color="WHITE", font_size=24)
		question_group = VGroup(question_text).arrange(buff=0.5).shift(UP*2)
		self.add(question_group)



		snakey_bois = VGroup()

		segments = [[0, -1], [0, 0], [0, 1], [0, 2], [0, 3]]
		squares = VGroup()
		
		colours = ["#306998", "#FFD43B"]
		count = 0
		for piece in segments:
			i, j = piece[0], piece[1]

			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[count%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*i + RIGHT*j)
			snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
			scale = VGroup(snake_piece, snake_coords)

			squares.add(scale)
			count += 1

		squares.move_to(ORIGIN+RIGHT+UP*2)
		snakey_bois.add(squares)

		dir_text = Text("new_snake['segments']", font_size=24).next_to(squares, UP)
		snakey_bois.add(dir_text)



		segments2 = [[0, -3], [0, -2], [0, -1], [0, 0], [0, 1]]
		squares2 = VGroup()
		
		count = 0
		for piece in segments2:
			i, j = piece[0], piece[1]

			snake_piece = Rectangle(
				width=1, height=1, 
				color=colours[count%2], 
				fill_opacity=1,
				stroke_width=0
			).move_to(ORIGIN + DOWN*i + RIGHT*j)
			snake_coords = Text('('+str(i)+','+str(j)+')', font_size=16).move_to(snake_piece.get_center())
			scale = VGroup(snake_piece, snake_coords)

			squares2.add(scale)
			count += 1

		squares2.move_to(ORIGIN+LEFT)
		snakey_bois.add(squares2)

		dir_text2 = Text("current_snake['segments']", font_size=24).next_to(squares2, UP)
		snakey_bois.add(dir_text2)


		self.add(snakey_bois.scale(0.5).shift(DOWN*1.25+RIGHT*4))