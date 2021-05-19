#!/usr/bin/env python3
import tkinter as tk
from tkinter import *
import shutil         
import os
import easygui
from tkinter import filedialog
from tkinter import messagebox as mb
import speech_recognition as sr
from pathlib import Path

# open a file box window 
# when we want to select a file
def open_window():
    read=easygui.fileopenbox()
    return read
# open file function
def open_file():
    string = open_window()
    try:
        os.startfile(string)
    except:
        mb.showinfo('confirmation', "File not found!")
# copy file function
def copy_file():
    source1 = open_window()
    destination1=filedialog.askdirectory()
    shutil.copy(source1,destination1)
    mb.showinfo('confirmation', "File Copied !")
# delete file function
def delete_file():
    del_file = open_window()
    if os.path.exists(del_file):
        os.remove(del_file)             
    else:
        mb.showinfo('confirmation', "File not found !")
# rename file function
def rename_file():
    chosenFile = open_window()
    path1 = os.path.dirname(chosenFile)
    extension=os.path.splitext(chosenFile)[1]
    print("Enter new name for the chosen file")
    newName=input()
    path = os.path.join(path1, newName+extension)
    print(path)
    os.rename(chosenFile,path) 
    mb.showinfo('confirmation', "File Renamed !")
# move file function
def move_file():
    source = open_window()
    destination =filedialog.askdirectory()
    if(source==destination):
        mb.showinfo('confirmation', "Source and destination are same")
    else:
        shutil.move(source, destination)  
        mb.showinfo('confirmation', "File Moved !")
# function to make a new folder
def make_folder():
    newFolderPath = filedialog.askdirectory()
    print("Enter name of new folder")

    newFolder=input()
    path = os.path.join(newFolderPath, newFolder)  

    os.mkdir(path)
    mb.showinfo('confirmation', "Folder created !")
# function to remove a folder
def remove_folder():
    delFolder = filedialog.askdirectory()
    os.rmdir(delFolder)
    mb.showinfo('confirmation', "Folder Deleted !")
# function to list all the files in folder
def list_files():
    folderList = filedialog.askdirectory()
    sortlist=sorted(os.listdir(folderList))       
    i=0
    print("Files in ", folderList, "folder are:")
    while(i<len(sortlist)):
        print(sortlist[i]+'\n')
        i+=1

#Listen and process Voice
def vsearch_files():
    print("voice search")
    r = sr.Recognizer()
    # obtain audio from the microphone
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
        mb.showinfo('confirmation', "Click ok to start Listenning")
        print("Listening...")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    try:
        text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)
        find_files(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        mb.showerror("Error", "Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        mb.showerror("Error", "Could not request results from Google Speech Recognition service; {0}".format(e))

#Search From Home Directory in Top-Down approach
def find_files(filename):
    fresult = []
    home = str(Path.home()) #setting root search directory (in this case it is C:/users/<username>)
    # Wlaking top-down from the root
    for root, dir, files in os.walk(home):
        for file in files:
            if filename.lower() == file.lower().split('.')[0]:
                fresult.append(os.path.join(root, file))
        for diry in dir:
            if filename.lower() == diry.lower():
                fresult.append(os.path.join(root, diry))

    #Displaying Search results
    if not fresult:
        print("No Such Files/Directory")
        mb.showinfo('Info', "No Such Files/Directory")
    else:
        sres = tk.Tk()
        sres.title("Voice Search Results")
        i=0
        for x in fresult:
            #print(x)
            tk.Button(sres, text=x, command=lambda x=x: openf(x)).grid(row=i, column =2)
            i=i+1
        sres.mainloop()

#Open Files/Directory
def openf(fpath):
    print(fpath)
    try:
        os.startfile(fpath)
    except:
        print('File not found')
        mb.showerror("Error", "File/Directory not found")


root = tk.Tk()
root.title("File Manager")
#GUI Elements
Button(root, text = "Open a File", command = open_file).grid(row=1, column =2)

Button(root, text = "Copy a File", command = copy_file).grid(row = 2, column = 2)

Button(root, text = "Delete a File", command = delete_file).grid(row = 3, column = 2)

Button(root, text = "Rename a File", command = rename_file).grid(row = 4, column = 2)

Button(root, text = "Move a File", command = move_file).grid(row = 5, column =2)

Button(root, text = "Make a Folder", command = make_folder).grid(row = 7, column = 2)

Button(root, text = "Remove a Folder", command = remove_folder).grid(row = 6, column =2)

Button(root, text = "List all Files in Directory", command = list_files).grid(row = 8,column = 2)

btn = Button(root, text="Voice Search", command=vsearch_files).grid(row = 9,column = 2)

root.mainloop()