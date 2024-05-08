from posting import Posting
import os
import json
from tokenizer import tokenize, compute_word_frequencies
from posting import Posting

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

        result, stemmed_result = tokenize(file_content)
        word_freq_dict = get_word_freq(stemmed_result)

        for token, freq in word_freq_dict.items():
            if token not in index:
                index[token] = []
            index[token].append(Posting(freq, document_id, data['url'], data['encoding']))
        
        if document_id % 2000 == 0:
            print(index)

    return index

if __name__ == "__main__":
    result = build_inverted_index("/Users/vince/Desktop/ICS 121/Assignment3/Comp121_Assignment3/TEST_DEV")
    print(f"----------------------------final result----------------------------")
    print(result)
