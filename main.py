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
birdX = 100
birdY = 250
bird = background.create_image(birdX, birdY, image=birdImg) # (x, y, source)
flyToggle = 0
IA = True

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + 125, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

try:
	with open('stats.json', 'r') as f:
		temp = f.read()
		temp = codecs.decode(base64.b85decode(codecs.encode(temp)))
		temp = json.loads(temp)
		iS, bS, nG = 0, temp['bestScore'], temp['numberGames']
except:
	iS, bS, nG = 0, 0, 1

def getBirdY(): # hauteur de l'oiseau relative au pipeline
	return pipelineY+125 - birdY

def getBirdX(): # distance de l'oiseau relative au pipeline
	return pipelineX-birdX

iSText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # texte score actuel

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
	nG += 1 # incremente le nombre de parties
	iS = 0 # reset instant score
	background.itemconfig(iSText, text=iS)

def motion(): # fonction principale
	global birdY, flyToggle
	global pipelineX, pipelineY
	global iS
	print(getBirdY())
	if (birdY < 470 and flyToggle <= 0): # effet de gravite
		birdY += 4
		background.coords(bird, 100, birdY)
	if (birdY > 30 and flyToggle > 0): # vole
		birdY -= 4.5 # 4.5 * 15 = 67.5
		flyToggle -= 1
		background.coords(bird, 100, birdY)
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
	background.coords(pipelineTop, pipelineX, 0, pipelineX + 70, pipelineY)
	background.coords(pipelineBottom, pipelineX, pipelineY + 100, pipelineX + 70, 500)
	if (IA != False): # avec ia
		if (ia.doIJump(getBirdY()) == True):
			fly(0)
		if int(getBirdX()) in range(int(g1.getdistancenode() - 10), int(g1.getdistancenode() + 10)):
			fly(0)
	window.after(20, motion) # boucle infinie, 100 images par secondes

def fly(event = 0): # active l'action de voler
	global flyToggle
	flyToggle = 15

# run
g1 = gen.genGenome()
window.after(10, motion)
window.bind("<space>", fly)
window.mainloop()
