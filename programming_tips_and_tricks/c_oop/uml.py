from manim import *


class Uml:
	START = LEFT*4
	END = RIGHT*4

	def __init__(self, class_name, attributes, methods):
		self.class_name = self.make_class_name(class_name)
		self.attributes = self.make_attributes(attributes)
		self.methods = self.make_methods(methods)
		self.uml_inner = VGroup(
			self.class_name, 
			self.attributes, 
			self.methods
		).arrange(DOWN)

		self.box = SurroundingRectangle(self.uml_inner, color=WHITE, buff=0)

		self.uml = VGroup(
			self.box, 
			self.uml_inner
		)


	def get_uml(self):
		return self.uml

	def get_box(self):
		return self.uml[0]

	def get_class_name(self):
		return self.uml[1][0]

	def get_attributes(self):
		return self.uml[1][1]

	def get_methods(self):
		return self.uml[1][2]


	def make_class_name(self, class_name):
		cn_text = Text(class_name, font_size=30, weight=BOLD)
		cn_line = Line(start=Uml.START, end=Uml.END)
		return VGroup(cn_text, cn_line).arrange(DOWN)

	def make_attributes(self, attributes):
		att_group = VGroup()
		for attribute in attributes:
			att_group.add(Text(attribute, font_size=20, t2c={"+": GREEN, "-": RED, "#": BLUE}))
		att_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
		att_line = Line(start=Uml.START, end=Uml.END)
		return VGroup(att_group, att_line).arrange(DOWN)

	def make_methods(self, methods):
		method_group = VGroup()
		for method in methods:
			method_group.add(Text(method, font_size=20, t2c={"+": GREEN, "-": RED, "#": BLUE}))
		method_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
		return method_group