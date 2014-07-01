from random import randint
import time
import copy
from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from VerticalEdgeIterator import *

#function that reads in the graph returns a 2D string list of the graph
def getInput(fileName):
	faceGraph = []
	inputFile = open(fileName, 'r')
	
	row = inputFile.readline()
	y = 0
	while len(row) > 0:
		row = row.replace('\n', '')
		row = row.split(";")		
		
		for i in range(len(row)):
			x = row[i].split(',')
			faceGraph.append((Face(int(x[1]), y)))

		row = inputFile.readline()
		y += 1
		
	inputFile.close()
		
	return faceGraph

def faceGraphToInts(faceGraph):
	rowCount = 0
	row = []
	intG = []

	for face in faceGraph:
		if face.getY() != rowCount:
			intG.append(row)
			rowCount = face.getY()
			row = list()
		row.append(face.getX())
	intG.append(row)
	return intG

#checks if the graph is connected
def isConnected(g):
	dual = assignComponents(g)
	connected = checkConnected(dual, g)
	
	return connected
 
#assigns each face a seperate component. Faces change component as it is discovered that they are connected
def assignComponents(g):
	dual = []
	counter = 0
	
	for i in range(len(g)):
		row = g[i]
		dualRow = []
		for j in range(len(row)):
			dualRow.append(counter)
			counter = counter + 1
		dual.append(dualRow)
	return dual
	
#alters the dual from the assignComponent function to see if the graph is connected
def checkConnected(d, g):

	totalFaceCount = getNumFaces(g)
	compList = list(range(totalFaceCount))

	for i in range(len(g)):
		dualRow = d[i]
		row = g[i]
		for j in range(len(row)):
			face = row[j]
			#For the face to the right
			if j < len(row)-1:
				otherFace = row[j+1]
				if (otherFace - 1) == face:
					d.remove(dualRow)
					comp = getLower(dualRow[j], dualRow[j+1])
					reassignComps(compList, comp, dualRow[j], dualRow[j+1])
					dualRow[j] = comp
					dualRow[j+1] = comp
					d.insert(i, dualRow)
			#For the faces below
			if i < len(g)-1:
				belowRow = g[i+1]
				belowDualRow = d[i+1]
				try:
					otherFace = belowRow[j]
				except:
					otherFace = None
				if otherFace != None:
					#For the face down and to the left
					if otherFace == face or (otherFace-1) == face:
						d.remove(dualRow)
						d.remove(belowDualRow)
						comp = getLower(dualRow[j], belowDualRow[j])
						reassignComps(compList, comp, dualRow[j], belowDualRow[j])
						dualRow[j] = comp
						belowDualRow[j] = comp
						d.insert(i, dualRow)
						d.insert(i+1, belowDualRow)
				try:
					otherFace = belowRow[j+1]
				except:
					otherFace = None
				if otherFace != None:
					#for the face down and to the left
					if (otherFace - 1) == face or otherFace == face:
						d.remove(dualRow)
						d.remove(belowDualRow)
						comp = getLower(dualRow[j], belowDualRow[j+1])
						reassignComps(compList, comp, dualRow[j], belowDualRow[j+1])
						dualRow[j] = comp
						belowDualRow[j+1] = comp
						d.insert(i, dualRow)
						d.insert(i+1, belowDualRow)

	return _checkConnected(compList)

#using a seperate component list, the graph is detrimened to be connected if all faces have the same component. Which sould be zero
def getNumFaces(g):
	numFaces = 0
	for i in range(len(g)):
		row = g[i]
		numFaces += len(row)
	return numFaces

#Components in compList from checkConnected are changed as common connections are found.
def reassignComps(compList, newValue, dual1, dual2):
	for i in range(len(compList)):
		if compList[i] == dual1 or compList[i] == dual2:
			compList[i] = newValue
	return compList

#checks if graph is connected if compList (or d) is all of one component
def _checkConnected(d):
	flag = True

	if d.count(0) != len(d):
		flag = False
	return flag					

def getLower(f1, f2):
	if f1 <= f2:
		return f1
	else:
		return f2

