import jinja2
from jinja2 import Template
import datetime
import imgkit
import pdfkit
import os


class Campaign:

    results= []
    stat = {}
    stat_perc = {}

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
        self.calc_stats(campaign["results"])

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
        serialized['stat'] = self.stat
        serialized['stat_perc'] = self.stat_perc
        serialized['url'] = self.url
 #       serialized['sent'] = self.sent
 #       serialized['opened'] = self.opened
 #       serialized['clicked'] = self.clicked
 #       serialized['submitted'] = self.submitted
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

    def calc_stats(self, results):
        self.stat["sent"] = 0
        self.stat["opened"] = 0
        self.stat["clicked"] = 0
        self.stat["submitted"] = 0
        for result in results:
            if result["status"] == 'Email Sent' or result["status"] == 'Email Opened' or result["status"] == 'Clicked Link' or result["status"] == 'Submitted Data' :
                self.stat["sent"] += 1
            if result["status"] == 'Email Opened' or result["status"] == 'Clicked Link' or result["status"] == 'Submitted Data':
                self.stat["opened"] += 1
            if result["status"] == 'Clicked Link' or result["status"] == 'Submitted Data':
                self.stat["clicked"] += 1
            if result["status"] == 'Submitted Data':
                self.stat["submitted"] += 1
        self.stat_perc["sent"] = 100
        self.stat_perc["opened"] = 100 / self.stat["sent"] * self.stat["opened"]
        self.stat_perc["clicked"] = 100 / self.stat["sent"] * self.stat["clicked"]
        self.stat_perc["submitted"] = 100 / self.stat["sent"] * self.stat["submitted"]