import re
from json import load
from collections import Counter

def load_lexicon(lexicon_file='./media/impo.json'):
    with open(lexicon_file, 'r') as json_file:
        return load(json_file)

def load_token_list(token_list):
    tokens = tokenize_sentences_and_words(token_list)
    lexicon = load_lexicon()  # Call the load_lexicon function to load lexicon data
    affect_frequencies = __build_word_affect__(tokens, lexicon)
    
    # Calculate top emotions
    max_value = max(affect_frequencies.values())
    top_emotions = []
    for key in affect_frequencies.keys():
        if affect_frequencies[key] == max_value:
            top_emotions.append((key, max_value))
    
    return tokens, top_emotions

def tokenize_sentences_and_words(text):
    # Split text into sentences based on periods, exclamation marks, and question marks
    sentences = re.split(r'[.!?]', text)
    
    # Tokenize words in each sentence
    tokenized_words = []
    for sentence in sentences:
        words = sentence.split()
        tokenized_words.extend(words)  # Extend the tokenized_words list with the words from the current sentence
    
    return tokenized_words

def __build_word_affect__(tokens, lexicon):
    affect_list = []
    affect_dict = dict()
    affect_frequencies = Counter()
    lexicon_keys = lexicon.keys()
    for word in tokens:
        if word in lexicon_keys:
            affect_list.extend(lexicon[word])
            affect_dict.update({word: lexicon[word]})
    for word in affect_list:
        affect_frequencies[word] += 1
    sum_values = sum(affect_frequencies.values())
    affect_percent = {'fear': 0.0, 'anger': 0.0, 'anticipation': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0,
                      'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
    for key in affect_frequencies.keys():
        affect_percent.update({key: float(affect_frequencies[key]) / float(sum_values)})
    return affect_percent

def top_emotions(text):
    if not isinstance(text, str):  # Ensure text is a string
        text = str(text)
    return load_token_list(text)[1]
