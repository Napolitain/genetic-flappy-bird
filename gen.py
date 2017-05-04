#! python3

import random

TAUX_MUTATION = 0.1
HAUTEUR_MIN = -500
HAUTEUR_MAX = 500

class Genome:
	def __init__(self, h):
		self.hauteurNode = h
		self.hauteurActu = 0 # hauteur actuelle de l'oiseau sur le plan du jeu
		self.score = 0 # Score maximum du genome

	def setscore(self, score): # definit le score
		self.score = score

	def mutate(self): # Retourne le genome mute
		return Genome(self.hauteurNode+random.uniform(10*TAUX_MUTATION, 30*TAUX_MUTATION))

	def crossover(self, other): # retourne le genome retrouve par association avec un autre
		return Genome((self.hauteurNode + other.hauteurNode)/2)

	def showinfo(self): # Afficher des informations sur le genome
		print("hauteurNode : ", self.hauteurNode,\
		 "\nHauteur actuelle : ", self.hauteurActu, \
		  "\nScore :", self.score)

def randomHauteur(): # Donne une hauteur aleatoire
	return random.uniform(HAUTEUR_MIN, HAUTEUR_MAX);

# Generation d'un genome
def genGenome(bestG = 0):
	if (bestG == 0):
		return Genome(randomHauteur())
	else:
		return bestG.mutate()
