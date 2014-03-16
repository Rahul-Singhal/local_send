#Programmer : Rahul Singhal
#client

# a client is always listening on a udp port for the incoming connections
from socket import *
from subprocess import *
import sys
import os

myIp = gethostbyname("%s.local" % gethostname())
serverIp = ""
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
	global myIp
	# myIp = gethostbyname("%s.local" % gethostname())
	# print "hey"
	s_udp = socket(AF_INET, SOCK_DGRAM)
	myIp = gethostbyname("%s.local" % gethostname())
	s_udp.bind((myIp, 8003))

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
	global serverIp
	sendFilename = os.path.split(filename)[1]
	message = "file,"+sendFilename ;
	message += "," + gethostbyname("%s.local" % gethostname()) + " requesting to send a file."
	# print serverIp + "hey there"
	# sys.exit(0)
	# print message
	s_udp.sendto(message,(serverIp, 8003))
	request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	# print request
	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.connect((serverIp, int(request)))
	# s_tcp.send("hey there dellilah")
	file = open(filename, "rb")
	chunk = file.read(1024)
	while chunk:
		s_tcp.send(chunk)
		chunk = file.read(1024)

def sendMessage(send_message):
	global serverIp
	global s_udp
	message = "message,Message from " ;
	message += gethostbyname("%s.local" % gethostname()) + ": " + send_message
	# print message
	# print serverIp
	s_udp.sendto(message,(serverIp, 8003))

def sendFolder(folderName):
	folderName = folderName.rstrip('/')
	global user
	global serverIp
	changeFolder = os.path.split(folderName)[0]
	cwd = os.getcwd()
	if changeFolder!="":
		os.chdir(changeFolder)
	# print "changeFolder = " + changeFolder
	# print "cwd = " + cwd
	# print "foldername = " + folderName
	# print "culprit =" + os.path.split(folderName)[1]
	cmd = ["find", os.path.split(folderName)[1],"-type","f"]
	out = check_output(cmd).strip()
	# print " main hoon out"
	# print out
	file_list = out.split('\n')
	message = "folder,"+out;
	message += "," + gethostbyname("%s.local" % gethostname()) + " requesting to send a folder."
	# print " aur main hoon message"
	# print message
	s_udp.sendto(message,(serverIp, 8003))
	# request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
	# print request
	# rec_port = int(request)

	global s_tcp
	global myTcpPort
	
	# s_tcp.send("hey there dellilah")
	for filename in file_list:
		# print "loop mein aaya"
		request, addr = s_udp.recvfrom(1024) # buffer size is 1024 bytes  
		rec_port = int(request)
		# print "request hoon main -> " + request
		s_tcp = socket(AF_INET, SOCK_STREAM)
		s_tcp.connect((serverIp, int(request)))
		# print "filename = "+filename
		file = open(filename, "rb")
		chunk = file.read(1024)
		while chunk:
			s_tcp.send(chunk)
			chunk = file.read(1024)
		file.close()
		s_tcp.close()
	os.chdir(cwd)

def check_flags():
	# print sys.argv[1]
	global serverIp
	args = str(sys.argv)
	args = args.translate(None,'\'').strip('[]').split(',')
	# print args
	# m for message, f for file and r for folder

	if(len(sys.argv) != 4):
		if(args[2].strip(' ') == "-m"):
			# print ''.join(args[2:])
			serverIp = args[1].strip(' ')
			# createUdpSocket()
			sendMessage(''.join(args[3:]))
		else:
			print "Wrong command line arguments!"
			sys.exit(0)
	else:
		if(args[2].strip(' ') == "-f"):
			serverIp = args[1].strip(' ')
			# createUdpSocket()
			sendFile(args[3].strip(' '))
		elif(args[2].strip(' ') == "-r"):
			serverIp = args[1].strip(' ')
			# createUdpSocket()
			sendFolder(args[3].strip(' '))
		elif(args[2].strip(' ') == "-m"):
			serverIp = args[1].strip(' ')
			# createUdpSocket()
			sendMessage(args[3].strip(' '))
		else:
			print "Wrong command line arguments!"
			sys.exit(0)


if call(["fuser", "8003/udp"], stdout=PIPE, stderr=PIPE) != 0:
	createUdpSocket()
else:
	myIp = gethostbyname("%s.local" % gethostname())
	s_udp.connect((myIp, 8003))
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