#This requires a vertex graph
def makeVertexGraph(faceGraph):
	vertexGraph = []
	faceInt = faceGraphToInts(faceGraph)
	for face in faceGraph:
		for i in range(6):
			x = getXCoor(i, face.getX())
			y = getYCoor(i, face.getY())
			
			v = findVertex(x, y, vertexGraph)
			if v != False:
				v.root = v
				v.addFace(face)
				face.addVertex(i, v)
			else:
				v = Vertex(x, y)
				v.root = v
				v.addFace(face)
				face.addVertex(i, v)
				vertexGraph.append(v)

	for face in faceGraph:
		#this assign the neighbors of the vertices, NOT the faces themsleves
		assignNeighbors(face) 

	return vertexGraph

def getXCoor(loc, faceX):
	if loc == Face.TOP or loc == Face.TOP_LEFT or loc == Face.BOTTOM_LEFT:
		return faceX
	else:
		return faceX + 1

def getYCoor(loc, faceY):
	base = faceY * 2
	if loc == Face.TOP:
		return base
	elif loc == Face.TOP_LEFT or loc == Face.TOP_RIGHT:
		return base + 1
	elif loc == Face.BOTTOM_LEFT or loc == Face.BOTTOM_RIGHT:
		return base + 2
	else:
		return base + 3

def findVertex(x, y, vertexGraph):
	vertex = False
	for v in vertexGraph:
		if v.getY() == y and v.getX() == x:
			vertex = v
			break
	return vertex

#this assign the neighbors of the vertices, NOT the faces themsleves
def assignNeighbors(face):
	verts = face.getVertices()
	topVert = verts[Face.TOP]
	topLeftVert = verts[Face.TOP_LEFT]
	topRightVert = verts[Face.TOP_RIGHT]
	bottomLeftVert = verts[Face.BOTTOM_LEFT]
	bottomRightVert = verts[Face.BOTTOM_RIGHT]
	bottomVert = verts[Face.BOTTOM]

	topVert.addNeighbor(Vertex.LEFT, topLeftVert)
	topVert.addNeighbor(Vertex.RIGHT, topRightVert)

	topRightVert.addNeighbor(Vertex.LEFT, topVert)
	topRightVert.addNeighbor(Vertex.VERTICAL, bottomRightVert)

	bottomRightVert.addNeighbor(Vertex.VERTICAL, topRightVert)
	bottomRightVert.addNeighbor(Vertex.LEFT, bottomVert)

	bottomVert.addNeighbor(Vertex.RIGHT, bottomRightVert)
	bottomVert.addNeighbor(Vertex.LEFT, bottomLeftVert)

	bottomLeftVert.addNeighbor(Vertex.RIGHT, bottomVert)
	bottomLeftVert.addNeighbor(Vertex.VERTICAL, topLeftVert)

	topLeftVert.addNeighbor(Vertex.VERTICAL, bottomLeftVert)
	topLeftVert.addNeighbor(Vertex.RIGHT, topVert)

def isKekulean(graph):
	flag = False
	if len(graph.getVertexGraph()) % 2 == 0:
		if countPeaksAndValleys(graph.getFaceGraph()) == True:
			pm = perfectMatching(graph)
			if pm == True:
				#print "The graph has a perfect matching"
				flag = True
			else:
				pass
				#print "The graph does not have a perfect matching"
		else:
			pass
			#print "The graph does not have the same number of peaks and valleys"
	else:
		pass
		#print "The graph has an uneven number of vertices: ", len(graph.getVertexGraph()) 
	return flag

def perfectMatching(graph):
	r = getR(graph)
	hasPerfectMatching = True

	matched = {}

	while len(r) > 0:
		v = r.pop(0)
		while v.visited == True and len(r) > 0:
			v = r.pop(0)
		if len(r) <= 0:
			#The graph is Kekulean
			break
		v.visited = True
		neighbors = v.getNeighbors()
		try:
			vertical = neighbors["VERTICAL"]
		except:
			vertical = None
		try:
			left = neighbors["LEFT"]
		except: 
			left = None
		try:
			right = neighbors["RIGHT"]
		except:
			right = None

		isolated = isIsolated(v)

		if isolated == True:
			hasPerfectMatching = False
			break
		if vertical is not None:
			if vertical.visited != True:
				matched[v] = vertical
				vertical.visited = True
			else:
				if left is not None:
					if left.visited != True:
						matched[v] = left
						left.visited = True
				elif right is not None:
					if right.visited != True:
						matched[v] = right
						right.visited = True
		elif vertical is None:
			if left is not None:
				if left.visited != True:
						matched[v] = left
						left.visited = True
				elif right is not None:
					if right.visited != True:
						matched[v] = right
						right.visited = True

	return hasPerfectMatching

