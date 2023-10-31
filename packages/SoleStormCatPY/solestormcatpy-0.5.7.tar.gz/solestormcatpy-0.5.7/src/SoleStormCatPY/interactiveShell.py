#This allows for a user to run their terminal inside of a SoleStormCat-made Interactive Shell! Inside are some commands that are custom made by SoleStormCat, and can also run your normal commands!
#How to use:
#import SoleStormCatPY.interactiveShell as cmd
#cmd.shellOpen()

#You may also open the shell using some code by using:
#cmd.shellUse('command')

import os
import platform as pf

username = os.getlogin()
hostname = pf.node()

def shellUse(command):
    if command == 'help':
        print('Here are the active SoleStormCat Commands:')
        print('help')
        print('sscpy')
        print('python')
        print('web')
        print(' ')
        print('For system commands, type help --os')
        print('You may also use help -m name for help with a specific module!')
    elif command == 'help --os':
        print('Here are your system commands:')
        os.system('help')
    elif command == 'help -m help':
        print('help shows the help information for the SoleStormCat terminal.')
        print('You can also use help --os to run the OS help menu.')
    elif command == 'sscpy':
        import SoleStormCatPY.sscPyStandalone as sscpy
        sscpy.fullPythonAppCMD()
    elif command == 'sscpy --gui':
        import SoleStormCatPY.sscPyStandalone as sscpy
        sscpy.fullPythonApp()
    elif command == 'help -m sscpy':
        print('sscpy is an applacation developed by SoleStormCat Corp. SoleStormCatPY offers many features, and you can visit the GitHub page at https://github.com/solestormcat-corp/solestormcatpy')
        print('You may also run sscpy --gui to run SoleStormCatPY in GUI mode!')
    elif command == 'python':
        import SoleStormCatPY.appOpener as appo
        appo.openAppManual('Python')
    elif command == 'help -m python':
        print('python is a coding platform developed by the Python Software Foundation.')
    elif command == 'web':
        import SoleStormCatPY.WebOpen as web
        web.webCMDgui()
    elif command == 'web --tk':
        import SoleStormCatPY.WebOpen as web
        web.webGUI()
    elif command == 'web --db':
        import SoleStormCatPY.WebOpen as web
        print('What website do you want to visit?')
        website = input(' ')
        web.webCMD(website)
    elif command == 'help -m web':
        print('web utilizes the SoleStormCatPY webOpen module to use a web browser.')
        print('You can run web --tk to use a tkinter window for the URL asker.')
        print('You can run web --df to use your defult browser.')
    else:
        os.system(command)
    print()
    shellOpen()

def shellOpen():
    print(username, '@', hostname)
    command = input('')
    shellUse(command)