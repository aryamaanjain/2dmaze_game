from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import floor
from random import randint


class Enemy:
	"""docstring for Enemy"""


	def __init__(self, world):
		self.x = world.cols * world.w - 2 * world.w
		self.y = world.rows * world.w - 2 * world.w
		self.speed = 0.04
		self.size = world.w / 4


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		# glColor3f(1.0, 0.0, 0.0)
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (1.0, 0.0, 0.0, 1.0)
		mspecular = (0.2, 0.2, 0.2, 1.0)
		mshininess = 10.0

		glMaterialfv(GL_FRONT, GL_AMBIENT, mambient)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mdiffuse)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mspecular)
		glMaterialfv(GL_FRONT, GL_SHININESS, mshininess)

		glBegin(GL_QUADS)
		glNormal3f(0.0, 0.0, 1.0)
		glVertex3f(x  , y  , 0.0)
		glVertex3f(x+s, y  , 0.0)
		glVertex3f(x+s, y+s, 0.0)
		glVertex3f(x  , y+s, 0.0)
		glEnd()

		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.0, 0.0, 0.0, 1.0)
		mspecular = (0.0, 0.0, 0.0, 1.0)
		mshininess = 10.0

		glMaterialfv(GL_FRONT, GL_AMBIENT, mambient)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mdiffuse)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mspecular)
		glMaterialfv(GL_FRONT, GL_SHININESS, mshininess)

		glBegin(GL_QUADS)
		glNormal3f(0.0, 0.0, 1.0)
		# left eye
		glVertex3f(x+s*2/10, y+s*7/10, 0.001)
		glVertex3f(x+s*3/10, y+s*7/10, 0.001)
		glVertex3f(x+s*3/10, y+s*8/10, 0.001)
		glVertex3f(x+s*2/10, y+s*8/10, 0.001)
		# right eye
		glVertex3f(x+s*7/10, y+s*7/10, 0.001)
		glVertex3f(x+s*8/10, y+s*7/10, 0.001)
		glVertex3f(x+s*8/10, y+s*8/10, 0.001)
		glVertex3f(x+s*7/10, y+s*8/10, 0.001)
		# nose
		glVertex3f(x+s*9/20, y+s*9/20, 0.001)
		glVertex3f(x+s*11/20, y+s*9/20, 0.001)
		glVertex3f(x+s*11/20, y+s*11/20, 0.001)
		glVertex3f(x+s*9/20, y+s*11/20, 0.001)
		# mouth
		glVertex3f(x+s*2/10, y+s*2/10, 0.001)
		glVertex3f(x+s*8/10, y+s*2/10, 0.001)
		glVertex3f(x+s*8/10, y+s*3/10, 0.001)
		glVertex3f(x+s*2/10, y+s*3/10, 0.001)
		
		glEnd()
		# glColor3f(1.0, 1.0, 1.0)


	def updatePosition(self, player, world):
		"""moves with some intelligence towards player"""
		r = randint(0, 3) 

		# random direction to not get stuck
		if r == 0:
			self.moveLeft(world)
			self.moveLeft(world)
		elif r == 1:
			self.moveRight(world)
			self.moveRight(world)
		elif r == 2:
			self.moveUp(world)
			self.moveUp(world)
		else:
			self.moveDown(world)
			self.moveDown(world)

		# towards player to go towards him incrementally
		erow = floor(self.y / world.w)
		ecol = floor(self.x / world.w)
		ecell = world.grid[world.index(erow, ecol)]
		
		if player.x - self.x < 0 and ecell.walls[3] == False:
			self.moveLeft(world)
		elif player.x - self.x > 0 and ecell.walls[1] == False:
			self.moveRight(world)
		
		if player.y - self.y < 0 and ecell.walls[0] == False:
			self.moveDown(world)
		elif player.y - self.y > 0 and ecell.walls[2] == False:
			self.moveUp(world)
		

	def checkCollision(self, p, scoreboard):
		x = self.x
		y = self.y
		s = self.size

		collision = False

		if p.x < x < p.x + p.size and p.y < y < p.y + p.size:
			# then first vertex in collision zone
			collision = True
		elif p.x < x+s < p.x + p.size and p.y < y < p.y + p.size:
			collision = True
		elif p.x < x+s < p.x + p.size and p.y < y+s < p.y + p.size:
			collision = True
		elif p.x < x < p.x + p.size and p.y < y+s < p.y + p.size:
			collision = True
		
		if collision:
			scoreboard.health = 0


	def moveLeft(self, w):
		if not self.checkWallCollision(w, self.x-self.speed, self.y):
			self.x -= self.speed


	def moveRight(self, w):
		if not self.checkWallCollision(w, self.x+self.speed, self.y):
			self.x += self.speed


	def moveUp(self, w):
		if not self.checkWallCollision(w, self.x, self.y+self.speed):
			self.y += self.speed
	

	def moveDown(self, w):
		if not self.checkWallCollision(w, self.x, self.y-self.speed):
			self.y -= self.speed


	def checkWallCollision(self, world, x, y):
		"""returns true if colliding with any wall, else false"""
		s = self.size
		w = world.w

		# cell where bottom-left vertex lies
		vblx = floor(x / w)
		vbly = floor(y / w)
		# cell where bottom-right vertex lies
		vbrx = floor((x+s) / w)
		vbry = floor(y / w)
		# cell where top-left vertex lies
		vtlx = floor(x / w)
		vtly = floor((y+s) / w)
		# cell where top-right vertex lies
		vtrx = floor((x+s) / w)
		vtry = floor((y+s) / w)

		# compare vbl and vbr
		# if they are in diffent cells then check whether there is a wall between them
		# None check is for when player goes out of the world 
		if vblx - vbrx != 0:
			index = world.index(vbly, vblx)
			if index is None:
				return True
			cell = world.grid[index]
			if cell.walls[1] == True:
				return True

		if vbly - vtly != 0:
			index = world.index(vbly, vblx)
			if index is None:
				return True
			cell = world.grid[index]
			if cell.walls[2] == True:
				return True
		
		if vbry - vtry != 0:
			index = world.index(vbry, vbrx)
			if index is None:
				return True
			cell = world.grid[index]
			if cell.walls[2] == True:
				return True

		if vtlx - vtrx != 0:
			index = world.index(vtly, vtlx)
			if index is None:
				return True
			cell = world.grid[index]
			if cell.walls[1] == True:
				return True

		return False


