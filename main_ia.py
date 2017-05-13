#! python3

# import de librairies
from libs.gen import * # import de la librarie personnelle d'un sous dossier avec libs. ET un fichier __init__.py blanc dedans
from tkinter import * # GUI
import random # fonctions aleatoires
import json, base64, codecs # pour les stats
import time

# initialisation
window = Tk()
window.resizable(width = False, height = False)
window.title("Flappy Bird")
window.iconbitmap("img/adn.ico")
window.geometry("500x500")

# constantes et variables
FPS = IntVar()
FPS.set(50) # images par secondes
POP = IntVar()
POP.set(10) # nombres d'oiseaux par population
POP_NUM = 1 # numero de la population
HOLE = 90 # taille en pixels en les deux pipes

background = Canvas(window, width = 500, height = 500, background = "#4CC", bd=0, highlightthickness=0)
background.pack()

birdImg = PhotoImage(file="img/bird.png")
birdImgBig = PhotoImage(file="img/bird-big.png")

class Population: # definit une population de birds
	def __init__(self, n):
		self.birds = [Bird() for x in range(n)]
		self.survivors = n
		self.best = 0
		self.elitism = {'fitness':0, 'genome':None}

class Bird: # definit un oiseau
	def __init__(self):
		self.X = 100 # coordonnees de depart de l'oiseau
		self.Y = 250
		self.genome = genGenome()
		if (self.genome.size < 1.5):
			self.object = background.create_image(self.X, self.Y, image=birdImg) # (x, y, source)
			self.sizeMultiplier = 1
		else:
			self.object = background.create_image(self.X, self.Y, image=birdImgBig) # (x, y, source)
			self.sizeMultiplier = 1.5
		self.alive = True
		self.fitness = 0 # habilite / score plus precis
		self.score = 0
		self.velocity = 0 # vitesse

	def reset(self): # remet a zero les coordonnees
		self.X = 100
		self.Y = 250
		if (self.genome.size < 1.5):
			background.itemconfig(self.object, image=birdImg)
			self.sizeMultiplier = 1
		else:
			background.itemconfig(self.object, image=birdImgBig)
			self.sizeMultiplier = 1.42
		background.coords(self.object, self.X, self.Y)
		self.alive = True
		self.fitness = 0
		self.score = 0
		self.velocity = 0

	def fly(self): # etablit une vitesse forte negative (vers le haut)
		self.velocity = -4.75

	def getBirdY(self): # hauteur de l'oiseau relative au pipeline
		return pipelineY + 125 - self.Y

	def getBirdX(self): # distance de l'oiseau relative au pipeline
		return pipelineX - self.X

population = Population(POP.get()) # designe une population de POP oiseaux (int)
endMarker = time.time() # pour le debug / stats
result = '' # stats

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + HOLE, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

scoreText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # texte score actuel
popText = background.create_text(60, 485, fill="white", font="Times 12 bold", text="Population n° 1") # texte population actuelle

# fonctions
def restart(event):
	global population, POP_NUM
	global pipelineX, pipelineY
	POP_NUM += 1

	background.itemconfig(popText, text="Population n° {}".format(POP_NUM)) # Affiche le nombre de pop qui ont vecu
	pipelineX = 500
	pipelineY = 150
	updateResult()
	for bird in population.birds: # reforme la population
		if (bird.fitness >= population.elitism['fitness']): # enregistre le meilleur genome (elitism)
			population.elitism['fitness'] = bird.fitness
			population.elitism['genome'] = bird.genome
		if (population.elitism['fitness'] < 100): # si le meilleur n'est pas si bon que ca
			bird.genome = genGenome()
		else:
			bird.genome = bird.genome.mutate()
			bird.genome = Genome(bird.genome.hauteurNode, bird.genome.size).crossover(population.elitism['genome'])
		bird.reset() # reset (coordonnees)
	if (population.elitism['genome'] != None):
		population.birds[0].genome = population.elitism['genome'] # selection sure (sans mutation) pour eviter une mauvaise evolution
		population.birds[1].genome = population.elitism['genome'].mutate() # selection sure avec mutation pour assurer une evolution quelconque

	population.survivors = POP.get()
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + HOLE, pipelineX + 70, 500)
	background.itemconfig(scoreText, text="0")
	motion()

