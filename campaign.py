
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
        self.launch_date = campaign["launch_date"]
        self.send_by_date = campaign["send_by_date"]
        self.completed_date = campaign["completed_date"]
        self.url = campaign["url"]

    def serialize(self):
        serialized = {}
        serialized['name'] = self.name
        serialized['landing_name'] = self.landing_name
        serialized['landing_html_rendered'] = self.render_html()
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

    def render_html(self):
        date = datetime.datetime.now()
        filename =  date.strftime("%f") + ".png"
        path = './latex/' + filename
        path_wkhtmltoimage = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkhtmltoimage)
        options = {'format':'png','quality':'25'}
        #options = {'enable-local-file-access': True}
        imgkit.from_string(self.landing_html,os.path.abspath(path),config=config,options=options)
        return filename