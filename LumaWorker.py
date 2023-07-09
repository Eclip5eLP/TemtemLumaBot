###################
# Made by Eclip5e #
###################

# Import Modules
from pyautogui import *
from threading import Thread, Lock
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
from ecpreader import ecpreader
import os, json, win32gui
import pyautogui
import time
import keyboard
import random
import colorama
import pushbullet

colorama.init()

# Enum Botstates
class BotState:
	INIT = 0
	SEARCHING = 1
	BATTLE = 2

# Main Worker
class LumaBotWorker:
	# Setup
	INIT_TIME = 2

	stopped = True
	lock = None
	state = None
	appName = "Unknown"
	version = "0"
	settings = None

	reposTime = 0
	lumaCheck = 0
	walkTime = 0
	reposType = 0
	controls = 0
	pushNotifKey = ""
	notifClient = None

	inbattle = False
	encounter = datetime.now()
	tracker = 0
	paused = False
	found = False
	clr = "                 "
	runtime = None
	freader = ecpreader()
	resolution = [1920, 1080]
	resList = ["1920x1080", "3440x1440"]
	resId = -1
	window = None

	# Init
	def __init__(self, settings, appName, version):
		self.lock = Lock()

		self.state = BotState.INIT
		self.version = version
		self.appName = appName

		self.settings = settings
		self.reposTime = settings['reposTime']
		self.lumaCheck = settings['lumaCheck']
		self.walkTime = settings['walkTime']
		self.reposType = settings['reposType']
		self.controls = settings['controls']
		self.pattern = settings['pattern']
		self.pushNotifKey = settings['pushNotifKey']

	# Start the bot
	def start(self):
		self.stopped = False
		t = Thread(target=self.run)
		t.start()
		
		# Init
		print(Fore.CYAN + "Temtem LumaBot v" + self.version + Fore.WHITE)
		print(Fore.MAGENTA + "Made by Eclip5e\n" + Fore.WHITE)
		print("Initializing...", end="\r")

		time.sleep(1)
		self.getRes()

		time.sleep(1)
		self.runtime = self.loadRuntime("runtime")
		self.state = BotState.SEARCHING
		print(Fore.GREEN + "Bot running!" + Fore.WHITE+self.clr)
		self.sendPushNotif("Bot started")

	# Stop the bot
	def stop(self, luma=False):
		self.stopped = True

		# Save runtime
		self.saveRuntime("runtime")

		# Quit App
		print(Fore.CYAN + "Encounters: " + str(self.tracker) + Fore.WHITE+self.clr)
		if luma:
			print(Fore.LIGHTRED_EX + "End" + Fore.WHITE+self.clr)
		else:
			print(Fore.LIGHTRED_EX + "Quit" + Fore.WHITE+self.clr)
			self.sendPushNotif("Bot stopped")

	# Main Bot Logic
	def run(self):
		while not self.stopped:
			if not self.paused and self.resId != -1:
				# Check for battle
				if self.state != BotState.INIT:
					self.inbattle = self.checkBattle()
					if self.inbattle:
						self.state = BotState.BATTLE
					else:
						self.state = BotState.SEARCHING

				if self.state == BotState.INIT: # Initializing
					pass # Wait
				elif self.state == BotState.SEARCHING: # Searching for battle
					self.findBattle()
				elif self.state == BotState.BATTLE: # Check Luma and flee
					time.sleep(0.5)
					if self.checkLuma():
						self.saveRuntime(self.freader.id_generator(random.randint(9,15)))
						self.stop(True)
						break

	# Save Runtime
	def saveRuntime(self, name):
		file = "./data/" + name + ".ecp"
		runvars = json.dumps({"appName":self.appName,"pushNotifKey":self.pushNotifKey,"reposTime":self.reposTime,"reposType":self.reposType,"lumaCheck":self.lumaCheck,"walkTime":self.walkTime,"controls":self.controls,"version":self.version,"inbattle":self.inbattle,"tracker":self.tracker,"paused":self.paused,"found":self.found})
		if (os.path.exists(file)):
			os.remove(file)
		self.freader.make(file, runvars, 1)

	# Load Runtime
	def loadRuntime(self, name):
		file = "./data/" + name + ".ecp"
		if (os.path.exists(file)):
			return self.freader.read(file)
		return None

	# Returns a random number
	def randnum(self, a, b):
		return round(random.uniform(a, b), 3)

	# Walk around to find a battle
	def findBattle(self):
		if self.pattern == 0: # Fast
			self.walkLR()
			#self.walkUD()
		elif self.pattern == 1: # Random
			self.walk(random.choice([self.controls["up"],self.controls["down"],self.controls["left"],self.controls["right"]]))
			time.sleep(self.randnum(0.25, 0.45))
		elif self.pattern == 0: # Real
			# todo
			self.walkLR()

		# Repositioning in case of no encounters
		if not self.stopped and not self.paused:
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

	# Flee from Battle
	def battleFlee(self):
		if not keyboard.is_pressed(self.controls["hold"]):
			keyboard.send("8")
			time.sleep(0.3)
			keyboard.send("8")
			self.inbattle = False
			time.sleep(self.randnum(1.5, 2.5))

	# Walk left and right
	def walkLR(self):
		self.walk(self.controls["left"])
		time.sleep(self.randnum(0.15, 0.35))
		self.walk(self.controls["right"])
	# Walk up and down
	def walkUD(self):
		self.walk(self.controls["up"])
		time.sleep(self.randnum(0.15, 0.35))
		self.walk(self.controls["down"])

	# Walk any direction
	def walk(self, direction):
		if not keyboard.is_pressed(self.controls["hold"]) and not self.paused:
			keyboard.press(direction)
			time.sleep(self.randnum(self.walkTime[0], self.walkTime[1]))
			keyboard.release(direction)

	# Check if inside Battle
	def checkBattle(self):
		# Check for Battle
		find = self.search('flee_' + str(self.resId), region=self.resolution[1] // 2)
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
		return self.searchLuma()

	# Luma Image recognition
	def searchLuma(self):
		if pyautogui.locateOnScreen('./images/luma_'+str(self.resId)+'.png', confidence=self.lumaCheck, grayscale=True, region=(0, 0, self.resolution[0], self.resolution[1] // 2)) != None: # Luma found
			print(Fore.CYAN + "Luma found!" + Fore.WHITE+self.clr)
			self.sendPushNotif("Luma found!")
			self.found = True
			return True
		else: # No Luma - Flee
			self.battleFlee()
			self.encounter = datetime.now()
		return False

	# Image recognition
	def search(self, img, conf=0.8, region=0):
		simg = pyautogui.locateOnScreen('./images/' + img + '.png', confidence=conf, grayscale=True, region=(0, region, self.resolution[0], self.resolution[1] - region))
		if simg != None:
			return simg
		else:
			return False

	# Recognize game resolution
	def getRes(self):
		hwnd = win32gui.FindWindow(None, "Temtem")
		self.window = hwnd
		if (hwnd == 0):
			print(Fore.LIGHTRED_EX + "Game is not running!" + Fore.WHITE)
			self.stopped = True
			return False

		rect = win32gui.GetWindowRect(hwnd)
		x = rect[0]
		y = rect[1]
		w = rect[2] - x
		h = rect[3] - y

		self.resolution = [w, h]
		print(Fore.CYAN + "Game Resolution: " + str(self.resolution[0]) + "x" + str(self.resolution[1]) + Fore.WHITE)

		i = 0
		for x in self.resList:
			if str(w) + "x" + str(h) == x:
				self.resId = i
				i = -1
				break
			i += 1
		if i != -1:
			self.resId = 0
			print(Fore.LIGHTRED_EX + "Resolution not directly supported" + Fore.WHITE)
			return False
		return True

	# Send a custom Push Notification to users phone
	def sendPushNotif(self, msg="No Message"):
		if self.pushNotifKey == "":
			return False
		if self.notifClient == None:
			self.notifClient = pushbullet.PushBullet(self.pushNotifKey)

		push = self.notifClient.push_note(self.appName, msg)
		return True