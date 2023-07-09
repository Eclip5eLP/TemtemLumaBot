###################
# Made by Eclip5e #
###################

# Check installed Modules
import sys
sys.path.append('./data')
from importer import Importer
Importer.verifyLibs({'pyautogui', 'keyboard', 'colorama', 'requests', 'opencv-python', 'pypiwin32', 'pushbullet.py'}, False)

# Import Modules
from pyautogui import *
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
from ecpreader import ecpreader
from LumaWorker import LumaBotWorker, BotState
import os, json, win32gui, shutil
import pyautogui
import time
import keyboard
import random
import json
import colorama

# Load Settings
with open('settings.json') as f:
	settings = json.load(f)

colorama.init()

class LumaBot:
	# Setup
	appName = "Temtem LumaBot"
	controls = settings['controls']

	version = "0.5.1"

	bot = LumaBotWorker(settings, appName, version)

	def start(self):
		self.bot.start()

		# Main Loop
		while(True):
			if not self.bot.paused:
				# Print State
				pass

			if self.bot.stopped:
				break

			# Hotkeys
			if keyboard.is_pressed(self.controls["exit"]): # Quit
				self.bot.stop()
				break
			if keyboard.is_pressed(self.controls["pause"]): # Pause
				if self.bot.paused: # Resume
					self.bot.paused = False
					self.bot.encounter = datetime.now()
					print(Fore.LIGHTCYAN_EX + "Unpaused" + Fore.WHITE + self.bot.clr, end='\r')
					sleep(0.5)
				else: # Pause
					self.bot.paused = True
					print(Fore.LIGHTCYAN_EX + "Paused" + Fore.WHITE + self.bot.clr, end='\r')
					sleep(0.5)
		# Exit cleanup
		shutil.rmtree('__pycache__')
		shutil.rmtree('./data/__pycache__')

if __name__ == "__main__":
	luma = LumaBot()
	luma.start()