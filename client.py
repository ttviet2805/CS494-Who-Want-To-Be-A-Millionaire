import socket

class ClientSocket:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
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

clientSocket = ClientSocket()
clientSocket.runClient("localhost", 2828)