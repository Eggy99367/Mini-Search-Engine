import json, re
from .posting import *

def fetch_urls(path):
    with open(path, 'r') as file:
        return json.loads(file.read())
    
def fetch_token_list(path):
    with open(path, 'r') as file:
        return file.read().split(',')
    
urls_dict = fetch_urls("all_urls.txt")
token_list = fetch_token_list("words.txt")

def fetch_token(record:str):
    return re.search(r'\[(.*?)\]', record).group(1)

def _fetch_postings(record:str):
    print(record)
    record = record.strip().split(']')[1]
    posting_txts = record.split('/')
    postings = [str_to_posting(txt) for txt in posting_txts]
    return postings

def get_url_by_id(docId: int | str) -> str:
    return urls_dict[str(docId)]["url"]

def get_url_encoding_by_id(docId: int | str) -> str:
    return urls_dict[str(docId)]["encoding"]

def _get_token_line_number(token: str) -> str:
    return token_list.index(token) + 1

def _get_line(path, line_number):
    with open(path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num == line_number:
                return line.strip()
            
def get_token_line(token):
    return _get_line("index.txt", _get_token_line_number(token))

def get_token_freq(token):
    try:
        return len(get_token_line(token).split('/'))
    except Exception:
        return 0

def get_postings(token):
    try:
        return _fetch_postings(get_token_line(token))
    except Exception:
        return []

def get_docIds_by_token(token):
    try:
        return [p.docId() for p in get_postings(token)]
    except Exception:
        return []
    
def get_weights_by_token(token):
    try:
        return [p.weight() for p in get_postings(token)]
    except Exception:
        return []