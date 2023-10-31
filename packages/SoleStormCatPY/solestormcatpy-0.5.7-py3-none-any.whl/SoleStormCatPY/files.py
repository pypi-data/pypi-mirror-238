#This Implements a file explorer into Python. Here is how you use it (Terminal Version):
#import SoleStormCatPY.files as sscfile
#sscfile.filesCMD()

#To Use this in the GUI, use:
#import SoleStormCatPY.files as sscfile
#sscfile.filesGUI()


#This is a modified version of a file explorer from https://data-flair.training/blogs/python-file-explorer-project/
import os
from tkinter import *

def filesCMD():
	
	def openfile():
		file = input('Please provide the location to your file:  ')
		os.system(os.path.abspath(file))
		print('File Opened!')
		
	def deletefile():
		file = input('Please provide the location to your file:  ')
		os.remove(os.path.abspath(file))
		print('File Deleted!')
		
	def renamefile():
		file = input('Please provide the location to your file:  ')
		filenewname = input('Please provide the new file name:   ')
		
		os.rename(file, filenewname)
		print(f'File {file} has been renamed to {filenewname}!')
	def openfolder():
		folder = input('Please provide a location to your folder:   ')
		os.system(folder)
	def deletefolder():
		folder = input('Please provide a location to your folder:   ')
		os.rmdir(folder)
		print('Folder Removed!')
	def listfiles():
		folder = input('Please provide the location of your folder:    ')
		listfiles = os.listdir(folder)
		print('Files and folder found within ',folder,': ')
		print(listfiles)
	
	print('What type of operation do you want your file to provide? (Type One Of The Names Below (or their commands listed))')
	print('Open File (opfl)')
	print('Delete File (rmfl)')
	print('Rename File (rnfl)')
	print('Open Folder (opfo)')
	print('Delete Folder (rmfo)')
	print('List Files (lst)')
	operationty = input(' ')
	
	if operationty == 'Open File':
		openfile()
	elif operationty == 'opfl':
		openfile()
	elif operationty == 'Delete File':
		deletefile()
	elif operationty == 'rmfl':
		deletefile()
	elif operationty == 'Rename File':
		renamefile()
	elif operationty == 'rnfl':
		renamefile()
	elif operationty == 'Open Folder':
		openfolder()
	elif operationty == 'opfo':
		openfolder()
	elif operationty == 'Delete Folder':
		deletefolder()
	elif operationty == 'rmfo':
		deletefolder()
	elif operationty == 'List Files':
		listfiles()
	elif operationty == 'lst':
		listfiles()
	else:
		print('There was an error in your command. Please check the commands and try again')
		filesCMD()
	

def filesGUI():
	import tkinter.filedialog as fd
	import tkinter.messagebox as mb
	
	def openfile():
		file = fd.askopenfilename(title ='File Picker', filetypes=[("All files", "*.*")])
		os.system(file)
		
	def deletefile():
		file = fd.askopenfilename(title ='File Deleter', filetypes=[("All files", "*.*")])
		os.remove(os.path.abspath(file))
		
		mb.showinfo(title="Operation Complete", message='The File that you have been selected has been deleted. Status: Operation Completed!')
		
	def renamefile():
		file = fd.askopenfilename(title ='File Re-namer', filetypes=[("All files", "*.*")])
		
		rename_frame = Toplevel(frame)
		rename_frame.title('Rename File To:')
		rename_frame.geometry('250x70')
		
		Label(rename_frame, text='What do you want to re-name the file to?', font=("Times New Roman", 10)).place(x=0, y=0)
		
		file_newname = Entry(rename_frame, width=40, font=("Times New Roman", 10))
		file_newname.place(x=0, y=30)
		
		os.rename(file, file_newname)
		mb.showinfo(title="Operation Complete", message='The File that you have been selected has been renamed. Status: Operation Completed!')
		
	def openfolder():
		folder = fd.askdirectory(title='Select Your Folder')
		os.startfile(folder)
		
	def deletefolder():
		folder = fd.askdirectory(title='Select Your Folder to Delete')
		os.rmdir(folder)
		
		mb.showinfo(title="Operation Complete", message='The Folder that you have selected to delete has been deleted. Status: Operation Complete!')
		
	def listfiles():
		i = 0
			
		folder = fd.askdirectory(title='Select Your Folder')
		
		listfrm = Toplevel(frame)
		listfrm.title(f"Files Found in {folder}")
		listfrm.geometry('500x500')
		
		listbox = Listbox(listfrm, font=("Georgia", 10))
		listbox.place(relx=0, rely=0, relheight=1, relwidth=1)
		
		scrollbar = Scrollbar(listbox, orient=VERTICAL, command=listbox.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		listbox.config(yscrollcommand=scrollbar.set)
		
		while i < len(files):
			listbox.insert(END, files[i])
			i += 1
			
	title = 'SoleStormCatPY Files'
		
	frame = Tk()
	frame.title(title)
	frame.geometry('250x400')
	
	lbl = Label(frame, text="Welcome to SoleStormCatPY's File App! Click a button below to do an operation!")
	lbl.pack()
	
	openfilebutton = Button(frame, text='Open File', command=openfile)
	deletefilebutton = Button(frame, text='Delete File', command=deletefile)
	renamefilebutton = Button(frame, text='Rename File', command=renamefile)
	openfolderbutton = Button(frame, text='Open Folder', command=openfolder)
	deletefolderbutton = Button(frame, text='Delete Folder', command=deletefolder)
	listfilesbutton = Button(frame, text='List Files in Folder', command=listfiles)
	
	openfilebutton.pack()
	deletefilebutton.pack()
	renamefilebutton.pack()
	openfolderbutton.pack()
	deletefolderbutton.pack()
	listfilesbutton.pack()
	
	frame.update()
	frame.mainloop()

