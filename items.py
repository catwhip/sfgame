from constants import *

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

class ItemMenu:
	visible = False
	margin  = 4
	select  = 0

	def __init__(self):
		self.font = pygame.font.Font("./assets/geopixel.ttf", 5)
		self.text = []
	
	def update(self, eventList):
		self.text = [self.font.render(f.name, False, (191, 191, 191)) for f in FURNITURE]

		for event in eventList:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					self.visible = not self.visible
				
				if event.key == pygame.K_UP:
					self.select -= 1

					if self.select < 0:
						self.select = len(self.text) - 1

				if event.key == pygame.K_DOWN:
					self.select += 1

					if self.select > len(self.text) - 1:
						self.select = 0
				
				if event.key == pygame.K_x:
					return self.select
		
		self.text[self.select] = self.font.render(FURNITURE[self.select].name, False, (255, 255, 255))
		return -1

	def draw(self, surface):
		pygame.draw.rect(surface, (19, 126, 166), pygame.Rect(self.margin, self.margin, 128 - (self.margin * 2), 128 - (self.margin * 2)), 0, 4)

		for x in range(0, len(self.text)):
			surface.blit(self.text[x], (self.margin * 2, (self.margin * 2) + sum(f.get_rect().h + (self.margin / 2) for f in self.text[:x])))