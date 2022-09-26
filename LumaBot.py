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
from ecpreader import ecpreader
import os
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import json
import colorama

# Load Settings
with open('settings.json') as f:
	settings = json.load(f)

colorama.init()

class LumaBot:
	# Setup
	appName = "Temtem LumaBot"
	reposTime = settings['reposTime']
	lumaCheck = settings['lumaCheck']
	walkTime = settings['walkTime']
	reposType = settings['reposType']
	controls = settings['controls']

	version = "0.4.1"
	inbattle = False
	encounter = datetime.now()
	tracker = 0
	paused = False
	found = False
	clr = "                 "
	runtime = None
	freader = ecpreader()

	# Click Function
	def click(self, x,y):
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
		time.sleep(self.randnum(0.075, 0.085))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

	# Save Runtime
	def saveRuntime(self, name):
		file = "./data/" + name + ".ecp"
		runvars = json.dumps({"appName":self.appName,"reposTime":self.reposTime,"reposType":self.reposType,"lumaCheck":self.lumaCheck,"walkTime":self.walkTime,"controls":self.controls,"version":self.version,"inbattle":self.inbattle,"tracker":self.tracker,"paused":self.paused,"found":self.found})
		if (os.path.exists(file)):
			os.remove(file)
		self.freader.make(file, runvars, 1)

	# Load Runtime
	def loadRuntime(self, name):
		file = "./data/" + name + ".ecp"
		if (os.path.exists(file)):
			return self.freader.read(file)
		return None

	def randnum(self, a, b):
		return round(random.uniform(a, b), 3)

	# Flee from Battle
	def battleFlee(self):
		if not keyboard.is_pressed(self.controls["hold"]):
			find = self.search('flee')
			if find != False:
				click(find.left + 10, find.top + 10)
				time.sleep(self.randnum(0.45, 0.55))
				click(find.left + 10, find.top + 10)
				self.inbattle = False
				time.sleep(self.randnum(1.5, 2.5))

	# Walk left and right
	def walkLR(self):
		self.walk(self.controls["left"])
		time.sleep(self.randnum(0.25, 0.45))
		self.walk(self.controls["right"])
	# Walk up and down
	def walkUD(self):
		self.walk(self.controls["up"])
		time.sleep(self.randnum(0.25, 0.45))
		self.walk(self.controls["down"])

	# Walk any direction
	def walk(self, direction):
		if not keyboard.is_pressed(self.controls["hold"]) and not self.paused:
			keyboard.press(direction)
			time.sleep(self.randnum(self.walkTime[0], self.walkTime[1]))
			keyboard.release(direction)

	# Pause Bot
	def checkPause(self):
		if self.paused and keyboard.is_pressed(self.controls["pause"]): # Resume
			self.paused = False
			print(Fore.GREEN + "Resumed" + Fore.WHITE+self.clr, end='\r')
			self.encounter = datetime.now()
			time.sleep(0.75)
			return True
		if keyboard.is_pressed(self.controls["pause"]): # Pause
			self.paused = True
			print(Fore.GREEN + "Paused" + Fore.WHITE+self.clr, end='\r')
			time.sleep(0.75)
			return True

	# Check if inside Battle
	def checkBattle(self):
		# Check for Battle
		find = self.search('flee')
		if find != False:
			print(Fore.GREEN + "Battle found" + Fore.WHITE+self.clr, end='\r')
			if not self.inbattle:
				self.tracker += 1
			return True
		else:
			return False

	# Reposition Character Manual
	def repositionManual(self):
		print(Fore.RED + "Please reposition character" + Fore.WHITE+self.clr, end='\r')
		while not keyboard.is_pressed(self.controls["hold"]) or not self.checkBattle():
			time.sleep(0.5)
		print(Fore.GREEN + "Bot resumed" + Fore.WHITE+self.clr, end='\r')

	# Reposition Character Automatic
	def repositionAuto(self):
		if not self.paused:
			startTime = datetime.now()
			delta = datetime.now() - startTime
			print("Finding Grass...", end='\r')

			# Walk into random directions
			while delta.seconds <= self.reposTime * 2:
				delta = datetime.now() - startTime
				rand = random.choice([self.controls["up"],self.controls["left"],self.controls["down"],self.controls["right"]])
				time.sleep(self.randnum(self.walkTime[0], self.walkTime[1]))
				self.walk(rand)
				if self.checkBattle():
					self.inbattle = True
					return True
			return False

	# Check if Luma encounter
	def checkLuma(self):
		if self.inbattle:
			time.sleep(1)
			return self.searchLuma()
		else: # Walk
			self.walkLR()
			#self.walkUD()
			print(Fore.WHITE + "Looking for battle..." + Fore.WHITE+self.clr, end='\r')
			delta = datetime.now() - self.encounter

			# Reposition
			# 0 - Dont reposition
			# 1 - Automatic
			# 2 - Automatic -> Manual on fail
			if self.reposType != 0:
				if delta.seconds >= self.reposTime: # Reposition
					if self.reposType >= 1 and self.repositionAuto() == False:
						if self.reposType == 2:
							self.repositionManual()


	# Luma Image recognition
	def searchLuma(self):
		if pyautogui.locateOnScreen('./images/luma.png', confidence=self.lumaCheck) != None: # Luma found
			print(Fore.CYAN + "Luma found!" + Fore.WHITE+self.clr)
			self.found = True
			return True
		else: # No Luma - Flee
			self.battleFlee()
			self.encounter = datetime.now()
		return False

	# Image recognition
	def search(self, img, conf=0.8):
		simg = pyautogui.locateOnScreen('./images/' + img + '.png', confidence=conf)
		if simg != None:
			return simg
		else:
			return False

	# Start Bot
	def start(self):
		# Init
		print(Fore.CYAN + "Temtem LumaBot v" + self.version + Fore.WHITE)
		print(Fore.MAGENTA + "Made by Eclip5e\n" + Fore.WHITE)
		print("Initializing...", end="\r")

		time.sleep(2)
		self.runtime = self.loadRuntime("runtime")
		print(Fore.GREEN + "Bot running!" + Fore.WHITE+self.clr)

		# Main Loop
		while not keyboard.is_pressed(self.controls["exit"]):
			self.checkPause()
			if not self.paused:
				self.inbattle = self.checkBattle()
				if self.checkLuma():
					self.saveRuntime(self.freader.id_generator(random.randint(9,15)))
					break
		self.stop()

	# Stop Bot
	def stop(self):
		# Save runtime
		self.saveRuntime("runtime")

		# Quit App
		print(Fore.CYAN + "Encounters: " + str(self.tracker) + Fore.WHITE+self.clr)
		print(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE+self.clr)
		exit()

luma = LumaBot()
luma.start()