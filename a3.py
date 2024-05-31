from src import *
from porter2stemmer import Porter2Stemmer

#take two docID list as input, return common docIDs
def intersect(posting1, posting2):
    answer = []
    p1 = 0
    p2 = 0
    while p1 != len(posting1) and p2 != len(posting2):
        if int(posting1[p1]) == int(posting2[p2]):
            answer.append(posting1[p1])
            p1 += 1
            p2 += 1
        else:
            if int(posting1[p1]) < int(posting2[p2]):
                p1 += 1
            else:
                p2 += 1
    return answer


if __name__ == "__main__":
    # just run the build_inverted_index once, comment it after you have the index built
    with Timer("Inverted Index Built Time"):
        if not os.path.exists("all_urls.txt") or not os.path.exists("index.txt") or not os.path.exists("words.txt"):
            build_inverted_index("/Users/vince/Desktop/UCI/Sophomore/Spring 2024/ICS 121/Assignment3/Comp121_Assignment3/DEV")

    with fetcher("all_urls.txt", "words.txt", "updated_index.txt") as newFetcher:
        p2s = Porter2Stemmer()
        # result = compute_cosine_score(newFetcher, ["class", "ics"])

        print("What do you want to search? (If you want to exit, type 'exit')")
        key = input()
        while key != "exit":
            with Timer():
                stemmed_tokens = []  # Create a new list of stemmed tokens
                current_word = []
                for char in key:
                    if isAlpNum(char):
                        current_word.append(char)
                    elif len(current_word) != 0:
                        word = "".join(current_word).lower()
                        stemmed_tokens.append(p2s.stem(word))  # appending stemmed tokens
                        current_word = []
                if current_word:
                    word = "".join(current_word).lower()
                    stemmed_tokens.append(p2s.stem(word))
                result = data_processing(stemmed_tokens, newFetcher)
                for each_score in result:
                    print(newFetcher.get_url_by_id(each_score[0]))
                print()
            print("What do you want to search? (If you want to exit, type 'exit')")
            key = input()

