
'''
import prevail.modules.tile as tile
'''

import pathlib
from os.path import dirname, join, normpath
import sys
this_folder = pathlib.Path (__file__).parent.resolve ()	
template = normpath (join (this_folder, "Avila.png"))

def build (
	paragraph
):
	from mako.template import Template

	mytemplate = Template (filename = template)
	print(mytemplate.render())

	return;