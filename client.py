import socket
import selectors
import json
import protocol

def readJson(content):
	cnt = 0
	curString = ''
	res = []
	for c in content:
		curString = curString + c
		# print("# ", c)
		if c == '{':
			cnt += 1
		if c == '}':
			cnt -= 1
			if cnt == 0:
				res.append(curString)
				curString = ''

	return res

class ClientSocket:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySel = selectors.DefaultSelector()

        self.responses = {}

    def clientConnectToServer(self, serverIP, port):
        print("Client connect to server")
        self.client.connect((serverIP, port))
        self.client.setblocking(False)
        self.mySel.register(self.client, selectors.EVENT_READ,)

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

    def isReceiveResponse(self):
        for key, mask in self.mySel.select(timeout=0):
            if mask & selectors.EVENT_READ:
                message = self.client.recv(1024)
                message = message.decode()
                if message == "":
                    continue
                print("MES: ", message)
                responses = readJson(message)
                for responseJson in responses: 
                    response = json.loads(responseJson)
                    self.receiveResponse(response, protocol.REG_NICKNAME_TYPE)
                    self.receiveResponse(response, protocol.WAITING_ROOM_TYPE)
                    self.receiveResponse(response, protocol.START_GAME_TYPE)
                    self.receiveResponse(response, protocol.QUESTION_TYPE)
                    self.receiveResponse(response, protocol.RAISE_QUESTION_TYPE)
                    self.receiveResponse(response, protocol.ANSWER_TYPE)
                    self.receiveResponse(response, protocol.DISQUALIFIED_TYPE)
                    self.receiveResponse(response, protocol.WINNER_TYPE)
                    self.receiveResponse(response, protocol.CLOSE_TYPE)
    
    def closeClient(self):
        print("Client connect to server closed")
        self.client.close()
        self.mySel.close()

    def sendRequest(self, protocol, request_type, data):
        request = {
            "protocol": protocol,
            "type": request_type,
            "data": data
        }
        self.client.sendall(json.dumps(request, indent=2).encode()) 
    
    def receiveResponse(self, response, protocolType):
        if response.get("type") is None or response.get("protocol") is None:
            return None
        if response.get("protocol") != "RESPONSE" or response["type"] != protocolType:
            return None
        print(response)
        data = response["data"]
        if self.responses.get(protocolType) == None:
            self.responses[protocolType] = []
        self.responses[protocolType].append(data)

    def receiveUIResponse(self, protocolType):
        if self.responses.get(protocolType) == None:
            return None
        if len(self.responses.get(protocolType)) == 0:
            return None
        val = self.responses[protocolType].pop(0)
        return val
    
# import sys

# def main():
#     for arg in sys.argv[1:]:
#         print("Argument:", arg)
    
#     serverIP = "localhost"
#     port = 2828
#     print(serverIP, port)
#     if(len(sys.argv) >= 2):
#         serverIP = sys.argv[1]
#     if(len(sys.argv) >= 3):
#         port = int(sys.argv[2])
    
#     clientSocket = ClientSocket()
#     clientSocket.runClientForNonBlockingSocket(serverIP, port)

# if __name__ == "__main__":
#     main()  