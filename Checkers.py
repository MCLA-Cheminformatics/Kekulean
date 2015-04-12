from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from Output import *
from KekuleanMethods import *

#These methods help create the graph from the input and helps check for other needed properties, like connectness.

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
	queue = []

	#make faceGraph
	faceGraph = []
	y = 0
	while y < len(g):
		row = g[y]		
		for x in row:
			faceGraph.append((Face(int(x), y)))
		y += 1

	vg = makeVertexGraph(faceGraph)
	graph = Graph(faceGraph, vg)
		
	queue.append(graph.getFaceGraph()[0])
	visited = set()

	while len(visited) < len(graph.getFaceGraph()):
		face = queue.pop(0)
		while face in visited:
			#print "in while"
			if len(queue) > 0:
				face = queue.pop(0)
			else:
				break
		#this means that the face is visited and grpah is disconnected	
		if face in visited:
			break

		nextGroup = face.getNeighbors()
		if len(nextGroup) == 0:
			break
		else:
			queue.extend(nextGroup)

		#print "stats"
		#print len(graph.getFaceGraph()), len(queue), len(visited)
		visited.add(face)

		#print "graph"
		#print graph
		#print "-------------------"
	return len(graph.getFaceGraph()) == len(visited)

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

def isKekulean(graph):
	flag = False
	if len(graph.getVertexGraph()) % 2 == 0:
		if countPeaksAndValleys(graph.getFaceGraph()) == True:
			#pm = perfectMatching(graph)
			pm = isPM(graph)
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

def checkNeighbors(v, visited):
	count = 0
	#print v
	for n in v.getNeighbors().values():
		if n in visited:
			count += 1
	return count != v.getDegree()

def isPM(rootGraph):
	found = False
	v1 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP_LEFT]
	v2 = rootGraph.getFaceGraph()[0].getVertices()[Face.BOTTOM_LEFT]
	found = findPM(rootGraph, v1, v2)

	if found == False:
		v3 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP_LEFT]
		v4 = rootGraph.getFaceGraph()[0].getVertices()[Face.TOP]
		found = findPM(rootGraph, v3, v4)

	return found

def findPM(graph, v1, v2, matching=None, visitedVerts=None):
	#matchingList = []
	found = False

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
	while len(visited) < len(graph.getVertexGraph()) and found == False:
		added = None
		"""print "\nBonds"
		for k, v in matchings.items():
			print k.getX(), k.getY(), ":", v.getX(), v.getY()"""
		#print "len:", len(matchingsList)
		vertex = vList.pop()
		#print "current V:", v.getX(), v.getY()
		if vertex is None:
			break

		if checkNeighbors(vertex, visited) == False:
			found = False
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

						found = findPM(graph, vertex, n, newMatching, newVisited)


		if added is not None and found == False:
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
		elif added is None:
			#print "added is None"
			break

		vList.update(visited)

		#print "unvisited count:", graph.unvisitedCount()
	if len(matchings) == len(graph.getVertexGraph())/2:
		 found = True
	return found 
 
def perfectMatching(graph):
	w = getW(graph)
	r = getR(w)
	hasPerfectMatching = True

	graph.assignUpperBounds()
	rowCount = graph.rowCount

	matched = {}

	while len(r) > 0 and hasPerfectMatching == True:
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
		#print "\nCurrent Vertex:", v 
		#print "there are", len(neighbors), "neighbors"
		#for n in v.getNeighbors().values():
		#	print "\t", n, ":", n.visited
		#print "isolated:", isolated
		#print "matchings thus far"
		#for v1, v2 in matched.items():
		#	print v1, ":", v2


		found = False

		if isolated == True:
			hasPerfectMatching = False

		elif vertical is not None:
			if vertical.visited == False:
				faces = vertical.getFaces() & v.getFaces()
				index = faces.pop().getY()
				if rowCount[index] > 0:
					rowCount[index] -= 1
					matched[v] = vertical
					vertical.visited = True
					found = True
			elif found == False:
				if left is not None:
					if left.visited == False:
						matched[v] = left
						left.visited = True
						found = True
				if right is not None and found == False:
					if right.visited == False:
						matched[v] = right
						right.visited = True
						found = True
		elif vertical is None:
			if left is not None:
				if left.visited == False:
						matched[v] = left
						left.visited = True
						found = True
				if right is not None and found == False:
					if right.visited == False:
						matched[v] = right
						right.visited = True
						found = True

	#print "number of unmatched vertices:", graph.unvisitedCount()
	return hasPerfectMatching

def isIsolated(v):
	count = 0
	neighbors = v.getNeighbors().values()
	for n in neighbors:
		if n is not None:
			if n.visited == True:
				count += 1
	return count == v.getDegree()