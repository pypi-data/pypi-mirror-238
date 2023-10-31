#This is a notepad taking service, which creates a ".sscGreeNotes" (It is hidden unless your file manager shows you hidden files), which allows you to save your own notes for future reference. Here is how you'll be able to run it (currently only supports terminal):
#import SoleStormCatPY.GreeNotes as notes
#notes.GreeNotes()


def GetNotesFile():
	try:
		"This'll find the file"
		notesfile = open(".sscGreeNotes", "x")
		
		"If The File does not exist, the file will be created here"
		
		notesfile = open(".sscGreeNotes", "x")
		print('File Was Created! Started GreeNotes!')
		print(' ')
	except FileExistsError:
		"If the file exists"
		print('File Found! Opening GreeNotes!')
		print(' ')


def GreeNotes():
	"Makes sure that the file exists"
	GetNotesFile()
	
	notesfile = open(".sscGreeNotes", "r+")
	
	print('What operation do you want to do for your notes?')
	print('"read" (rd) or "write" (wr)')
	readwrite = input(' ')
	
	if readwrite == 'read':
		print('Here is the contents of your reminders/notes:')
		print(' ')
		print(notesfile.read())
	elif readwrite == 'rd':
		print('Here is the contents of your reminders/notes:')
		print(' ')
		print(notesfile.read())
	elif readwrite == 'write':
		print('What do you want to write to your reminders?')
		writeline = input(' ')
		notesfile.writelines([writeline,"\n"])
		print(' ')
		print('Your line has been written to the file.')
		print(' ')
	elif readwrite == 'wr':
		print('What do you want to write to your reminders?')
		writeline = input(' ')
		notesfile.writelines(["\n",writeline,"\n"])
		print(' ')
		print('Your line has been written to the file.')
		print(' ')
	else:
		print('Operation Unknown. Please try again.')
		print(' ')
		GreeNotes()
	
	anotherline = input('Do you want to add another reminder? (y or n)')
	if anotherline == 'y':
		GreeNotes()
	elif anotherline == 'n':
		notesfile.close()
		quit()
	else:
		print('Unknown Command. Reopening GreeNotes.')
		print(' ')
		GreeNotes()
