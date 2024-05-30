import json, re
from .posting import *


def fetch_urls(path):
    with open(path, 'r') as file:
        return json.loads(file.read())


def fetch_token_list(path):
    with open(path, 'r') as file:
        return file.read().split(',')


def fetch_token(record: str):
    return re.search(r'\[(.*?)\]', record).group(1).split(":")[0]

def fetch_freq(record: str):
    return int(re.search(r'\[(.*?)\]', record).group(1).split(":")[1])


def fetch_postings(record: str):
    #print(record)
    record = record.strip().split(']')[1]
    posting_txts = record.split('/')
    postings = [txt.split(',') for txt in posting_txts]
    return postings


class fetcher:
    def __init__(self, urls_path, tokens_path):
        self.urls_dict = fetch_urls(urls_path)
        self.token_list = fetch_token_list(tokens_path)

    # input a docID, return the url
    def get_url_by_id(self, docId) -> str:
        return self.urls_dict[str(docId)]["url"]

    # input the docID, get the encoding of the doc
    def get_url_encoding_by_id(self, docId) -> str:
        return self.urls_dict[str(docId)]["encoding"]

    def _get_token_line_number(self, token: str) -> int:
        return self.token_list.index(token) + 1

    def _get_line(self, path, line_number):
        with open(path, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                if line_num == line_number:
                    return line.strip()

    def get_token_line(self, token):
        return self._get_line("index.txt", self._get_token_line_number(token))

    def get_token_freq(self, token):
        try:
            return len(self.get_token_line(token).split('/'))
        except Exception:
            return 0

    def get_postings(self, token):
        try:
            return fetch_postings(self.get_token_line(token))
        except Exception:
            return []


    def get_docIds_by_token(self, token):
        try:
            return [p.docId() for p in self.get_postings(token)]
        except Exception:
            return []


    def get_weights_by_token(self, token):
        try:
            return [p.weight() for p in self.get_postings(token)]
        except Exception:
            return []
