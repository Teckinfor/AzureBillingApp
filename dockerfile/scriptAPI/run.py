#######################################
############ Version 1.4.1 ############
#######################################

from files.apicalls import *
from files.sorter import *
from time import sleep
import json, sys, os , re

def generate_config () :
    config =   {
                    "subscriptions":{
                        "ID":os.getenv("SubscriptionID"),
                        "BillingProfileID":os.getenv("BillingProfileID"),
                        "BillingAccountID":os.getenv("BillingAccountID"),
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


if __name__ == "__main__":

    config = generate_config()

    while(True):

        try :
            token = get_authorization(config)
        
            if token != NO_TOKEN :
            
                # Get all bill informations
                bill = get_details_bill(config, token)
    
                # VM billing
                VM_doc = make_VM_final_document(bill)
    
                # Blob stats and billing
                Blob_doc = make_blob_final_document(bill)
    
                # Container Instance billing
                Container_doc = make_container_final_document(bill)
    
                # EventHub billing
                EventHub_doc = make_eventhub_final_document(bill)
    
                # Merge all documents
                Resume_doc = merge_docs([VM_doc, Blob_doc, Container_doc, EventHub_doc])
    
                # Send Data to elastic enterprise search
                try :
                    send_data_to_elasticsearch(config, config["elasticAPI"]["engine-name"], Resume_doc)
                except :
                    continue
                
                sleep(3600) # 1h

        except :
            continue
