import jinja2
from jinja2 import Template
import datetime
import imgkit
import pdfkit
from api import *
import os


class Campaign:



    def __init__(self, campaign):
        self.name = campaign["name"].replace("_"," ")
        self.id = campaign["id"]
        self.landing_html = campaign["page"]["html"]
        self.landing_name = campaign["page"]["name"]
        self.landing_credentials = campaign["page"]["capture_credentials"]
        self.landing_passwords = campaign["page"]["capture_passwords"]
        self.landing_redirect = campaign["page"]["redirect_url"]
        self.mail_html = campaign["template"]["html"]
        self.mail_name = campaign["template"]["name"]
        self.mail_subject = campaign["template"]["subject"]
        self.launch_date = campaign["launch_date"]
        self.send_by_date = campaign["send_by_date"]
        self.completed_date = campaign["completed_date"]
        self.url = campaign["url"]

    def serialize(self):
        serialized = {}
        serialized['name'] = self.name
        serialized['landing_name'] = self.landing_name
        serialized['landing_html_rendered'] = self.render_html(self.landing_html)
        serialized['email_html_rendered'] = self.render_email()
        serialized['email_name'] = self.mail_name
        serialized['email_subject'] = self.mail_subject
        serialized['redirect'] = self.landing_redirect
        if self.landing_credentials:
            serialized['credentials'] = 'Oui'
        else :
            serialized['credentials'] = 'Non'
        if self.landing_passwords:
            serialized['passwords'] = 'Oui'
        else:
            serialized['passwords'] = 'Non'
        serialized['launch_date'] = self.launch_date
        serialized['send_by_date'] = self.send_by_date
        serialized['completed_date'] = self.completed_date
        serialized['url'] = self.url
        return serialized

    def render_email(self):
        date = datetime.datetime.now()
        filename = date.strftime("%f") + '.jinja2'
        path = './template/' + filename
        f = open(os.path.abspath(path), "a")
        f.write(self.mail_html)
        f.close()
        latex_jinja_env = jinja2.Environment(
        variable_start_string = '{{.',
    	variable_end_string = '}}',
	    trim_blocks = True,
	    autoescape = False,
	    loader = jinja2.FileSystemLoader(os.path.abspath('./template'))
        )
        template = latex_jinja_env.get_template(filename)
        html = template.render({'FirstName' : 'FirstName', "LastName" : "LastName", "Email" : "lastname@domain.com", "Position" : "position", "RId" : "Rid", "From":"From"})
        os.remove(os.path.abspath(path))
        return self.render_html(html)

    def render_html(self,html):
        date = datetime.datetime.now()
        filename =  date.strftime("%f") + ".png"
        path = './latex/' + filename
        path_wkhtmltoimage = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkhtmltoimage)
        options = {'enable-local-file-access': ""}
        #options = {'enable-local-file-access': True}
        imgkit.from_string(html,os.path.abspath(path),config=config,options=options)
        return filename

