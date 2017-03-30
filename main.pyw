#! python3

# import de librairies
import tkinter
import random
import json, base64, codecs
import time
import gen

# initialisation
window = tkinter.Tk()
window.resizable(width = False, height = False)
window.title("Flappy Bird")
window.geometry("500x500")

background = tkinter.Canvas(window, width = 500, height = 500, background = "#4CC", bd=0, highlightthickness=0)
background.pack()

birdImg = tkinter.PhotoImage(file="img/bird5.png")
birdX = 100
birdY = 250
bird = background.create_image(birdX, birdY, image=birdImg) # (x, y, source)
flyToggle = 0

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + 100, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

try:
	with open('stats.json', 'r') as f:
		temp = f.read()
		temp = codecs.decode(base64.b85decode(codecs.encode(temp)))
		temp = json.loads(temp)
		iS, bS, nG = 0, temp['bestScore'], temp['numberGames']
except:
	iS, bS, nG = 0, 0, 1

def getBirdY():
	return birdY-(pipelineY+100)

def getBirdX():
	return pipelineX-birdX

iSText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # texte score actuel
bSText = background.create_text(50, 410, fill="white", font="Times 15 bold", text="best: " + str(bS)) # meilleur score
nGText = background.create_text(50, 430, fill="white", font="Times 15 bold", text="n: " + str(nG)) # nombre de parties
heightText = background.create_text(50, 450, fill="white", font="Times 15 bold", text="h: " + str(getBirdY())) # hauteur de l'oiseau relative au pipeline
distanceText = background.create_text(50, 470, fill="white", font="Times 15 bold", text="d: " + str(getBirdX())) # distance de l'oiseau relative au pipeline

# fonctions
def restart(event):
	global birdX, birdY
	global pipelineX, pipelineY
	global iS, bS, nG
	birdX = 100
	birdY = 250
	pipelineX = 500
	pipelineY = 150
	background.coords(bird, 100, birdY)
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	motion()
	if (bS < iS): # update best score
		bS = iS
	with open('stats.json', 'w+') as f: # write to stats.json
		temp = json.dumps({'bestScore':bS, 'numberGames':nG})
		temp = codecs.decode(base64.b85encode(codecs.encode(temp)))
		f.write(temp)
	print('Reboot: %i\nScore: %i\nbest: %i\n' % (nG, iS, bS))
	nG += 1 # incremente le nombre de parties
	background.itemconfig(nGText, text="n: " + str(nG))
	iS = 0 # reset instant score
	background.itemconfig(iSText, text=iS)

def motion(): # fonction principale
	global birdY, flyToggle
	global pipelineX, pipelineY
	global iS
	if (birdY < 470 and flyToggle <= 0): # effet de gravite
		birdY += 4
		background.coords(bird, 100, birdY)
		background.itemconfig(bSText, text="best: " + str(bS))
		background.itemconfig(heightText, text="h: " + str(getBirdY()))
	if (birdY > 30 and flyToggle > 0): # vole
		birdY -= 4
		flyToggle -= 1
		background.coords(bird, 100, birdY)
		background.itemconfig(bSText, text="best: " + str(bS))
		background.itemconfig(heightText, text="h: " + str(getBirdY()))
	if (pipelineX < -100): # pipelines
		pipelineX = 500
		pipelineY = random.randint(max(pipelineY - 160, 0), min(pipelineY + 160, 350)) # (0, 350) avant, maintenant cas impossibles bannis
	else:
		pipelineX -= 5
	if (birdX < pipelineX and (birdX + 9) >= pipelineX): # incremente le score
		iS += 1
		background.itemconfig(iSText, text=iS)
	if ((birdX + 21) >= pipelineX and birdX <= (pipelineX + 70)): # collisions
		if ((birdY - 17) <= pipelineY or (birdY + 17) >= (pipelineY + 100)):
			restart(0)
			return False
	background.itemconfig(distanceText, text="d: " + str(getBirdX()))
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	window.after(10, motion) # boucle infinie, 100 images par secondes

def fly(event): # active l'action de voler
	global flyToggle
	flyToggle = 10

# run
window.after(10, motion)
window.bind("<space>", fly)
window.mainloop()
