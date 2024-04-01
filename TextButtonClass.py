import pygame
import Const
import TextClass

class TextButton:
	def __init__(self, buttonSize, buttonImage, containerInfo):
		self.size = (buttonSize[0], buttonSize[1])
		self.imageID = 0
		self.image = [pygame.transform.scale(buttonImage[i], self.size) for i in range(len(buttonImage))]
		self.rect = self.image[0].get_rect()
		self.coord = (containerInfo[0] + (containerInfo[2] - self.size[0]) / 2, containerInfo[1] + (containerInfo[3] - self.size[1]) / 2)
		self.rect.topleft = self.coord
		self.inputStr = ""
		self.text = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.size[1] // 2, 
			self.inputStr, 
			(containerInfo[0], containerInfo[1], containerInfo[2], containerInfo[3])
		)
		self.clicked = False

	def draw(self, gameScreen):
		gameScreen.blit(self.image[self.imageID], (self.rect.x , self.rect.y))
		self.text.draw(gameScreen)

	def changeTextContent(self, newContent):
		self.text.changeTextContent(newContent)

	def handle_event(self, gameScreen):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key in range(32, 127):
						if len(self.inputStr) < 10:
							self.inputStr += event.unicode
							self.changeTextContent(self.inputStr)
					elif event.key == pygame.K_RETURN:
						return
					elif event.key == pygame.K_BACKSPACE:
						if len(self.inputStr) > 0:
							self.inputStr = self.inputStr[:-1]
							self.changeTextContent(self.inputStr)
			pygame.display.update()
			self.draw(gameScreen)
							
	def isClicked(self, gameScreen): 
		action = False 

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos) :
			if(pygame.mouse.get_pressed()[0] == 1  and self.clicked == False):
				self.clicked = True
				action = True
				self.imageID = 1 - self.imageID 
				self.handle_event(gameScreen)
				self.imageID = 1 - self.imageID
				print(self.inputStr)
		if(pygame.mouse.get_pressed()[0] == 0): 
			self.clicked = False 
		return action 