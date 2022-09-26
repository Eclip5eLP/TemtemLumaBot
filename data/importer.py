###################
# Made by Eclip5e #
###################

# Check installed Modules
import sys
import subprocess
import pkg_resources

class Importer:
	@staticmethod
	def verifyLibs(required=None, dl=False):
		if (required == None):
			return True

		installed = {pkg.key for pkg in pkg_resources.working_set}
		missing = required - installed

		if missing:
			print("Missing dependencies:")
			for dep in missing:
				print(dep)
				print("\nPlease install missing dependencies before running")

			if (dl):
				print("Installing dependencies...")
				python = sys.executable
				subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
			else:
				exit()