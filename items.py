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
	visible = False
	select  = 0

	def __init__(self, cMap):
		self.size = (cMap.tileSize * 4, cMap.tileSize * 4)
		self.margin = int(cMap.tileSize / 8)
		self.font = pygame.font.Font("./assets/fonts/geopixel.ttf", 10)
		self.text = []

		self.sfx = {
			"click": pygame.mixer.Sound("./assets/sfx/click.mp3"),
		}
		self.sfxChannel = pygame.mixer.find_channel()
	
	def update(self, eventList):
		self.text = [self.font.render(f"{f.name} (${f.cost})", False, (191, 191, 191)) for f in FURNITURE]

		for event in eventList:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					self.visible = not self.visible
				
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
				
				if event.key == pygame.K_x:
					return self.select
			
			if event.type == pygame.JOYBUTTONDOWN:
				if event.button == 1:
					self.visible = not self.visible
				
				if event.button == 0:
					return self.select
			
			if event.type == pygame.JOYHATMOTION:
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
		
		self.text[self.select] = self.font.render(f"{FURNITURE[self.select].name} (${FURNITURE[self.select].cost})", False, (255, 255, 255))
		return -1

	def draw(self, surface):
		pygame.draw.rect(surface, (19, 126, 166), pygame.Rect(self.margin, self.margin, self.size[0] - (self.margin * 2), self.size[1] - (self.margin * 2)), 0, self.margin)

		for x in range(0, len(self.text)):
			surface.blit(self.text[x], (self.margin * 2, (self.margin * 2) + sum(f.get_rect().h + (self.margin / 2) for f in self.text[:x])))