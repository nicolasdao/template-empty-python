import configparser
import sys
import subprocess
import re
import os
from functools import partial
from pip._vendor import pkg_resources

# Defines constants
SETUP_FILE = 'setup.cfg'
LIB_COMPARATOR_REGEX = r'[>=<\n\s,]'
GLOBAL_REQUIREMENTS = 'requirements.txt'
PROD_REQUIREMENTS = 'prod-requirements.txt'
FREEZE = ('pip', 'freeze', '>')
PROD_SECTION = 'options'
PROD_SECTION_REQUIRE = 'install_requires'
DEV_SECTION = 'options.extras_require'
DEV_SECTION_REQUIRE = 'dev'

# Gets the terminal inputs
_, *libs = sys.argv

# Exists if no inputs were provided
if not(len(libs)):
	exit()

# Filters the inputs between libraries and options (e.g., -D for dev dependencies)
libDefs = []
options = []
for lib in libs:
	tar = options if re.search(r'^-', lib) else libDefs
	tar.append(lib)

def getItems(s=''):
	if not s:
		return ([],[])
	'''Gets the unique items in a list where the separator is a new line'''
	items = list(set(x for x in re.split('\n', s) if x))
	names = [getLibNameOnly(x) for x in items]
	return (items, names)

def getConfig(config, section, property):
	val = '' if section not in config or property not in config[section] else config[section][property]	
	val = val if val else ''
	return val

def initConfig(config, section, property):
	'''Makes sure that config[section][property] exists.'''
	if (section not in config):
		config[section] = {}
	if (property not in config[section]):
		config[section][property] = ''

def find(val, items):
	return next((x for x in items if val in x), None)

def getLibNameOnly(lib=''):
	return [x for  x in re.split(LIB_COMPARATOR_REGEX, lib) if x][0].strip()

def getPackageDeps(lib):
	'''Gets a package's dependencies withouth their versions'''
	_package = pkg_resources.working_set.by_key[lib]
	return [getLibNameOnly(str(r)) for r in _package.requires()]

def main():
	'''Main program'''
	
	# Reads the 'setup.cfg' file
	config = configparser.ConfigParser()
	config.read(SETUP_FILE)
	dev = '-D' in options
	uninstall = '-u' in options
	prodDeps, prodNames = getItems(getConfig(config, PROD_SECTION, PROD_SECTION_REQUIRE))
	devDeps, devNames = getItems(getConfig(config, DEV_SECTION, DEV_SECTION_REQUIRE))

	prodChanged = False
	devChanged = False
	for lib in libDefs:
		# Gets the library that must be installed without its version
		name = getLibNameOnly(lib)
		cleanName = re.sub(r",\s*$", '', lib)
		if not name:
			continue

		existingProdName = find(name, prodDeps)
		existingDevName = find(name, devDeps)

		if uninstall: 
			if existingProdName:
				prodChanged = True
				prodDeps.remove(existingProdName)
			if existingDevName:
				devChanged = True
				devDeps.remove(existingDevName)
			uninstall(name)
		else:
			if existingProdName or existingDevName:
				pass
			if dev:
				if existingDevName or existingProdName:
					pass
				else:
					devChanged = True
					devDeps.append(cleanName)
			else:
				if existingProdName:
					pass
				else:
					if existingDevName:
						# If the dep is already in dev, remove it from there and add it to prod
						devChanged = True
						devDeps.remove(existingDevName)
						uninstall(name)
						
					prodChanged = True
					prodDeps.append(cleanName)
			install(lib)

	if prodChanged:
		initConfig(config, PROD_SECTION, PROD_SECTION_REQUIRE)
		if len(prodDeps):
			config[PROD_SECTION][PROD_SECTION_REQUIRE] = '\n' + '\n'.join(prodDeps)
		else:
			del config[PROD_SECTION][PROD_SECTION_REQUIRE]
	if devChanged:
		initConfig(config, DEV_SECTION, DEV_SECTION_REQUIRE)
		if len(devDeps):
			config[DEV_SECTION][DEV_SECTION_REQUIRE] = '\n' + '\n'.join(devDeps)
		else:
			del config[DEV_SECTION][DEV_SECTION_REQUIRE]

	with open(SETUP_FILE, 'w') as configfile:
		config.write(configfile)

