import random

<<<<<<< HEAD
global POPULATION # nombre d'individu en test a la fois
global HAUTEUR_MIN
global HAUTEUR_MAX
global DISTANCE_MIN
global DISTANCE_MAX
global g0, g1, g2, g3, g4, g5, g6, g7, g8, g9


=======
>>>>>>> fb78a3fe1dda2ef8e80b463d77ff34262b691dae
TAUX_MUTATION = 0.1
POPULATION = 10
HAUTEUR_MIN = 0
HAUTEUR_MAX = 500
DISTANCE_MIN = 0
DISTANCE_MAX = 300


class Genome:
	def __init__(self, h, d):
<<<<<<< HEAD
		self.hauteur = h
		self.distance = d
		self.score = 0

	def setdistance(self, d): # definit la node distance
		self.distance = d

	def sethauteur(self, h): # definit la node hauteur
		self.hauteur = h

	def setscore(self, score): # definit le score
=======
		self.nodeHauteur = h
		self.nodeDistance = d
		self.distanceActu = 0 # distance actuelle de l'oiseau sur le plan du jeu
		self.hauteurActu = 0 # hauteur actuelle de l'oiseau sur le plan du jeu
		self.score = 0 # Score maximum du génome

	def setdistancenode(self, d): # definit la node distance
		self.distanceNode = d

	def sethauteurnode(self, h): # definit la node hauteur
		self.hauteurNode = h

	def setscore(self, score): # definit le score 
>>>>>>> fb78a3fe1dda2ef8e80b463d77ff34262b691dae
		self.score = score

	def mutation(self): # Retourne le genome mute
		return Genome(self.h+random.uniform(HAUTEUR_MIN*TAUX_MUTATION, HAUTEUR_MAX*TAUX_MUTATION),\
		 self.d+random.uniform(DISTANCE_MIN*TAUX_MUTATION, DISTANCE_MAX*TAUX_MUTATION))

<<<<<<< HEAD
	def getdistance(self): # Retourne la distance
		return self.distance

	def gethauteur(self): # Retourne la distance
		return self.hauteur

=======
	def getdistancenode(self): # Retourne la distance
		return self.distance

	def gethauteurnode(self): # Retourne la distance
		return self.hauteur

	def getdistanceactu(self, d): # Retourne la distance actuelle
		self.distanceActu = d

	def gethauteuractu(self, h): # Retourne la node hauteur actuelle
		self.hauteurActu = h

>>>>>>> fb78a3fe1dda2ef8e80b463d77ff34262b691dae
	def showinfo(self): # Afficher des informations sur le genome
		print("Hauteur : ", self.hauteur, "\nDistance : ", self.distance, "\nScore :", self.score)


def randomHauteur(): # Donne une hauteur aleatoire
	return random.uniform(HAUTEUR_MIN, HAUTEUR_MAX);

def randomDistance(): # Donne une distance aleatoire
	return random.uniform(DISTANCE_MIN, DISTANCE_MAX);
<<<<<<< HEAD


=======
	

# Generation d'un genome
>>>>>>> fb78a3fe1dda2ef8e80b463d77ff34262b691dae
def genGenome(bestG = 0):
	if bestG == 0:
		return Genome(randomHauteur(), randomDistance())
	else:
<<<<<<< HEAD
		return bestG.mutation()
=======
		return bestG.mutation()
>>>>>>> fb78a3fe1dda2ef8e80b463d77ff34262b691dae