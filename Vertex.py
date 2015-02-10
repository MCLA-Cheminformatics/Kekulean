class Vertex(object):
	__slots__ = ['neighbors', 'faces', 'x', 'y', 'visited', 'inQueue', 'root', 'rQueue', 'w', 'wx', 'wy', 'required']

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
		self.w = False
		self.wx = 0
		self.wy = 0
		self.required = False

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

	def __eq__(self, other):
		if other is False:
			return False
		else:
			return self.getX() == other.getX() and self.getY() == other.getY() and self.getDegree() == other.getDegree()

	def __ne__(self, other):
		return not self.__eq__(other)