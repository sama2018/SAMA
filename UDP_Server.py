from socket import *
from _thread import *
import json
import time 
import sys

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")



list = []

while True:

		message, clientAddress = serverSocket.recvfrom(2048)
		modifiedMessage = message.decode()

		
		
		for i in range(180):
			
			if modifiedMessage == 'yes':

				data = json.dumps(i)

			
				serverSocket.sendto(data.encode(), clientAddress)
				#start_new_thread(clientAddress ).start()

			if i == 90:
				sys.stdout.flush()
			time.sleep(1)
		

			


    



