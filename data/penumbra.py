### --- PENUMBRA --- ###
##  Made by Eclip5e   ##
##  ©Penumbra Games   ##
### ---------------- ###

from pathlib import Path
import secrets
import math
import re, sys, os
import random
import string
import argparse

class Penumbra:

	# Vars
	seed = 0
	alph32 = []
	alph64 = []
	numSec = secrets.SystemRandom()
	lkey = "penumbra"
	verbose = False

	def __init__(self):
		self.seed = self.numSec.randrange(1000000, 99999999 + 1)
		self.alph32 = [ # Alphabet to encrypt
			'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
			'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
			'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '?', '_',
			'=', ':', '.', ',', '#', '\'', '"', '+', '-', ' ', '', '\\', '$',
			'%', '&', '(', ')', '[', ']', '{', '}', '*', ';', '/', '<', '>',
			'@', '^', '`', '´', '|', '~', 'ü', 'Ü', 'ä', 'Ä', 'ö', 'Ö', '°',
			'\n', '§'
		]
		self.alph64 = [ # Random Charset
			'K1x92iH', 'sHCxknj', '9onzMUS', 'uuufycE', '6SbzVmU', 'j6KHRXu', 'ZjX4Mjq', 't3wrwab', 'AOvBzPX', 'SpJEXWp', 'tcU5Q8I', 'nX5CmQ5', 'NZSInUD',
			'mPRKqqP', 'AWfWQMn', '5BfGeOV', 'LTMNEy2', '4OycbDz', 'IaCgdrg', 'CegIbIj', 'VQcezsQ', 'NPnXPDL', 'Q8Hy9Is', 'cPga3M5', 'RFjVLwt', 'aQNghME',
			'qtwQAnH', 'IsNO9jE', 'eCDFv5l', 'MVwF2tu', 'joYPugk', 'h5zI7nm', 'tIbO42Z', 'ETCuaqO', 'A1txQDl', 'n4fqlum', 'A8GKNsy', 'cAPvhN4', 'EZj7fbm',
			'k24BTgN', 'FQz1OXr', '6cAQFId', 'EEHFi6X', 'WVVjAR1', 'fnYiY6A', 'XnydcQp', '5lNHhJO', '9djKfWl', 'zZNc8tG', 'zj73VGY', 'vdxSs5K', 'eiMz6pz',
			'Um22km8', '79OzDgl', 'bmCsRVJ', 'XTcoiZR', 'QtNkHc3', 'B6NxZ6i', 'kppGy1Q', 'Goj6asD', '0EhzFeV', 'A9UaNvn', 'U6Xxp0f', 'R68GBY0', 'mckIKa0',
			'1yW9R58', 'TCmbLhy', 'TrYztMy', 'rU6HTc6', 'xYo8YqB', '0Tr2C6A', 'P42OoVE', 'ydp3W7S', 'WeEX4Ww', 'yjjHcep', 'DM3k5p5', 'BgWHrpz', 'HIXiSB4',
			'n4RDOHH', '2FIhRuw', 'I5mY1KV', 'zZ2IAnO', '11DsLZs', 'TrddoqA', 'pf1Uiy5', 'STWPRcb', 'L737Zdo', 'Q4DkPFG', 'Eyq57e6', 'bVAvz5Y', 'bhVfuL7',
			'WEyOSFe', 'FHdgWkg', 'iHKAjNL', '22egLBv', 'PXp9ftx', 'fq9VRMC', 'cMiiOB0', 'PAHaNis', 'ocG4USq', '1q9GZ2G', 'az9F70I', '4u4RX6i', 'aTROxEZ',
			'a9wGHA2', 'Opl5wF6'
		]

	# Encrypt
	def encrypt(self, inp, key):
		cipher = ""
		length = len(inp)
		ochar = ""
		nchar = ""
		pos = 0;

		# Create Seed
		n = 0;
		for i in range(len(key)):
			n = n + int(ord(key[i]))
		key = n
		self.setSeed(key)

		# Encrypt
		for i in range(length):
			ochar = inp[i:i+1]
			try:
				pos = self.alph32.index(ochar)
			except:
				continue

			if pos != -1:
				randAdd = self.randomseed();
				pos += randAdd;
				if pos > len(self.alph32) - 1:
					pos -= len(self.alph32)
				if pos < 0:
					pos = len(self.alph32) - (pos * -1)
				nchar = self.alph64[pos]
			else:
				nchar = ochar
			cipher = cipher + nchar

		self.seed = self.numSec.randrange(1000000, 99999999 + 1)
		return (re.sub('\t', '', str(cipher)).split('\r\n'))[0]

	# Decrypt
	def decrypt(self, inp, key):
		cipher = ""
		length = len(inp)
		ochar = ""
		nchar = ""
		pos = 0;

		# Create Seed
		n = 0;
		for i in range(len(key)):
			n = n + int(ord(key[i]))
		key = n
		self.setSeed(key)

		# Decrypt
		for d in range(int(length / 7)):
			i = d * 7
			ochar = inp[i:i+7]
			try:
				pos = self.alph64.index(ochar)
			except:
				continue

			if pos != -1:
				randAdd = self.randomseed();
				pos -= randAdd;
				if pos > len(self.alph64) - 1:
					pos -= len(self.alph64)
				if pos < 0:
					pos = len(self.alph64) - (pos * -1)
				nchar = self.alph32[pos]
			else:
				nchar = ochar
			cipher = cipher + nchar

		self.seed = self.numSec.randrange(1000000, 99999999 + 1)
		return (re.sub('\t', '', str(cipher)).split('\r\n'))[0]

	# Clear alph base
	def clear(self):
		self.alph32 = []
		self.alph64 = []

	# Get Random Number from current Seed
	def randomseed(self):
		x = math.sin(int(self.seed)) * 10000
		self.seedAdvance()
		return math.floor((x - math.floor(x)) * 100);

	# Set Seed
	def setSeed(self, seed):
		self.seed = seed;

	# Advance Seed by one
	def seedAdvance(self):
		self.seed = int(self.seed) + 1;

	# Remove one from See
	def seedBack(self):
		self.seed = int(self.seed) - 1;

	# Check CMD Parameters
	def isParam(self, param):
		i = 0
		for x in sys.argv:
			if x == param:
				return i
			i += 1
		return -1

	def id_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

