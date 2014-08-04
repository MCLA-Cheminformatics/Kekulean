class ConjectureData(object):
	def __init__ (self, numVertices, clarsNumber, numStructures):
		self.numVertices = numVertices
		self.clarsNumber = clarsNumber
		self.numStructures = numStructures

		self.string = 'empty'

	def getNumVertices(self):
		return self.numVertices
	def getClarsNumber(self):
		return self.clarsNumber
	def getNumStructures(self):
		return self.numStructures
	def setString(self, s):
		self.string = s
	def __str__(self):
		return self.string
	def __cmp__(self, other):
		if self.getNumVertices() < other.getNumVertices():
			return -1
		elif self.getNumVertices() == other.getNumVertices():
			return 0
		else:
			return 1
