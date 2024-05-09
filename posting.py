

class Posting: # This is the posting class that stores indexes information

    def __init__(self, frequency:int, docId: list, url: str, encoding:str, weight: int):
        self.frequency = frequency
        self.docId = docId
        self.url = url
        self.encoding = encoding 
        self.weight = weight
        # probably need more attributes
    
    def addDocId(self, the_tuple: tuple) -> None:

        self.docId.append(the_tuple)
    
    def freqInfo(self):

        return self.frequency
    
    def docIdInfo(self):

        return self.docId
    
    def urlInfo(self):

        return self.url
    
    def encodingInfo(self):

        return self.encoding
    
    def __repr__(self):
        return f"{self.docId}: {self.frequency}: {self.weight}"
