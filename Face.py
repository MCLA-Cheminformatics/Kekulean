class Face(object):
	#vertices
	TOP = 0
	TOP_RIGHT = 1
	BOTTOM_RIGHT = 2
	BOTTOM = 3
	BOTTOM_LEFT = 4
	TOP_LEFT = 5

	
	def __init__(self, x, y):
		self.vertices = [0] * 6
		self.x = x
		self.y = y

		self.isFries = False
		self.isClars = False
		self.isIsolatedFries = False

		self.neighbors = []

	def addVertex(self, location, vertex):
		self.vertices[location] = vertex
	def assignVertices(self, vertices):
		self.vertices = vertices
	def getVertices(self):
		return self.vertices
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def setNeighbors(self, n):
		self.neighbors = n
	def getNeighbors(self):
		return self.neighbors

	def __str__(self):
		return str(self.getY()) + ", " + str(self.getX()) 