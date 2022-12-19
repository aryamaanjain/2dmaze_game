from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import random
from random import randint


class Powerups:
	"""docstring for Powerups"""
	def __init__(self, world):
		self.powerups = []
		self.size = world.w / 8
		self.probability = 0.4

		for i in range(world.cols):
			for j in range(world.rows):
				if random() < self.probability:
					x = i * world.w + world.w*3/4
					y = j * world.w + world.w*3/4
					r = randint(1, 3)
					
					if r == 1:
						self.powerups.append(Battery(x, y, self.size))
					elif r == 2:
						self.powerups.append(Scoreup(x, y, self.size))
					elif r == 3:
						self.powerups.append(Healthup(x, y, self.size))


	def display(self):
		for powerup in self.powerups:
			powerup.display()


	def checkCollision(self, player, scoreboard):
		newPowerups = []

		for powerup in self.powerups:
			if powerup.checkCollision(player):
				powerup.takeAction(scoreboard)
			else:
				newPowerups.append(powerup)

		self.powerups = newPowerups



class Powerup:
	"""docstring for Powerup"""
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size


	def display(self):
		pass


	def checkCollision(self, p):
		x = self.x
		y = self.y
		s = self.size

		if p.x < x < p.x + p.size and p.y < y < p.y + p.size:
			# then first vertex in collision zone
			return True
		elif p.x < x+s < p.x + p.size and p.y < y < p.y + p.size:
			return True
		elif p.x < x+s < p.x + p.size and p.y < y+s < p.y + p.size:
			return True
		elif p.x < x < p.x + p.size and p.y < y+s < p.y + p.size:
			return True
		else:
			# no vertex in collision zone
			return False


	def takeAction(self, scoreboard):
		pass
						

class Battery(Powerup):
	"""docstring for Battery"""
	def __init__(self, x, y, size):
		super().__init__(x, y, size)


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		# glColor3f(1.0, 1.0, 0.0)
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (1.0, 1.0, 0.0, 1.0)
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

		# glColor3f(1.0, 1.0, 1.0)


	def takeAction(self, scoreboard):
		scoreboard.battery += 1


class Scoreup(Powerup):
	"""docstring for Scoreup"""
	def __init__(self, x, y, size):
		super().__init__(x, y, size)


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.0, 1.0, 1.0, 1.0)
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


	def takeAction(self, scoreboard):
		scoreboard.score += 1


class Healthup(Powerup):
	"""docstring for Healthup"""
	def __init__(self, x, y, size):
		super().__init__(x, y, size)


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.0, 0.0, 1.0, 1.0)
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


	def takeAction(self, scoreboard):
		scoreboard.health += 1