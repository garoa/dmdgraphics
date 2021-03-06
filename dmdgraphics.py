#!/usr/bin/env python

import serial
ser = serial.Serial(port="/dev/ttyUSB0")

ser.setBaudrate(19200)

buffer = None
	
WIDTH  = 168
HEIGHT = 16 

class Particle(object):
	
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
	
	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.vy += GRAVITY

def reset():
	global buffer
	buffer = [ [ 0x00 for _ in range(HEIGHT/8) ] for _ in range(WIDTH) ]

init = reset

def send_buffer():
	ser.write("D")
	for line in buffer:
		for byte in line:
			ser.write(chr(byte))

def plot(x, y, color=1):
	if x<0 or y<0:
		return
	x = int(x)
	y = int(y)
	try:
		if color:
			buffer[x][y/8] |= 1 << (7-y%8)
		else:
			buffer[x][y/8] &= 255 - 1 << (7-y%8)
	except IndexError, e:
		print e

def draw_rectangle(x, y, width, height, fill=False):
	if fill:
		for i in range(x, x+width+1):
			for j in range(y, y+height+1):
				plot(i, j)
	else:
		for i in range(x, x+width+1):
			plot (i,y)
			plot (i,y+height)

		for j in range(y, y+height+1):
			plot (x,j)
			plot (x+width,j)
			
import time, random

init()

while 0:
	raw_input()
	for i in range(60):
		for j in range(2):
			buffer[i][j] = 0xFF
	send_buffer()
	#print buffer
	raw_input()
while 0:
	x = random.choice(range(WIDTH))
	y = random.choice(range(HEIGHT))
	plot(x,y)
	#time.sleep(1)
	send_buffer()
	#raw_input()

while 0: #random rectangles
	x = random.choice(range(WIDTH))
	y = random.choice(range(HEIGHT))
	w = random.choice(range(HEIGHT))
	h = random.choice(range(HEIGHT))
	draw_rectangle(x, y, w, h, True)
	#time.sleep(1)
	send_buffer()

NUM_PARTICLES = 40
GRAVITY = 0.5
VMAX=4
while 42:
	x = random.choice(range(WIDTH))
	y = random.choice(range(HEIGHT/2))

	particles = [ Particle(x, y, random.random()*2*VMAX - VMAX, random.random()*2*VMAX - VMAX) for _ in range(NUM_PARTICLES) ]

	for _ in range(12):
		reset()
		map(Particle.update, particles)
		[ plot(p.x,p.y) for p in particles ]
		send_buffer()