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

#Load Settings
with open('settings.json') as f:
	settings = json.load(f)

#Setup
appName = "LumaBot"
reposTime = settings['reposTime']
lumaCheck = settings['lumaCheck']
walkTime = settings['walkTime']
conApi = settings['conApi']

#Vars
version = "0.3"
inbattle = False
result = None
encounter = datetime.now()
paused = False
pixLoc = []

#Resolution Setup
if settings['resolution'] == 0: #1920x1080
	pixLoc.append([1846,50]) #Minimap
	pixLoc.append([1704,139]) #Battle1
	pixLoc.append([1303,84]) #Battle2
	pixLoc.append([975,896]) #Flee

if settings['resolution'] == 1: #3440x1440
	pixLoc.append([3334,66]) #Minimap
	pixLoc.append([3146,187]) #Battle1
	pixLoc.append([2611,113]) #Battle2
	pixLoc.append([1304,1194]) #Flee

init()

#Click Function
def click(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(0.01)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Flee from Battle
def battleFlee():
	if keyboard.is_pressed('0') == False:
		click(pixLoc[3][0],pixLoc[3][1])
		time.sleep(0.5)
		click(pixLoc[3][0],pixLoc[3][1])
		inbattle = False
		time.sleep(0.5)

#Walk left and right
def walkLR():
	walk('a')
	walk('d')

#Walk any direction
def walk(direction):
	global paused

	if keyboard.is_pressed('0') == False and paused == False:
		keyboard.press(direction)
		time.sleep(walkTime)
		keyboard.release(direction)

def checkPause():
	global paused
	global encounter

	while paused == True:
		if keyboard.is_pressed('p') == True:
			paused = False
			terminal(Fore.GREEN + "Resumed" + Fore.WHITE)
			encounter = datetime.now()
	if keyboard.is_pressed('p') == True:
		paused = True
		terminal(Fore.GREEN + "Paused" + Fore.WHITE)

#Check if inside Battle
def checkBattle():
	global inbattle
	global result

	#Check Outside Battle
	if pyautogui.pixel(pixLoc[0][0],pixLoc[0][1])[0] == 255 and pyautogui.pixel(pixLoc[0][0],pixLoc[0][1])[1] == 167 and pyautogui.pixel(pixLoc[0][0],pixLoc[0][1])[2] == 51:
		inbattle = False
		result = None

	#Check in Battle
	if pyautogui.pixel(pixLoc[1][0],pixLoc[1][1])[0] == 28 and pyautogui.pixel(pixLoc[1][0],pixLoc[1][1])[1] == 209 and pyautogui.pixel(pixLoc[1][0],pixLoc[1][1])[2] == 211:
		inbattle = True

	if pyautogui.pixel(pixLoc[2][0],pixLoc[2][1])[0] == 28 and pyautogui.pixel(pixLoc[2][0],pixLoc[2][1])[1] == 209 and pyautogui.pixel(pixLoc[2][0],pixLoc[2][1])[2] == 211:
		inbattle = True

	return inbattle

#Reposition Character Manual
def repositionManual():
	terminal(Fore.RED + "Please reposition character" + Fore.WHITE)
	while keyboard.is_pressed('0') == False:
		time.sleep(0.5)
	terminal(Fore.GREEN + "Bot resumed" + Fore.WHITE)

#Reposition Character Automatic
def repositionAuto():
	global reposTime
	global paused

	if paused == False:

		startTime = datetime.now()
		terminal("Finding Grass...")

		delta = datetime.now() - startTime
		while delta.seconds <= reposTime * 2:
			rand = random.choice(["w", "a", "s", "d"])
			time.sleep(0.25)
			walk(rand)
			if checkBattle():
				terminal(Fore.GREEN + "Grass found" + Fore.WHITE)
				return True
		return False

#Print to local and remote Terminal
def terminal(text):
	print(text)
	if conApi != "":
		apiCall = conApi + "?app=" + appName + "&log=" + text
		response = requests.get(apiCall)

def checkLuma():
	global inbattle
	global result
	global encounter
	global lumaCheck
	global reposTime

	if inbattle == True:
		time.sleep(1)
		return search()
	else: #Walk
		walkLR()
		delta = datetime.now() - encounter
		if delta.seconds >= reposTime: #Reposition
			if repositionAuto() == False:
				repositionManual()

def search():
	global lumaCheck
	global result
	global encounter

	lumaList = ['lumaGrass', 'lumaCave']

	for img in lumaList:
		if pyautogui.locateOnScreen('./needle/' + img + '.png', confidence=lumaCheck) != None:
			terminal(Fore.CYAN + "Luma found!" + Fore.WHITE)
			result = True
			return True
		else:
			result = False
			battleFlee()
			encounter = datetime.now()
	return False

#Start Bot
terminal("Temtem Luma Hunting Bot\nMade by Eclip5e\n")
terminal("Initializing...")
time.sleep(2)
terminal(Fore.GREEN + "Bot running!" + Fore.WHITE)

#Main Loop
while keyboard.is_pressed('q') == False:
	checkPause()
	checkBattle()
	if checkLuma() == True:
		break

terminal(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE)