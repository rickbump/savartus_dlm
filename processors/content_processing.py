
import spacy
from textblob import TextBlob # can use TextBlob, VADER, TensorFlow and PyTorch for sentiment analysis
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake
import nltk
from nltk.tokenize import word_tokenize

#nltk.download('stopwords')
#nltk.download('punkt')

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")


# Named Entity Recognition (NER) using spaCy
def extract_named_entities(content):
    doc = nlp(content)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    unique_entities = list(set(entities))
    unique_entities = list(dict.fromkeys(unique_entities))
    unique_entities = sorted(list(set(unique_entities)))

    return unique_entities


# Sentiment Analysis using TextBlob
def analyze_sentiment(content):
    blob = TextBlob(content)
    sentiment = blob.sentiment
    return {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity
    }


# Keyword extraction using RAKE (Rapid Automatic Keyword Extraction)
def extract_keywords_rake(content):
    rake = Rake()
    rake.extract_keywords_from_text(content)
    keywords = rake.get_ranked_phrases()
    return keywords


# Keywords and phrases using TF-IDF (Term Frequency-Inverse Document Frequency)
def extract_keywords_tfidf(content):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([content])
    keywords = vectorizer.get_feature_names_out()
    return keywords


# Function to process text and extract metadata
def content_processing(body_text):
    try:
        #with open(file_path, 'r', encoding='utf-8') as file:
        #    content = file.read()

        # Named Entity Recognition (NER) using spaCy
        entities = extract_named_entities(body_text)

        # Sentiment Analysis using TextBlob
        sentiment = analyze_sentiment(body_text)

        # Keyword extraction using RAKE (Rapid Automatic Keyword Extraction)
        keywords_rake = extract_keywords_rake(body_text)

        # Keywords and phrases using TF-IDF (Term Frequency-Inverse Document Frequency)
        keywords_tfidf = extract_keywords_tfidf(body_text)

        # Creating metadata dictionary
        content_data = {
            'named_entities': entities,
            'sentiment': sentiment,
            'keywords_rake': keywords_rake,
            'keywords_tfidf': keywords_tfidf
        }
        return content_data
    except Exception as e:
        return {'error': str(e)}

#from nltk.tokenize import word_tokenize

#text = "This is a test sentence."
#tokens = word_tokenize(text)
#print(tokens)