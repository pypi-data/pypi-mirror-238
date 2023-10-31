#This is the standalone app for 'SoleStormCatPY'. Here, any user can use 'SoleStormCatPY' with little to no coding (Depends on if the user uses a script to open this script). Here is how you can make your own script to open this app:

#import SoleStormCatPY.sscPyStandalone as SSCstand
#SSCstand.fullPythonApp()

#You can also use the Python app in the command prompt:

#import SoleStormCatPY.sscPyStandalone as SSCstand
#SSCstand.fullPythonAppCMD()


from tkinter import *
from tkinter.ttk import *
from time import strftime
import os
import platform as pf

"Apps"
def WebGUI():
	import SoleStormCatPY.WebOpen
	SoleStormCatPY.WebOpen.webGUI()
def TerminalGUI():
	import SoleStormCatPY.terminal
	SoleStormCatPY.terminal.terminalGUI()
def SystemInfo():
	import SoleStormCatPY.SystemInfo as si
	si.systemInfoPrint()
def ClockTimerGUI():
	import SoleStormCatPY.ClockTimer
	SoleStormCatPY.ClockTimer.clockTimerGUI()
def FilesGUI():
	import SoleStormCatPY.files
	SoleStormCatPY.files.filesGUI()
def appOpenerGUI():
	import SoleStormCatPY.appOpener as app
	app.openAppGUI()

def SoleStormCatUpdate():
	UpgradeFrame = Tk()
	UpgradeFrame.title('SoleStormCatPY - Update')
	UpgradeFrame.geometry('1000x50')
	
	UpgradeLabel = Label(UpgradeFrame, text='SoleStormCatPY is currently being upgraded to the latest version. You may view progress in terminal.')
	UpgradeLabel.pack()
	
	osV = pf.system()
	print('Updating SoleStormCatPY!')
	
	if osV == 'Windows':
		os.system('py -m pip install --upgrade SoleStormCatPY')
	else:
		os.system('python3 -m pip install --upgrade SoleStormCatPY')
	
	UpgradeLabel.mainloop()
	
"App Loader:"
def fullPythonApp():
	frame = Tk()
	frame.title('SoleStormCatPY')
	frame.geometry('1024x768')
	
	MenuBar = Menu(frame)
	file = Menu(MenuBar, tearoff=0)
	MenuBar.add_cascade(label ="File", menu = file)
	file.add_command(label ="Update", command=SoleStormCatUpdate)
	file.add_command(label ="Quit", command=quit)
	
	appsBar = Menu(MenuBar, tearoff=0)
	MenuBar.add_cascade(label ="Apps", menu = appsBar)
	appsBar.add_command(label ="ClockTimer", command=ClockTimerGUI)
	appsBar.add_command(label ="System Info", command=SystemInfo)
	appsBar.add_command(label ="Terminal", command=TerminalGUI)
	appsBar.add_command(label ="Web", command=WebGUI)
	appsBar.add_command(label ="Files", command=FilesGUI)
	appsBar.add_command(label ="appOpener", command=appOpenerGUI)
	
	"GUI TAB"
	appLabel = Label(frame, text = 'Welcome to "SoleStormCatPY"! Please choose an app below!')
	appLabel.pack()
	
		
	WebB = Button(frame,text='Web', command=lambda: WebGUI())
	WebB.pack()
	
	
	TerminalB = Button(frame,text='Terminal', command=lambda: TerminalGUI())
	TerminalB.pack()
	
	
	SystemInfoB = Button(frame,text='System Info', command=lambda: SystemInfo())
	SystemInfoB.pack()
	
		
	ClockTimerB = Button(frame,text='ClockTimer', command=lambda: ClockTimerGUI())
	ClockTimerB.pack()
	
	FilesGUIB = Button(frame,text='Files', command=lambda: FilesGUI())
	FilesGUIB.pack()

	appOpenerGUIB = Button(frame, text='appOpener', command=lambda: appOpenerGUI())
	appOpenerGUIB.pack()

	
	frame.config(menu = MenuBar)
	frame.mainloop()

def fullPythonAppCMD():
	print('Welcome to SoleStormCatPY! Please print the name of the app that you want!')
	myapp = input(' ')

	if myapp == 'Web':
		import SoleStormCatPY.WebOpen as web

		print('What website do you want to access?')
		website = input(' ')

		web.webCMD(website)
	elif myapp == 'WebGUI':
		import SoleStormCatPY.WebOpen as web

		print('Opening WebOpen in GUI mode!')
		web.webGUI()
	elif myapp == 'Terminal':
		import SoleStormCatPY.terminal as cmd

		print('Which command do you want to run in the terminal?')
		command = input('')
		cmd.terminalrun(command)
	elif myapp == 'TerminalGUI':
		import SoleStormCatPY.terminal as cmd

		print('Opening Terminal in GUI mode!')
		cmd.terminalGUI()
	elif myapp == 'SystemInfo':
		import SoleStormCatPY.SystemInfo as si

		print('Printing system info!')
		si.systemInfoPrint()
	elif myapp == 'ClockTimer':
		import SoleStormCatPY.ClockTimer as ct
		
		print('How many seconds do you want the timer to be?')
		seconds = input('')

		ct.clockTimerManual(seconds)
	elif myapp == 'ClockTimerGUI':
		import SoleStormCatPY.ClockTimer as ct

		print('Opening ClockTimer in GUI mode!')
		ct.clockTimerGUI()
	elif myapp == 'Files':
		import SoleStormCatPY.files as files
		
		files.filesCMD()
	elif myapp == 'FilesGUI':
		import SoleStormCatPY.files as files

		print('Opening Files in GUI mode!')
		files.filesGUI()
	elif myapp == 'MathSolver':
		import SoleStormCatPY.MathSolver as ms

		print('What is the first number that you are wanting in the equation?')
		num1 = input(' ')
		print('What is the second number that you are wanting in the equation?')
		num2 = input(' ')
		print('What type of equation do you want?')
		ty = input('')
		ms.numPrint(num1, num2, ty)
	elif myapp == 'GreeNotes':
		import SoleStormCatPY.GreeNotes as gn

		print('Opening GreeNotes in Terminal mode!')
		gn.GreeNotes()
	elif myapp == 'EmailClient':
		import SoleStormCatPY.MyEmailClient as email
		
		print('Opening MyEmailClient in Terminal Mode!')
		email.emailClient()
	elif myapp == 'SSCPYgui':
		print('Sending you to the GUI app!')
		fullPythonApp()
	elif myapp == 'appOpener':
		import SoleStormCatPY.appOpener as app
		
		print('What app do you want to open?')
		appname = input(' ')

		app.openAppManual(appname)
	elif myapp == 'appOpenerGUI':
		import SoleStormCatPY.appOpener as app

		print('Opening appOpener in GUI mode!')
		app.openAppGUI()
	elif myapp == 'Shell':
		import SoleStormCatPY.interactiveShell as cmd
		cmd.shellOpen()
	else:
		print('The app you are looking for is not found. Please take a look over the apps below and try again!')
		print('Web')
		print('WebGUI')
		print('Terminal')
		print('TerminalGUI')
		print('SystemInfo')
		print('ClockTimer')
		print('ClockTimerGUI')
		print('Files')
		print('FilesGUI')
		print('MathSolver')
		print('GreeNotes')
		print('EmailClient')
		print('appOpener')
		print('appOpenerGUI')
		print('SSCPYgui')
		print('Shell')