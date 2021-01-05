from jinja2 import Template
from audit import Audit
import jinja2
import pdflatex
import json
import os.path


class Report():
    
    def __init__(self, audit):
        self.audit=audit

    def  render(self,template_file):
        latex_jinja_env = jinja2.Environment(
	    block_start_string = '\BLOCK{',
	    block_end_string = '}',
	    variable_start_string = '\VAR{',
    	variable_end_string = '}',
    	comment_start_string = '\#{',
    	comment_end_string = '}',
	    line_statement_prefix = '%%',
	    line_comment_prefix = '%#',
	    trim_blocks = True,
	    autoescape = False,
	    loader = jinja2.FileSystemLoader(os.path.abspath('./template'))
        )
        template = latex_jinja_env.get_template('template.tex.jinja2')
        data = self.audit.serialize()
        print(data)
        f = open(os.path.abspath('./latex/rendered.tex'), "a")
        f.truncate(0)
        f.write(template.render(data))
        f.close()
