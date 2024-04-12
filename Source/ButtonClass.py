import pygame
import Const

class Button:
	def __init__(self, buttonSize, buttonImage, containerInfo):
		self.size = (buttonSize[0], buttonSize[1])
		self.imageID = 0
		self.image = [pygame.transform.scale(buttonImage[i], self.size) for i in range(len(buttonImage))]
		self.rect = self.image[self.imageID].get_rect()
		self.coord = (containerInfo[0] + (containerInfo[2] - self.size[0]) / 2, containerInfo[1] + (containerInfo[3] - self.size[1]) / 2)
		self.rect.topleft = self.coord
		self.clicked = False

	def draw(self, gameScreen):
		gameScreen.blit(self.image[self.imageID], (self.rect.x , self.rect.y))


	def isClicked(self, gameScreen): 
		action = False 

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			self.imageID = 1
			if(pygame.mouse.get_pressed()[0] == 1  and self.clicked == False):
				self.clicked = True
				action = True 
		else:
			self.imageID = 0
		if(pygame.mouse.get_pressed()[0] == 0): 
			self.clicked = False 
		return action 