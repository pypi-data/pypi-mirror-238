
'''
import prevail.photo.build as photo_builder
'''


import base64

def start (path):
    extension = path.split ('.') [-1]
    format = f'data:image/{extension};base64,'
	
    with open (path, 'rb') as fp:
        photo = fp.read ()
		
    return format + base64.b64encode (photo).decode ('utf-8')
