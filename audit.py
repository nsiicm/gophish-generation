##############################################################
#Class to manage an audit (multiple campaigns for 1 customer)#
##############################################################

import json
from api import *
from campaign import Campaign

class Audit():

    campaigns = []
    prefix =""

    def __init__(self, client_name):
        self.prefix = client_name # Define prefix of campaigns name to allow identification of customer 
        self.__sort_campaigns() # Use prefix to keep only the campaigns of the righ customer
        
    def __sort_campaigns(self):
        api = Api() # Initialize the API
        campaigns_response = api.request("/api/campaigns/") #Request the camapaigns to the API
        for campaign_response in campaigns_response:
            if self.prefix in campaign_response['name']:# Check ih the campaign match the customer
                campaign = Campaign(campaign_response)#Create campaign an append to the list of campaigns
                self.campaigns.append(campaign)
    #returns the number of campaigns that match the filter
    def len(self):
        return len(self.campaigns)

    #Return a list of campaigns name
    def get_names(self):
        names = []
        for campaign in self.campaigns:
            names.append(campaign.name)
        return names

    #Format the data for jinja2 exploitation
    def serialize(self):
        serialized = {}
        serialized['prefix'] = self.prefix
        serialized['campaigns'] = []
        for campaign in self.campaigns:
            serialized['campaigns'].append(campaign.serialize())
        return serialized
