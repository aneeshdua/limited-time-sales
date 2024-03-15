import uuid

class DealClaims:
    def __init__(self, dealId:str, userId: str, itemId: str) -> None:
        self.dealId = dealId
        self.userId = userId
        self.itemId = itemId
        self.orderId = uuid.uuid4().hex
    
    def getKey(self):
        return self.userId+self.dealId+self.itemId