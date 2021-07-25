###################
# Made by Eclip5e #
###################

#Check installed Modules
import sys
import subprocess
import pkg_resources

required = {'pyautogui', 'keyboard', 'colorama', 'datetime'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
	print("Installing dependencies...")
	python = sys.executable
	subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

#Import Modules
from pyautogui import *
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import requests
import json
from subprocess import call
import tkinter as tk
from tkinter import ttk
from tkinter import * 

#Load Settings
with open('settings.json') as f:
	settings = json.load(f)

### GUI ###

# this is a function which returns the selected combo box item
def resolutionGet():
	return resolutionSelect.get()

# this is a function which returns the selected combo box item
def patternGet():
	return patternSelect.get()

# this is a function to get the user input from the text input box
def reposTimeGet():
	userInput = reposTimeIn.get()
	return userInput

# this is a function to get the user input from the text input box
def walkTimeGet():
	userInput = walkTimeIn.get()
	return userInput

# this is a function to get the user input from the text input box
def conApiGet():
	userInput = conApiIn.get()
	return userInput

# this is the function called when the button is clicked
def btnSave():
	global settings

	settings['conApi'] = conApiGet()
	settings['walkTime'] = float(walkTimeGet())
	settings['reposTime'] = float(reposTimeGet())
	settings['resolution'] = resolutionSelect.current()
	settings['pattern'] = patternSelect.current()

	with open('settings.json', 'w', encoding='utf-8') as f:
		json.dump(settings, f, ensure_ascii=False, indent=4)

	print("Settings Saved")

# this is the function called when the button is clicked
def btnStart():
	call('start /wait python core.py', shell=True)
	print("Bot Started")

root = Tk()

# This is the section of code which creates the main window
root.geometry('715x366')
root.configure(background='#F0F8FF')
root.title('Temtem Luma Bot by Eclip5e')

# This is the section of code which creates a combo box
resList = []
for i in settings['resList']:
	resList.append(str(i[0]) + "x" + str(i[1]))
resolutionSelect= ttk.Combobox(root, values=resList, font=('arial', 12, 'normal'), width=12, state="readonly")
resolutionSelect.place(x=11, y=36)
resolutionSelect.current(settings['resolution'])

# This is the section of code which creates the a label
Label(root, text='Resolution', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=12, y=9)

# This is the section of code which creates the a label
Label(root, text='Movement Pattern', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=196, y=10)

# This is the section of code which creates a combo box
patternSelect= ttk.Combobox(root, values=settings['patternList'], font=('arial', 12, 'normal'), width=12, state="readonly")
patternSelect.place(x=195, y=36)
patternSelect.current(settings['pattern'])

# This is the section of code which creates a text input box
reposTimeIn=Entry(root)
reposTimeIn.place(x=11, y=168)
reposTimeIn.insert(0,str(settings['reposTime']))

# This is the section of code which creates the a label
Label(root, text='Reposition Time', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=12, y=141)

# This is the section of code which creates the a label
Label(root, text='Walk Time', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=196, y=140)

# This is the section of code which creates a text input box
walkTimeIn=Entry(root)
walkTimeIn.place(x=193, y=168)
walkTimeIn.insert(0,str(settings['walkTime']))

# This is the section of code which creates the a label
Label(root, text='Output API', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=12, y=268)

# This is the section of code which creates a text input box
conApiIn=Entry(root)
conApiIn.place(x=11, y=296)
conApiIn.insert(0,str(settings['conApi']))

# This is the section of code which creates a button
Button(root, text='Save Settings', bg='#D6D6D6', font=('arial', 12, 'normal'), command=btnSave).place(x=200, y=291)

# This is the section of code which creates a button
Button(root, text='Start Bot', bg='#D6D6D6', font=('arial', 12, 'normal'), command=btnStart).place(x=491, y=158)

print("App launched")
root.mainloop()