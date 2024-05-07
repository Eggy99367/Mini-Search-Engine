import json
from porter2stemmer import Porter2Stemmer # we can use this
from posting import Posting




def read_in_the_json_file(textFile_path: str): # read in the json file but don't know what parameter is given(need to fix)

    with open(textFile_path, 'r') as file1:
        data = json.load(file1)

    # url = data['url']

    # Access the content
    content = data['content']
    result, stemmed_result = tokenize(content)
    # print(result)
    # print(stemmed_result)
    the_word_dict = compute_word_frequencies(1, result, 
                                             stemmed_result, data['url'], data['encoding'])
    for key, value in the_word_dict.items():

        print(f"{key}: {value.docIdInfo()}")
    
    # Access the encoding
    # encoding = data['encoding']

def tokenize(text) -> {list, list}:
    porter2Stemmer1 = Porter2Stemmer() #declaring snowballStemmer object
    tokens = []
    stemmed_tokens = [] # Create a new list of stemmed tokens
    current_word = []
    for char in text:
        if char.isalpha() or char.isdigit():
            current_word.append(char)
        elif len(current_word) != 0:
            word = "".join(current_word).lower()
            tokens.append(word)
            stemmed_tokens.append(porter2Stemmer1.stem(word)) # appending stemmed tokens
            current_word = []
    if current_word:
        word = "".join(current_word).lower()
        tokens.append(word)
    return tokens, stemmed_tokens

def compute_word_frequencies(document_number: int, 
                             token_list: list, 
                             stemmed_token_list: list,
                             url: str,
                             encoding: str) -> dict: 
    result = {}
    #haven't think of a way to use stemmed_token_list
    for index in range(len(token_list)):

        token = token_list[index]

        if token not in result:

            result[token] = Posting(1, [(document_number, index)], url, encoding)

        else:
            result[token].addDocId((document_number, index))

    return result






if __name__ == "__main__":
    #testing
    read_in_the_json_file("/home/hsingl1/comp121_Assignment3/ANALYST/www_cs_uci_edu/0a0056fb9a53ec6f190aa2b5fb1a97c33cd69726c8841f89d24fa5abd84d276c.json")