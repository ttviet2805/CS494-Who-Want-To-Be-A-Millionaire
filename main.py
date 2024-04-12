import MenuClass
import pygame
import sys
import client
import protocol
import socket

def get_router_ip():
    try:
        # Connect to a public DNS server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        router_ip = s.getsockname()[0]
        s.close()
        return router_ip
    except Exception as e:
        print("Error occurred:", e)
        return None

def main():
    for arg in sys.argv[1:]:
        print("Argument:", arg)
    
    serverIP = "localhost"
    port = 2828
    if(len(sys.argv) >= 2):
        serverIP = sys.argv[1]
    if(len(sys.argv) >= 3):
        port = int(sys.argv[2])
    
    if serverIP.lower() == 'lan':
        serverIP = get_router_ip()
        print("LAN IP:", serverIP)

    clientSocket = client.ClientSocket()
    clientSocket.clientConnectToServer(serverIP, port)

    # Init
    pygame.init()
    infoObject = pygame.display.Info()
    screenProportion = 3 / 4

    menuGame = MenuClass.Menu((infoObject.current_w * screenProportion, infoObject.current_h * screenProportion))
    menuGame.run(clientSocket)

    clientSocket.sendRequest("REQUEST", protocol.CLOSE_TYPE, "")
    clientSocket.closeClient()

if __name__ == "__main__":
    main()