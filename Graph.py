from Face import *
from Vertex import *
from Tkinter import *

#add proper support for the R and W
#add proper support for sorting
#make comparison a static member
class Graph(object):

	comparison = 'fries'

	def __init__(self, faceGraph, vertexGraph):
		self.faceGraph = faceGraph
		self.vertexGraph = vertexGraph

		self._assignFaceNeighbors()

		self.doubleBonds = {}
		self.vertexRoots = {}
		self.lastAddPair = tuple()

		self.FriesNumber = 0
		self.ClarsNumber = 0

		self.rowCount = [0] * self.getNumberOfRows()
		self.totalUpperBounds = 0

		self.leftMostFace = None
		self.rightMostFace = None
		self.rankFaces()

		self.assignUpperBounds()

	def getVertexGraph(self):
		return self.vertexGraph
	def getFaceGraph(self):
		return self.faceGraph
	def getNumberOfRows(self):
		#the minus one is for the off by one error induced by len(); The plus one is to account for the face that the row count starts at zero, throwing off the actual row count by one
		return self.faceGraph[len(self.faceGraph) - 1].getY() + 1
	def getDoubleBonds(self):
		return self.doubleBonds
	def setDoubleBonds(self, doubleBonds):
		self.doubleBonds = doubleBonds
	def getVertexRoots(self):
		return self.vertexRoots
	def setVertexRoots(self, newRoots):
		self.vertexRoots = newRoots
	def getRowUpperBonds(self, index):
		return self.rowCount[index]
	def getLastAddedPair(self):
		return self.lastAddPair
	def getFriesNumber(self):
		return self.FriesNumber
	def getClarsNumber(self):
		return self.ClarsNumber

	def getClarsFriesDiff(self):
		return float(self.ClarsNumber)/float(self.FriesNumber)

	def assignFriesFaces(self):
		for f in self.faceGraph:
			self._checkVertices(f)
			if f.isFries == True:
				self.FriesNumber += 1


	#checks the vertices of a face to see if there are 3 double-bonds within it. If so, then the face is considered a Fries Face
	def _checkVertices(self, face):
		verts = face.getVertices()
		bondCount = 0
		if verts[Face.TOP_LEFT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP_LEFT]] == verts[Face.TOP] or self.doubleBonds[verts[Face.TOP_LEFT]] == verts[Face.BOTTOM_LEFT]:
				bondCount += 1
		if verts[Face.TOP] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP]] == verts[Face.TOP_LEFT] or self.doubleBonds[verts[Face.TOP]] == verts[Face.TOP_RIGHT]:
				bondCount += 1
		if verts[Face.TOP_RIGHT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP_RIGHT]] == verts[Face.TOP] or self.doubleBonds[verts[Face.TOP_RIGHT]] == verts[Face.BOTTOM_RIGHT]:
				bondCount += 1
		if verts[Face.BOTTOM_RIGHT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM_RIGHT]] == verts[Face.BOTTOM] or self.doubleBonds[verts[Face.BOTTOM_RIGHT]] == verts[Face.TOP_RIGHT]:
				bondCount += 1
		if verts[Face.BOTTOM] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM]] == verts[Face.BOTTOM_RIGHT] or self.doubleBonds[verts[Face.BOTTOM]] == verts[Face.BOTTOM_LEFT]:
				bondCount += 1
		if verts[Face.BOTTOM_LEFT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM_LEFT]] == verts[Face.TOP_LEFT] or self.doubleBonds[verts[Face.BOTTOM_LEFT]] == verts[Face.BOTTOM]:
				bondCount += 1
		if bondCount == 3:
			face.isFries = True
		#print bondCount

	#method is used to get the pixel locations of the double bonds in the graph. Used for displayGrpah method
	def getBondedVertices(self, face):
		verts = face.getVertices()
		pairs = []
		if verts[Face.TOP_LEFT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP_LEFT]] == verts[Face.TOP]:
				pairs.append((0, 10, 10, 0))
			elif self.doubleBonds[verts[Face.TOP_LEFT]] == verts[Face.BOTTOM_LEFT]:
				pairs.append((0, 10, 0, 30))

		if verts[Face.TOP] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP]] == verts[Face.TOP_LEFT]:
				pairs.append((10, 0, 0, 10))
			elif self.doubleBonds[verts[Face.TOP]] == verts[Face.TOP_RIGHT]:
				pairs.append((10, 0, 20, 10))

		if verts[Face.TOP_RIGHT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.TOP_RIGHT]] == verts[Face.TOP]:
				pairs.append((20, 10, 10, 0))
			elif self.doubleBonds[verts[Face.TOP_RIGHT]] == verts[Face.BOTTOM_RIGHT]:
				pairs.append((20, 10, 20, 30))

		if verts[Face.BOTTOM_RIGHT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM_RIGHT]] == verts[Face.BOTTOM]:
				pairs.append((20, 30, 10, 40))
			elif self.doubleBonds[verts[Face.BOTTOM_RIGHT]] == verts[Face.TOP_RIGHT]:
				pairs.append((20, 30, 20, 10))

		if verts[Face.BOTTOM] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM]] == verts[Face.BOTTOM_RIGHT]:
				pairs.append((10, 40, 20, 30))
			elif self.doubleBonds[verts[Face.BOTTOM]] == verts[Face.BOTTOM_LEFT]:
				pairs.append((10, 40, 0, 30))

		if verts[Face.BOTTOM_LEFT] in self.doubleBonds:
			if self.doubleBonds[verts[Face.BOTTOM_LEFT]] == verts[Face.TOP_LEFT]:
				pairs.append((0, 30, 0, 10))
			elif self.doubleBonds[verts[Face.BOTTOM_LEFT]] == verts[Face.BOTTOM]:
				pairs.append((0, 30, 10, 40))
		return pairs

	#assigns Clars Faces the independent Fries Faces. Boes not yet find the heighest possible Clars number
	def assignClarsFaces(self):
		friesList = []

		for face in self.faceGraph:
			if face.isFries == True:
				friesList.append(face)
				neighbors = self._checkNeighbors(face)
				#1 impies that there are Fries nieghbors, but no Clars
				if neighbors == 1:
					face.isClars = True
					self.ClarsNumber += 1
				#0 implies that there are no Clars or Fries neighbors
				elif neighbors == 0:
					face.isClars = True
					face.isIsolatedFries = True
					self.ClarsNumber += 1

		self._maxClars(friesList)

	def _maxClars(self, friesList):
		setList = []

		for f in friesList:
			s = set()
			s.add(f)
			friesList.remove(f)

			neighbors = f.getNeighbors()
			#print 'max Clars:', len(neighbors)
			for n in neighbors:
				if n in friesList and n not in s:
					neighbors.extend(n.getNeighbors())
					s.add(n)
					friesList.remove(n)
			setList.append(s)

		for s in setList:
			if len(s) > 1:
				oldClars, newClars = self._compareClarsFaces(s)
				#print oldClars, newClars
				if newClars > oldClars:
					#print 'flipping'
					for f in s:
						if f.isClars == True:
							f.isClars = False
							self.ClarsNumber -= 1
						else:
							f.isClars = True
							self.ClarsNumber += 1

	def _compareClarsFaces(self, flipped):
		oldClars = 0
		newClars = 0

		for f in flipped:
			if f.isClars == True:
				oldClars += 1
			else:
				newClars += 1
		return oldClars, newClars

	#returns 0 if it borders no Fries/Clars; 1 if it border 1+ Fries faces; 2 if it borders 1+ Clars faces
	def _checkNeighbors(self, face):
		topLeft = None
		topRight = None
		right = None
		bottomRight = None
		bottomLeft = None
		left = None

		topLeft = self.findFace(face.getX()-1, face.getY()-1)
		topRight = self.findFace(face.getX(), face.getY()-1)
		right = self.findFace(face.getX()+1, face.getY())
		bottomRight = self.findFace(face.getX()+1, face.getY()+1)
		bottomLeft = self.findFace(face.getX(), face.getY()+1)
		left = self.findFace(face.getX()-1, face.getY())

		neighbors = [topLeft, topRight, right, bottomRight, bottomLeft, left]

		hasFries = False
		hasClars = False

		for n in neighbors:
			if n is not None:	
				if n.isClars == True:
					hasClars = True
					break
				elif n.isFries == True:
					hasFries = True

		if hasClars == True:
			return 2
		elif hasFries == True:
			return 1
		else:
			return 0

	def _assignFaceNeighbors(self):
		for face in self.getFaceGraph():
			n = []
			#Top-left
			f = self.findFace(face.getX()-1, face.getY()-1)
			if f is not None:
				n.append(f)
			
			#Top-right
			f = self.findFace(face.getX(), face.getY()-1)
			if f is not None:
				n.append(f)
			#Right
			f = self.findFace(face.getX()+1, face.getY())
			if f is not None:
				n.append(f)
			#Bottom-right
			f = self.findFace(face.getX()+1, face.getY()+1)
			if f is not None:
				n.append(f)
			#Bottom-left
			f = self.findFace(face.getX(), face.getY()+1)
			if f is not None:
				n.append(f)
			#Left
			f = self.findFace(face.getX()-1, face.getY())
			if f is not None:
				n.append(f)

			#print 'neighbors:', len(n)
			#print n 
			face.setNeighbors(n)

	#returns the face with the x- and y-coor given
	def findFace(self, x, y):
		if x < 0 or y < 0:
			return None
		else:
			face = None
			for f in self.faceGraph:
				if f.getX() == x and f.getY() == y:
					face = f
					break
			return face

	#checks if the graph structure is kekulean or not, knowning that the root graph is Kekulean
	def checkKekulean(self):
		"""if len(self.getDoubleBonds()) == len(self.getVertexGraph())/2:
			for key, value in self.getDoubleBonds().items():
				if key in self.getDoubleBonds().values() or value in self.getDoubleBonds().keys():
					break
			else:
				#did not reach break 
				return True
			#did reach break
			return False
		else:
			return False"""

		return len(self.getDoubleBonds()) == len(self.getVertexGraph())/2

	def getW(self):
		w = []
		l = []
		
		initVert = self.getVertexGraph()[0]
		initVert.w = True

		l.append(initVert)
		w.append(initVert)

		while len(l) > 0:
			#print "len of l:", len(l)
			v = l.pop(0)
			neighbors = v.getNeighbors()
			left = None
			vertical = None
			right = None
			for n in neighbors:
				if n == Vertex.LEFT:
					left = neighbors[n]
					if left.w != True:
						left.w = True
						left.wx = v.wx - 1
						#this implies that left is above the current vertex
						if left.getY() < v.getY():
							left.wy = v.wy + 1
						#This imples that left is below the current verrtex
						else:
							left.wy = v.wy - 1
					else:
						left = None
				elif n == Vertex.RIGHT:
					right = neighbors[n]
					if right.w != True:
						right.w = True
						right.wx = v.wx + 1
						#this implies that right is above the current vertex
						if right.getY() < v.getY():
							right.wy = v.wy + 1
						#This imples that right is below the current verrtex
						else:
							right.wy = v.wy - 1
					else:
						right = None
				elif n == Vertex.VERTICAL:
					vertical = neighbors[n]
					if vertical.w != True:
						vertical.w = True
						vertical.wx = v.wx
						#this imples that vertical is above the current vertex
						if vertical.getY() < v.getY():
							vertical.wy = v.wy + 1
						#this imples that vertical is below the current vertex
						else:
							vertical.wy = v.wy - 1
					else:
						vertical = None

			addons = [left, right, vertical]
			#added = 0
			for a in addons:
				if a is not None:
					l.append(a)
					w.append(a)
					#added += 1
			#print "added:", added
		return w

	def getR(self, w):
		r = []
		for vw in w:
			for vr in r:
				if vw.wx < vr.wx:
					r.insert(r.index(vr), vw)
					break
			else:
				r.append(vw)
		return r

	def rankFaces(self):
		ranking = {}
		for f in self.faceGraph:
			ranking[f] = f.getX() - f.getY()

		minRank = sys.maxint
		maxRank = -sys.maxint - 1
		minFace = None
		maxFace = None
		for f, rank in ranking.items():
			if rank < minRank:
				minRank = rank
				minFace = f 
			if rank > maxRank:
				maxRank = rank
				maxFace = f

		self.leftMostFace = minFace
		self.rightMostFace = maxFace

	def getXOffset(self):
		x = self.leftMostFace.getX()
		y = self.leftMostFace.getY()

		return 10 * -(x - y) + 10

	def getWidth(self):
		leftX = self.getXOffset()
		#print 'leftX:', leftX

		x = self.rightMostFace.getX()
		y = self.rightMostFace.getY() 

		#print 'x:', x, 'y:', y

		rightX = 20 * (x + y)
		#print 'rightX', rightX 

		return int(1.5 * (abs(leftX) + abs(rightX)))

	def displayGraph(self):
		root = Tk()

		xScrollbar = Scrollbar(root, orient=HORIZONTAL)
		xScrollbar.pack(side=BOTTOM, fill=X)

		yScrollbar = Scrollbar(root, orient=VERTICAL)
		yScrollbar.pack(side=RIGHT, fill=Y)

		canvas = Canvas(root, width=500, height=400, xscrollcommand=xScrollbar.set, yscrollcommand=yScrollbar.set)
		canvas.pack()

		xScrollbar.configure(command=canvas.xview)
		yScrollbar.configure(command=canvas.yview)

		for f in self.faceGraph:
			x = f.getX() 
			y = f.getY()
			faceColor = 'gray'
			#assign colors for faces
			if f.isClars == True:
				faceColor = 'blue'
			elif f.isFries == True:
				faceColor = 'green'

			xoffset = self.getXOffset()

			points = [0 + x*20 - y*10 + xoffset, 10 + y*30, 10 + x*20 - y*10 + xoffset, 0 + y*30, 20 + x*20 - y*10 + xoffset, 10 + y*30, 20 + x*20 - y*10 + xoffset, 30 + y*30, 10 + x*20 - y*10 + xoffset, 40 + y*30, 0 + x*20 - y*10 + xoffset, 30 + y*30]

			#draw hexagons
			canvas.create_polygon(points, outline='black', fill=faceColor, width=2)

			pairs = self.getBondedVertices(f)

			for pair in pairs:
				#paint pair
				x1, y1, x2, y2 = pair
				x1 += x*20 - y*10 + xoffset
				y1 += y*30
				x2 += x*20 - y*10 + xoffset
				y2 += y*30
				canvas.create_line(x1, y1, x2, y2, fill='red', width=3)

		mainloop()

	def toString(self):
		self.printUpperBounds()
		string = '' 
		string = "Fries Number: " + str(self.getFriesNumber()) + " Clars Number: " + str(self.getClarsNumber()) + '\n'
		string += "Clars-Fries Differential: " + str(self.getClarsFriesDiff()) + '\n'
		string += "There are " + str(len(self.vertexGraph)) + " vertices" + '\n'

		string += "Number of Double Bonds: " + str(len(self.getDoubleBonds())) + '\n'
		for v1, v2 in self.getDoubleBonds().items():
			string += str(v1) + ':' + str(v2) + '\n'	
		return string

	def printUpperBounds(self):
		print "Upper Bounds of the graph from top to bottom"
		for row in range(len(self.rowCount)):
			print "Row " + str(row + 1) + ":", self.rowCount[row]
		print "Total Upper Bounds:", self.totalUpperBounds 
	
	def simpleToString(self):
		row = 0
		string = ""
		for face in self.faceGraph:
			if face.getY() != row:
				string += "\n"
				row = face.getY()  	
			string += " " + str(face.getX()) + " "
		return string

	def assignUpperBounds(self):
		whiteCount = [0] * len(self.rowCount)
		blackCount = [0] * len(self.rowCount)

		for v in self.getVertexGraph():
			#even y numbers mean the vertex is marked white on the graph
			if v.getY() % 2 == 0:
				index = v.getY() / 2
				if index < len(whiteCount):
					whiteCount[index] += 1
			#The else implies that the vertex's y is odd, and thus the verex is marked black 
			else:
				index = (v.getY() - 1) / 2
				if index < len(blackCount):
					blackCount[index] += 1

		for index in range(len(self.rowCount)):
			count = abs(sum(whiteCount[0:index+1]) - sum(blackCount[0:index+1]))
			#print count
			self.rowCount[index] = count

		self.totalUpperBounds = sum(self.rowCount)

	def doubleBondsToString(self):
		for key, value in self.getDoubleBonds().items():
			print key.getX(), key.getY(), ":", value.getX(), value.getY()

	def __cmp__(self, other):
		if self.comparison == 'clars':
			if self.getClarsNumber() < other.getClarsNumber():
				return -1
			elif self.getClarsNumber == other.getClarsNumber():
				return 0
			else:
				return 1
		elif self.comparison == 'fries':
			if self.getFriesNumber() < other.getFriesNumber():
				return -1
			elif self.getFriesNumber == other.getFriesNumber():
				return 0
			else:
				return 1