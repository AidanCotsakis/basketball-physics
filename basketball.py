import numpy as np
import math
import random
import pygame
pygame.init()

screen_size = [1920, 1080]
fps = 120
CAPTION = 'Basketball'

fill_colour = (25,25,25)
surface_colour = (255,255,255)
ball_colour = (255,255,255)
trail_colour = (255,255,255)

trail_required_speed = 20
trail_cooldown = 120
trail_timer = 0

speed_multipleyer = 0.05
click = False

particles = []
tick = 0

surfaces = []
net =  [[1625, 375], [125, 50]]
surfaces.append([np.array([0, 1060]), np.array([1920,50])])

surfaces.append([np.array([1850, 250]), np.array([25,780])])
surfaces.append([np.array([1775, 200]), np.array([25,225])])

surfaces.append([np.array([1800, 260]), np.array([50,25])])
surfaces.append([np.array([1800, 340]), np.array([50,25])])

surfaces.append([np.array([1600, 375]), np.array([25,25])])
surfaces.append([np.array([1750, 375]), np.array([25,25])])

surfaces.append([np.array([1825, 1000]), np.array([75,60])])

corners = []
for surface in surfaces:
	corners.append(np.array([surface[0][0], surface[0][1]]))
	corners.append(np.array([surface[0][0]+surface[1][0], surface[0][1]]))
	corners.append(np.array([surface[0][0], surface[0][1]+surface[1][1]]))
	corners.append(np.array([surface[0][0]+surface[1][0], surface[0][1]+surface[1][1]]))

grass = pygame.image.load('grass.png')

clock = pygame.time.Clock()
win = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

class ball_physics(object):
	def __init__(self, radius, ball_center):
		self.radius = radius
		self.ball_center = np.array(ball_center)
		self.ball_speed = np.array([0.0, 0.0])
		self.gravity = np.array([0.0,0.25])
		self.friction = np.array([0.005,0.0])
		self.apply_gravity = True
		self.disable_gravity = 1
		self.disable_friction = 0.1
		self.bounce_strength = 0.8
		self.speed_cap = 50
		self.collided = False
		self.scored = False
		self.countdown_time = 20
		self.explosion_time = -120
		self.countdown = self.countdown_time
		self.show = True

	def apply_force(self):
		if self.ball_speed[0] > self.speed_cap:
			self.ball_speed[0] = self.speed_cap
		if self.ball_speed[0] < -self.speed_cap:
			self.ball_speed[0] = -self.speed_cap
		if self.ball_speed[1] > self.speed_cap:
			self.ball_speed[1] = self.speed_cap
		if self.ball_speed[1] < -self.speed_cap:
			self.ball_speed[1] = -self.speed_cap

		#friction
		if self.apply_gravity == False:
			if self.ball_speed[0] > self.disable_friction:
				self.ball_speed -= self.friction
			elif self.ball_speed[0] < -self.disable_friction:
				self.ball_speed += self.friction
			else:
				self.ball_speed[0] = 0

		#gravity
		if self.apply_gravity:
			self.ball_speed += self.gravity

		#edit ball position
		self.ball_center += self.ball_speed

	def mirror_martix(self, n, f):
		# f is the fraction of speed that remains (in the direction of n)
		# n is perpendicular to the mirror surface
		# return: Matrix associated with the mirror

		L = np.array([[-f, 0],[0, 1]])  # flips the x, and dampens x motion (vertical mirror)

		# Compute change of basis matrix
		new_x = -n  # First e.vector
		new_y = np.array([-new_x[1], new_x[0]])  # second e.vector
		S = np.array([new_x, new_y]) 
		S = S.T  # matrix of e.vectors as columns instead of rows

		return S @ L @ np.linalg.inv(S)
	
	def collision(self):
		self.apply_gravity = True
		self.collided = False
		ball_speed_old = self.ball_speed
		
		if self.ball_center[1] > screen_size[1] * 1.2:
			self.scored = True
			self.countdown = self.explosion_time - 1

		point = np.array([self.ball_center[0] + self.radius, self.ball_center[1]])
		if point[0] > screen_size[0]:
			self.collided = True
			M = self.mirror_martix(np.array([1, 0]), self.bounce_strength)
			self.ball_speed = M @ self.ball_speed
			self.ball_center[0] = screen_size[0] - self.radius + 1
		
		point = np.array([self.ball_center[0] - self.radius, self.ball_center[1]])
		if point[0] < 0:
			self.collided = True
			M = self.mirror_martix(np.array([1, 0]), self.bounce_strength)
			self.ball_speed = M @ self.ball_speed
			self.ball_center[0] = 0 + self.radius - 1
		
		for surface in surfaces:
			
			#test collision on botttom of ball
			if ball_speed_old[1] >= 0:
				point = np.array([self.ball_center[0], self.ball_center[1] + self.radius])
				if point[0] > surface[0][0] and point[0] < surface[0][0] + surface[1][0] and point[1] > surface[0][1] and point[1] < surface[0][1] + surface[1][1]:
					if self.ball_speed[1] > -self.disable_gravity and self.ball_speed[1] < self.disable_gravity:
						self.ball_speed[1] = 0
						self.ball_center[1] = surface[0][1] - self.radius + 1
						self.apply_gravity = False
					else:
						self.collided = True
						M = self.mirror_martix(np.array([0, 1]), self.bounce_strength)
						self.ball_speed = M @ self.ball_speed
						self.ball_center[1] = surface[0][1] - self.radius + 1
			
			#test collision on right of ball
			if ball_speed_old[0] > 0:
				point = np.array([self.ball_center[0] + self.radius, self.ball_center[1]])
				if point[0] > surface[0][0] and point[0] < surface[0][0] + surface[1][0] and point[1] > surface[0][1] and point[1] < surface[0][1] + surface[1][1]:
					self.collided = True
					M = self.mirror_martix(np.array([1, 0]), self.bounce_strength)
					self.ball_speed = M @ self.ball_speed
					self.ball_center[0] = surface[0][0] - self.radius + 1
			
			#test collision on left of ball
			if ball_speed_old[0] < 0:
				point = np.array([self.ball_center[0] - self.radius, self.ball_center[1]])
				if point[0] > surface[0][0] and point[0] < surface[0][0] + surface[1][0] and point[1] > surface[0][1] and point[1] < surface[0][1] + surface[1][1]:
					self.collided = True
					M = self.mirror_martix(np.array([1, 0]), self.bounce_strength)
					self.ball_speed = M @ self.ball_speed
					self.ball_center[0] = surface[0][0] + surface[1][0] + self.radius - 1
			
			#test collision on left of ball
			if ball_speed_old[1] < 0:
				point = np.array([self.ball_center[0], self.ball_center[1] - self.radius])
				if point[0] > surface[0][0] and point[0] < surface[0][0] + surface[1][0] and point[1] > surface[0][1] and point[1] < surface[0][1] + surface[1][1]:
					self.collided = True
					M = self.mirror_martix(np.array([0, 1]), self.bounce_strength)
					self.ball_speed = M @ self.ball_speed
					self.ball_center[1] = surface[0][1] + surface[1][1] + self.radius - 1

		if self.collided == False:
			smallest_corner = [1000000000.0, np.array([0, 0])]
			for corner in corners:
				distance = math.sqrt((self.ball_center[0] - corner[0])**2+(self.ball_center[1] - corner[1])**2)
				if distance < smallest_corner[0]:
					smallest_corner[0] = distance
					smallest_corner[1] = corner

			if smallest_corner[0] < 50:
				n = self.ball_center - smallest_corner[1]
				M = self.mirror_martix(n, self.bounce_strength)
				self.ball_speed = M @ self.ball_speed
				self.apply_force()

		if self.ball_center[0] > net[0][0] and self.ball_center[0] < net[0][0] + net[1][0] and self.ball_center[1] > net[0][1] and self.ball_center[1] < net[0][1] + net[1][1] and self.ball_speed[1] > 0:
			self.scored = True

	def explode(self):
		if self.scored:
			self.countdown -= 1
			if self.countdown == 0:
				self.show = False
				for i in range(100):
					particles.append(particle(self.ball_center, [-10,10], [-10,10], [5,15], [0,120], trail_colour, True))
			elif self.countdown <= self.explosion_time:
				self.ball_speed = np.array([0.0, 0.0])
				self.ball_center = np.array([random.uniform(300, 1620), 900])
				self.show = True
				self.scored = False
				self.countdown = self.countdown_time

