# pap

from constants import *
from items import *

clock = pygame.time.Clock()

class Map():
	cost = 0
	# y goes first, x goes second
	
	def __init__(self, size, tileSize):
		self.grid = []
		self.size = size
		self.tileSize = tileSize
		self.surface = pygame.surface.Surface((self.size[0] * self.tileSize, self.size[1] * self.tileSize))

		self.stats = {}

		for y in range(0, size[0]):
			self.grid.append([])

			for x in range(0, size[1]):
				self.grid[y].append(0)
	
	def clear(self):
		for y in self.grid:
			for x in y:
				x = 0
	
	def update(self):
		for s in self.stats:
			self.stats[s] = 0
			self.cost = 0
		
		for y in self.grid:
			for x in y:
				if x > 0:
					for z in FURNITURE[x - 1].stats:
						if z not in self.stats:
							self.stats[z] = FURNITURE[x - 1].stats[z]
						else:
							self.stats[z] += FURNITURE[x - 1].stats[z]

					self.cost += FURNITURE[x - 1].cost

class UI:
	def __init__(self):
		self.font = pygame.font.Font("./assets/geopixel.ttf", 10)

		self.tutorial = []
		self.props = {}
	
	def update(self, cMap, guy):
		for s in cMap.stats:
			self.props[s] = self.font.render(f"{s}: {cMap.stats[s]}", False, (177, 156, 217))
		
		self.props["cash"] = self.font.render(f"cash: ${guy.cash}", False, (119, 221, 119))

		self.tutorial = [
			self.font.render("sfgame v0.0.1 - 16/02/21 build", False, (255, 255, 255)),
			self.font.render(" ", False, (255, 255, 255)),
			self.font.render(" ", False, (255, 255, 255)),
		]

		if guy.menu.visible:
			self.tutorial.append(self.font.render("arrow keys - select", False, (255, 255, 255)))
			self.tutorial.append(self.font.render("c - close menu", False, (255, 255, 255)))
			if FURNITURE[guy.menu.select].cost <= guy.cash:
				self.tutorial.append(self.font.render("x - buy + place", False, (255, 255, 255)))
		else:
			self.tutorial.append(self.font.render("arrow keys - move", False, (255, 255, 255)))
			self.tutorial.append(self.font.render("c - open menu", False, (255, 255, 255)))
		
		if guy.direction == "up":
			if not (guy.pos[1] == 0):
				if cMap.grid[guy.pos[0]][guy.pos[1] - 1] > 0:
					self.tutorial.append(self.font.render("x - sell", False, (255, 255, 255)))
		elif guy.direction == "down":
			if not (guy.pos[1] == cMap.size[1] - 1):
				if cMap.grid[guy.pos[0]][guy.pos[1] + 1] > 0:
					self.tutorial.append(self.font.render("x - sell", False, (255, 255, 255)))
		elif guy.direction == "left":
			if not (guy.pos[0] == 0):
				if cMap.grid[guy.pos[0] - 1][guy.pos[1]] > 0:
					self.tutorial.append(self.font.render("x - sell", False, (255, 255, 255)))
		elif guy.direction == "right":
			if not (guy.pos[0] == cMap.size[0] - 1):
				if cMap.grid[guy.pos[0] + 1][guy.pos[1]] > 0:
					self.tutorial.append(self.font.render("x - sell", False, (255, 255, 255)))
	
	def draw(self, surface, cMap):
		if self.props:
			pSurface = pygame.surface.Surface((max(self.props[x].get_rect().w for x in self.props), sum(self.props[y].get_rect().h + 3 for y in self.props) - 3))
		else:
			pSurface = pygame.surface.Surface((0, 0))

		tSurface = pygame.surface.Surface((max(x.get_rect().w for x in self.tutorial), sum(y.get_rect().h + 3 for y in self.tutorial) - 3))
		
		for t in range(0, len(self.tutorial)):
		 	y = sum(x.get_rect().h + 3 for x in self.tutorial[:t])
		 	tSurface.blit(self.tutorial[t], ((tSurface.get_width() / 2) - (self.tutorial[t].get_rect().w / 2), y))
		
		counter = 0
		for t in self.props:
			y = sum(x.get_rect().h + 3 for x in [self.props[y] for y in self.props][:counter]) #self.tutorial[:t]
			pSurface.blit(self.props[t], ((pSurface.get_width() / 2) - (self.props[t].get_rect().w / 2), y))
			counter += 1
		
		surface.blit(tSurface, ((((SURFACE_SIZE[0] / 2) - (cMap.size[0] * (cMap.tileSize / 2))) / 2) - (tSurface.get_width() / 2), (SURFACE_SIZE[1] / 2) - (tSurface.get_height() / 2)))
		surface.blit(pSurface, (SURFACE_SIZE[0] - ((((SURFACE_SIZE[0] / 2) - (cMap.size[0] * (cMap.tileSize / 2))) / 2)) - (pSurface.get_width() / 2), (SURFACE_SIZE[1] / 2) - (pSurface.get_height() / 2)))

