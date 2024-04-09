import socket
import json
import protocol

class ClientSocket:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectSocket(self, serverIP, port):
        print("Client connect to server")
        self.client.connect((serverIP, port))

    # def sendRequest(self, _message):
    #     message = _message
    #     self.client.send(message.encode())

    def receiveResponse(self):
        response = self.client.recv(1024)
        response = response.decode()
        return response
    
    def closeConnection(self):
        print("Connection to server closed")
        self.client.close()

    def runClient(self, _serverIP, _port):
        serverIP = _serverIP
        port = _port

        self.client.connect((serverIP, port))

        while True:
            message = input("Enter message: ")
            self.client.send(message.encode())

            response = self.client.recv(1024)
            response = response.decode()

            if response.lower() == "closed":
                break
            print(f"Received: {response}")
        
        self.client.close()
        print("Connection to server closed")

    def sendRequest(self, protocol, request_type, data):
        request = {
            "protocol": protocol,
            "type": request_type,
            "data": data
        }
        self.client.sendall(json.dumps(request, indent=2).encode()) 
    
    def receiveRequestForName(self):
        message = self.client.recv(1024)
        message = message.decode()
        response = json.loads(message)
        print(response)
        if response.get("type") is None or response.get("protocol") is None:
            return None
        if response.get("protocol") != "RESPONSE" or response["type"] != protocol.REG_NICKNAME_TYPE:
            return None
        data = response["data"]
        return (data == protocol.REG_COMPLETE_RESPONSE)
    
    def receiveRequestForWaitingRoom(self):
        message = self.client.recv(1024)
        message = message.decode()
        response = json.loads(message)
        print(response)
        if response.get("type") is None or response.get("protocol") is None:
            return None
        if response.get("protocol") != "RESPONSE" or response["type"] != protocol.WAITING_ROOM_TYPE:
            return None
        data = response["data"]
        return data
    
    def receiveRequestForQuestion(self):
        message = self.client.recv(1024)
        message = message.decode()
        response = json.loads(message)
        print(response)
        if response.get("type") is None or response.get("protocol") is None:
            return None
        if response.get("protocol") != "RESPONSE" or response["type"] != protocol.QUESTION_TYPE:
            return None
        data = response["data"]
        return data

    def receiveRequestForAnswer(self):
        message = self.client.recv(1024)
        message = message.decode()
        response = json.loads(message)
        print(response)
        if response.get("type") is None or response.get("protocol") is None:
            return None
        if response.get("protocol") != "RESPONSE" or response["type"] != protocol.ANSWER_TYPE:
            return None
        data = response["data"]
        return data

# clientSocket = ClientSocket()
# clientSocket.runClient("10.124.4.169", 2828)