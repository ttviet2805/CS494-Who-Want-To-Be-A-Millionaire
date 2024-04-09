import Const
import pygame
import TextClass
import ButtonClass
import TextButtonClass
import protocol

class InGame:
	def __init__(self, screenSize, playerName):
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

		# Player's name
		self.playerName = playerName

		# Numplayers Text
		self.numsPlayer = 10
		self.numsPlayerText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Number of Players: {self.numsPlayer}", 
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
			Const.RED, 
			self.screenHeight // 30, 
			f"Your Order: {self.myOrder}", 
			(self.screenWidth // 60, self.screenHeight // 100 + self.screenHeight // 15, self.screenWidth // 6, self.screenHeight // 30)
		)
		
		# Your Name Text
		self.myNameText = TextClass.Text(
			Const.FONT, 
			Const.RED, 
			self.screenHeight // 25, 
			f"Your Name: {self.playerName}", 
			(0, self.screenHeight // 100, self.screenWidth, self.screenHeight // 25)
		)
	
		# Nums Questions Text
		self.numsQuestions = 20
		self.numsQuestionsText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Number of Question: {self.numsQuestions}", 
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
		self.currentQuestionID = 0
		self.currentQuestionContent = ""
		self.currentQuestionText = TextButtonClass.TextButton(
			(5 * self.screenWidth // 7, self.screenHeight // 5), 
			Const.QUESTION_BUTTON, 
			(self.screenWidth // 7, self.screenHeight // 6, 5 * self.screenWidth // 7, self.screenHeight // 5),
			f"Question {self.currentQuestionID} : {self.currentQuestionContent}", 
		)

		# List Answers Button
		self.listAnswers = [
			"A",
			"B",
			"C",
			"D"
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

	def run(self, clientSocket):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break

			if self.currentQuestionID == 0:
				self.currentQuestionID += 1
				self.updateQuestion(clientSocket)

			# Check if the answer buttons are clicked
			isAnswer = False
			for i in range(4):
				if self.listAnswersButton[i].isClickedInGame(self.gameScreen):
					answerData = {
						"nickname": self.playerName,
						"answer": i
					}
					clientSocket.sendRequest("REQUEST", protocol.ANSWER_TYPE, answerData)
					responseData = clientSocket.receiveRequestForAnswer()
					if responseData == True:
						self.listAnswersButton[i].setStatus('correct')
					else:
						self.listAnswersButton[i].setStatus('wrong')
					print(f"Answer {self.listAnswers[i]} is clicked")
					isAnswer = True

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
			self.myNameText.draw(self.gameScreen)
			self.numsQuestionsText.drawRightToLeft(self.gameScreen)
			self.remainTimeText.drawRightToLeft(self.gameScreen)
			self.currentQuestionText.drawInGame(self.gameScreen)
			for i in range(4):
				self.listAnswersButton[i].drawInGame(self.gameScreen)
			self.nextButton.draw(self.gameScreen)
			pygame.display.update()

			if isAnswer == True:
				pygame.time.delay(2000)
				self.currentQuestionID += 1
				self.updateQuestion(clientSocket)

	def updateQuestion(self, clientSocket):
		clientSocket.sendRequest("REQUEST", protocol.QUESTION_TYPE, self.playerName)
		responseData = clientSocket.receiveRequestForQuestion()

		self.numsPlayer = responseData["num_players"]
		self.currentOrder = responseData["current_order"]
		self.myOrder = responseData["your_order"]
		self.numsQuestions = responseData["num_questions"]
		self.remainTime = responseData["time"]
		self.currentQuestionID = responseData["current_question"]
		self.currentQuestionContent = responseData["question"]["question"]
		self.listAnswers = responseData["question"]["answer"]

		self.numsPlayerText.changeTextContent(f"Number of Players: {self.numsPlayer}")
		self.currentOrderText.changeTextContent(f"Current Order: {self.currentOrder}")
		self.myOrderText.changeTextContent(f"Your Order: {self.myOrder}")
		self.myNameText.changeTextContent(f"Name: {self.playerName}")
		self.numsQuestionsText.changeTextContent(f"Number of Question: {self.numsQuestions}")
		self.remainTimeText.changeTextContent(f"Time: {self.remainTime}")
		self.currentQuestionText.changeTextContent(f"Question {self.currentQuestionID}: {self.currentQuestionContent}")
		for i in range(len(self.listAnswersButton)):
			self.listAnswersButton[i].changeTextContent(self.listAnswers[i])
				