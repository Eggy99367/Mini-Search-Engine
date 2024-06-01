import math
from collections import defaultdict
import heapq
import numpy as np

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

# compute cosine score
def compute_cosine_score(newFetcher, termList:list, query_count: dict, doc_count:dict, N:int):
    scores = np.zeros(N)

    for t in termList:
        doc_dict = doc_count[t]
        top_doc = heapq.nlargest(50, doc_dict.items(), key=lambda x: x[1])
        for doc in top_doc:
            scores[doc[0]] += doc[1]*query_count[t]

    top_urls = np.argsort(-scores)[:10]

    urlList = []
    scoreList = []

    for url in top_urls:
        urlList.append(newFetcher.get_url_by_id(url))
        scoreList.append(scores[url])

    # # Print the top 10 URLs
    return urlList, scoreList


def data_processing(stemmed_tokens, newFetcher):
    # Dictionary to count occurrences of each query term
    query_count = defaultdict(int)
    for token in stemmed_tokens:
        query_count[token] += 1

    # Get term list
    termList = list(query_count.keys())

    # Get the total number of documents
    N = newFetcher.get_url_size()

    # Calculate tf-idf for query
    for token in query_count:
        query_count[token] = (1 + math.log10(query_count[token])) * math.log10(N / newFetcher.get_token_freq(token))

    # Calculate the query length
    queryLength = 0
    for token in query_count:
        queryLength += math.pow(query_count[token], 2)
    queryLength = math.sqrt(queryLength)

    # Last step, calculate normalized tf-idf for query
    for token in query_count:
        query_count[token] = query_count[token]/queryLength

    #get token sorted by freq
    sortedToken = sorted([(token, newFetcher.get_token_freq(token)) for token in query_count], key=(lambda x: x[1]))

    # One term query
    if len(sortedToken) == 1:
        doc_count = {sortedToken[0][0]: newFetcher.get_posting_info_by_token(sortedToken[0][0])}
        result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)
    # Two or more terms query
    else:
        curr_token = sortedToken[0][0]
        ids = newFetcher.get_docIds_by_token(curr_token)
        for index in range(1, len(sortedToken)):
            curr_token = sortedToken[index][0]
            ids = intersect(ids, newFetcher.get_docIds_by_token(curr_token))

        # Enough document for conjunctive search
        if len(ids) >= 50:
            doc_count = {}
            for token in sortedToken:
                doc_count[token[0]] = newFetcher.get_posting_info_by_token_docID(token[0], ids)
            result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)
        # Not enough document for conjunctive search
        else:
            doc_count = {}
            for token in sortedToken:
                doc_count[token[0]] = newFetcher.get_posting_info_by_token(token[0])
            result, score = compute_cosine_score(newFetcher, termList, query_count, doc_count, N)

    return result, score


stopwordSet = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
               "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
               "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
               "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
               "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
               "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
               "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've",
               "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
               "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
               "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
               "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
               "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
               "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
               "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
               "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
               "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
               "you're", "you've", "your", "yours", "yourself", "yourselves"}
