#! python3

# import de librairies
import tkinter
import random
import json, base64, codecs
import time
import gen
import ia

# initialisation
window = tkinter.Tk()
window.resizable(width = False, height = False)
window.title("Flappy Bird")
window.geometry("500x500")

background = tkinter.Canvas(window, width = 500, height = 500, background = "#4CC", bd=0, highlightthickness=0)
background.pack()

birdImg = tkinter.PhotoImage(file="img/bird5.png")

POP = 5 # min = 3, max = undefined

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
		self.flyToggle = 0
		self.alive = True
		self.fitness = 0
		self.score = 0
		self.genome = gen.genGenome()

	def reset(self):
		self.X = 100
		self.Y = 250
		background.coords(self.object, self.X, self.Y)
		self.flyToggle = 0
		self.alive = True
		self.fitness = 0
		self.score = 0

	def fly(self):
		self.flyToggle = 15

	def getBirdY(self): # hauteur de l'oiseau relative au pipeline
		return pipelineY + 125 - self.Y

	def getBirdX(self): # distance de l'oiseau relative au pipeline
		return pipelineX - self.X

population = Population(POP)

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + 125, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

scoreText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # texte score actuel

try:
	with open('stats.json', 'r') as f:
		temp = f.read()
		temp = codecs.decode(base64.b85decode(codecs.encode(temp)))
		temp = json.loads(temp)
		bS, nG = temp['bestScore'], temp['numberGames']
except:
	bS, nG = 0, 1

# fonctions
def restart(event):
	global population
	global pipelineX, pipelineY
	global bS, nG
	pipelineX = 500
	pipelineY = 150
	for bird in population.birds: # reforme la population
		if (bird.fitness >= population.elitism['fitness']): # enregistre le meilleur genome
			population.elitism[1] = bird.genome
		bird.reset() # reset
		if (random.randint(0, 1) == 1): # mutations, aleatoires
			bird.genome = bird.genome.mutate()
		'''if (random.randint(0, 2) == 2): # crossover, reproductions
			bird.genome = gen.Genome(bird.genome.hauteurNode, bird.genome.distanceNode).crossover(population.elitism['genome'])'''
	if (population.elitism['genome'] != None):
		population.birds[-1].genome = population.elitism['genome']
	population.survivors = POP
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	with open('stats.json', 'w+') as f: # write to stats.json
		temp = json.dumps({'bestScore':bS, 'numberGames':nG})
		temp = codecs.decode(base64.b85encode(codecs.encode(temp)))
		f.write(temp)
	nG += 1 # incremente le nombre de parties
	background.itemconfig(scoreText, text="0")
	motion()

def motion(): # fonction principale
	global pipelineX, pipelineY
	global population
	print([bird.fitness for bird in population.birds])
	if (population.survivors <= 0):
		restart(0)
		return False
	for bird in population.birds:
		if (bird.alive == True):
			if (bird.Y < 470 and bird.flyToggle <= 0): # effet de gravite
				bird.Y += 4
				background.coords(bird.object, 100, bird.Y)
			if (bird.Y > 30 and bird.flyToggle > 0): # vole
				bird.Y -= 4.5 # 4.5 * 15 = 67.5
				bird.flyToggle -= 1
				background.coords(bird.object, 100, bird.Y)
			if (bird.X < pipelineX and (bird.X + 9) >= pipelineX): # incremente le score
				bird.score += 1
				background.itemconfig(scoreText, text=bird.score)
			if ((bird.X + 21) >= pipelineX and bird.X <= (pipelineX + 70)): # collisions
				if ((bird.Y - 17) <= pipelineY or (bird.Y + 17) >= (pipelineY + 100)):
					bird.alive = False
					population.survivors -= 1
			bird.fitness += 1
			if (bird.getBirdY() < bird.genome.gethauteurnode() and bird.getBirdX() > bird.genome.getdistancenode()): # IA
				bird.fly()
		else: # bird stick to pipeline when dead
			bird.X -= 5
			background.coords(bird.object, bird.X, bird.Y)
	if (pipelineX < -100): # pipelines
		pipelineX = 500
		pipelineY = random.randint(max(pipelineY - 160, 0), min(pipelineY + 160, 350)) # (0, 350) avant, maintenant cas impossibles bannis
	else:
		pipelineX -= 5
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	window.after(20, motion) # boucle infinie, 100 images par secondes

# run
motion()
window.mainloop()
