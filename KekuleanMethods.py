from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from ConjectureData import *
from DriverMethods import *
from Output import *
from Checkers import *

#These methods check to see if the graph is Kekulean.

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
		#print "current V:", vertex
		if vertex is None:
			break

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


def assignFriesAndClars(graphs):
	try: 
		for g in graphs:
			g.assignFriesFaces()
			g.assignClarsFaces()
		return graphs
	except:
		graphs.assignFriesFaces()
		graphs.assignClarsFaces()
	return graphs 

def assignMatching(rootGraph):	
	matchings = []

	#This section finds all the matchings in the graph
	face = rootGraph.getFaceGraph()[0]

	d = {0:5, 5:0, 4:5, 5:4}
	for i in d:
		v1 = face.getVertices()[i]
		v2 = face.getVertices()[d[i]]
		m = assignBonds(rootGraph, v1, v2)
		matchings.extend(m)
 
	matchings = removeDuplicates(matchings)


	#This section makes graph objects out of the matchings found.
	graphs = []
	for m in matchings:
		g = copy.copy(rootGraph)
		g.faceGraph = createNewFaceGraph(rootGraph.getFaceGraph()) 

		g._assignFaceNeighbors()
		g.setDoubleBonds(m.getMatching())
		#g.update(m.getMatching())
		
		graphs.append(g)

	#multiprocessing
	#pool = mp.Pool(mp.cpu_count())

	#r = [pool.map(assignFriesAndClars, graphs)]
	#results = [item for sublist in r for item in sublist]
	
	#non-multiprocessing
	results = assignFriesAndClars(graphs)

	#ret = assignFriesAndClars(ret)

	return results

def removeDuplicates(matchings):
	tempMatchings = []

	#old method that works, but may be too slow
	for pm in matchings:
		for tpm in tempMatchings:
			if pm is tpm:
				break
			if pm.getExpandedMatching() == tpm.getExpandedMatching():
				break
		else:
			tempMatchings.append(pm)

	return tempMatchings