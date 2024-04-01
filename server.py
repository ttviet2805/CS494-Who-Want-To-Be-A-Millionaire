import socket

class ServerSocket:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def runServer(self, _serverIP, _port):
        serverIP = _serverIP
        port = _port

        self.server.bind((serverIP, port))
        self.server.listen(0)
        print(f"Listening on {serverIP}:{port}")

        clientSocket, clientAddress = self.server.accept()
        print(f"Accepted connection from {clientAddress[0]}:{clientAddress[1]}")

        while True:
            request = clientSocket.recv(1024)
            request = request.decode()

            if request.lower() == "close":
                clientSocket.send("closed".encode())
                break

            print(f"Received: {request}")
            response = f"accepted {request}".encode()
            clientSocket.send(response)

        clientSocket.close()
        print("Connection to client closed")
        self.server.close()

serverSocket = ServerSocket()
serverSocket.runServer("localhost", 2828)