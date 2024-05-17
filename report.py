import os
import json

def get_file_size_in_kb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_kb = size_in_bytes / 1024
    return size_in_kb

def serialize_posting(idx):
    return {key: [post.to_list() for post in value] for key, value in idx.items()}

def merge_index(idx_a, idx_b):
    for key, value in idx_b.items():
        if key not in idx_a:
            idx_a[key] = value
        else:
            idx_a[key] += value
    return idx_a

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def update_report(index, all_urls, doc_count):

    keyPositionDict = {}
    index = serialize_posting(index)
    try:
        if os.path.exists('result.txt'):
            with open('result.txt', 'r') as file:
                content = file.read()
                index_from_disk = json.loads(content)
                # print(len(index_from_disk), len(index))
                index = merge_index(index_from_disk, index)
    except Exception:
        pass

    with open('all_urls.txt', 'w') as file:
        all_urls_text = json.dumps(all_urls)
        file.write(all_urls_text)
    
    with open('words.txt', 'w') as file:
        file.write(','.join([x for x in index if check_int(x)]))

    with open('result.txt', 'w') as file:
        index_text = json.dumps(index)
        file.write(index_text)
    
    with open('report.txt', 'w') as file: 
        file.write(f"DocumentNum: {doc_count}\n")
        file.write(f"Number of Unique words: {len(index)}\n")
        file.write(f"Number of Non Integer words: {len([x for x in index if not check_int(x)])}\n")
        file.write(f"size: {get_file_size_in_kb('result.txt')}KB\n")

    # with open("result.txt", 'r') as file:
    #     file.seek(18294)
    #     print(file.readline())
    # print(keyPositionDict)
    return keyPositionDict

if __name__ == "__main__":
    with open('result.txt', 'r') as file:
        content = file.read()
        index_from_disk = json.loads(content)
        print(len(index_from_disk))