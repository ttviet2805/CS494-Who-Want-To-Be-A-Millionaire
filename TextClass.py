import pygame
import Const

class Text:
	def __init__(self, textFont, textColor, textSize, textContent, containerInfo):
		self.textFont = pygame.font.Font(textFont, textSize)
		self.textColor = textColor
		self.text = self.textFont.render(textContent, True, textColor)
		self.containerInfo = containerInfo
		textHeight = self.textFont.size(textContent)[1]
		textWidth = self.textFont.size(textContent)[0]
		self.textCoord = (containerInfo[0] + (containerInfo[2] - textWidth) / 2, containerInfo[1] + (containerInfo[3] - textHeight) / 2)
		self.leftToRightTextCoord = (containerInfo[0], containerInfo[1] + (containerInfo[3] - textHeight) / 2)
		self.bottomRightTextCoord = (containerInfo[0] + containerInfo[2] - textWidth - containerInfo[2] / 10, containerInfo[1] + containerInfo[3] - textHeight - containerInfo[3] / 10)
		self.upLeftTextCoord = (containerInfo[0] + containerInfo[2] / 10, containerInfo[1] + containerInfo[3] / 20)

	def changeTextContent(self, newContent):
		self.text = self.textFont.render(newContent, True, self.textColor)
		textHeight = self.textFont.size(newContent)[1]
		textWidth = self.textFont.size(newContent)[0]
		self.textCoord = (self.containerInfo[0] + (self.containerInfo[2] - textWidth) / 2, self.containerInfo[1] + (self.containerInfo[3] - textHeight) / 2)
		self.leftToRightTextCoord = (self.containerInfo[0], self.containerInfo[1] + (self.containerInfo[3] - textHeight) / 2)

	def draw(self, gameScreen):
		gameScreen.blit(self.text, self.textCoord)

	def drawLeftToRight(self, gameScreen):
		gameScreen.blit(self.text, self.leftToRightTextCoord)

	def drawBottomRight(self, gameScreen):
		gameScreen.blit(self.text, self.bottomRightTextCoord)

	def drawUpLeft(self, gameScreen):
		gameScreen.blit(self.text, self.upLeftTextCoord)