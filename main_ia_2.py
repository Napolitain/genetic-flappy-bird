#! python3

# import de librairies
from gen import *
import tkinter # GUI
import random # fonctions aleatoires
import json, base64, codecs # pour les stats
import time

# initialisation
window = tkinter.Tk()
window.resizable(width = False, height = False)
window.title("Flappy Bird")
window.geometry("500x500")

background = tkinter.Canvas(window, width = 500, height = 500, background = "#4CC", bd=0, highlightthickness=0)
background.pack()
birdImg = tkinter.PhotoImage(file="img/bird5.png")

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

POP = 10 # min = 3, max = 50+ <=> Nombre d'oisea
population = Population(POP)
endMarker = time.time()
result = ''

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + 100, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

scoreText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # texte score actuel
popText = background.create_text(60, 485, fill="white", font="Times 12 bold", text="Population n° 1") # texte population actuelle

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
	global population, POP_NUM
	global pipelineX, pipelineY
	global bS, nG
	POP_NUM += 1
	background.itemconfig(popText, text="Population n° {}".format(POP_NUM)) # Affiche le nombre de pop qui ont vecu
	pipelineX = 500
	pipelineY = 150
	updateResult()
	for bird in population.birds: # reforme la population
		if (bird.fitness >= population.elitism['fitness']): # enregistre le meilleur genome (elitism)
			population.elitism['fitness'] = bird.fitness
			population.elitism['genome'] = bird.genome
		bird.reset() # reset
		if (random.randint(0, 1) == 0): # mutations legeres tous les 1/2
			bird.genome = bird.genome.mutate()
		if (random.randint(0, 1) == 0): # crossover tous les 1/2
			bird.genome = Genome(bird.genome.hauteurNode, bird.genome.distanceNode).crossover(population.elitism['genome'])
		if (random.randint(0, 2) == 0 and bird.fitness < population.elitism['fitness']): # mutations importantes tous les 1/4 (reset)
			bird.genome = genGenome()
	if (population.elitism['genome'] != None):
		population.birds[0].genome = population.elitism['genome'] # selection sure (sans mutation) pour eviter une mauvaise evolution
		population.birds[1].genome = population.elitism['genome'].mutate() # selection sure avec mutation pour assurer une evolution quelconque
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

def updateResult():
	global result
	temp = {'soluces':[], 'fitness':[]}
	for bird in population.birds:
		temp['soluces'].append(str(int(bird.genome.hauteurNode)))
		temp['fitness'].append(str(bird.fitness))
	result += '\t'.join(temp['soluces']) + '\n' +  '\t'.join(temp['fitness']) + '\n%s' % (time.time()-endMarker) + '\n==========\n'

def motion(): # fonction principale
	global pipelineX, pipelineY, population
	print([bird.fitness for bird in population.birds], population.best, population.elitism['fitness'])
	if (population.survivors <= 0):
		restart(0)
		return False
	for bird in population.birds:
		if (bird.alive == True):
			bird.Y += bird.velocity # update position
			bird.velocity += 0.25 # gravity
			background.coords(bird.object, 100, bird.Y)
			if (bird.X < pipelineX and (bird.X + 9) >= pipelineX): # incremente le score
				bird.score += 1
				background.itemconfig(scoreText, text=bird.score)
			if ((bird.X + 21) >= pipelineX and bird.X <= (pipelineX + 70)): # collisions
				if ((bird.Y - 17) <= pipelineY or (bird.Y + 17) >= (pipelineY + 100)):
					bird.alive = False
					population.survivors -= 1
			bird.fitness += 1
			if (bird.getBirdY() < bird.genome.gethauteurnode()): # IA
				bird.fly()
		else: # bird stick to pipeline when dead
			bird.X -= 5
			background.coords(bird.object, bird.X, bird.Y)
	if (pipelineX < -100): # pipelines
		pipelineX = 500
		pipelineY = random.randint(0, 350) # max(pipelineY - 160, 0), min(pipelineY + 160, 350) pour bannir tous cas impossibles
	else:
		pipelineX -= 5
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	if (time.time() - endMarker > 180): # pour ecrire des resultats statistiques
		with open('result.json', 'w') as f:
			updateResult()
			f.write(result)
		return False
	window.after(20, motion) # boucle infinie, 100 images par secondes

# run
motion()
window.mainloop()
