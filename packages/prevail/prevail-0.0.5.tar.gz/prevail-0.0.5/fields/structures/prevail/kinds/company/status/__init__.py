
def INTRODUCE_PLACES (PLACES):
	START = ("""
	<section>
		<h3>places</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for PLACE in PLACES:
		STRING += (
f"""			<li>{ PLACE }</li>"""
		)
	
	
	

	return START + STRING + END;
	
	
def INTRODUCE_DATES (DATES):
	START = ("""
	<section>
		<h3>dates</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for DATE in DATES:
		STRING += (
f"""			<li>{ DATE }</li>"""
		)
	
	
	

	return START + STRING + END;
	
	
def INTRODUCE_FEATS (FEATS):
	START = ("""
	<section>
		<h3>feats</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for FEAT in FEATS:
		STRING += (
f"""			<li>{ FEAT }</li>"""
		)

	return START + STRING + END;

def INTRODUCE_NAMES (NAMES):
	STRING = ""
	for NAME in NAMES:
		STRING += (f"""
			<li>{ NAME }</li>		
		""")

	return STRING

def INTRODUCE (OBJECT):
	print ("STATUS", OBJECT)

	NAMES = OBJECT ["names"]

	START = (
	f"""
<article
	style="
		border: .05in solid black;
		border-radius: .1in;
		padding: .25in;
		
		margin-bottom: .1in;
	"
>
	<header>
		<h3>Statuses</h3>
		<h1>
			<ul>
				{ INTRODUCE_NAMES (NAMES) }
			</ul>
		</h1>	
	</header>
""")

	END = (
f"""
</article>"""	
	)	

	STRING = ""

	if ("places" in OBJECT):
		STRING += INTRODUCE_PLACES (OBJECT ["places"])
		
	if ("dates" in OBJECT):
		STRING += INTRODUCE_DATES (OBJECT ["dates"])
		
	if ("feats" in OBJECT):
		STRING += INTRODUCE_DATES (OBJECT ["feats"])

	return START + STRING + END;