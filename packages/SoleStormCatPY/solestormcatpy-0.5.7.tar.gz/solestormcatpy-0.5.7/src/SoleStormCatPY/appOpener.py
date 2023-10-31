#This allows for a user (or developer) to open a specific app. How to run this app:
#import SoleStormCatPY.appOpener
#SoleStormCatPY.appOpener.openAppManual('appname')

#OR

#import SoleStormCatPY.appOpener
#SoleStormCatPY.appOpener.openApp()

"Imports the os and platform modules"
import os
"os is used to open the app"
import platform as pf
"platform is used to find device OS, to open an app with the correct system"

"Gathers the device OS"
deviceOS = pf.system()

"App Opener for Windows"
def openAppWINDOWS(appname):
    if appname == 'Python':
        print('Opening py!')
        os.system('py')
    else:
         print('The name for your app is not currently on this list. Please contact SoleStormCat Corp to add your app to this list!')

"App opener for Linux"
def openAppLINUX(appname):
    if appname == 'Python':
        print('Opening python3!')
        os.system('python3')
    elif appname == 'Minecraft':
        print('Opening minecraft-launcher!')
        os.system('minecraft-launcher')
    elif appname == 'vsCode':
        print('Opening Visual Studio Code!')
        os.system('code')
    elif appname == 'Spotify':
        print('Opening Spotify!')
        os.system('spotify')
    elif appname == 'nano':
        print('Opening nano (as current user)!')
        os.system('nano')
    elif appname == 'nanoSU':
        print('Opening nano (as root)!')
        os.system('sudo nano')
    elif appname == 'vim':
        print('Opening Vim (as current user)!')
        os.system('vi')
    elif appname == 'vimSU':
        print('Opening Vim (as root)!')
        os.system('sudo vi')
    else:
        print('The name for your app is not currently on this list. Please contact SoleStormCat Corp to add your app to this list!')

"App opener for MacOS"
def openAppAPPLE(appname):
    if appname == 'Python':
        print('Opening python3!')
        os.system('python3')
    elif appname == 'Minecraft':
        print('Opening Minecraft Launcher!')
        os.system('cd /')
        os.system('cd Applications')
        os.system('open Minecraft.app')
    else:
         print('The name for your app is not currently on this list. Please contact SoleStormCat Corp to add your app to this list!')

"The manual opener"
def openAppManual(appname):
    if deviceOS == 'Windows':
        openAppWINDOWS(appname)
    elif deviceOS == 'Linux':
        openAppLINUX(appname)
    elif deviceOS == 'Darwin':
        openAppAPPLE(appname)
    else:
        print('The current system you are on is not on the list. Please contact SoleStormCat Corp with your device os, and the device os name listed when running the commands below:')
        print(' ')
        print('import platform as pf')
        print('print(pf.system)')
        print(' ')
        quit()

def openAppGUI():
    import tkinter as tk

    def openAppGUIg():
        lbl.config(text='Opening App!')
        appname = inputtxt.get(1.0, "end-1c")
        openAppManual(appname)
    frame = tk.Tk()
    frame.title('SoleStormCatPY - openApp')
    frame.geometry('525x125')

    inputtxt = tk.Text(frame, height=1, width=45)
    inputtxt.pack()

    openAppButton = tk.Button(frame, text='Open App', command=openAppGUIg)
    openAppButton.pack()

    lbl = tk.Label(frame, text='Type in the box with the name for your app. Then, press the "Open App" button!')
    lbl.pack()

    frame.mainloop()