



def introduce (fields):
	name = fields ['name']

	this_template = Template ("""
<article
	tile
	style="
		border: .05in solid black;
		border-radius: .1in;
		padding: .25in;
		margin-bottom: .1in;
	"
>
	<header>
		<h1>${ name }</h1>	
	</header>
	<p style="white-space: pre-wrap;">${ summary }</p>
</article>
	""")
	
	return this_template.render (
		name = name,
		summary = summary
	)