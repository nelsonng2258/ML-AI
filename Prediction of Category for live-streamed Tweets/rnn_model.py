import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import unicodedata
import re
import string
import json
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

"""
This module's purposes are:

1. to provide the preprocessing function needed to preprocess a tweet before using the model to predict
the category of the tweet.

2. to provide the model used for prediction.
"""
wnl = WordNetLemmatizer()

### strip_linkes and strip_all_entities from
### https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def remove_stopwords_and_lemmatize(text):
    stopword = stopwords.words('english')
    text_splitted = text.split()    
    text = " ".join([wnl.lemmatize(word) for word in text_splitted if word not in stopword])
    return text

def preprocess_single_tweet(single_tweet):
    """single_tweet is a string, a tweet, output is another string which is processed."""
    
    single_tweet = remove_stopwords_and_lemmatize(strip_links(single_tweet))
    single_tweet = (lambda single_twt: re.sub(r'[^a-zA-Z]', ' ', single_twt))(single_tweet)
    single_tweet = (lambda x: re.sub('  ', ' ', x))(single_tweet)
    
    return single_tweet

def get_prediction(single_tweet):
    example_tweet = preprocess_single_tweet(single_tweet)
    tokenized_tweet = tokenizer.texts_to_sequences([example_tweet])
    tokenized_tweet = tf.keras.preprocessing.sequence.pad_sequences(tokenized_tweet,
                                                                    maxlen=max_sentence_length,
                                                                    padding='pre',
                                                                    truncating = 'pre')
    prediction = rnn_model.predict(tokenized_tweet)
    category = categories[np.squeeze(np.argmax(prediction, axis = -1))]
    return category

def get_processed_tweet(single_tweet):
    wnl = WordNetLemmatizer()

    ### Get the tokenizer's and model's parameters ###
    tokenizer_config_filename = os.path.join('.','tokenizer_config.json')
    model_params_filename = os.path.join('.','model_params.json')

    with open(tokenizer_config_filename) as file:
        # Load its content and make a new json string
        tokenizer_config_string = json.load(file)

    ### Get the tokenizer ###
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_config_string)

    ### Get the model's parameters, vocab_size and max_sentence_length ###
    with open(model_params_filename) as file:
        # Load its content and make a new json string
        model_params = json.load(file)
        
    vocab_size = model_params['vocab_size']
    max_sentence_length = model_params['max_sentence_length']

    ### Preprocess, tokenize and pad the tweet, then return it ###
    example_tweet = preprocess_single_tweet(single_tweet)
    tokenized_tweet = tokenizer.texts_to_sequences([example_tweet])
    tokenized_tweet = tf.keras.preprocessing.sequence.pad_sequences(tokenized_tweet,
                                                                    maxlen=max_sentence_length,
                                                                    padding='pre',
                                                                    truncating = 'pre')

    return tokenized_tweet

def get_rnn_model():
    load_model_flag = True    

    if load_model_flag:
        rnn_model = tf.keras.models.load_model('models/rnn_model_weights.h5')

    return rnn_model
