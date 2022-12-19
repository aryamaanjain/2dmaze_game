from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import floor


class Player:
	"""docstring for Player"""
	

	def __init__(self, world):
		self.x = world.cols * world.w - world.w / 2
		self.y = world.rows * world.w - world.w / 2
		self.speed = 0.1
		self.size = world.w / 4


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		# glColor3f(0.0, 1.0, 0.0)
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.0, 1.0, 0.0, 1.0)
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


	def checkExit(self):
		if floor(self.x / self.size) == 0 and floor(self.y / self.size) == 0:
			return True
		else:
			return False


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

