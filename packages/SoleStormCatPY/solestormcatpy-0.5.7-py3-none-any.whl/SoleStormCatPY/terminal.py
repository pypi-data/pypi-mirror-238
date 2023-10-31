#This brings the user's terminal into your Python script. Run any command you want. In this example, the user will enter their command:

#import SoleStormCatPY.terminal as cmd
#
#command = input("What Command Do You want to run?   ")
#
#cmd.terminalrun(command)

#This example runs your custom commands:

#import SoleStormCatPY.terminal as cmd
#
#command = 'pip list'
#cmd.terminalrun(command)

#This Example Uses GUI, letting Users use their own commands, even if they want to use GUI!:
#import SoleStormCatPY.terminal as cmd
#
#cmd.terminalGUI()


"This Imports the 'os' Module, which is used to run system commands!"
import os
import platform as pf

"This Runs the command specified!"
def terminalrun(command):
	if command == 'UpgrdePyApp':
		osV = pf.system()
		print('Updating SoleStormCatPY!')
		if pf == 'Windows':
			os.system('py -m pip install --upgrade SoleStormCatPY')
		else:
			os.system('python3 -m pip install --upgrade SoleStormCatPY')
	else:
		os.system(command)
	
def terminalGUI():
	import tkinter as tk
	
	def terminalGUIrun():
		command = inputtxt.get(1.0, "end-1c")
		
		terminalrun(command)
		lbl.config(text = 'Your Command Has been printed out in the terminal!')
		
	frame = tk.Tk()
	frame.title("Enter A Command")
	frame.geometry('500x125')
	inputtxt = tk.Text(frame,
	height = 1,
	width = 45)
	
	inputtxt.pack()
	
	gotoTerminalButton = tk.Button(frame,
	text = "Run Command",
	command = terminalGUIrun)
	gotoTerminalButton.pack()
	
	lbl = tk.Label(frame, text = "Enter a Terminal Command into the Box")
	lbl.pack()
	frame.mainloop()
