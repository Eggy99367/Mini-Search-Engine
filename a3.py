from posting import Posting

def parse(path: str) -> str:
  pass

def tokenize(parsed_text: str) -> list[str]:
  pass

def stemming(tokens: list[str]) -> dict[str: int]:
  pass

def build_index(file_paths):
  index = {}
  document_id = 0
  for path in file_paths:
    document_id += 1
    parsed_text = parse(path)
    tokens = tokenize(parsed_text)
    stemmed_tokens = stemming(tokens)

    for token, freq in stemmed_tokens.items():
      if token not in index:
        index[token] = []
      index[token].append(Posting())
      
  return index

# Create the inverted index: a map with the token as a key and a list of its corresponding postings
# def invert_index(tokenList):
#   result = dict()
#   for token in tokenList:
#     if token in result:
#       result[token] +=1
#     else:
#       result[token] = 1