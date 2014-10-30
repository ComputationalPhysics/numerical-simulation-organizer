"""
>>> simForest = SimulationForest()
>>> sims = [Simulation("1"), Simulation("11"), Simulation("5", "2"), Simulation("6", "3"), Simulation("7", "3"), Simulation("2", "1"), Simulation("3", "1"), Simulation("4", "3")]
>>> for sim in sims:
...		simForest.add(sim)
Added new root simulation
Added new root simulation
>>> for key in simForest.simulations:
... 	if not simForest.simulations[key].parentID:
...			simForest.simulations[key].printChildIDsRecursive()
11
1
1 ---> 3
3 ---> 4
3 ---> 7
3 ---> 6
1 ---> 2
2 ---> 5
>>> simForest.simulations["4"].printParentIDsRecursive()
4
3
1
>>> print simForest.missingRelations
{}
"""


class Simulation:
	def __init__(self, id, parentID=None):
		# Critical variables
		self.id = id
		self.parent = None
		self.parentID = parentID
		self.children = {}				

		self.lastKnownLocations = [] 	# Place to look for simulation data to avoid searching for it.
		self.tags = set([])					# For searching in simulations.

	def addChild(self, child):
		self.children[child.id] = child

	def addTag(self, string):
		tags.add(string)

	def printChildIDsRecursive(self):
		print self.id
		for key in self.children:
			print self.id, "--->" , 
			self.children[key].printChildIDsRecursive()

	def printParentIDsRecursive(self):
		print self.id
		if self.parent:
			self.parent.printParentIDsRecursive()

class SimulationForest:
	def __init__(self):
		self.roots = {}
		self.simulations = {}
		self.missingRelations = {} # To put ID for parents reported missing by their children
	
	def add(self, newSim):
		""" Add a simulation to the forest. 
		If the simulation has a parent in the forest, it shall be included in the right tree.
		If the simulation has a children in the forest, they have to be root nodes before they are set as children of the new simulation.
		If the simulation doesn't have a parent and no children, it is the root of its own tree. 
		"""
		if newSim.id not in self.simulations:
			if newSim.parentID:
				if newSim.parentID in self.simulations:
					self.simulations[newSim.parentID].addChild(newSim)
					newSim.parent = self.simulations[newSim.parentID]
				else:
					if newSim.parentID in self.missingRelations:
						self.missingRelations[newSim.parentID].append(newSim.id)
					else:
						self.missingRelations[newSim.parentID] = [newSim.id]
			else:
				print "Added new root simulation"

			if newSim.id in self.missingRelations:
				for child in self.missingRelations[newSim.id]:
					self.simulations[child].parent = newSim
					newSim.addChild(self.simulations[child])
				self.missingRelations.pop(newSim.id)

			self.simulations[newSim.id] = newSim
		else:
			print "Simulation with id:", simulation.id, "already exists"

	def get(self, id):
		if id in self.simulations:
			return self.simulations[id]

	def sendToDatabase(self):
		raise NotImplementedError

	def getFromDatabase(self):
		raise NotImplementedError



if __name__ == '__main__':
	simForest = SimulationForest()
	sims = [Simulation("1"), Simulation("11"), Simulation("5", "2"), Simulation("6", "3"), Simulation("7", "3"), Simulation("2", "1"), Simulation("3", "1"), Simulation("4", "3")]
	for sim in sims:
		simForest.add(sim)

	for key in simForest.simulations:
		if not simForest.simulations[key].parentID:
			simForest.simulations[key].printChildIDsRecursive()
 	simForest.simulations["4"].printParentIDsRecursive()
	print simForest.missingRelations
 