from manim import *

from props import Human

class Family:
	def __init__(self, fill_opacity, human_size, group_size, positions):
		self.fill_opacity = fill_opacity
		self.human_size = human_size
		self.group_size = group_size
		self.positions = positions

		self.label_colour = WHITE
		self.labels = ["Grandpa", "Uncle", "Dad", "Mum", "Brother", "You"]
		self.colours = [ORANGE, GOLD, GREEN, TEAL, BLUE, PURPLE]

		# VGroup of the manim objects
		self.family_group = None

		# List of the actual classes
		self.family_list = None


	def get_family_list(self):
		if self.family_list == None:
			self.family_list = self.make_family_list()
		return self.family_list

	def get_family_group(self):
		if self.family_group == None:
			self.family_group = self.make_family_group()
		return self.family_group

	def get_family_list_member(self, label):
		return self.family_list[self.labels.index(label)]

	def get_family_group_member(self, label):
		return self.family_group[self.labels.index(label)]


	def set_labels(self, labels):
		self.labels = labels

	def set_colours(self, colours):
		self.colours = colours

	def set_label_colour(self, label_colour):
		self.label_colour = label_colour


	def make_family_list(self):
		family_list = []

		for i in range(0, len(self.labels)):
			family_member = Human(self.colours[i], self.fill_opacity).add_label(self.labels[i], label_colour=self.label_colour)
			family_member.get_human().scale(self.human_size).move_to(self.positions[i])
			family_list.append(family_member)

		return family_list

	def make_family_group(self):
		if self.family_list == None:
			self.family_list = self.make_family_list()

		family_group = VGroup()

		for i in range(0, len(self.family_list)):
			family_group.add(self.family_list[i].get_human())

		family_group.scale(self.group_size)
		return family_group