def install(lib, dev=False):
	'''
	Installs library 'lib' and freeze the dependencies into requirements.txt 
	and prod-requirements.txt (if the dev mode is not on). The strategy used to 
	install the new dependencies in prod mode is as follow:
	1.	Gets all the dependencies (incl. the lib itself).
	2.	Add or update those dependencies in prod-requirements.txt.

		Parameters:
			lib (string):	e.g., 'numpy' or 'flake8==6.0.0'.
			dev (boolean):	Default False. When False, the prod-requirements.txt is also updated.
	'''
	subprocess.check_call('pip', 'install', lib)
	subprocess.check_call(*FREEZE, GLOBAL_REQUIREMENTS)
	if not dev:
		deps = getExactDeps(requirements, lib)
		if len(deps):
			with open(PROD_REQUIREMENTS, 'w') as pfile: 
				prodRequirements = getFileContent(PROD_REQUIREMENTS)
				prodDeps, prodNames = getItems(prodRequirements)
				for dependency in deps:
					libName = getLibNameOnly(dependency)
					if libName not in prodNames:
						prodDeps.append(dependency)
					else:
						prodDeps[prodNames.index(libName)] = dependency
				prodDeps = list(set(prodDeps))
				prodDeps.sort()
				pfile.write('\n'.join(prodDeps))

def uninstall(lib):
	'''
	Uninstalls library 'lib' and freeze the dependencies in both requirements.txt and prod-requirements.txt.
	The strategy used to uninstall the dependencies in prod mode is as follow:
	1.	Check which dependencies were removed from requirements.txt. It's safer to do that rather than
		checking the lib's dependencies explicitly, as some shared dependencies may not have been removed.
	2.	Remove the dependencies from prod-requirements.txt.

		Parameters:
			lib (string):	e.g., 'numpy' or 'flake8==6.0.0'.
	'''
	oldRequirements = getFileContent(GLOBAL_REQUIREMENTS)
	subprocess.check_call('pip', 'uninstall', lib, '-y')
	subprocess.check_call(*FREEZE, GLOBAL_REQUIREMENTS)
	newRequirements = getFileContent(GLOBAL_REQUIREMENTS)
	deletedLines = getDeletedLines(oldRequirements, newRequirements)
	if len(deletedLines):
		with open(PROD_REQUIREMENTS, 'w') as pfile: 
			oldProdRequirements = getFileContent(PROD_REQUIREMENTS)
			prodLines = oldProdRequirements.split('\n')
			newProdLines = []
			for line in prodLines:
				if line not in deletedLines:
					newProdLines.append(line)
			newProdLines = list(set(newProdLines))
			newProdLines.sort()
			pfile.write('\n'.join(newProdLines))

def getFileContent(file):
	content = ''
	if not file:
		return content

	if os.path.exists(file):
		with open(file) as f:
			content = f.read()

	return content

def getDiffLines(oldContent='', newContent='', mode='new'):
	oldLines = oldContent.split('\n')
	newLines = newContent.split('\n')
	lines = []
	ls1, ls2 = (newLines, oldContent) if mode == 'new' else (oldContent, newLines)
	for line in ls1:
		if line not in ls2:
			lines.append(line)
	return lines

def getExactDeps(requirementsContent, lib):
	requirements = requirementsContent.split('\n')
	deps = getPackageDeps(lib)
	libName = getLibNameOnly(lib)
	deps.append(libName)
	exactDeps = []
	findDeps = partial(find, items=requirements)
	for dep in deps:
		fullName = findDeps(dep)
		if fullName:
			exactDeps.append(fullName)
	exactDeps.sort()
	return exactDeps

getNewLines = partial(getDiffLines, mode='new')
getDeletedLines = partial(getDiffLines, mode='deleted')


if __name__ == '__main__':
	main()