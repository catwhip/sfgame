# imports
from constants import *

class Item():
	def __init__(self, name, image, level, stats, cost):
		self.name = name
		self.level = level
		self.stats = stats
		self.cost = cost

		self.image = pygame.image.load(image)
	
	def draw(self, surface, pos, size):
		surface.blit(pygame.transform.scale(self.image, size), pos)

# all furniture
FURNITURE = (
	Item(
		"bookcase", # name
		"./assets/sprites/furniture/bookcase.png", # image
		1, # level (1 = not passable)
		{"comfort": 2, "entertainment": 10,}, # stat points
		150, # cost
	),

	Item(
		"rug",
		"./assets/sprites/furniture/rug.png",
		0,
		{"comfort": 10,},
		80,
	),
)

class ItemMenu:
	# tha player's item menu
	visible = False
	select  = 0

	def __init__(self, cMap):
		self.size = (cMap.tileSize * 4, cMap.tileSize * 4)
		self.margin = int(cMap.tileSize / 8)
		self.font = pygame.font.Font("./assets/fonts/geopixel.ttf", 10)
		self.text = []
		self.iText = None

		# sfx stuff
		self.sfx = {
			"click": pygame.mixer.Sound("./assets/sfx/click.mp3"),
		}
		self.sfxChannel = pygame.mixer.find_channel()
	
	def update(self, eventList, guy):
		self.text = [self.font.render(f"{f.name} (${f.cost})", False, (191, 191, 191)) for f in FURNITURE]

		for event in eventList:
			if event.type == pygame.KEYDOWN or pygame.JOYBUTTONDOWN:
				if controlEqual(event, pygame.K_x, 0):
					return self.select
				
				if controlEqual(event, pygame.K_z, 2):
					if self.select in guy.inventory and guy.inventory[self.select] > 0:
						guy.inventory[self.select] -= 1
						guy.cash += FURNITURE[self.select].cost
				
				if controlEqual(event, pygame.K_c, 1):
					self.visible = not self.visible
			
			if event.type == pygame.KEYDOWN:
				# movement (this has to be in a different place to the buttons because joyhatmotion needs to be used, not joybuttondown)
				if event.key == pygame.K_UP:
					self.select -= 1
					self.sfxChannel.play(self.sfx["click"])

					if self.select < 0:
						self.select = len(self.text) - 1

				if event.key == pygame.K_DOWN:
					self.select += 1
					self.sfxChannel.play(self.sfx["click"])

					if self.select > len(self.text) - 1:
						self.select = 0
			
			if event.type == pygame.JOYHATMOTION:
				# movement
				if event.value[1] == -1:
					self.select -= 1
					self.sfxChannel.play(self.sfx["click"])

					if self.select < 0:
						self.select = len(self.text) - 1
				
				if event.value[1] == 1:
					self.select += 1
					self.sfxChannel.play(self.sfx["click"])

					if self.select > len(self.text) - 1:
						self.select = 0
		
		# render white text for selected object
		self.text[self.select] = self.font.render(f"{FURNITURE[self.select].name} (${FURNITURE[self.select].cost})", False, (255, 255, 255))
		
		# lil number in the corner that shows how much u have
		self.iText = None
		if self.select in guy.inventory and guy.inventory[self.select] > 0:
			self.iText = self.font.render(str(guy.inventory[self.select]), False, (255, 255, 255))
		
		return None

	def draw(self, surface):
		pygame.draw.rect(surface, (19, 126, 166), pygame.Rect(self.margin, self.margin, self.size[0] - (self.margin * 2), self.size[1] - (self.margin * 2)), 0, self.margin)

		for x in range(0, len(self.text)):
			surface.blit(self.text[x], (self.margin * 2, (self.margin * 2) + sum(f.get_rect().h + (self.margin / 2) for f in self.text[:x])))
			if not self.iText == None and x == self.select:
				surface.blit(self.iText, (self.size[0] - (self.margin * 2) - (self.iText.get_width()), (self.margin * 2) + sum(f.get_rect().h + (self.margin / 2) for f in self.text[:x])))