class Guy:
	anims = {}
	pos   = [1, 1]
	move  = [0, 0]

	direction  = "down"
	animTimer  = 0
	animFrames = 4
	animLength = 8

	cash = 1000

	def __init__(self, cMap):
		self.size = (cMap.tileSize, cMap.tileSize)
		self.speed = int(cMap.tileSize / 16)

		self.anims["up"] = pygame.transform.scale(pygame.image.load("./assets/Character_Up.png"), (self.size[0] * self.animFrames, self.size[1]))
		self.anims["down"] = pygame.transform.scale(pygame.image.load("./assets/Character_Down.png"), (self.size[0] * self.animFrames, self.size[1]))
		self.anims["left"] = pygame.transform.scale(pygame.image.load("./assets/Character_Left.png"), (self.size[0] * self.animFrames, self.size[1]))
		self.anims["right"] = pygame.transform.scale(pygame.image.load("./assets/Character_Right.png"), (self.size[0] * self.animFrames, self.size[1]))
		self.animRect = pygame.Rect(0, 0, self.size[0], self.size[1])

		self.sfx = {
			"wrong": pygame.mixer.Sound("./assets/sfx/wrong.mp3"),
			"click": pygame.mixer.Sound("./assets/sfx/click.mp3"),
			"step":  pygame.mixer.Sound("./assets/sfx/step.mp3"),
		}
		self.sfxChannel = pygame.mixer.find_channel()

		self.menu = ItemMenu(cMap)

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
		
		if self.move == [0, 0] and not self.menu.visible:
			self.sfx["step"].stop()

			if not self.menu.visible:
				if keys[pygame.K_UP]:
					self.direction = "up"
					if not (self.pos[1] == 0):
						if (cMap.grid[self.pos[0]][self.pos[1] - 1] == 0):
							self.pos[1] -= 1
							self.move[1] += self.size[1]
							self.sfx["step"].play()
						else:
							if (FURNITURE[cMap.grid[self.pos[0]][self.pos[1] - 1] - 1].level == 0):
								self.pos[1] -= 1
								self.move[1] += self.size[1]
								self.sfx["step"].play()
							else:
								if not self.sfxChannel.get_busy():
									self.sfxChannel.play(self.sfx["wrong"])
				elif keys[pygame.K_DOWN]:
					self.direction = "down"
					if not (self.pos[1] == cMap.size[1] - 1):
						if (cMap.grid[self.pos[0]][self.pos[1] + 1] == 0):
							self.pos[1] += 1
							self.move[1] -= self.size[1]
							self.sfx["step"].play()
						else:
							if (FURNITURE[cMap.grid[self.pos[0]][self.pos[1] + 1] - 1].level == 0):
								self.pos[1] += 1
								self.move[1] -= self.size[1]
								self.sfx["step"].play()
							else:
								if not self.sfxChannel.get_busy():
									self.sfxChannel.play(self.sfx["wrong"])
				elif keys[pygame.K_LEFT]:
					self.direction = "left"
					if not (self.pos[0] == 0):
						if (cMap.grid[self.pos[0] - 1][self.pos[1]] == 0):
							self.pos[0] -= 1
							self.move[0] += self.size[1]
							self.sfx["step"].play()
						else:
							if (FURNITURE[cMap.grid[self.pos[0] - 1][self.pos[1]] - 1].level == 0):
								self.pos[0] -= 1
								self.move[0] += self.size[1]
								self.sfx["step"].play()
							else:
								if not self.sfxChannel.get_busy():
									self.sfxChannel.play(self.sfx["wrong"])
				elif keys[pygame.K_RIGHT]:
					self.direction = "right"
					if not (self.pos[0] == cMap.size[0] - 1):
						if (cMap.grid[self.pos[0] + 1][self.pos[1]] == 0):
							self.pos[0] += 1
							self.move[0] -= self.size[1]
							self.sfx["step"].play()
						else:
							if (FURNITURE[cMap.grid[self.pos[0] + 1][self.pos[1]] - 1].level == 0):
								self.pos[0] += 1
								self.move[0] -= self.size[1]
								self.sfx["step"].play()
							else:
								if not self.sfxChannel.get_busy():
									self.sfxChannel.play(self.sfx["wrong"])
				else:
					self.animTimer = 0
		
		if self.menu.visible:
			response = self.menu.update(eventList)

			if self.move == [0, 0]:
				self.animTimer = 0

			if response > -1:
				if self.cash >= FURNITURE[response].cost:
					if self.direction == "up":
						if not (self.pos[1] == 0):
							if cMap.grid[self.pos[0]][self.pos[1] - 1] > 0:
								self.cash += FURNITURE[cMap.grid[self.pos[0]][self.pos[1] - 1] - 1].cost
							cMap.grid[self.pos[0]][self.pos[1] - 1] = self.menu.select + 1
							
							self.cash -= FURNITURE[response].cost
							self.menu.visible = False
							self.sfxChannel.play(self.sfx["click"])
						else:
							if not self.sfxChannel.get_busy():
								self.sfxChannel.play(self.sfx["wrong"])
					elif self.direction == "down":
						if not (self.pos[1] == cMap.size[1] - 1):
							if cMap.grid[self.pos[0]][self.pos[1] + 1] > 0:
								self.cash += FURNITURE[cMap.grid[self.pos[0]][self.pos[1] + 1] - 1].cost
							cMap.grid[self.pos[0]][self.pos[1] + 1] = self.menu.select + 1

							self.cash -= FURNITURE[response].cost
							self.menu.visible = False
							self.sfxChannel.play(self.sfx["click"])
						else:
							if not self.sfxChannel.get_busy():
								self.sfxChannel.play(self.sfx["wrong"])
					elif self.direction == "left":
						if not (self.pos[0] == 0):
							if cMap.grid[self.pos[0] - 1][self.pos[1]] > 0:
								self.cash += FURNITURE[cMap.grid[self.pos[0] - 1][self.pos[1]] - 1].cost
							cMap.grid[self.pos[0] - 1][self.pos[1]] = self.menu.select + 1

							self.cash -= FURNITURE[response].cost
							self.menu.visible = False
							self.sfxChannel.play(self.sfx["click"])
						else:
							if not self.sfxChannel.get_busy():
								self.sfxChannel.play(self.sfx["wrong"])
					elif self.direction == "right":
						if not (self.pos[0] == cMap.size[0] - 1):
							if cMap.grid[self.pos[0] + 1][self.pos[1]] > 0:
								self.cash += FURNITURE[cMap.grid[self.pos[0] + 1][self.pos[1]] - 1].cost
							cMap.grid[self.pos[0] + 1][self.pos[1]] = self.menu.select + 1

							self.cash -= FURNITURE[response].cost
							self.menu.visible = False
							self.sfxChannel.play(self.sfx["click"])
						else:
							if not self.sfxChannel.get_busy():
								self.sfxChannel.play(self.sfx["wrong"])
				else:
					if not self.sfxChannel.get_busy():
						self.sfxChannel.play(self.sfx["wrong"])

		else:
			for event in eventList:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						self.menu.visible = not self.menu.visible
						self.sfxChannel.play(self.sfx["click"])
					
					if event.key == pygame.K_x:
						if self.direction == "up":
							if not (self.pos[1] == 0):
								if cMap.grid[self.pos[0]][self.pos[1] - 1] > 0:
									self.cash += FURNITURE[cMap.grid[self.pos[0]][self.pos[1] - 1] - 1].cost
									cMap.grid[self.pos[0]][self.pos[1] - 1] = 0
									self.sfxChannel.play(self.sfx["click"])
						elif self.direction == "down":
							if not (self.pos[1] == cMap.size[1] - 1):
								if cMap.grid[self.pos[0]][self.pos[1] + 1] > 0:
									self.cash += FURNITURE[cMap.grid[self.pos[0]][self.pos[1] + 1] - 1].cost
									cMap.grid[self.pos[0]][self.pos[1] + 1] = 0
									self.sfxChannel.play(self.sfx["click"])
						elif self.direction == "left":
							if not (self.pos[0] == 0):
								if cMap.grid[self.pos[0] - 1][self.pos[1]] > 0:
									self.cash += FURNITURE[cMap.grid[self.pos[0] - 1][self.pos[1]] - 1].cost
									cMap.grid[self.pos[0] - 1][self.pos[1]] = 0
									self.sfxChannel.play(self.sfx["click"])
						elif self.direction == "right":
							if not (self.pos[0] == cMap.size[0] - 1):
								if cMap.grid[self.pos[0] + 1][self.pos[1]] > 0:
									self.cash += FURNITURE[cMap.grid[self.pos[0] + 1][self.pos[1]] - 1].cost
									cMap.grid[self.pos[0] + 1][self.pos[1]] = 0
									self.sfxChannel.play(self.sfx["click"])
						
					if event.key == pygame.K_v:
						self.cash += 1000
		
		if int(self.animTimer / self.animLength) >= self.animFrames:
			self.animTimer = 0
		self.animRect.x = int(self.animTimer / self.animLength) * self.size[0]

	def draw(self, surface):
		surface.blit(self.anims[self.direction], [(self.pos[a] * self.size[0]) + self.move[a] for a in range(0, len(self.pos))], self.animRect)
		if self.menu.visible:
			self.menu.draw(surface)

