#! python3

# imports
import tkinter
import random
import json, base64, codecs

# initialisation
window = tkinter.Tk()
window.resizable(width = False, height = False)
window.title("Flappy Bird")
window.geometry("500x500")

background = tkinter.Canvas(window, width = 500, height = 500, background = "#4CC", bd=0, highlightthickness=0)
background.pack()

birdImg = tkinter.PhotoImage(file="bird5.png")
birdX = 100
birdY = 250
bird = background.create_image(birdX, birdY, image=birdImg) # (x, y, source)
flyToggle = 0

pipelineX = 500
pipelineY = 150
pipelineTop = background.create_rectangle(pipelineX, 0, pipelineX + 70, pipelineY, fill="#7B2", outline="#7B2")
pipelineBottom = background.create_rectangle(pipelineX, pipelineY + 100, pipelineX + 70, 500, fill="#7B2", outline="#7B2")

iSText = background.create_text(230, 50, fill="white", font="Times 50 bold", text="0") # instant score text
byText = background.create_text(50, 430, fill="white", font="Times 15 bold", text="hb: " + str(birdY)) # bird y text
pyText = background.create_text(50, 450, fill="white", font="Times 15 bold", text="hp: " + str(pipelineY+100)) # pipeline y text
differenceText = background.create_text(50, 470, fill="white", font="Times 15 bold", text="h: " + str(birdY-(pipelineY+100))) # difference h

try:
	with open('stats.json', 'r') as f:
		temp = f.read()
		temp = codecs.decode(base64.b85decode(codecs.encode(temp)))
		temp = json.loads(temp)
		iS, bS, nG = 0, temp['bestScore'], temp['numberGames']
except:
	iS, bS, nG = 0, 0, 1

# functions
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
	print('Reboot: %i\nScore: %i\nBest: %i\n' % (nG, iS, bS))
	nG += 1 # incrémente le nombre de parties
	iS = 0 # reset instant score
	background.itemconfig(iSText, text=iS)

def motion():
	global birdY, flyToggle
	global pipelineX, pipelineY
	global iS
	if (birdY < 470 and flyToggle <= 0): # effet de gravité
		birdY += 4
		background.coords(bird, 100, birdY)
		background.itemconfig(byText, text="hb: " + str(birdY))
		background.itemconfig(differenceText, text="h: " + str(birdY-(pipelineY+100)))
	if (birdY > 30 and flyToggle > 0): # vole
		birdY -= 4
		flyToggle -= 1
		background.coords(bird, 100, birdY)
		background.itemconfig(byText, text="hb: " + str(birdY))
		background.itemconfig(differenceText, text="h: " + str(birdY-(pipelineY+100)))
	if (pipelineX < -100): # pipelines
		pipelineX = 500
		temp = [max(pipelineY - 160, 0), min(pipelineY + 160, 350)] # cas impossibles à régler
		pipelineY = random.randint(50, 350) # (0, 350)
		background.itemconfig(pyText, text="hp: " + str(pipelineY+100))
	else:
		pipelineX -= 5
	if (birdX < pipelineX and (birdX + 9) >= pipelineX): # incrémente le score
		iS += 1
		background.itemconfig(iSText, text=iS)
	if ((birdX + 21) >= pipelineX and birdX <= (pipelineX + 70)): # collisions
		if ((birdY - 17) <= pipelineY or (birdY + 17) >= (pipelineY + 100)):
			restart(0)
			return False
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