# Main
if __name__ == "__main__":
	pen = Penumbra()
	lkey = pen.lkey

	# CMD Argument Parser
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--encrypt", help="Encrypt a file or string", type=str)
	parser.add_argument("-d", "--decrypt", help="Decrypt a file or string", type=str)
	parser.add_argument("-o", "--output", help="Output to file", type=str)
	parser.add_argument("-k", "--key", help="Encryption key", type=str)
	parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
	args = parser.parse_args()

	# Key
	if args.key != None:
		lkey = args.key

	# Key
	if args.verbose == True:
		pen.verbose = True

	# Encrypt
	if args.encrypt != None:
		if args.encrypt != "" and Path(args.encrypt).is_file(): # Crypt File
			f = open(args.encrypt, "r")
			cont = f.read()
			f.close()

			# Encrypt
			enc = pen.encrypt(cont, lkey)
			if (pen.verbose):
				print(enc)

			# Write Output
			if args.output != None:
				f = open(args.output, "w")
			else:
				f = open(args.encrypt, "w")

			if enc == "":
				f.write(cont)
				print("error: File is empty")
			else:
				f.write(enc)
				if args.verbose != None:
					print("Success")
			f.close()
		else: # Crypt String
			enc = pen.encrypt(args.encrypt, lkey)
			if (pen.verbose):
				print(enc)

	# Decrypt
	if args.decrypt != None:
		if args.decrypt != "" and Path(args.decrypt).is_file(): # Crypt File
			f = open(args.decrypt, "r")
			cont = f.read()
			f.close()

			# Decrypt
			dec = pen.decrypt(cont, lkey)
			if (pen.verbose):
				print(dec)

			# Write Output
			if args.output != None:
				f = open(args.output, "w")
			else:
				f = open(args.decrypt, "w")

			if dec == "":
				f.write(cont)
				print("error: File is empty")
			else:
				f.write(dec)
				if args.verbose != None:
					print("Success")
			f.close()
		else: # Crypt String
			dec = pen.decrypt(args.decrypt, lkey)
			if (pen.verbose):
				print(dec)