from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from Output import *
from KekuleanMethods import *
from Checkers import *
from RequiredEdgeMethods import *

from random import randint
import time
import os

#These methods the main drivers of the program. Some of their helper methods are also present here.

settings = {}

#function that reads in the graph returns a 2D string list of the graph
def getInput(fileName):
	faceGraph = []
	inputFile = open(fileName, 'r')
	
	row = inputFile.readline()
	y = 0
	while len(row) > 0:
		row = row.replace('\n', '')
		row = row.split(" ")		
		
		for i in range(len(row)):
			x = row[i]
			faceGraph.append((Face(int(x), y)))

		row = inputFile.readline()
		y += 1
		
	inputFile.close()
		
	return faceGraph

def getSettings():
	settingsFile = open('settings.txt', 'r')
	
	line = settingsFile.readline()
	while len(line) > 0:
		line = line.replace('\n', '')
		line = line.split(":")		
		
		settings[line[0]] = float(line[1])

		line = settingsFile.readline()

	settingsFile.close()

def analyzeGraphFromFile(fileName="graph.txt"):
	faceGraph = getInput(fileName)
	matchingsList = []

	#check for connectedness
	connected = isConnected(faceGraphToInts(faceGraph))
	if connected == True:
		print "Graph is connected"

		vertexGraph = makeVertexGraph(faceGraph)

		rootGraph = Graph(faceGraph, vertexGraph)

		graphs = assignMatching(rootGraph)
		if len(graphs) > 0:
			print "There are", len(vertexGraph), "vertices"

			#graphs = assignMatching(rootGraph)
			print "There are", len(graphs), "PM's"			

			#must be 'fries' or 'clars'
			graphs.sort()
			graphs.reverse()
			
			_findRequiredEdges(graphs)

			#save graphs as PNG file
			savePNG(graphs, "graphs - Fries.png")

			Graph.comparison = 'clars'
			graphs.sort()
			graphs.reverse()

			savePNG(graphs, "graphs - Clars.png")
 
			while True:
				choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
				while choice.lower() != 'fries' and choice.lower() != 'clars' and choice.lower() != 'quit':
					choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
				if choice.lower() == 'clars':
					Graph.comparison = 'clars'

				elif choice.lower() == 'fries':
					Graph.comparison = 'fries'

				else:
					break
					
				graphs.sort()
				graphs.reverse()
				
				displayGraphs(graphs)
		else:
			print "Not Kekulean"
			#graphs = assignMatching(rootGraph)
			#print "Trying anyway, there are", len(graphs), "PM's"
			#displayGraphs(graphs)
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
		faceGraph = createRandomConnectedGraph()
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

#creates a random Kekulean graph ands does stuff with it and saves it to an png		
def createRandomKekulean():
	#creates a face graphs
	randomFaces = createRandomGraph()

	randomGraph = _createRandomKekulean()

	print "There are", len(randomGraph.getVertexGraph()), "vertices"

	graphs = assignMatching(randomGraph)
	graphs.sort()

	if len(graphs) > 0:
		#save graphs as PNG file
		savePNG(graphs, "graphs - Fries.png")

		Graph.comparison = 'clars'
		graphs.sort()

		savePNG(graphs, "graphs - Clars.png")

		while True:
			choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
			while choice.lower() != 'fries' and choice.lower() != 'clars' and choice.lower() != 'quit':
				choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
			if choice.lower() == 'clars':
				Graph.comparison = 'clars'

			elif choice.lower() == 'fries':
				Graph.comparison = 'fries'

			else:
				break
					
			graphs.sort()
			graphs.reverse()
			
			print "There are", len(graphs), "Kekulean structures"
			displayGraphs(graphs)
		
	else:
		print "error - Graph is Kekulean but has no perfect matching - see error.txt for graph"
		errorFile = open("error.txt", "w")
		errorFile.write(randomGraph.simpleToString() + '\n')

#Creates a random planar graph, which may not be connected			
def createRandomGraph():
	height = randint(settings["MIN_HEIGHT"], settings["MAX_HEIGHT"])
	
	randGraph = []
	for i in range(height):
		rowLength = randint(settings["MIN_WIDTH"], settings["MAX_WIDTH"])
		row = getRow(rowLength, i)
		while len(row) == 0:
			row = getRow(rowLength, i)
		randGraph.extend(row)
	
	if checkAlignment(randGraph) == False:
		randGraph = createRandomGraph()
	return randGraph

def checkAlignment(graph):
	for face in graph:
		if face.getX() == 0:
			break
	else:
		#there is no face on the y-axis
		return False
	for face in graph:
		if face.getY() == 0:
			break
	else:
		#there is no face on the x-axis
		return False
	#there is a face on the x-axis
	return True

