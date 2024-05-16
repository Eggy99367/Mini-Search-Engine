

class Posting: # This is the posting class that stores indexes information

    def __init__(self, frequency:int, docId: list, url: str, encoding:str, weight: int, index: list):
        self.frequency = frequency
        self.docId = docId
        self.url = url
        self.encoding = encoding 
        self.weight = weight
        self.index = index
        # probably need more attributes
    
    def addDocId(self, the_tuple: tuple) -> None:

        self.docId.append(the_tuple)

    def indexInfo(self):

        return self.index
    
    def freqInfo(self):

        return self.frequency
    
    def docIdInfo(self):

        return self.docId
    
    def urlInfo(self):

        return self.url
    
    def encodingInfo(self):

        return self.encoding
    
    def to_dict(self):
        return {
            "freq": self.frequency,
            "docId": self.docId,
            "url": self.url,
            "encoding": self.encoding,
            "wgt": self.weight,
            "idx": self.index
        }
    
    def __repr__(self):
        return (f"docID: {self.docId}, "
        f"Freq: {self.frequency}, "
        f"Weight: {self.weight}, "
        f"Index: {self.index}, "
        f"Url: {self.url}, "
        f"Encoding: {self.encoding}")
    
    def __eq__(self, other):
        if not isinstance(other, Posting):
            return False
        return (self.index, self.frequency, self.weight) == (other.index, other.frequency, other.weight)

    def __hash__(self):
        return hash((self.index, self.frequency, self.weight))
