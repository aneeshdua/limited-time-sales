import datetime
import uuid

from item import Item

class Deal:
    def __init__(self,startTime: datetime.datetime,endTime: datetime.datetime,itemList: dict, dealId = uuid.uuid4().hex):
        self.startTime = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
        self.endTime = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")
        # self.startTime = startTime
        # self.endTime = endTime
        self.itemList = {}
        for key,value in itemList.items():
            # newItem = Item(**item)
            newItem = Item(id=key,stockCount=value)
            self.itemList[newItem.id] = newItem.stockCount
        # for i in range(len(itemList)):
        #     #newItem = Item(itemList[i].id, itemList[i].stockCount)
        #     newItem = Item(**itemList[i])
        #     self.itemList[newItem.id] = newItem.stockCount
        self.dealId = dealId
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
