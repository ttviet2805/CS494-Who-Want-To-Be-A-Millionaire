import Const
import pygame
import TextClass
import ButtonClass
import TextButtonClass
import InGameClass
import WaitRoomClass
import protocol

class Menu:
	def __init__(self, screenSize):
		pygame.init()

		# Menu screen
		self.gameScreen = pygame.display.set_mode(screenSize)
		self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
		pygame.display.set_caption("Who want to be a Millionaire")
		pygame.display.flip()

		# Run
		self.running = True

		# Menu Background
		self.backgroundImage = pygame.transform.scale(Const.BACKGROUND, (self.screenWidth, self.screenHeight))

		# Enter User Name Text
		self.enterUserNameText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 15, 
			"Enter your name:", 
			(0, self.screenHeight/6, self.screenWidth, self.screenHeight // 10)
		)

		# Text Button Box
		self.enterUserNameButton = TextButtonClass.TextButton(
			(self.screenWidth // 2, self.screenHeight // 10), 
			Const.TEXT_BOX, 
			(0, self.screenHeight // 3, self.screenWidth, self.screenHeight // 10),
			""
		)

		# Register Button
		self.registerButton = ButtonClass.Button(
			(self.screenWidth // 4, self.screenHeight // 8), 
			Const.REGISTER_BUTTON, 
			(0, self.screenHeight // 2, self.screenWidth, self.screenHeight // 8)
		)	
		
		# Announcement
		self.announceRegister = TextClass.Text(
			Const.FONT, 
			Const.RED, 
			self.screenHeight // 20, 
			"", 
			(0, 3 * self.screenHeight // 4, self.screenWidth, self.screenHeight // 20)
		)

	def run(self, clientSocket):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break

			# Check if the register button is clicked
			isIngame = False
			if self.registerButton.isClicked(self.gameScreen):
				clientSocket.sendRequest("REQUEST", protocol.REG_NICKNAME_TYPE, self.enterUserNameButton.getText())
				responseState = clientSocket.receiveRequestForName()
				if responseState == True:
					self.announceRegister.changeTextContent(protocol.REG_COMPLETE_RESPONSE)
					isIngame = True
				elif responseState == False:
					self.announceRegister.changeTextContent(protocol.REG_EXIST_RESPONSE)

			if self.enterUserNameButton.isClicked(self.gameScreen):
				pass
				
			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))
			self.enterUserNameText.draw(self.gameScreen)
			self.enterUserNameButton.drawMenu(self.gameScreen)
			self.registerButton.draw(self.gameScreen)
			self.announceRegister.draw(self.gameScreen)
			pygame.display.update()

            # Test WaitingRoom
			waitRoom = WaitRoomClass.WaitRoom((self.screenWidth, self.screenHeight))
			waitRoom.run(clientSocket)

			if isIngame:
				pygame.time.delay(2000)
				inGame = InGameClass.InGame((self.screenWidth, self.screenHeight), self.enterUserNameButton.getText())
				inGame.run(clientSocket)
				break
			
				