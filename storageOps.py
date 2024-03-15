import json
import datetime
import os
from item import Item
from deal import Deal

def customSerialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Item):
        serial = obj.__dict__
        return serial
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    return obj.__dict__

def dumpDealtoStorage(deal: Deal):
    fileName= "storage/deals/"+str(deal.dealId)+".json"
    file = open(fileName,"w")
    json.dump(deal.__dict__,file, default = customSerialize)

def dumpDatatoStorage(fileName: str, data):
    #fileName= "storage/deals/"+str(deal.dealId)+".json"
    file = open(fileName,"w")
    json.dump(data.__dict__,file, default = customSerialize)

def checkIfFileExists(filenameWithPath: str):
    return os.path.isfile(filenameWithPath)


def getDealFromStorage(dealId: str):
    fileName= "storage/deals/"+dealId+".json"
    file = open(fileName,"r")
    data = json.load(file)
    file.close()
    return data