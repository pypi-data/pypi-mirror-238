#THIS APPLICATION HELPS A USER MAKE AN TIMER IN THE TERMINAL. TO RUN (DO NOT CHANGE THE 'minutes' WITHIN 'timer.clockTimer()':
#import SoleStormCatPY.ClockTimer as timer
#
#timer.clockTimerCMD(minutes)

#TO MANUALLY RUN THE TIMER BY THE DEVELOPER, RUN:
#import SoleStormCatPY.ClockTimer as timer
#
#seconds = {"HOW MANY SECONDS YOU WANT. IF YOU REQUIRE MINUTES, USE "{minutes} * 60"}
#timer.clockTimerManual(seconds)

#Here is how to run the GUI version of ClockTimer:
#import SoleStormCatPY.ClockTimer as timer
#timer.clockTimerGUI()


from threading import Timer
import subprocess
from playsound import playsound
import tkinter
import tkinter.ttk as ttk

def timeout():
    print("Finished Timer!")
    playsound('SoleStormCatPY.ClockTimerAssets.timerUP')

def getNum():
    minutesSTR = input('How Many Minutes do you require?     ')
    minutes = int(minutesSTR)
    return minutes

def clockTimerSETUP(minutes):
    t = Timer(minutes * 60, timeout)
    t.start()
    print('Waiting for timer of ',minutes,' minutes to complete!')
    
    t.join()
    
def clockTimerManual(seconds):
    t = Timer(seconds, timeout)
    t.start()
    print('Waiting for timer of ',seconds,' seconds to complete!')
    
    t.join()
    
def clockTimerCMD():
    minutes = getNum()
    clockTimerSETUP(minutes)
    
def clockTimerGUI():
	def timeout():
		frameEND = tkinter.Tk()
		frameEND.title('Timer, ENDED!')
		frameEND.geometry('500x500')
		
		lblEND = tkinter.Label(frameEND,
		text = "Your Timer Has Ended!")
		lblEND.pack()
		
		playsound('SoleStormCatPY.ClockTimerAssets.timerUP')
		frameEND.mainloop()
		
	def clockTimerGUIS():
		timeSTR = inputtxt.get(1.0, 'end-1c')
		time = int(timeSTR)
		t = Timer(time, timeout)
		t.start()
		
		frameTime = tkinter.Tk()
		frameTime.title('Timer, Started')
		frameTime.geometry('500x500')
		
		lblTime = tkinter.Label(frameTime,
		text = "Your Timer Of:")
		lblTime.pack()
		lbltimeS = tkinter.Label(frameTime,
		text = timeSTR)
		lbltimeS.pack()
		
		lbltime1 = tkinter.Label(frameTime,
		text = "Seconds has started!")
		lbltime1.pack()
		
		frameTime.mainloop()
		
		t.join()
	def clockTimerGUImin():
		timeSTR = inputtxt.get(1.0, "end-1c")
		time = int(timeSTR)
		
		t = Timer(time * 60, timeout)
		t.start()
		
		frameTime = tkinter.Tk()
		frameTime.title('Timer, Started')
		frameTime.geometry('500x500')
		
		lblTime = tkinter.Label(frameTime,
		text = "Your Timer Of:")
		lblTime.pack()
		
		lbltimeS = tkinter.Label(frameTime,
		text = timeSTR)
		lbltimeS.pack()
		
		lbltime1 = tkinter.Label(frameTime,
		text = "Minutes Has Started!")
		lbltime1.pack()
		
		frameTime.mainloop()
		
		t.join()
    
	def clockTimerGUIhour():
		timeSTR = inputtxt.get(1.0, "end-1c")
		time = int(timeSTR)
		
		t = Timer(time * 3600, timeout)
		t.start()
		
		frameTime = tkinter.Tk()
		frameTime.title('Timer, Started')
		frameTime.geometry('500x500')
		
		lblTime = tkinter.Label(frameTime,
		text = "Your Timer Of:")
		lblTime.pack()
		
		lbltimeS = tkinter.Label(frameTime,
		text = timeSTR)
		lbltimeS.pack()
		
		lbltime1 = tkinter.Label(frameTime,
		text = "Hours Has Started!")
		lbltime1.pack()
		
		lbltimeD = tkinter.Label(frameTime,
		text = "DISCLAIMER: THIS WILL TAKE A WHILE!")
		lbltimeD.pack()
		
		frameTime.mainloop()
		t.join()
	
	frame = tkinter.Tk()
	frame.title('Timer')
	frame.geometry('1000x250')
	tabControl = ttk.Notebook(frame)
	
	tabSEC = ttk.Frame(tabControl)
	tabMIN = ttk.Frame(tabControl)
	tabHOUR = ttk.Frame(tabControl)
	tabControl.add(tabSEC, text='Seconds')
	tabControl.add(tabMIN, text='Minutes')
	tabControl.add(tabHOUR, text='Hours')
	tabControl.pack(expand = 1, fill ="both")
	
	
	lblBLANK = tkinter.Label(tabSEC,
	text = " ")
	lblBLANK.pack()
	lblBLANK = tkinter.Label(tabMIN,
	text = " ")
	lblBLANK.pack()
	lblBLANK = tkinter.Label(tabHOUR,
	text = " ")
	lblBLANK.pack()
	
	inputtxt = tkinter.Text(tabSEC,
	height = 1,
	width = 45)
	inputtxt.pack()
	inputtxt = tkinter.Text(tabMIN,
	height = 1,
	width = 45)
	inputtxt.pack()
	inputtxt = tkinter.Text(tabHOUR,
	height = 1,
	width = 45)
	inputtxt.pack()
	
	startTimerButton = tkinter.Button(tabSEC,
	text = "Start Timer",
	command = clockTimerGUIS)
	startTimerButton.pack()
	startTimerButton = tkinter.Button(tabMIN,
	text = "Start Timer",
	command = clockTimerGUImin)
	startTimerButton.pack()
	startTimerButton = tkinter.Button(tabHOUR,
	text = "Start Timer",
	command = clockTimerGUIhour)
	startTimerButton.pack()
	
	
	lbl = tkinter.Label(tabSEC,
	text = "Enter your time in the box, then click the 'Start Timer' button. You may use the tabs to change your time setting, your current 	time setting is: Seconds")
	lbl.pack()
	lbl = tkinter.Label(tabMIN,
	text = "Enter your time in the box, then click the 'Start Timer' button. You may use the tabs to change your time setting, your current time setting is: Minutes")
	lbl.pack()
	lbl = tkinter.Label(tabHOUR,
	text = "Enter your time in the box, then click the 'Start Timer' button. You may use the tabs to change your time setting, your current time setting is: Hours")
	lbl.pack()
	
	frame.mainloop()
	
