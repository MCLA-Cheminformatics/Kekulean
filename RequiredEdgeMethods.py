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
			masterSet = masterSet & edgeSet
		graphNumber += 1
	return masterSet

def getExternalEdges(edges):
	externalEdges = set()
	for v1, v2 in edges:
		if len(v1.getFaces() & v2.getFaces()) == 1:
			externalEdges.add((v1,v2))
	return externalEdges