def getR(graph):
	r = []
	for f in graph.getFaceGraph():
		verts = f.getVertices()
		for v in verts:
			if v not in r:
				v.rQueue = v.getX() - f.getY()
				for vertex in r:
					if v.rQueue < vertex.rQueue:
						r.insert(r.index(vertex), v)
						break
				else:
					r.append(v)
		"""if verts[Face.TOP_LEFT] not in r:
			r.append(verts[Face.TOP_LEFT])
		if verts[Face.TOP] not in r:
			r.append(verts[Face.TOP])
		if verts[Face.TOP_RIGHT] not in r:
			r.append(verts[Face.TOP_RIGHT])
		if verts[Face.BOTTOM_RIGHT] not in r:
			r.append(verts[Face.BOTTOM_RIGHT])
		if verts[Face.BOTTOM] not in r:
			r.append(verts[Face.BOTTOM])
		if verts[Face.BOTTOM_LEFT] not in r:
			r.append(verts[Face.BOTTOM_LEFT])"""
	return r

def isIsolated(v):
	count = 0
	neighbors = v.getNeighbors().values()
	for n in neighbors:
		if n is not None:
			if n.visited == True:
				count += 1
	return count == v.getDegree()


#Counts up all the peaks and valleys of the graph g and returns True if the peak count equals the valley count
def countPeaksAndValleys(graph):
	peakCount = 0
	valleyCount = 0

	fg = faceGraphToInts(graph)

	rowCount  = len(fg)
	
	for r in range(len(fg)):
		row = fg[r]
		for col in range(len(row)):
			face = row[col]
			if searchRow(face, True, fg, r) == True:
				peakCount += 1
				#print "Peak at: " + str(r) + ", " + str(col)
			if searchRow(face, False, fg, r) == True:
				valleyCount += 1
				#print "Valley at: " + str(r) + ", " + str(col)
			
	#print "P: " + str(peakCount) + " V: " + str(valleyCount)	
	if peakCount == valleyCount:
		return True
	else:
		return False
		
#returns a true if f is a peak or valley, false if otherwise
def searchRow(f, up, faceGraph, rowNum):
	flag = False
	#we are checking for peaks by looking for faces in the above row
	if up == True:
		#check if we are on the top row
		if rowNum - 1 < 0:
			flag = True
		else:
			row = faceGraph[rowNum-1]
			#special case for faces that are first in row and zero units away from y-axis in our cooridante system, because -1 index problems
			if f == 0:
				if row.count(f) == 0:
					flag = True
			#All other cases
			else:
				if row.count(f) == 0 and row.count(f-1) == 0:
					flag = True
	else:
		#check if we are on the bottom of the graph
		if rowNum + 1 > len(faceGraph) - 1:
			flag = True
		else:
			#general case algothirm
			row = faceGraph[rowNum + 1]
			if row.count(f) == 0 and row.count(f+1) == 0:
				flag = True
	return flag


def createNewGraph(oldGraph):
	#make a new faceGraph
	oldFace = oldGraph.getFaceGraph()
	newFace = []

	for i in range(len(oldFace)):
		newFace.append(Face(oldFace[i].getX(), oldFace[i].getY()))

	#create the vertexGraph
	newVertexGraph = makeVertexGraph(newFace)

	#add roots to vertices
	for i in range(len(newVertexGraph)):
		newVertexGraph[i].root = oldGraph.getVertexGraph()[i].root

	#create the new root graph
	newRoot = Graph(newFace, newVertexGraph)
	
	#re-create the double bonds 
	if len(oldGraph.getDoubleBonds()) > 0:
		newDoubleBonds = createNewDoubleBonds(oldGraph, newRoot)

	return newRoot

