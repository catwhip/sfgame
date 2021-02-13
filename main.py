# pap

import pygame, math

SURFACE_SIZE = (640, 480)
WINDOW_SIZE = (1280, 960)
clock = pygame.time.Clock()

class Item():
	def __init__(self, name, image, size, level):
		self.name = name
		self.size = size
		self.level = level

		self.image = pygame.image.load(image)
	
	def draw(self, surface, pos):
		surface.blit(pygame.transform.scale(self.image, self.size), pos)
	
FURNITURE = (
	Item("bookcase", "./assets/furniture1.png", (32, 32), 1),
	Item("rug", "./assets/furniture21.png", (32, 32), 0),
)

class Map():
	# y goes first, x goes second
	
	def __init__(self, size):
		self.grid = []
		self.size = size

		for y in range(0, size[0]):
			self.grid.append([])

			for x in range(0, size[1]):
				self.grid[y].append(0)
	
	def clear(self):
		for y in self.grid:
			for x in y:
				x = 0

class Guy:
	speed = 2
	anims = {}
	size  = (32, 32)
	pos   = [1, 1]
	move  = [0, 0]

	direction  = "down"
	animTimer  = 0
	animFrames = 4
	animLength = 8

	def __init__(self):
		self.anims["up"] = pygame.image.load("./assets/Character_Up.png")
		self.anims["down"] = pygame.image.load("./assets/Character_Down.png")
		self.anims["left"] = pygame.image.load("./assets/Character_Left.png")
		self.anims["right"] = pygame.image.load("./assets/Character_Right.png")
	
	def update(self, eventList, cMap):
		keys = pygame.key.get_pressed()

		self.animTimer += 1

		if not self.move == [0, 0]:
			if self.move[1] > 0:
				self.move[1] -= self.speed
			if self.move[1] < 0:
				self.move[1] += self.speed
			if self.move[0] > 0:
				self.move[0] -= self.speed
			if self.move[0] < 0:
				self.move[0] += self.speed
		else:
			if keys[pygame.K_UP]:
				self.direction = "up"
				if not (self.pos[1] == 0):
					if (cMap.grid[self.pos[0]][self.pos[1] - 1] == 0):
						self.pos[1] -= 1
						self.move[1] += self.size[1]
					else:
						if (FURNITURE[cMap.grid[self.pos[0]][self.pos[1] - 1] - 1].level == 0):
							self.pos[1] -= 1
							self.move[1] += self.size[1]
			elif keys[pygame.K_DOWN]:
				self.direction = "down"
				if not (self.pos[1] == cMap.size[1] - 1):
					if (cMap.grid[self.pos[0]][self.pos[1] + 1] == 0):
						self.pos[1] += 1
						self.move[1] -= self.size[1]
					else:
						if (FURNITURE[cMap.grid[self.pos[0]][self.pos[1] + 1] - 1].level == 0):
							self.pos[1] += 1
							self.move[1] -= self.size[1]
			if keys[pygame.K_LEFT]:
				self.direction = "left"
				if not (self.pos[0] == 0):
					if (cMap.grid[self.pos[0] - 1][self.pos[1]] == 0):
						self.pos[0] -= 1
						self.move[0] += self.size[1]
					else:
						if (FURNITURE[cMap.grid[self.pos[0] - 1][self.pos[1]] - 1].level == 0):
							self.pos[0] -= 1
							self.move[0] += self.size[1]
			elif keys[pygame.K_RIGHT]:
				self.direction = "right"
				if not (self.pos[0] == cMap.size[0] - 1):
					if (cMap.grid[self.pos[0] + 1][self.pos[1]] == 0):
						self.pos[0] += 1
						self.move[0] -= self.size[1]
					else:
						if (FURNITURE[cMap.grid[self.pos[0] + 1][self.pos[1]] - 1].level == 0):
							self.pos[0] += 1
							self.move[0] -= self.size[1]
			else:
				self.animTimer = 0

		for event in eventList:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z:
					if self.direction == "up":
						if not (self.pos[1] == 0):
							cMap.grid[self.pos[0]][self.pos[1] - 1] = 1 if (cMap.grid[self.pos[0]][self.pos[1] - 1] == 0) else 0
					elif self.direction == "down":
						if not (self.pos[1] == cMap.size[1] - 1):
							cMap.grid[self.pos[0]][self.pos[1] + 1] = 1 if (cMap.grid[self.pos[0]][self.pos[1] + 1] == 0) else 0
					elif self.direction == "left":
						if not (self.pos[0] == 0):
							cMap.grid[self.pos[0] - 1][self.pos[1]] = 1 if (cMap.grid[self.pos[0] - 1][self.pos[1]] == 0) else 0
					elif self.direction == "right":
						if not (self.pos[0] == cMap.size[0] - 1):
							cMap.grid[self.pos[0] + 1][self.pos[1]] = 1 if (cMap.grid[self.pos[0] + 1][self.pos[1]] == 0) else 0
				
				if event.key == pygame.K_x:
					if self.direction == "up":
						if not (self.pos[1] == 0):
							cMap.grid[self.pos[0]][self.pos[1] - 1] = 2 if (cMap.grid[self.pos[0]][self.pos[1] - 1] == 0) else 0
					elif self.direction == "down":
						if not (self.pos[1] == cMap.size[1] - 1):
							cMap.grid[self.pos[0]][self.pos[1] + 1] = 2 if (cMap.grid[self.pos[0]][self.pos[1] + 1] == 0) else 0
					elif self.direction == "left":
						if not (self.pos[0] == 0):
							cMap.grid[self.pos[0] - 1][self.pos[1]] = 2 if (cMap.grid[self.pos[0] - 1][self.pos[1]] == 0) else 0
					elif self.direction == "right":
						if not (self.pos[0] == cMap.size[0] - 1):
							cMap.grid[self.pos[0] + 1][self.pos[1]] = 2 if (cMap.grid[self.pos[0] + 1][self.pos[1]] == 0) else 0
		
		if int(self.animTimer / self.animLength) >= self.animFrames:
			self.animTimer = 0

	def draw(self, surface):
		surface.blit(self.anims[self.direction], [(self.pos[a] * 32) + self.move[a] for a in range(0, len(self.pos))], pygame.Rect(int(self.animTimer / self.animLength) * self.size[0], 0, self.size[0], self.size[1]))

