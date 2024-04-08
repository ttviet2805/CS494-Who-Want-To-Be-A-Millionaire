import socket
import json
import protocol
import database
import random

class ServerSocket:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickNames = []

        # In game
        self.questions = database.questions
        random.shuffle(self.questions)
        self.currentOrder = 0
        self.numsQuestions = len(self.questions)
        self.curQuestion = -1
    
    def runServer(self, serverIP, port):
        self.server.bind((serverIP, port))
        self.server.listen(0)
        print(f"Listening on {serverIP}:{port}")

        clientSocket, clientAddress = self.server.accept()
        print(f"Accepted connection from {clientAddress[0]}:{clientAddress[1]}")

        while True:
            request = clientSocket.recv(1024).decode()

            # print(f"Received: {request}")
            # response = f"accepted {request}".encode()
            # clientSocket.send(response)
            if self.receiveRequestForClose(clientSocket, request) == True:
                break

            self.receiveRequestForName(clientSocket, request)
            self.receiveRequestForQuestion(clientSocket, request)
            self.receiveRequestForAnswer(clientSocket, request)

        clientSocket.close()
        print("Connection to client closed")
        self.server.close()

    def receiveRequestForClose(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return False
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.CLOSE_TYPE:
            return False
        return True

    def receiveRequestForName(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.REG_NICKNAME_TYPE:
            return
        print("Server Received: ", request["data"])
        if self.checkNickName(request["data"]):
            self.nickNames.append(request["data"])
            regCompleteJson = {
                "protocol": "RESPONSE", 
                "type": protocol.REG_NICKNAME_TYPE,
                "data": protocol.REG_COMPLETE_RESPONSE
            }
            clientSocket.send(json.dumps(regCompleteJson, indent=2).encode())
        else:
            regExistJson = {
                "protocol": "RESPONSE", 
                "type": protocol.REG_NICKNAME_TYPE,
                "data": protocol.REG_EXIST_RESPONSE
            }
            clientSocket.send(json.dumps(regExistJson, indent=2).encode())

    def checkNickName(self, curStr):
        if len(curStr) == 0 or len(curStr) > 10:
            return False
        for i in curStr:
            if i.isdigit() or i.isalpha():
                pass
            else:
                return False
        for i in self.nickNames:
            if i == curStr:
                return False
        return True
    
    def receiveRequestForQuestion(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.QUESTION_TYPE:
            return
        print("Server Received: ", request["data"])
        self.curQuestion += 1
        questionJson = {
            "protocol": "RESPONSE",
            "type": protocol.QUESTION_TYPE,
            "data": {
                "nickname": request["data"],
                "num_players": len(self.nickNames),
                "current_order": 1,
                "your_order": 1,
                "num_questions": self.numsQuestions,
                "time": 40,
                "current_question": self.curQuestion,
                "question": self.questions[self.curQuestion]
            }
        }
        clientSocket.send(json.dumps(questionJson, indent=2).encode())
    
    def receiveRequestForAnswer(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.ANSWER_TYPE:
            return
        print("Server Received: ", request["data"])
        answerJson = {
            "protocol": "RESPONSE", 
            "type": protocol.ANSWER_TYPE,
            "data": (request["data"]["answer"] == self.questions[self.curQuestion]["correct_answer"])
        }
        clientSocket.send(json.dumps(answerJson, indent=2).encode())


import sys

def main():
    for arg in sys.argv[1:]:
        print("Argument:", arg)
    
    serverIP = "192.168.1.4"
    port = 2828
    print(serverIP, port)
    if(len(sys.argv) >= 2):
        serverIP = sys.argv[1]
    if(len(sys.argv) >= 3):
        port = int(sys.argv[2])
    
    serverSocket = ServerSocket()
    serverSocket.runServer(serverIP, port)

if __name__ == "__main__":
    main()