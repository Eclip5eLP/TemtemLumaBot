###################
# Made by Eclip5e #
###################

# Check installed Modules
import sys
sys.path.append('./data')
from importer import Importer
Importer.verifyLibs({'pyautogui', 'keyboard', 'colorama', 'datetime', 'pypiwin32'})

# Import Modules
from pyautogui import *
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
from subprocess import call
from tkinter import ttk
from tkinter import * 
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import json
import tkinter as tk
import colorama
import ast

colorama.init()

# Load Settings
with open('settings.json') as f:
	settings = json.load(f)

### GUI ###

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

# this is the function called when the button is clicked
def btnSave():
	global settings

	settings['walkTime'] = ast.literal_eval(walkTimeGet())
	settings['reposTime'] = float(reposTimeGet())
	settings['pattern'] = patternSelect.current()

	with open('settings.json', 'w', encoding='utf-8') as f:
		json.dump(settings, f, ensure_ascii=False, indent=4)

	print("Settings Saved")

# this is the function called when the button is clicked
def btnStart():
	print("Bot Started")
	call('start /wait python LumaBot.py', shell=True)
	print("Done")

root = Tk()

# This is the section of code which creates the main window
root.geometry('715x366')
root.configure(background='#F0F8FF')
root.title('Temtem LumaBot by Eclip5e')

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

# This is the section of code which creates a button
Button(root, text='Save Settings', bg='#D6D6D6', font=('arial', 12, 'normal'), command=btnSave).place(x=200, y=291)

# This is the section of code which creates a button
Button(root, text='Start Bot', bg='#D6D6D6', font=('arial', 12, 'normal'), command=btnStart).place(x=491, y=158)

print("App launched")
root.mainloop()