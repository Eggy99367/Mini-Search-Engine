# import math
# from collections import defaultdict
# from stopwords import stopwords

# #take two docID list as input, return common docIDs
# def intersect(posting1, posting2):
#     answer = []
#     p1 = 0
#     p2 = 0
#     while p1 != len(posting1) and p2 != len(posting2):
#         if int(posting1[p1]) == int(posting2[p2]):
#             answer.append(posting1[p1])
#             p1 += 1
#             p2 += 1
#         else:
#             if int(posting1[p1]) < int(posting2[p2]):
#                 p1 += 1
#             else:
#                 p2 += 1
#     return answer

# # need to fix here
# def compute_each_score(scores: list, length: list, list_of_postings: list, query_weight: float, fetcher, token): # adding each score of posting object
#     for each_posting in list_of_postings:
#         first_values = [sublist[0] for sublist in scores]
#         cosine_weight = each_posting[1] * query_weight
#         if each_posting[0] in first_values:
#             index = first_values.index(each_posting[0])
#             scores[index][1] += cosine_weight
#         else:
#             scores.append([each_posting[0], cosine_weight])
#             get_freq_of_each_term(length, fetcher.get_token_freq(token))

# # need to fix here
# def compute_query_weight(length_of_query: int, keyword_count: int): # get the weight for the query (Wtq)
#     return math.log(length_of_query / keyword_count)

# def get_freq_of_each_term(length: list, token_freq: int):
#     if(token_freq > 0):
#         length.append(token_freq)

# def compute_cosine_score(fetcher, list_of_keywords: list):
#     scores = [] # score for each document
#     length = [] # freq for each document
    
#     # Dictionary to count occurrences of each document ID
#     doc_count = defaultdict(int)
    
#     # Intermediate storage for postings
#     postings_dict = {}
    
#     # Count occurrences of each document ID
#     for each_token in list_of_keywords:
#         postings = fetcher.get_postings(each_token)
#         postings_dict[each_token] = postings
#         for doc_id, _ in postings:
#             doc_count[doc_id] += 1

#     # Filter documents that appear in at least 4 out of the 4 keywords
#     relevant_docs = {doc_id for doc_id, count in doc_count.items() if count >= len(list_of_keywords)}

#     # Calculate scores for every keyword documents
#     for each_token in list_of_keywords:
#         if each_token in stopwords:
#             continue
#         query_weight = compute_query_weight(55393, list_of_keywords.count(each_token))
#         postings = [value for value in postings_dict[each_token] if value[0] in relevant_docs]
#         compute_each_score(scores, length, postings, query_weight, fetcher, each_token)

#     for each_score, each_length in zip(scores, length):
#         each_score[1] = each_score[1] / each_length
    
#     # Sort the scores in descending order
#     scores = sorted(scores, key=lambda x: x[1], reverse=True)

#     # Print the top 10 URLs
#     return scores[:10]

# def data_processing(stemmed_tokens, newFetcher):
#     #get token sorted by freq
#     sortedToken = sorted([(token, newFetcher.get_token_freq(token)) for token in stemmed_tokens], key=(lambda x: x[1]))
#     if len(sortedToken)==1:
#         ids = newFetcher.get_docIds_by_token(sortedToken[0][0])
#         print("The top ten urls under this search:")
#         result = compute_cosine_score(newFetcher, stemmed_tokens)
#     else:
#         # curr_token = sortedToken[0][0]
#         # ids = newFetcher.get_docIds_by_token(curr_token)
#         # for index in range(1,len(sortedToken)):
#         #     curr_token = sortedToken[index][0]
#         #     ids = intersect(ids, newFetcher.get_docIds_by_token(curr_token))
#         # Print the first five url that contains all token
#         print("The top ten urls under this search:")
#         # for idNum in ids[:10]:
#         #     print(newFetcher.get_url_by_id(idNum))
#         result = compute_cosine_score(newFetcher, stemmed_tokens)
    
#     return result