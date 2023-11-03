




'''
import prevail.climate as climate
climate.change ("", {})
'''

'''
import prevail.climate as climate
ports = climate.find ("ports")
'''

import copy

climate = {
	
}

def change (ellipse, planet):
	climate [ ellipse ] = planet


def find (ellipse):
	return copy.deepcopy (climate) [ ellipse ]