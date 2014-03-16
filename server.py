#Programmer : Rahul Singhal
#client

# a client is always listening on a udp port for the incoming connections
from socket import *
from subprocess import call
import os
import termios, fcntl, sys, time

serverIp = gethostbyname("%s.local" % gethostname())
serverPort = 8003

s_tcp = socket(AF_INET, SOCK_STREAM)
s_udp = socket(AF_INET, SOCK_DGRAM)
myTcpPort = 0
user = "userName"

downloadDirectory = os.getenv("HOME")+"/Downloads/myDownloads/"

def createTcpSocket():
	global s_tcp
	global myTcpPort
	s_tcp = socket(AF_INET, SOCK_STREAM)
	s_tcp.bind(("localhost", 0))
	addrInfo = s_tcp.getsockname()
	s_tcp.listen(5)
	myTcpPort = addrInfo[1]

def createUdpSocket():
	global user
	global myTcpPort
	global s_udp
	# myIp = gethostbyname("%s.local" % gethostname())
	# print "hey"
	s_udp.bind(("localhost", 8003))

# def connectToFriend():
# 	friend = raw_input("Enter your friend's name: ")
# 	# addrInfo = s.getsockname()
# 	# print addrInfo
# 	#message format friend's name,userIp,userPort
# 	message=""
# 	message += user + "," + friend + "," + `myTcpPort`;
# 	#print message
# 	s_udp.sendto(message,("localhost", serverPort))
# 	response, addr = s_udp.recvfrom(65536) # buffer size is 65536 bytes                                                                                                      
# 	print "received message:", response

def listenOnUdpForCall():
	global s_tcp
	global s_udp
	request, addr = s_udp.recvfrom(65536) # buffer size is 65536 bytes                                                                                                      
	# print "received message:", request
	# print "over"
	# print "request hai ye"
	# print request
	request = request.split(',')

	if(request[0]=="file"):
		call(["notify-send", request[2], "-i",  "/usr/share/pixmaps/local_send_file.png"])
		receiveFile(request,addr);
	elif(request[0] == "folder"):
		call(["notify-send", request[2], "-i",  "/usr/share/pixmaps/local_send_folder.png"])
		receiveFolder(request,addr);
	elif(request[0] == "message"):
		call(["notify-send", request[1], "-i",  "/usr/share/pixmaps/local_send_message.png"])


def receiveFile(request,addr):
	createTcpSocket()
	s_udp.sendto(str(myTcpPort),addr)
	con, ad = s_tcp.accept()
	filename = request[1]
	recFile = open(filename, "wb")
	message = con.recv(1024)
	# print message
	while(message):
		recFile.write(message);
		message = con.recv(1024)
		# print message
	recFile.close();

def receiveFolder(request,addr):
	fileList = request[1].split('\n');
	for filename in fileList:
		createTcpSocket()
		# print myTcpPort
		s_udp.sendto(str(myTcpPort),addr)
		con, ad = s_tcp.accept()
		dirname = os.path.split(filename)[0]
		# print "DIRNAME "+dirname
		if (dirname != "" and not os.path.exists(dirname)):
			os.makedirs(dirname)
		recFile = open(filename, "wb")
		message = con.recv(1024)
		# print message
		while(message):
			recFile.write(message);
			message = con.recv(1024)
			# print message
		recFile.close();
		s_tcp.close()





# def startSession():
# 	global s_tcp
# 	newConnection, friendAddress = s_tcp.accept()
# 	print "connected!!" 

# def makeOnline():
# 	global user
# 	message=""
# 	message += "makeOnline," + user + "," + `myTcpPort`;
# 	#print message
# 	s_udp.sendto(message,("localhost", serverPort))



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
call(["mkdir","-p",os.getenv("HOME")+"/Downloads/myDownloads/"])
os.chdir(os.getenv("HOME")+"/Downloads/myDownloads/")
createUdpSocket()
while 1:
	listenOnUdpForCall()

# HOST = ''
# PORT = 8001
# s = socket(AF_INET, SOCK_STREAM)
# s.connect((HOST, 0)) # client-side, connects to a host
# while True: 
# 	message = raw_input("Your Message: ") 
# 	s.send(message) 
# 	print "Awaiting reply" 
# 	reply = s.recv(65536) # 65536 is max data that can be received 
# 	print "Received ", repr(reply)
# s.close()
