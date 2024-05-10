from posting import Posting
import os
import json
from tokenizer import tokenize
from posting import Posting
from bs4 import BeautifulSoup

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def get_word_freq(tokens):
    word_freq_dict = {}
    for index, token in enumerate(tokens):
        if token not in word_freq_dict:
            word_freq_dict[token] = []
        word_freq_dict[token].append(index)
    return word_freq_dict

def add_in_dictionary(index, document_id, stemmed_dict, url, encoding, weight):
    for token, freq in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append(Posting(len(freq), document_id, url, encoding, weight, freq)) # treat as normal text

def get_file_size_in_kb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_kb = size_in_bytes / 1024
    return size_in_kb

def update_report(index, document_id):

    with open('result.txt', 'w') as file1: 
        for key, value in index.items():
            for each_posting in value:
                file1.write(f"Key: {key}: {each_posting}")
            file1.write("\n")
    
    with open('Q1.txt', 'w') as file1: 
        file1.write(f"DocumentNum: {document_id}")

    with open('Q2.txt', 'w') as file1: 
        file1.write(f"Number of Unique words: {len(index)}")

    with open('Q3.txt', 'w') as file1: 
        file1.write(f"size: {get_file_size_in_kb('result.txt')}KB")

def seperate_tokens(parsedHTML):
    tokens = [[], [], []]
    stemmed_tokens = [[], [], []]
    for element in parsedHTML.find_all():
        index = None
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']: # heading
            index = 0
        elif element.name in ['b', 'strong']:# bolds and strongs
            index = 1
        elif element.name in ['p']:  # Exclude links include body
            index = 2
        if index is not None:
            tmpTokens, tmpStemmedTokens = tokenize(element.text)
            tokens[index] += tmpTokens
            stemmed_tokens[index] += tmpStemmedTokens
    return tokens, stemmed_tokens

def build_inverted_index(directory_path: str):
    index = {}
    document_id = 0
    paths = list(iterate_files(directory_path))
    total_paths = len(paths)
    for path in paths:
        # print(path)
        document_id += 1
        if(not path.endswith(".json")):
            continue
        with open(path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            file_content = data['content']

        if '<html>' in file_content.lower(): # check if the content is HTML content
            parsedHTML = BeautifulSoup(file_content, 'html.parser')

            tokens, stemmed_tokens = seperate_tokens(parsedHTML)
            # for element in parsedHTML.find_all():
            #     if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']: # heading
            #         tmpTokens, tmpStemmedTokens = tokenize(element.text)
            #         headingTokens += tmpTokens
            #         stemmedHeadingTokens += tmpStemmedTokens
            #     elif element.name in ['b', 'strong']:# bolds and strongs
            #         tmpTokens, tmpStemmedTokens = tokenize(element.text)
            #         strongsBoldsTokens += tmpTokens
            #         stemmedStrongsBoldsTokens += tmpStemmedTokens
            #     elif element.name in ['body', 'p']:  # Exclude links include body
            #         tmpTokens, tmpStemmedTokens = tokenize(element.text)
            #         normalTokens += tmpTokens
            #         stemmedNormalTokens += tmpStemmedTokens
            
            # print(stemmedHeadingTokens)
            # print(stemmedHeadingTokens)
                
            heading_word_freq_dict = get_word_freq(stemmed_tokens[0])
            bolds_word_freq_dict = get_word_freq(stemmed_tokens[1])
            normal_word_freq_dict = get_word_freq(stemmed_tokens[2])
            #heading
            add_in_dictionary(index, document_id, heading_word_freq_dict, data['url'], data['encoding'], 100)

            #bolds and strongs
            add_in_dictionary(index, document_id, bolds_word_freq_dict, data['url'], data['encoding'], 30)
            
            # Regular texts
            add_in_dictionary(index, document_id, normal_word_freq_dict, data['url'], data['encoding'], 1)

        
        else:
            result, stemmed_result = tokenize(file_content)
            word_freq_dict = get_word_freq(stemmed_result)

            add_in_dictionary(index, document_id, word_freq_dict, data['url'], data['encoding'], 1)

        if document_id % 10 == 0:
            print(f"process document #{document_id}/{total_paths}")
        if document_id % 2000 == 0:
            update_report(index, document_id)
    update_report(index, document_id)
    return index

# def test(path):
#     index = {}
#     with open(path, 'r', encoding="utf-8") as file:
#             data = json.load(file)
#             file_content = data['content']
#     parsedHTML = BeautifulSoup(file_content, 'html.parser')
#     tokens, stemmed_tokens = seperate_tokens(parsedHTML)
#     heading_word_freq_dict = get_word_freq(stemmed_tokens[0])
#     bolds_word_freq_dict = get_word_freq(stemmed_tokens[1])
#     normal_word_freq_dict = get_word_freq(stemmed_tokens[2])
#     add_in_dictionary(index, 0, heading_word_freq_dict, data['url'], data['encoding'], 100)

#     #bolds and strongs
#     add_in_dictionary(index, 0, bolds_word_freq_dict, data['url'], data['encoding'], 30)
    
#     # Regular texts
#     add_in_dictionary(index, 0, normal_word_freq_dict, data['url'], data['encoding'], 1)

#     # print(index.keys())
#     # print(len(index))

if __name__ == "__main__":
    # result = build_inverted_index("/home/hsingl1/comp121_Assignment3/TEST_DEV")
    # print(f"----------------------------final result----------------------------")
    # print(result)
    build_inverted_index("/home/hsingl1/comp121_Assignment3/DEV")
    # test("/home/hsingl1/comp121_Assignment3/TEST_DEV/www_cs_uci_edu/0a77b224f19e2fadc0ec26a19e7b6219dc56833f005fbd658f6eb8194804883e.json")