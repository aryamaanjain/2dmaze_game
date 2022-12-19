from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ctypes import c_int
from sys import exit


class Scoreboard:
	"""docstring for Scoreboard"""
	

	def __init__(self, world):
		self.score = 0
		self.health = 10
		
		self.battery = 10
		self.batteryTime = 1  # updated every frame, to track when to reduce battery
		self.batteryReduce = 200  # reduce battery after these many frames

		self.y = world.w * (world.rows+0.5)
		self.font = GLUT_BITMAP_8_BY_13


	def display(self):
		x = 0
		y = self.y

		# display string
		dstring = "Score = %d | Health = %d | Battery = %d" % (self.score, self.health, self.battery)

		# glRasterPos2f(x, y)
		glWindowPos2i(10, 10)
		for ch in dstring:
			glutBitmapCharacter(self.font, c_int(ord(ch)))


	def giveHealth(self):
		return self.health


	def reduceBattery(self):
		self.batteryTime = (self.batteryTime + 1) % self.batteryReduce

		if self.batteryTime == 0:
			self.battery = max(self.battery-1, 0)


	def final(self, message, win):
		print(message)
		print("Score =", self.score)
		print("Health =", self.health)
		print("Battery =", self.battery)
		glutDestroyWindow(win)
		exit(0)
