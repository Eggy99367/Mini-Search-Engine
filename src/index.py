import os
import json
from bs4 import BeautifulSoup
from .report import *
from .posting import Posting
from .posting import Posting
from .text_processor import *
from .test_timer import Timer

def iterate_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

def add_in_dictionary(index, document_id, stemmed_dict):
    for token, idxs in stemmed_dict.items():
        if token not in index:
            index[token] = []
        index[token].append(Posting(document_id, len(idxs), [], [], idxs)) # treat as normal text
    return index

def html_add_in_dictionary(index, document_id, stemmed_dict):
    weight = 0
    wgt_list = [10, 3, 1]
    for token, idxs_list in stemmed_dict.items():
        for list_idx, idxs in enumerate(idxs_list):
            weight += len(idxs) * wgt_list[list_idx]
        if token not in index:
            index[token] = []
        index[token].append(Posting(document_id, weight, *idxs_list))
    return index

def build_inverted_index(directory_path: str):
    index = {}
    all_urls = {}
    document_id = 0
    open('index.txt', 'w')

    paths = list(iterate_files(directory_path))
    total_paths = len(paths)
    for path in paths:
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
            
            index = html_add_in_dictionary(index, document_id, word_freq_dict)
            print(f"\r\x1b[Kprocess document #{document_id}/{total_paths} [html]", end="")
        else:
            result, stemmed_result = tokenize(file_content)
            word_freq_dict = get_word_freq(stemmed_result)

            add_in_dictionary(index, document_id, word_freq_dict)
            print(f"\r\x1b[Kprocess document #{document_id}/{total_paths}", end="")
        if document_id % 10000 == 0:
            print(f"\r\x1b[Kprocess document #{document_id}/{total_paths} Updating to Disk...", end="")
            with Timer():
                update_report(index, all_urls, document_id)
                print("\r\x1b[K", end="")
            index = {}
    with Timer():
        update_report(index, all_urls, document_id)
        print("\r\x1b[K", end="")

if __name__ == "__main__":
    build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Spring 2024/ICS 121/Assignment3/Comp121_Assignment3/DEV")