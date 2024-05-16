from posting import Posting
import os
import json
from text_processor import *
from report import *
from posting import Posting
from bs4 import BeautifulSoup

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def add_in_dictionary(index, document_id, stemmed_dict, url, encoding, weight):
    for token, freq in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append(Posting(len(freq), document_id, url, encoding, weight, freq)) # treat as normal text

def build_inverted_index(directory_path: str):
    index = {}
    all_footprints = []
    keyPositionDict = {} # This record the index of each key in the result so we can locate them quickly
    document_id = 0
    with open('result.txt', 'w') as file: 
        file.write("{}")

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

        if '<!DOCTYPE html' in file_content.lower(): # check if the content is HTML content
            parsedHTML = BeautifulSoup(file_content, 'html.parser')

            tokens, stemmed_tokens = seperate_tokens(parsedHTML)
            normal_word_freq_dict = get_word_freq(stemmed_tokens[2])
            footprint = simhash(normal_word_freq_dict)
            print(footprint)
            if not is_new_footprint(footprint, all_footprints):
                print("similar content, skip")
                continue
            all_footprints.append(footprint)
                
            #heading
            heading_word_freq_dict = get_word_freq(stemmed_tokens[0])
            add_in_dictionary(index, document_id, heading_word_freq_dict, data['url'], data['encoding'], 100)
            #bolds and strongs
            bolds_word_freq_dict = get_word_freq(stemmed_tokens[1])
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
            index = {}
    keyPositionDict = update_report(index, document_id)
    return index

if __name__ == "__main__":
    build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Sprint 2024/ICS 121/Assignment3/Comp121_Assignment3/TEST_DEV")