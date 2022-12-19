from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import random
from random import randint


class Obstacles:
	"""docstring for Obstacles"""


	def __init__(self, world):
		self.obstacles = []
		self.size = world.w / 8
		self.probability = 0.2

		for i in range(world.cols):
			for j in range(world.rows):
				if random() < self.probability:
					x = i * world.w + world.w/4
					y = j * world.w + world.w/4
					damage = randint(1, 3)
					self.obstacles.append(Obstacle(x, y, self.size, damage))


	def display(self):
		for obstacle in self.obstacles:
			obstacle.display()


	def checkCollision(self, player, scoreboard):
		for obstacle in self.obstacles:
			if obstacle.checkCollision(player):
				obstacle.takeAction(scoreboard)


class Obstacle:
	"""docstring for Obstacle"""
	

	def __init__(self, x, y, size, damage):
		self.x = x
		self.y = y
		self.size = size
		self.damage = damage  # each obstacle providing a variable damage
		self.contact = False  # to have just 1 damege in single contact


	def display(self):
		x = self.x
		y = self.y
		s = self.size

		# glColor3f(1.0, 0.0, 1.0)
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (1.0, 0.0, 1.0, 1.0)
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


	def checkCollision(self, p):
		x = self.x
		y = self.y
		s = self.size

		if p.x < x < p.x + p.size and p.y < y < p.y + p.size:
			# then first vertex in collision zone
			if not self.contact:
				# damage not done yet due to collision
				self.contact = True
				return True
			else:
				return False
		
		elif p.x < x+s < p.x + p.size and p.y < y < p.y + p.size:
			if not self.contact:
				self.contact = True
				return True
			else:
				return False

		elif p.x < x+s < p.x + p.size and p.y < y+s < p.y + p.size:
			if not self.contact:
				self.contact = True
				return True
			else:
				return False
		
		elif p.x < x < p.x + p.size and p.y < y+s < p.y + p.size:
			if not self.contact:
				self.contact = True
				return True
			else:
				return False
		
		elif self.contact:
			self.contact = False
		
		return False


	def takeAction(self, scoreboard):
		scoreboard.health = max(scoreboard.health - self.damage, 0)
