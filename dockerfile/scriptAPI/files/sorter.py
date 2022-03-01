import re

def get_All_VM_price(file:dict):
    price = 0
    for item in file["value"] :
        if "virtualMachines" in item["properties"]["instanceName"] :
            price += item["properties"]["costInBillingCurrency"]
        elif "Microsoft.Compute/disks/" in item["properties"]["instanceName"] :
            price += item["properties"]["costInBillingCurrency"]
    return round(price,2)

def get_each_VM_price(file:dict):
    list_vm = {}
    for item in file["value"] :
        if "virtualMachines" in item["properties"]["instanceName"] :
            name = re.search(r'Machines\/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_vm.keys():
                list_vm[name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_vm[name.group(1).lower()] = item["properties"]["costInBillingCurrency"]
                
        elif "Microsoft.Compute/disks/" in item["properties"]["instanceName"] :
            name = re.search(r'disks/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_vm.keys():
                list_vm[name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_vm[name.group(1).lower()] = item["properties"]["costInBillingCurrency"]

    for vm in list_vm.keys():
        list_vm[vm] = round(list_vm[vm],2)
        
    return list_vm
    
def get_each_VM_price_per_day(file:dict):
    list_day = {}
    for item in file["value"] :
        date = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',item["properties"]["date"])
        date = date.group(0)
        
        if not date in list_day.keys():
            list_day[date] = {}

        if "virtualMachines" in item["properties"]["instanceName"] :
            name = re.search(r'Machines\/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_day[date].keys():
                list_day[date][name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_day[date][name.group(1).lower()] = item["properties"]["costInBillingCurrency"]
                
        elif "Microsoft.Compute/disks/" in item["properties"]["instanceName"] :
            name = re.search(r'disks/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_day[date].keys():
                list_day[date][name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_day[date][name.group(1).lower()] = item["properties"]["costInBillingCurrency"]

    for day in list_day.values():
        for vm in day.keys() :
            day[vm] = round(day[vm],2)

    return list_day

def make_VM_final_document(file:dict):
    bill = get_each_VM_price_per_day(file)
    doc_array = []

    for date in bill.keys() :
        tmp_dic = {"id":date,"date":date}

        for vm in bill[date].keys() :
            tmp_dic[vm] = bill[date][vm]    
        
        doc_array.append(tmp_dic)

    return doc_array

def format_blob_data(file:dict):
    list_day = {}
    for item in file["value"] :
        date = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',item["properties"]["date"])
        date = date.group(0)

        if not date in list_day.keys():
            list_day[date] = {}

        if "storageAccounts" in item["properties"]["instanceName"] :

            blob = re.search(r'Accounts\/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            blob = blob.group(1).lower()

            if blob not in list_day[date].keys():
                list_day[date][blob] = {"price":0}
            
            if "Bandwidth" == item["properties"]["meterCategory"] :
                list_day[date][blob]["price"] += item["properties"]["costInBillingCurrency"]

            elif "Storage" == item["properties"]["meterCategory"] :
                list_day[date][blob]["price"] += item["properties"]["costInBillingCurrency"]

    return list_day

def make_blob_final_document(file:dict):
    
    list_day = format_blob_data(file)

    array=[]
    for date in list_day.keys() :
        tmp_dict = {"id":date, "date":date}
        for account in list_day[date].keys() :
            tmp_dict[account] = list_day[date][account]["price"]
        array.append(tmp_dict)

    return array

def get_each_container_price_per_day(file:dict):
    list_day = {}
    for item in file["value"] :
        date = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',item["properties"]["date"])
        date = date.group(0)
        
        if not date in list_day.keys():
            list_day[date] = {}

        if "containerGroups" in item["properties"]["instanceName"] :
            name = re.search(r'containerGroups\/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_day[date].keys():
                list_day[date][name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_day[date][name.group(1).lower()] = item["properties"]["costInBillingCurrency"]

    for day in list_day.values():
        for vm in day.keys() :
            day[vm] = round(day[vm],2)

    return list_day

def make_container_final_document(file:dict):
    bill = get_each_container_price_per_day(file)
    doc_array = []

    for date in bill.keys() :
        tmp_dic = {"id":date,"date":date}

        for vm in bill[date].keys() :
            tmp_dic[vm] = bill[date][vm]    
        
        doc_array.append(tmp_dic)

    return doc_array

def merge_docs(docs:list):
    final_docs = docs[0]
    lenght = len(docs)
    for lst in docs[1:lenght]:
        for doc in lst :
            for final_date in final_docs :
                if doc["date"] in final_date["date"] :
                    final_date.update(doc)
                else :
                    continue
    
    return final_docs
        
def get_each_eventhub_per_day(file:dict):

    list_day = {}
    for item in file["value"] :
        date = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',item["properties"]["date"])
        date = date.group(0)
        
        if not date in list_day.keys():
            list_day[date] = {}

        if "EventHub" in item["properties"]["instanceName"] :
            name = re.search(r'EventHub\/namespaces\/([a-zA-Z0-9]{1,255})', item["properties"]["instanceName"])
            if name.group(1).lower() in list_day[date].keys():
                list_day[date][name.group(1).lower()] += item["properties"]["costInBillingCurrency"]
            else :
                list_day[date][name.group(1).lower()] = item["properties"]["costInBillingCurrency"]

    for day in list_day.values():
        for eventhub in day.keys() :
            day[eventhub] = round(day[eventhub],2)

    return list_day

def make_eventhub_final_document(file:dict):
    bill = get_each_eventhub_per_day(file)
    doc_array = []

    for date in bill.keys() :
        tmp_dic = {"id":date,"date":date}

        for eventhub in bill[date].keys() :
            tmp_dic[eventhub] = bill[date][eventhub]    
        
        doc_array.append(tmp_dic)

    return doc_array