def createNewDoubleBonds(oldGraph, newGraph):
	v1, v2 = oldGraph.getLastAddedPair()
	for oldVertex, oldPair in oldGraph.getDoubleBonds().items():
		if oldVertex != v1 and oldPair != v2:
			newVertex = findVertex(oldVertex.getX(), oldVertex.getY(), newGraph.getVertexGraph())
			newPair = findVertex(oldPair.getX(), oldPair.getY(), newGraph.getVertexGraph())
			newGraph.assignBond(newVertex, newPair)

def createNewFaceGraph(rootFace):
	oldFace = rootFace
	newFace = []

	for i in range(len(oldFace)):
		newFace.append(Face(oldFace[i].getX(), oldFace[i].getY()))

	#add vertices to faces
	for i in range(len(oldFace)):
		newFace[i].assignVertices(oldFace[i].getVertices())

	return newFace

def assignBonds(graph, v1, v2, matching=None, visitedVerts=None):
	#print "in function"
	matchingsList = []	

	#graph.assignBond(v1, v2)

	vList = VertexList()

	matchings = {}
	if matching is not None:
		#print "matchings before", matchings
		#print "parameter", matching
		matchings = matching
		#print "after", matchings
		
	matchings[v1] = v2
	
	visited = {}	
	if visitedVerts is None:
		for key in matchings.keys():
			visited[key] = key
			v = matchings[key]
			visited[v] = v
	else:
		visited = visitedVerts

	#print "matchings:", len(matchings)
	#print "visited:", len(visited)

	for v in graph.getVertexGraph():
		if v in visited:#This means that v is part of the perfect matching
			for n in v.getNeighbors().values():
				if n not in visited:
					#print "adding"
					vList.add(n)
				elif n in vList:
					#print "removeing"
					vList.remove(n)

	#while len(vList) > 0:
	while len(visited) < len(graph.getVertexGraph()):
		added = None
		notKekulean = False
		"""print "\nBonds"
		for k, v in matchings.items():
			print k.getX(), k.getY(), ":", v.getX(), v.getY()"""
		#print "len:", len(matchingsList)
		vertex = vList.pop()
		#print "current V:", v.getX(), v.getY()

		if checkNeighbors(vertex, visited) == False:
			notKekulean = True
			#print "not kekulean"
			break

		if vertex.getDegree() == 2:
			neighbors = vertex.getNeighbors().values()
			for v in neighbors:
				if v not in visited:
					matchings[vertex] = v
					visited[vertex] = vertex
					visited[v] = v
					added = v

		elif vertex.getDegree() == 3:
			#print "in elif"
			#print vertex
			flag = False
			for n in vertex.getNeighbors().values():
				#if n in visited:
					#print n, "is visisited"
				if n not in visited:
					#print n, "is not visisited"
					if flag == False:
						#print "first time", n 	
						flag = True
						matchings[vertex] = n
						visited[vertex] = vertex
						visited[n] = n
						added = n
					else:
						#print "in the else in the elif"
						#print n
						newMatching = dict(matchings)
						newVisited = dict(visited)

						#print "before:", len(matchings)

						del newMatching[vertex]
						del newVisited[vertex]
						del newVisited[added]

						#print "after:", len(matchings)

						newMatching[vertex] = n
						newVisited[vertex] = vertex
						newVisited[n] = n

						matchingsList.extend(assignBonds(graph, vertex, n, newMatching, newVisited))


		if added is not None:
			for n in added.getNeighbors().values():
				if n not in visited:
					if n not in vList:
						#print "adding in while loop"
						vList.add(n)
					else:
						pass#for some reason I think I want to add something here
				elif n in vList:
					#print "removeing"
					vList.remove(n)
		else:
			print "added is None"
			break

		vList.update(visited)

		#print "unvisited count:", graph.unvisitedCount()
	if len(matchings) == len(graph.getVertexGraph())/2 and matchings not in matchingsList:
		matchingsList.append(PerfectMatchingData(matchings))
	
	return matchingsList

def checkNeighbors(v, visited):
	count = 0
	for n in v.getNeighbors().values():
		if n in visited:
			count += 1
	return count != v.getDegree()

