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

    newFetcher = fetcher("all_urls.txt", "words.txt", "updated_index.txt")
    p2s = Porter2Stemmer()

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

            #get token sorted by freq
            sortedToken = sorted([(token, newFetcher.get_token_freq(token)) for token in stemmed_tokens], key=(lambda x: x[1]))
            if len(sortedToken)==1:
                ids = newFetcher.get_docIds_by_token(sortedToken[0][0])
                print("The top five urls under this search:")
                for idNum in ids[:5]:
                    print(newFetcher.get_url_by_id(idNum))
                print()
            else:
                curr_token = sortedToken[0][0]
                ids = newFetcher.get_docIds_by_token(curr_token)
                for index in range(1,len(sortedToken)):
                    curr_token = sortedToken[index][0]
                    ids = intersect(ids, newFetcher.get_docIds_by_token(curr_token))
                # Print the first five url that contains all token
                print("The top five urls under this search:")
                for idNum in ids[:5]:
                    print(newFetcher.get_url_by_id(idNum))
                print()
        print("What do you want to search? (If you want to exit, type 'exit')")
        key = input()

