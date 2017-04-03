#! python3

import random

TAUX_MUTATION = 0.1
HAUTEUR_MIN = 0
HAUTEUR_MAX = 500
DISTANCE_MIN = 0
DISTANCE_MAX = 300

class Genome:
	def __init__(self, h, d):
		self.hauteurNode = h
		self.distanceNode = d
		self.distanceActu = 0 # distance actuelle de l'oiseau sur le plan du jeu
		self.hauteurActu = 0 # hauteur actuelle de l'oiseau sur le plan du jeu
		self.score = 0 # Score maximum du genome

	def setdistancenode(self, d): # definit la node distance
		self.distanceNode = d

	def sethauteurnode(self, h): # definit la node hauteur
		self.hauteurNode = h

	def setdistanceactu(self, d): # definit la node distance
		self.distanceActu = d

	def sethauteuractu(self, h): # definit la node hauteur
		self.hauteurActu = h

	def setscore(self, score): # definit le score
		self.score = score

	def mutate(self): # Retourne le genome mute
		return Genome(self.hauteurNode+random.uniform(HAUTEUR_MIN*TAUX_MUTATION, HAUTEUR_MAX*TAUX_MUTATION),\
		 self.distanceNode+random.uniform(DISTANCE_MIN*TAUX_MUTATION, DISTANCE_MAX*TAUX_MUTATION))

	def crossover(self, other): # retourne le genome retrouve par association avec un autre
		return Genome((self.h+other.h)/2, (self.d+other.d)/2)

	def getdistancenode(self): # Retourne la distance
		return self.distanceNode

	def gethauteurnode(self): # Retourne la distance
		return self.hauteurNode

	def getdistanceactu(self): # Retourne la distance actuelle
		return self.distanceActu

	def gethauteuractu(self): # Retourne la node hauteur actuelle
		return self.hauteurActu

	def showinfo(self): # Afficher des informations sur le genome
		print("hauteurNode : ", self.hauteurNode,\
		 "\ndistanceNode : ", self.distanceNode,\
		 "\nHauteur actuelle : ", self.hauteurActu, \
		 "\nDistance actuelle : ", self.distanceActu, \
		  "\nScore :", self.score)

def randomHauteur(): # Donne une hauteur aleatoire
	return random.uniform(HAUTEUR_MIN, HAUTEUR_MAX);

def randomDistance(): # Donne une distance aleatoire
	return random.uniform(DISTANCE_MIN, DISTANCE_MAX);

# Generation d'un genome
def genGenome(bestG = 0):
	if (bestG == 0):
		return Genome(randomHauteur(), randomDistance())
	else:
		return bestG.mutate()
