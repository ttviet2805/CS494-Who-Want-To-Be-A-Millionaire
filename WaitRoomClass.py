import Const
import pygame
import TextClass
import ButtonClass
import TextButtonClass
import InGameClass
import protocol

class WaitRoom:
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
		self.waitingRoomTitle = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 15, 
			"WAITING ROOM", 
			(0, self.screenHeight // 100, self.screenWidth, self.screenHeight // 10)
		)
		
		# List Players
		self.listPlayersButton = []
		# for i in range(10):
		# 	self.listPlayersButton.append(
		# 		TextButtonClass.TextButton(
		# 			(self.screenWidth // 6, self.screenHeight // 8), 
		# 			Const.NAME_BUTTON, 
		# 			(
		# 				(i % 4 + 1) * self.screenWidth // 15 + (i % 4) * self.screenWidth // 6,
	   	# 				(i // 4 + 1) * self.screenHeight // 6,
		# 				self.screenWidth // 6,
		# 				self.screenHeight // 8
		# 			),
		# 			"Viet"
		# 		)
		# 	)


		# Start Button
		self.startButton = ButtonClass.Button(
			(self.screenWidth // 4, self.screenHeight // 8), 
			Const.START_BUTTON, 
			(0, 4 * self.screenHeight // 5, self.screenWidth, self.screenHeight // 8)
		)	

	def run(self, clientSocket, playerName):
		clientSocket.sendRequest("REQUEST", protocol.WAITING_ROOM_TYPE, playerName)
		responseState = clientSocket.receiveRequestForWaitingRoom()
		for i in range(len(responseState)):
			self.listPlayersButton.append(
				TextButtonClass.TextButton(
					(self.screenWidth // 6, self.screenHeight // 8), 
					Const.NAME_BUTTON, 
					(
						(i % 4 + 1) * self.screenWidth // 15 + (i % 4) * self.screenWidth // 6,
	   					(i // 4 + 1) * self.screenHeight // 6,
						self.screenWidth // 6,
						self.screenHeight // 8
					),
					responseState[i]
				)
			)

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break
				
			# Check if the start button is clicked
			if self.startButton.isClicked(self.gameScreen):
				inGame = InGameClass.InGame((self.screenWidth, self.screenHeight), playerName)
				inGame.run(clientSocket)
				print("Start Button Clicked")
				break

			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))
			self.waitingRoomTitle.draw(self.gameScreen)
			self.startButton.draw(self.gameScreen)
			for i in range(len(self.listPlayersButton)):
				self.listPlayersButton[i].drawMenu(self.gameScreen)
			pygame.display.update()