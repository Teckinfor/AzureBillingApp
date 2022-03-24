from elastic_enterprise_search import AppSearch
from files.sorter import *
import requests

NO_TOKEN = {"Error":"Impossible to get an authorization"}

def get_authorization(config:dict) :
    url = 'https://login.microsoftonline.com/' + config["subscriptions"]["App"]["TenantID"] + '/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type':'client_credentials','client_id':config["subscriptions"]["App"]["ApplicationID"],'client_secret':config["subscriptions"]["App"]["secret"],'resource':'https://management.azure.com'}

    try :
        authorization = requests.post(url, data=data, headers=headers)
        if authorization.status_code == 200 :
            authorization_json = authorization.json()
    except :
        return NO_TOKEN

    return authorization_json["access_token"]  

def get_details_bill(config:dict, token:str) :
    headers = {"Authorization": "Bearer " + token}
    url = "https://management.azure.com/subscriptions/"+ config["subscriptions"]["ID"] +"/providers/Microsoft.Consumption/usageDetails?api-version=2021-10-01"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    
def send_data_to_elasticsearch(config:dict, engine:str, files:list):
    
    app_search = AppSearch(config["elasticAPI"]["endpoint"], http_auth=config["elasticAPI"]["key"])
    
    try :
        for doc in files :
            app_search.index_documents(engine_name=engine, documents=doc)
    except :
        return "Indexing failed"
    return "Ok"
