### Version 1.0 of animation.py for PKU 2018 CGT
### by Dan Garcia (ddgarcia@cs.berkeley.edu)

from tkinter import *
import random

master = Tk()
SLOT = 200 ## slot size (square on the board)
NUMSTEPS = 10 ## Number of steps, or "frames" per animation (fewer=faster)
STEP = SLOT/NUMSTEPS ## How much the piece moves every step
POSITION = 0 ## This would be the current position
ROWS = 3
COLS = 4

WIN = "win"
LOSE = "lose"
TIE = "tie"
DRAW = "draw"
VALUE_TO_COLOR = {WIN:"darkgreen", LOSE:"darkred", TIE:"yellow", DRAW:"yellow"}

c = Canvas(master, width=COLS*SLOT, height=ROWS*SLOT)
c.pack()

def GetColor(position):
	"""Here, you would display the color based on the value from your database"""
	value = random.choice([WIN, LOSE, TIE, DRAW]) ## your DB query
	return VALUE_TO_COLOR[value]

def GetRemotenessViz(position):
	"""Here, you would display the remoteness based on your database.
	We categorize remoteness into four categories, best move, 2nd, 3rd, 4th best.
	Best remoteness would be "" (solid line)
	2nd best remoteness would be "20 5" (almost solid), etc."""
	solid = str(SLOT//10)+" "
	dash1 = str(SLOT//10-1*SLOT//40)
	dash2 = str(SLOT//10-2*SLOT//40)
	dash3 = str(SLOT//10-3*SLOT//40)
	return random.choice(["", solid+dash1, solid+dash2, solid+dash3])

def MakeAnimateHandler(fr,to,frsignx,frsigny):
	def AnimateHandler(someevent):
		c.itemconfig(fr, state="hidden")
		def Animate(dx,dy,n):
			c.move(b,dx,dy)
			if n > 1:
				c.after(1,Animate,dx,dy,n-1)
			else:
				c.itemconfig(to, state="normal")
		Animate(STEP*frsignx,STEP*frsigny,NUMSTEPS)
	return AnimateHandler

def CreateArrows():
	arrowwidth = 0.25 * (0.4 * SLOT)
	arrowshape = str(2*arrowwidth)+" "+str(2*arrowwidth)+" "+str(arrowwidth)
	for fri in range(ROWS*COLS):
		for toi in range(ROWS*COLS):
			frrow, frcol, torow, tocol = fri // COLS, fri % COLS, toi // COLS, toi % COLS
			if fri == toi or abs(frrow-torow) > 1 or abs(frcol-tocol) > 1:
				pass
			else:
				a = c.create_line(SLOT/2+frcol*SLOT,SLOT/2+frrow*SLOT,SLOT/2+tocol*SLOT,SLOT/2+torow*SLOT, width=arrowwidth, fill=GetColor(POSITION), dash=GetRemotenessViz(POSITION), activefill="black", arrowshape=arrowshape, arrow="last", state="hidden", tags=("arrow"+str(fri)))
				c.tag_bind(a, sequence="<Button-1>",func=MakeAnimateHandler("arrow"+str(fri),"arrow"+str(toi),tocol-frcol,torow-frrow))

def CreateBoard():
	"""Create the ROWS * COLS rectangles that make up the board"""
	for col in range(COLS):
		for row in range(ROWS):
			c.create_rectangle(col*SLOT, row*SLOT, (col+1)*SLOT, (row+1)*SLOT, fill="grey")

CreateBoard()	
CreateArrows() ## These all start hidden
c.tag_raise("piece") ## Put the piece above the arrows
c.itemconfig("arrow0", state="normal") ## Raise the NW arrows to start
b = c.create_oval(15, 15, SLOT-15, SLOT-15, fill="blue", outline="blue", tags=("piece"))

mainloop()

