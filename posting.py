

class Posting: # This is the posting class that stores indexes information

    def __init__(self, weight:int, docId: int, title_index: list, bold_index: list, reg_index: list):
        self._docId = docId
        self._weight = weight
        self._title_index = title_index
        self._bold_index = bold_index
        self._reg_index = reg_index
        # probably need more attributes

    def docId(self):
        return self._docId
    
    def weight(self):
        return self._weight
    
    def title_index(self):
        return self._title_index
    
    def bold_index(self):
        return self._bold_index
    
    def reg_index(self):
        return self._reg_index
    
    def to_dict(self):
        return {
            "wgt": self.weight(),
            "docId": self.docId(),
            "t_idx": self.title_index(),
            "b_idx": self.bold_index(),
            "r_idx": self.reg_index()
        }
    
    def to_list(self):
        return [
            self.docId(),
            self.weight(),
            self.title_index(),
            self.bold_index(),
            self.reg_index()
        ]
    
    # def __repr__(self):
    #     return (f"docID: {self.docId}, "
    #     f"Freq: {self.frequency}, "
    #     f"Weight: {self.weight}, "
    #     f"Index: {self.index}")
    
    # def __eq__(self, other):
    #     if not isinstance(other, Posting):
    #         return False
    #     return (self.index, self.frequency, self.weight) == (other.index, other.frequency, other.weight)

    # def __hash__(self):
    #     return hash((self.index, self.frequency, self.weight))
