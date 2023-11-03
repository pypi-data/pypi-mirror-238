
'''
import prevail.modules.paragraph as paragraph
paragraph.build ("this is a paragraph")
'''

import pathlib
from os.path import dirname, join, normpath
import sys
this_folder = pathlib.Path (__file__).parent.resolve ()	
template = normpath (join (this_folder, "template.html"))

from mako.template import Template

def build (
	paragraph,
	size = "1.3em"
):
	return Template (filename = template).render (
		paragraph = paragraph,
		size = size
	)