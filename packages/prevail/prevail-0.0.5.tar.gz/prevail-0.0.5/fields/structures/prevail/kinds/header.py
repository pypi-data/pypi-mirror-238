
'''
import prevail.kinds.header as header
header.build (structure)
'''
from mako.template import Template
import prevail.modules.paragraph as paragraph

def build (structure):
	name = structure ["name"]
	background = structure ["background"]
	summary = structure ["summary"]

	print ("header structure:", structure)

	p1 = paragraph.build (name)
	p2 = paragraph.build (summary)
	
	mytemplate = Template (
f"""<section
	tile
	style="
		position: relative;
		overflow: hidden;
	
		border: .05in solid black;
		border-radius: .1in;
		padding: .25in;
	
		margin-bottom: .1in;
	
		display: flex;
		justify-content: space-between;
		align-items: center;
	"
>
	<img 
		style="
			position: absolute;
			top: 0;
			left: 0;
			
			width: 100%;
			
			opacity: .3;
		"
	
		src="{ background }" 
	/>
		
	<div>
		<label>name</label>
		{ p1 }
	</div>
	
	<div>
		<label>summary</label>
		{ p2 }
	</div>
</section>"""	
	)


	return mytemplate.render (name = name)

