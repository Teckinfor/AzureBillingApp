#######################################
############ Version 1.5.2 ############
##### Please, read the README.md ######
#######################################

from files.apicalls import *
from files.sorter import *
from time import sleep
import json, sys, os

def check_configuration () :
    file = open("config.json")
    config = json.load(file)
    file.close()
    return config  

def generate_config () :
    config =   {
                    "subscriptions":{
                        "ID":os.getenv("SubscriptionID"),
                        "App":{
                            "ApplicationID":os.getenv("ApplicationID"),
                            "TenantID":os.getenv("TenantID"),
                            "secret":os.getenv("Appsecret")
                        },
                    },

                    "elasticAPI":{
                        "endpoint":os.getenv("Elastic_endpoint"),
                        "key":os.getenv("Elastic_key"),
                        "engine-name":os.getenv("Elastic_enginename")
                    }
                }
    
    return config


if __name__ == "__main__" :

    if len(sys.argv) > 1 :
        config = generate_config()

    else :
        config = check_configuration()

    while(True):

        try :
            token = get_authorization(config)
        
            if token != NO_TOKEN :
            
                #Get all bill informations
                bill = get_details_bill(config, token)
    
                #VM billing
                VM_doc = make_VM_final_document(bill)
    
                #Blob stats and billing
                Blob_doc = make_blob_final_document(bill)
    
                #Container Instance billing
                Container_doc = make_container_final_document(bill)
    
                #EventHub billing
                EventHub_doc = make_eventhub_final_document(bill)
    
                #Merge all documents
                Resume_doc = merge_docs([VM_doc, Blob_doc, Container_doc, EventHub_doc])
    
                #Send Data to elastic enterprise search
                try :
                    send_data_to_elasticsearch(config, config["elasticAPI"]["engine-name"], Resume_doc)
                except :
                    continue
                
                sleep(3600) # 1h

            json_object = json.dumps(Resume_doc, indent = 4)
            with open("sample.json", "w") as outfile:
                outfile.write(json_object)

        except :
            continue
