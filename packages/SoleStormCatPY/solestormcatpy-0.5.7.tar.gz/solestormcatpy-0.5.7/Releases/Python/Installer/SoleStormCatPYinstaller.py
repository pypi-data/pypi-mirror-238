"""THIS INSTALLS 'SoleStormCatPY' VIA 'Python'. If you do not have Python, you may install it at python.org!"""

import os
import platform as pf

ask = input('Do you want to install SoleStormCatPY onto your system? ("yes" or "no")     ')

if ask == 'yes':
	print('Downloading SoleStormCatPY from PyPi via pip, along with other required modules!')
	osV = pf.system()
	if osV == 'Windows':
		os.system('py -m pip install --upgrade SoleStormCatPY')
		os.system('py -m pip install --upgrade tkinter')
		os.system('py -m pip install --upgrade threading')
		os.system('py -m pip install --upgrade subprocess')
		os.system('py -m pip install --upgrade playsound')
		os.system('py -m pip install --upgrade PyQt5')
		os.system('py -m pip install --upgrade PyQtWebEngine')
	else:
		os.system('python3 -m pip install --upgrade SoleStormCatPY')
		os.system('python3 -m pip install --upgrade tkinter')
		os.system('python3 -m pip install --upgrade threading')
		os.system('python3 -m pip install --upgrade subprocess')
		os.system('python3 -m pip install --upgrade playsound')
		os.system('python3 -m pip install --upgrade PyQt5')
		os.system('python3 -m pip install --upgrade PyQtWebEngine')
	input('The modules of "SoleStormCatPY", "tkinter", "threading", "subprocess", "playsound", "PyQt5", and "PyQtWebEngine" were installed (if not already). Entering the GUI of SoleStormCatPY!')
	import SoleStormCatPY.sscPyStandalone as standalone
	standalone.fullPythonApp()
	
elif ask == 'no':
	input('No Changes Were Made To Your System. If you would like to install SoleStormCatPY, you may use this file, or run "pip install SoleStormCatPY" in your terminal!')
