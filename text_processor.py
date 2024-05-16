import json
from porter2stemmer import Porter2Stemmer # we can use this
from posting import Posting
import hashlib

def tokenize(text) -> {list, list}:
    porter2Stemmer1 = Porter2Stemmer() #declaring snowballStemmer object
    tokens = []
    stemmed_tokens = [] # Create a new list of stemmed tokens
    current_word = []
    for char in text:
        if char.isalpha() or char.isdigit():
            current_word.append(char)
        elif len(current_word) != 0:
            word = "".join(current_word).lower()
            tokens.append(word)
            stemmed_tokens.append(porter2Stemmer1.stem(word)) # appending stemmed tokens
            current_word = []
    if current_word:
        word = "".join(current_word).lower()
        tokens.append(word)
    return tokens, stemmed_tokens

def seperate_tokens(parsedHTML):
    tokens = [[], [], []]
    stemmed_tokens = [[], [], []]
    for element in parsedHTML.find_all():
        index = None
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']: # heading
            index = 0
        elif element.name in ['b', 'strong']:# bolds and strongs
            index = 1
        elif element.name in ['p']:  # Exclude links include body
            index = 2
        if index is not None:
            tmpTokens, tmpStemmedTokens = tokenize(element.text)
            tokens[index] += tmpTokens
            stemmed_tokens[index] += tmpStemmedTokens
    return tokens, stemmed_tokens

def get_word_freq(tokens):
    word_freq_dict = {}
    for index, token in enumerate(tokens):
        if token not in word_freq_dict:
            word_freq_dict[token] = []
        word_freq_dict[token].append(index)
    return word_freq_dict

def simhash(tokens, hash_bits=128):
    V = [0] * hash_bits
    for word, all_presence in tokens.items():
        hash_value = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        for i in range(hash_bits):
            # extracts the value of the i-th bit from the right of hash_value
            bit = (hash_value >> i) & 1
            if bit == 1:
                V[i] += len(all_presence)
            else:
                V[i] -= len(all_presence)
    fingerprint = 0
    for i in range(hash_bits):
        if V[i] >= 0:
            # sets the i-th bit of fingerprint to 1 without affecting the other bits
            fingerprint |= (1 << i)
    return fingerprint

def are_similar(hash_a, hash_b, threshold, hash_bits=128):
    # XOR to find differing bits
    differing_bits = hash_a ^ hash_b

    # Count the number of same bits
    same_bits = hash_bits - bin(differing_bits).count('1')

    # Calculate similarity as the fraction of bits that are the same
    similarity = same_bits / hash_bits
    return similarity >= threshold

def is_new_footprint(new_footprint, footprints):
    for value in footprints:
        if are_similar(new_footprint, value, 0.9):
            return False
    return True

if __name__ == "__main__":
    pass