





#
#	cp module.r.html module.txt
#	(rm -rf dist && python3 -m build --sdist && twine upload dist/*)
#


#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages
from glob import glob


def scan_description ():
	try:
		with open ('module.txt') as f:
			return f.read ()

	except Exception as E:
		pass;
		
	return '';


name = "cyte"

structures = 'lovely/structures'
structure = structures + '/' + name
script = structures + '/' + 'scripts/cyte' 

setup (
    name = name,
	description = "Measurements (System International, US Customary, etc.)",
    version = "0.2.7",
    install_requires = [
		"botanical",
		"pydash",
		"requests",
		"tinydb"
	],	
	
	package_dir = { 
		"cyte": structure
	},
	
	#
	#	PACKAGE DATA
	#
	package_data = {
		structures: [ "*.HTML" ],
		"": [ "*.HTML" ],
		"": [ "*.json" ]
    },
	include_package_data = True,
	
	project_urls = {
		"GitLab": "https://gitlab.com/reptilian_climates/cyte.git"
	},
	
	#scripts = [ 
	#	SCRIPT
	#],
	
	license = "the health license",
	long_description = scan_description (),
	long_description_content_type = "text/plain"
)

