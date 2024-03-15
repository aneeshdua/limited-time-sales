from typing import Union
from fastapi import FastAPI, Query, Body, Request
import json
import datetime
from types import SimpleNamespace

from deal import Deal
from item import Item
from order import DealClaims

import storageOps

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/createDeal")
async def create_deal(request: Request):
    body = await request.json()
    latestDeal = Deal(body["startTime"],endTime=body["endTime"],itemList=body["items"])
    storageOps.dumpDealtoStorage(latestDeal)
    #return {"dealId": latestDeal.dealId}
    return json.dumps(latestDeal, default=storageOps.customSerialize)

@app.patch("/updateDeal")
async def update_deal(request: Request):
    # add a check if deal already exists
    body = await request.json()
    latestDeal = Deal(startTime=body["startTime"],endTime=body["endTime"],itemList=body["items"], dealId=body["dealId"])
    storageOps.dumpDealtoStorage(latestDeal)
    return json.dumps(latestDeal, default=storageOps.customSerialize)
    #return {"dealId": latestDeal.dealId}


@app.post("/claimDeal")
async def claim_deal(request: Request):
    body = await request.json()
    newClaim = DealClaims(dealId=body["dealId"], userId=body["userId"], itemId=body["itemId"])
    
    # Check 1 request time within deal range
    dealJson = storageOps.getDealFromStorage(newClaim.dealId)
    deal = Deal(**dealJson)
    if datetime.datetime.now()< deal.startTime or datetime.datetime.now() > deal.endTime:
        return {"invalid. Deal not active"}
    # Check 2 if user already took deal
    elif storageOps.checkIfFileExists("storage/orders/"+newClaim.getKey()+".json"):
        return {"Invalid. Deal already claimed by user."}
    # Check 2 if stock is over
    elif deal.itemList[newClaim.itemId] ==0:
        return {"Invalid. Stock over for requested item."}
    else:
        # valid order
        # decrement inventory and add order to storage
        deal.itemList[newClaim.itemId] -= 1
        storageOps.dumpDealtoStorage(deal) 
        fileName= "storage/orders/"+newClaim.getKey()+".json"
        storageOps.dumpDatatoStorage(fileName,newClaim)
        return json.dumps(newClaim, default=storageOps.customSerialize)