class Game:
	surface = pygame.surface.Surface(SURFACE_SIZE)
	window  = pygame.display.set_mode(WINDOW_SIZE)
	active  = True
	muted   = False

	pygame.display.set_caption("sfgame")

	def __init__(self):
		#pygame.mixer.pre_init(44100, 16, 2, 4096)
		pygame.init()

		self.cMap = Map((8, 8), 48)
		self.guy = Guy(self.cMap)
		self.bg = pygame.transform.scale(pygame.image.load("./assets/floor_1.png"), (self.cMap.tileSize, self.cMap.tileSize))
		self.ui = UI()

		pygame.mixer.music.load("./assets/music/nc9.mp3")
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)

		#pygame.mixer.music.pause()
	
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
				
				if event.key == pygame.K_m:
					if self.muted:
						pygame.mixer.music.unpause()
					else:
						pygame.mixer.music.pause()
					
					self.muted = not self.muted
		
		self.guy.update(eventList, self.cMap)
		self.cMap.update()
		self.ui.update(self.cMap, self.guy)
	
	def draw(self):
		self.surface.fill((0, 0, 0))
		self.ui.draw(self.surface, self.cMap)
		
		for x in range(0, self.cMap.size[0]):
			for y in range(0, self.cMap.size[1]):
				self.cMap.surface.blit(self.bg, (x * self.cMap.tileSize, y * self.cMap.tileSize))
				if not self.cMap.grid[x][y] == 0:
					FURNITURE[self.cMap.grid[x][y] - 1].draw(self.cMap.surface, (x * self.cMap.tileSize, y * self.cMap.tileSize), (self.cMap.tileSize, self.cMap.tileSize))
		
		self.guy.draw(self.cMap.surface)

		self.surface.blit(self.cMap.surface, ((SURFACE_SIZE[0] / 2) - (self.cMap.size[0] * (self.cMap.tileSize / 2)), (SURFACE_SIZE[1] / 2) - (self.cMap.size[1] * (self.cMap.tileSize / 2))))
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