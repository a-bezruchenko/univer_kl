import nltk
import re
import random
from nltk.corpus import stopwords
from nltk import FreqDist
from pymystem3 import Mystem
import pandas as pd
from string import punctuation
# Для первого запуска
# nltk.download('averaged_perceptron_tagger_ru')
# nltk.download('punkt')
# nltk.download('stopwords')


# Нужно ускорить
def lemmatize_sentence(text):
    stop_words = stopwords.words('russian')
    mysteam = Mystem()
    tokens = mysteam.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in stop_words
              and token != " "
              and token.strip() not in punctuation]
    return tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def tokenizer(tweets):
    tweets_tokens = []
    for tweet in tweets:
        tweets_tokens.append(nltk.word_tokenize(tweet))
    return tweets_tokens


def get_tweet_for_model(cleaned_tokens_list):
    for tweet in cleaned_tokens_list:
        yield dict([token, True] for token in tweet)


if __name__ == '__main__':
    tt = []
    n = ['id', 'date', 'name', 'text', 'typr', 'rep', 'rtw', 'faw', 'stcount', 'foll', 'frien', 'listcount']
    positive_tweets = pd.read_csv('./data/positive.csv', sep=';', error_bad_lines=False, names=n)[:10]
    negative_tweets = pd.read_csv('./data/negative.csv', sep=';', error_bad_lines=False, names=n)[:10]

    positive_tweets_tokens = tokenizer(positive_tweets.text)
    negative_tweets_tokens = tokenizer(negative_tweets.text)

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweets.text:
        positive_cleaned_tokens_list.append(lemmatize_sentence(tokens))

    for tokens in negative_tweets.text:
        negative_cleaned_tokens_list.append(lemmatize_sentence(tokens))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweet_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweet_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)
    print(len(dataset))
