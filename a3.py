# Create the inverted index: a map with the token as a key and a list of its corresponding postings
def invert_index(tokenList):
  result = dict()
  for token in tokenList:
    if token in result:
      result[token] +=1
    else:
      result[token] = 1
