




import prevail.kinds.company.status as STATUS

def introduce (fields):
	NAME = fields ["name"]
	STATUSES = fields ["statuses"]
	
	START = (
	f"""
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
		<h1>{ NAME }</h1>	
	</header>
""")

	END = (
f"""
</article>"""	
	)
	
	STRING = ""
	
	for _STATUS in STATUSES:
		STRING += STATUS.INTRODUCE (_STATUS)
	
	
	
	
	return START + STRING + END;