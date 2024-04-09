import pygame
import Const
import TextClass

class TextButton:
	def __init__(self, buttonSize, buttonImage, containerInfo, inputStr):
		self.size = (buttonSize[0], buttonSize[1])
		self.imageID = 0
		self.image = [pygame.transform.scale(buttonImage[i], self.size) for i in range(len(buttonImage))]
		self.rect = self.image[0].get_rect()
		self.coord = (containerInfo[0] + (containerInfo[2] - self.size[0]) / 2, containerInfo[1] + (containerInfo[3] - self.size[1]) / 2)
		self.rect.topleft = self.coord
		self.inputStr = inputStr
		self.text = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.size[1] // 2 if inputStr == "" else self.size[1] // 4,  
			self.inputStr, 
			(containerInfo[0], containerInfo[1], containerInfo[2], containerInfo[3])
		)
		self.containerInfo = containerInfo
		# print(inputStr, containerInfo[0], containerInfo[1], containerInfo[2], containerInfo[3])
		self.clicked = False
		self.wrapTextList = self.wrapText(self.inputStr)

	def wrapText(self, curStr):
		# Wrap text
		words = curStr.split()
		textFont = pygame.font.Font(Const.FONT, self.size[1] // 4)
		wordWidth, wordHeight = 0, 0
		currentWidth = 0
		wrapTextContent = ""
		wrapTextList = []
		for i in range(0, len(words)):
			wordWidth = textFont.size(words[i])[0] + textFont.size(" ")[0]
			wordHeight = textFont.size(words[i])[1]
			if (currentWidth + wordWidth < self.size[0] - self.size[0] / 10):
				currentWidth += wordWidth
			else:
				wrapTextList.append(
					TextClass.Text(
						Const.FONT, 
						Const.WHITE, 
						self.size[1] // 2 if curStr == "" else self.size[1] // 4,  
						wrapTextContent, 
						(self.containerInfo[0] + (self.containerInfo[2] - self.size[0]) / 2, self.containerInfo[1], self.size[0], self.size[1])
					)
				)
				currentWidth = 0
				wrapTextContent = ""
			wrapTextContent += words[i] + " "
		
		if (wrapTextContent != ""):
			wrapTextList.append(
				TextClass.Text(
					Const.FONT, 
					Const.WHITE, 
					self.size[1] // 2 if curStr == "" else self.size[1] // 4,  
					wrapTextContent, 
					(self.containerInfo[0] + (self.containerInfo[2] - self.size[0]) / 2, self.containerInfo[1], self.size[0], self.size[1])
				)
			)
		paddingFromTop = (self.size[1] - len(wrapTextList) * wordHeight - self.size[1] // 20) // 2
		for i in range(len(wrapTextList)):
			wrapTextList[i].changeContainerInfo(
				(
					self.containerInfo[0], 
					self.containerInfo[1] + paddingFromTop + i * wordHeight, 
					self.size[0], 
					wordHeight
				)
			)
		return wrapTextList

	def getText(self):
		return self.inputStr

	def drawMenu(self, gameScreen):
		gameScreen.blit(self.image[self.imageID], (self.rect.x , self.rect.y))
		self.text.draw(gameScreen)

	def drawInGame(self, gameScreen):
		if (len(self.buttonImage) >= 1):
			gameScreen.blit(self.image[self.imageID], (self.rect.x , self.rect.y))
		
		wrapTextListLen = len(self.wrapTextList)
		for i in range(wrapTextListLen):
			# print("Ve ", i, self.wrapTextList[i].containerInfo[0], self.wrapTextList[i].containerInfo[1], self.wrapTextList[i].containerInfo[2], self.wrapTextList[i].containerInfo[3])
			self.wrapTextList[i].draw(gameScreen)

	def changeTextContent(self, newContent):
		self.text.changeTextContent(newContent)
		self.wrapTextList = self.wrapText(newContent)

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
			self.drawMenu(gameScreen)
							
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
				# print(self.inputStr)
		if(pygame.mouse.get_pressed()[0] == 0): 
			self.clicked = False 
		return action 
	
	def isClickedInGame(self, gameScreen):
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
	
	def setStatus(self, answer):
		if answer == 'correct':
			self.imageID = 2
		if answer == 'wrong':
			self.imageID = 3
