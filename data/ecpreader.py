#!/usr/bin/env python
# -*- coding: utf-8 -*-
### --- PENUMBRA --- ###
##  Made by Eclip5e   ##
##  ©Penumbra Games   ##
### ---------------- ###

import math
import re, sys, os
import random
import string
import json
import pathlib
import base64
import zlib
import argparse
from pathlib import Path
from penumbra import Penumbra
from datetime import datetime

pen = Penumbra()

class ecpreader:

	# Vars
	version = "0.2.4"
	net = "Python"
	pdef = "P3nEncrypt3d"

	# File Encoding
	stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()

	def __init__(self):
		# Setup Subtypes
		self.archive = self
		self.archive.zip = self.arch_zip
		self.archive.unzip = self.arch_unzip

	# Read file
	def read(self, file, sigcheck=False):
		if not Path(file).is_file():
			return False

		# Read file
		f = open(file, "r")
		text = f.read()
		f.close()

		# Get file encryption password
		try:
			passlen = int(text[:3])
			passw = text[3:passlen + 3]
			fpass = pen.decrypt(passw, self.pdef)
			fcont = text[passlen + 3::]
		except:
			print("Not an ecp file!")
			return False

		# Decrypt Contents
		content = pen.decrypt(fcont, fpass).split("\n", 4)

		# Check if ECP
		if content == "":
			print("Not an ecp file!")
			return False

		# Signature
		if sigcheck:
			sig = self.id_generator(random.randint(9,15))
			content.append(pen.encrypt("verified", sig))
			content.append(sig)

		# Data types
		if int(content[3]) == 1:
			try:
				content[4] = json.loads(content[4]);
			except:
				print("Failed to load data as json! Loaded plaintext instead")

		return content

	# Make file
	def make(self, file, body, typeov=-1):
		# Data types
		# 0 = Text
		# 1 = Json
		# 2 = Archive
		try:
			json.loads(body)
			types = 1
		except:
			types = 0

		# Type Overwrite
		if typeov != -1:
			types = typeov

		# Prepare vars
		timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		enc = self.id_generator(random.randint(9,15))
		header = [self.version, self.net, timestamp, enc, types]
		passw = pen.encrypt(header[3], self.pdef)
		passlen = ('00' + str(len(passw)))[-3:]

		# Combine Data
		_res = str(header[0]) + "\n" + str(header[1]) + "\n" + str(header[2]) + "\n" + str(header[4]) + "\n" + body
		_res = str(passlen) + passw + pen.encrypt(_res, header[3])

		# Write Output
		f = open(file, "w")
		f.write(str(_res))
		f.close()

		return _res

	# Generate random ID/Password for each file
	def id_generator(self, size=9, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	# Convert file from or to ecp
	def convert(self, file, ftype="ecp", overwrite=True):
		if not Path(file).is_file():
			return False

		nfile = os.path.splitext(file)[0] + "." + ftype

		if ftype == "ecp": # Into ecp
			try:
				# Read file
				f = open(file, "r")
				text = f.read()
				f.close()

				if overwrite:
					if os.path.exists(file):
		  				os.remove(file)
			except:
				print("File contains unreadable characters!")
				return False

			self.make(nfile, text)
			return True
		elif ftype == "txt": # From ecp
			conts = self.read(file)[4]

			if overwrite:
				if os.path.exists(file):
	  				os.remove(file)

			# Write Output
			f = open(nfile, "w")
			f.write(str(conts))
			f.close()

		return True

	# Create a ZIP archive
	def arch_zip(self, files, zname="Archive"):
		zfile = zname + ".ecp"

		zarr = "[[["
		for x in files:
			try:
				# Read file
				f = open(x, "r")
				text = f.read()
				f.close()
			except:
				print("Failed to read \"" + x + "\"!")
				continue
			zarr = zarr + "[[" + "ECP_ARCHZIP_DIVIDER" + "]][" + "<]" + x + "[>" + "]" + text # Weirdify String to allow self archiving

		if zarr == "[[[":
			print("Failed to create Archive! (empty)")
			return False
		self.make(zfile, zarr, 2)

		print("Done")
		return True

	# Unzip a ZIP archive
	def arch_unzip(self, file, overwrite=True):
		tdir = str(pathlib.Path(file).parent.resolve())
		conts = self.read(file)
		try:
			fileConts = conts[4].split("[[" + "ECP_ARCHZIP_DIVIDER" + "]]") # Weirdify String to allow self archiving
		except:
			print("File is not an archive!")
			return False

		del fileConts[0]

		for x in fileConts:
			file = x[3:x.find('[>]')]
			conts = x[x.find('[>]') + 3::]

			# Write Output
			if not os.path.isfile(tdir + "/" + file) or overwrite: 
				f = open(tdir + "/" + file, "w")
				f.write(str(conts))
				f.close()
				print(file)

		print("Done")
		return True

# Command line
if __name__ == "__main__":
	reader = ecpreader()

	# CMD Argument Parser
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--read", help="Read file", type=str)
	parser.add_argument("-m", "--make", help="Make file", type=str, nargs='+')
	parser.add_argument("-z", "--zip", help="Zip file", type=str)
	parser.add_argument("-uz", "--unzip", help="Unzip file", type=str)
	parser.add_argument("-c", "--convert", help="Convert file", type=str, nargs='+')
	args = parser.parse_args()

	# Read file
	if args.read != None:
		try:
			ret = reader.read(args.read)
			if ret == False:
				print("File not found")
			else:
				print(ret)
		except Exception as e:
			print("Filetype not supported")
			print(e)

	# Make file
	if args.make != None:
		ret = reader.make(args.make[0], args.make[1])

	# Convert file
	if args.convert != None:
		#try:
		reader.convert(args.convert[0], args.convert[1])
		#except:
		#	print("an unexptected error occured!")

	# Archive file
	if args.unzip != None:
		try:
			reader.archive.unzip(args.unzip)
		except:
			print("an unexptected error occured!")