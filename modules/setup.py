import nltk
import warnings

def setup_nltk_resources():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

def suppress_warnings():
    warnings.filterwarnings("ignore")


if __name__ == "__main__":
    setup_nltk_resources()
    suppress_warnings()
