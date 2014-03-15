#Programmer : Rahul Singhal
#client

# a client is always listening on a udp port for the incoming connections
from socket import *
from subprocess import *

serverIp = gethostbyname("%s.local" % gethostname())
serverPort = 8003

s_tcp = socket(AF_INET, SOCK_STREAM)
s_udp = socket(AF_INET, SOCK_DGRAM)
myTcpPort = 0
user = "userName"

# def createTcpSocket():
# 	global s_tcp
# 	global myTcpPort
# 	s_tcp = socket(AF_INET, SOCK_STREAM)
# 	s_tcp.bind(("localhost", 0))
# 	addrInfo = s_tcp.getsockname()
# 	s_tcp.listen(5)
# 	myTcpPort = addrInfo[1]

def createUdpSocket():
	global user
	global myTcpPort
	global s_udp
	# myIp = gethostbyname("%s.local" % gethostname())
	# print "hey"
	s_udp.connect(("localhost", 0))

# def connectToFriend():
# 	friend = raw_input("Enter your friend's name: ")
# 	# addrInfo = s.getsockname()
# 	# print addrInfo
# 	#message format friend's name,userIp,userPort
# 	message=""
# 	message += user + "," + friend + "," + `myTcpPort`;
# 	#print message
# 	s_udp.sendto(message,("localhost", serverPort))
# 	response, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes                                                                                                      
# 	print "received message:", response

# def listenOnUdpForCall():
# 	global s_tcp
# 	global s_udp
# 	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes                                                                                                      
# 	print "received message:", request
	# request = request.split(',')
	# newConnection = socket(AF_INET, SOCK_STREAM)
	# newConnection.bind(("localhost", 0))
	# newConnection.connect((request[0], int(request[1])))

# def startSession():
# 	global s_tcp
# 	newConnection, friendAddress = s_tcp.accept()
# 	print "connected!!" 

def makeOnline():
	global user
	message=""
	message += "folder,send,";
	print message
	s_udp.sendto(message,("localhost", 8003))
	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	print request
	sendFolder(int(request))

def sendFile(rec_port):
	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.connect(("localhost", rec_port))
	# s_tcp.send("hey there dellilah")
	file = open("sendfile", "rb")
	chunk = file.read(65536)
	while chunk:
		s_tcp.send(chunk)
		chunk = file.read(65536)

def sendFolder():
	global user
	cmd = ["find", ".","-type","f"]
	out = check_output(cmd).strip()
	print out
	file_list = out.split('\n')

	message=""
	message += "folder,";
	message += out;
	# print message
	s_udp.sendto(message,("localhost", 8003))
	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	print request
	rec_port = int(request)

	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.connect(("localhost", rec_port))
	# s_tcp.send("hey there dellilah")
	for filename in file_list:
		file = open(filename, "rb")
		chunk = file.read(65536)
		while chunk:
			s_tcp.send(chunk)
			chunk = file.read(65536)
		file.close()



# main starts here
# user = raw_input("Enter your name: ")
# createTcpSocket()

# action = input("Press 1 to start video chat with a friend and 0 to wait for a call!!")
# print action
# if action == 1:
# 	createUdpSocket()
# 	connectToFriend()
# 	startSession()
# else:
createUdpSocket()
sendFolder()

# HOST = ''
# PORT = 8001
# s = socket(AF_INET, SOCK_STREAM)
# s.connect((HOST, 0)) # client-side, connects to a host
# while True: 
# 	message = raw_input("Your Message: ") 
# 	s.send(message) 
# 	print "Awaiting reply" 
# 	reply = s.recv(1024) # 1024 is max data that can be received 
# 	print "Received ", repr(reply)
# s.close()
