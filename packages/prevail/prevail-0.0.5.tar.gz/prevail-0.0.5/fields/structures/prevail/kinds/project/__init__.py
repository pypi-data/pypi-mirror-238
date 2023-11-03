

'''
{
	"kind": "projects",
	"fields": {
		"name": "project 1",
		"summary": ""
	}
}
'''

'''
import prevail.kinds.project as project
project.preset ({
	"name": "",
	"description": ""
})
'''

from mako.template import Template



def present (fields):
	name = fields ['name']
	summary = fields ['summary']
	
	if (type (summary) == list):
		summary = "\n".join (summary)
	
	
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
	
	
	
	
	
	
	
	
#