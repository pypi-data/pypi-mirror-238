#This Tool Sends emails through your email client. During first setup, you'll be asked to set up your account via the terminal.
#To Run this, run:
#import SoleStormCatPY.MyEmailClient as sscEmail
#sscEmail.emailClient()


"These modules are required for the app to run correctly"
import smtplib
import ssl
import platform as pf
import os

"This Gets The Email info from the email file"
def FileFinderE():
	deviceOS = pf.system()
	if deviceOS == 'Windows':
		emailfile = open('C:\\Program Files\\SoleStormCatPY\\EmailClient\\solestormcatEmail.txt', 'x')
	else:
		emailfile = open('~\\.SoleStormCatPY\\EmailClient\\solestormcatEmail.txt', 'x')
	return emailfile
def FileFinderP():
	deviceOS = pf.system()
	if deviceOS == 'Windows':
		passwordfile = open('C:\\Program Files\\SoleStormCatPY\\EmailClient\\solestormcatPassword.txt', 'x')
	else:
		passwordfile = open('~\\.SoleStormCatPY\\EmailClient\\solestormcatPassword.txt', 'x')
	return passwordfile
def FileFinderS():
	deviceOS = pf.system()
	if deviceOS == 'Windows':
		serverfile = open('C:\\Program Files\\SoleStormCatPY\\EmailClient\\solestormcatServer.txt', 'x')
	else:
		serverfile = open('~\\.SoleStormCatPY\\EmailClient\\solestormcatServer.txt', 'x')
	return serverfile
def FileFinderPO():
	deviceOS = pf.system()
	if deviceOS == 'Windows':
		portfile = open('C:\\Program Files\\SoleStormCatPY\\EmailClient\\solestormcatPort.txt', 'x')
	else:
		portfile = open('~\\.SoleStormCatPY\\EmailClient\\solestormcatPort.txt', 'x')
	return portfile

def getEmailInfo():

	"The FolderFiner() came from https://stackoverflow.com/a/1274465"

	def FolderFinder():
		deviceOS = pf.system()
		if deviceOS == 'Windows':
			mypath = r'C:\\Program Files\\SoleStormCatPY\\EmailClient'
		else:
			mypath = r'~\\.SoleStormCatPY\\EmailClient'
		if not os.path.exists(mypath):
			os.makedirs(mypath)

	
	try:
		"Finds the file"
		FolderFinder()
		emailfile = FileFinderE()
		passwordfile = FileFinderP()
		serverfile = FileFinderS()
		portfile = FileFinderPO()
	
		"Runs if the email file (solestormcatEmail.txt) is not found"
		print('The files for the email client does not exist. Creating files. You will be asked questions about your email info.')
		
		email = input('What is the email that you want to use?     ')
		
		password = input('What is the password to this email?   ')
		
		server = input('What is the site of the server (not including the port number)   ')

		port = input('What is the port to your email server?   ')
		
		emailfile.writelines([email])
		passwordfile.writelines([password])
		serverfile.writelines([server])
		portfile.writelines([port])
		
		print('Email File Created!')
		"This then points back to the emailClient() code"
		
	except FileExistsError:
		"Runs if the file is found"
		print('Files Found!')
		"This then points back to the emailClient() code"
		

def emailClient():
	"Makes sure that the email file exists"
	print("Reading Email File...")
	getEmailInfo()
	
	"Opens the email file, gathers info."
	emailfile = FileFinderE()
	passwordfile = FileFinderP()
	serverfile = FileFinderS()
	portfile = FileFinderPO()
	
	def readEmailFile(file,x):
		"From https://stackoverflow.com/a/7523061"
		for index,line in enumerate(iter(file)):
			if index+1 == x: return line

		return None
    	
	myemail = readEmailFile(emailfile)
	mypassword = readEmailFile(passwordfile)
	server = readEmailFile(serverfile)
	port = readEmailFile(portfile)
	
	"Closes File, gives conformation"
	emailfile.close()
	print('Email Info has been gotten!')
	
	"Attempts to connect to server"
	context = ssl.create_default_context()
	
	try:
		smtp_server = smtplib.SMTP(server,port)
		smtp_server.connect()
		smtp_server.ehlo()
		smtp_server.starttls(context=context)
		smtp_server.ehlo()
		smtp_server.login(myemail,mypassword)
		
		"This is where the email gets created!"
		print('Connection to server secured!')
		print(' ')
		
		friend_email = input('Who is this email for?    ')
		subject = input('What is the subject of the email?    ')
		body = input('What is the body of the email?       ')
		message = """\
		Subject:""",subject,"""
		
		
		""",body
		
		print('''Here is your message info:
		''','Email being sent to: ',friend_email,'''
		''','''Subject and Body:
		''',message)
		print(' ')
		print('The message is being sent')
		
	except Exception as e:
		"This works if an error has occured"
		print('There was an error. Error info is below:')
		print(e)
