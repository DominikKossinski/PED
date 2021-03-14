import re
from copy import deepcopy

import nltk
from nltk.corpus import stopwords
import string

RE_SPACES = re.compile("\s+")
RE_HASHTAG = re.compile("[@#][_a-z0-9]+")
RE_EMOTICONS = re.compile("(:-?\))|(:p)|(:d+)|(:-?\()|(:/)|(;-?\))|(<3)|(=\))|(\)-?:)|(:'\()|(8\))")
RE_HTTP = re.compile("http(s)?://[/\.a-z0-9]+")
nltk.download('stopwords')

stop_words = stopwords.words('english')


class Tokenizer:

    @staticmethod
    def normalize(text):
        text = text.strip().lower()
        text = text.replace('\\n', ' ')
        text = text.replace('\\t', ' ')
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        text = text.replace('&pound;', u'£')
        text = text.replace('&euro;', u'€')
        text = text.replace('&copy;', u'©')
        text = text.replace('&reg;', u'®')
        return text

    @staticmethod
    def tokenize(text):
        text = re.sub(r'[^\x00-\x7f]', r'', text)

        text = Tokenizer.normalize(text)
        tokens = re.split(RE_SPACES, text)
        i = 0
        while i < len(tokens):
            token = tokens[i]
            match = any([re.match(RE_HASHTAG, token), re.match(RE_EMOTICONS, token), re.match(RE_HTTP, token)])
            if match:
                i += 1
            else:
                del tokens[i]
                for character in string.punctuation:
                    token = token.replace(character, '')
                if token:
                    tokens[i:i] = nltk.word_tokenize(token)
                    i += 1

        stemmer = nltk.SnowballStemmer("english", ignore_stopwords=False)
        tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
        return tokens