class Game:
	surface = pygame.surface.Surface(SURFACE_SIZE)
	window = pygame.display.set_mode(WINDOW_SIZE)
	active  = True

	pygame.display.set_caption("sanfrancisco")

	def __init__(self):
		pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()

		self.guy = Guy()
		self.cMap = Map((8, 8))

		self.font = pygame.font.Font("./assets/geopixel.ttf", 5)
		self.tutorial = [
			self.font.render("arrow keys - move", False, (255, 255, 255)),
			self.font.render("z - place bookcase", False, (255, 255, 255)),
			self.font.render("x - place rug", False, (255, 255, 255)),
			self.font.render("z or x - remove", False, (255, 255, 255)),
		]
	
	def __del__(self):
		pygame.quit()
	
	def update(self):
		eventList = pygame.event.get()

		for event in eventList:
			if event.type == pygame.QUIT:
				self.active = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.active = False
		
		self.guy.update(eventList, self.cMap)
	
	def draw(self):
		self.surface.fill((0, 0, 0))

		pygame.draw.rect(self.surface, (44, 44, 44), pygame.rect.Rect(0, 0, self.cMap.size[0] * 32, self.cMap.size[1] * 32))
		for x in range(0, self.cMap.size[0]):
			pygame.draw.rect(self.surface, (88, 88, 88), pygame.rect.Rect((x * 32) + 32, 0, 1, self.cMap.size[1] * 32))
		for y in range(0, self.cMap.size[1]):
			pygame.draw.rect(self.surface, (88, 88, 88), pygame.rect.Rect(0, (y * 32) + 32, self.cMap.size[0] * 32, 1))
		
		for x in range(0, self.cMap.size[0]):
			for y in range(0, self.cMap.size[1]):
				if not self.cMap.grid[x][y] == 0:
					FURNITURE[self.cMap.grid[x][y] - 1].draw(self.surface, (x * 32, y * 32))
		
		self.guy.draw(self.surface)

		for t in range(0, len(self.tutorial)):
			if t == 0:
				y = 0
			else:
				y = sum(x.get_rect().h + 3 for x in self.tutorial[:t])
			self.surface.blit(self.tutorial[t], ((self.cMap.size[0] * 32) + 6, y + 6))

		self.window.blit(pygame.transform.scale(self.surface, WINDOW_SIZE), (0, 0))
		pygame.display.flip()
	
	def main(self):
		while self.active:
			self.update()
			self.draw()

			clock.tick(60)

game = Game()
game.main()
del game