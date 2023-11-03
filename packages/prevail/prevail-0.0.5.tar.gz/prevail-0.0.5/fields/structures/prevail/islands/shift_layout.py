
'''
	1in = 96px
	
	11 * 96 = 1056
'''


def start ():

	return """
function get_position (element) {
	const boundaries = element.getBoundingClientRect ();
	
	return {
		y2: boundaries.top + window.offsetTop
	};
}

tiles = document.querySelectorAll ("[tile]")
pages = document.querySelectorAll ("[page]")
	
for (let s = 0; s < tiles.length - 1; s++) {
	const tile = tiles [s]
	const tile_position = get_position (tile)
	
	console.log (tile, tile_position)
	
	// if past 1056, add to the next page
}
	
	"""