#This document opens a web browser. Here is an example code (For Terminal Use)!:
# import SoleStormCatPY.WebOpen as web
#
# website = 'http://127.0.0.1'
# web.webCMD(website)

#Here is another example on how to use this! (For GUI Use)!:
# import SoleStormCatPY.WebOpen as web
#
# web.webGUI()

#Here is an example of opening GUI using the command line:
# import SoleStormCatPY.WebOpen as web
#
# web.webCMDgui('http://127.0.0.1')


def webList(website):
	if website == 'Python':
		print('Sending you to Python!')
		websiteURL = 'https://python.org'
	elif website == 'GitHub':
		print('Sending you to GitHub!')
		websiteURL = 'https://github.com'
	elif website == 'Google':
		print('Sending you to Google!')
		websiteURL = 'https://google.com'
	elif website == 'Bing':
		print('Sending you to Bing!')
		websiteURL = 'https://bing.com'
	elif website == 'Facebook':
		print('Sending you to Facebook!')
		websiteURL = 'https://facebook.com'
	elif website == 'Twitter':
		print('Sending you to Twitter!')
		websiteURL = 'https://twitter.com'
	elif website == 'ChunkBase':
		print('Sending you to ChunkBase!')
		websiteURL = 'https://chunkbase.com'
	elif website == 'Minecraft':
		print('Sending you to Minecraft!')
		websiteURL = 'https://minecraft.net'
	elif website == 'Roblox':
		print('Sending you to Roblox!')
		websiteURL = 'https://roblox.com'
	elif website == 'Microsoft 365':
		print('Sending you to Microsoft 365!')
		websiteURL = 'https://microsoft365.com'
	elif website == 'YouTube':
		print('Sending you to YouTube!')
		websiteURL = 'https://youtube.com'
	elif website == 'Steam':
		print('Sending you to Steam!')
		websiteURL = 'https://store.steampowered.com'
	elif website == 'Walmart':
		print('Sending you to Walmart!')
		websiteURL = 'https://walmart.com'
	elif website == 'Amazon':
		print('Sending you to Amazon!')
		websiteURL = 'https://amazon.com'
	elif website == 'Local':
		print('Sending you to your local website!')
		websiteURL = 'http://127.0.0.1'
	elif website == 'Ebay':
		print('Sending you to Ebay!')
		websiteURL = 'https://ebay.com'
	elif website == 'Netflix':
		print('Sending you to Netflix!')
		websiteURL = 'https://netflix.com'
	elif website == 'PlayStation':
		print('Sending you to PlayStation!')
		websiteURL = 'https://playstation.com'
	elif website == 'Apple':
		print('Sending you to Apple!')
		websiteURL = 'https://apple.com'
	elif website == 'Proton':
		print('Sending you to Proton!')
		websiteURL = 'https://proton.me'
	elif website == 'Snapchat':
		print('Sending you to Snapchat!')
		websiteURL = 'https://web.snapchat.com'
	elif website == 'Twitch':
		print('Sending you to Twitch!')
		websiteURL = 'https://twitch.tv'
	elif website == 'Xbox':
		print('Sending you to Xbox!')
		websiteURL = 'https://xbox.com'
	elif website == 'ChatGPT':
		print('Sending you to ChatGPT!')
		websiteURL = 'https://chat.openai.com'
	elif website == 'BardAI':
		print('Sending you to Google Bard!')
		websiteURL = 'https://bard.google.com'
	elif website == 'GeForceNow':
		print("Sending you to Nvidia GeForce Now!")
		websiteURL = 'https://play.geforcenow.com'
	elif website == 'XBCloud':
		print('Sending you to Xbox Cloud Gaming!')
		websiteURL = 'https://xbox.com/play'
	elif website == 'GoogleVoice':
		print('Sending you to Google Voice!')
		websiteURL = 'https://voice.google.com'
	elif website == 'Android':
		print('Sending you to Android!')
		websiteURL = 'https://android.com'
	elif website == 'GitHubDev':
		print("Sending you to GitHub's Visual Studio Code Developer page!")
		websiteURL = 'https://github.dev'
	elif website == 'sscPY-GitHub':
		print('Sending you to SoleStormCatPY GitHub!')
		websiteURL = 'https://github.com/solestormcat-corp/solestormcatpy'
	elif website == 'sscPY-PyPi':
		print('Sending you to SoleStormCatPY PyPi!')
		websiteURL = 'https://pypi.org/projects/solestormcatpy'
	else:
		print('Sending you to: ',website)
		websiteURL = website
	return websiteURL

def webCMD(website):
	"This imports the 'webbrowser' module"
	import webbrowser

	websiteURL = webList(website)
	webbrowser.open(websiteURL)
	
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
import sys

def webCMDgui(website):
	websiteURL = webList(website)

	app = QApplication(sys.argv)
	web = QWebEngineView()
	web.load(QUrl(websiteURL))
	web.show()
	sys.exit(app.exec_())

def webGUI():
	import tkinter as tk
	
	
	def webGUIinputGET():
		website = inputtxt.get(1.0, "end-1c")
		websiteURL = webList(website)
		 
		app = QApplication(sys.argv)
 
		web = QWebEngineView()
		web.load(QUrl(websiteURL))
		web.show()
		sys.exit(app.exec_())

	frame = tk.Tk()
	frame.title("SoleStormCatPY - WebOpen")
	frame.geometry('500x125')
	inputtxt = tk.Text(frame,
	height = 1,
	width = 45)
	
	inputtxt.pack()
		
	gotoWebButton = tk.Button(frame,
	text = "Go To URL",
	command = webGUIinputGET)
	gotoWebButton.pack()
		
	lbl = tk.Label(frame, text = "Enter your website's URL into the box above. Make sure that your URL does not have the name of a file/folder in your home folder.")
	lbl.pack()
	frame.mainloop()
	
