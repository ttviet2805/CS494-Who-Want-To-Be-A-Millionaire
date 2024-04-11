import socket
import selectors
import json
import protocol
import database
import random

class ServerSocket:
    def __init__(self):
        self.mySel = selectors.DefaultSelector()
        self.numClients = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

        # Waiting Room
        self.nickNames = []

        # In game
        self.currentPlayers = []
        self.currentPlayerIndex = 0
        self.questions = database.questions
        random.shuffle(self.questions)
        self.curQuestion = 0
    
    def runServer(self, serverIP, port):
        self.server.bind((serverIP, port))
        self.server.listen(0)
        print(f"Listening on {serverIP}:{port}")

        clientSocket, clientAddress = self.server.accept()
        print(f"Accepted connection from {clientAddress[0]}:{clientAddress[1]}")

        while True:
            request = clientSocket.recv(1024).decode()

            if self.receiveRequestForClose(clientSocket, request) == True:
                break

            self.receiveRequestForName(clientSocket, request)
            self.receiveRequestForWaitingRoom(clientSocket, request)
            self.receiveRequestForQuestion(clientSocket, request)
            self.receiveRequestForAnswer(clientSocket, request)

        clientSocket.close()
        print("Connection to client closed")
        self.server.close()

    def runServerForNonBlockingSocket(self, serverIP, port):
        self.server.setblocking(False)
        self.server.bind((serverIP, port))
        self.server.listen()
        print(f"Server Listening on {serverIP}:{port}")

        self.mySel.register(self.server, selectors.EVENT_READ, self.accept)

        while self.numClients == None or self.numClients > 0:
            for key, mask in self.mySel.select(timeout=1):
                callback = key.data
                callback(key.fileobj, mask)

        print("Server connection closed")
        self.mySel.close()
        self.server.close()

    def accept(self, sock, mask):
        new_connection, addr = sock.accept()
        if self.numClients == None:
            self.numClients = 1
        else:
            self.numClients += 1
        print('Server Accept({})'.format(addr))
        new_connection.setblocking(False)
        self.mySel.register(new_connection, selectors.EVENT_READ, self.read)
        self.clients.append(new_connection)

    def read(self, clientSocket, mask):
        client_address = clientSocket.getpeername()
        print('Read({})'.format(client_address))
        request = clientSocket.recv(1024).decode()

        if self.receiveRequestForClose(clientSocket, request) == True:
            for name in self.nickNames:
                if name[1] == clientSocket:
                    for player in self.currentPlayers:
                        if player[0] == name[0]:
                            self.currentPlayers.remove(player)
                    self.nickNames.remove(name)
            self.mySel.unregister(clientSocket)
            self.clients.remove(clientSocket)
            clientSocket.close()
            self.numClients -= 1

        self.receiveRequestForName(clientSocket, request)
        self.receiveRequestForWaitingRoom(clientSocket, request)
        self.receiveRequestForStartGame(clientSocket, request)
        self.receiveRequestForQuestion(clientSocket, request)
        self.receiveRequestForRaiseQuestion(clientSocket, request)
        self.receiveRequestForAnswer(clientSocket, request)

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
            self.nickNames.append((request["data"], clientSocket))
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
            if i[0] == curStr:
                return False
        return True
    
    def receiveRequestForWaitingRoom(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.WAITING_ROOM_TYPE:
            return
        print("Server Received: ", request["data"])
        nameList = [i[0] for i in self.nickNames]
        for index, name in enumerate(self.nickNames):
            waitingRoomJson = {
                "protocol": "RESPONSE", 
                "type": protocol.WAITING_ROOM_TYPE,
                "data": {
                    "nickname": name[0],
                    "list_nicknames": nameList,
                    "order": index
                }
            }
            client = name[1]
            client.send(json.dumps(waitingRoomJson, indent=2).encode())

    def receiveRequestForStartGame(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.START_GAME_TYPE:
            return
        print("Server Received: ", request["data"])
        for index, name in enumerate(self.nickNames):
            startGameJson = {
                "protocol": "RESPONSE", 
                "type": protocol.START_GAME_TYPE,
                "data": {
                    'nickname': request["data"],
                }
            }
            client = name[1]
            client.send(json.dumps(startGameJson, indent=2).encode())
            self.currentPlayers.append((name[0], index))

    def receiveRequestForQuestion(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.QUESTION_TYPE:
            return
        print("Server Received: ", request["data"])
        nickname = request["data"]
        questionJson = {
            "protocol": "RESPONSE",
            "type": protocol.QUESTION_TYPE,
            "data": {
                "nickname": nickname,
                "num_players": len(self.nickNames),
                "current_order": f'#{self.currentPlayers[self.currentPlayerIndex][1]} - {self.currentPlayers[self.currentPlayerIndex][0]}',
                "your_order": f'#{self.getNicknameOrder(nickname)} - {nickname}',
                "num_questions": len(self.questions),
                "time": 40,
                "current_question": self.curQuestion,
                "question": {
                    "question": self.questions[self.curQuestion]["question"],
                    "answer": self.questions[self.curQuestion]["answer"]
                }
            }
        }
        clientSocket.send(json.dumps(questionJson, indent=2).encode())

    def receiveRequestForRaiseQuestion(self, clientSocket, message):
        request = json.loads(message)
        if request.get("type") is None or request.get("protocol") is None:
            return
        if request.get("protocol") != "REQUEST" or request["type"] != protocol.RAISE_QUESTION_TYPE:
            return
        print("Server Received: ", request["data"])
        self.curQuestion += 1
        self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.currentPlayers)
        for name in self.nickNames:
            questionJson = {
                "protocol": "RESPONSE",
                "type": protocol.QUESTION_TYPE,
                "data": {
                    "nickname": name[0],
                    "num_players": len(self.nickNames),
                    "current_order": f'#{self.currentPlayers[self.currentPlayerIndex][1]} - {self.currentPlayers[self.currentPlayerIndex][0]}',
                    "your_order": f'#{self.getNicknameOrder(name[0])} - {name[0]}',
                    "num_questions": len(self.questions),
                    "time": 40,
                    "current_question": self.curQuestion,
                    "question": {
                        "question": self.questions[self.curQuestion]["question"],
                        "answer": self.questions[self.curQuestion]["answer"]
                    }
                }
            }
            client = name[1]
            client.send(json.dumps(questionJson, indent=2).encode())
    
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
            "data": {
                "answer": request["data"]["answer"],
                "correct_answer": self.questions[self.curQuestion]["correct_answer"]
            }
        }
        for name in self.nickNames:
            client = name[1]
            client.send(json.dumps(answerJson, indent=2).encode())

    def getNicknameOrder(self, nickname):
        for index, name in enumerate(self.nickNames):
            if name[0] == nickname:
                return index
        return -1

import sys

def main():
    for arg in sys.argv[1:]:
        print("Argument:", arg)
    
    serverIP = "localhost"
    port = 2828
    print(serverIP, port)
    if(len(sys.argv) >= 2):
        serverIP = sys.argv[1]
    if(len(sys.argv) >= 3):
        port = int(sys.argv[2])
    
    serverSocket = ServerSocket()
    serverSocket.runServerForNonBlockingSocket(serverIP, port)

if __name__ == "__main__":
    main()  