def createRandomConnectedGraph():
	g = createRandomGraph()
	while isConnected(faceGraphToInts(g)) == False:
		g = createRandomGraph()

	return g

#generates a row for the the createRandomGraph method
def getRow(rl, rowNum):
	r = []
	for j in range(rl): 
			chance = randint(0, 100)
			if chance > settings['POROSITY'] * 100:
				r.append(Face(j, rowNum))
	return r

def _createRandomKekulean():
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
	return randomGraph

def createManyKekuleans():
	graphs = [] #list of kekulean graphs 
	graphList = [] #list of the Kekulean graphs with their matchings, and Fries/Clars Faces 
	trials = int(raw_input("How many graphs would you like to create? "))

	pool = mp.Pool(mp.cpu_count())
	results = [pool.apply_async(_createRandomKekulean) for x in range(trials)]
	graphs = [r.get() for r in results]

	for g in graphs:
		graphList.extend(assignMatching(g))

	graphList.sort()

	if len(graphList) > 0:
		print "There are", len(graphList), "Kekulean structures"
		displayGraphs(graphList)

def testKekuleanThms():
	conflictFile = open("conflict.txt", "w")

	interval = float(raw_input("How many hours would you like to run the program?"))

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	counter = 0
	while t2 - t1 < timeLimit:
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
			
			conflictFile.write("Perfect matching: " + str(perfectMatchingThm) + " Nelson Thm: " + str(nelsonThm) + "\n")
			conflictFile.write(randomGraph.simpleToString())
			conflictFile.write("\n") 

		t2 = time.time()
		counter += 1
	conflictFile.close()

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

def getMinRows(g):
	minRows = {}
	index = 0
	minEdges = sys.maxint
	for r in g:
		edgeCount = getRowEdgeCount(r)
		if edgeCount < minEdges:
			minEdges = edgeCount
			minRows.clear()
			minRows[index] = r
		elif edgeCount == minEdges:
			minRows[index] = r
		index += 1
	return minRows
	
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
	minRows = getMinRows(g)
	for i, row in minRows.items():
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

def getUpperBounds(graph):
	#faceGraph = getInput(filename)
	#vertexGraph = makeVertexGraph(faceGraph)

	#graph = Graph(faceGraph, vertexGraph)

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

def testConjecture(hours=0):
	graphList = []
	results = open("results.txt", "w")
	results.write("The program actually run!")

	if hours == 0:
		interval = float(raw_input("How many hours would you like to run the program? "))
	else:
		interval = hours

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	counter = 0
	while t2 - t1 < timeLimit:
		print "graph #" + str(counter)

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)
			
			#must be 'fries' or 'clars'
			Graph.comparison = 'clars'
			structures.sort()

			h = structures[-1]
			h.setNumStructures(len(structures))
			#h.setString(structures[0].simpleToString())

			#is the data right?
			#print "Verts:", h.getNumVertices()
			#print "Structures:", h.getNumStructures()
			#print "Clar:", h.getFriesNumber()

			for g in graphList:
				if h.getNumVertices() == g.getNumVertices():
					if h.getNumStructures() < g.getNumStructures():
						if h.getClarsNumber() > g.getClarsNumber():
							print 'Conjecture is false:'
							results.write('\ngraph H: Clars: ' + str(h.getClarsNumber()) + " Number of Structures: " + str(h.getNumStructures()) + " Number of vertices: " + str(h.getNumVertices()) + "\n") 
							results.write(str(h))
							results.write('\ngraph G: Clars: ' + str(g.getClarsNumber()) + " Number of Structures: " + str(g.getNumStructures()) + " Number of vertices: " + str(g.getNumVertices()) + "\n") 
							results.write(str(g))
							results.write("\n\n")

							drawConflicts(g, h)

			#only adds graphs to list if it under some number of vertices
			graphList.append(h)

		t2 = time.time()
		counter += 1

def findHighestClars(graphs):
	clars = 0
	for g in graphs:
		if g.getClarsNumber() > clars:
			clars = g.getClarsNumber()
	return clars

def _findRequiredEdges(graphs):
	masterSet = getRequiredSet(graphs)
	if len(masterSet) > 0:
		for edge in masterSet:
			v1, v2 = edge
			v1.required = True
			v2.required = True
		return True
	else:
		return False
	
