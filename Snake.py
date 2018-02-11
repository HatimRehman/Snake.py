from Tkinter import *
import copy
import random

INT_GRID_SIZE = 500
GRID_SIZE = str(INT_GRID_SIZE) + "x" + str(INT_GRID_SIZE)
ROW_SIZE = COLUMN_SIZE = 25

class Snake(object):

	HORIZONTAL_KEY_IMPACT = { 	"Up": -1,
					"Down": 1,
					"Right": 0,
					"Left": 0
	}
	VERTICAL_KEY_IMPACT = { 	"Up": 0,
					"Down": 0,
					"Right": 1,
					"Left": -1
	}

	direction = ["Right", "Left", "Up", "Down"][random.randint(0,3)]

	fruit = {"row": None, "column": None }

	snake = [ {"row": 0 , "column": 0} ]

	def __init__(self):

		self.master = Tk()
		self.master.geometry(GRID_SIZE)
		self.master.bind( '<Key>', self.key_was_pressed )
		self.master.title("Snake by Hatim. 0")
		self.generate_fruit()
		self.refresher()
		self.master.mainloop()

	def collision(self, head):

		return head in self.snake

	def ate_fruit(self, head):

		return head == self.fruit

	def move(self, row, column):

		Frame(self.master, width=INT_GRID_SIZE/ROW_SIZE, height=INT_GRID_SIZE/COLUMN_SIZE, background="Black").grid(row=row, column=column)

	def remove(self, row, column):

		Frame(self.master, width=INT_GRID_SIZE/ROW_SIZE, height=INT_GRID_SIZE/COLUMN_SIZE).grid(row=row, column=column)

	def generate_fruit(self):

		old_fruit = self.fruit.copy()	#used to ensure not in same place as before
		self.fruit = {"row": random.randint(0, ROW_SIZE-1), "column": random.randint(0, COLUMN_SIZE-1)}

		while self.fruit in self.snake or self.fruit == old_fruit:
			self.fruit = {"row": random.randint(0, ROW_SIZE-1), "column": random.randint(0, COLUMN_SIZE-1)}

		Frame(self.master, width=INT_GRID_SIZE/ROW_SIZE, height=INT_GRID_SIZE/COLUMN_SIZE, background="Red").grid(row = self.fruit["row"], column= self.fruit["column"])

	def key_was_pressed(self, event):

		if self.direction in ["Right", "Left"] and event.keysym in ["Right", "Left"]:
			return
		if self.direction in ["Up", "Down"] and event.keysym in ["Up", "Down"]:
			return

		self.direction = event.keysym

	def animate(self):

		head = self.snake[0].copy() # get head object BY VALUE

		# calculate where head moves based on current direction
		head["row"] = ( head["row"] + Snake.HORIZONTAL_KEY_IMPACT[self.direction] ) % ROW_SIZE
		head["column"] = ( head["column"] + Snake.VERTICAL_KEY_IMPACT[self.direction]) % COLUMN_SIZE

		if self.collision(head):
			self.master.event_generate("<Return>")
		elif self.ate_fruit(head):	# if new head position corresponds to eating fruit, dont remove tail (+1 size)
			self.generate_fruit()
			self.master.title("Snake by Hatim. " + str(len( self.snake )))
		else:						# move tail up by one
			tail = self.snake.pop()
			self.remove( tail["row"], tail["column"] )

		#insert position of head and move on screen
		self.snake.insert( 0, head )
		self.move( head["row"], head["column"] )

	def refresher(self):
		self.animate()
		self.master.after(50, self.refresher)

_ = Snake()
