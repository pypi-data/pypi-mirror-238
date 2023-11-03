



def build ():
	html_document = {
		"start": (
"""
<html>
<head></head>
<body>
<style>
h1, h2, h3, p, ul, li {
	margin: 0;
	padding: 0;
}

ul {
	padding-left: 20px;
}

main {
	position: relative;
	margin: 0 auto;
	width: 8.5in;
	height: 11in;
}

</style>
<main>
	<article page>
"""),
		"main": "",
		"end": (
"""
	</article>
</main>
<script>
document.addEventListener("DOMContentLoaded", function(event) {

	
	
});
</script>
</body>
""")
	}
	
	return html_document