basketball = ball_physics(50, [700.0,800.0])

class particle(object):
	def __init__(self, pos, horizontal_range, vertical_range, radius_range, life_range, colour, apply_gravity):
		self.pos = np.array([pos[0], pos[1]])
		self.momentum = np.array([(random.uniform(horizontal_range[0], horizontal_range[1])), (random.uniform(vertical_range[0], vertical_range[1]))])
		self.radius = random.randint(radius_range[0], radius_range[1])
		self.colour = colour
		self.apply_gravity = apply_gravity
		self.life = random.randint(life_range[0], life_range[1])
		self.gravity = np.array([0.0,0.25])

	def apply_force(self):
		#gravity
		if self.apply_gravity:
			self.momentum += self.gravity

		#edit ball position
		self.pos += self.momentum

		#kill particle
		self.life -= 1
		if self.life <= 0:
			particles.pop(particles.index(self))

	def draw(self):
		pygame.draw.circle(win, self.colour, [int(self.pos[0]), int(self.pos[1])], self.radius)


def draw():
	win.fill(fill_colour)

	for part in particles:
		part.draw()

	if basketball.show:
		pygame.draw.circle(win, ball_colour, [int(basketball.ball_center[0]), int(basketball.ball_center[1])], basketball.radius)

	pygame.draw.rect(win, surface_colour, [1625, 380, 125, 15])

	for surface in surfaces:
		pygame.draw.rect(win, surface_colour, [surface[0][0], surface[0][1], surface[1][0], surface[1][1]])

	win.blit(grass, [0, 1080 - 20 - 300])

	pygame.display.update()


while True:
	
	clock.tick(fps)
	caption = "{} - FPS: {:.2f}".format(CAPTION,clock.get_fps())
	pygame.display.set_caption(caption)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			click = True

	if click:
		mouseX, mouseY = pygame.mouse.get_pos()
		mouse = np.array([float(mouseX), float(mouseY)])
		difference = mouse - basketball.ball_center
		basketball.ball_speed = np.array([difference[0]*speed_multipleyer, difference[1]*speed_multipleyer])

	click = False
	trail_timer -= 1
	tick += 1

	basketball.collision()
	basketball.apply_force()
	basketball.explode()

	if tick % 120 == 0:
		particles.append(particle([random.uniform(0, screen_size[0]), random.uniform(0, screen_size[1])], [-0.5,0.5], [-0.5,0.5], [1,4], [500,1000], trail_colour, False))

	for part in particles:
		part.apply_force()

	draw()
