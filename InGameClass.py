import Const
import pygame
import EndRoom
import TextClass
import ButtonClass
import TextButtonClass
import protocol

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
		self.currentOrder = None
		self.myOrder = None

		# Menu Background
		self.backgroundImage = pygame.transform.scale(Const.BACKGROUND, (self.screenWidth, self.screenHeight))

		# Numplayers Text
		self.numsPlayerText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Number of Players: 0", 
			(self.screenWidth // 60, self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Current Order Text
		self.currentOrderText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Current Order: 0", 
			(self.screenWidth // 60, self.screenHeight // 100 + self.screenHeight // 30, self.screenWidth // 6, self.screenHeight // 30)
		)
	
		# My Order Text
		self.myOrderText = TextClass.Text(
			Const.FONT, 
			Const.RED, 
			self.screenHeight // 30, 
			f"Your Order: 0", 
			(self.screenWidth // 60, self.screenHeight // 100 + self.screenHeight // 15, self.screenWidth // 6, self.screenHeight // 30)
		)
		
		# Your Name Text
		self.mode = "Player Mode"
		self.modeText = TextClass.Text(
			Const.FONT, 
			Const.RED, 
			self.screenHeight // 20, 
			self.mode, 
			(0, self.screenHeight // 100, self.screenWidth, self.screenHeight // 25)
		)
	
		# Nums Questions Text
		self.numsQuestionsText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Number of Question: 0", 
			(5 * self.screenWidth // 6 - self.screenWidth // 60, self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Remaining Time Button
		self.remainTimeText = TextClass.Text(
			Const.FONT, 
			Const.WHITE, 
			self.screenHeight // 30, 
			f"Time: 0s", 
			(5 * self.screenWidth // 6 - self.screenWidth // 60, self.screenHeight // 30 + self.screenHeight // 100, self.screenWidth // 6, self.screenHeight // 30)
		)

		# Question Text
		self.currentQuestionText = TextButtonClass.TextButton(
			(5 * self.screenWidth // 7, self.screenHeight // 5), 
			Const.QUESTION_BUTTON, 
			(self.screenWidth // 7, self.screenHeight // 6, 5 * self.screenWidth // 7, self.screenHeight // 5),
			f"Question 0 : 0", 
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

	def run(self, clientSocket, playerName):
		clientSocket.sendRequest("REQUEST", protocol.QUESTION_TYPE, playerName)

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break

			clientSocket.isReceiveResponse()

			# Check if the answer buttons are clicked
			if self.currentOrder == self.myOrder and self.mode == "Player Mode":
				for i in range(4):
					if self.listAnswersButton[i].isClickedInGame(self.gameScreen):
						answerData = {
							"nickname": playerName,
							"answer": i
						}
						clientSocket.sendRequest("REQUEST", protocol.ANSWER_TYPE, answerData)

			# Check if the next button is clicked
			if self.myOrder == self.currentOrder and self.mode == "Player Mode":
				nextButtonClick = self.nextButton.isClicked(self.gameScreen)
				if (nextButtonClick == True):
					self.clickedNextButton = True
				if (self.clickedNextButton == True):
					self.nextButton.imageID = 2

			clientSocket.isReceiveResponse()

			self.updateQuestion(clientSocket)
			isAnswer = self.updateAnswer(clientSocket)
			self.updateDisqualify(clientSocket)
			winnerResponse = clientSocket.receiveUIResponse(protocol.WINNER_TYPE)
			if winnerResponse != None:
				if winnerResponse['winner'] != None:
					endRoom = EndRoom.EndRoom((self.screenWidth, self.screenHeight))
					endRoom.run(clientSocket, winnerResponse['winner'])
					break

			# Draw Window
			self.gameScreen.blit(self.backgroundImage, (0, 0))
			self.numsPlayerText.drawLeftToRight(self.gameScreen)
			self.currentOrderText.drawLeftToRight(self.gameScreen)
			self.myOrderText.drawLeftToRight(self.gameScreen)
			self.modeText.draw(self.gameScreen)
			self.numsQuestionsText.drawRightToLeft(self.gameScreen)
			self.remainTimeText.drawRightToLeft(self.gameScreen)
			self.currentQuestionText.drawInGame(self.gameScreen)
			for i in range(4):
				self.listAnswersButton[i].drawInGame(self.gameScreen)
			self.nextButton.draw(self.gameScreen)
			pygame.display.update()

			if self.currentOrder == self.myOrder and isAnswer != None:
				pygame.time.delay(2000)
				clientSocket.sendRequest("REQUEST", protocol.RAISE_QUESTION_TYPE, playerName)
				clientSocket.isReceiveResponse()
				if isAnswer == False:
					pygame.time.delay(100)
					clientSocket.sendRequest("REQUEST", protocol.DISQUALIFIED_TYPE, playerName)
					clientSocket.isReceiveResponse()
				pygame.time.delay(500)
				clientSocket.sendRequest("REQUEST", protocol.WINNER_TYPE, playerName)
				clientSocket.isReceiveResponse()

	def updateQuestion(self, clientSocket):
		questionResponse = clientSocket.receiveUIResponse(protocol.QUESTION_TYPE)
		if questionResponse == None:
			return

		playerName = questionResponse["nickname"]
		numsPlayer = questionResponse["num_players"]
		currentOrder = questionResponse["current_order"]
		myOrder = questionResponse["your_order"]
		numsQuestions = questionResponse["num_questions"]
		remainTime = questionResponse["time"]
		currentQuestionID = questionResponse["current_question"]
		currentQuestionContent = questionResponse["question"]["question"]
		listAnswers = questionResponse["question"]["answer"]

		self.numsPlayerText.changeTextContent(f"Number of Players: {numsPlayer}")
		self.currentOrderText.changeTextContent(f"Current Order: {currentOrder}")
		self.myOrderText.changeTextContent(f"Your Order: {myOrder}")
		# self.myNameText.changeTextContent(f"Name: {playerName}")
		self.numsQuestionsText.changeTextContent(f"Number of Question: {numsQuestions}")
		self.remainTimeText.changeTextContent(f"Time: {remainTime}")
		self.currentQuestionText.changeTextContent(f"Question {currentQuestionID}: {currentQuestionContent}")
		for i in range(len(self.listAnswersButton)):
			self.listAnswersButton[i].setStatus('nothing')
			self.listAnswersButton[i].changeTextContent(listAnswers[i])

		self.currentOrder = currentOrder
		self.myOrder = myOrder
	
	def updateAnswer(self, clientSocket):
		answerResponse = clientSocket.receiveUIResponse(protocol.ANSWER_TYPE)
		if answerResponse == None:
			return None
		answer = answerResponse['answer']
		correct_answer = answerResponse['correct_answer']
		if answer != correct_answer:
			self.listAnswersButton[answer].setStatus('wrong')
		self.listAnswersButton[correct_answer].setStatus('correct')
		return answer == correct_answer
	
	def updateDisqualify(self, clientSocket):
		disqualifiedResponse = clientSocket.receiveUIResponse(protocol.DISQUALIFIED_TYPE)
		if disqualifiedResponse == None:
			return None
		if disqualifiedResponse == True:
			self.mode = "Supervisor Mode"
			self.modeText.changeTextContent(self.mode)
			for i in range(len(self.listAnswersButton)):
				self.listAnswersButton[i].setStatus('nothing')
