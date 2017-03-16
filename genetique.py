import random

global POPULATION # nombre d'individu en test a la fois
global HAUTEUR_MIN
global HAUTEUR_MAX
global DISTANCE_MIN
global DISTANCE_MAX
global g0, g1, g2, g3, g4, g5, g6, g7, g8, g9


TAUX_MUTATION = 0.1
POPULATION = 10
HAUTEUR_MIN = 0
HAUTEUR_MAX = 500
DISTANCE_MIN = 0
DISTANCE_MAX = 300


class Genome:
	def __init__(self, h, d):
		self.hauteur = h
		self.distance = d
		self.score = 0

	def setdistance(self, d): # definit la node distance
		self.distance = d

	def sethauteur(self, h): # definit la node hauteur
		self.hauteur = h

	def setscore(self, score): # definit le score 
		self.score = score

	def mutation(self): # Retourne le genome mute
		return Genome(self.h+random.uniform(HAUTEUR_MIN*TAUX_MUTATION, HAUTEUR_MAX*TAUX_MUTATION), self.d+random.uniform(DISTANCE_MIN*TAUX_MUTATION, DISTANCE_MAX*TAUX_MUTATION))

	def getdistance(self): # Retourne la distance
		return self.distance

	def gethauteur(self): # Retourne la distance
		return self.hauteur	

	def showinfo(self): # Afficher des informations sur le genome
		print("Hauteur : ", self.hauteur, "\nDistance : ", self.distance, "\nScore :", self.score)


def randomHauteur(): # Donne une hauteur aleatoire
	return random.uniform(HAUTEUR_MIN, HAUTEUR_MAX);

def randomDistance(): # Donne une distance aleatoire
	return random.uniform(DISTANCE_MIN, DISTANCE_MAX);
	

def genGenome(bestG = 0):
	if bestG == 0:
		return Genome(randomHauteur(), randomDistance())
	else:
		return bestG.mutation()