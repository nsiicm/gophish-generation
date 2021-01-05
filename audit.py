import json
from api import *
from campaign import Campaign

class Audit():

    campaigns = []
    prefix =""

    def __init__(self, client_name):
        self.prefix = client_name
        self.__sort_campaigns()
        
    def __sort_campaigns(self):
        api = Api()
        campaigns_response = api.request("/api/campaigns/")
        for campaign_response in campaigns_response:
            if self.prefix in campaign_response['name']:
                campaign = Campaign(campaign_response)
                self.campaigns.append(campaign)

    def len(self):
        return len(self.campaigns)

    def get_names(self):
        names = []
        for campaign in self.campaigns:
            names.append(campaign.name)
        return names

    def serialize(self):
        serialized = {}
        serialized['prefix'] = self.prefix
        serialized['campaigns'] = []
        for campaign in self.campaigns:
            serialized['campaigns'].append(campaign.serialize())
        return serialized
