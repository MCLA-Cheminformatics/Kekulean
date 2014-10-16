from Vertex import *

class VertexList(object):
	def __init__(self):
		self.degree2 = []
		self.degree3 = []

	def add(self, v):
		if v.getDegree() == 2:
			self.degree2.append(v)
		else:
			self.degree3.append(v)

	def pop(self):
		if len(self.degree2) > 0:
			return self.degree2[0]
		elif len(self.degree3) > 0:
			return self.degree3[0]
		else:
			return None
	def __len__(self):
		return len(self.degree2) + len(self.degree3)

	def __contains__(self, key):
		return key in self.degree2 or key in self.degree3

	def remove(self, v):
		if v.getDegree() == 2:
			self.degree2.remove(v)
		else:
			self.degree3.remove(v)

	def update(self, visited):
		for v in visited:
			if v.getDegree() == 2:
				if v in self.degree2:
					self.degree2.remove(v)
			else:
				if v in self.degree3:
					self.degree3.remove(v)