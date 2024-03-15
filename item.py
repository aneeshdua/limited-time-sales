class Item:
    def __init__(self,id,stockCount) -> None:
        self.id = id
        self.stockCount = stockCount
    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result
    
    def __repr__(self) -> str:
        return "<Item id="+str(self.id)+" stockCount="+str(self.stockCount)+">"