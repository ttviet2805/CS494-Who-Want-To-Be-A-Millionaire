import Const
import pygame
import TextClass
import ButtonClass
import TextButtonClass

class InGame:
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

		# Numplayers Text
		self.numsPlayer = 10
		self.numsPlayerText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Nums Players: {self.numsPlayer}", 
			(self.screenWidth // 60, self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Current Order Text
		self.currentOrder = 1
		self.currentOrderText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Current Order: {self.currentOrder}", 
			(self.screenWidth // 60, self.screenHeight // 100 + self.screenHeight // 30, self.screenWidth // 6, self.screenHeight // 30)
		)
	
		# My Order Text
		self.myOrder = 1
		self.myOrderText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Your Order: {self.myOrder}", 
			(self.screenWidth // 60, self.screenHeight // 100 + self.screenHeight // 15, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Nums Questions Text
		self.numsQuestions = 20
		self.numsQuestionsText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Nums Question: {self.numsQuestions}", 
			(5 * self.screenWidth // 6 - self.screenWidth // 60, self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Remaining Time Button
		self.remainTime = 40
		self.remainTimeText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Time: {self.remainTime}s", 
			(5 * self.screenWidth // 6 - self.screenWidth // 60, self.screenHeight // 30 + self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Question Text
		self.currentQuestionID = 1
		self.currentQuestionContent = "What is the capital of Vietnam?"
		self.currentQuestionText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 20, 
			f"Question {self.currentQuestionID} : {self.currentQuestionContent}", 
			(0, self.screenHeight // 6, self.screenWidth, self.screenHeight // 30)
		)

		# List Answers Button
		self.listAnswers = [
			"Tam Ky Quang Nam Da Nang Nghe An Thanh Pho Ho Chi Minh Ha Noi",
			"Da Nang Tran Tuan Viet Dang Trung Nghia Nguyen Dinh Tung",
			"Ho Chi Minh City",
			"Can Tho"
		]
		self.listAnswersButton = []
		x_position, y_position = 0, 5 * self.screenHeight // 12 
		for i in range(4):
			if i % 2 == 0:
				x_position = self.screenWidth // 12
			else:
				x_position = self.screenWidth // 2 + self.screenWidth // 12
			
			if (i == 2 or i == 3):
				y_position = 5 * self.screenHeight // 12 + self.screenHeight // 5 + self.screenHeight // 10
			else:
				y_position = 5 * self.screenHeight // 12
			
			self.listAnswersButton.append(TextButtonClass.TextButton(
				(self.screenWidth // 3, self.screenHeight // 5), 
				Const.ANSWER_BUTTON, 
				(x_position, y_position, self.screenWidth // 3, self.screenHeight // 5),
				self.listAnswers[i]
			))

		# Next Button
		self.clickedNextButton = False
		self.nextButton = ButtonClass.Button(
			(self.screenWidth // 10, self.screenHeight // 12), 
			Const.NEXT_BUTTON, 
			(9 * self.screenWidth // 10 - self.screenWidth // 100, self.screenHeight // 8, self.screenWidth // 10, self.screenHeight // 12)
		)

	def run(self):
		while self.running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break

			# Check if the answer buttons are clicked
			for i in range(4):
				if self.listAnswersButton[i].isClickedInGame(self.gameScreen):
					print(f"Answer {self.listAnswers[i]} is clicked")

			# Check if the next button is clicked
			nextButtonClick = self.nextButton.isClicked(self.gameScreen)
			if (nextButtonClick == True):
				self.clickedNextButton = True
			if (self.clickedNextButton == True):
				self.nextButton.imageID = 2

			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))
			self.numsPlayerText.drawLeftToRight(self.gameScreen)
			self.currentOrderText.drawLeftToRight(self.gameScreen)
			self.myOrderText.drawLeftToRight(self.gameScreen)
			self.numsQuestionsText.drawRightToLeft(self.gameScreen)
			self.remainTimeText.drawRightToLeft(self.gameScreen)
			self.currentQuestionText.draw(self.gameScreen)
			for i in range(4):
				self.listAnswersButton[i].drawInGame(self.gameScreen)
			self.nextButton.draw(self.gameScreen)

			pygame.display.update()
			
				