def findRequiredEdges(hours=0):
	if not os.path.exists("requiredEdges"):
		os.mkdir("requiredEdges")

	edgeFile = open("requiredEdges/RequiredEdges.txt", "w")
	graphNumber = 0
	rqNum = 0

	flag = False
	if hours == 0:
		interval = float(raw_input("How many hours would you like to run the program? "))
	else:
		interval = hours

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:
		print "graph", graphNumber

		flag = False

		graph = _createRandomKekulean()
		graphs = assignMatching(graph)
		
		flag = _findRequiredEdges(graphs)
		if flag == True:
			print "Found graph with required edges"
			edgeFile.write("Graph: " + str(rqNum) + "\n")
			edgeFile.write(graph.simpleToString())
			edgeFile.write("\n\n")

			#save PNG's
			fileName = "requiredEdges/Graph" + str(rqNum) + ".png"
			saveSinglePNG(graphs[0], fileName)
			rqNum += 1

		graphNumber += 1
		t2 = time.time()

def combineGraphs():
	graphNumber = 0
	superGraphNumber = 0
	storedGraphs = {}

	interval = float(raw_input("How many hours would you like to run the program? "))

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:
		print "graph", graphNumber

		flag = False

		graph = _createRandomKekulean()

		#For testing
		#fgraph = getInput("graph.txt");
		#vgraph = makeVertexGraph(fgraph)
		#graph = Graph(fgraph, vgraph)

		matchings = assignMatching(graph)
		
		req_edges = getRequiredSet(matchings)
		externalEdges = getExternalEdges(req_edges)

		#print len(externalEdges)
		#for edge in externalEdges:
		#	face = (edge[0].getFaces() & edge[1].getFaces()).pop()
		#	print face, "\t", face.getVertices().index(edge[0]), "\t", face.getVertices().index(edge[1])

		if len(externalEdges) > 0:
			#add graph and edges to list
			storedGraphs[graph] = externalEdges

			for g, edges in storedGraphs.items():
				complements = getComplements(externalEdges, edges)

				#print "len", len(complements)
				for edge, compEdge in complements:
					faceA = (edge[0].getFaces() & edge[1].getFaces()).pop()
					#print compEdge
					faceB = (compEdge[0].getFaces() & compEdge[1].getFaces()).pop()
					
					x = faceA.getX() - faceB.getX()
					y = faceA.getY() - faceB.getY()
					#print "A:   x:", faceA.x, "y:", faceA.y
					#print "B:   x:", faceB.x, "y:", faceB.y
					#print "xdiff:", x, "ydiff:", y
					if edge[2] == "TOP_RIGHT" and compEdge[2] == "BOTTOM_LEFT":
						newGraph = offsetFaces(g, x, y + 1);
					elif edge[2] == "RIGHT" and compEdge[2] == "LEFT":
						newGraph = offsetFaces(g, x + 1, y);
					elif edge[2] == "TOP_LEFT" and compEdge[2] == "BOTTOM_RIGHT":
						newGraph = offsetFaces(g, x + 1, y + 1);

					elif edge[2] == "BOTTOM_LEFT" and compEdge[2] == "TOP_RIGHT":
						newGraph = offsetFaces(g, x, y - 1);
					elif edge[2] == "LEFT" and compEdge[2] == "RIGHT":
						newGraph = offsetFaces(g, x - 1, y);
					elif edge[2] == "BOTTOM_RIGHT" and compEdge[2] == "TOP_LEFT":
						newGraph = offsetFaces(g, x - 1, y - 1);

					overlap = checkFaceOverlap(graph, newGraph)
					print overlap
					if overlap is False:
						faceGraph = graph.getFaceGraph() + newGraph.getFaceGraph()
						faceGraph = adjustForNegatives(faceGraph)
								
						vertexGraph = makeVertexGraph(faceGraph)
						superGraph = Graph(faceGraph, vertexGraph)

						if not os.path.exists("CombinedGraphs"):
							os.mkdir("CombinedGraphs")

						folderName = "CombinedGraphs/superGraph" + str(graphNumber)
						#setup folder
						if not os.path.exists(folderName):
							os.mkdir(folderName)

						#save PNG's
						superName = folderName + "/superGraph.png"
						saveSinglePNG(superGraph, superName)

						graphName = folderName + "/graphA.png"
						saveSinglePNG(graph, graphName)

						graphName = folderName + "/graphB.png"
						saveSinglePNG(newGraph, graphName)

						f = open(folderName + "/graphs.txt", 'w')
						f.write('graph A\n')
						f.write(str(graph) + '\n\n')

						f.write('graph B\n')
						f.write(str(newGraph) + '\n\n')

						f.write('super graph\n')
						f.write(str(superGraph) + '\n')

						f.close()

						superGraphNumber += 1

		graphNumber += 1
		t2 = time.time()