def assignMatching(rootGraph):
	verticalEdgeIterator = VerticalEdgeIterator(rootGraph)
	
	matchings = []
	"""while verticalEdgeIterator.hasNext():		
		v1, v2 = verticalEdgeIterator.next()
		#v1 = findVertex(v1.getX(), v1.getY(), graph.getVertexGraph())
		#v2 = findVertex(v2.getX(), v2.getY(), graph.getVertexGraph())
		matchings.extend(assignBonds(rootGraph, v1, v2))"""

	#alternate method, may be just as effectice, faster, and may produce no duplicates
	v1 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP_LEFT]
	v2 = rootGraph.getFaceGraph()[0].getVertices()[Face.BOTTOM_LEFT]
	m1 = assignBonds(rootGraph, v1, v2)
	matchings.extend(m1)

	v3 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP_LEFT]
	v4 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP]
	m2 = assignBonds(rootGraph, v3, v4)
	matchings.extend(m2)

	matchingSet = removeDuplicates(matchings)

	matched = []
	for m in matchingSet:
		matched.append(m.getMatching())

	ret = []
	for m in matched:
		#g = Graph(rootGraph.getFaceGraph(), rootGraph.getVertexGraph())
		g = copy.copy(rootGraph)
		g.faceGraph = createNewFaceGraph(rootGraph.getFaceGraph())
		g.setDoubleBonds(m)
		ret.append(g)

	ret = assignFriesAndClars(ret)

	return ret

def assignFriesAndClars(graphs):
	for g in graphs:
		g.assignFriesFaces()
		g.assignClarsFaces()
	return graphs

def displayGraphs(graphs):
	if len(graphs) > 0:
		index = int(raw_input("what graph do you want to look at? "))
		while index != -1:
			
			graph = graphs[index]

			print "Graph", index
			print graph.toString()

			print "Fries Number:", graph.getFriesNumber(), " Clars Number:", graph.getClarsNumber()

			print "Double Bonds Length:", len(graph.getDoubleBonds()) 
			for v1, v2 in graph.getDoubleBonds().items():
				print v1.getX(), ",", v1.getY(), ":", v2.getX(), ",", v2.getY()
			print "\n"
			
			graph.displayGraph()
			print "There are", len(graphs), "Kekule structures"
			index = int(raw_input("what graph do you want to look at? "))

def analyzeGraphFromFile(fileName="graph.txt"):
	faceGraph = getInput(fileName)
	matchingsList = []

	#check for connectedness
	connected = isConnected(faceGraphToInts(faceGraph))
	if connected == True:
		print "Graph is connected"

		vertexGraph = makeVertexGraph(faceGraph)

		rootGraph = Graph(faceGraph, vertexGraph)
		kekulean = isKekulean(rootGraph)
		if kekulean == True:
			print "There are", len(vertexGraph), "vertices"

			graphs = assignMatching(rootGraph)
			print "There are", len(graphs), "PM's"

			#graphs = assignFriesAndClars(graphs)
			displayGraphs(graphs)
		else:
			print "Not Kekulean"
	else:
		print "Graph is not connected"

#A user-entered number of graphs are generated and tested for Kekulean-ness and written to their proper text files
def randomIntoFiles():
	kekuleanFile = open("Kekuleans.txt", "w")
	notKekuleanFile = open("NotKekulean.txt", "w")
	
	numK = 0
	numNotK = 0
	
	trials = int(raw_input("How many graphs would you like to create? "))
	print "\n" #just to provide some visual space	
	
	t1 = time.time()

	for i in range(trials):
		faceGraph = createRandomGraph()
		vGraph = makeVertexGraph(faceGraph)
		randGraph = Graph(faceGraph, vGraph)

		if isKekulean(randGraph) == True:
			numK += 1
			
			kekuleanFile.write("Graph #" + str(numK) + "\n")
			kekuleanFile.write(randGraph.simpleToString() + '\n')
		else:
			numNotK += 1
			
			notKekuleanFile.write("Graph #" + str(numNotK) + "\n")
			notKekuleanFile.write(randGraph.simpleToString() + '\n')
		#print randGraph
		#print "\n"

	t2 = time.time()

	print "\n" + str(numK) + " Kekulean graph(s) were found.\n" + str(numNotK) + " non-Kekulean graph(s) were found."
	print "Time elapsed (in seconds): " + str(t2 - t1) + "\n"
	kekuleanFile.close()
	notKekuleanFile.close()

