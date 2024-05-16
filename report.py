import os
import json

def get_file_size_in_kb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_kb = size_in_bytes / 1024
    return size_in_kb

def serialize_posting(idx):
    return {key: [post.to_dict() for post in value] for key, value in idx.items()}

def merge_index(idx_a, idx_b):
    for key, value in idx_b.items():
        if key not in idx_a:
            idx_a[key] = value
        else:
            idx_a[key] += value
    return idx_a


def update_report(index, doc_count):

    keyPositionDict = {}
    index = serialize_posting(index)
    try:
        if os.path.exists('result.txt'):
            with open('result.txt', 'r') as file:
                content = file.read()
                index_from_disk = json.loads(content)
                print(len(index_from_disk), len(index))
                index = merge_index(index_from_disk, index)
    except Exception:
        pass

    with open('result.txt', 'w') as file: 
        # start_index = 5
        # for key, value in index.items():
        #     for each_posting in value:
        #         file.write(f"Key: {key}: {each_posting}")
        #     keyPositionDict[key] = start_index
        #     start_index = file.tell() + 1
        #     file.write("\n")
        index_text = json.dumps(index)
        file.write(index_text)
    
    with open('report.txt', 'w') as file: 
        file.write(f"DocumentNum: {doc_count}\n")
        file.write(f"Number of Unique words: {len(index)}\n")
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