def getRequiredSet(graphs):
	masterSet = set()
	graphNumber = 0
	for g in graphs:
		edgeSet = set()
		for k, v in g.getDoubleBonds().items():
			if hash(k) < hash(v):
				edge = (k, v)
			else:
				edge = (v, k)
			edgeSet.add(edge)
		if len(masterSet) == 0 and graphNumber == 0:
			masterSet.update(edgeSet)
		else:
			#this gets just the required edges
			masterSet = masterSet & edgeSet
		graphNumber += 1
	return masterSet

def getExternalEdges(edges):
	externalEdges = set()
	for v1, v2 in edges:
		if len(v1.getFaces() & v2.getFaces()) == 1:
			face = (v1.getFaces() & v2.getFaces()).pop()
			direction = getDirection(face, v1, v2)
			
			if direction is not None:
				externalEdges.add((v1, v2))
	return externalEdges

def getDirection(face, v1, v2):
	index1 = face.getVertices().index(v1)
	index2 = face.getVertices().index(v2)

	directions = {(0,1): 'TOP_RIGHT', (1,2): 'RIGHT', (2,3): 'BOTTOM_RIGHT', (3,4): 'BOTTOM_LEFT', (4,5): 'LEFT', (5,0): 'TOP_LEFT'}

	if (index1,index2) in directions:
		return directions[(index1,index2)]
	elif (index2,index1) in directions:
		return directions[(index2,index1)]
	else:
		return None

def getComplements(edgesA, edgesB):
	complements = set()

	for edgeA in edgesA:
		for edgeB in edgesB:
			if areComplements(edgeA, edgeB):
				complements.add((edgeA, edgeB))

def areComplements(edgeA, edgeB):
	complements = {'TOP_LEFT':'BOTTOM_LEFT', 'RIGHT':'LEFT', 'TOP_RIGHT':'BOTTOM_RIGHT'}

	if edgeB[2] == complements[edgeA[2]]:
		return True
	elif edgeA[2] == complements[edgeB[2]]:
		return True
	else:
		return False
