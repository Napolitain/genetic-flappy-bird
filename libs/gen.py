#! python3

import random

TAUX_MUTATION = 0.1
HAUTEUR_MIN = -500
HAUTEUR_MAX = 500

class Genome:
	def __init__(self, h, s):
		self.hauteurNode = h
		self.size = s

	def mutate(self): # Retourne le genome mute
		return Genome(self.hauteurNode + random.uniform(-30*TAUX_MUTATION, 30*TAUX_MUTATION), self.size)

	def crossover(self, other): # retourne le genome retrouve par association avec un autre
		return Genome((self.hauteurNode + other.hauteurNode)/2, (self.size + other.size)/2)

	def showinfo(self): # Afficher des informations sur le genome
		print("hauteurNode : ", self.hauteurNode,\
		 "\nHauteur actuelle : ", self.hauteurActu,\
		  "\nScore :", self.score)

def randomHauteur(): # Donne une hauteur aleatoire
	return random.uniform(HAUTEUR_MIN, HAUTEUR_MAX)

def randomSize():
	return random.uniform(1, 2)

# Generation d'un genome
def genGenome():
	return Genome(randomHauteur(), randomSize())
