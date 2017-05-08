#! python3

class Population: # definit une population de birds
	def __init__(self, n):
		self.birds = [Bird() for x in range(n)]
		self.survivors = n
		self.best = 0
		self.elitism = {'fitness':0, 'genome':None}

class Bird: # definit un oiseau
	def __init__(self):
		self.X = 100
		self.Y = 250
		self.object = background.create_image(self.X, self.Y, image=birdImg) # (x, y, source)
		self.alive = True
		self.fitness = 0
		self.score = 0
		self.genome = genGenome()
		self.velocity = 0

	def reset(self):
		self.X = 100
		self.Y = 250
		background.coords(self.object, self.X, self.Y)
		self.alive = True
		self.fitness = 0
		self.score = 0
		self.velocity = 0

	def fly(self):
		self.velocity = -4.75

	def getBirdY(self): # hauteur de l'oiseau relative au pipeline
		return pipelineY + 125 - self.Y

	def getBirdX(self): # distance de l'oiseau relative au pipeline
		return pipelineX - self.X