def updateResult(): # fonction servant a formater les donnees qu'on va ensuite ecrire dans un fichier texte (pour des stats uniquement)
	global result
	temp = {'soluces':[], 'fitness':[]}
	for bird in population.birds:
		temp['soluces'].append(str(int(bird.genome.hauteurNode)))
		temp['fitness'].append(str(bird.fitness))
	result += '\t'.join(temp['soluces']) + '\n' +  '\t'.join(temp['fitness']) + '\n%s' % (time.time()-endMarker) + '\n==========\n'

def motion(): # fonction principale
	global pipelineX, pipelineY, population
	print([bird.fitness for bird in population.birds], population.best, population.elitism['fitness']) # affichage fitness

	if (population.survivors <= 0): # s'il n'y a pas de survivants, redemarrage
		restart(0)
		return False

	for bird in population.birds: # boucle dans tous les oiseaux
		if (bird.alive == True):
			bird.Y += bird.velocity # augmente la hauteur par la valeur vitesse
			bird.velocity += 0.25 # gravite (augmente la vitesse)
			background.coords(bird.object, 100, bird.Y)

			if (bird.X < pipelineX and (bird.X + 9) >= pipelineX): # incremente le score
				bird.score += 1
				background.itemconfig(scoreText, text=bird.score)

			if ((bird.X + (21*bird.sizeMultiplier)) >= pipelineX and bird.X <= (pipelineX + 70)): # collisions : l'oiseau est mort
				if ((bird.Y - (17*bird.sizeMultiplier)) <= pipelineY or (bird.Y + (17*bird.sizeMultiplier)) >= (pipelineY + HOLE)):
					bird.alive = False
					population.survivors -= 1

			bird.fitness += 1

			if (bird.getBirdY() < bird.genome.hauteurNode): # IA : si l'oiseau est en dessous de son node, il saute
				bird.fly()

		else: # l'oiseau reste sur le pipe à sa mort (il perds aussi vite que les pipes en X)
			bird.X -= 5
			background.coords(bird.object, bird.X, bird.Y)

	if (pipelineX < -100): # pipelines
		pipelineX = 500
		pipelineY = random.randint(0, 350) # max(pipelineY - 160, 0), min(pipelineY + 160, 350) pour bannir tous cas impossibles

	else:
		pipelineX -= 5

	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + HOLE, pipelineX + 70, 500)
	if (time.time() - endMarker > 180): # pour ecrire des resultats statistiques
		with open('data/result.txt', 'w') as f:
			updateResult()
			f.write(result)
		return False
	window.after(int(1000/FPS.get()), motion) # boucle infinie, 1000/x img par secondes (ex: 1000/50, 1000/150 1000/500)

# Fenetre de controle
controls = Toplevel()

controls.resizable(width = False, height = False)
controls.title("Flappy Bird - Controles")
controls.geometry("200x350")
controls.attributes("-toolwindow", 1)	# Enlever le bouton pour redimensionner la fenetre

label1 = Label(controls, text="Vitesse : ", cursor='pirate')
vitesseScale = Scale(controls, orient=HORIZONTAL, from_=1, to=1000, length=180, variable=FPS , cursor='sb_h_double_arrow') # Curseur pour modifier les FPS

label2 = Label(controls, text="Nombre d'oiseau par population : ")
popScale = Scale(controls, orient=HORIZONTAL, from_=1, to=200, length=180, variable=POP, cursor='sb_h_double_arrow') # Curseur pour modifier le nombre d'oiseaux

label1.pack()
vitesseScale.pack()
label2.pack()
popScale.pack()

# run
motion()
window.mainloop()
