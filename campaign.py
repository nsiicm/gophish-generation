import jinja2
from jinja2 import Template
import json
import imgkit
import pdfkit
import os
from datetime import datetime
import codecs


class Campaign:

   # results= []

    

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
        self.critical = 0
        self.events_timeline(campaign["timeline"])

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
        serialized['timeline'] = self.events
        serialized['critical'] = self.critical
        print(self.name)
        print(self.stat)
        return serialized

    def render_email(self):
        date = datetime.now()
        filename = date.strftime("%f") + '.jinja2'
        path = './template/' + filename
        f = codecs.open(os.path.abspath(path), "a", encoding='utf8')
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
        actual_date = datetime.now()
        filename =  actual_date.strftime("%f") + ".png"
        path = './latex/' + filename
        path_wkhtmltoimage = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkhtmltoimage)
        options = {'disable-local-file-access': "", 'load-error-handling' : 'skip', 'load-media-error-handling' : 'skip'}
        #options = {'enable-local-file-access': True}
        try :
            imgkit.from_string(html,os.path.abspath(path),config=config,options=options)
        except:
            print("Erreur au cours du rendu")
        
        return filename

    def calc_stats(self, results):
        self.stat = {}
        self.stat_perc = {}
        self.stat["sent"] = 0
        self.stat["opened"] = 0
        self.stat["clicked"] = 0
        self.stat["submitted"] = 0
        print(self.stat["opened"])
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
        

    def events_timeline(self,eventlist):
        self.events = []
        mintimestamp = 999999999999999999
        maxtimestamp = 0
        for event in eventlist:
            if event["message"] != "Campaign Created":
                eventtimestamp = datetime.fromisoformat(event["time"][:-1]).timestamp()
                if eventtimestamp > maxtimestamp:
                    maxtimestamp = eventtimestamp
                if mintimestamp > eventtimestamp:
                    mintimestamp = eventtimestamp

        timestamp = maxtimestamp - mintimestamp
        for event in eventlist:
            if event["message"] != "Campaign Created":
                event_timestamp = datetime.fromisoformat(event["time"][:-1]).timestamp() - mintimestamp
                time = (100 / (timestamp)) * (event_timestamp)
                if 'Sent' in event["message"]:
                    status = "sent"
                elif 'Opened' in event["message"]:
                    status = "opened"
                elif event["message"] == 'Clicked Link':
                    status = "clicked"
                elif event["message"] == 'Submitted Data':
                    status = 'submitted'
                    self.critical_data(event["details"],event["email"])
                else:
                    status = "aaaaaa"
                eventdict = {'adv' : str(round(time,1)), 'status' : status  }
            #"{'adv' : " + str(int(time)) + ",'status' : '" + status + "'}"
                self.events.append(eventdict)
                print(self.stat["opened"])

    def critical_data(self,event_detail,event_email):
        email_split = event_email.split('@')
        username_split = email_split[0].split('.')
        detail = json.loads(event_detail)
        login = detail['payload']['loginfmt'][0]
        if email_split[0] in login or email_split[1] in login or event_email in login or login in username_split:
            self.critical += 1