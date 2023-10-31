#This gets/shows information about the user's system! Here is a way to use it:"
#import SoleStormCatPY.SystemInfo as SystemInfo
#
#SystemInfo.systemInfoPrint()


#This Gets the system info, but does not print it:

#import SoleStormCatPY.SystemInfo as SystemInfo
#SystemInfo.systemInfoFind()


import os
import platform as pf
import subprocess as sp


def systemInfoFind():
	"GETS THE SYSTEM INFO"
	deviceOS = pf.system()
	userName = os.getlogin()
	if deviceOS == "Windows":
		pythonVersion = os.system('py --version')
	else:
		pythonVersion = os.system('python3 --version')
	wifiinfo = sp.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
	wifissid = wifiinfo.decode('utf-8')
	hostName = pf.node()
	return deviceOS, userName, pythonVersion, wifissid, hostName


def systemInfoPrintGET(deviceOS,userName,pythonVersion,wifissid,hostName):
	"PRINTS THE SYSTEM INFO"
	deviceOS = systemInfoFind()
	userName = systemInfoFind()
	pythonVersion = systemInfoFind()
	
	print('The Current User OS is:  ')
	print(deviceOS)
	print(' ')
	print('The Current User is:   ')
	print(userName)
	print(' ')
	print('The Current Python Version is:   ')
	print(pythonVersion)
	print(' ')
	print('The Current Wifi is:     ')
	print(wifissid)
	print('The Current Host Name is:  ')
	print(hostName)

def systemInfoPrint():
	deviceOS, userName, pythonVersion, wifissid, hostName = systemInfoFind()
	systemInfoPrintGET(deviceOS,userName,pythonVersion,wifissid,hostName)




