from socket import *
import json 

serverName = 'localhost'
serverPort= 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
	message = input('Allow server to start timing:') #This is quivalent to hit start on timing element to start drawing 
	clientSocket.sendto(message.encode(), (serverName, serverPort))





	for i in range(180):
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		print(modifiedMessage.decode())
	clientSocket.close()
