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
    for token in tokens:
        if token not in word_freq_dict:
            word_freq_dict[token] = 0
        word_freq_dict[token] += 1
    return word_freq_dict

def build_inverted_index(directory_path: str):
    index = {}
    document_id = 0
    for path in iterate_files(directory_path):
        # print(path)
        document_id += 1

        with open(path, 'r') as file:
            data = json.load(file)
            file_content = data['content']

        if '<html>' in file_content.lower(): # check if the content is HTML content
            parsedHTML = BeautifulSoup(file_content, 'html.parser')
            headingTokens = []
            stemmedHeadingTokens = []
            strongsBoldsTokens = []
            stemmedStrongsBoldsTokens = []
            normalTokens = []
            stemmedNormalTokens = []

            for element in parsedHTML.find_all():
                tmpTokens = []
                tmpStemmedTokens = []

                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']: # heading
                    tmpTokens, tmpStemmedTokens = tokenize(element.text)
                    headingTokens += tmpTokens
                    stemmedHeadingTokens += tmpStemmedTokens
                elif element.name in ['b', 'strong']:# bolds and strongs
                    tmpTokens, tmpStemmedTokens = tokenize(element.text)
                    strongsBoldsTokens += tmpTokens
                    stemmedStrongsBoldsTokens += tmpStemmedTokens
                elif element.name in ['body', 'p']:  # Exclude links include body
                    tmpTokens, tmpStemmedTokens = tokenize(element.text)
                    normalTokens += tmpTokens
                    stemmedNormalTokens += tmpStemmedTokens
            
            # print(stemmedHeadingTokens)
            # print(stemmedHeadingTokens)
                
            heading_word_freq_dict = get_word_freq(stemmedHeadingTokens)
            bolds_word_freq_dict = get_word_freq(stemmedStrongsBoldsTokens)
            normal_word_freq_dict = get_word_freq(stemmedNormalTokens)
            #heading
            add_in_dictionary(index, document_id, heading_word_freq_dict, data['url'], data['encoding'], 100)
            # for token, freq in heading_word_freq_dict.items():
            #     if token not in index:
            #         index[token] = []
            #     index[token].append(Posting(freq, document_id, data['url'], data['encoding'], 100)) # heading weight is 3

            #bolds and strongs
            add_in_dictionary(index, document_id, bolds_word_freq_dict, data['url'], data['encoding'], 30)

            # for token, freq in bolds_word_freq_dict.items():
            #     if token not in index:
            #         index[token] = []
            #     index[token].append(Posting(freq, document_id, data['url'], data['encoding'], 30)) # bolds weight 30
            
            # Regular texts
            add_in_dictionary(index, document_id, normal_word_freq_dict, data['url'], data['encoding'], 1)

            # for token, freq in normal_word_freq_dict.items():
            #     if token not in index:
            #         index[token] = []
            #     index[token].append(Posting(freq, document_id, data['url'], data['encoding'], 1)) # normal weight 1
        
        else:
            result, stemmed_result = tokenize(file_content)
            word_freq_dict = get_word_freq(stemmed_result)

            add_in_dictionary(index, document_id, word_freq_dict, data['url'], data['encoding'], 1)

            # for token, freq in word_freq_dict.items():
            #     if token not in index:
            #         index[token] = []
            #     index[token].append(Posting(freq, document_id, data['url'], data['encoding'], 1)) # treat as normal text
        
        if document_id % 2000 == 0:
            print(index)

    return index

def add_in_dictionary(index, document_id, stemmed_dict, url, encoding, weight):
    for token, freq in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append(Posting(freq, document_id, url, encoding, weight)) # treat as normal text



if __name__ == "__main__":
    result = build_inverted_index("/home/hsingl1/comp121_Assignment3/TEST_DEV")
    print(f"----------------------------final result----------------------------")
    print(result)
