from posting import Posting
import os
import json
from text_processor import *
from report import *
from posting import Posting
from bs4 import BeautifulSoup
from test_timer import Timer

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def add_in_dictionary(index, document_id, stemmed_dict):
    for token, idxs in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append(Posting(len(idxs), document_id, [], [], idxs)) # treat as normal text
    return index

def html_add_in_dictionary(index, document_id, stemmed_dict):
    weight = 0
    wgt_list = [10, 3, 1]
    for token, idxs_list in stemmed_dict.items():
        for list_idx, idxs in enumerate(idxs_list):
            weight += len(idxs) * wgt_list[list_idx]
        if token not in index:
            index[token] = []
        index[token].append(Posting(weight, document_id, *idxs_list))
    return index

def build_inverted_index(directory_path: str):
    index = {}
    all_footprints = []
    all_urls = {}
    keyPositionDict = {} # This record the index of each key in the result so we can locate them quickly
    document_id = 0
    with open('result.txt', 'w') as file: 
        file.write("{}")
    with open('all_urls.txt', 'w') as file: 
        file.write("{}")
    with open('words.txt', 'w') as file: 
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
            all_urls[document_id] = {"url": data['url'], "encoding": data['encoding']}
            file_content = data['content']

        if '<!doctype html' in file_content.lower(): # check if the content is HTML content
            parsedHTML = BeautifulSoup(file_content, 'html.parser')

            tokens, stemmed_tokens = seperate_tokens(parsedHTML)
            word_freq_dict = html_get_word_freq(stemmed_tokens)

            # heading_word_freq_dict = get_word_freq(stemmed_tokens[0])
            # bolds_word_freq_dict = get_word_freq(stemmed_tokens[1])
            # normal_word_freq_dict = get_word_freq(stemmed_tokens[2])

            # footprint = simhash(normal_word_freq_dict)
            # print(footprint)
            # if not is_new_footprint(footprint, all_footprints):
            #     print("similar content, skip")
            #     continue
            # all_footprints.append(footprint)
            
            index = html_add_in_dictionary(index, document_id, word_freq_dict)
            #heading
            # add_in_dictionary(index, document_id, heading_word_freq_dict, 100)
            #bolds and strongs
            # add_in_dictionary(index, document_id, bolds_word_freq_dict, 30)
            # Regular texts
            # add_in_dictionary(index, document_id, normal_word_freq_dict, 1)
            print(f"\rprocess document #{document_id}/{total_paths} [html]             ", end="")
        else:
            result, stemmed_result = tokenize(file_content)
            word_freq_dict = get_word_freq(stemmed_result)

            add_in_dictionary(index, document_id, word_freq_dict)
            print(f"\rprocess document #{document_id}/{total_paths}                    ", end="")
        if document_id % 10 == 0:
            print(f"\rprocess document #{document_id}/{total_paths} Updating to Disk...", end="")
            with Timer():
                update_report(index, all_urls, document_id)
                print("\r\x1b[K", end="")
            index = {}
    with Timer():
        keyPositionDict = update_report(index, all_urls, document_id)
        print("\r\x1b[K", end="")
    return index

if __name__ == "__main__":
    build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Sprint 2024/ICS 121/Assignment3/Comp121_Assignment3/DEV")