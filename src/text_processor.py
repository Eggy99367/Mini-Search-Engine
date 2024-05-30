from porter2stemmer import Porter2Stemmer

def isAlpNum(chr: str) -> bool:
    #return true if the character is within the range of a-z A-Z or 0-9
    return ord('a') <= ord(chr) <= ord('z') or ord('0') <= ord(chr) <= ord('9') or ord('A') <= ord(chr) <= ord('Z')

def tokenize(text) -> {list, list}:
    porter2Stemmer1 = Porter2Stemmer() #declaring snowballStemmer object
    tokens = []
    stemmed_tokens = [] # Create a new list of stemmed tokens
    current_word = []
    for char in text:
        if isAlpNum(char):
        # if char.isalpha() or char.isdigit():
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
    for token in tokens:
        if token not in word_freq_dict:
            word_freq_dict[token] = 0
        word_freq_dict[token] += 1
    return word_freq_dict

def html_get_word_freq(token_lists):
    word_freq_dict = {}
    for wgt, token_list in enumerate(token_lists):
        for index, token in enumerate(token_list):
            if token not in word_freq_dict:
                word_freq_dict[token] = [[], [], []]
            word_freq_dict[token][wgt].append(index)
    return word_freq_dict

if __name__ == "__main__":
    pass