# imports
from constants import *
from items import *

class UI:
	fontSize = 10

	def __init__(self, joystickType):
		self.font = pygame.font.Font("./assets/fonts/geopixel.ttf", self.fontSize)
		self.baseFolder = "./assets/sprites/icons/"
		self.joystickType = joystickType

		self.tutorial = []
		self.props = {}
	
	def _iconText(self, icon, text):
		# adds big icon for text
		t = self.font.render(text, False, (255, 255, 255))
		i = pygame.image.load(icon)
		i = pygame.transform.scale(i, (int(i.get_width() / self.fontSize / 2), int(i.get_height() / self.fontSize / 2)))

		s = pygame.surface.Surface((t.get_width() + i.get_width(), i.get_height()))

		s.blit(i, (0, 0))
		s.blit(t, (i.get_width(), (i.get_height() / 2) - (t.get_height() / 2)))

		return s
	
	def _keyButtonText(self, buttonIcon, keyString, string):
		# returns surface w text depending on whether controller or keyboard is used
		if joysticks or JOYSTICKTEST:
			return self._iconText(buttonIcon, f" - {string}")
		else:
			return self.font.render(f"{keyString} - {string}", False, (255, 255, 255))
	
	def _controllerType(self, buttonXbox, buttonPs):
		if self.joystickType == "xbox":
			return self.baseFolder + buttonXbox
		else:
			return self.baseFolder + buttonPs
	
	def update(self, cMap, guy):
		# base property for props
		for s in cMap.stats:
			self.props[s] = self.font.render(f"{s}: {cMap.stats[s]}", False, (177, 156, 217))
		
		self.props["cash"] = self.font.render(f"cash: ${guy.cash}", False, (119, 221, 119))

		# base text for tutorial
		self.tutorial = [
			self.font.render("sfgame v0.0.1 - 17/02/21 build", False, (255, 255, 255)),
			self.font.render(" ", False, (255, 255, 255)),
			self.font.render(" ", False, (255, 255, 255)),
		]

		# different controls displayed depending on character's position in bunker/next to furniture/in menu
		if guy.menu.visible:
			self.tutorial.append(self._keyButtonText(self._controllerType("xbox/dpad_updown.png", "ps/dpad.png"), "arrow keys", "select"))

			if guy.menu.select in guy.inventory and guy.inventory[guy.menu.select] > 0:
				self.tutorial.append(self._keyButtonText(self._controllerType("xbox/a.png", "ps/cross.png"), "x", "place from inventory"))
				self.tutorial.append(self._keyButtonText(self._controllerType("xbox/b.png", "ps/circle.png"), "c", "close menu"))
				self.tutorial.append(self._keyButtonText(self._controllerType("xbox/x.png", "ps/square.png"), "z", "sell"))
			else:
				if FURNITURE[guy.menu.select].cost <= guy.cash:
					self.tutorial.append(self._keyButtonText(self._controllerType("xbox/a.png", "ps/cross.png"), "x", "buy + place"))
				self.tutorial.append(self._keyButtonText(self._controllerType("xbox/b.png", "ps/circle.png"), "c", "close menu"))

		else:
			self.tutorial.append(self._keyButtonText(self._controllerType("xbox/thumbstick_left.png", "ps/thumbstick_left.png"), "arrow keys", "move"))
			if joysticks or JOYSTICKTEST:
				self.tutorial.append(self._iconText(self._controllerType("xbox/thumbstick_right.png", "ps/thumbstick_right.png"), " - look"))
			self.tutorial.append(self._keyButtonText(self._controllerType("xbox/a.png", "ps/cross.png"), "c", "open menu"))
		
			if guy._checkBorder(cMap):
				if not cMap.grid[guy.dExp[guy.direction]()[0]][guy.dExp[guy.direction]()[1]] == None:
					self.tutorial.append(self._keyButtonText(self._controllerType("xbox/x.png", "ps/square.png"), "x", "pick up"))
	
	def draw(self, surface, cMap):
		# draw both bits of text on either side of game surface
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