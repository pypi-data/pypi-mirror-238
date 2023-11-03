

'''
plan:

import prevail

prevail.abundantly ({
	"build": [{
		"kind": "header"
	}]
})

'''

import prevail.kinds.header as header
import prevail.kinds.company as company
import prevail.kinds.project as project

import prevail.modules.document as document

from flask import Flask

def abundantly (OBJECT):
	BUILDS = OBJECT ["build"]
	
	html_document = document.build ()

	for structure in BUILDS:
		kind = structure ["kind"]
		fields = structure ["fields"]
		
		if (kind == "header"):
			html_document ["main"] += header.build (fields)
		
		elif (kind == "company"):
			html_document ["main"] += company.introduce (fields)
		
		elif (kind == "academics"):
			pass;
			
		elif (kind == "projects"):
			html_document ["main"] += project.present (fields)
			
		else:
			print (f'Kind "{ kind }" is not an option.')
			

	html_string = (
		html_document ["start"] + 
		html_document ["main"] + 
		html_document ["end"]
	)


	app = Flask (__name__)
	
	'''
	@app.route ("/picture.png")
	def picture ():
		return html_string
	'''
	
	@app.route ("/")
	def prevail ():
		return html_string

	app.run (
		debug = True
	)

	return;