#creates a random Kekulean graph		
def createRandomKekulean():
	#creates a face graphs
	randomFaces = createRandomGraph()

	while isConnected(faceGraphToInts(randomFaces)) == False:
		randomFaces = createRandomGraph()

	vertexGraph = makeVertexGraph(randomFaces)
	randomGraph = Graph(randomFaces, vertexGraph)

	while isKekulean(randomGraph) == False:
		randomFaces = createRandomGraph()
		while isConnected(faceGraphToInts(randomFaces)) == False:
			randomFaces = createRandomGraph()

		vertexGraph = makeVertexGraph(randomFaces)
		randomGraph = Graph(randomFaces, vertexGraph)

	graphs = assignMatching(randomGraph)

	if len(graphs) > 0:
		print "There are", len(graphs), "Kekulean structures"
		graphs = assignFriesAndClars(graphs)
		displayGraphs(graphs)
	else:
		print "error - see error.txt for graph"
		errorFile = open("error.txt", "w")
		errorFile.write(randomGraph.simpleToString() + '\n')

#Creates a random planar graph, which may not be connected			
def createRandomGraph():
	height = randint(3, 10)
	
	randGraph = []
	for i in range(height):
		rowLength = randint(3, 10)
		row = getRow(rowLength, i)
		while len(row) == 0:
			row = getRow(rowLength, i)
		randGraph.extend(row)
	#print randGraph
	return randGraph

#generates a row for the the createRandomGraph method
def getRow(rl, rowNum):
	r = []
	for j in range(rl): 
			chance = randint(0, 1)
			if chance == 1:
				r.append(Face(j, rowNum))
	return r

def removeDuplicates(matchings):
	for i in matchings:
		for j in matchings:
			if i != j: 
				if cmp(i.getExpandedMatching(), j.getExpandedMatching()) == 0:
					#This implies that the two graphs match one-for-one
					print "deleting"
					del matchings[matchings.index(j)]
	return matchings

def createManyKekuleans():
	graphs = [] #list of kekulean graphs 
	graphList = [] #list of the Kekulean graphs with their matchings, and Fries/Clars Faces 
	trials = int(raw_input("How many graphs would you like to create? "))

	for i in range(trials):
		#creates a face graphs
		randomFaces = createRandomGraph()

		while isConnected(faceGraphToInts(randomFaces)) == False:
			randomFaces = createRandomGraph()

		vertexGraph = makeVertexGraph(randomFaces)
		randomGraph = Graph(randomFaces, vertexGraph)

		while isKekulean(randomGraph) == False:
			#print "making K"
			randomFaces = createRandomGraph()
			while isConnected(faceGraphToInts(randomFaces)) == False:
				randomFaces = createRandomGraph()

			vertexGraph = makeVertexGraph(randomFaces)
			randomGraph = Graph(randomFaces, vertexGraph)

		print "There are", len(vertexGraph), "vertices"

		graphs.append(randomGraph)



	for g in graphs:
		graphList.extend(assignMatching(g))

	if len(graphList) > 0:
		print "There are", len(graphList), "Kekulean structures"
		graphList = assignFriesAndClars(graphList)
		displayGraphs(graphList)

def testKekuleanThms():
	conflict = False

	t1 = time.time()

	counter = 0
	while conflict != True:
		print "graph #" + str(counter)

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		nelsonThm = isOldKekulean(randomGraph)
		perfectMatchingThm = isKekulean(randomGraph)

		if nelsonThm != perfectMatchingThm:
			print "conflict"
			errorFile = open("conflict.txt", "w")
			errorFile.write("Perfect matching: " + str(perfectMatchingThm) + " Nelson Thm: " + str(nelsonThm) + "\n")
			errorFile.write(randomGraph.simpleToString())
			errorFile.close()
			conflict = True

			t2 = time.time()
			print "Time elapsed (in seconds): " + str(t2 - t1) + "\n"

			print randomGraph.debugString()
			#for row in faceGraphToInts(randomFaces):
			#	print len(row)

		else:
			pass
			#print "no conflict"
			#print randomGraph.simpleToString()
		counter += 1

