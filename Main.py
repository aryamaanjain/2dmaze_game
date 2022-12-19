import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from World import *
from Player import *
from Enemy import *
from Obstacles import *
from Powerups import *
from Scoreboard import *


def init():
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glEnable(GL_DEPTH_TEST)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)


def lighting():
	# set light intensity and color
	lambient  = (0.0, 0.0, 0.0, 1.0)
	ldiffuseFullBattery  = (1.0, 1.0, 1.0, 1.0)
	lspecularFullBattery = (0.2, 0.2, 0.2, 1.0)

	k = (s.battery - s.batteryTime/s.batteryReduce)/10.0  # constant for light reduction with battery
	ldiffuse = tuple([min(i * k, 1.0) for i in ldiffuseFullBattery])
	lspecular = tuple([min(i * k, 0.2) for i in lspecularFullBattery])

	glLightfv(GL_LIGHT0, GL_AMBIENT, lambient)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, ldiffuse)
	glLightfv(GL_LIGHT0, GL_SPECULAR, lspecular)

	# set light position
	lposition = (p.x, p.y, w.w/2, 1.0)
	glLightfv(GL_LIGHT0, GL_POSITION, lposition)


def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()  # resets all matrix transformations in model-view matrix / resets co-ordinate system

	gluLookAt( p.x-2.5, p.y-2.5, camz, 
			   p.x-2.5, p.y-2.5, -10.0, 
			   0.0, 1.0,  0.0)

	glTranslatef(-2.5, -2.5, -8.0)  # load identity necessary else translate relative to previous translate
	# glRotatef(angle, 1, 1, 1)

	# glBegin(GL_QUADS)
	# glEnd()

	w.display()
	w.shadow(p)
	p.display()
	e.display()
	o.display()
	u.display()
	s.display()

	glutSwapBuffers()  # since using double buffers


def reshape(width, height):
	if height == 0:
		height = 1
	ratio = width * 1.0 / height
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0, 0, width, height)
	# gluOrtho2D(-100, 100, -100, 100)
	# glOrtho(-4, 4, -4, 4, 0, 100)
	gluPerspective(45.0, ratio, 0.1, 100.0)  # fov, ar, znear, zfar
	glMatrixMode(GL_MODELVIEW)


def timer(t):
	fps = int(1000/60)  # 60 fps
	glutTimerFunc(fps, timer, 0)

	lighting()
	
	if playerMove[0]:
		p.moveLeft(w)
		playerMove[0] = False
	
	if playerMove[1]:
		p.moveRight(w)
		playerMove[1] = False
	
	if playerMove[2]:
		p.moveUp(w)
		playerMove[2] = False

	if playerMove[3]:
		p.moveDown(w)
		playerMove[3] = False

	u.checkCollision(p, s)
	s.reduceBattery()
	o.checkCollision(p, s)
	e.updatePosition(p, w)
	e.checkCollision(p, s)

	if p.checkExit():
		s.final('You Win!', win)
	elif s.giveHealth() == 0:
		s.final('You Lose!', win)

	glutPostRedisplay()


def processNormalKeys(key, x, y):
	global camz

	if key == b'\x1b':  # Esc
		s.final('You exited the game', win)
	
	elif key == b'z':  # zoom in
		camz -= 0.1

	elif key == b'x':  # zoom out
		camz += 0.1


def processSpecialKeys(key, x, y):
	
	if key == GLUT_KEY_LEFT:
		playerMove[0] = True
	elif key == GLUT_KEY_RIGHT:
		playerMove[1] = True
	elif key == GLUT_KEY_UP:
		playerMove[2] = True
	elif key == GLUT_KEY_DOWN:
		playerMove[3] = True


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowPosition(10, 10)
glutInitWindowSize(650, 650)
win = glutCreateWindow("Game")
	
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutTimerFunc(0, timer, 0)
glutKeyboardFunc(processNormalKeys)
glutSpecialFunc(processSpecialKeys)

init()
w = World(10, 10, 0.5)
p = Player(w)
e = Enemy(w)
o = Obstacles(w)
u = Powerups(w)
s = Scoreboard(w)

playerMove = [False, False, False, False]  # keeps track of which directions to move player on every timer tick, order: l r u d
camz = -6.2

glutMainLoop()
