class Vertex(object):
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	VERTICAL = "VERTICAL"

	def __init__(self, x, y):
		self.neighbors = {} #
		self.faces = set() #set of faces it belongs to.
		self.x = x
		self.y = y
		self.visited = False
		self.inQueue = False
		self.root = None
		self.rQueue = None

	def addNeighbor(self, location, vertex):
		self.neighbors[location] = vertex
	def addFace(self, face):
		self.faces.add(face)
	def getFaces(self):
		return self.faces
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getDegree(self):
		return len(self.neighbors)
	def getNeighbors(self):
		return self.neighbors

	def __str__(self):
		return str(self.getX()) + ", " + str(self.getY()) 