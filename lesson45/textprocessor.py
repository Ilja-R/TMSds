import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string


class TextPreprocessor:
    def __init__(self, language='english', custom_stopwords=None):
        """
        Initialize the TextPreprocessor class with the specified language for stopwords.
        :param language: The language of stopwords to use (default is 'english').
        """
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('punkt_tab')

        self.stop_words = set(stopwords.words(language))
        if custom_stopwords:
            self.stop_words.update(custom_stopwords)
        self.lemmatizer = WordNetLemmatizer()
        self.punctuation = set(string.punctuation)

    def preprocess(self, text):
        """
        Preprocess the input text by lowering case, removing stopwords, and lemmatizing words.
        :param text: The text to preprocess.
        :return: A string containing the preprocessed text.
        """
        # Lowercase the text
        text = text.lower()

        # Tokenize the text
        words = word_tokenize(text)

        # Remove stopwords and lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words if
                 word.isalpha() and word.lower() not in self.stop_words]

        return ' '.join(words)