#takes a row and returns a the number of vertical edges in that row
def getRowEdgeCount(row):
	edgeCount = 0
	f = 0
	for i in range(len(row)):
		edgeCount += 1
		try:
			f = row[i+1]
		except:
			f = None
		if row[i] + 1 != f or f == None:
			edgeCount += 1
	return edgeCount
	
#counts up the number of peaks above each row and stores those values in a list at indexes that correspond to the the row of the graph
def getPeaksAboveRows(g):

	peaksAboveRow = [0]*(len(g))
	
	for r in range(len(g)):
		#print "r: " + str(r)
		row = g[r]
		if r > 0:
			peaksAboveRow[r] += peaksAboveRow[r-1]
		for col in range(len(row)):
			face = row[col]
			if searchRow(face, True, g, r) == True:
				peaksAboveRow[r] += 1
				#print "Peak at: " + str(r) + ", " + str(col)
			if searchRow(face, False, g, r) == True and r < len(g)-1:
				peaksAboveRow[r+1] -= 1
				#print "Valley at: " + str(r) + ", " + str(col)
			peaksAboveRow[r] = abs(peaksAboveRow[r])
				
	return peaksAboveRow
	
#Theorem I devoloped
def NelsonThm(peaks, g):
	kekulean = True
	for i in range(len(g)):
		row = g[i]
		#print "P: " + str(peaks[i]) + "Edges: " + str(getRowEdgeCount(row))
		if peaks[i] > getRowEdgeCount(row):
			kekulean = False
			break
	return kekulean
	
#ckesks of a graph is Kekulean and returns a boolean
def isOldKekulean(graph):
	fg = faceGraphToInts(graph.getFaceGraph())	

	peaksAbove = getPeaksAboveRows(fg)
	#print peaksAbove
	
	kekulean = NelsonThm(peaksAbove, fg)
		
	return kekulean

def getUpperBonds(filename='graph.txt'):
	faceGraph = getInput(filename)
	vertexGraph = makeVertexGraph(faceGraph)

	graph = Graph(faceGraph, vertexGraph)

	kekulean = isKekulean(graph)
	if kekulean == True: 
		rowCount = [0] * graph.getNumberOfRows()
		whiteCount = [0] * graph.getNumberOfRows()
		blackCount = [0] * graph.getNumberOfRows()

		print "len:", len(whiteCount)

		for v in graph.getVertexGraph():
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

		print "Upper Bonds of the graph per row:"
		for index in range(len(rowCount)):
			count = abs(sum(whiteCount[0:index+1]) - sum(blackCount[0:index+1]))
			print count
			rowCount[index] = count

		totalUpperBonds = sum(rowCount)
		print "Upper bond of the graph:", totalUpperBonds


	else:
		print "The graph is not Kekulean"

#The Main

selection = 0
while True:
	print "1) Read graph from graph.txt\n2) Get a random Kekulean graph\n3) Create and test random graphs\n4) Create several Kekuleans\n5) Don't click\n6) Test Nelson Thm\n7) Get Upper Bonds\n8) Quit"
	selection = int(raw_input("Selection: "))
	while selection < 1 or selection > 8:
		 print "\nInvalid response, please enter a proper selection."
		 print "1) Read graph from graph.txt\n2) Get a random Kekulean graph\n3) Create and test random graphs\n4) Create several Kekuleans\n5) Don't Click\n6) Test Nelson Thm\n7) Get Upper Bonds\n8) Quit"
		 selection = int(raw_input("Selection: "))

	if selection == 1:
		analyzeGraphFromFile()
	elif selection == 2:
		createRandomKekulean()
	elif selection == 3:
		randomIntoFiles()
	elif selection == 4:
		createManyKekuleans()
	elif selection == 5:
		randomIntoFilesThreaded()
	elif selection == 6:
		testKekuleanThms()
	elif selection == 7:
		getUpperBonds()
	else:
		sys.exit()
