#       SFGAME       #
#     pygame demo    #
#    catwhip 2020    #

# imports
from constants import *
from items import *
from ui import *

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

		for x in range(0, size[0]):
			# adding list for each x coordinate, and then list inside list for each y coordinate
			# x before y so it's easier to write code looking for a specific tile (so you can go cMap[x][y] rather than cMap[y][x])
			self.grid.append([])

			for y in range(0, size[1]):
				self.grid[x].append(None)
	
	def update(self):
		for s in self.stats:
			self.stats[s] = 0
			self.cost = 0
		
		for y in self.grid:
			for x in y:
				if not x == None:
					# calculate bunker stats with each piece of furniture
					for z in FURNITURE[x].stats:
						if z not in self.stats:
							self.stats[z] = FURNITURE[x].stats[z]
						else:
							self.stats[z] += FURNITURE[x].stats[z]

					self.cost += FURNITURE[x].cost

class Guy:
	pos   = [1, 1]
	move  = [0, 0]

	direction  = "down"
	animTimer  = 0
	animFrames = 4
	animLength = 8

	cash = 1000
	inventory = {}

	def __init__(self, cMap):
		self.size = (cMap.tileSize, cMap.tileSize)
		self.speed = int(cMap.tileSize / 16)

		# lambda functions to find tile in front of player based on direction
		self.dExp = {
			"up":    lambda : (self.pos[0], self.pos[1] - 1),
			"down":  lambda : (self.pos[0], self.pos[1] + 1),
			"left":  lambda : (self.pos[0] - 1, self.pos[1]),
			"right": lambda : (self.pos[0] + 1, self.pos[1]),
		}

		# loading each of the animations
		self.anims = {
			"up":    pygame.transform.scale(pygame.image.load("./assets/sprites/guy/up.png"), (self.size[0] * self.animFrames, self.size[1])),
			"down":  pygame.transform.scale(pygame.image.load("./assets/sprites/guy/down.png"), (self.size[0] * self.animFrames, self.size[1])),
			"left":  pygame.transform.scale(pygame.image.load("./assets/sprites/guy/left.png"), (self.size[0] * self.animFrames, self.size[1])),
			"right": pygame.transform.scale(pygame.image.load("./assets/sprites/guy/right.png"), (self.size[0] * self.animFrames, self.size[1])),
		}
		self.animRect = pygame.Rect(0, 0, self.size[0], self.size[1])

		# sfx stuff
		self.sfx = {
			"wrong": pygame.mixer.Sound("./assets/sfx/wrong.mp3"),
			"click": pygame.mixer.Sound("./assets/sfx/click.mp3"),
			"step":  pygame.mixer.Sound("./assets/sfx/step.mp3"),
		}
		self.sfxChannel = pygame.mixer.find_channel()

		self.menu = ItemMenu(cMap)
	
	def _checkBorder(self, cMap):
		# check if player hitting border
		if self.direction == "up":
			if not (self.pos[1] == 0):
				return True
		elif self.direction == "down":
			if not (self.pos[1] == cMap.size[1] - 1):
				return True
		elif self.direction == "left":
			if not (self.pos[0] == 0):
				return True
		elif self.direction == "right":
			if not (self.pos[0] == cMap.size[0] - 1):
				return True
		
		return False

	def _inventoryAdd(self, cMap):
		# add tile in front of player to inventory
		# this looks super messy but i SWEAR its just one semi-long piece of code copy and pasted 4 times
		if not cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]] == None:
			if not cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]] in self.inventory:
				self.inventory[cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]]] = 0
			self.inventory[cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]]] += 1
			return True
		return False
	
	def _move(self, direction, cMap):
		self.direction = direction

		if self._checkBorder(cMap):
			# basic checking direction and moving if nothing obstructing
			if cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]] == None or FURNITURE[cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]]].level == 0:
				self.pos = self.dExp[self.direction]()
				self.sfx["step"].play()
				
				if self.direction == "up" or self.direction == "down":
					self.move[1] += self.size[1] if self.direction == "up" else -self.size[1]
				if self.direction == "left" or self.direction == "right":
					self.move[0] += self.size[0] if self.direction == "left" else -self.size[0]
			else:
				if not self.sfxChannel.get_busy():
					self.sfxChannel.play(self.sfx["wrong"])
	
	def update(self, eventList, cMap):
		keys = pygame.key.get_pressed()

		self.animTimer += 1

		if not self.move == [0, 0]:
			# move until self.move (animated moving) goes to 0
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
				# basic controls (keyboard)
				if keys[pygame.K_UP]:
					self._move("up", cMap)
				elif keys[pygame.K_DOWN]:
					self._move("down", cMap)
				elif keys[pygame.K_LEFT]:
					self._move("left", cMap)
				elif keys[pygame.K_RIGHT]:
					self._move("right", cMap)
				else:
					if joysticks:
						# basic controls (controller)
						if joysticks[-1].get_axis(1) < -0.9:
							self._move("up", cMap)
						elif joysticks[-1].get_axis(1) > 0.9:
							self._move("down", cMap)
						elif joysticks[-1].get_axis(0) < -0.9:
							self._move("left", cMap)
						elif joysticks[-1].get_axis(0) > 0.9:
							self._move("right", cMap)
						else:
							self.animTimer = 0

							# looking around (controller)
							if joysticks[-1].get_axis(3) < -0.9:
								self.direction = "up"
							elif joysticks[-1].get_axis(3) > 0.9:
								self.direction = "down"
							elif joysticks[-1].get_axis(2) < -0.9:
								self.direction = "left"
							elif joysticks[-1].get_axis(2) > 0.9:
								self.direction = "right"
					else:
						self.animTimer = 0
		
		if self.menu.visible:
			response = self.menu.update(eventList, self)

			if self.move == [0, 0]:
				# reset animations since not moving
				self.animTimer = 0

			if not response == None:
				# add furniture: add existing to inventory if exists, add to grid, take cash (if necessary), and play sfx
				if ((self.cash >= FURNITURE[response].cost) or (response in self.inventory and self.inventory[response] > 0)) and self._checkBorder(cMap):
					self._inventoryAdd(cMap)
					cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]] = self.menu.select

					if response in self.inventory and self.inventory[response] > 0:
						self.inventory[response] -= 1
					else:
						self.cash -= FURNITURE[response].cost

					self.menu.visible = False
					self.sfxChannel.play(self.sfx["click"])
				else:
					if not self.sfxChannel.get_busy():
						self.sfxChannel.play(self.sfx["wrong"])

		else:
			for event in eventList:
				if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
					if controlEqual(event, pygame.K_c, 0):
						# open menu (c or a)
						self.menu.visible = not self.menu.visible
						self.sfxChannel.play(self.sfx["click"])
					
					if controlEqual(event, pygame.K_x, 2):
						# remove furniture: checks for item in front of player, and adds it to inventory (x or x)
						if self._checkBorder(cMap):
							if self._inventoryAdd(cMap):
								cMap.grid[self.dExp[self.direction]()[0]][self.dExp[self.direction]()[1]] = None
								self.sfxChannel.play(self.sfx["click"])
						
					if controlEqual(event, pygame.K_v, 1):
						# thing for testing: add $1000 to cash (v or b)
						self.cash += 1000
		
		# animation and animrect stuff
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
		pygame.init()

		self.cMap = Map((8, 8), 48)
		self.guy = Guy(self.cMap)
		self.bg = pygame.transform.scale(pygame.image.load("./assets/sprites/room/floor.png"), (self.cMap.tileSize, self.cMap.tileSize))
		self.ui = UI()

		for j in range(pygame.joystick.get_count()):
			# controllers
			joysticks.append(pygame.joystick.Joystick(j))
			joysticks[-1].init()

		# music
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
			
			if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
				if controlEqual(event, pygame.K_ESCAPE, 7):
					# exit game (esc or start)
					self.active = False
				
				if controlEqual(event, pygame.K_m, 6):
					# mute game (m or back)
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
				# draw background one tile at a time
				self.cMap.surface.blit(self.bg, (x * self.cMap.tileSize, y * self.cMap.tileSize))
				if not self.cMap.grid[x][y] == None:
					# draw furniture one tile at a time
					FURNITURE[self.cMap.grid[x][y]].draw(self.cMap.surface, (x * self.cMap.tileSize, y * self.cMap.tileSize), (self.cMap.tileSize, self.cMap.tileSize))
		
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