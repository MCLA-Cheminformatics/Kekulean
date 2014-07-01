class PerfectMatchingData(object):
	def __init__(self, matching):
		self.matching = matching

		self.expandedMatching = {}
		
		for k, v in self.matching.items():
			self.expandedMatching[k] = v
			self.expandedMatching[v] = k
		
	def getMatching(self):
		return self.matching
	def getExpandedMatching(self):
		return self.expandedMatching