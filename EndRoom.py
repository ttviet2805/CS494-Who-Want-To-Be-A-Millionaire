import Const
import pygame
import TextClass
import ButtonClass
import TextButtonClass
import WaitRoomClass

class EndRoom:
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

		# Waiting Room Title
		self.standingTitle = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 15, 
			"STANDING", 
			(0, self.screenHeight // 100, self.screenWidth, self.screenHeight // 10)
		)
		
		# Winner
		self.winnerButton = TextButtonClass.TextButton(
					(self.screenWidth // 3, self.screenHeight // 6), 
					Const.NAME_BUTTON, 
					(
						self.screenWidth // 3,
	   					self.screenHeight // 4,
						self.screenWidth // 3,
						self.screenHeight // 6
					),
					"Viet"
				)


		# Home Button
		self.quitButton = ButtonClass.Button(
			(self.screenWidth // 4, self.screenHeight // 8), 
			Const.HOME_BUTTON, 
			(0, 3 * self.screenHeight // 6, self.screenWidth, self.screenHeight // 8)
		)	

	def run(self, clientSocket, playerName, winnerName):
		self.winnerButton.changeTextContent(winnerName)
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break
				
			# Check if the start button is clicked
			if self.quitButton.isClicked(self.gameScreen):
				pygame.time.delay(1000)
				waitRoom = WaitRoomClass.WaitRoom((self.screenWidth, self.screenHeight))
				waitRoom.run(clientSocket, playerName)
				break

			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))
			self.standingTitle.draw(self.gameScreen)
			self.winnerButton.drawInGame(self.gameScreen)
			self.quitButton.draw(self.gameScreen)
			pygame.display.update()