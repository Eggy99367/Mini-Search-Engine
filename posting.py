

class Posting: # This is the posting class that stores indexes information

    def __init__(self, frequency:int, docId: list, url: str, encoding:str):
        self.frequency = frequency
        self.docId = docId
        self.url = url
        self.encoding = encoding
    
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
