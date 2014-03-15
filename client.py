#Programmer : Rahul Singhal
#client

# a client is always listening on a udp port for the incoming connections
from socket import *
from subprocess import *
import sys

serverIp = gethostbyname("%s.local" % gethostname())
serverPort = 8003

s_tcp = socket(AF_INET, SOCK_STREAM)
s_udp = socket(AF_INET, SOCK_DGRAM)
myTcpPort = 0

# def createTcpSocket():
# 	global s_tcp
# 	global myTcpPort
# 	s_tcp = socket(AF_INET, SOCK_STREAM)
# 	s_tcp.bind(("localhost", 0))
# 	addrInfo = s_tcp.getsockname()
# 	s_tcp.listen(5)
# 	myTcpPort = addrInfo[1]

def createUdpSocket():
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

def sendFile(filename):
	message = "file,"+filename ;
	message += "," + gethostbyname("%s.local" % gethostname()) + " requesting to send a file."
	s_udp.sendto(message,("localhost", 8003))
	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	# print request
	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.connect(("localhost", int(request)))
	# s_tcp.send("hey there dellilah")
	file = open(filename, "rb")
	chunk = file.read(65536)
	while chunk:
		s_tcp.send(chunk)
		chunk = file.read(65536)

def sendMessage(send_message):
	message = "message,Message from " ;
	message += gethostbyname("%s.local" % gethostname()) + ": " + send_message
	s_udp.sendto(message,("localhost", 8003))

def sendFolder(folderName):
	global user
	cmd = ["find", folderName,"-type","f"]
	out = check_output(cmd).strip()
	# print out
	file_list = out.split('\n')

	message = "folder,"+out;
	message += "," + gethostbyname("%s.local" % gethostname()) + " requesting to send a folder."
	# print message
	s_udp.sendto(message,("localhost", 8003))
	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	# print request
	rec_port = int(request)

	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.connect(("localhost", int(request)))
	# s_tcp.send("hey there dellilah")
	for filename in file_list:
		file = open(filename, "rb")
		chunk = file.read(65536)
		while chunk:
			s_tcp.send(chunk)
			chunk = file.read(65536)
		file.close()

def check_flags():
	print sys.argv[1]
	args = str(sys.argv)
	args = args.translate(None,'\'').strip('[]').split(',')
	# print args
	# m for message, f for file and r for folder
	if(len(sys.argv) != 3):
		if(args[1].strip(' ') == "-m"):
			# print ''.join(args[2:])
			createUdpSocket()
			sendMessage(''.join(args[2:]))
		else:
			print "Wrong command line arguments!"
			sys.exit(0)
	else:
		if(args[1].strip(' ') == "-f"):
			createUdpSocket()
			sendFile(args[2].strip(' '))
		elif(args[1].strip(' ') == "-r"):
			createUdpSocket()
			sendFolder(args[2].strip(' '))
		elif(args[1].strip(' ') == "-m"):
			createUdpSocket()
			sendMessage(args[2].strip(' '))
		else:
			print "Wrong command line arguments!"
			sys.exit(0)


check_flags()



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
