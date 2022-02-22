from elastic_enterprise_search import AppSearch
from files.sorter import *
import requests, datetime, xmltodict, json

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
    
def get_credits(config:dict, token:str) :
    headers = {"Authorization": "Bearer " + token}
    url = "https://management.azure.com/providers/Microsoft.Billing/billingAccounts/"+ config["subscriptions"]["BillingAccountID"] +"/billingProfiles/" + config["subscriptions"]["BillingProfileID"] + "/providers/Microsoft.Consumption/credits/balanceSummary?api-version=2021-10-01"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json

def get_details_bill(config:dict, token:str) :
    headers = {"Authorization": "Bearer " + token}
    url = "https://management.azure.com/subscriptions/"+ config["subscriptions"]["ID"] +"/providers/Microsoft.Consumption/usageDetails?api-version=2021-10-01"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        return response_json

def list_containers_in_blobs(config:dict) :

    headers = {"x-ms-version":"2020-04-08", "x-ms-date":datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
    array = []
    response_dict = {}

    for account in config["subscriptions"]["StorageAccount"].keys():
        array.append(account)

    for blob in array :
        url = "https://"+ blob +".blob.core.windows.net/"+ config["subscriptions"]["StorageAccount"][blob]+"&comp=list"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = xmltodict.parse(response.content)
            temp = []

            if isinstance(content["EnumerationResults"]["Containers"]["Container"], list) :

                for container in content["EnumerationResults"]["Containers"]["Container"] :
                    temp.append(container["Name"])
            
            else :
                temp.append(content["EnumerationResults"]["Containers"]["Container"]["Name"])

            response_dict[blob] = temp

    return response_dict
    
def send_data_to_elasticsearch(config:dict, engine:str, files:list):
    
    app_search = AppSearch(config["elasticAPI"]["endpoint"], http_auth=config["elasticAPI"]["key"])
    
    try :
        for doc in files :
            app_search.index_documents(engine_name=engine, documents=doc)
    except :
        return "Indexing failed"
    return "Ok"

